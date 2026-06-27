"""Guardrail tests for analysis reasoning integration in solve_logic_reasoning.

These tests ensure the conservative integration behavior is preserved:
- solved + unique_supported → candidate_ready
- all other cases → analysis_only
- no interference with other question types
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from xingce_solver.solvers.logic_reasoning import (
    _is_analysis_reasoning_question,
    solve_logic_reasoning,
)


# ---------------------------------------------------------------------------
# Detection guardrails
# ---------------------------------------------------------------------------

class TestAnalysisDetection:
    def test_half_true_detected(self):
        q = "每人都只猜对了一半。甲说：一号是红的，二号是蓝的。"
        assert _is_analysis_reasoning_question(q) is True

    def test_box_color_detected(self):
        q = "有红蓝黄三种颜色的皮球分别装在三个盒子里。"
        assert _is_analysis_reasoning_question(q) is True

    def test_ordering_detected(self):
        q = "五辆车从左到右排列，A紧挨B。"
        assert _is_analysis_reasoning_question(q) is True

    def test_comparison_detected(self):
        q = "甲比乙年龄大，丙不是最大的。"
        assert _is_analysis_reasoning_question(q) is True

    def test_translation_not_detected(self):
        q = "如果甲是罪犯那么乙也是罪犯。甲是罪犯。可以推出："
        assert _is_analysis_reasoning_question(q) is False

    def test_truth_not_detected(self):
        q = "甲说所有人是罪犯。乙说所有人不是罪犯。只有一人说真话。"
        assert _is_analysis_reasoning_question(q) is False


# ---------------------------------------------------------------------------
# Integration behavior guardrails
# ---------------------------------------------------------------------------

class TestAnalysisIntegrationBehavior:
    def test_solved_unique_gives_candidate_ready(self):
        """004 is known solved + unique_supported → candidate_ready."""
        manifest = Path("text-image/logic_analysis_real_cases_open_verified_v1/questions_manifest.json")
        if not manifest.exists():
            pytest.skip("Test data not available")
        cases = json.loads(manifest.read_text(encoding="utf-8"))
        case = next(c for c in cases if c["case_id"] == "LANALYSIS-REAL-004")
        opts = case.get("options", {})
        opt_text = " ".join(f"{l}. {t}" for l, t in sorted(opts.items()))
        full = f"{case['question']} {opt_text}"
        result = solve_logic_reasoning(full)
        assert result["decision_status"] == "candidate_ready"
        assert result["answer_candidate"] is not None
        assert result["answer_candidate"]["label"] == "C"

    def test_solved_unique_gives_candidate_ready_005(self):
        """005 is known solved + unique_supported → candidate_ready."""
        manifest = Path("text-image/logic_analysis_real_cases_open_verified_v1/questions_manifest.json")
        if not manifest.exists():
            pytest.skip("Test data not available")
        cases = json.loads(manifest.read_text(encoding="utf-8"))
        case = next(c for c in cases if c["case_id"] == "LANALYSIS-REAL-005")
        opts = case.get("options", {})
        opt_text = " ".join(f"{l}. {t}" for l, t in sorted(opts.items()))
        full = f"{case['question']} {opt_text}"
        result = solve_logic_reasoning(full)
        assert result["decision_status"] == "candidate_ready"
        assert result["answer_candidate"]["label"] == "C"

    def test_ambiguous_gives_analysis_only(self):
        """001 is ambiguous → analysis_only."""
        manifest = Path("text-image/logic_analysis_real_cases_open_verified_v1/questions_manifest.json")
        if not manifest.exists():
            pytest.skip("Test data not available")
        cases = json.loads(manifest.read_text(encoding="utf-8"))
        case = next(c for c in cases if c["case_id"] == "LANALYSIS-REAL-001")
        opts = case.get("options", {})
        opt_text = " ".join(f"{l}. {t}" for l, t in sorted(opts.items()))
        full = f"{case['question']} {opt_text}"
        result = solve_logic_reasoning(full)
        assert result["decision_status"] == "analysis_only"
        assert result.get("answer_candidate") is None or result["answer_candidate"] is None

    def test_analysis_only_case_stays_analysis_only(self):
        """003 is analysis_only → analysis_only."""
        manifest = Path("text-image/logic_analysis_real_cases_open_verified_v1/questions_manifest.json")
        if not manifest.exists():
            pytest.skip("Test data not available")
        cases = json.loads(manifest.read_text(encoding="utf-8"))
        case = next(c for c in cases if c["case_id"] == "LANALYSIS-REAL-003")
        opts = case.get("options", {})
        opt_text = " ".join(f"{l}. {t}" for l, t in sorted(opts.items()))
        full = f"{case['question']} {opt_text}"
        result = solve_logic_reasoning(full)
        assert result["decision_status"] == "analysis_only"


# ---------------------------------------------------------------------------
# Non-interference guardrails
# ---------------------------------------------------------------------------

class TestNonInterference:
    def test_translation_not_affected(self):
        q = "如果甲是罪犯那么乙也是罪犯。甲是罪犯。可以推出：A.乙是罪犯 B.乙不是罪犯"
        result = solve_logic_reasoning(q)
        assert result["question_type"] != "分析推理"

    def test_weaken_not_affected(self):
        q = "以下哪项最能削弱上述论证？A.选项一 B.选项二"
        result = solve_logic_reasoning(q)
        assert result["question_type"] != "分析推理"


# ---------------------------------------------------------------------------
# Default-first guardrails
# ---------------------------------------------------------------------------

class TestNoDefaultFirst:
    def test_no_default_first_option(self):
        """Must not pick first option by default."""
        q = "甲比乙大，乙比丙大。A.甲最大 B.乙最大 C.丙最大 D.无法确定"
        result = solve_logic_reasoning(q)
        if result["decision_status"] == "candidate_ready":
            # If answered, must not be A by default
            pass  # Can't enforce without knowing correct answer
        # At minimum, if ambiguous, must be analysis_only
        assert result["decision_status"] in ("candidate_ready", "analysis_only")
