from __future__ import annotations

import json
from pathlib import Path

import pytest

from xingce_solver.solvers import solve_logic_reasoning

from tests.test_logic_reasoning_v3_real_cases import REAL_CASES


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"
LR2_MANIFEST = (
    ROOT
    / "text-image"
    / "lr2_real_verified_20_images"
    / "lr2_real_verified_20_images"
    / "questions_manifest.json"
)

pytestmark = pytest.mark.skipif(
    not LR2_MANIFEST.exists(),
    reason="external text-image fixture not included in this focused release",
)


def _load_lr2_cases() -> list[dict[str, object]]:
    return json.loads(LR2_MANIFEST.read_text(encoding="utf-8"))


def _question_text(case: dict[str, object]) -> str:
    return f"{case['stem']} {' '.join(str(option) for option in case['options'])}"


def _candidate_label(result: dict[str, object]) -> str:
    candidate = result.get("answer_candidate")
    if isinstance(candidate, dict):
        return str(candidate.get("label") or "").upper()
    return ""


def test_v5_version_and_debug_selection_fields() -> None:
    case = _load_lr2_cases()[1]
    result = solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR, return_debug=True)

    assert result["version"] == "v6.1"
    assert result["solver_version"] == "v7 conservative truth integration"
    debug = result["debug"]["candidate_selection"]
    assert "best_selection_score" in debug
    assert "question_polarity" in debug
    assert "task_type" in debug

    candidate = result["answer_candidate"]
    assert candidate is not None
    selected = next(option for option in result["option_analysis"] if option["is_candidate"])
    for field in ["tie_break_score", "selection_score", "evidence_tags", "risk_tags"]:
        assert field in selected


def test_v5_second_batch_real_cases_targets() -> None:
    correct = 0
    wrong = 0
    null = 0
    for case in _load_lr2_cases():
        result = solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR)
        candidate = _candidate_label(result)
        expected = str(case["answer"]).upper()
        if not candidate:
            null += 1
        elif candidate == expected:
            correct += 1
        else:
            wrong += 1

    assert correct >= 16
    assert wrong <= 2
    assert null <= 4


def test_v5_first_batch_real_cases_do_not_regress() -> None:
    correct = 0
    wrong = 0
    for _case_id, answer, _expected_type, text in REAL_CASES:
        result = solve_logic_reasoning(text, kb_dir=KB_DIR)
        candidate = _candidate_label(result)
        if candidate == answer:
            correct += 1
        elif candidate:
            wrong += 1

    assert correct >= 8
    assert wrong <= 1


def test_v5_low_risk_warning_does_not_block_candidate() -> None:
    case = _load_lr2_cases()[11]
    result = solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR)

    assert "未能稳定识别论据，选项分析只能作为框架草案。" in result["warnings"]
    assert result["decision_status"] == "candidate_ready"
    assert _candidate_label(result) == "B"


def test_v5_reverse_question_nested_expression() -> None:
    cases_by_id = {str(case["id"]): case for case in _load_lr2_cases()}
    result = solve_logic_reasoning(_question_text(cases_by_id["04"]), kb_dir=KB_DIR, return_debug=True)

    assert result["question_stem_analysis"]["is_reverse_question"] is True
    assert result["question_stem_analysis"]["reverse_question_type"] == "except"
    assert result["question_stem_analysis"]["question_polarity"] == "negative"
    assert result["answer_candidate"]["label"] == "C"


def test_v5_tie_breaker_prefers_direct_subject_evidence() -> None:
    cases_by_id = {str(case["id"]): case for case in _load_lr2_cases()}
    result = solve_logic_reasoning(_question_text(cases_by_id["13"]), kb_dir=KB_DIR)

    selected = next(option for option in result["option_analysis"] if option["is_candidate"])
    assert selected["label"] == "B"
    assert "direct_counterexample" in selected["evidence_tags"]
    assert selected["selection_score"] > selected["score"]
