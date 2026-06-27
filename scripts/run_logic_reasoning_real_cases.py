from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from xingce_solver.solvers.logic_reasoning import solve_logic_reasoning


def load_cases(path: str | Path) -> list[dict[str, Any]]:
    input_path = Path(path)
    text = input_path.read_text(encoding="utf-8")
    if input_path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("cases", "questions", "items"):
            if isinstance(data.get(key), list):
                return data[key]
    raise ValueError(f"Unsupported case file structure: {input_path}")


def normalize_case(raw: dict[str, Any]) -> dict[str, Any]:
    case_id = str(raw.get("case_id") or raw.get("id") or "").strip()
    title = str(raw.get("title") or raw.get("name") or "").strip()
    source = str(raw.get("source") or raw.get("url") or "").strip()
    expected_answer = str(raw.get("expected_answer") or raw.get("answer") or "").strip().upper()
    stem = str(raw.get("stem") or raw.get("question") or raw.get("question_text") or "").strip()
    options = raw.get("options") or {}
    if isinstance(options, list):
        option_text = " ".join(str(option).strip() for option in options)
    elif isinstance(options, dict):
        option_text = " ".join(
            f"{label}. {text}" for label, text in sorted(options.items())
        )
    else:
        option_text = str(options).strip()
    return {
        "case_id": case_id,
        "title": title,
        "source": source,
        "expected_answer": expected_answer,
        "question_text": f"{stem} {option_text}".strip(),
    }


def run_case(raw: dict[str, Any]) -> dict[str, Any]:
    case = normalize_case(raw)
    result = solve_logic_reasoning(case["question_text"])
    candidate = result.get("answer_candidate")
    candidate_label = ""
    if isinstance(candidate, dict):
        candidate_label = str(candidate.get("label") or "").strip().upper()
    expected = case["expected_answer"]
    is_correct: bool | None
    if not expected:
        is_correct = None
    else:
        is_correct = bool(candidate_label and candidate_label == expected)
    return {
        "case_id": case["case_id"],
        "title": case["title"],
        "source": case["source"],
        "expected_answer": expected,
        "answer_candidate": candidate_label,
        "is_correct": is_correct,
        "decision_status": result.get("decision_status", ""),
        "confidence": result.get("confidence", 0.0),
        "sub_type_actual": " / ".join(
            part for part in [result.get("question_type"), result.get("sub_type")] if part
        ),
        "needs_more_data": result.get("needs_more_data", False),
        "source_method_ids": result.get("source_method_ids", []),
        "warnings": result.get("warnings", []),
        "high_risk_warnings": result.get("high_risk_warnings", []),
    }


def write_jsonl(rows: list[dict[str, Any]], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    correct = sum(1 for row in rows if row["is_correct"] is True)
    wrong = sum(1 for row in rows if row["is_correct"] is False and row["answer_candidate"])
    null = sum(1 for row in rows if not row["answer_candidate"])
    unknown = sum(1 for row in rows if row["is_correct"] is None)
    status_counts = Counter(str(row["decision_status"]) for row in rows)
    type_counts = Counter(str(row["sub_type_actual"]) for row in rows)
    high_risk_counts = Counter(
        warning for row in rows for warning in row.get("high_risk_warnings", [])
    )
    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "null": null,
        "unknown": unknown,
        "decision_status": dict(status_counts),
        "sub_type_actual": dict(type_counts),
        "high_risk_warnings": dict(high_risk_counts),
    }


def write_summary(rows: list[dict[str, Any]], path: str | Path) -> dict[str, Any]:
    summary = summarize(rows)
    summary_path = Path(path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Logic Reasoning Real Case Batch Summary",
        "",
        "## Summary",
        "",
        f"- total: {summary['total']}",
        f"- correct: {summary['correct']}",
        f"- wrong: {summary['wrong']}",
        f"- null: {summary['null']}",
        f"- unknown_expected_answer: {summary['unknown']}",
        "",
        "## decision_status",
        "",
    ]
    for status, count in summary["decision_status"].items():
        lines.append(f"- {status}: {count}")
    lines.extend(["", "## Cases", ""])
    lines.append("| case_id | expected | candidate | correct | decision_status | confidence | sub_type_actual |")
    lines.append("|---|---:|---:|---|---|---:|---|")
    for row in rows:
        lines.append(
            "| {case_id} | {expected_answer} | {answer_candidate} | {is_correct} | "
            "{decision_status} | {confidence} | {sub_type_actual} |".format(**row)
        )
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def run_batch(input_path: str | Path, output_path: str | Path, summary_path: str | Path) -> dict[str, Any]:
    rows = [run_case(case) for case in load_cases(input_path)]
    write_jsonl(rows, output_path)
    return write_summary(rows, summary_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run solve_logic_reasoning on real logic cases.")
    parser.add_argument("--input", required=True, help="Input JSON or JSONL case file.")
    parser.add_argument("--output", required=True, help="Output JSONL path.")
    parser.add_argument("--summary", required=True, help="Output Markdown summary path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = run_batch(args.input, args.output, args.summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
