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
    stem = str(case["stem"])
    options = " ".join(str(option) for option in case["options"])
    return f"{stem} {options}"


def _candidate_label(result: dict[str, object]) -> str:
    candidate = result.get("answer_candidate")
    if isinstance(candidate, dict):
        return str(candidate.get("label") or "").upper()
    return ""


def test_v4_second_batch_has_cautious_but_useful_candidates() -> None:
    cases = _load_lr2_cases()
    results = [(case, solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR)) for case in cases]

    correct = 0
    wrong = 0
    null = 0
    for case, result in results:
        candidate = _candidate_label(result)
        expected = str(case["answer"]).upper()
        if not candidate:
            null += 1
        elif candidate == expected:
            correct += 1
        else:
            wrong += 1

    assert correct >= 8
    assert wrong <= 5
    assert null <= 10


def test_v4_second_batch_detects_reverse_questions_and_premises() -> None:
    cases_by_id = {str(case["id"]): case for case in _load_lr2_cases()}
    results = {
        case_id: solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR)
        for case_id, case in cases_by_id.items()
    }

    for case_id in ["04", "08", "09", "10", "15"]:
        stem = results[case_id]["question_stem_analysis"]
        assert stem["is_reverse_question"] is True
        assert stem["reverse_question_type"] in {
            "except",
            "least_strengthen",
            "least_weaken",
            "cannot_infer",
            "incorrect",
        }

    for case_id in ["01", "05", "14"]:
        assert results[case_id]["question_type"] == "前提假设"


def test_v4_first_batch_real_cases_do_not_regress() -> None:
    correct = 0
    wrong = 0
    for _case_id, answer, _expected_type, text in REAL_CASES:
        result = solve_logic_reasoning(text, kb_dir=KB_DIR)
        candidate = _candidate_label(result)
        if candidate == answer:
            correct += 1
        elif candidate:
            wrong += 1

    assert correct >= 7
    assert wrong <= 2


def test_v4_debug_output_is_optional() -> None:
    case = _load_lr2_cases()[0]
    normal = solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR)
    debug = solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR, return_debug=True)

    assert "debug" not in normal
    assert "debug" in debug
    assert "candidate_selection" in debug["debug"]
