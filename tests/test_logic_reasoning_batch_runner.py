from __future__ import annotations

import json
from pathlib import Path

from scripts.run_logic_reasoning_real_cases import run_batch


def test_logic_reasoning_batch_runner_outputs_files(tmp_path: Path) -> None:
    manifest = tmp_path / "questions_manifest.json"
    output = tmp_path / "results.jsonl"
    summary = tmp_path / "summary.md"
    cases = [
        {
            "id": "T01",
            "title": "削弱样例",
            "source": "unit-test",
            "answer": "A",
            "stem": "某研究认为，经常喝茶的人更健康。因此，喝茶可以提高健康水平。以下哪项最能削弱上述论证？",
            "options": [
                "A. 健康的人更可能有喝茶习惯",
                "B. 喝茶的人通常也更爱运动",
                "C. 部分人喝茶后睡眠变差",
                "D. 茶叶价格逐年上涨",
            ],
        }
    ]
    manifest.write_text(json.dumps(cases, ensure_ascii=False), encoding="utf-8")

    run_batch(manifest, output, summary)

    assert output.exists()
    assert summary.exists()
    rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    for field in [
        "case_id",
        "expected_answer",
        "answer_candidate",
        "decision_status",
        "confidence",
        "is_correct",
    ]:
        assert field in rows[0]
    assert "Logic Reasoning Real Case Batch Summary" in summary.read_text(encoding="utf-8")
