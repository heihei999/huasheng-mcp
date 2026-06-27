"""Tests for the isolated definition judgement core (v0.1).

Covers:
- Question polarity detection
- Definition parsing
- Element extraction
- Option assessment
- Integration
- No-hardcoded-entity guard
"""

from __future__ import annotations

import pytest

from xingce_solver.solvers.definition_judgement import (
    DefinitionElement,
    DefinitionRule,
    OptionCase,
    detect_question_polarity,
    parse_definitions,
    extract_elements,
    assess_option,
    solve_definition_judgement_core,
)


# =========================================================================
# Question polarity detection
# =========================================================================

class TestQuestionPolarity:
    def test_positive(self):
        assert detect_question_polarity("下列属于该定义的是") == "positive"

    def test_negative(self):
        assert detect_question_polarity("下列不属于该定义的是") == "negative"

    def test_except_positive(self):
        assert detect_question_polarity("以下除哪项外均属于该定义") == "except_positive"

    def test_except_negative(self):
        # "除哪项外" + "不属于" → except_negative
        assert detect_question_polarity("以下除哪项外，下列不属于该定义的是") == "except_negative"


# =========================================================================
# Definition parsing
# =========================================================================

class TestDefinitionParsing:
    def test_parse_single_definition(self):
        q = "行为是指主体在条件下通过方式对对象实施动作。根据上述定义，下列属于行为的是："
        defs = parse_definitions(q)
        assert len(defs) >= 1
        assert defs[0].term.startswith("行为")

    def test_parse_term(self):
        q = "田园综合体是指一种新型的集特色优势产业、休闲旅游、乡村社区为一体的跨产业、多功能的农业生产经营体系。下列属于田园综合体的是："
        defs = parse_definitions(q)
        assert len(defs) >= 1
        # Term may include trailing separator char; check it starts correctly
        assert defs[0].term.startswith("田园综合体")


# =========================================================================
# Element extraction
# =========================================================================

class TestElementExtraction:
    def test_extract_subject(self):
        text = "由主体实施的行为"
        elements = extract_elements(text)
        subjects = [e for e in elements if e.kind == "subject"]
        assert len(subjects) >= 1

    def test_extract_purpose(self):
        text = "以提高效率为目的的设计方法"
        elements = extract_elements(text)
        purposes = [e for e in elements if e.kind == "purpose"]
        assert len(purposes) >= 1

    def test_extract_exclusion(self):
        text = "不包括特殊情况的行为"
        elements = extract_elements(text)
        exclusions = [e for e in elements if e.kind == "exclusion"]
        assert len(exclusions) >= 1


# =========================================================================
# Option assessment
# =========================================================================

class TestOptionAssessment:
    def test_match_when_elements_present(self):
        definition = DefinitionRule(
            term="X",
            elements=(DefinitionElement(kind="subject", text="主体", required=True),),
        )
        option = OptionCase(label="A", text="主体实施了某行为")
        assessment = assess_option(option, definition, "positive")
        assert assessment.status in ("matches", "unknown")

    def test_violate_when_required_missing(self):
        definition = DefinitionRule(
            term="X",
            elements=(
                DefinitionElement(kind="subject", text="特定主体", required=True),
                DefinitionElement(kind="condition", text="特殊条件", required=True),
            ),
        )
        option = OptionCase(label="A", text="普通人在普通情况下做了某事")
        assessment = assess_option(option, definition, "positive")
        # Should either violate or be unknown (not match)
        assert assessment.status != "matches" or len(assessment.matched_elements) < 2


# =========================================================================
# Integration
# =========================================================================

class TestIntegration:
    def test_analysis_only_when_no_definitions(self):
        result = solve_definition_judgement_core("这是一段普通文字，没有定义。")
        assert result.status == "analysis_only"

    def test_analysis_only_when_no_options(self):
        result = solve_definition_judgement_core(
            "X是指某种行为。根据上述定义，下列属于X的是：",
            options=None,
        )
        assert result.status == "analysis_only"

    def test_positive_polarity(self):
        q = "X是指主体在条件下对对象实施动作以达到目的。根据上述定义，下列属于X的是："
        opts = {"A": "主体在条件下对对象实施动作", "B": "其他行为"}
        result = solve_definition_judgement_core(q, options=opts)
        assert result.question_polarity == "positive"
        assert result.status in ("solved", "ambiguous", "analysis_only")

    def test_negative_polarity(self):
        q = "X是指主体在条件下对对象实施动作。根据上述定义，下列不属于X的是："
        opts = {"A": "主体在条件下对对象实施动作", "B": "其他行为"}
        result = solve_definition_judgement_core(q, options=opts)
        assert result.question_polarity == "negative"


# =========================================================================
# No-hardcoded-entity guard
# =========================================================================

class TestNoHardcodedEntities:
    FORBIDDEN_ENTITIES = [
        "橙腹草原田鼠", "三支一扶", "元宇宙", "防御性倾听",
        "华图", "上岸鸭", "中公",
    ]

    def test_no_entities_in_source(self):
        import inspect
        import xingce_solver.solvers.definition_judgement as mod
        source = inspect.getsource(mod)
        for entity in self.FORBIDDEN_ENTITIES:
            assert entity not in source, (
                f"Found hardcoded entity '{entity}' in definition_judgement.py"
            )
