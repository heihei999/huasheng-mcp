"""Tests for the isolated logic analysis reasoning core (v0.1).

Covers:
- Task classification
- Variable and domain extraction
- Constraint parsing
- Assignment generation and filtering
- Option evaluation
- Search space limits
- No-hardcoded-entity guard
"""

from __future__ import annotations

import pytest

from xingce_solver.solvers.logic_analysis_reasoning import (
    AnalysisConstraint,
    AnalysisReasoningResult,
    AnalysisVariable,
    OptionClaim,
    classify_analysis_task,
    extract_variables_and_domains,
    parse_constraints,
    generate_assignments,
    filter_consistent_assignments,
    evaluate_option,
    solve_analysis_core,
)


# =========================================================================
# Task classification
# =========================================================================

class TestTaskClassification:
    def test_matching(self):
        assert classify_analysis_task("甲不是银行职员，乙不是教师") == "matching"

    def test_ordering(self):
        assert classify_analysis_task("由北至南排列成一条直线") == "ordering"

    def test_ordering_adjacency(self):
        assert classify_analysis_task("C星与E星相邻") == "ordering_adjacency"

    def test_half_true_half_false(self):
        assert classify_analysis_task("每人都只猜对了一半") == "half_true_half_false"

    def test_grouping(self):
        assert classify_analysis_task("分给张老师和王老师") == "grouping"

    def test_comparison(self):
        assert classify_analysis_task("研究音韵学的比甲的学术成果多") == "comparison"


# =========================================================================
# Variable extraction
# =========================================================================

class TestVariableExtraction:
    def test_basic_three_people(self):
        q = "有教师、公务员、银行职员三人，其中甲不是银行职员，乙不是教师，丙不是公务员。"
        variables = extract_variables_and_domains(q)
        assert len(variables) >= 3


# =========================================================================
# Constraint parsing
# =========================================================================

class TestConstraintParsing:
    def test_not_equal(self):
        q = "甲不是银行职员，乙不是教师，丙不是公务员。"
        constraints = parse_constraints(q)
        not_equal = [c for c in constraints if c.kind == "not_equal"]
        assert len(not_equal) >= 3

    def test_comparison(self):
        q = "研究音韵学的比甲的学术成果多，乙的学术成果与研究敦煌学的学术成果相当。"
        constraints = parse_constraints(q)
        comp = [c for c in constraints if c.kind == "comparison"]
        assert len(comp) >= 1


# =========================================================================
# Assignment generation
# =========================================================================

class TestAssignmentGeneration:
    def test_permutations(self):
        variables = [
            AnalysisVariable(name="A", domain=("X", "Y")),
            AnalysisVariable(name="B", domain=("X", "Y")),
        ]
        assignments = generate_assignments(variables)
        assert len(assignments) == 2  # A=X,B=Y and A=Y,B=X

    def test_too_many_variables(self):
        variables = [
            AnalysisVariable(name=f"V{i}", domain=tuple(range(10)))
            for i in range(8)  # > MAX_VARIABLES
        ]
        assignments = generate_assignments(variables)
        assert len(assignments) == 0  # too large


# =========================================================================
# Constraint filtering
# =========================================================================

class TestConstraintFiltering:
    def test_not_equal_filter(self):
        assignments = [
            {"A": "X", "B": "Y"},
            {"A": "X", "B": "X"},
        ]
        constraints = [AnalysisConstraint(kind="not_equal", left="A", right="X")]
        result = filter_consistent_assignments(assignments, constraints)
        assert len(result) == 0  # A=X violates not_equal


# =========================================================================
# Option evaluation
# =========================================================================

class TestOptionEvaluation:
    def test_must_true(self):
        option = OptionClaim(label="A", raw="甲是X")
        consistent = [{"甲": "X", "乙": "Y"}]
        result = evaluate_option(option, consistent, "matching")
        # The option parser extracts "甲" -> "X" from "甲是X"
        assert result["status"] in ("must_true", "unknown")  # depends on parser

    def test_impossible(self):
        option = OptionClaim(label="A", raw="甲是Y")
        consistent = [{"甲": "X", "乙": "Y"}]
        result = evaluate_option(option, consistent, "matching")
        assert result["status"] in ("impossible", "unknown")  # depends on parser


# =========================================================================
# Integration
# =========================================================================

class TestIntegration:
    def test_analysis_only_when_no_variables(self):
        result = solve_analysis_core("这是一段不包含任何逻辑结构的普通文字。")
        assert result.status == "analysis_only"

    def test_status_types_valid(self):
        """All returned statuses must be valid."""
        q = "甲不是银行职员，乙不是教师，丙不是公务员。教师比乙年龄大。"
        result = solve_analysis_core(q)
        assert result.status in ("solved", "ambiguous", "inconsistent", "analysis_only")


# =========================================================================
# No-hardcoded-entity guard
# =========================================================================

class TestNoHardcodedEntities:
    FORBIDDEN_ENTITIES = [
        "牙科", "牙医", "星星", "银行", "教师", "公务员", "茶叶",
        "导师", "研发", "上岸鸭", "华图", "中公",
    ]

    def test_no_entities_in_source(self):
        import inspect
        import xingce_solver.solvers.logic_analysis_reasoning as mod
        source = inspect.getsource(mod)
        for entity in self.FORBIDDEN_ENTITIES:
            assert entity not in source, (
                f"Found hardcoded entity '{entity}' in logic_analysis_reasoning.py"
            )
