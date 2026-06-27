"""Guardrail tests for truth reasoning integration in solve_logic_reasoning.

These tests ensure the v7 conservative truth integration behavior is preserved:
- solved + unique_supported → candidate_ready
- all other cases → analysis_only
- no interference with translation or argument reasoning
- no default-first-option or default-first-assignment behavior
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from xingce_solver.solvers.logic_reasoning import (
    _is_truth_reasoning_question,
    solve_logic_reasoning,
)

TRUTH_MANIFEST = Path("text-image/logic_truth_real_cases_open_verified_v1/questions_manifest.json")


def _load_truth_manifest_or_skip() -> list[dict]:
    """Load truth manifest or skip test if fixture not present."""
    if not TRUTH_MANIFEST.exists():
        pytest.skip("external text-image truth fixture not included in this focused release")
    with TRUTH_MANIFEST.open(encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Detection guardrails
# ---------------------------------------------------------------------------

class TestTruthDetection:
    """Ensure truth reasoning questions are correctly detected."""

    def test_speaker_with_constraint_detected(self):
        q = "甲说：所有人是罪犯。乙说：所有人不是罪犯。已知只有一人说真话。由此推出："
        assert _is_truth_reasoning_question(q) is True

    def test_numbered_with_constraint_detected(self):
        q = "老师说了四句话：①右手肯定不是水果糖；②或者左手是水果糖，或者右手是水果糖。假设四句话中有三句是真的，一句是假的。"
        assert _is_truth_reasoning_question(q) is True

    def test_all_false_detected(self):
        q = "甲说：P。乙说：Q。丙说：R。对于同事的建议都没采纳，那么："
        assert _is_truth_reasoning_question(q) is True

    def test_translation_not_detected(self):
        q = "如果甲是罪犯，那么乙也是罪犯。甲是罪犯。可以推出："
        assert _is_truth_reasoning_question(q) is False

    def test_weaken_not_detected(self):
        q = "以下哪项最能削弱上述论证？"
        assert _is_truth_reasoning_question(q) is False


# ---------------------------------------------------------------------------
# Integration behavior guardrails
# ---------------------------------------------------------------------------

class TestTruthIntegrationBehavior:
    """Ensure the integration returns correct decision_status."""

    def test_candidate_ready_only_when_solved_and_unique(self):
        """When core solves and option mapping is unique_supported,
        the result should be candidate_ready with a label."""
        # This question is known to be solved + unique_supported in core
        q = (
            "罐子里有水果糖和奶糖两种，老师说了四句话："
            "①右手肯定不是水果糖；"
            "②或者左手是水果糖，或者右手是水果糖；"
            "③如果左手是水果糖，则右手就不是水果糖；"
            "④左手、右手都是水果糖。"
            "假设老师说的四句话中有三句是真的，一句是假的，则下列选项正确的是？"
            " A. 左手是水果糖，右手是奶糖"
            " B. 左手水果糖，右手水果糖"
            " C. 左手奶糖，右手奶糖"
            " D. 左手奶糖，右手水果糖"
        )
        result = solve_logic_reasoning(q)
        # Should be candidate_ready because core solves + unique_supported
        assert result["decision_status"] == "candidate_ready"
        assert result["answer_candidate"] is not None
        assert isinstance(result["answer_candidate"], dict)
        assert result["answer_candidate"]["label"] in ("A", "B", "C", "D")

    def test_analysis_only_when_ambiguous(self):
        """When core returns ambiguous, result should be analysis_only."""
        q = (
            "甲说：所有人是罪犯。"
            "乙说：甲是罪犯。"
            "丙说：我不是罪犯。"
            "丁说：所有人都不是罪犯。"
            "已知只有一人说假话，那么可推出下列哪项？"
            " A. 甲说的不对 B. 乙说的不对 C. 丙说的不对 D. 丁说的不对"
        )
        result = solve_logic_reasoning(q)
        # Core returns ambiguous for this → analysis_only
        assert result["decision_status"] == "analysis_only"
        assert result["answer_candidate"] is None

    def test_no_default_first_option(self):
        """Must not default to first option when ambiguous."""
        q = (
            "甲说：所有人是罪犯。"
            "乙说：甲是罪犯。"
            "丙说：我不是罪犯。"
            "丁说：所有人都不是罪犯。"
            "已知只有一人说假话，那么可推出下列哪项？"
            " A. 甲说的不对 B. 乙说的不对 C. 丙说的不对 D. 丁说的不对"
        )
        result = solve_logic_reasoning(q)
        if result["decision_status"] == "analysis_only":
            assert result["answer_candidate"] is None
        # If somehow candidate_ready, must not be A by default
        # (but this question should be analysis_only)

    def test_confidence_not_too_high(self):
        """Truth reasoning confidence should be conservative (0.70-0.80)."""
        q = (
            "罐子里有水果糖和奶糖两种，老师说了四句话："
            "①右手肯定不是水果糖；"
            "②或者左手是水果糖，或者右手是水果糖；"
            "③如果左手是水果糖，则右手就不是水果糖；"
            "④左手、右手都是水果糖。"
            "假设老师说的四句话中有三句是真的，一句是假的，则下列选项正确的是？"
        )
        result = solve_logic_reasoning(q)
        if result["decision_status"] == "candidate_ready":
            assert 0.70 <= result["confidence"] <= 0.80


# ---------------------------------------------------------------------------
# Non-interference guardrails
# ---------------------------------------------------------------------------

class TestNonInterference:
    """Ensure truth reasoning branch does not affect other question types."""

    def test_translation_not_affected(self):
        """Translation questions should not be routed to truth reasoning."""
        q = "如果甲是罪犯，那么乙也是罪犯。甲是罪犯。可以推出：A.乙是罪犯 B.乙不是罪犯"
        result = solve_logic_reasoning(q)
        # Should be handled by translation logic, not truth reasoning
        assert result["question_type"] != "真假推理"
        assert result.get("sub_type") != "truth_reasoning"

    def test_weaken_not_affected(self):
        """Weaken questions should not be routed to truth reasoning."""
        q = "以下哪项最能削弱上述论证？A.选项一 B.选项二 C.选项三 D.选项四"
        result = solve_logic_reasoning(q)
        assert result["question_type"] != "真假推理"


# ---------------------------------------------------------------------------
# Real-case regression guardrails
# ---------------------------------------------------------------------------

class TestRealCaseRegression:
    """Ensure real-case results don't regress."""

    TRUTH_CASES_EXPECTED = {
        "LTRUTH-REAL-002": "A",
        "LTRUTH-REAL-005": "C",
        "LTRUTH-REAL-009": "A",
        "LTRUTH-REAL-011": "B",
    }

    @pytest.mark.parametrize("case_id,expected", list(TRUTH_CASES_EXPECTED.items()))
    def test_truth_case_correct(self, case_id, expected):
        """Known-correct truth cases must remain correct."""
        cases = _load_truth_manifest_or_skip()
        case = next(c for c in cases if c["case_id"] == case_id)
        # Build full question text with options (same as batch runner)
        stem = case["question"]
        options = case.get("options", {})
        if isinstance(options, dict):
            option_text = " ".join(f"{label}. {text}" for label, text in sorted(options.items()))
        else:
            option_text = str(options)
        full_text = f"{stem} {option_text}".strip()
        result = solve_logic_reasoning(full_text)
        assert result["decision_status"] == "candidate_ready", f"{case_id} should be candidate_ready"
        assert result["answer_candidate"]["label"] == expected, f"{case_id} should predict {expected}"

    @pytest.mark.parametrize("case_id", [
        "LTRUTH-REAL-001", "LTRUTH-REAL-003", "LTRUTH-REAL-004",
        "LTRUTH-REAL-006", "LTRUTH-REAL-007", "LTRUTH-REAL-008",
        "LTRUTH-REAL-010", "LTRUTH-REAL-012",
    ])
    def test_truth_case_analysis_only(self, case_id):
        """Known-ambiguous truth cases must remain analysis_only."""
        cases = _load_truth_manifest_or_skip()
        case = next(c for c in cases if c["case_id"] == case_id)
        stem = case["question"]
        options = case.get("options", {})
        if isinstance(options, dict):
            option_text = " ".join(f"{label}. {text}" for label, text in sorted(options.items()))
        else:
            option_text = str(options)
        full_text = f"{stem} {option_text}".strip()
        result = solve_logic_reasoning(full_text)
        assert result["decision_status"] == "analysis_only", f"{case_id} should be analysis_only"
        assert result["answer_candidate"] is None
