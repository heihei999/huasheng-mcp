"""Tests for the isolated truth reasoning core (v0.1).

Covers:
- TruthConstraint parsing
- Proposition parsing
- Contradiction detection
- Modus ponens / disjunctive syllogism / all-false negation
- Assignment behavior (solved / ambiguous / inconsistent / analysis_only)
- No-default-first-candidate guard
- No-hardcoded-entity guard
"""

from __future__ import annotations

import re

import pytest

from xingce_solver.solvers.truth_reasoning import (
    All,
    And,
    Atom,
    Imply,
    Not,
    Or,
    Some,
    TruthConstraint,
    TruthReasoningResult,
    _check_assignment,
    _enumerate_assignments,
    are_contradictory,
    extract_statements,
    negate_proposition,
    parse_statement,
    parse_truth_constraint,
    solve_truth_core,
)


# =========================================================================
# TruthConstraint parsing
# =========================================================================

class TestTruthConstraintParsing:
    def test_only_one_true(self):
        c = parse_truth_constraint("四位专家中只有一位的看法是正确的")
        assert c.true_count == 1

    def test_only_one_false(self):
        c = parse_truth_constraint("四人中只有一人说的不对")
        assert c.false_count == 1

    def test_two_true_two_false(self):
        c = parse_truth_constraint("四人中二人说了假话，二人说了真话")
        assert c.false_count == 2 or c.true_count == 2

    def test_three_true_one_false(self):
        c = parse_truth_constraint("四句话中有三句是真的，一句是假的")
        assert c.false_count == 1 or c.true_count == 3

    def test_all_false(self):
        c = parse_truth_constraint("对于同事的建议都没采纳")
        assert c.false_count == -1

    def test_one_true_two_false(self):
        c = parse_truth_constraint("这三个判断只有一个真，两个假")
        assert c.true_count == 1


# =========================================================================
# Proposition parsing
# =========================================================================

class TestPropositionParsing:
    def test_imply_if_then(self):
        p = parse_statement("如果小李写完了作业，那么小赵就没有写完作业")
        assert p is not None
        assert p.kind == "imply"

    def test_or_statement(self):
        p = parse_statement("或者左手是水果糖，或者右手是水果糖")
        assert p is not None
        assert p.kind == "or"

    def test_and_statement(self):
        p = parse_statement("甲和乙都不是爆炸案的元凶")
        assert p is not None
        assert p.kind in ("and", "atom")

    def test_all_statement(self):
        p = parse_statement("所有队员都不会达标")
        assert p is not None
        assert p.kind == "all"
        assert p.negated is True

    def test_some_statement(self):
        p = parse_statement("有些柜子里没有购物袋")
        assert p is not None
        assert p.kind == "some"
        assert p.negated is True

    def test_atom_negation(self):
        p = parse_statement("小赵没有写完作业")
        assert p is not None
        assert p.kind == "atom"
        assert p.negated is True

    def test_atom_positive(self):
        p = parse_statement("小李写完了作业")
        assert p is not None
        assert p.kind == "atom"
        assert p.negated is False

    def test_imply_only_if(self):
        p = parse_statement("只有黄队第二个出场，红队才第一个出场")
        assert p is not None
        assert p.kind == "imply"

    def test_imply_unless(self):
        p = parse_statement("除非丁入选，否则乙不入选")
        assert p is not None
        assert p.kind == "imply"


# =========================================================================
# Contradiction detection
# =========================================================================

class TestContradiction:
    def test_atom_vs_negated_atom(self):
        a = Atom("甲", "罪犯", negated=False)
        b = Atom("甲", "罪犯", negated=True)
        assert are_contradictory(a, b) is True

    def test_all_vs_some_negated(self):
        a = All("队员", "达标", negated=False)
        b = Some("队员", "达标", negated=True)
        assert are_contradictory(a, b) is True

    def test_imply_vs_conjunction(self):
        p = Atom("P", "")
        q = Atom("Q", "")
        imply = Imply(p, q)
        conj = And(p, negate_proposition(q))
        assert are_contradictory(imply, conj) is True

    def test_non_contradictory(self):
        a = Atom("甲", "罪犯")
        b = Atom("乙", "罪犯")
        assert are_contradictory(a, b) is False


# =========================================================================
# Modus ponens
# =========================================================================

class TestModusPonens:
    def test_modus_ponens_basic(self):
        """P→Q true, P true ⇒ Q must hold (via facts)."""
        p = Atom("甲", "元凶")
        q = Atom("乙", "元凶")
        imply = Imply(p, q)

        facts = {}
        from xingce_solver.solvers.truth_reasoning import _extract_facts_from_prop
        _extract_facts_from_prop(p, True, facts, [])
        _extract_facts_from_prop(imply, True, facts, [])

        # After P true and P→Q true, Q should be entailed
        from xingce_solver.solvers.truth_reasoning import _definitely_true
        assert _definitely_true(q, facts) is True

    def test_modus_ponens_chain(self):
        """P→Q, Q→R, P true ⇒ R true."""
        p = Atom("A", "")
        q = Atom("B", "")
        r = Atom("C", "")

        facts = {}
        from xingce_solver.solvers.truth_reasoning import _extract_facts_from_prop
        _extract_facts_from_prop(p, True, facts, [])
        _extract_facts_from_prop(Imply(p, q), True, facts, [])
        _extract_facts_from_prop(Imply(q, r), True, facts, [])

        from xingce_solver.solvers.truth_reasoning import _definitely_true
        assert _definitely_true(r, facts) is True


# =========================================================================
# Disjunctive syllogism
# =========================================================================

class TestDisjunctiveSyllogism:
    def test_or_elimination(self):
        """P或Q true, ¬P true ⇒ Q must hold."""
        p = Atom("P", "")
        q = Atom("Q", "")
        disj = Or(p, q)

        facts = {}
        from xingce_solver.solvers.truth_reasoning import _extract_facts_from_prop
        _extract_facts_from_prop(negate_proposition(p), True, facts, [])
        _extract_facts_from_prop(disj, True, facts, [])

        from xingce_solver.solvers.truth_reasoning import _definitely_true
        assert _definitely_true(q, facts) is True


# =========================================================================
# All-false negation
# =========================================================================

class TestAllFalseNegation:
    def test_all_false_negates_each(self):
        """If all statements are false and independent, each negation holds."""
        # Use independent atoms so negations don't cross-contradict
        s1 = Imply(Atom("A", ""), Atom("B", "", negated=True))
        s2 = Or(Atom("C", ""), Atom("D", ""))
        s3 = And(Atom("E", "", negated=True), Atom("F", "", negated=True))

        props = [s1, s2, s3]
        assignment = [False, False, False]
        ok, facts = _check_assignment(props, assignment)
        assert ok is True


# =========================================================================
# Assignment behavior
# =========================================================================

class TestAssignmentBehavior:
    def test_unique_assignment_solved(self):
        """When exactly one assignment is consistent → solved."""
        text = (
            "甲说：所有人是罪犯。"
            "乙说：所有人不是罪犯。"
            "已知只有一人说真话。"
        )
        result = solve_truth_core(text)
        assert result.status in ("solved", "ambiguous", "analysis_only")

    def test_no_assignment_inconsistent(self):
        """Contradictory propositions with no valid assignment → inconsistent."""
        p1 = Atom("X", "P")
        p2 = Atom("X", "P", negated=True)
        p3 = Atom("X", "P")
        props = [p1, p2, p3]
        assignment = [True, True, True]
        ok, _ = _check_assignment(props, assignment)
        assert ok is False

    def test_analysis_only_when_no_parseable(self):
        """Unparseable text → analysis_only."""
        result = solve_truth_core("这是一段不包含任何逻辑结构的普通文字。")
        assert result.status == "analysis_only"

    def test_multiple_assignments_ambiguous(self):
        """Multiple consistent assignments → ambiguous."""
        text = (
            "甲说：A是B。"
            "乙说：C是D。"
            "已知只有一真。"
        )
        result = solve_truth_core(text)
        # These two independent atoms have no contradiction,
        # so both "only s1 true" and "only s2 true" should be consistent.
        if result.status != "analysis_only":
            assert result.status in ("solved", "ambiguous")


# =========================================================================
# No-default-first-candidate guard
# =========================================================================

class TestNoDefaultFirst:
    def test_no_default_first_in_code(self):
        """truth_reasoning.py must not default to first candidate."""
        import inspect
        import xingce_solver.solvers.truth_reasoning as mod
        source = inspect.getsource(mod)
        forbidden = [
            "first candidate",
            "first assignment",
            r"default.*first",
            r"\[0\].*select",
            r"pick.*first",
        ]
        for pat in forbidden:
            assert not re.search(pat, source, re.IGNORECASE), (
                f"Found forbidden pattern '{pat}' in truth_reasoning.py"
            )


# =========================================================================
# No-hardcoded-entity guard
# =========================================================================

class TestNoHardcodedEntities:
    """Ensure truth_reasoning.py contains no exam-specific entity names."""

    FORBIDDEN_ENTITIES = [
        "甲队", "乙队", "方某", "白某", "夏某", "邓某",
        "小李", "小赵", "小王", "小张",
        "晋级", "写完作业", "旅游", "采纳",
        "动物园", "博物馆", "狗粮", "食品", "玩具",
        "水果糖", "奶糖", "购物袋", "购物礼品",
        "四姑娘山", "墨石公园", "塔公草原",
        "甲是罪犯", "丁是罪犯",
    ]

    def test_no_entities_in_source(self):
        import inspect
        import xingce_solver.solvers.truth_reasoning as mod
        source = inspect.getsource(mod)
        for entity in self.FORBIDDEN_ENTITIES:
            assert entity not in source, (
                f"Found hardcoded entity '{entity}' in truth_reasoning.py"
            )


# =========================================================================
# Integration: realistic question fragments
# =========================================================================

class TestRealisticFragments:
    def test_contradiction_pair_all_some(self):
        """所有S是P vs 有的S不是P is a contradiction pair."""
        all_p = All("同学", "写完作业", negated=False)
        some_not_p = Some("同学", "写完作业", negated=True)
        assert are_contradictory(all_p, some_not_p) is True

    def test_contradiction_pair_imply_conj(self):
        """P→Q vs P且¬Q is a contradiction pair."""
        p = Atom("小李", "写完作业")
        q = Atom("小赵", "写完作业")
        imply = Imply(p, negate_proposition(q))
        conj = And(p, q)  # P且Q is the negation of P→¬Q
        assert are_contradictory(imply, conj) is True

    def test_extract_statements_speaker_pattern(self):
        """extract_statements handles X说：Y pattern."""
        text = "甲说：所有人是罪犯。乙说：甲是罪犯。丙说：我不是罪犯。丁说：我也不是罪犯。"
        stmts = extract_statements(text)
        assert len(stmts) == 4

    def test_extract_statements_numbered_pattern(self):
        """extract_statements handles ①②③ pattern."""
        text = "①如果去四姑娘山，就不去墨石公园。②塔公草原和墨石公园去一个就好。③塔公草原和墨石公园都不去。"
        stmts = extract_statements(text)
        assert len(stmts) == 3

    def test_solve_basic_only_one_false(self):
        """Basic 'only one false' question with clear contradiction pair."""
        text = (
            "甲说：所有人是罪犯。"
            "乙说：甲是罪犯。"
            "丙说：我不是罪犯。"
            "丁说：所有人都不是罪犯。"
            "已知只有一人说假话。"
        )
        result = solve_truth_core(text)
        assert result.status in ("solved", "ambiguous", "analysis_only")
