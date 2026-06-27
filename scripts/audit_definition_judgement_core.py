"""Audit script for definition_judgement_core on real exam cases.

Runs solve_definition_judgement_core() on each case in questions_manifest.json,
classifies the result, and outputs structured audit data.

Usage:
    python scripts/audit_definition_judgement_core.py \
        --input text-image/definition_judgement_real_cases_open_verified_v1/questions_manifest.json \
        --answers text-image/definition_judgement_real_cases_open_verified_v1/ANSWER_KEY.md \
        --output outputs/definition_judgement_core_v1_0_audit_results.jsonl \
        --summary outputs/definition_judgement_core_v1_0_audit_summary.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from xingce_solver.solvers.definition_judgement import (
    DefinitionJudgementResult,
    solve_definition_judgement_core,
)


def load_answer_key(path: str) -> dict[str, str]:
    """Load ANSWER_KEY.md into {case_id: answer_letter}."""
    answers: dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*(dj_open_v1_\d+)\s*\|.*?\|\s*([A-D])\s*\|", line)
            if m:
                answers[m.group(1)] = m.group(2)
    return answers


def audit_case(case: dict, answer_key: dict[str, str]) -> dict:
    """Audit a single case."""
    case_id = case["case_id"]
    question = case["question_text"]
    expected = answer_key.get(case_id, case.get("expected_answer", case.get("answer", "")))
    options = case.get("options", {})
    polarity = case.get("polarity", "")

    result = solve_definition_judgement_core(question, options=options if options else None)

    # Determine failure stage
    failure_stage = "none"
    if result.status == "analysis_only":
        if not result.definitions:
            failure_stage = "definition_parse"
        elif not result.options:
            failure_stage = "option_parse"
        else:
            failure_stage = "option_assessment"
    elif result.status == "ambiguous":
        failure_stage = "option_assessment"

    # Check correctness
    option_correct = None
    if result.predicted_label and expected:
        option_correct = result.predicted_label == expected

    return {
        "case_id": case_id,
        "expected_answer": expected,
        "status": result.status,
        "question_polarity": result.question_polarity,
        "target_definition": result.target_definition,
        "num_definitions": len(result.definitions),
        "num_definition_elements": sum(len(d.elements) for d in result.definitions),
        "num_options": len(result.options),
        "option_status": result.option_status,
        "predicted_label": result.predicted_label,
        "option_correct": option_correct,
        "failure_stage": failure_stage,
        "warnings": result.warnings,
        "assessments": [
            {
                "label": a.label,
                "status": a.status,
                "matched": a.matched_elements,
                "missing": a.missing_elements,
                "violated": a.violated_elements,
                "score": a.score,
            }
            for a in result.assessments
        ],
    }


def generate_summary(results: list[dict]) -> str:
    """Generate summary.md content."""
    total = len(results)
    status_counts = {}
    option_counts = {}
    stage_counts = {}
    correct = wrong = null = 0

    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
        option_counts[r["option_status"]] = option_counts.get(r["option_status"], 0) + 1
        stage_counts[r["failure_stage"]] = stage_counts.get(r["failure_stage"], 0) + 1

        if r["option_correct"] is True:
            correct += 1
        elif r["option_correct"] is False:
            wrong += 1
        else:
            null += 1

    lines = [
        "# Definition Judgement Core — Audit Summary",
        "",
        "## Overall",
        "",
        f"- total: {total}",
        f"- solved: {status_counts.get('solved', 0)}",
        f"- ambiguous: {status_counts.get('ambiguous', 0)}",
        f"- analysis_only: {status_counts.get('analysis_only', 0)}",
        f"- inconsistent: {status_counts.get('inconsistent', 0)}",
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
        f"- correct: {correct}",
        f"- wrong: {wrong}",
        f"- null: {null}",
        "",
        "## Failure Stage Distribution",
        "",
    ]
    for stage, count in sorted(stage_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {stage}: {count}")

    lines += [
        "",
        "## Per-Case Results",
        "",
        "| case_id | expected | status | polarity | option_status | predicted | correct | failure_stage |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        pred = r["predicted_label"] or "-"
        corr = "Y" if r["option_correct"] else ("N" if r["option_correct"] is False else "-")
        lines.append(
            f"| {r['case_id']} | {r['expected_answer']} | {r['status']} "
            f"| {r['question_polarity']} | {r['option_status']} | {pred} | {corr} | {r['failure_stage']} |"
        )

    # Option assessment details
    lines += ["", "## Option Assessment Details", ""]
    for r in results:
        if r["assessments"]:
            lines.append(f"### {r['case_id']} (polarity={r['question_polarity']})")
            for a in r["assessments"]:
                lines.append(f"- {a['label']}: {a['status']} matched={a['matched']} missing={a['missing']} violated={a['violated']} score={a['score']:.2f}")
            lines.append("")

    # Recommendation
    lines += ["## Recommendation", ""]
    if wrong > 0:
        lines.append("**Fix wrong answers first.** Tighten option assessment logic.")
    elif correct >= 3:
        lines.append("**Consider v1.2 refinement or conservative integration.**")
    elif correct >= 1:
        lines.append("**Continue v1.1 refinement.** Improve element extraction and option matching.")
    else:
        lines.append("**Focus on parser improvements.** Most cases fail at definition parsing or element extraction.")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Audit definition judgement core")
    parser.add_argument("--input", required=True, help="Path to questions_manifest.json")
    parser.add_argument("--answers", required=True, help="Path to ANSWER_KEY.md")
    parser.add_argument("--output", required=True, help="Path to output .jsonl")
    parser.add_argument("--summary", required=True, help="Path to summary .md")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    # Handle both list and dict formats
    if isinstance(data, list):
        cases = data
    elif isinstance(data, dict) and "cases" in data:
        cases = data["cases"]
    else:
        raise ValueError("Unsupported manifest format")

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
        print(f"  {r['case_id']}: {r['status']} polarity={r['question_polarity']} option={r['option_status']} pred={pred} correct={corr}")


if __name__ == "__main__":
    main()
