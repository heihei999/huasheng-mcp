from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .kb import KnowledgeBase, KnowledgeBaseError
from .router import classify_question
from .solvers import solve_data_analysis, solve_logic_reasoning


def _dump_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _compact_card(card: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": card.get("id"),
        "method_name": card.get("method_name"),
        "module": card.get("module"),
        "question_type": card.get("question_type"),
        "sub_type": card.get("sub_type"),
        "tags": card.get("tags", []),
        "confidence": card.get("confidence"),
        "need_review": card.get("need_review", False),
    }


def _print_data_analysis_solution(result: dict[str, Any]) -> None:
    def show_list(values: list[Any]) -> str:
        return "、".join(str(value) for value in values) if values else "未识别"

    print("题型判断")
    print(f"- 模块：{result.get('module')}")
    print(f"- 题型：{result.get('question_type') or '未识别'}")
    print(f"- 子题型：{result.get('sub_type') or '未识别'}")
    print(f"- 需要更多数据：{result.get('needs_more_data')}")
    print()

    print("调用方法")
    for method in result.get("recommended_methods", []):
        print(
            f"- {method.get('method_id')}：{method.get('method_name')} "
            f"({method.get('reason')})"
        )
    if not result.get("recommended_methods"):
        print("- 未推荐")
    print()

    print("关键要素")
    elements = result.get("extracted_elements", {})
    print(f"- 时间：{show_list(elements.get('time', []))}")
    print(f"- 主体：{show_list(elements.get('subject', []))}")
    print(f"- 指标：{show_list(elements.get('metrics', []))}")
    print(f"- 数字：{show_list(elements.get('numbers', []))}")
    print(f"- 百分数/百分点：{show_list(elements.get('rates', []))}")
    print(f"- 百分点：{show_list(elements.get('percentage_points', []))}")
    print(f"- 单位：{show_list(elements.get('units', []))}")
    print(f"- 选项值：{show_list(elements.get('option_values', []))}")
    for option in elements.get("options", []):
        print(
            f"  - {option.get('label')}. {option.get('raw')} "
            f"(value={option.get('value')}, unit={option.get('unit')})"
        )
    print()

    print("选项差距判断")
    gap = result.get("option_gap_analysis", {})
    print(f"- 是否有选项：{gap.get('has_options')}")
    print(f"- 差距级别：{gap.get('gap_level')}")
    print(f"- 推荐精度：{gap.get('recommended_precision')}")
    for note in gap.get("gap_notes", []):
        print(f"- {note}")
    print()

    print("公式草案")
    formula = result.get("formula_plan", {})
    print(f"- 公式：{formula.get('formula') or '未识别'}")
    print(f"- 变量：{json.dumps(formula.get('variables', {}), ensure_ascii=False)}")
    print(f"- 缺失变量：{show_list(formula.get('missing_variables', []))}")
    print()

    print("估算草案")
    for step in result.get("estimation_plan", []):
        print(f"- {step}")
    if not result.get("estimation_plan"):
        print("- 暂无")
    print()

    print("computed_result / answer_candidate")
    print(f"- computed_result：{result.get('computed_result')}")
    candidate = result.get("answer_candidate")
    print(f"- answer_candidate：{json.dumps(candidate, ensure_ascii=False) if candidate else 'null'}")
    print()

    print("解题步骤草案")
    for step in result.get("solving_plan", []):
        print(f"- {step}")
    if not result.get("solving_plan"):
        print("- 暂无")
    print()

    print("考场速算策略")
    policy = result.get("calculation_policy", {})
    print(f"- 允许精确计算：{policy.get('allow_exact_calculation')}")
    print(f"- 优先估算：{policy.get('prefer_estimation')}")
    print(f"- 必须检查选项差距：{policy.get('must_check_option_gap')}")
    for item in policy.get("forbidden", []):
        print(f"- {item}")
    print()

    print("警告/缺失信息")
    for warning in result.get("warnings", []):
        print(f"- {warning}")
    if not result.get("warnings"):
        print("- 无")
    print()

    print("来源 method_id")
    print(show_list(result.get("source_method_ids", [])))
    print()

    print("说明草案")
    print(result.get("exam_style_explanation_draft", ""))


def _print_logic_reasoning_solution(result: dict[str, Any]) -> None:
    def show_list(values: list[Any]) -> str:
        return "、".join(str(value) for value in values) if values else "未识别"

    print("题型判断")
    print(f"- 模块：{result.get('module')}")
    print(f"- 题型：{result.get('question_type') or '未识别'}")
    print(f"- 子题型：{result.get('sub_type') or '未识别'}")
    print(f"- 需要更多数据：{result.get('needs_more_data')}")
    stem = result.get("question_stem_analysis", {})
    print(f"- 问法：{stem.get('stem_type') or '未识别'}")
    print(f"- 任务：{stem.get('task') or '未识别'}")
    print()

    print("调用方法")
    for method in result.get("recommended_methods", []):
        print(
            f"- {method.get('method_id')}：{method.get('method_name')} "
            f"({method.get('reason')})"
        )
    if not result.get("recommended_methods"):
        print("- 未推荐")
    print()

    argument = result.get("argument_structure", {})
    print("论点")
    print(f"- {argument.get('conclusion') or '未识别'}")
    print()

    print("论据")
    for premise in argument.get("premises", []):
        print(f"- {premise}")
    if not argument.get("premises"):
        print("- 未识别")
    print()

    print("论证关系")
    print(f"- 推理链：{argument.get('reasoning_chain') or '未识别'}")
    print(f"- 缺口：{argument.get('gap') or '未识别'}")
    print()

    print("选项分析")
    for option in result.get("option_analysis", []):
        print(
            f"- {option.get('label')}. {option.get('text')} | "
            f"{option.get('relation_to_argument')} | {option.get('effect')} | "
            f"力度：{option.get('strength_level')}"
        )
    if not result.get("option_analysis"):
        print("- 暂无")
    print()

    candidate = result.get("answer_candidate")
    print("答案候选")
    print(json.dumps(candidate, ensure_ascii=False) if candidate else "null")
    print()

    print("解题步骤草案")
    for step in result.get("solving_plan", []):
        print(f"- {step}")
    if not result.get("solving_plan"):
        print("- 暂无")
    print()

    print("warnings")
    for warning in result.get("warnings", []):
        print(f"- {warning}")
    if not result.get("warnings"):
        print("- 无")
    print()

    print("依据 method_id")
    print(show_list(result.get("source_method_ids", [])))
    print()

    print("说明草案")
    print(result.get("exam_style_explanation_draft", ""))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="xingce-solver")
    parser.add_argument("--kb-dir", help="Path to knowledge_base/. Defaults to ./knowledge_base.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search method cards.")
    search_parser.add_argument("--query", required=True, help="Keyword query, e.g. '比重 增长率'.")
    search_parser.add_argument("--module", help="Optional exact module filter.")
    search_parser.add_argument("--top-k", type=int, default=5, help="Maximum number of results.")

    card_parser = subparsers.add_parser("card", help="Show a method card by id.")
    card_parser.add_argument("--id", required=True, dest="method_id", help="Method id.")

    classify_parser = subparsers.add_parser("classify", help="Classify a question text file.")
    classify_parser.add_argument("--question", required=True, help="Path to question text file.")
    classify_parser.add_argument("--top-k", type=int, default=5, help="Maximum number of routes.")

    source_parser = subparsers.add_parser("source", help="Show source references by method id.")
    source_parser.add_argument("--method-id", required=True, help="Method id.")

    solve_data_parser = subparsers.add_parser(
        "solve-data", help="Build a structured data-analysis solving draft."
    )
    solve_data_input = solve_data_parser.add_mutually_exclusive_group(required=True)
    solve_data_input.add_argument("--question", help="Path to question text file.")
    solve_data_input.add_argument("--text", help="Question text.")

    solve_logic_parser = subparsers.add_parser(
        "solve-logic", help="Build a structured logic-reasoning solving draft."
    )
    solve_logic_input = solve_logic_parser.add_mutually_exclusive_group(required=True)
    solve_logic_input.add_argument("--question", help="Path to question text file.")
    solve_logic_input.add_argument("--text", help="Question text.")

    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        kb = KnowledgeBase(args.kb_dir)

        if args.command == "search":
            results = kb.search_methods(args.query, args.module, args.top_k)
            _dump_json([_compact_card(card) for card in results])
            return 0

        if args.command == "card":
            card = kb.get_method_card(args.method_id)
            if card is None:
                print(f"Method card not found: {args.method_id}", file=sys.stderr)
                return 1
            _dump_json(card)
            return 0

        if args.command == "classify":
            question_path = Path(args.question)
            question_text = question_path.read_text(encoding="utf-8")
            _dump_json(classify_question(question_text, args.kb_dir, args.top_k))
            return 0

        if args.command == "source":
            reference = kb.get_source_reference(args.method_id)
            if reference is None:
                print(f"Method card not found: {args.method_id}", file=sys.stderr)
                return 1
            _dump_json(reference)
            return 0

        if args.command == "solve-data":
            if args.question:
                question_text = Path(args.question).read_text(encoding="utf-8")
            else:
                question_text = args.text
            result = solve_data_analysis(question_text, kb_dir=args.kb_dir)
            _print_data_analysis_solution(result)
            return 0

        if args.command == "solve-logic":
            if args.question:
                question_text = Path(args.question).read_text(encoding="utf-8")
            else:
                question_text = args.text
            result = solve_logic_reasoning(question_text, kb_dir=args.kb_dir)
            _print_logic_reasoning_solution(result)
            return 0

    except (OSError, KnowledgeBaseError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
