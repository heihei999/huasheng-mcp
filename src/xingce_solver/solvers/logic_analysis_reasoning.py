"""Isolated analysis reasoning core for logic judgment questions.

This module implements a minimal structured analysis reasoner for
"分析推理" / "朴素逻辑" questions commonly found in Chinese civil
service exams (行测).

It is NOT integrated into solve_logic_reasoning. It is a standalone
engine for testing the core algorithm in isolation.

Version: v0.1
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from itertools import permutations, product
from typing import Any


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AnalysisVariable:
    """A variable in an analysis reasoning problem."""
    name: str
    domain: tuple[str, ...]
    raw: str = ""


@dataclass(frozen=True)
class AnalysisConstraint:
    """A constraint on variables."""
    kind: str  # equal, not_equal, left_of, right_of, adjacent, position,
               # same_group, diff_group, selected, not_selected,
               # imply, half_true, comparison
    left: str | None = None
    right: str | None = None
    relation: str | None = None
    value: str | None = None
    value2: str | None = None  # for half_true: second claim
    raw: str = ""


@dataclass(frozen=True)
class OptionClaim:
    """A parsed answer option."""
    label: str
    raw: str
    assignments: dict[str, str] | None = None  # variable -> value
    negated: bool = False
    claim_kind: str = "assignment"  # assignment, comparison, ordering


@dataclass
class AnalysisReasoningResult:
    """Result of the analysis reasoning engine."""
    status: str  # solved / ambiguous / inconsistent / analysis_only
    task_type: str = ""
    variables: list[AnalysisVariable] = field(default_factory=list)
    constraints: list[AnalysisConstraint] = field(default_factory=list)
    assignments: list[dict[str, str]] = field(default_factory=list)
    option_status: str = "not_attempted"
    predicted_label: str | None = None
    option_trace: list[dict[str, Any]] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_VARIABLES = 7
MAX_PERMUTATIONS = 5040  # 7!
MAX_CARTESIAN = 20000


# ---------------------------------------------------------------------------
# Task classification
# ---------------------------------------------------------------------------

def classify_analysis_task(question_text: str) -> str:
    """Classify the analysis reasoning task type."""
    if re.search(r"半真半假|只猜对了一半|一真一假|一半", question_text):
        return "half_true_half_false"
    if re.search(r"相邻|紧挨|挨着", question_text):
        return "ordering_adjacency"
    if re.search(r"从[左到右由北至南东西前后]|排列|顺序|第[一二三四五六七]位|第[一二三四五六七]个", question_text):
        return "ordering"
    if re.search(r"同组|不同组|分给|分组", question_text):
        return "grouping"
    if re.search(r"比.{1,6}[大多少高矮]", question_text):
        return "comparison"
    if re.search(r"是|不是|职业|研究|技能|茶|颜色|球", question_text):
        return "matching"
    return "unknown"


# ---------------------------------------------------------------------------
# Entity and domain extraction
# ---------------------------------------------------------------------------

def _extract_names_from_text(text: str) -> list[str]:
    """Extract person/entity names from text."""
    names: list[str] = []

    # Pattern: 甲、乙、丙、丁
    cn_names = re.findall(r"[甲乙丙丁戊己庚辛壬癸]", text)
    names.extend(cn_names)

    # Pattern: A星、B星 (single letter + 星)
    star_names = re.findall(r"([A-G])星", text)
    names.extend(star_names)

    # Pattern: 小华、小峰、小明 (2-char names starting with 小)
    small_names = re.findall(r"(小[一-龥]{1,2})", text)
    names.extend(small_names)

    # Pattern: 梅兰竹菊
    if "梅兰竹菊" in text:
        names.extend(["梅", "兰", "竹", "菊"])

    # Dedupe preserving order
    seen = set()
    result = []
    for n in names:
        if n not in seen:
            seen.add(n)
            result.append(n)
    return result


def _extract_domain_from_text(text: str) -> list[str]:
    """Extract domain values from question text."""
    domains: list[str] = []

    # Pattern: X班、Y班、Z班 (team/class names)
    team_names = re.findall(r"([一二三四五六七八九十])[班组队]", text)
    if len(team_names) >= 2:
        for t in team_names:
            domains.append(f"{t}班")
        return list(dict.fromkeys(domains))

    # Pattern: X、Y、Z三人 (descriptive names)
    m = re.search(r"([一-龥]+(?:、[一-龥]+)+)(?:[三四五六七])人", text)
    if m:
        values = m.group(1).split("、")
        for v in values:
            v = v.strip()
            # Skip single-char names and common non-domain words
            if v and len(v) >= 2 and len(v) <= 4:
                # Remove leading 有/是/为
                v = re.sub(r"^[有是为]", "", v)
                if v and v not in ("甲", "乙", "丙", "丁", "戊", "己", "其中"):
                    domains.append(v)

    # Pattern: 研究X学、Y学、Z学 (only from explicit domain listing)
    # Match "分别研究X学、Y学、Z学" or "研究X学、Y学、Z学三种"
    m = re.search(r"(?:分别)?研究([一-龥]+学)(?:、([一-龥]+学))(?:、([一-龥]+学))", text)
    if m:
        for i in range(1, 4):
            if m.group(i):
                domains.append(m.group(i))
    else:
        # Fallback: find all X学 patterns
        research = re.findall(r"研究([一-龥]+学)", text)
        domains.extend(research)

    # Pattern: X老师 (teacher names)
    teachers = re.findall(r"([一-龥]+)老师", text)
    domains.extend(teachers)

    # Pattern: 技能/能力 list: "编程、插花、绘画、书法"
    m = re.search(r"(?:技能|能力)[^，。]*?(?:有|是|为)?\s*([一-龥]+(?:、[一-龥]+)+)", text)
    if m:
        for v in m.group(1).split("、"):
            v = v.strip()
            if v and len(v) >= 2:
                domains.append(v)

    # Pattern: 职业 list: "作家、翻译、主持人"
    m = re.search(r"(?:职业|身份)[^，。]*?(?:有|是|为)?\s*([一-龥]+(?:、[一-龥]+)+)", text)
    if m:
        for v in m.group(1).split("、"):
            v = v.strip()
            if v and len(v) >= 2:
                domains.append(v)

    # Pattern: 车辆 list: "自行车、三轮车、拖拉机、面包车"
    vehicles = re.findall(r"(自行车|三轮车|拖拉机|面包车|汽车|摩托车|电动车)", text)
    domains.extend(list(dict.fromkeys(vehicles)))

    # Pattern: 抽屉/位置: "最上层、中间、最底层"
    positions = re.findall(r"(最[上下左右前后]|中间|第[一二三四五]层|第[一二三四五]个|第[一二三四五]位)", text)
    domains.extend(list(dict.fromkeys(positions)))

    # Dedupe
    return list(dict.fromkeys(domains))


def _extract_domain_from_options(options: list[OptionClaim]) -> list[str]:
    """Extract domain values from options."""
    domains: list[str] = []

    for opt in options:
        # Pattern: X是Y
        for m in re.finditer(r"是([一-龥]+?)(?:，|、|。|$)", opt.raw):
            val = m.group(1)
            if val not in ("不", "没", "有"):
                domains.append(val)

        # Pattern: X研究Y
        for m in re.finditer(r"研究([一-龥]+)", opt.raw):
            domains.append(m.group(1))

    return list(dict.fromkeys(domains))


def extract_variables_and_domains(question_text: str, options: list[OptionClaim] | None = None, task_type: str = "") -> list[AnalysisVariable]:
    """Extract variables and their domains from question text and options."""
    variables: list[AnalysisVariable] = []

    # Extract names
    names = _extract_names_from_text(question_text)
    if not names and options:
        for opt in options:
            names.extend(_extract_names_from_text(opt.raw))
        names = list(dict.fromkeys(names))

    # Extract domains
    domains = _extract_domain_from_text(question_text)
    if not domains and options:
        domains = _extract_domain_from_options(options)

    # Check if it's an ordering question (positions as domain)
    if re.search(r"排列|顺序|位|第[一二三四五六七八九十]|从左到右|从北至南|出场", question_text):
        n = len(names) if names else 0
        if n > 0:
            domains = [str(i) for i in range(1, n + 1)]

    # Check if it's a drawer/box question
    if re.search(r"抽屉|盒子|柜子", question_text):
        m = re.search(r"([三四五六七八九十])个", question_text)
        if m:
            n = _cn_digit(m.group(1))
            domains = [str(i) for i in range(1, n + 1)]

    # For ordering questions, try to extract actual entities from half-true statements
    if task_type == "half_true_half_false" and re.search(r"出场|顺序|排列", question_text):
        # Extract entities from speaker statements (e.g., "一班第一个出场")
        entities = re.findall(r"([一二三四五六七八九十])[班组队]", question_text)
        if len(entities) >= 2:
            # Deduplicate
            seen = set()
            unique_entities = []
            for e in entities:
                if e not in seen:
                    seen.add(e)
                    unique_entities.append(e)
            names = [f"{e}班" for e in unique_entities]
            domains = [str(i) for i in range(1, len(names) + 1)]

    # For box/color matching questions (e.g., "五个盒子" + "五种颜色")
    if re.search(r"盒子|抽屉", question_text):
        box_names = re.findall(r"([一二三四五六七八九十])[个盒子抽屉]", question_text)
        color_names = re.findall(r"(红|蓝|黄|白|紫|绿|橙|粉)(?:球|色|的)", question_text)
        if len(box_names) >= 2 and len(color_names) >= 2:
            # Deduplicate box names
            seen = set()
            unique_boxes = []
            for b in box_names:
                if b not in seen:
                    seen.add(b)
                    unique_boxes.append(b)
            names = [f"第{n}盒" for n in unique_boxes]
            domains = list(dict.fromkeys(color_names))

    # For skill matching questions (e.g., "编程、插花、绘画、书法四种技能")
    if re.search(r"技能|能力", question_text) and not domains:
        skill_names = re.findall(r"(编程|插花|绘画|书法|唱歌|跳舞|弹琴|画画|写作|游泳|跑步|篮球|足球)", question_text)
        if len(skill_names) >= 2:
            domains = list(dict.fromkeys(skill_names))

    # For vehicle ordering questions (e.g., "两辆自行车、一辆三轮车")
    if re.search(r"自行车|三轮车|拖拉机|面包车", question_text) and not domains:
        vehicle_types = re.findall(r"(自行车|三轮车|拖拉机|面包车|汽车|摩托车)", question_text)
        if len(vehicle_types) >= 2:
            domains = list(dict.fromkeys(vehicle_types))

    # Build variables
    if names and domains:
        for name in names:
            variables.append(AnalysisVariable(name=name, domain=tuple(domains), raw=name))
    elif names:
        for name in names:
            variables.append(AnalysisVariable(name=name, domain=(), raw=name))

    return variables

    # Pattern: X星、Y星、Z星
    star_pattern = re.compile(r"([A-G])星")
    stars = star_pattern.findall(question_text)
    if len(stars) >= 3:
        variables = [AnalysisVariable(name=s, domain=(), raw=f"{s}星") for s in stars]

    # Pattern: 梅兰竹菊
    if "梅兰竹菊" in question_text:
        variables = [
            AnalysisVariable(name="梅", domain=(), raw="梅"),
            AnalysisVariable(name="兰", domain=(), raw="兰"),
            AnalysisVariable(name="竹", domain=(), raw="竹"),
            AnalysisVariable(name="菊", domain=(), raw="菊"),
        ]

    # Pattern: 小张、小文、小娟
    m = re.search(r"(小[一-龥](?:、小[一-龥])+)", question_text)
    if m and not variables:
        names = m.group(1).split("、")
        variables = [AnalysisVariable(name=n.strip(), domain=(), raw=n.strip()) for n in names]

    # Extract domains from context
    # Profession domain
    prof_match = re.search(r"(?:职业|身份).*?(?:有|是|为)\s*([一-龥]+(?:、[一-龥]+)+)", question_text)
    if prof_match:
        domains = prof_match.group(1).split("、")
        for v in variables:
            if not v.domain:
                object.__setattr__(v, 'domain', tuple(d.strip() for d in domains if d.strip()))

    # Skill domain
    skill_match = re.search(r"(?:技能|能力).*?(?:有|是|为)\s*([一-龥]+(?:、[一-龥]+)+)", question_text)
    if skill_match:
        domains = skill_match.group(1).split("、")
        for v in variables:
            if not v.domain:
                object.__setattr__(v, 'domain', tuple(d.strip() for d in domains if d.strip()))

    # Research domain
    research_match = re.search(r"研究\s*([一-龥]+(?:学|方向)(?:、[一-龥]+(?:学|方向))*)", question_text)
    if research_match:
        domains = [d.strip() for d in research_match.group(1).split("、") if d.strip()]
        for v in variables:
            if not v.domain:
                object.__setattr__(v, 'domain', tuple(domains))

    # Color domain
    color_match = re.search(r"([红蓝黄白紫绿橙粉])(?:球|色|箱)(?:.*?([红蓝黄白紫绿橙粉])(?:球|色|箱))", question_text)
    if color_match:
        colors = list(set(re.findall(r"[红蓝黄白紫紫绿橙粉](?:球|色)", question_text)))
        colors = [re.sub(r"[球色]", "", c) for c in colors]
        if len(colors) >= 2:
            for v in variables:
                if not v.domain:
                    object.__setattr__(v, 'domain', tuple(colors))

    # Position domain (for ordering questions)
    if re.search(r"排列|顺序|位", question_text):
        n = len(variables) if variables else 0
        if n > 0:
            for v in variables:
                if not v.domain:
                    object.__setattr__(v, 'domain', tuple(range(1, n + 1)))

    # Vehicle domain
    if "自行车" in question_text or "三轮车" in question_text:
        vehicles = re.findall(r"(自行车|三轮车|拖拉机|面包车|汽车|摩托车)", question_text)
        vehicles = list(dict.fromkeys(vehicles))  # dedupe preserving order
        if vehicles:
            for v in variables:
                if not v.domain:
                    object.__setattr__(v, 'domain', tuple(vehicles))

    return variables


# ---------------------------------------------------------------------------
# Constraint parsing
# ---------------------------------------------------------------------------

def parse_constraints(question_text: str) -> list[AnalysisConstraint]:
    """Parse constraints from question text."""
    constraints: list[AnalysisConstraint] = []

    # "X不是Y" / "其中X不是Y" (avoid duplicates, filter noise)
    seen_not_equal = set()
    for m in re.finditer(r"(?:其中)?([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)不是([一-龥]+)", question_text):
        left = m.group(1)
        right = m.group(2)
        # Filter noise: left must be a valid entity (not single-char noise like "不")
        if len(left) < 2 and left not in "甲乙丙丁戊己庚辛壬癸A-G":
            continue
        key = (left, right)
        if key not in seen_not_equal:
            seen_not_equal.add(key)
            constraints.append(AnalysisConstraint(
                kind="not_equal", left=left, right=right, raw=m.group()
            ))

    # "X是Y" (positive assignment, filter noise)
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)是([一-龥]+?)(?:，|。|；|$)", question_text):
        left = m.group(1)
        right = m.group(2)
        # Filter noise words
        noise_words = {"不", "没", "没有", "他们", "什么", "其中", "则", "如果", "那么"}
        if right in noise_words or left in noise_words:
            continue
        if len(left) < 2 and left not in "甲乙丙丁戊己庚辛壬癸":
            continue
        constraints.append(AnalysisConstraint(
            kind="equal", left=left, right=right, raw=m.group()
            ))

    # "X在Y左边/北侧/前面"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)在([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:的)?(?:左[边侧]|北[侧边]|前[面边])", question_text):
        constraints.append(AnalysisConstraint(
            kind="left_of", left=m.group(1), right=m.group(2), raw=m.group()
        ))

    # "X在N人中最小/最大" / "X在三人中年龄最小"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)在.*?[中里](?:年龄)?(?:最小|最年轻|最低)", question_text):
        constraints.append(AnalysisConstraint(
            kind="position", left=m.group(1), value="min", raw=m.group()
        ))

    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)在.*?[中里](?:年龄)?(?:最大|最年长|最高)", question_text):
        constraints.append(AnalysisConstraint(
            kind="position", left=m.group(1), value="max", raw=m.group()
        ))
        constraints.append(AnalysisConstraint(
            kind="left_of", left=m.group(1), right=m.group(2), raw=m.group()
        ))

    # "X在Y右边/南侧/后面"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)在([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:的)?(?:右[边侧]|南[侧边]|后[面边])", question_text):
        constraints.append(AnalysisConstraint(
            kind="right_of", left=m.group(1), right=m.group(2), raw=m.group()
        ))

    # "X与Y相邻/紧挨着"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:与|和)([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:相邻|紧挨|挨着)", question_text):
        constraints.append(AnalysisConstraint(
            kind="adjacent", left=m.group(1), right=m.group(2), raw=m.group()
        ))

    # "X在第N位"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)在第([一二三四五六七八九十1-9])位", question_text):
        pos = _cn_digit(m.group(2))
        constraints.append(AnalysisConstraint(
            kind="position", left=m.group(1), value=str(pos), raw=m.group()
        ))

    # "X和Y同组/分给同一个人"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)和([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:同组|分给了?同)", question_text):
        constraints.append(AnalysisConstraint(
            kind="same_group", left=m.group(1), right=m.group(2), raw=m.group()
        ))

    # "X和Y不同组"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)和([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)不同组", question_text):
        constraints.append(AnalysisConstraint(
            kind="diff_group", left=m.group(1), right=m.group(2), raw=m.group()
        ))

    # "X比Y大/多/高" / "X比Y年龄大"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:的)?(?:年龄|学术成果|收入)?比([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:的|的?年龄|学术成果|收入)?[大多高]", question_text):
        left = m.group(1).strip()
        right = m.group(2).strip()
        # Clean up right side - remove 年龄 suffix
        right = re.sub(r"年龄$", "", right)
        constraints.append(AnalysisConstraint(
            kind="comparison", left=left, right=right, relation="greater", raw=m.group()
        ))
        constraints.append(AnalysisConstraint(
            kind="comparison", left=m.group(1), right=m.group(2), relation="greater", raw=m.group()
        ))

    # "X比Y小/少/矮"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:的)?(?:学术成果|收入|年龄)?比([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:的)?(?:学术成果|收入|年龄)?[小少矮低]", question_text):
        constraints.append(AnalysisConstraint(
            kind="comparison", left=m.group(1), right=m.group(2), relation="less", raw=m.group()
        ))

    # "X与Y相当/相同"
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:的)?(?:学术成果|收入|年龄)?与([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)(?:的)?(?:学术成果|收入|年龄)?(?:相当|相同|一样)", question_text):
        constraints.append(AnalysisConstraint(
            kind="comparison", left=m.group(1), right=m.group(2), relation="equal", raw=m.group()
        ))

    # "X会Y" (skill) - subject must be 1-2 chars (name)
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸]|小[一-龥])会([一-龥]+)", question_text):
        constraints.append(AnalysisConstraint(
            kind="equal", left=m.group(1), right=m.group(2), raw=m.group()
        ))

    # "X不会Y" (no skill)
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸]|小[一-龥])不会([一-龥]+)", question_text):
        constraints.append(AnalysisConstraint(
            kind="not_equal", left=m.group(1), right=m.group(2), raw=m.group()
        ))

    # "X分给了Y" (assignment)
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)分给了?([一-龥]+?)(?:老师|$)", question_text):
        constraints.append(AnalysisConstraint(
            kind="equal", left=m.group(1), right=m.group(2) + "老师", raw=m.group()
        ))

    # Half-true-half-false: "每人只猜对了一半" / "每人都只猜对了一种" / "只说对了一半"
    if re.search(r"每人.*?猜对.*?一半|每人.*?一真一假|每人.*?两句.*?一真|猜测.*?只对了.*?一半|每人都只猜对|一真一假|每人.*?只猜对了.*?[一种]|只[说猜]对了.*?一半|说对了一半|判断完全正确.*?只说对了一半", question_text):
        half_true_constraints = _parse_half_true_statements(question_text)
        constraints.extend(half_true_constraints)

    return constraints


def _parse_half_true_statements(question_text: str) -> list[AnalysisConstraint]:
    """Parse half-true-half-false statements from question text.

    For patterns like:
    - 甲：第二盒是紫的，第三盒是黄的
    - 乙：第二盒是蓝的，第四盒是红的

    Each speaker has two statements, exactly one is true.
    """
    constraints: list[AnalysisConstraint] = []

    # Pattern: X说/猜：statement1，statement2 or X：statement1，statement2
    # Speaker name: single char 甲-癸, or 小X
    speaker_pattern = re.compile(
        r"([甲乙丙丁戊己庚辛壬癸]|小[一-龥])[说道猜：][：]?\s*(.+?)(?=[甲乙丙丁戊己庚辛壬癸][说道猜：]|小[一-龥][说道猜：]|结果|发现|猜完|每人|。[甲乙丙丁]|$)"
    )

    for m in speaker_pattern.finditer(question_text):
        speaker = m.group(1)
        text = m.group(2).strip()

        # Split by comma or 、
        parts = re.split(r"[，,、；]", text)
        if len(parts) >= 2:
            sub_constraints = []
            for part in parts[:2]:  # Take first two
                part = part.strip().rstrip("。；，,")
                if not part:
                    continue
                # Parse each part as a simple constraint
                # Pattern: X第N个出场
                pos_m = re.search(r"([一-龥]+)第([一二三四五六七八九十1-9])个?出场", part)
                if pos_m:
                    sub_constraints.append({
                        "kind": "position",
                        "left": pos_m.group(1),
                        "right": str(_cn_digit(pos_m.group(2))),
                    })
                    continue
                # Pattern: X不是Y (check BEFORE X是Y to avoid false match)
                # First char must not be 不/没/未 to avoid matching bare "不是Y"
                neq_m = re.search(r"(?<![不没未])([一-龥]+)不是([一-龥]+)", part)
                if not neq_m:
                    # Bare "不是Y" → implicit subject
                    neq_m = re.match(r"^不是([一-龥]+?)[。；，,]?$", part.strip())
                    if neq_m:
                        sub_constraints.append({
                            "kind": "not_equal",
                            "left": "_implicit_",
                            "right": neq_m.group(1),
                        })
                        continue
                if neq_m:
                    left = neq_m.group(1)
                    right = neq_m.group(2)
                    if len(left) >= 2:
                        sub_constraints.append({
                            "kind": "not_equal",
                            "left": left,
                            "right": right,
                        })
                    else:
                        sub_constraints.append({
                            "kind": "not_equal",
                            "left": "_implicit_",
                            "right": right,
                        })
                    continue
                # Pattern: X是Y (including "第二盒是紫的")
                # Must not start with 不/没/未
                eq_m = re.search(r"(?<![不没未])([一-龥]+(?:盒|球|屉|位|号)?)是([一-龥]+?)(?:的)?$", part)
                if not eq_m:
                    # Bare "是Y" → implicit subject
                    eq_m = re.match(r"^是([一-龥]+?)(?:的)?[。；，,]?$", part.strip())
                    if eq_m:
                        sub_constraints.append({
                            "kind": "equal",
                            "left": "_implicit_",
                            "right": eq_m.group(1),
                        })
                        continue
                if eq_m:
                    left = eq_m.group(1)
                    right = eq_m.group(2)
                    if len(left) >= 2 or left in "甲乙丙丁戊己庚辛壬癸":
                        sub_constraints.append({
                            "kind": "equal",
                            "left": left,
                            "right": right,
                        })
                    else:
                        sub_constraints.append({
                            "kind": "equal",
                            "left": "_implicit_",
                            "right": right,
                        })
                    continue
                # Pattern: X在第N位
                pos_m = re.search(r"([一-龥]+)在第([一二三四五六七八九十1-9])位", part)
                if pos_m:
                    sub_constraints.append({
                        "kind": "position",
                        "left": pos_m.group(1),
                        "right": str(_cn_digit(pos_m.group(2))),
                    })
                    continue

            if len(sub_constraints) >= 2:
                constraints.append(AnalysisConstraint(
                    kind="half_true",
                    left=speaker,
                    value="1",  # expected true count
                    value2=sub_constraints,
                    raw=f"{speaker}: exactly 1 true of {len(sub_constraints)}",
                ))

    return constraints


def _parse_half_true_from_options(question_text: str, options: dict[str, str]) -> list[AnalysisConstraint]:
    """Parse half-true-half-false constraints from option text.

    For patterns like:
    A. 四班第一，三班第二，一班第三，二班第四
    B. 二班第一，一班第二，三班第三，四班第四

    Each option represents a complete assignment.
    The half-true constraint means each speaker's two claims have exactly one true.
    """
    constraints: list[AnalysisConstraint] = []

    # Extract speaker claims from question text
    # Pattern: X说/猜："claim1，claim2"
    speaker_claims = re.findall(
        r"([甲乙丙丁戊己庚辛壬癸]|小[一-龥])[说道猜][：:]?\s*(.+?)(?=[甲乙丙丁戊己庚辛壬癸][说道猜：]|小[一-龥][说道猜：]|结果|发现|猜完|每人|。[甲乙丙丁]|$)",
        question_text
    )

    for speaker, text in speaker_claims:
        # Split by comma
        parts = re.split(r"[，,、；]", text)
        if len(parts) >= 2:
            sub_constraints = []
            for part in parts[:2]:
                part = part.strip().rstrip("。；，,")
                if not part:
                    continue
                # Pattern: X第N个出场
                pos_m = re.search(r"([一-龥]+)第([一二三四五六七八九十1-9])个?出场", part)
                if pos_m:
                    sub_constraints.append({
                        "kind": "position",
                        "left": pos_m.group(1),
                        "right": str(_cn_digit(pos_m.group(2))),
                    })
                    continue
                # Pattern: X不是Y (check BEFORE X是Y)
                neq_m = re.search(r"(?<![不没未])([一-龥]+)不是([一-龥]+)", part)
                if not neq_m:
                    neq_m = re.match(r"^不是([一-龥]+?)[。；，,]?$", part.strip())
                    if neq_m:
                        sub_constraints.append({"kind": "not_equal", "left": "_implicit_", "right": neq_m.group(1)})
                        continue
                if neq_m:
                    left = neq_m.group(1)
                    right = neq_m.group(2)
                    if len(left) >= 2:
                        sub_constraints.append({"kind": "not_equal", "left": left, "right": right})
                    else:
                        sub_constraints.append({"kind": "not_equal", "left": "_implicit_", "right": right})
                    continue
                # Pattern: X是Y
                eq_m = re.search(r"(?<![不没未])([一-龥]+(?:盒|球|屉|位|号)?)是([一-龥]+?)(?:的)?$", part)
                if not eq_m:
                    eq_m = re.match(r"^是([一-龥]+?)(?:的)?[。；，,]?$", part.strip())
                    if eq_m:
                        sub_constraints.append({"kind": "equal", "left": "_implicit_", "right": eq_m.group(1)})
                        continue
                if eq_m:
                    left = eq_m.group(1)
                    right = eq_m.group(2)
                    if len(left) >= 2 or left in "甲乙丙丁戊己庚辛壬癸":
                        sub_constraints.append({"kind": "equal", "left": left, "right": right})
                    else:
                        sub_constraints.append({"kind": "equal", "left": "_implicit_", "right": right})
                    continue

            if len(sub_constraints) >= 2:
                constraints.append(AnalysisConstraint(
                    kind="half_true",
                    left=speaker,
                    value="1",
                    value2=sub_constraints,
                    raw=f"{speaker}: exactly 1 true of {len(sub_constraints)}",
                ))

    return constraints


def _cn_digit(s: str) -> int:
    """Convert Chinese digit to int."""
    cn = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
          "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    if s in cn:
        return cn[s]
    try:
        return int(s)
    except ValueError:
        return 0


# ---------------------------------------------------------------------------
# Option parsing
# ---------------------------------------------------------------------------

def extract_options(question_text: str) -> list[OptionClaim]:
    """Extract A/B/C/D options from question text."""
    options: list[OptionClaim] = []
    pattern = re.compile(
        r"([A-D])\s*[.、:：]\s*(.+?)(?=\s*[A-D]\s*[.、:：]|$)",
        re.DOTALL
    )
    for m in pattern.finditer(question_text):
        label = m.group(1)
        text = m.group(2).strip()
        text = re.split(r"\s*[A-D]\s*[.、:：]", text)[0].strip()
        text = text.rstrip("。；;，,")
        if text:
            options.append(OptionClaim(label=label, raw=text))
    return options


def parse_option_assignments(option: OptionClaim) -> dict[str, str] | None:
    """Parse option text into variable->value assignments."""
    text = option.raw
    assignments: dict[str, str] = {}

    # Pattern: X是Y
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)是([一-龥]+?)(?:，|、|。|$)", text):
        assignments[m.group(1)] = m.group(2)

    # Pattern: X研究Y
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)研究([一-龥]+?)(?:，|、|。|$)", text):
        assignments[m.group(1)] = m.group(2)

    # Pattern: X会Y
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)会([一-龥]+?)(?:，|、|。|$)", text):
        assignments[m.group(1)] = m.group(2)

    # Pattern: X在第N位
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)在第([一二三四五六七八九十1-9])位", text):
        assignments[m.group(1)] = str(_cn_digit(m.group(2)))

    # Pattern: X排第N
    for m in re.finditer(r"([甲乙丙丁戊己庚辛壬癸一-龥A-G小大]+)排第([一二三四五六七八九十1-9])", text):
        assignments[m.group(1)] = str(_cn_digit(m.group(2)))

    # Pattern: X第N (e.g., "四班第一")
    for m in re.finditer(r"([一-龥]+?)第([一二三四五六七八九十1-9])", text):
        assignments[m.group(1)] = str(_cn_digit(m.group(2)))

    # Pattern: 第N个盒子内的皮球是Y → 第N盒=Y
    for m in re.finditer(r"第([一二三四五六七八九十1-9])个?(?:盒子|抽屉|柜子)?(?:内|里)?(?:的)?(?:皮球|球|物品)?是([一-龥]+?)(?:的)?(?:，|、|。|$)", text):
        var_name = f"第{m.group(1)}盒"
        val = m.group(2)
        assignments[var_name] = val

    if assignments:
        return assignments
    return None


# ---------------------------------------------------------------------------
# Assignment generation and filtering
# ---------------------------------------------------------------------------

def generate_assignments(variables: list[AnalysisVariable]) -> list[dict[str, str]]:
    """Generate all possible assignments (permutations of domain values)."""
    if not variables or not variables[0].domain:
        return []

    domain = variables[0].domain
    n_vars = len(variables)
    n_domain = len(domain)

    # Check search space
    if n_vars > MAX_VARIABLES:
        return []  # too large

    # Permutation: each variable gets a unique value from domain
    if n_vars == n_domain:
        perms = list(permutations(domain))
        if len(perms) > MAX_PERMUTATIONS:
            return []
        return [{v.name: val for v, val in zip(variables, perm)} for perm in perms]

    # Cartesian product: variables can share values
    cart = list(product(domain, repeat=n_vars))
    if len(cart) > MAX_CARTESIAN:
        return []
    return [{v.name: val for v, val in zip(variables, combo)} for combo in cart]


def check_constraint(assignment: dict[str, str], constraint: AnalysisConstraint) -> bool | None:
    """Check if an assignment satisfies a constraint. Returns None if undetermined."""
    kind = constraint.kind

    if kind == "equal":
        left_val = str(assignment.get(constraint.left, ""))
        right_val = str(constraint.right or "")
        if right_val in left_val or left_val in right_val:
            return True
        return None

    if kind == "not_equal":
        left_val = str(assignment.get(constraint.left, ""))
        right_val = str(constraint.right or "")
        if right_val in left_val or left_val in right_val:
            return False
        return None

    if kind == "position":
        left_val = assignment.get(constraint.left, "")
        if constraint.value == "min":
            # Check if left has the smallest position
            try:
                left_num = int(left_val)
                all_vals = [int(v) for v in assignment.values() if v]
                return left_num == min(all_vals)
            except (ValueError, TypeError):
                return None
        elif constraint.value == "max":
            try:
                left_num = int(left_val)
                all_vals = [int(v) for v in assignment.values() if v]
                return left_num == max(all_vals)
            except (ValueError, TypeError):
                return None
        else:
            left_val_str = str(left_val)
            if left_val_str == str(constraint.value):
                return True
            return None

    if kind == "left_of":
        left_pos = assignment.get(constraint.left)
        right_pos = assignment.get(constraint.right)
        if left_pos is not None and right_pos is not None:
            try:
                return int(left_pos) < int(right_pos)
            except (ValueError, TypeError):
                pass
        return None

    if kind == "right_of":
        left_pos = assignment.get(constraint.left)
        right_pos = assignment.get(constraint.right)
        if left_pos is not None and right_pos is not None:
            try:
                return int(left_pos) > int(right_pos)
            except (ValueError, TypeError):
                pass
        return None

    if kind == "adjacent":
        left_pos = assignment.get(constraint.left)
        right_pos = assignment.get(constraint.right)
        if left_pos is not None and right_pos is not None:
            try:
                return abs(int(left_pos) - int(right_pos)) == 1
            except (ValueError, TypeError):
                pass
        return None

    if kind == "same_group":
        left_val = assignment.get(constraint.left)
        right_val = assignment.get(constraint.right)
        if left_val is not None and right_val is not None:
            return left_val == right_val
        return None

    if kind == "diff_group":
        left_val = assignment.get(constraint.left)
        right_val = assignment.get(constraint.right)
        if left_val is not None and right_val is not None:
            return left_val != right_val
        return None

    if kind == "comparison":
        # For comparison, we need to check relative ordering
        # This is handled separately in filter_consistent_assignments
        return None

    if kind == "half_true":
        # Half-true-half-false: exactly one of the two claims is true
        # This is handled separately in filter_consistent_assignments
        return None

    return None


def filter_consistent_assignments(
    assignments: list[dict[str, str]],
    constraints: list[AnalysisConstraint],
) -> list[dict[str, str]]:
    """Filter assignments that satisfy all constraints."""
    consistent = []
    for assignment in assignments:
        valid = True
        for constraint in constraints:
            result = check_constraint(assignment, constraint)
            if result is False:
                valid = False
                break

        # Check comparison constraints
        if valid:
            for constraint in constraints:
                if constraint.kind == "comparison":
                    if not _check_comparison(assignment, constraint):
                        valid = False
                        break

        # Check half-true constraints
        if valid:
            half_true_constraints = [c for c in constraints if c.kind == "half_true"]
            for ht in half_true_constraints:
                if not _check_half_true(assignment, ht):
                    valid = False
                    break

        if valid:
            consistent.append(assignment)
    return consistent


def _check_comparison(assignment: dict[str, str], constraint: AnalysisConstraint) -> bool:
    """Check comparison constraint against assignment."""
    left_name = constraint.left or ""
    right_name = constraint.right or ""
    relation = constraint.relation or ""

    # Find the position/value of left and right in assignment
    left_val = None
    right_val = None

    for var, val in assignment.items():
        # Check if variable name matches
        if var == left_name:
            try:
                left_val = int(val)
            except (ValueError, TypeError):
                left_val = val
        if var == right_name:
            try:
                right_val = int(val)
            except (ValueError, TypeError):
                right_val = val
        # Check if variable value matches (domain value lookup)
        if val == left_name:
            try:
                left_val = int(var)
            except (ValueError, TypeError):
                left_val = var
        if val == right_name:
            try:
                right_val = int(var)
            except (ValueError, TypeError):
                right_val = var

    if left_val is None or right_val is None:
        return True  # Can't determine, assume consistent

    if isinstance(left_val, int) and isinstance(right_val, int):
        if relation == "greater":
            return left_val > right_val
        elif relation == "less":
            return left_val < right_val
        elif relation == "equal":
            return left_val == right_val

    return True


def _check_half_true(assignment: dict[str, str], constraint: AnalysisConstraint) -> bool:
    """Check half-true-half-false constraint.

    The constraint has 'parts' (sub-constraints) and 'expected_true_count'.
    We check how many of the parts are satisfied by the assignment.
    """
    parts = constraint.value2  # stored as list of (left, right, kind) tuples
    if not parts:
        return True

    true_count = 0
    for part in parts:
        part_kind = part.get("kind", "equal")
        part_left = part.get("left", "")
        part_right = part.get("right", "")

        if part_kind == "equal":
            if part_left == "_implicit_":
                # Implicit subject: check if any variable has this value
                for var, val in assignment.items():
                    if str(part_right) in str(val) or str(val) in str(part_right):
                        true_count += 1
                        break
            else:
                left_val = str(assignment.get(part_left, ""))
                right_val = str(part_right)
                if right_val in left_val or left_val in right_val:
                    true_count += 1
        elif part_kind == "not_equal":
            if part_left == "_implicit_":
                # Implicit subject: check if any variable does NOT have this value
                all_match = True
                for var, val in assignment.items():
                    if str(part_right) not in str(val) and str(val) not in str(part_right):
                        all_match = False
                        break
                if not all_match:
                    true_count += 1
            else:
                left_val = str(assignment.get(part_left, ""))
                right_val = str(part_right)
                if right_val not in left_val and left_val not in right_val:
                    true_count += 1
        elif part_kind == "position":
            left_val = assignment.get(part_left, "")
            if str(left_val) == str(part_right):
                true_count += 1

    expected = int(constraint.value or 1)
    return true_count == expected


# ---------------------------------------------------------------------------
# Option evaluation
# ---------------------------------------------------------------------------

def evaluate_option(
    option: OptionClaim,
    consistent_assignments: list[dict[str, str]],
    task_type: str,
) -> dict[str, Any]:
    """Evaluate an option against consistent assignments."""
    option_assignments = parse_option_assignments(option)

    if option_assignments is None:
        return {"status": "unknown", "supporting": 0, "total": len(consistent_assignments)}

    supporting = 0
    contradicting = 0

    for assignment in consistent_assignments:
        match = True
        matched_any = False
        for var, val in option_assignments.items():
            if var in assignment:
                matched_any = True
                # Check if assignment value matches option value
                if val not in str(assignment[var]) and str(assignment[var]) not in val:
                    match = False
                    break
        if not matched_any:
            match = False
        if match:
            supporting += 1
        else:
            contradicting += 1

    total = len(consistent_assignments)

    if total == 0:
        return {"status": "unknown", "supporting": 0, "total": 0}

    if supporting == total:
        return {"status": "must_true", "supporting": supporting, "total": total}
    elif supporting > 0:
        return {"status": "possible", "supporting": supporting, "total": total}
    else:
        return {"status": "impossible", "supporting": 0, "total": total}


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve_analysis_core(question_text: str, options: dict[str, str] | None = None) -> AnalysisReasoningResult:
    """Solve an analysis reasoning question.

    Returns an AnalysisReasoningResult with status:
    - solved: exactly one consistent assignment or unique option
    - ambiguous: multiple consistent assignments
    - inconsistent: no consistent assignments
    - analysis_only: could not parse enough structure
    """
    # Classify task
    task_type = classify_analysis_task(question_text)

    # Extract options first (needed for domain extraction)
    raw_options = extract_options(question_text)
    if not raw_options and options:
        raw_options = [OptionClaim(label=l, raw=t) for l, t in sorted(options.items())]

    # Strip options from question text for constraint parsing
    # (options should not be parsed as constraints)
    stem_text = question_text
    if raw_options:
        for opt in raw_options:
            # Remove option text from stem
            stem_text = stem_text.replace(opt.raw, "").strip()
        # Also remove "A. " "B. " etc. prefixes
        stem_text = re.sub(r"\s*[A-D]\s*[.、:：]\s*", " ", stem_text).strip()

    # Extract variables and domains from question text + options
    variables = extract_variables_and_domains(question_text, raw_options if raw_options else None, task_type)
    if not variables:
        return AnalysisReasoningResult(
            status="analysis_only",
            task_type=task_type,
            warnings=["no_variables_extracted"],
        )

    # Check if we have domains
    if not variables[0].domain:
        # Try to infer domain from options
        if raw_options:
            opt_domains = _extract_domain_from_options(raw_options)
            if opt_domains:
                for v in variables:
                    object.__setattr__(v, 'domain', tuple(opt_domains))

    if not variables[0].domain:
        return AnalysisReasoningResult(
            status="analysis_only",
            task_type=task_type,
            variables=variables,
            warnings=["no_domain_extracted"],
        )

    # Parse constraints
    constraints = parse_constraints(stem_text)

    # Also parse half-true constraints from options if available
    if options:
        half_true_from_opts = _parse_half_true_from_options(question_text, options)
        constraints.extend(half_true_from_opts)

    # Generate assignments
    all_assignments = generate_assignments(variables)
    if not all_assignments:
        return AnalysisReasoningResult(
            status="analysis_only",
            task_type=task_type,
            variables=variables,
            constraints=constraints,
            warnings=["search_space_too_large"],
        )

    # Filter consistent assignments
    consistent = filter_consistent_assignments(all_assignments, constraints)

    # Extract and evaluate options
    option_status = "not_attempted"
    predicted_label = None
    option_trace: list[dict[str, Any]] = []

    if raw_options and consistent:
        # Determine question type
        is_possible = "可能" in question_text and "为真" in question_text
        is_must = "一定" in question_text and "为真" in question_text
        is_impossible = "不可能" in question_text or "不能推出" in question_text
        is_except = "除了" in question_text or "错误" in question_text or "不符" in question_text

        for opt in raw_options:
            eval_result = evaluate_option(opt, consistent, task_type)
            option_trace.append({
                "label": opt.label,
                "raw": opt.raw[:60],
                "status": eval_result["status"],
                "supporting": eval_result["supporting"],
                "total": eval_result["total"],
            })

        # Determine predicted label
        if is_except:
            # "except" question: find the one that's NOT must_true (i.e., could be false)
            # Options that are "must_true" in all assignments are correct
            # The "except" answer is the one that's NOT always true
            always_true = [t for t in option_trace if t["status"] == "must_true"]
            not_always_true = [t for t in option_trace if t["status"] != "must_true"]
            if len(not_always_true) == 1:
                predicted_label = not_always_true[0]["label"]
                option_status = "unique_supported"
            elif len(not_always_true) == 0:
                option_status = "no_supported_option"
            else:
                option_status = "ambiguous_options"
        elif is_possible:
            candidates = [t for t in option_trace if t["status"] in ("possible", "must_true")]
            if len(candidates) == 1:
                predicted_label = candidates[0]["label"]
                option_status = "unique_supported"
        elif is_must or not is_impossible:
            candidates = [t for t in option_trace if t["status"] == "must_true"]
            if len(candidates) == 1:
                predicted_label = candidates[0]["label"]
                option_status = "unique_supported"
            elif len(candidates) > 1:
                option_status = "ambiguous_options"
            else:
                # No must_true, check possible
                possible = [t for t in option_trace if t["status"] == "possible"]
                if len(possible) == 1:
                    predicted_label = possible[0]["label"]
                    option_status = "unique_supported"
                elif len(possible) > 1:
                    option_status = "ambiguous_options"
                else:
                    option_status = "no_supported_option"

        # Default: if still not_attempted, set based on option_trace
        if option_status == "not_attempted" and option_trace:
            option_status = "no_supported_option"

    # Determine overall status
    if not consistent:
        status = "inconsistent"
    elif len(consistent) == 1 and predicted_label:
        status = "solved"
    elif predicted_label and option_status == "unique_supported":
        status = "solved"
    elif len(consistent) > 1:
        status = "ambiguous"
    else:
        status = "analysis_only"

    return AnalysisReasoningResult(
        status=status,
        task_type=task_type,
        variables=variables,
        constraints=constraints,
        assignments=consistent,
        option_status=option_status,
        predicted_label=predicted_label,
        option_trace=option_trace,
        warnings=[],
    )
