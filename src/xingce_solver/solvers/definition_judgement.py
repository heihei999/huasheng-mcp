"""Isolated definition judgement core for logic judgment questions.

This module implements a minimal structured definition judge for
"定义判断" questions commonly found in Chinese civil service exams.

It is NOT integrated into solve_logic_reasoning. It is a standalone
engine for testing the core algorithm in isolation.

Version: v0.1
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DefinitionElement:
    """An element extracted from a definition."""
    kind: str  # subject, object, condition, method, purpose, result, exclusion, action, attribute, keyword
    text: str
    required: bool = True
    polarity: bool = True  # True = positive, False = negative (exclusion)
    raw: str = ""


@dataclass(frozen=True)
class DefinitionRule:
    """A parsed definition with its elements."""
    term: str
    elements: tuple[DefinitionElement, ...]
    raw_definition: str = ""
    definition_type: str = "single"  # single, multi_target, classification


@dataclass(frozen=True)
class OptionCase:
    """A parsed answer option."""
    label: str
    text: str


@dataclass
class OptionAssessment:
    """Assessment of an option against a definition."""
    label: str
    status: str  # matches, violates, unknown
    matched_elements: list[str] = field(default_factory=list)
    missing_elements: list[str] = field(default_factory=list)
    violated_elements: list[str] = field(default_factory=list)
    unknown_elements: list[str] = field(default_factory=list)
    score: float = 0.0
    trace: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class DefinitionJudgementResult:
    """Result of the definition judgement engine."""
    status: str  # solved / ambiguous / analysis_only / inconsistent
    question_polarity: str = "unknown"
    target_definition: str | None = None
    definitions: list[DefinitionRule] = field(default_factory=list)
    options: list[OptionCase] = field(default_factory=list)
    assessments: list[OptionAssessment] = field(default_factory=list)
    option_status: str = "not_attempted"
    predicted_label: str | None = None
    confidence: float = 0.0
    warnings: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Question polarity detection
# ---------------------------------------------------------------------------

def detect_question_polarity(question_text: str) -> str:
    """Detect the question polarity from the question text."""
    # Check except patterns FIRST (before negative/positive)
    if re.search(r"除哪项外|除哪项外均|以下除哪项外|下列除哪项外", question_text):
        if re.search(r"不属于|不符合|不能体现|没有体现", question_text):
            return "except_negative"
        return "except_positive"

    # Negative patterns (high priority)
    if re.search(r"不属于|不符合|不能体现|没有体现|不满足|下列不属于|下列不符合|没有体现|不正确的|错误的|错误的是|不正确的是|没有体现|违背", question_text):
        return "negative"

    # Positive patterns
    if re.search(r"属于|符合|体现|满足|下列属于|下列符合|可以体现|正确的|正确的是|与定义相符|对应正确", question_text):
        return "positive"

    return "unknown"


# ---------------------------------------------------------------------------
# Definition parsing
# ---------------------------------------------------------------------------

def parse_definitions(question_text: str) -> list[DefinitionRule]:
    """Parse definitions from question text."""
    definitions: list[DefinitionRule] = []

    # Split by "。" to find definition sentences
    sentences = re.split(r"[。；]", question_text)

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue

        # Pattern 1: "X是指..." or "X指的是..." or "X指..." or "X即..." or "X所谓..."
        # Use non-greedy match and ensure term doesn't end with 是
        m = re.search(
            r"([一-龥]{2,10}?)(?:是指|指的是|指|即|所谓)\s*(.+)",
            sent
        )
        if m:
            term = m.group(1).strip()
            defn_text = m.group(2).strip()
            if len(defn_text) >= 10:
                elements = extract_elements(defn_text)
                definitions.append(DefinitionRule(
                    term=term,
                    elements=tuple(elements),
                    raw_definition=defn_text,
                ))
                continue

        # Pattern 2: "X：..." (colon format)
        m = re.search(r"([一-龥]{2,10})\s*[：:]\s*(.+)", sent)
        if m:
            term = m.group(1).strip()
            defn_text = m.group(2).strip()
            if len(defn_text) >= 10:
                elements = extract_elements(defn_text)
                definitions.append(DefinitionRule(
                    term=term,
                    elements=tuple(elements),
                    raw_definition=defn_text,
                ))

    return definitions


def extract_elements(definition_text: str) -> list[DefinitionElement]:
    """Extract key elements from a definition text.

    Focus on extracting short, meaningful concepts rather than full phrases.
    """
    elements: list[DefinitionElement] = []

    # Subject: "由X实施" / "X实施" patterns
    for m in re.finditer(r"由([一-龥]{2,6}?)(?:实施|进行|完成|提供|来做)", definition_text):
        elements.append(DefinitionElement(kind="subject", text=m.group(1), required=True, raw=m.group()))

    # Object: "对X" patterns (short)
    for m in re.finditer(r"对([一-龥]{2,6}?)(?:实施|进行|提供|产生|造成|的|进行)", definition_text):
        elements.append(DefinitionElement(kind="object", text=m.group(1), required=True, raw=m.group()))

    # Condition: "在X情况下/时" (short)
    for m in re.finditer(r"在([一-龥]{2,10}?)(?:情况|条件|状态|下|时)", definition_text):
        elements.append(DefinitionElement(kind="condition", text=m.group(1).strip(), required=True, raw=m.group()))

    # Method: "通过X" / "采用X" / "运用X" (short)
    for m in re.finditer(r"(?:通过|采用|运用)([一-龥]{2,10}?)(?:来|实现|达到|产生|获得|进行|的)", definition_text):
        elements.append(DefinitionElement(kind="method", text=m.group(1).strip(), required=True, raw=m.group()))

    # Purpose: "为了X" / "以X为目的"
    for m in re.finditer(r"(?:为了|以)([一-龥]{2,10}?)(?:为目的|为目标|为目的的)", definition_text):
        elements.append(DefinitionElement(kind="purpose", text=m.group(1).strip(), required=True, raw=m.group()))

    # Result: "导致X" / "产生X"
    for m in re.finditer(r"(?:从而|进而|导致|造成|产生|使得)([一-龥]{2,10}?)(?:[，。；]|$)", definition_text):
        elements.append(DefinitionElement(kind="result", text=m.group(1).strip(), required=True, raw=m.group()))

    # Exclusion: "不包括X" / "除X外"
    for m in re.finditer(r"(?:不包括|除了|除……外|排除|例外)([一-龥]{2,10}?)(?:[，。；]|$)", definition_text):
        elements.append(DefinitionElement(kind="exclusion", text=m.group(1).strip(), required=True, polarity=False, raw=m.group()))

    # Attribute: "特点为X" / "特征是X"
    for m in re.finditer(r"(?:特点|特征|性质|属性)(?:多为|为|是)([一-龥]{2,10}?)(?:[，。；]|$)", definition_text):
        elements.append(DefinitionElement(kind="attribute", text=m.group(1).strip(), required=True, raw=m.group()))

    # If no elements found, extract key noun phrases
    if not elements:
        keywords = re.findall(r"[一-龥]{2,6}", definition_text)
        seen = set()
        for kw in keywords:
            if kw not in seen and len(kw) >= 2:
                seen.add(kw)
                elements.append(DefinitionElement(kind="keyword", text=kw, required=False, raw=kw))
                if len(elements) >= 5:
                    break

    return elements


# ---------------------------------------------------------------------------
# Option parsing
# ---------------------------------------------------------------------------

def parse_options(options_dict: dict[str, str]) -> list[OptionCase]:
    """Parse options from the options dict."""
    return [
        OptionCase(label=label, text=text)
        for label, text in sorted(options_dict.items())
    ]


# ---------------------------------------------------------------------------
# Option assessment
# ---------------------------------------------------------------------------

def assess_option(
    option: OptionCase,
    definition: DefinitionRule,
    polarity: str,
) -> OptionAssessment:
    """Assess an option against a definition using keyword-based scoring."""
    matched = []
    missing = []
    violated = []
    unknown = []

    option_text = option.text
    defn_text = definition.raw_definition

    # Extract meaningful keywords from definition
    # Use definition term + short phrases from punctuation splits
    defn_keywords: set[str] = set()

    # Add the definition term itself
    if definition.term:
        defn_keywords.add(definition.term)

    # Split on punctuation and take short meaningful phrases
    for phrase in re.split(r"[，。；、（）()：:]", defn_text):
        phrase = phrase.strip()
        if 2 <= len(phrase) <= 8:
            defn_keywords.add(phrase)

    # Match definition keywords in option text
    matched_keywords: list[str] = []
    for kw in defn_keywords:
        if kw in option_text:
            matched_keywords.append(kw)

    # Check each element against option
    for elem in definition.elements:
        elem_text = elem.text
        if not elem_text:
            continue

        elem_norm = elem_text.strip()
        opt_norm = option_text.strip()

        is_matched = False

        # Exact substring match
        if elem_norm in opt_norm:
            is_matched = True
        elif _fuzzy_contains(elem_norm, opt_norm):
            is_matched = True
        else:
            # Keyword overlap
            elem_words = set(re.findall(r"[一-龥]{2,}", elem_norm))
            opt_words = set(re.findall(r"[一-龥]{2,}", opt_norm))
            overlap = elem_words & opt_words
            if len(overlap) >= max(1, len(elem_words) // 2):
                is_matched = True

        if is_matched:
            if elem.polarity:
                matched.append(elem.kind)
            else:
                violated.append(elem.kind)
        else:
            if elem.required and elem.polarity:
                missing.append(elem.kind)
            elif not elem.required:
                unknown.append(elem.kind)

    # Calculate score based on keyword overlap and element matching
    keyword_score = len(matched_keywords) / max(1, len(defn_keywords))
    element_score = len(matched) / max(1, len(definition.elements)) if definition.elements else 0
    violation_penalty = len(violated) * 0.3

    # Combined score
    score = keyword_score * 0.6 + element_score * 0.4 - violation_penalty

    # Determine status
    if violated:
        status = "violates"
    elif score > 0.3 and not missing:
        status = "matches"
    elif score > 0.2:
        status = "matches" if score > 0.3 else "unknown"
    elif missing:
        status = "violates"
    else:
        status = "unknown"

    return OptionAssessment(
        label=option.label,
        status=status,
        matched_elements=matched,
        missing_elements=missing,
        violated_elements=violated,
        unknown_elements=unknown,
        score=score,
    )


def _fuzzy_contains(needle: str, haystack: str) -> bool:
    """Check if needle is approximately contained in haystack."""
    # Simple character overlap check
    if len(needle) < 2:
        return False
    # Check if all characters of needle appear in haystack in order
    idx = 0
    for ch in haystack:
        if idx < len(needle) and ch == needle[idx]:
            idx += 1
    return idx == len(needle)


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve_definition_judgement_core(
    question_text: str,
    options: dict[str, str] | None = None,
) -> DefinitionJudgementResult:
    """Solve a definition judgement question.

    Returns a DefinitionJudgementResult with status:
    - solved: exactly one option uniquely matches/violates
    - ambiguous: multiple options could match/violate
    - analysis_only: could not parse enough structure
    - inconsistent: input structure self-contradicts
    """
    warnings: list[str] = []

    # Detect polarity
    polarity = detect_question_polarity(question_text)

    # Parse definitions
    definitions = parse_definitions(question_text)
    if not definitions:
        return DefinitionJudgementResult(
            status="analysis_only",
            question_polarity=polarity,
            warnings=["no_definitions_parsed"],
        )

    # Parse options
    if not options:
        return DefinitionJudgementResult(
            status="analysis_only",
            question_polarity=polarity,
            definitions=definitions,
            warnings=["no_options_provided"],
        )

    option_cases = parse_options(options)

    # Determine target definition
    target_def = definitions[0]  # Default to first
    target_term = None

    # Check for multi-definition with target
    if len(definitions) > 1:
        # Look for "属于X" or "下列属于X" pattern
        m = re.search(r"属于([一-龥]+?)(?:的是|的)", question_text)
        if m:
            target_term = m.group(1).strip()
            for d in definitions:
                if d.term == target_term:
                    target_def = d
                    break

    # Assess each option
    assessments: list[OptionAssessment] = []
    for opt in option_cases:
        assessment = assess_option(opt, target_def, polarity)
        assessments.append(assessment)

    # Determine result based on polarity and scores
    predicted = None
    option_status = "not_attempted"

    # Sort assessments by score
    scored = sorted(assessments, key=lambda a: a.score, reverse=True)

    if polarity == "positive":
        # Find the best matching option
        if scored and scored[0].score > 0:
            # Check if the top option is clearly better than the rest
            top_score = scored[0].score
            second_score = scored[1].score if len(scored) > 1 else 0
            if top_score > second_score and scored[0].status != "violates":
                predicted = scored[0].label
                option_status = "unique_supported"
            elif top_score > 0:
                # Multiple options have positive scores
                option_status = "ambiguous_options"
            else:
                option_status = "no_supported_option"
        else:
            option_status = "no_supported_option"

    elif polarity == "negative":
        # Find the option that violates the definition
        violations = [a for a in assessments if a.status == "violates"]
        if len(violations) == 1:
            predicted = violations[0].label
            option_status = "unique_supported"
        elif len(violations) > 1:
            option_status = "ambiguous_options"
        else:
            # No clear violations — use score to find the weakest match
            if scored and scored[-1].score < scored[0].score:
                predicted = scored[-1].label
                option_status = "unique_supported"
            else:
                option_status = "no_supported_option"

    elif polarity in ("except_positive", "except_negative"):
        if polarity == "except_positive":
            non_matches = [a for a in assessments if a.status != "matches"]
            if len(non_matches) == 1:
                predicted = non_matches[0].label
                option_status = "unique_supported"
            elif len(non_matches) > 1:
                option_status = "ambiguous_options"
        else:
            non_violations = [a for a in assessments if a.status != "violates"]
            if len(non_violations) == 1:
                predicted = non_violations[0].label
                option_status = "unique_supported"
            elif len(non_violations) > 1:
                option_status = "ambiguous_options"

    # Determine overall status
    if predicted and option_status == "unique_supported":
        status = "solved"
    elif option_status == "ambiguous_options":
        status = "ambiguous"
    elif option_status == "no_supported_option":
        status = "ambiguous"
    else:
        status = "analysis_only"

    return DefinitionJudgementResult(
        status=status,
        question_polarity=polarity,
        target_definition=target_def.term if definitions else None,
        definitions=definitions,
        options=option_cases,
        assessments=assessments,
        option_status=option_status,
        predicted_label=predicted,
        confidence=0.75 if predicted else 0.0,
        warnings=warnings,
    )
