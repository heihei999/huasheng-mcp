"""Audit script for truth_reasoning_core on real exam cases.

Runs solve_truth_core() on each case, extracts options, maps options to
assignment facts, and outputs structured audit data.

Usage:
    python scripts/audit_truth_reasoning_core.py \
        --input text-image/logic_truth_real_cases_open_verified_v1/questions_manifest.json \
        --answers text-image/logic_truth_real_cases_open_verified_v1/ANSWER_KEY.md \
        --output outputs/truth_reasoning_core_v0_4_audit_results.jsonl \
        --summary outputs/truth_reasoning_core_v0_4_audit_summary.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from xingce_solver.solvers.truth_reasoning import (
    OptionClaim,
    TruthReasoningResult,
    extract_binary_domains,
    extract_options,
    extract_statements,
    map_options_to_assignments,
    parse_statement,
    parse_truth_constraint,
    solve_truth_core,
)


def load_answer_key(path: str) -> dict[str, str]:
    """Load ANSWER_KEY.md into {case_id: answer_letter}."""
    answers: dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"-\s+(LTRUTH-REAL-\d+):\s+([A-D])", line)
            if m:
                answers[m.group(1)] = m.group(2)
    return answers


def classify_failure_stage(
    case: dict,
    constraint,
    raw_stmts: list,
    propositions: list,
    result: TruthReasoningResult,
) -> str:
    """Determine the failure stage for a case."""
    if result.status == "solved":
        return "none"

    if constraint.true_count is None and constraint.false_count is None:
        return "parse_constraint"

    if len(raw_stmts) < 2:
        return "extract_statements"

    parsed = [p for p in propositions if p is not None]
    if len(parsed) < 2:
        return "parse_statement"

    if result.status in ("inconsistent", "ambiguous"):
        return "assignment"

    if result.status == "analysis_only":
        for w in result.warnings:
            if "no_statements" in w:
                return "extract_statements"
            if "statements_parsed" in w:
                return "parse_statement"
        return "derive_facts"

    return "none"


def audit_case(case: dict, answer_key: dict[str, str]) -> dict:
    """Audit a single case with option mapping."""
    case_id = case["case_id"]
    question = case["question"]
    expected = answer_key.get(case_id, case.get("answer", ""))

    # Parse components
    constraint = parse_truth_constraint(question)
    raw_stmts = extract_statements(question)
    propositions = [parse_statement(s["text"]) for s in raw_stmts]

    # Solve
    result = solve_truth_core(question)

    # Classify failure
    failure_stage = classify_failure_stage(
        case, constraint, raw_stmts, propositions, result
    )

    # Build trace summary
    trace_summary = []
    for i, (stmt, prop) in enumerate(zip(raw_stmts, propositions)):
        entry = {
            "index": i,
            "speaker": stmt.get("speaker"),
            "text": stmt["text"][:80],
            "parsed_kind": prop.kind if prop else None,
        }
        trace_summary.append(entry)

    # Facts count from assignments
    facts_count = 0
    if result.assignments:
        facts_count = len(result.assignments[0].get("facts", {}))

    # Option mapping — use options from JSON if available, else extract from text
    raw_options = case.get("options", {})
    if raw_options and isinstance(raw_options, dict):
        options = [
            OptionClaim(label=label, raw=text)
            for label, text in sorted(raw_options.items())
        ]
    else:
        options = extract_options(question)

    option_status = "not_attempted"
    predicted_label = None
    option_correct = None
    option_trace = []
    option_warnings = []

    if options and result.assignments:
        valid_assignments = [
            (a["assignment"], a["facts"]) for a in result.assignments
        ]
        mapping_result = map_options_to_assignments(
            options, valid_assignments,
            question_text=question,
            propositions=propositions,
        )
        option_status = mapping_result.option_status
        predicted_label = mapping_result.selected_label
        option_trace = mapping_result.option_trace
        option_warnings = mapping_result.warnings

        # Check correctness (only for audit, not used in reasoning)
        if predicted_label and expected:
            option_correct = predicted_label == expected
    elif not options:
        option_status = "not_attempted"
        option_warnings = ["no_options_extracted"]
    elif not result.assignments:
        option_status = "not_attempted"
        option_warnings = ["no_assignments"]

    # Binary domains and universal instantiation stats
    binary_domains = extract_binary_domains(question)
    num_binary_domains = len(binary_domains)

    return {
        "case_id": case_id,
        "expected_answer": expected,
        "status": result.status,
        "num_statements": len(raw_stmts),
        "constraint": {
            "true_count": constraint.true_count,
            "false_count": constraint.false_count,
            "raw": constraint.raw,
        },
        "num_assignments": len(result.assignments),
        "facts_count": facts_count,
        "failure_stage": failure_stage,
        "option_status": option_status,
        "predicted_label": predicted_label,
        "option_correct": option_correct,
        "num_binary_domains": num_binary_domains,
        "option_trace": option_trace,
        "warnings": result.warnings + option_warnings,
        "trace_summary": trace_summary,
    }


def generate_summary(results: list[dict]) -> str:
    """Generate summary.md content."""
    total = len(results)
    status_counts = {}
    stage_counts = {}
    option_counts = {}
    correct_count = 0
    wrong_count = 0
    null_count = 0

    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
        stage_counts[r["failure_stage"]] = stage_counts.get(r["failure_stage"], 0) + 1
        option_counts[r["option_status"]] = option_counts.get(r["option_status"], 0) + 1

        if r["option_correct"] is True:
            correct_count += 1
        elif r["option_correct"] is False:
            wrong_count += 1
        else:
            null_count += 1

    # Binary domain stats
    binary_domain_cases = sum(1 for r in results if r.get("num_binary_domains", 0) > 0)

    lines = [
        "# Truth Reasoning Core v0.5 — Normalization & First-Order Audit Summary",
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

    lines += [
        "",
        "## Binary Domains",
        "",
        f"- cases with binary domains: {binary_domain_cases}",
        "",
        "## Per-Case Results",
        "",
        "| case_id | expected | status | option_status | predicted | correct | bin_domains |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        pred = r["predicted_label"] or "-"
        corr = "Y" if r["option_correct"] else ("N" if r["option_correct"] is False else "-")
        bin_d = r.get("num_binary_domains", 0)
        lines.append(
            f"| {r['case_id']} | {r['expected_answer']} | {r['status']} "
            f"| {r['option_status']} | {pred} | {corr} | {bin_d} |"
        )

    # Option trace detail
    lines += ["", "## Option Trace Detail", ""]
    for r in results:
        if r["option_trace"]:
            lines.append(f"### {r['case_id']} (status={r['status']}, option_status={r['option_status']})")
            for ot in r["option_trace"]:
                ent_str = ", ".join(
                    "T" if e is True else "F" if e is False else "?"
                    for e in ot.get("entailments", [])
                )
                lines.append(f"- {ot['label']}: {ot['option_status']} [{ent_str}] {ot['raw'][:60]}")
            lines.append("")

    # Analysis
    lines += ["## Analysis", ""]
    unique_cases = [r for r in results if r["option_status"] == "unique_supported"]
    if unique_cases:
        lines.append("### unique_supported cases")
        for r in unique_cases:
            lines.append(f"- {r['case_id']}: predicted={r['predicted_label']}, expected={r['expected_answer']}, correct={r['option_correct']}")
    else:
        lines.append("### unique_supported cases: (none)")

    lines += ["", "## Recommendation", ""]
    if correct_count >= 8:
        lines.append("**Consider v7 integration.** Option mapping is working well.")
    elif correct_count >= 5:
        lines.append("**Continue to v0.5.** Option mapping shows promise but needs more work.")
    else:
        lines.append("**Continue core enhancement.** Option mapping accuracy too low for integration.")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Audit truth reasoning core on real cases")
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
        print(f"  {r['case_id']}: {r['status']} option={r['option_status']} pred={pred} correct={corr}")


if __name__ == "__main__":
    main()
