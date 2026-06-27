"""Audit analogy reasoning core against real cases.

Usage:
    python scripts/audit_analogy_reasoning_core.py [--version v1_0]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = (
    PROJECT_ROOT
    / "text-image"
    / "analogy_reasoning_real_cases_open_verified_v1"
    / "questions_manifest.json"
)
ANSWER_KEY_PATH = (
    PROJECT_ROOT
    / "text-image"
    / "analogy_reasoning_real_cases_open_verified_v1"
    / "ANSWER_KEY.md"
)


def _load_answer_key(path: Path) -> dict[str, str]:
    """Load answer key from ANSWER_KEY.md.

    Supports two formats:
    1. | case_id | source_no | answer | relation_focus |
    2. | case_id | answer | relation_focus | answer_basis |
    """
    text = path.read_text(encoding="utf-8")
    answers: dict[str, str] = {}
    answer_col_idx: int | None = None

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Skip separator lines (contain ---)
        if line.startswith("|") and "---" in line:
            continue

        # Detect answer column from header row
        if line.startswith("|") and "answer" in line.lower() and answer_col_idx is None:
            parts = [p.strip().lower() for p in line.split("|") if p.strip()]
            for i, p in enumerate(parts):
                if p == "answer":
                    answer_col_idx = i
                    break
            continue

        if line.startswith("|"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 2:
                continue

            case_id = parts[0]
            # Use detected column index, or default to 2 (old format)
            if answer_col_idx is not None and answer_col_idx < len(parts):
                answer = parts[answer_col_idx]
            elif len(parts) >= 3:
                answer = parts[2]
            else:
                answer = parts[1]

            if case_id and answer and answer in ("A", "B", "C", "D"):
                answers[case_id] = answer
    return answers


def _run_audit(
    version: str,
    manifest_path: Path | None = None,
    answer_key_path: Path | None = None,
    results_path: Path | None = None,
    summary_path: Path | None = None,
) -> None:
    """Run the audit for the given version."""
    # Import the core
    from xingce_solver.solvers.analogy_reasoning import solve_analogy_reasoning_core

    # Use provided paths or defaults
    _manifest_path = manifest_path or MANIFEST_PATH
    _answer_key_path = answer_key_path or ANSWER_KEY_PATH

    # Load manifest
    with open(_manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    cases = manifest.get("cases", [])
    answer_key = _load_answer_key(_answer_key_path)

    # Output paths
    if results_path is None:
        results_path = PROJECT_ROOT / "outputs" / f"analogy_reasoning_core_{version}_audit_results.jsonl"
    if summary_path is None:
        summary_path = PROJECT_ROOT / "outputs" / f"analogy_reasoning_core_{version}_audit_summary.md"

    results: list[dict] = []
    total = len(cases)
    solved = 0
    ambiguous = 0
    analysis_only = 0
    inconsistent = 0
    option_correct = 0
    option_wrong = 0
    option_null = 0
    failure_stages: dict[str, int] = {}
    option_status_dist: dict[str, int] = {}

    for case in cases:
        case_id = case.get("case_id", "unknown")
        expected = answer_key.get(case_id, "?")

        # Run solver
        result = solve_analogy_reasoning_core(case)

        # Determine option correctness
        opt_correct = None
        if result.predicted_label is not None:
            if result.predicted_label == expected:
                opt_correct = True
                option_correct += 1
            else:
                opt_correct = False
                option_wrong += 1
        else:
            option_null += 1

        # Count status
        if result.status == "solved":
            solved += 1
        elif result.status == "ambiguous":
            ambiguous += 1
        elif result.status == "analysis_only":
            analysis_only += 1
        elif result.status == "inconsistent":
            inconsistent += 1

        # Count option_status
        option_status_dist[result.option_status] = option_status_dist.get(result.option_status, 0) + 1

        # Determine failure stage
        failure_stage = "none"
        if result.status == "analysis_only":
            if not result.stem_pair or (not result.stem_pair.left and not result.stem_pair.right):
                failure_stage = "stem_parse"
            elif not result.options:
                failure_stage = "option_parse"
            elif all(a.score == 0 for a in result.assessments):
                failure_stage = "relation_detect"
            else:
                failure_stage = "option_match"
        failure_stages[failure_stage] = failure_stages.get(failure_stage, 0) + 1

        # Build result record
        record = {
            "case_id": case_id,
            "expected_answer": expected,
            "status": result.status,
            "stem_pair": f"{result.stem_pair.left}∶{result.stem_pair.right}" if result.stem_pair else "",
            "stem_relation_types": [r.relation_type for r in result.stem_relations],
            "num_options": len(result.options),
            "option_status": result.option_status,
            "predicted_label": result.predicted_label,
            "option_correct": opt_correct,
            "failure_stage": failure_stage,
            "warnings": result.warnings,
            "trace_summary": [
                {
                    "stem_relations": [r.relation_type for r in result.stem_relations],
                }
            ],
        }
        results.append(record)

    # Write JSONL
    with open(results_path, "w", encoding="utf-8") as f:
        for record in results:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Write summary
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"# analogy_reasoning core {version} Audit Summary\n\n")
        f.write("## Overview\n\n")
        f.write(f"- Total: {total}\n")
        f.write(f"- Solved: {solved}\n")
        f.write(f"- Ambiguous: {ambiguous}\n")
        f.write(f"- Analysis_only: {analysis_only}\n")
        f.write(f"- Inconsistent: {inconsistent}\n\n")

        f.write("## Option Status Distribution\n\n")
        for status, count in sorted(option_status_dist.items()):
            f.write(f"- {status}: {count}\n")
        f.write("\n")

        f.write("## Option Correctness\n\n")
        f.write(f"- Correct: {option_correct}\n")
        f.write(f"- Wrong: {option_wrong}\n")
        f.write(f"- Null: {option_null}\n\n")

        f.write("## Failure Stage Distribution\n\n")
        for stage, count in sorted(failure_stages.items()):
            f.write(f"- {stage}: {count}\n")
        f.write("\n")

        f.write("## Per-Case Results\n\n")
        f.write("| case_id | status | stem_relation | option_status | predicted | expected | correct |\n")
        f.write("|---------|--------|---------------|---------------|-----------|----------|---------|\n")
        for record in results:
            correct_str = "✅" if record["option_correct"] else ("❌" if record["option_correct"] is False else "—")
            stem_rel = ", ".join(record["stem_relation_types"][:2]) if record["stem_relation_types"] else "—"
            f.write(
                f"| {record['case_id']} "
                f"| {record['status']} "
                f"| {stem_rel} "
                f"| {record['option_status']} "
                f"| {record['predicted_label'] or '—'} "
                f"| {record['expected_answer']} "
                f"| {correct_str} |\n"
            )
        f.write("\n")

        if option_wrong > 0:
            f.write("## ⚠️ Warning\n\n")
            f.write(f"Found {option_wrong} wrong predictions. Must tighten rules before integration.\n\n")

        f.write("## Recommendation\n\n")
        if option_wrong == 0 and option_correct >= 3:
            f.write("✅ Ready for v1.2 refinement or integration consideration.\n")
        elif option_wrong == 0:
            f.write("✅ No wrong predictions. Continue refinement to increase solved count.\n")
        else:
            f.write("❌ Has wrong predictions. Must fix before proceeding.\n")

    print(f"Audit complete: {results_path}")
    print(f"Summary: {summary_path}")
    print(f"Total={total}, Solved={solved}, Ambiguous={ambiguous}, Analysis_only={analysis_only}")
    print(f"Correct={option_correct}, Wrong={option_wrong}, Null={option_null}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit analogy reasoning core")
    parser.add_argument("--version", default="v1_0", help="Version label for output files")
    parser.add_argument("--input", dest="input_path", help="Path to questions_manifest.json")
    parser.add_argument("--answers", dest="answers_path", help="Path to ANSWER_KEY.md")
    parser.add_argument("--output", dest="output_path", help="Path to output JSONL")
    parser.add_argument("--summary", dest="summary_path", help="Path to output summary MD")
    args = parser.parse_args()

    manifest_path = Path(args.input_path) if args.input_path else None
    answer_key_path = Path(args.answers_path) if args.answers_path else None
    output_path = Path(args.output_path) if args.output_path else None
    summary_path = Path(args.summary_path) if args.summary_path else None

    _run_audit(
        args.version,
        manifest_path=manifest_path,
        answer_key_path=answer_key_path,
        results_path=output_path,
        summary_path=summary_path,
    )


if __name__ == "__main__":
    main()
