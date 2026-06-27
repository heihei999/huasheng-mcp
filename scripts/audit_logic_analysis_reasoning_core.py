"""Audit script for logic_analysis_reasoning_core v0.1 on real exam cases.

Runs solve_analysis_core() on each case in questions_manifest.json,
classifies the result, and outputs structured audit data.

Usage:
    python scripts/audit_logic_analysis_reasoning_core.py \
        --input text-image/logic_analysis_real_cases_open_verified_v1/questions_manifest.json \
        --answers text-image/logic_analysis_real_cases_open_verified_v1/ANSWER_KEY.md \
        --output outputs/logic_analysis_core_v8_0_audit_results.jsonl \
        --summary outputs/logic_analysis_core_v8_0_audit_summary.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from xingce_solver.solvers.logic_analysis_reasoning import (
    AnalysisReasoningResult,
    solve_analysis_core,
)


def load_answer_key(path: str) -> dict[str, str]:
    """Load ANSWER_KEY.md into {case_id: answer_letter}."""
    answers: dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"-\s+(LANALYSIS-\w+):\s+([A-D])", line)
            if m:
                answers[m.group(1)] = m.group(2)
    return answers


def audit_case(case: dict, answer_key: dict[str, str]) -> dict:
    """Audit a single case."""
    case_id = case["case_id"]
    question = case["question"]
    expected = answer_key.get(case_id, case.get("answer", ""))
    options = case.get("options", {})

    result = solve_analysis_core(question, options=options if options else None)

    # Check correctness
    option_correct = None
    if result.predicted_label and expected:
        option_correct = result.predicted_label == expected

    # Determine failure stage
    failure_stage = "none"
    if result.status == "analysis_only":
        if not result.variables:
            failure_stage = "entity_domain_extract"
        elif not result.constraints:
            failure_stage = "constraint_parse"
        elif not result.assignments:
            failure_stage = "assignment_search"
        else:
            failure_stage = "option_mapping"
    elif result.status == "inconsistent":
        failure_stage = "constraint_parse"
    elif result.status == "ambiguous" and result.option_status == "no_supported_option":
        failure_stage = "option_mapping"

    return {
        "case_id": case_id,
        "expected_answer": expected,
        "status": result.status,
        "task_type": result.task_type,
        "num_variables": len(result.variables),
        "num_constraints": len(result.constraints),
        "num_assignments": len(result.assignments),
        "num_consistent_assignments": len(result.assignments),
        "option_status": result.option_status,
        "predicted_label": result.predicted_label,
        "option_correct": option_correct,
        "failure_stage": failure_stage,
        "warnings": result.warnings,
        "option_trace": result.option_trace,
    }


def generate_summary(results: list[dict]) -> str:
    """Generate summary.md content."""
    total = len(results)
    status_counts = {}
    option_counts = {}
    correct_count = 0
    wrong_count = 0
    null_count = 0
    stage_counts = {}
    task_counts = {}

    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
        option_counts[r["option_status"]] = option_counts.get(r["option_status"], 0) + 1
        stage_counts[r["failure_stage"]] = stage_counts.get(r["failure_stage"], 0) + 1
        task_counts[r["task_type"]] = task_counts.get(r["task_type"], 0) + 1

        if r["option_correct"] is True:
            correct_count += 1
        elif r["option_correct"] is False:
            wrong_count += 1
        else:
            null_count += 1

    lines = [
        "# Logic Analysis Reasoning Core v8.0 — Audit Summary",
        "",
        "## Overall",
        "",
        f"- total: {total}",
        f"- solved: {status_counts.get('solved', 0)}",
        f"- ambiguous: {status_counts.get('ambiguous', 0)}",
        f"- inconsistent: {status_counts.get('inconsistent', 0)}",
        f"- analysis_only: {status_counts.get('analysis_only', 0)}",
        "",
        "## Option Mapping Results",
        "",
        f"- unique_supported: {option_counts.get('unique_supported', 0)}",
        f"- ambiguous_options: {option_counts.get('ambiguous_options', 0)}",
        f"- no_supported_option: {option_counts.get('no_supported_option', 0)}",
        f"- not_attempted: {option_counts.get('not_attempted', 0)}",
        "",
        "## Option Correctness",
        "",
        f"- correct: {correct_count}",
        f"- wrong: {wrong_count}",
        f"- null: {null_count}",
        "",
        "## Failure Stage Distribution",
        "",
    ]
    for stage, count in sorted(stage_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {stage}: {count}")

    lines += ["", "## Task Type Distribution", ""]
    for task, count in sorted(task_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {task}: {count}")

    lines += [
        "",
        "## Per-Case Results",
        "",
        "| case_id | task_type | status | option_status | predicted | correct |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        pred = r["predicted_label"] or "-"
        corr = "Y" if r["option_correct"] else ("N" if r["option_correct"] is False else "-")
        lines.append(
            f"| {r['case_id']} | {r['task_type']} | {r['status']} "
            f"| {r['option_status']} | {pred} | {corr} |"
        )

    lines += [
        "",
        "## Recommendation",
        "",
    ]
    if wrong_count > 0:
        lines.append("**Fix wrong answers first.** Convert to no_supported_option or analysis_only.")
    elif correct_count >= 4:
        lines.append("**Consider v8.1 core refinement.** Good foundation for integration.")
    elif correct_count >= 2:
        lines.append("**Continue core enhancement.** Parser and constraint logic need improvement.")
    else:
        lines.append("**Focus on parser improvements.** Most cases fail at entity/domain extraction or constraint parsing.")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Audit logic analysis reasoning core")
    parser.add_argument("--input", required=True, help="Path to questions_manifest.json")
    parser.add_argument("--answers", required=True, help="Path to ANSWER_KEY.md")
    parser.add_argument("--output", required=True, help="Path to output .jsonl")
    parser.add_argument("--summary", required=True, help="Path to summary .md")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        cases = json.load(f)

    answer_key = load_answer_key(args.answers)

    results = []
    for case in cases:
        result = audit_case(case, answer_key)
        results.append(result)

    # Write JSONL
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Write summary
    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(generate_summary(results))

    # Print summary
    print(f"Audit complete: {len(results)} cases")
    for r in results:
        pred = r["predicted_label"] or "-"
        corr = "Y" if r["option_correct"] else ("N" if r["option_correct"] is False else "-")
        print(f"  {r['case_id']}: {r['status']} task={r['task_type']} option={r['option_status']} pred={pred} correct={corr}")


if __name__ == "__main__":
    main()
