import json
from pathlib import Path

import pytest

from xingce_solver.solvers import solve_data_analysis


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"
CASES_PATH = ROOT / "tests" / "fixtures" / "data_analysis_real_exam_style_cases.jsonl"


def load_cases() -> list[dict]:
    with CASES_PATH.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def method_ids(result: dict) -> set[str]:
    return {method["method_id"] for method in result["recommended_methods"]}


@pytest.mark.parametrize("case", load_cases(), ids=lambda case: case["case_id"])
def test_real_exam_style_case(case: dict) -> None:
    result = solve_data_analysis(case["question_text"], kb_dir=KB_DIR)
    matched_methods = method_ids(result)

    assert result["module"] == case["expected_module"]
    assert matched_methods.intersection(case["expected_methods_any"]), {
        "case_id": case["case_id"],
        "expected_any": case["expected_methods_any"],
        "actual": sorted(matched_methods),
        "gap_reason": case["gap_reason"],
    }

    if case["expected_gap"]:
        assert result["warnings"] or result["solving_plan"]
        return

    assert result["question_type"] == case["expected_question_type"]
    expected_answer = case["expected_answer_candidate_contains"]
    if expected_answer:
        assert result["answer_candidate"] is not None
        assert expected_answer in result["answer_candidate"]["label"]

    expected_value = case["expected_computed_result_approx"]
    if expected_value is not None:
        assert result["computed_result"] is not None
        assert abs(result["computed_result"] - expected_value) <= 1.0
