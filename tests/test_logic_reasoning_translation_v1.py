from __future__ import annotations

import json
from pathlib import Path

import pytest

from xingce_solver.solvers import solve_logic_reasoning

from tests.test_logic_reasoning_v3_real_cases import REAL_CASES
from tests.test_logic_reasoning_v5_real_cases import _load_lr2_cases


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"
TRANSLATION_MANIFEST = ROOT / "text-image" / "logic_translation_v1_cases" / "questions_manifest.json"

pytestmark = pytest.mark.skipif(
    not TRANSLATION_MANIFEST.exists(),
    reason="external text-image fixture not included in this focused release",
)


def _load_translation_cases() -> list[dict[str, object]]:
    return json.loads(TRANSLATION_MANIFEST.read_text(encoding="utf-8"))


def _question_text(case: dict[str, object]) -> str:
    return f"{case['stem']} {' '.join(str(option) for option in case['options'])}"


def _candidate_label(result: dict[str, object]) -> str:
    candidate = result.get("answer_candidate")
    if isinstance(candidate, dict):
        return str(candidate.get("label") or "").upper()
    return ""


def test_translation_v1_manifest_has_12_cases() -> None:
    cases = _load_translation_cases()

    assert len(cases) == 12
    assert {str(case["answer"]).upper() for case in cases} <= {"A", "B", "C", "D"}


def test_translation_v1_identifies_type_and_debug_context() -> None:
    case = _load_translation_cases()[0]
    result = solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR, return_debug=True)

    assert result["version"] == "v6.1"
    assert result["solver_version"] == "v7 conservative truth integration"
    assert result["question_type"] == "结论推出"
    assert result["sub_type"] == "翻译推理"
    assert result["question_stem_analysis"]["strength_direction"] == "translation"
    assert "translation_reasoning" in result["debug"]
    assert result["debug"]["translation_reasoning"]["rules"]
    assert result["debug"]["translation_reasoning"]["inferred_relations"]


def test_translation_v1_core_patterns_are_answered() -> None:
    results = {
        str(case["id"]): solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR)
        for case in _load_translation_cases()
    }

    assert _candidate_label(results["TR-001"]) == "B"  # 如果/那么，逆否
    assert _candidate_label(results["TR-002"]) == "A"  # 如果/那么，正向事实
    assert _candidate_label(results["TR-003"]) == "C"  # 只有/才
    assert _candidate_label(results["TR-004"]) == "D"  # 除非/否则
    assert _candidate_label(results["TR-006"]) == "B"  # 并非所有
    assert _candidate_label(results["TR-007"]) == "A"  # 要么/要么
    assert _candidate_label(results["TR-008"]) == "C"  # 要么/要么，否一推一
    assert _candidate_label(results["TR-009"]) == "A"  # 不能推出
    assert _candidate_label(results["TR-010"]) == "D"  # 不一定为真


def test_translation_v1_batch_targets() -> None:
    correct = 0
    wrong = 0
    null = 0
    for case in _load_translation_cases():
        result = solve_logic_reasoning(_question_text(case), kb_dir=KB_DIR)
        candidate = _candidate_label(result)
        expected = str(case["answer"]).upper()
        if not candidate:
            null += 1
        elif candidate == expected:
            correct += 1
        else:
            wrong += 1

    assert correct >= 10
    assert wrong <= 1
    assert null <= 2


def test_v6_argument_first_batch_regression() -> None:
    correct = 0
    wrong = 0
    null = 0
    for _case_id, answer, _expected_type, text in REAL_CASES:
        result = solve_logic_reasoning(text, kb_dir=KB_DIR)
        candidate = _candidate_label(result)
        if not candidate:
            null += 1
        elif candidate == answer:
            correct += 1
        else:
            wrong += 1

    assert correct >= 8
    assert wrong <= 1
    assert null <= 1


def test_v6_argument_second_batch_regression() -> None:
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

    assert correct >= 17
    assert wrong <= 1
    assert null <= 3
