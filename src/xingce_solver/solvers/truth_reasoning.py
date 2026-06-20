"""Isolated truth reasoning core for logic judgment questions.

This module implements a minimal structured truth reasoner for
"真假推理" (truth-falsehood reasoning) questions commonly found
in Chinese civil service exams (行测).

It is NOT integrated into solve_logic_reasoning. It is a standalone
engine for testing the core algorithm in isolation.

Version: v0.1
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Proposition:
    """Structured representation of a logical proposition."""
    kind: str  # atom, not, and, or, imply, all, some
    subject: str | None = None
    predicate: str | None = None
    left: Proposition | None = None
    right: Proposition | None = None
    negated: bool = False
    raw: str = ""


@dataclass(frozen=True)
class TruthConstraint:
    """How many statements must be true / false."""
    true_count: int | None = None
    false_count: int | None = None
    raw: str = ""


@dataclass
class TruthReasoningResult:
    """Result of the truth reasoning engine."""
    status: str  # solved / ambiguous / inconsistent / analysis_only
    facts: list[Proposition] = field(default_factory=list)
    assignments: list[dict[str, Any]] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Proposition constructors
# ---------------------------------------------------------------------------

def Atom(subject: str, predicate: str, negated: bool = False, raw: str = "") -> Proposition:
    # Clean up subject: remove leading discourse markers, action prefixes, and quotes
    subject = re.sub(r"^[则而就]+", "", subject).strip()
    subject = subject.strip("\"""''「」『』")
    # Strip action prefix if subject is short and predicate looks like a location/object
    if len(subject) <= 2 and re.match(r"^[去前往到了游]$", subject):
        subject = ""
    # Clean up predicate: strip discourse markers, action prefixes, copula, passive marker
    predicate = predicate.strip()
    predicate = re.sub(r"^[则而就]+", "", predicate).strip()
    predicate = _ACTION_PREFIXES.sub("", predicate).strip()
    predicate = re.sub(r"^(?:就?是|会|能|将|都|肯定|确定|必然|被)", "", predicate).strip()
    predicate = predicate.rstrip(_PUNCT_STRIP)
    # Auto-detect negation from predicate
    if "不" in predicate or "没" in predicate or "未" in predicate:
        if not negated:
            negated = True
        predicate = re.sub(r"^[不没未]+", "", predicate).strip()
        # Also strip passive marker and action prefix after negation removal
        predicate = re.sub(r"^被", "", predicate).strip()
        predicate = _ACTION_PREFIXES.sub("", predicate).strip()
    return Proposition(kind="atom", subject=subject, predicate=predicate, negated=negated, raw=raw)


def Not(inner: Proposition, raw: str = "") -> Proposition:
    return Proposition(kind="not", left=inner, raw=raw)


def And(left: Proposition, right: Proposition, raw: str = "") -> Proposition:
    return Proposition(kind="and", left=left, right=right, raw=raw)


def Or(left: Proposition, right: Proposition, raw: str = "") -> Proposition:
    return Proposition(kind="or", left=left, right=right, raw=raw)


def ExclusiveOne(left: Proposition, right: Proposition, raw: str = "") -> Proposition:
    """Exactly one of left/right is true (XOR semantics)."""
    return Proposition(kind="exactly_one", left=left, right=right, raw=raw)


def Imply(antecedent: Proposition, consequent: Proposition, raw: str = "") -> Proposition:
    return Proposition(kind="imply", left=antecedent, right=consequent, raw=raw)


def All(subject: str, predicate: str, negated: bool = False, raw: str = "") -> Proposition:
    return Proposition(kind="all", subject=subject, predicate=predicate, negated=negated, raw=raw)


def Some(subject: str, predicate: str, negated: bool = False, raw: str = "") -> Proposition:
    return Proposition(kind="some", subject=subject, predicate=predicate, negated=negated, raw=raw)


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

_ACTION_PREFIXES = re.compile(
    r"^(?:去了?|前往|到|游|游玩|参观|访问|去了?|到了?|去)"
)


def normalize_predicate(text: str) -> str:
    """Normalize a predicate string for matching.

    Strips action prefixes, copulas, passive markers, trailing punctuation.
    """
    text = text.strip()
    text = _ACTION_PREFIXES.sub("", text)
    text = re.sub(r"^(?:就?是|属于|为|被)", "", text).strip()
    text = re.sub(r"^(?:会|能|可以)", "", text).strip()
    # Handle negation + passive: 未被X → X, 不被X → X, 没有被X → X
    text = re.sub(r"^(?:未|不|没有|没)被?", "", text).strip()
    text = text.rstrip(_PUNCT_STRIP)
    return text


def normalize_atom_key(key: tuple) -> tuple:
    """Normalize an atom fact key for matching."""
    if key[0] != "atom":
        return key
    _, subj, pred, neg = key
    return ("atom", normalize_predicate(subj), normalize_predicate(pred), neg)


def _prop_to_normalized_key(p: Proposition) -> tuple | None:
    """Convert a proposition to a normalized fact key."""
    if p.kind == "atom":
        return normalize_atom_key(("atom", p.subject, p.predicate, p.negated))
    if p.kind == "all":
        return ("all", normalize_predicate(p.subject or ""), normalize_predicate(p.predicate or ""), p.negated)
    if p.kind == "some":
        return ("some", normalize_predicate(p.subject or ""), normalize_predicate(p.predicate or ""), p.negated)
    return None


# ---------------------------------------------------------------------------
# Binary complementary domains
# ---------------------------------------------------------------------------

def extract_binary_domains(question_text: str) -> list[tuple[str, str]]:
    """Extract binary complementary domain pairs from question text.

    Returns list of (A, B) pairs where ¬A ↔ B.
    Supports patterns like:
    - "有X和Y两种"
    - "不是X就是Y"
    - "要么X要么Y"
    """
    domains: list[tuple[str, str]] = []

    # "有X和Y两种"
    m = re.search(r"有(.+?)和(.+?)两种", question_text)
    if m:
        domains.append((m.group(1).strip(), m.group(2).strip()))

    # "不是X就是Y"
    m = re.search(r"不是(.+?)就是(.+?)(?:[，。；]|$)", question_text)
    if m:
        domains.append((m.group(1).strip(), m.group(2).strip()))

    # "要么X要么Y"
    m = re.search(r"要么(.+?)要么(.+?)(?:[，。；]|$)", question_text)
    if m:
        domains.append((m.group(1).strip(), m.group(2).strip()))

    # "X和Y二选一" / "X、Y二者必居其一"
    m = re.search(r"(.+?)[和、](.+?)(?:二选一|二者必居其一)", question_text)
    if m:
        domains.append((m.group(1).strip(), m.group(2).strip()))

    return domains


def _apply_binary_complement(
    facts: dict, domains: list[tuple[str, str]]
) -> dict:
    """Apply binary complement inference: if ¬A is known, derive B.

    Only applies when the domain pair is explicitly stated in the question.
    """
    new_facts = dict(facts)
    changed = True
    while changed:
        changed = False
        for a, b in domains:
            # Check if ¬A is in facts → derive B
            neg_a_key = ("atom", a, "", True)  # Atom(a, "", negated=True)
            pos_a_key = ("atom", a, "", False)  # Atom(a, "", negated=False)
            neg_b_key = ("atom", b, "", True)
            pos_b_key = ("atom", b, "", False)

            # If we know A is false, B must be true
            if neg_a_key in new_facts and new_facts[neg_a_key]:
                if pos_b_key not in new_facts:
                    new_facts[pos_b_key] = True
                    changed = True
            # If we know B is false, A must be true
            if neg_b_key in new_facts and new_facts[neg_b_key]:
                if pos_a_key not in new_facts:
                    new_facts[pos_a_key] = True
                    changed = True
            # If we know A is true, B must be false
            if pos_a_key in new_facts and new_facts[pos_a_key]:
                if neg_b_key not in new_facts:
                    new_facts[neg_b_key] = True
                    changed = True
            # If we know B is true, A must be false
            if pos_b_key in new_facts and new_facts[pos_b_key]:
                if neg_a_key not in new_facts:
                    new_facts[neg_a_key] = True
                    changed = True

    return new_facts


# ---------------------------------------------------------------------------
# Universal instantiation
# ---------------------------------------------------------------------------

def _extract_known_entities(statements: list[Proposition | None]) -> dict[str, set[str]]:
    """Extract known entities that belong to universal categories.

    Looks for patterns like:
    - All("S", "P") and Atom("x", "P") → x might be an instance of S
    - Statements about specific entities in a group context
    """
    entities: dict[str, set[str]] = {}  # category -> set of entities

    # Find all All statements
    all_categories: set[str] = set()
    for prop in statements:
        if prop and prop.kind == "all":
            all_categories.add(prop.subject or "")

    # Find all Atom statements with subjects that could be instances
    for prop in statements:
        if prop and prop.kind == "atom" and prop.subject:
            subj = prop.subject
            # If the subject is a short name (1-3 chars) and there are All categories,
            # it might be an instance
            if len(subj) <= 3 and all_categories:
                for cat in all_categories:
                    if cat not in entities:
                        entities[cat] = set()
                    entities[cat].add(subj)

    return entities


def _instantiate_universal_facts(
    facts: dict, known_entities: dict[str, set[str]]
) -> dict:
    """Instantiate All(S, P) facts to known entities of S."""
    new_facts = dict(facts)
    changed = True
    while changed:
        changed = False
        for key, val in list(new_facts.items()):
            if key[0] != "all" or not val:
                continue
            _, category, predicate, negated = key
            if category not in known_entities:
                continue
            for entity in known_entities[category]:
                atom_key = ("atom", entity, predicate, negated)
                if atom_key not in new_facts:
                    new_facts[atom_key] = val
                    changed = True
    return new_facts


# ---------------------------------------------------------------------------
# Negation
# ---------------------------------------------------------------------------

def negate_proposition(p: Proposition) -> Proposition:
    """Return the logical negation of p."""
    if p.kind == "atom":
        return Atom(p.subject, p.predicate, negated=not p.negated, raw=f"¬({p.raw})")
    if p.kind == "not":
        return p.left  # double negation
    if p.kind == "and":
        return Or(negate_proposition(p.left), negate_proposition(p.right), raw=f"¬({p.raw})")
    if p.kind == "or":
        return And(negate_proposition(p.left), negate_proposition(p.right), raw=f"¬({p.raw})")
    if p.kind == "imply":
        return And(p.left, negate_proposition(p.right), raw=f"¬({p.raw})")
    if p.kind == "all":
        return Some(p.subject, p.predicate, negated=not p.negated, raw=f"¬({p.raw})")
    if p.kind == "some":
        return All(p.subject, p.predicate, negated=not p.negated, raw=f"¬({p.raw})")
    if p.kind == "exactly_one":
        # ¬(exactly_one(A,B)) = (A∧B) ∨ (¬A∧¬B)
        both = And(p.left, p.right)
        neither = And(negate_proposition(p.left), negate_proposition(p.right))
        return Or(both, neither, raw=f"¬({p.raw})")
    return Not(p, raw=f"¬({p.raw})")


# ---------------------------------------------------------------------------
# Contradiction detection
# ---------------------------------------------------------------------------

def are_contradictory(a: Proposition, b: Proposition) -> bool:
    """Check if a and b are direct logical contradictions."""
    # Not(a) contradicts a
    if a.kind == "not" and a.left == b:
        return True
    if b.kind == "not" and b.left == a:
        return True
    # Atom: same subject/predicate, opposite polarity
    if a.kind == "atom" and b.kind == "atom":
        if a.subject == b.subject and a.predicate == b.predicate and a.negated != b.negated:
            return True
    # All vs Some with opposite polarity
    if a.kind == "all" and b.kind == "some":
        if a.subject == b.subject and a.predicate == b.predicate and a.negated != b.negated:
            return True
    if a.kind == "some" and b.kind == "all":
        if a.subject == b.subject and a.predicate == b.predicate and a.negated != b.negated:
            return True
    # P->Q vs P且¬Q
    if a.kind == "imply" and b.kind == "and":
        if b.left == a.left and are_contradictory(a.right, b.right):
            return True
    if b.kind == "imply" and a.kind == "and":
        if a.left == b.left and are_contradictory(b.right, a.right):
            return True
    # De Morgan: P且Q vs ¬P或¬Q
    if a.kind == "and" and b.kind == "or":
        if (are_contradictory(a.left, b.left) and are_contradictory(a.right, b.right)):
            return True
        if (are_contradictory(a.left, b.right) and are_contradictory(a.right, b.left)):
            return True
    if a.kind == "or" and b.kind == "and":
        if (are_contradictory(a.left, b.left) and are_contradictory(a.right, b.right)):
            return True
        if (are_contradictory(a.left, b.right) and are_contradictory(a.right, b.left)):
            return True
    return False


# ---------------------------------------------------------------------------
# Parsing: truth constraint
# ---------------------------------------------------------------------------

_CONSTRAINT_PATTERNS = [
    # "只有一人说的不对" / "只有一个人说假话"
    (re.compile(r"只有([一二三四五六七八九十1-9])个?(?:位|名)?人?[说讲]的?[不没]?对"), "false_count"),
    (re.compile(r"只有([一二三四五六七八九十1-9])个?(?:位|名)?人?说假?话"), "false_count"),
    # "只有一人说的对" / "只有一位的看法是正确的"
    (re.compile(r"只有([一二三四五六七八九十1-9])个?(?:位|名)?人?[说讲]的?对"), "true_count"),
    (re.compile(r"只有([一二三四五六七八九十1-9])个?(?:位|名)?人?说真话"), "true_count"),
    # "只有一位教练的预测是正确的" / "只有一位的看法是正确的" / "只有一人的猜测正确"
    (re.compile(r"只有([一二三四五六七八九十1-9])个?(?:位|名)?(?:人|教练|老师|专家|柜子|线索)?(?:的)?(?:预测|看法|猜测|观点|判断|描述)?[是]?正确的?"), "true_count"),
    (re.compile(r"只有([一二三四五六七八九十1-9])个?(?:位|名)?(?:人|教练|老师|专家|柜子|线索)?(?:的)?(?:预测|看法|猜测|观点|判断|描述)?正确"), "true_count"),
    # "只有一个柜子里的描述是真实的"
    (re.compile(r"只有([一二三四五六七八九十1-9])个?(?:位|名)?[一-鿿]*(?:的)?(?:预测|看法|猜测|观点|判断|描述)[是]?[真假]的?"), "true_count"),
    # "三条线索只有一条是假的" — X中只有一Y是假的
    (re.compile(r"[一二三四五六七八九十1-9][一-鿿]*[中里]?只有([一二三四五六七八九十1-9])[一-鿿]*[是]?假的?"), "false_count"),
    (re.compile(r"[一二三四五六七八九十1-9][一-鿿]*[中里]?只有([一二三四五六七八九十1-9])[一-鿿]*[是]?真的?"), "true_count"),
    # "只有一条是假的" (without preceding context)
    (re.compile(r"只有([一二三四五六七八九十1-9])[一-鿿]*[是]?假的?"), "false_count"),
    (re.compile(r"只有([一二三四五六七八九十1-9])[一-鿿]*[是]?真的?"), "true_count"),
    # "只有一人预测为真" / "只有一人预测是真"
    (re.compile(r"只有([一二三四五六七八九十1-9])个?(?:位|名)?人?(?:预测|猜测|判断)?[是为]?真"), "true_count"),
    # "四人中二人说了假话"
    (re.compile(r"[一二三四五六七八九十1-9]人?[中里]有?([一二三四五六七八九十1-9])人?[说讲]了假话"), "explicit_false"),
    # "四人中二人说了真话"
    (re.compile(r"[一二三四五六七八九十1-9]人?[中里]有?([一二三四五六七八九十1-9])人?[说讲]了真话"), "explicit_true"),
    # "四句话中有三句是真的，一句是假的"
    (re.compile(r"有?([一二三四五六七八九十1-9])句[是]?真的[，,]?有?([一二三四五六七八九十1-9])句[是]?假的?"), "true_false_explicit"),
    # "二真二假" / "三真一假"
    (re.compile(r"([一二三四五六七八九十1-9])真([一二三四五六七八九十1-9])假"), "true_false"),
    # "一真两假" etc.
    (re.compile(r"一真两假|1真2假"), "tf_1_2"),
    (re.compile(r"两真一假|2真1假"), "tf_2_1"),
    (re.compile(r"三真一假|3真1假"), "tf_3_1"),
    # "都是假的" / "都没有"
    (re.compile(r"[都均]是假的|全[部都均]假|都没[有]?"), "all_false"),
    # "四人中只有一人说的不对"
    (re.compile(r"[一二三四五六七八九十1-9]人?[中里]只有([一二三四五六七八九十1-9])人?[说讲]的?[不没]?对"), "explicit_false"),
    (re.compile(r"[一二三四五六七八九十1-9]人?[中里]只有([一二三四五六七八九十1-9])人?[说讲]的?对"), "explicit_true"),
    # "只有一真" / "只有一假"
    (re.compile(r"只有([一二三四五六七八九十1-9])[真假]"), "one_true"),
    (re.compile(r"一个[是]?真"), "one_true"),
    (re.compile(r"一个[是]?假"), "one_false"),
]

_CN_DIGIT = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def _parse_digit(s: str) -> int:
    """Parse a Chinese or Arabic digit."""
    if s in _CN_DIGIT:
        return _CN_DIGIT[s]
    return int(s)


def parse_truth_constraint(text: str) -> TruthConstraint:
    """Extract truth constraint from question text."""
    for pattern, kind in _CONSTRAINT_PATTERNS:
        m = pattern.search(text)
        if not m:
            continue
        if kind == "false_count":
            n = _parse_digit(m.group(1))
            return TruthConstraint(false_count=n, raw=m.group())
        if kind == "true_count":
            n = _parse_digit(m.group(1))
            return TruthConstraint(true_count=n, raw=m.group())
        if kind == "true_count_explicit":
            return TruthConstraint(true_count=_parse_digit(m.group(2)), raw=m.group())
        if kind == "true_false":
            return TruthConstraint(true_count=_parse_digit(m.group(1)), false_count=_parse_digit(m.group(2)), raw=m.group())
        if kind == "true_false_explicit":
            return TruthConstraint(true_count=_parse_digit(m.group(1)), false_count=_parse_digit(m.group(2)), raw=m.group())
        if kind == "tf_1_2":
            return TruthConstraint(true_count=1, false_count=2, raw=m.group())
        if kind == "tf_2_1":
            return TruthConstraint(true_count=2, false_count=1, raw=m.group())
        if kind == "tf_3_1":
            return TruthConstraint(true_count=3, false_count=1, raw=m.group())
        if kind == "all_false":
            return TruthConstraint(false_count=-1, raw=m.group())  # -1 = all
        if kind == "explicit_false":
            falses = _parse_digit(m.group(1))
            return TruthConstraint(false_count=falses, raw=m.group())
        if kind == "explicit_true":
            trues = _parse_digit(m.group(1))
            return TruthConstraint(true_count=trues, raw=m.group())
        if kind == "one_true":
            return TruthConstraint(true_count=1, raw=m.group())
        if kind == "one_false":
            return TruthConstraint(false_count=1, raw=m.group())
    return TruthConstraint(raw="")


# ---------------------------------------------------------------------------
# Parsing: proposition from text
# ---------------------------------------------------------------------------

_PUNCT_STRIP = "，,。；;：:"


def _clean_atom(p: Proposition) -> Proposition:
    """Strip trailing punctuation from atom subjects and predicates."""
    if p.kind == "atom":
        subj = (p.subject or "").strip().rstrip(_PUNCT_STRIP)
        pred = (p.predicate or "").strip().rstrip(_PUNCT_STRIP)
        if subj != p.subject or pred != p.predicate:
            return Atom(subj, pred, negated=p.negated, raw=p.raw)
    return p

def parse_statement(text: str) -> Proposition | None:
    """Parse a single statement into a structured Proposition.

    Handles common Chinese logical patterns:
    - 如果P那么Q / 只要P就Q → Imply(P, Q)
    - 只有P才Q → Imply(Q, P)
    - 除非P否则Q → Imply(¬Q, P)  [unless Q then P]
    - P或Q / 或者P或者Q → Or(P, Q)
    - P且Q / P和Q / P但Q → And(P, Q)
    - 所有S是P / 所有S都是P → All(S, P)
    - 所有S不是P → All(S, P, negated=True)
    - 有的S是P / 有些S是P → Some(S, P)
    - 有的S不是P → Some(S, P, negated=True)
    - S不是P / S没有P → Atom(S, P, negated=True)
    - S是P → Atom(S, P)
    """
    text = text.strip()
    if not text:
        return None

    # --- Imply: 只有P才Q → Q→P ---
    m = re.search(r"只有(.+?)才(.+)", text)
    if m:
        p = parse_statement(m.group(1).strip())
        q = parse_statement(m.group(2).strip())
        if p and q:
            return Imply(q, p, raw=text)

    # --- Imply: 除非P否则Q → ¬Q→P ---
    m = re.search(r"除非(.+?)(?:否则|不然)(.+)", text)
    if m:
        p = parse_statement(m.group(1).strip())
        q = parse_statement(m.group(2).strip())
        if p and q:
            return Imply(negate_proposition(q), p, raw=text)

    # --- Imply: 如果/若/只要P那么/则/就Q ---
    m = re.search(r"(?:如果|若|只要)(.+?)(?:[,，]?\s*那么|则|就|，)(.+)", text)
    if m:
        p = parse_statement(m.group(1).strip())
        q = parse_statement(m.group(2).strip())
        if p and q:
            return Imply(_clean_atom(p), _clean_atom(q), raw=text)

    # --- Or: 或者P或者Q / P或Q ---
    m = re.search(r"(?:或者)?(.+?)(?:或者|或)(.+)", text)
    if m:
        p = parse_statement(m.group(1).strip())
        q = parse_statement(m.group(2).strip())
        if p and q:
            return Or(_clean_atom(p), _clean_atom(q), raw=text)

    # --- ExclusiveOne: A和B去一个就好 / A、B只去一个 / A和B二选一 ---
    # These patterns indicate exactly-one semantics
    m = re.search(r"([^和且、]+?)(?:和|且|、)([^去只二选不]+?)(?:去一个就好|只去一个|二选一|只能选一个|不能都去|不能同时去)", text)
    if m:
        subj1 = m.group(1).strip()
        subj2 = m.group(2).strip()
        p = Atom("", subj1, raw=subj1)
        q = Atom("", subj2, raw=subj2)
        return ExclusiveOne(p, q, raw=text)

    # "要么A要么B"
    m = re.search(r"要么(.+?)要么(.+?)(?:[，。；]|$)", text)
    if m:
        p = Atom("", m.group(1).strip(), raw=m.group(1).strip())
        q = Atom("", m.group(2).strip(), raw=m.group(2).strip())
        return ExclusiveOne(p, q, raw=text)

    # "不是A就是B"
    m = re.search(r"不是(.+?)就是(.+?)(?:[，。；]|$)", text)
    if m:
        p = Atom("", m.group(1).strip(), raw=m.group(1).strip())
        q = Atom("", m.group(2).strip(), raw=m.group(2).strip())
        return ExclusiveOne(p, q, raw=text)

    # --- And: P且Q / P和Q / P但Q / P，Q都 / P、Q都 ---
    # Handle "A和B+classifier+均/都+P" (e.g., "戊和己两所高校均未中标")
    m = re.search(r"([^和且、]+?)(?:和|且|、)([^和且、]+?)(?:[两几数]?[所个名位条]?[一-鿿]*?)(?:均|都)(.+)", text)
    if m:
        subj1 = m.group(1).strip()
        subj2 = m.group(2).strip()
        pred = m.group(3).strip()
        pred_clean = re.sub(r"^不是|是", "", pred).strip()
        neg = "不" in pred or "没" in pred or "未" in pred
        p = Atom(subj1, pred_clean, negated=neg, raw=subj1 + pred)
        q = Atom(subj2, pred_clean, negated=neg, raw=subj2 + pred)
        return And(p, q, raw=text)

    # Handle "P和Q都不是R" / "P和Q都是R" / "P、Q都是R" (where 都 comes before the predicate)
    # Use greedy match for first subject to capture full compound words
    m = re.search(r"([^和且、]+)(?:和|且|、)([一-鿿]+?)(?:都)(.+)", text)

    if m:
        subj1 = m.group(1).strip()
        subj2 = m.group(2).strip()
        pred = m.group(3).strip()
        # Strip copula from predicate
        pred_clean = re.sub(r"^不是|是", "", pred).strip()
        neg = "不" in pred or "没" in pred
        p = Atom(subj1, pred_clean, negated=neg, raw=subj1 + pred)
        q = Atom(subj2, pred_clean, negated=neg, raw=subj2 + pred)
        return And(p, q, raw=text)

    # Handle "P和Q是/不是R" / "P、Q是/不是R" (without 都)
    m = re.search(r"([一-鿿]+)(?:和|且|、)([一-鿿]+)((?:不是|是).+)", text)
    if m:
        subj1 = m.group(1).strip()
        subj2 = m.group(2).strip()
        pred = m.group(3).strip()
        pred_clean = re.sub(r"^不是|是", "", pred).strip()
        neg = "不是" in pred
        p = Atom(subj1, pred_clean, negated=neg, raw=subj1 + pred)
        q = Atom(subj2, pred_clean, negated=neg, raw=subj2 + pred)
        return And(p, q, raw=text)

    m = re.search(r"(.+?)(?:且|和|但是?|，)(.+?)(?:都|$)", text)
    if m:
        p = parse_statement(m.group(1).strip())
        q = parse_statement(m.group(2).strip().rstrip("都"))
        if p and q:
            return And(p, q, raw=text)

    # --- All: 所有S是/都是P / 所有S都P ---
    m = re.search(r"所有(.+?)(?:都是|是|都)(.+)", text)
    if m:
        subj = m.group(1).strip()
        pred = m.group(2).strip()
        if "不是" in pred or "没" in pred or "不会" in pred:
            pred_clean = pred.replace("不是", "").replace("没有", "").replace("不会", "").strip()
            return All(subj, pred_clean, negated=True, raw=text)
        return All(subj, pred, raw=text)

    # --- Some: 有的/有些S是/不是P ---
    m = re.search(r"(?:有的|有些)(.+?)(?:是|不是|没有)(.+)", text)
    if m:
        subj = m.group(1).strip()
        pred = m.group(2).strip()
        full = m.group()
        if "不是" in full or "没有" in full:
            return Some(subj, pred, negated=True, raw=text)
        return Some(subj, pred, raw=text)

    # --- Atom with negation: S不是P / S没P / S没有P / S不会P ---
    m = re.search(r"(.+?)(?:不是|没有|没|不会|不能|不可)(.+)", text)
    if m:
        subj = m.group(1).strip()
        pred = m.group(2).strip()
        # Clean up subject
        subj = re.sub(r"^[则而就]+|[则而就]+$", "", subj).strip()
        subj = re.sub(r"(?:肯定|确定)$", "", subj).strip()
        pred = pred.rstrip(_PUNCT_STRIP)
        # Avoid matching "所有...不是" which is handled above
        if subj and not re.match(r"所有|有的|有些", subj):
            return Atom(subj, pred, negated=True, raw=text)

    # --- Atom: S是P / S就是P / S会P / S能P / S将P ---
    # Use negative lookbehind to avoid matching "则" or "就" after punctuation
    m = re.search(r"(?<![则而])(.+?)(?:就?是|会|能|将|都|肯定|确定|必然)(.+)", text)
    if m:
        subj = m.group(1).strip()
        pred = m.group(2).strip()
        # Clean up subject: remove leading 则/而/就, trailing 肯定/确定
        subj = re.sub(r"^[则而就]+|[则而就]+$", "", subj).strip()
        subj = re.sub(r"(?:肯定|确定)$", "", subj).strip()
        # Clean up predicate: remove trailing punctuation
        pred = pred.rstrip("，,。；;：:")
        if subj and not re.match(r"所有|有的|有些|如果|若|只要|只有|除非", subj):
            return Atom(subj, pred, raw=text)

    # --- Bare atom (no explicit copula) ---
    # Only match single-char subjects to avoid splitting compound words
    # Skip if text contains 和/且/、/或 (should be handled by And/Or pattern)
    if not re.search(r"[和且、或]", text):
        m = re.match(r"^([一-鿿])(.+)$", text)
        if m:
            subj = m.group(1)
            pred = m.group(2)
            if not re.match(r"所有|有的|有些|如果|若|只要|只有|除非|本|该|这|那", subj):
                return _clean_atom(Atom(subj, pred, raw=text))
        # Try 2-char subject for words like "本柜子"
        m = re.match(r"^([一-鿿]{2,4})(.+)$", text)
        if m:
            subj = m.group(1)
            pred = m.group(2)
            if not re.match(r"所有|有的|有些|如果|若|只要|只有|除非", subj):
                return _clean_atom(Atom(subj, pred, raw=text))

    return None


# ---------------------------------------------------------------------------
# Parsing: extract statements from question text
# ---------------------------------------------------------------------------

def extract_statements(question_text: str) -> list[dict[str, Any]]:
    """Extract individual statements from question text.

    Returns list of dicts: {"index": int, "speaker": str|None, "text": str}
    """
    results: list[dict[str, Any]] = []
    idx = 0

    # --- Pattern 1: ①②③ ---
    num_re = re.compile(r"[①②③④⑤⑥⑦⑧⑨⑩]")
    if num_re.search(question_text):
        parts = num_re.split(question_text)
        for part in parts[1:]:
            s = re.split(r"[。；]", part)[0].strip()
            if s and len(s) > 1:
                results.append({"index": idx, "speaker": None, "text": s})
                idx += 1
        if results:
            return results

    # --- Pattern 2: (1)(2)(3) / （1）（2）（3） ---
    paren_re = re.compile(r"[（(]\s*\d\s*[）)]")
    if paren_re.search(question_text):
        parts = paren_re.split(question_text)
        for part in parts[1:]:
            s = re.split(r"[。；]", part)[0].strip()
            if s and len(s) > 1:
                results.append({"index": idx, "speaker": None, "text": s})
                idx += 1
        if results:
            return results

    # --- Pattern 3: X说：Y ---
    _constraint_speaker_skip = re.compile(
        r"只有|所有|有人|没有|四人|三人|二人|一人|四句|三句|二句|一句|"
        r"四条|三条|二条|一条|四名|三名|二名|一名|"
        r"中只有|中有|中二|中三|中四|下肯定"
    )
    # Common non-speaker words that appear before "说" in introductory text
    _noise_speaker_skip = re.compile(
        r"^[队绩子测果员案子物绩行集训日测]$|"
        r"^期|^员|^队|^测|^果|^案|^物|^绩|^行|^集|^训|^日|^下|^几|^经|^调"
    )

    # 3a: Multi-char speakers (2-4 chars)
    speaker_re = re.compile(
        r"([一-鿿]{2,4}(?:某|教练|老师|专家|柜子)?)\s*[说道讲认为]\s*[：:]?\s*(.+?)"
        r"(?=[一-鿿]{2,4}(?:某|教练|老师|专家|柜子)?\s*[说道讲认为]\s*[：:]|$)"
    )
    for m in speaker_re.finditer(question_text):
        speaker = m.group(1).strip()
        if _constraint_speaker_skip.search(speaker):
            continue
        if _noise_speaker_skip.match(speaker):
            continue
        statement = m.group(2).strip()
        statement = re.split(r"[。；]", statement)[0].strip()
        for ch in ['"', '"', '「', '」', '『', '』', '"', '"']:
            statement = statement.strip(ch)
        if statement and len(statement) > 1:
            results.append({"index": idx, "speaker": speaker, "text": statement})
            idx += 1

    # 3b: Single-char speakers (甲说, 乙说, etc.)
    if not results:
        single_char_re = re.compile(
            r"([一-鿿])\s*说\s*[：:]?\s*(.+?)"
            r"(?=[一-鿿]\s*说\s*[：:]|$)"
        )
        for m in single_char_re.finditer(question_text):
            speaker = m.group(1).strip()
            statement = m.group(2).strip()
            statement = re.split(r"[。；]", statement)[0].strip()
            for ch in ['"', '"', '「', '」', '『', '』', '"', '"']:
                statement = statement.strip(ch)
            if statement and len(statement) > 1:
                results.append({"index": idx, "speaker": speaker, "text": statement})
                idx += 1

    if results:
        return results

    # --- Pattern 4: X写着/Y写着 (labels, cabinets, boxes, etc.) ---
    # "第一个柜子里写着：'...'" / "第二个标签写着：'...'" / "某处写着：'...'"
    xiezhe_re = re.compile(
        r"([一-鿿]*?(?:个|处|块|张|条)?[一-鿿]*?(?:里|上|中)?(?:都?)?写着)\s*[：:]?\s*['\"]?\s*(.+?)\s*['\"]?\s*(?=[，,。；]|$)"
    )
    for m in xiezhe_re.finditer(question_text):
        speaker = m.group(1).strip()
        statement = m.group(2).strip()
        statement = re.split(r"[。；]", statement)[0].strip()
        for ch in ['"', '"', '「', '」', '『', '』', '"', '"', "'", "'"]:
            statement = statement.strip(ch)
        if statement and len(statement) > 1:
            results.append({"index": idx, "speaker": speaker, "text": statement})
            idx += 1

    if results:
        return results

    # Fallback: sentence split (skip constraint and question parts)
    constraint = parse_truth_constraint(question_text)
    constraint_end = 0
    if constraint.raw:
        pos = question_text.find(constraint.raw)
        if pos != -1:
            constraint_end = pos + len(constraint.raw)

    question_markers = ["由此可以推出", "由此推出", "则下列", "以下哪项", "以下肯定", "那么下列"]
    q_pos = len(question_text)
    for marker in question_markers:
        p = question_text.find(marker, constraint_end)
        if p != -1 and p < q_pos:
            q_pos = p

    body = question_text[constraint_end:q_pos]
    sentences = re.split(r"[。；]", body)
    for s in sentences:
        s = s.strip()
        if len(s) > 4:
            results.append({"index": idx, "speaker": None, "text": s})
            idx += 1

    return results


# ---------------------------------------------------------------------------
# Fact tracking and consistency checking
# ---------------------------------------------------------------------------

def _add_fact(facts: dict, key: tuple, value: bool, warnings: list[str]) -> bool:
    """Add a fact. Returns False if contradiction detected."""
    if key in facts:
        if facts[key] != value:
            return False
    else:
        facts[key] = value
    return True


def _prop_to_fact_key(p: Proposition) -> tuple | None:
    """Convert a proposition to a hashable fact key, or None if not atomic."""
    if p.kind == "atom":
        return ("atom", p.subject, p.predicate, p.negated)
    if p.kind == "not" and p.left.kind == "atom":
        inner = p.left
        return ("atom", inner.subject, inner.predicate, not inner.negated)
    if p.kind == "all":
        return ("all", p.subject, p.predicate, p.negated)
    if p.kind == "some":
        return ("some", p.subject, p.predicate, p.negated)
    return None


def _check_contradiction_in_facts(facts: dict) -> bool:
    """Check if facts contain contradictions."""
    atoms: dict[tuple, bool] = {}
    for key, val in facts.items():
        if key[0] == "atom":
            k = (key[1], key[2])  # (subject, predicate)
            effective = val if not key[3] else not val  # account for negated
            if k in atoms and atoms[k] != effective:
                return True
            atoms[k] = effective

    alls: dict[tuple, bool] = {}
    somes: dict[tuple, bool] = {}
    for key, val in facts.items():
        if key[0] == "all":
            alls[(key[1], key[2])] = val if not key[3] else not key[3]
        if key[0] == "some":
            somes[(key[1], key[2])] = val if not key[3] else not key[3]

    for k in alls:
        if k in somes:
            if alls[k] and not somes[k]:
                return True
            if not alls[k] and somes[k]:
                return True

    return False


def _definitely_true(p: Proposition, facts: dict) -> bool | None:
    """Check if p is definitely true/false given facts. None = uncertain."""
    if p.kind == "atom":
        key = ("atom", p.subject, p.predicate, p.negated)
        if key in facts:
            return facts[key]
        # Check opposite polarity: if we know S is P, then S is not P is False
        opp_key = ("atom", p.subject, p.predicate, not p.negated)
        if opp_key in facts:
            return not facts[opp_key]
        return None

    if p.kind == "not":
        inner = _definitely_true(p.left, facts)
        if inner is None:
            return None
        return not inner

    if p.kind == "and":
        l = _definitely_true(p.left, facts)
        r = _definitely_true(p.right, facts)
        if l is False or r is False:
            return False
        if l is True and r is True:
            return True
        return None

    if p.kind == "or":
        l = _definitely_true(p.left, facts)
        r = _definitely_true(p.right, facts)
        if l is True or r is True:
            return True
        if l is False and r is False:
            return False
        return None

    if p.kind == "imply":
        a = _definitely_true(p.left, facts)
        c = _definitely_true(p.right, facts)
        if a is True and c is False:
            return False
        if a is False:
            return True
        if c is True:
            return True
        return None

    if p.kind == "all":
        return _definitely_true(Atom(p.subject, p.predicate, p.negated), facts)

    if p.kind == "some":
        return _definitely_true(Atom(p.subject, p.predicate, p.negated), facts)

    return None


def _extract_facts_from_prop(p: Proposition, val: bool, facts: dict, warnings: list[str]) -> bool:
    """Extract atomic facts from a proposition being val (True/False).
    Returns False if contradiction detected."""
    key = _prop_to_fact_key(p)
    if key is not None:
        return _add_fact(facts, key, val, warnings)

    # For compound propositions, derive what we can
    if val:
        # True proposition: check consistency, then derive entailed facts
        result = _definitely_true(p, facts)
        if result is False:
            return False

        # Imply(P, Q) true + P true → Q true
        if p.kind == "imply":
            ant_true = _definitely_true(p.left, facts)
            if ant_true is True:
                if not _extract_facts_from_prop(p.right, True, facts, warnings):
                    return False

        # Or(P, Q) true + ¬P true → Q true (disjunctive syllogism)
        if p.kind == "or":
            left_false = _definitely_true(p.left, facts)
            if left_false is False:
                if not _extract_facts_from_prop(p.right, True, facts, warnings):
                    return False
            right_false = _definitely_true(p.right, facts)
            if right_false is False:
                if not _extract_facts_from_prop(p.left, True, facts, warnings):
                    return False
            # Also check negated forms
            neg_left_key = _prop_to_fact_key(negate_proposition(p.left))
            if neg_left_key and neg_left_key in facts and facts[neg_left_key]:
                if not _extract_facts_from_prop(p.right, True, facts, warnings):
                    return False
            neg_right_key = _prop_to_fact_key(negate_proposition(p.right))
            if neg_right_key and neg_right_key in facts and facts[neg_right_key]:
                if not _extract_facts_from_prop(p.left, True, facts, warnings):
                    return False

        # And(P, Q) true → P true and Q true
        if p.kind == "and":
            if not _extract_facts_from_prop(p.left, True, facts, warnings):
                return False
            if not _extract_facts_from_prop(p.right, True, facts, warnings):
                return False
    else:
        # False proposition: its negation is true
        result = _definitely_true(p, facts)
        if result is True:
            return False

        # Imply(P, Q) false → P true and Q false
        if p.kind == "imply":
            if not _extract_facts_from_prop(p.left, True, facts, warnings):
                return False
            if not _extract_facts_from_prop(p.right, False, facts, warnings):
                return False

        # And(P, Q) false → at least one of P, Q is false
        # We can't determine which, but check if we already know
        if p.kind == "and":
            left_true = _definitely_true(p.left, facts)
            right_true = _definitely_true(p.right, facts)
            if left_true is True and right_true is True:
                return False  # Both true → And can't be false

        # Or(P, Q) false → P false and Q false
        if p.kind == "or":
            if not _extract_facts_from_prop(p.left, False, facts, warnings):
                return False
            if not _extract_facts_from_prop(p.right, False, facts, warnings):
                return False

    return True


def _evaluate_true(p: Proposition, facts: dict) -> bool:
    """Evaluate if a true proposition is consistent with facts."""
    if p.kind == "atom":
        key = ("atom", p.subject, p.predicate, p.negated)
        if key in facts and not facts[key]:
            return False
        return True

    if p.kind == "not":
        inner_true = _definitely_true(p.left, facts)
        if inner_true is True:
            return False
        return True

    if p.kind == "and":
        return _evaluate_true(p.left, facts) and _evaluate_true(p.right, facts)

    if p.kind == "or":
        l = _definitely_true(p.left, facts)
        r = _definitely_true(p.right, facts)
        if l is False and r is False:
            return False
        return True

    if p.kind == "imply":
        a = _definitely_true(p.left, facts)
        c = _definitely_true(p.right, facts)
        if a is True and c is False:
            return False
        return True

    if p.kind == "all":
        return _evaluate_true(Atom(p.subject, p.predicate, p.negated), facts)

    if p.kind == "some":
        return _evaluate_true(Atom(p.subject, p.predicate, p.negated), facts)

    return True


def _evaluate_false(p: Proposition, facts: dict) -> bool:
    """Evaluate if a false proposition (i.e. ¬p is true) is consistent with facts."""
    if p.kind == "atom":
        key = ("atom", p.subject, p.predicate, not p.negated)
        if key in facts and not facts[key]:
            return False
        return True

    if p.kind == "not":
        inner_true = _definitely_true(p.left, facts)
        if inner_true is False:
            return False
        return True

    if p.kind == "and":
        l = _definitely_true(p.left, facts)
        r = _definitely_true(p.right, facts)
        if l is True and r is True:
            return False
        return True

    if p.kind == "or":
        return _evaluate_false(p.left, facts) and _evaluate_false(p.right, facts)

    if p.kind == "imply":
        a = _definitely_true(p.left, facts)
        c = _definitely_true(p.right, facts)
        if a is True and c is False:
            return True  # P→Q false when P true, Q false: consistent
        if a is True and c is not False:
            return False  # Can't have P→Q false if Q might be true
        return True

    if p.kind == "all":
        return _evaluate_false(Atom(p.subject, p.predicate, p.negated), facts)

    if p.kind == "some":
        return _evaluate_false(Atom(p.subject, p.predicate, p.negated), facts)

    return True


# ---------------------------------------------------------------------------
# Option mapping
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OptionClaim:
    """A parsed answer option."""
    label: str  # A, B, C, D
    proposition: Proposition | None = None
    raw: str = ""


@dataclass
class OptionMappingResult:
    """Result of mapping options to assignment facts."""
    option_status: str  # unique_supported / ambiguous_options / no_supported_option / not_attempted
    selected_label: str | None = None
    option_trace: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def extract_options(question_text: str) -> list[OptionClaim]:
    """Extract A/B/C/D options from question text.

    Handles patterns like:
    - A. text / A、text / A：text
    - A. text B. text C. text D. text
    """
    options: list[OptionClaim] = []
    # Match A/B/C/D followed by punctuation and text
    pattern = re.compile(
        r"([A-D])\s*[.、:：]\s*(.+?)(?=\s*[A-D]\s*[.、:：]|$)",
        re.DOTALL
    )
    for m in pattern.finditer(question_text):
        label = m.group(1)
        text = m.group(2).strip()
        # Clean up: remove trailing whitespace, newlines, next option markers
        text = re.split(r"\s*[A-D]\s*[.、:：]", text)[0].strip()
        text = text.rstrip("。；;，,")
        if text:
            options.append(OptionClaim(label=label, raw=text))

    return options


def parse_option_text(text: str) -> Proposition | None:
    """Parse option text into a structured Proposition.

    Handles:
    - "A是P" / "A不是P" → Atom
    - "P且Q" / "P和Q" → And
    - "P或Q" → Or
    - "所有S是P" / "有的S不是P" → All/Some
    - "某人说得对/不对" → speaker truth evaluation
    - "A、B入选" / "A、B都未入选" → And of atoms
    """
    text = text.strip()
    if not text:
        return None

    # Handle "X说的不对，Y P" → And(Atom("X说的不对"), Atom("Y P"))
    m = re.match(r"([一-鿿]{1,4})说的?[不没]?对[，,]\s*(.+)", text)
    if m:
        speaker_eval = m.group(1) + "说得不对"
        rest = m.group(2).strip()
        p1 = Atom(speaker_eval, "", negated=False, raw=m.group(1) + "说的不对")
        p2 = parse_option_text(rest)
        if p2:
            return And(p1, p2, raw=text)
        return p1

    # Handle "A、B都P" / "A、B二人P" / "A、B P" pattern
    m = re.match(r"([一-鿿])[、和]([一-鿿])(?:二人|两人|都|均)?(.+)", text)
    if m:
        subj1 = m.group(1)
        subj2 = m.group(2)
        pred = m.group(3).strip()
        # Build atoms directly to avoid bare-atom splitting issues
        neg = "不" in pred or "没" in pred
        p1 = Atom(subj1, pred, negated=neg, raw=subj1 + pred)
        p2 = Atom(subj2, pred, negated=neg, raw=subj2 + pred)
        return And(p1, p2, raw=text)

    # Handle "去了X、Y、Z" / "没去X、Y" pattern
    m = re.match(r"(?:去了|没去|去过|没去过)(.+)", text)
    if m:
        rest = m.group(1)
        parts = re.split(r"[、和]", rest)
        if len(parts) >= 2:
            neg = "没" in text[:4]
            # Create atoms with location as predicate (matching Imply-parsed facts)
            atoms = [Atom("", p.strip(), negated=neg, raw=p.strip()) for p in parts if p.strip()]
            if len(atoms) >= 2:
                # Build right-associative And chain
                result = atoms[-1]
                for a in reversed(atoms[:-1]):
                    result = And(a, result, raw=text)
                return result

    # Try parse_statement for standard patterns
    prop = parse_statement(text)
    if prop:
        return prop

    return None


def _option_entailed_by_facts(
    option_prop: Proposition, facts: dict,
    binary_domains: list[tuple[str, str]] | None = None,
) -> bool | None:
    """Check if an option proposition is entailed by the given facts.

    Returns:
    - True: option is definitely true given facts
    - False: option is definitely false given facts
    - None: cannot determine
    """
    if option_prop is None:
        return None

    # For And: both sides must be entailed
    if option_prop.kind == "and":
        left = _option_entailed_by_facts(option_prop.left, facts, binary_domains)
        right = _option_entailed_by_facts(option_prop.right, facts, binary_domains)
        if left is True and right is True:
            return True
        if left is False or right is False:
            return False
        return None

    # For Or: at least one side must be entailed
    if option_prop.kind == "or":
        left = _option_entailed_by_facts(option_prop.left, facts, binary_domains)
        right = _option_entailed_by_facts(option_prop.right, facts, binary_domains)
        if left is True or right is True:
            return True
        if left is False and right is False:
            return False
        return None

    # For Imply: check if the implication holds
    if option_prop.kind == "imply":
        ant = _option_entailed_by_facts(option_prop.left, facts, binary_domains)
        cons = _option_entailed_by_facts(option_prop.right, facts, binary_domains)
        if ant is True and cons is True:
            return True
        if ant is True and cons is False:
            return False
        return None

    # For atoms: check against facts (with normalization and binary complement)
    if option_prop.kind == "atom":
        subj = option_prop.subject or ""
        pred = option_prop.predicate or ""
        neg = option_prop.negated

        # Try exact match first
        key = ("atom", subj, pred, neg)
        if key in facts:
            return facts[key]
        opp_key = ("atom", subj, pred, not neg)
        if opp_key in facts:
            return not facts[opp_key]

        # Try normalized match
        norm_key = normalize_atom_key(key)
        if norm_key != key:
            if norm_key in facts:
                return facts[norm_key]
            norm_opp = normalize_atom_key(opp_key)
            if norm_opp in facts:
                return not facts[norm_opp]

        # Try binary complement: if fact has Atom(subj, A, True) and
        # (A, B) is a binary domain, then Atom(subj, B, False) is entailed
        if binary_domains and pred:
            for fact_key, fact_val in facts.items():
                if fact_key[0] != "atom":
                    continue
                _, f_subj, f_pred, f_neg = fact_key
                if f_subj != subj:
                    continue
                # Check if f_pred and pred are complementary
                for a, b in binary_domains:
                    if (f_pred == a and pred == b) or (f_pred == b and pred == a):
                        # If fact says ¬A (f_neg=True, fact_val=True) → B is true
                        if f_neg and fact_val:
                            # B should be true (neg=False)
                            return not neg
                        # If fact says A (f_neg=False, fact_val=True) → B is false
                        if not f_neg and fact_val:
                            # B should be false (neg=True)
                            return neg

        # Try matching against all facts with normalized comparison
        for fact_key, fact_val in facts.items():
            if fact_key[0] != "atom":
                continue
            norm_fact = normalize_atom_key(fact_key)
            if norm_fact == norm_key:
                return fact_val
            if norm_fact == normalize_atom_key(opp_key):
                return not fact_val

        return None

    # For All/Some: check against facts
    if option_prop.kind in ("all", "some"):
        key = (option_prop.kind, option_prop.subject, option_prop.predicate, option_prop.negated)
        if key in facts:
            return facts[key]
        norm_key = _prop_to_normalized_key(option_prop)
        if norm_key and norm_key in facts:
            return facts[norm_key]
        return None

    return None


def _is_possibility_question(question_text: str) -> bool:
    """Detect if the question asks 'could be true' vs 'must be true'."""
    possibility_markers = ["可能为真", "可能正确", "可能成立", "哪项可能"]
    necessity_markers = ["一定为真", "一定正确", "必然", "肯定为真", "可以推出", "由此推出"]
    has_possibility = any(m in question_text for m in possibility_markers)
    has_necessity = any(m in question_text for m in necessity_markers)
    return has_possibility and not has_necessity


def map_options_to_assignments(
    options: list[OptionClaim],
    valid_assignments: list[tuple[list[bool], dict]],
    question_text: str = "",
    propositions: list[Proposition | None] | None = None,
) -> OptionMappingResult:
    """Map options to assignment facts and determine option status.

    For each option, check if it's entailed by ALL consistent assignments.
    If exactly one option is entailed by all assignments, it's unique_supported.
    """
    if not options:
        return OptionMappingResult(option_status="not_attempted", warnings=["no_options"])

    if not valid_assignments:
        return OptionMappingResult(option_status="not_attempted", warnings=["no_assignments"])

    # Extract binary domains and known entities from question text
    binary_domains = extract_binary_domains(question_text) if question_text else []
    known_entities = _extract_known_entities(propositions or [])

    # Parse options
    parsed_options: list[tuple[OptionClaim, Proposition | None]] = []
    for opt in options:
        prop = parse_option_text(opt.raw)
        parsed_options.append((opt, prop))

    # For each option, check entailment across all assignments
    option_results: list[dict] = []
    for opt, prop in parsed_options:
        entailments: list[bool | None] = []
        for assignment, facts in valid_assignments:
            # Apply binary complement and universal instantiation
            enriched = dict(facts)
            if binary_domains:
                enriched = _apply_binary_complement(enriched, binary_domains)
            if known_entities:
                enriched = _instantiate_universal_facts(enriched, known_entities)
            entailed = _option_entailed_by_facts(prop, enriched, binary_domains)
            entailments.append(entailed)

        # Determine overall status for this option
        all_true = all(e is True for e in entailments)
        all_false = all(e is False for e in entailments)
        any_true = any(e is True for e in entailments)

        if all_true:
            option_status = "entailed_by_all"
        elif all_false:
            option_status = "contradicted_by_all"
        elif any_true:
            option_status = "entailed_by_some"
        else:
            option_status = "unknown"

        option_results.append({
            "label": opt.label,
            "raw": opt.raw,
            "parsed_kind": prop.kind if prop else None,
            "entailments": entailments,
            "option_status": option_status,
        })

    # Determine overall option mapping status
    is_possibility = _is_possibility_question(question_text)

    # For possibility questions: an option is "possible" if entailed by at least one assignment
    if is_possibility:
        entailed_by_some = [r for r in option_results if r["option_status"] == "entailed_by_some"]
        entailed_by_all = [r for r in option_results if r["option_status"] == "entailed_by_all"]
        possible_options = entailed_by_all + entailed_by_some
        if len(possible_options) == 1:
            return OptionMappingResult(
                option_status="unique_supported",
                selected_label=possible_options[0]["label"],
                option_trace=option_results,
                warnings=["possibility_question"],
            )
        elif len(possible_options) > 1:
            return OptionMappingResult(
                option_status="ambiguous_options",
                option_trace=option_results,
                warnings=[f"{len(possible_options)}_options_possible"],
            )
        # Fall through to necessity logic if no option is possible

    entailed_by_all = [r for r in option_results if r["option_status"] == "entailed_by_all"]

    if len(entailed_by_all) == 1:
        return OptionMappingResult(
            option_status="unique_supported",
            selected_label=entailed_by_all[0]["label"],
            option_trace=option_results,
        )
    elif len(entailed_by_all) > 1:
        return OptionMappingResult(
            option_status="ambiguous_options",
            option_trace=option_results,
            warnings=[f"{len(entailed_by_all)}_options_entailed_by_all"],
        )
    else:
        # No option is entailed by all assignments
        entailed_by_some = [r for r in option_results if r["option_status"] == "entailed_by_some"]
        if entailed_by_some:
            return OptionMappingResult(
                option_status="ambiguous_options",
                option_trace=option_results,
                warnings=[f"{len(entailed_by_some)}_options_entailed_by_some"],
            )

        # Check for unique_supported_across_assignments:
        # An option is "not contradicted by any assignment" if all its entailments
        # are either True or None (never False). If exactly one such option exists
        # and it has at least one True entailment, it's the answer.
        not_contradicted = []
        for r in option_results:
            entailments = r["entailments"]
            has_true = any(e is True for e in entailments)
            has_false = any(e is False for e in entailments)
            if has_true and not has_false:
                not_contradicted.append(r)

        if len(not_contradicted) == 1:
            return OptionMappingResult(
                option_status="unique_supported_across_assignments",
                selected_label=not_contradicted[0]["label"],
                option_trace=option_results,
                warnings=["across_assignments"],
            )

        return OptionMappingResult(
            option_status="no_supported_option",
            option_trace=option_results,
        )


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve_truth_core(question_text: str) -> TruthReasoningResult:
    """Solve a truth reasoning question.

    Returns a TruthReasoningResult with status:
    - solved: exactly one consistent assignment found
    - ambiguous: multiple consistent assignments
    - inconsistent: no consistent assignments
    - analysis_only: could not parse enough structure
    """
    constraint = parse_truth_constraint(question_text)
    raw_stmts = extract_statements(question_text)

    if not raw_stmts:
        return TruthReasoningResult(status="analysis_only", warnings=["no_statements_extracted"])

    propositions: list[Proposition | None] = []
    for stmt in raw_stmts:
        prop = parse_statement(stmt["text"])
        propositions.append(prop)

    parsed = [p for p in propositions if p is not None]
    if len(parsed) < 2:
        return TruthReasoningResult(
            status="analysis_only",
            warnings=[f"only_{len(parsed)}_statements_parsed"],
        )

    n = len(propositions)
    valid_assignments: list[tuple[list[bool], dict]] = []

    for true_indices in _enumerate_assignments(n, constraint):
        assignment = [i in true_indices for i in range(n)]
        ok, facts = _check_assignment(propositions, assignment)
        if ok:
            valid_assignments.append((assignment, facts))

    if not valid_assignments:
        return TruthReasoningResult(
            status="inconsistent",
            assignments=[],
            warnings=["no_consistent_assignment"],
        )

    if len(valid_assignments) == 1:
        assignment, facts = valid_assignments[0]
        return TruthReasoningResult(
            status="solved",
            facts=[],
            assignments=[{"assignment": assignment, "facts": dict(facts)}],
        )

    return TruthReasoningResult(
        status="ambiguous",
        assignments=[
            {"assignment": a, "facts": dict(f)} for a, f in valid_assignments
        ],
        warnings=[f"{len(valid_assignments)}_consistent_assignments"],
    )


def _enumerate_assignments(n: int, constraint: TruthConstraint):
    """Yield sets of indices that should be True."""
    if constraint.true_count is not None:
        tc = constraint.true_count
        if tc == -1:  # all true
            yield frozenset(range(n))
            return
        if 0 <= tc <= n:
            for combo in combinations(range(n), tc):
                yield frozenset(combo)
        return

    if constraint.false_count is not None:
        fc = constraint.false_count
        if fc == -1:  # all false
            yield frozenset()
            return
        if 0 <= fc <= n:
            tc = n - fc
            for combo in combinations(range(n), tc):
                yield frozenset(combo)
        return

    # No constraint: try all subsets
    for k in range(n + 1):
        for combo in combinations(range(n), k):
            yield frozenset(combo)


def _derive_closure(atoms: dict, implications: list, disjunctions: list,
                     conjunctions: list, alls: dict, somes: dict,
                     exclusive_pairs: list | None = None) -> dict:
    """Derive all possible facts from the given set until fixpoint.

    Returns the final atoms dict (may be extended with new derivations).
    """
    atoms = dict(atoms)
    if exclusive_pairs is None:
        exclusive_pairs = []
    changed = True
    while changed:
        changed = False

        # 1. Modus ponens: Imply(P, Q) + P → Q
        for ante_key, cons_list in implications:
            if ante_key in atoms and atoms[ante_key]:
                for cons in cons_list:
                    if cons.kind == "atom":
                        k = ("atom", cons.subject, cons.predicate, cons.negated)
                        if k not in atoms:
                            atoms[k] = True
                            changed = True

        # 1b. Modus tollens (contrapositive): Imply(P, Q) + ¬Q → ¬P
        for ante_key, cons_list in implications:
            for cons in cons_list:
                if cons.kind == "atom":
                    cons_neg_key = ("atom", cons.subject, cons.predicate, not cons.negated)
                    if cons_neg_key in atoms and atoms[cons_neg_key]:
                        if ante_key[0] == "atom":
                            neg_ante = ("atom", ante_key[1], ante_key[2], not ante_key[3])
                            if neg_ante not in atoms:
                                atoms[neg_ante] = True
                                changed = True

        # 2. Disjunctive syllogism: Or(P, Q) + ¬P → Q
        for disj in disjunctions:
            left_key = _prop_to_fact_key(disj.left)
            right_key = _prop_to_fact_key(disj.right)
            if left_key and left_key in atoms and not atoms[left_key]:
                rk = _prop_to_fact_key(disj.right)
                if rk and rk not in atoms:
                    atoms[rk] = True
                    changed = True
            if right_key and right_key in atoms and not atoms[right_key]:
                lk = _prop_to_fact_key(disj.left)
                if lk and lk not in atoms:
                    atoms[lk] = True
                    changed = True

        # 3. And decomposition: And(P, Q) → P, Q
        for conj in conjunctions:
            for part in [conj.left, conj.right]:
                pk = _prop_to_fact_key(part)
                if pk and pk not in atoms:
                    atoms[pk] = True
                    changed = True

        # 4. Exclusive-one: exactly_one(A, B)
        # If A known true → B false; If A known false → B true; and vice versa
        for left, right in exclusive_pairs:
            lk = _prop_to_fact_key(left)
            rk = _prop_to_fact_key(right)
            if lk and lk in atoms:
                if atoms[lk]:
                    # A true → B false
                    if rk and rk not in atoms:
                        atoms[rk] = False
                        changed = True
                    neg_rk = _prop_to_fact_key(negate_proposition(right))
                    if neg_rk and neg_rk not in atoms:
                        atoms[neg_rk] = True
                        changed = True
                else:
                    # A false → B true
                    if rk and rk not in atoms:
                        atoms[rk] = True
                        changed = True
            if rk and rk in atoms:
                if atoms[rk]:
                    # B true → A false
                    if lk and lk not in atoms:
                        atoms[lk] = False
                        changed = True
                    neg_lk = _prop_to_fact_key(negate_proposition(left))
                    if neg_lk and neg_lk not in atoms:
                        atoms[neg_lk] = True
                        changed = True
                else:
                    # B false → A true
                    if lk and lk not in atoms:
                        atoms[lk] = True
                        changed = True

    return atoms


def _check_assignment(
    propositions: list[Proposition | None], assignment: list[bool]
) -> tuple[bool, dict]:
    """Check if an assignment is consistent using closure-based reasoning.

    Returns (is_consistent, facts_dict).
    """
    atoms: dict[tuple, bool] = {}
    implications: list[tuple[tuple, list[Proposition]]] = []
    disjunctions: list[Proposition] = []
    conjunctions: list[Proposition] = []
    exclusive_pairs: list[tuple[Proposition, Proposition]] = []

    def _add_atom(key: tuple, val: bool) -> bool:
        """Add atom fact. Returns False if contradiction."""
        if key in atoms:
            if atoms[key] != val:
                return False
        else:
            atoms[key] = val
        return True

    def _collect_from_prop(p: Proposition, val: bool) -> bool:
        """Collect facts from a proposition being val (True/False)."""
        if p.kind == "atom":
            key = ("atom", p.subject, p.predicate, p.negated)
            return _add_atom(key, val)
        if p.kind == "not" and p.left.kind == "atom":
            inner = p.left
            key = ("atom", inner.subject, inner.predicate, not inner.negated)
            return _add_atom(key, val)
        if p.kind == "all":
            key = ("atom", p.subject, p.predicate, p.negated)
            return _add_atom(key, val)
        if p.kind == "some":
            key = ("atom", p.subject, p.predicate, p.negated)
            return _add_atom(key, val)

        if val:
            if p.kind == "imply":
                # Store implication for modus ponens
                ante_key = _prop_to_fact_key(p.left)
                if ante_key:
                    # Find or create entry
                    found = False
                    for i, (k, cs) in enumerate(implications):
                        if k == ante_key:
                            implications[i] = (k, cs + [p.right])
                            found = True
                            break
                    if not found:
                        implications.append((ante_key, [p.right]))
                    # Also: if antecedent is already known true, derive consequent
                    if ante_key in atoms and atoms[ante_key]:
                        if not _collect_from_prop(p.right, True):
                            return False
            if p.kind == "or":
                disjunctions.append(p)
                # Check if one side is already known false (disjunctive syllogism)
                # Check both direct key and negated key
                for side, other in [(p.left, p.right), (p.right, p.left)]:
                    lk = _prop_to_fact_key(side)
                    if lk and lk in atoms and not atoms[lk]:
                        if not _collect_from_prop(other, True):
                            return False
                    # Also check if the negation of this side is known true
                    neg_side = negate_proposition(side)
                    nk = _prop_to_fact_key(neg_side)
                    if nk and nk in atoms and atoms[nk]:
                        if not _collect_from_prop(other, True):
                            return False
            if p.kind == "and":
                conjunctions.append(p)
                if not _collect_from_prop(p.left, True):
                    return False
                if not _collect_from_prop(p.right, True):
                    return False
            if p.kind == "exactly_one":
                # Store for closure loop
                exclusive_pairs.append((p.left, p.right))
                # Exactly one of A, B is true
                # If A is known true → B must be false
                # If B is known true → A must be false
                # If A is known false → B must be true
                # If B is known false → A must be true
                lk = _prop_to_fact_key(p.left)
                rk = _prop_to_fact_key(p.right)
                if lk and lk in atoms:
                    if atoms[lk]:
                        # A is true → B must be false
                        if not _collect_from_prop(p.right, False):
                            return False
                    else:
                        # A is false → B must be true
                        if not _collect_from_prop(p.right, True):
                            return False
                if rk and rk in atoms:
                    if atoms[rk]:
                        # B is true → A must be false
                        if not _collect_from_prop(p.left, False):
                            return False
                    else:
                        # B is false → A must be true
                        if not _collect_from_prop(p.left, True):
                            return False
        else:
            # False: negation is true
            if p.kind == "exactly_one":
                # ¬exactly_one(A,B) = (A∧B) ∨ (¬A∧¬B)
                # Check if we can determine which case holds
                lk = _prop_to_fact_key(p.left)
                rk = _prop_to_fact_key(p.right)
                left_known = lk and lk in atoms
                right_known = rk and rk in atoms
                if left_known and right_known:
                    if atoms[lk] and atoms[rk]:
                        # Both true → consistent with (A∧B)
                        pass
                    elif not atoms[lk] and not atoms[rk]:
                        # Both false → consistent with (¬A∧¬B)
                        pass
                    else:
                        # One true, one false → contradicts ¬exactly_one
                        return False
                elif left_known:
                    if atoms[lk]:
                        # A true → B must be true (from A∧B case)
                        if not _collect_from_prop(p.right, True):
                            return False
                    else:
                        # A false → B must be false (from ¬A∧¬B case)
                        if not _collect_from_prop(p.right, False):
                            return False
                elif right_known:
                    if atoms[rk]:
                        # B true → A must be true
                        if not _collect_from_prop(p.left, True):
                            return False
                    else:
                        # B false → A must be false
                        if not _collect_from_prop(p.left, False):
                            return False
            else:
                neg = negate_proposition(p)
                if not _collect_from_prop(neg, True):
                    return False

        return True

    # Phase 1: Collect all facts from the assignment
    for prop, is_true in zip(propositions, assignment):
        if prop is None:
            continue
        if not _collect_from_prop(prop, is_true):
            return False, atoms

    # Phase 2: Derive closure
    atoms = _derive_closure(atoms, implications, disjunctions, conjunctions, {}, {}, exclusive_pairs)

    # Phase 3: Check for contradictions
    # 3a: Direct atom contradictions
    atom_pairs: dict[tuple, bool] = {}
    for key, val in atoms.items():
        if key[0] == "atom":
            k = (key[1], key[2])  # (subject, predicate)
            effective = val if not key[3] else not val
            if k in atom_pairs and atom_pairs[k] != effective:
                return False, atoms
            atom_pairs[k] = effective

    # 3b: All vs Some contradictions
    for key, val in atoms.items():
        if key[0] == "all" and val:
            opp = ("some", key[1], key[2], not key[3])
            if opp in atoms and atoms[opp]:
                return False, atoms
        if key[0] == "some" and val:
            opp = ("all", key[1], key[2], not key[3])
            if opp in atoms and atoms[opp]:
                return False, atoms

    # 3c: All vs Atom contradictions
    all_facts = [(k, v) for k, v in atoms.items() if k[0] == "all" and v]
    atom_facts = [(k, v) for k, v in atoms.items() if k[0] == "atom" and v]
    for ak, _ in all_facts:
        for atk, _ in atom_facts:
            if ak[2] == atk[2] and ak[3] != atk[3]:
                return False, atoms

    # Phase 4: Check that true propositions are consistent with facts (after closure)
    true_props = [p for p, t in zip(propositions, assignment) if p is not None and t]
    for prop in true_props:
        if not _evaluate_true(prop, atoms):
            return False, atoms

    # Phase 5: Check that false propositions are contradicted by facts (after closure)
    for prop, is_true in zip(propositions, assignment):
        if prop is None or is_true:
            continue
        if not _evaluate_false(prop, atoms):
            return False, atoms

    return True, atoms
