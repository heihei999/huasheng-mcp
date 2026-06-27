from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.run_logic_reasoning_real_cases import normalize_case
from xingce_solver.solvers import solve_logic_reasoning


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"
REAL_TRANSLATION_MANIFEST = (
    ROOT / "text-image" / "logic_translation_real_cases_open_verified_v2" / "questions_manifest.json"
)

pytestmark = pytest.mark.skipif(
    not REAL_TRANSLATION_MANIFEST.exists(),
    reason="external text-image fixture not included in this focused release",
)


def _load_real_translation_cases() -> list[dict[str, object]]:
    return json.loads(REAL_TRANSLATION_MANIFEST.read_text(encoding="utf-8"))


def _candidate_label(result: dict[str, object]) -> str:
    candidate = result.get("answer_candidate")
    if isinstance(candidate, dict):
        return str(candidate.get("label") or "").upper()
    return ""


def test_v6_1_real_translation_manifest_has_16_cases() -> None:
    cases = _load_real_translation_cases()

    assert len(cases) == 16
    assert {str(case["answer"]).upper() for case in cases} <= {"A", "B", "C", "D"}


def test_v6_1_real_translation_batch_targets() -> None:
    correct = 0
    wrong = 0
    null = 0
    status_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}

    for case in _load_real_translation_cases():
        question_text = normalize_case(case)["question_text"]
        result = solve_logic_reasoning(question_text, kb_dir=KB_DIR)
        candidate = _candidate_label(result)
        expected = str(case["answer"]).upper()
        status_counts[str(result["decision_status"])] = status_counts.get(str(result["decision_status"]), 0) + 1
        type_key = f"{result['question_type']} / {result['sub_type']}"
        type_counts[type_key] = type_counts.get(type_key, 0) + 1
        if not candidate:
            null += 1
        elif candidate == expected:
            correct += 1
        else:
            wrong += 1

    assert correct >= 13
    assert wrong <= 2
    assert null <= 3
    assert status_counts.get("candidate_ready", 0) >= 13
    assert type_counts.get("结论推出 / 翻译推理", 0) >= 13


def test_v6_1_real_translation_representative_cases() -> None:
    cases = {str(case["case_id"]): case for case in _load_real_translation_cases()}

    expectations = {
        "LTR-REAL-001": "A",
        "LTR-REAL-003": "B",
        "LTR-REAL-007": "A",
        "LTR-REAL-011": "C",
        "LTR-REAL-015": "D",
    }
    for case_id, expected in expectations.items():
        result = solve_logic_reasoning(normalize_case(cases[case_id])["question_text"], kb_dir=KB_DIR)
        assert result["question_type"] == "结论推出"
        assert result["sub_type"] == "翻译推理"
        assert _candidate_label(result) == expected
