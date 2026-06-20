"""
Logic analysis reasoning method scaffold (guidance only, NOT a solver).

Provides structured thinking order, structure checklists, option verification
templates, and uncertainty constraints for future LLM-based reasoning.

This module does NOT output answers. It does NOT integrate with CLI/MCP.
"""
from __future__ import annotations

from typing import Any


def build_logic_analysis_scaffold() -> dict[str, Any]:
    """Build the complete logic analysis method scaffold."""
    return {
        "module": "logic_analysis",
        "version": "v0.1",
        "mode": "method_scaffold_only",
        "positioning": (
            "本模块不是 solver。"
            "本模块不直接枚举答案。"
            "本模块用于约束大模型先抽取对象、属性和约束，再建表/排序轴/分组框架，最后逐项代入选项，无法唯一时 analysis_only。"
        ),
        "stage_order": [
            "题型识别",
            "对象集合抽取",
            "属性集合抽取",
            "约束条件抽取",
            "结构框架建立",
            "条件传播",
            "选项代入验证",
            "唯一性判断",
            "不确定性约束",
        ],
        "problem_type_router": {
            "types": [
                {
                    "type": "排序题",
                    "framework": "建排序轴",
                },
                {
                    "type": "分组题",
                    "framework": "建分组框",
                },
                {
                    "type": "匹配题",
                    "framework": "建对象-属性表",
                },
                {
                    "type": "位置关系题",
                    "framework": "建位置槽",
                },
                {
                    "type": "真假话题",
                    "framework": "建真假约束",
                },
                {
                    "type": "半真半假题",
                    "framework": "拆分每句话的前半/后半",
                },
                {
                    "type": "条件组合题",
                    "framework": "建条件列表并逐步传播",
                },
                {
                    "type": "最大最小题",
                    "framework": "建边界条件和极值约束",
                },
            ],
        },
        "structure_templates": [
            "对象-属性表",
            "排序轴",
            "分组框",
            "位置槽",
            "真假矩阵",
            "半真半假拆句表",
            "条件传播表",
            "选项代入表",
        ],
        "constraint_extraction": {
            "constraints": [
                "确定条件",
                "否定条件",
                "至少",
                "至多",
                "恰好",
                "相邻",
                "不相邻",
                "在……之前",
                "在……之后",
                "同组",
                "不同组",
                "对应",
                "不对应",
                "包含",
                "排除",
                "如果……那么……",
                "只有……才……",
                "除非……否则……",
                "半真半假",
                "一真一假",
            ],
        },
        "option_verification": {
            "steps": [
                "逐项代入 A/B/C/D。",
                "检查是否违反确定条件。",
                "检查是否违反否定条件。",
                "检查是否满足数量约束。",
                "检查是否满足排序/位置/分组/匹配关系。",
                "如果多个 assignment 或多个选项成立，analysis_only。",
            ],
        },
        "response_template": (
            "【题型识别】\n"
            "判断本题属于排序题、分组题、匹配题、位置关系题、真假话题、半真半假题、条件组合题还是最大最小题。\n\n"
            "【对象集合】\n"
            "列出所有需要处理的对象。\n\n"
            "【属性集合】\n"
            "列出所有相关的属性维度。\n\n"
            "【约束条件】\n"
            "从题干中抽取所有确定条件、否定条件、数量约束、位置约束等。\n\n"
            "【结构化表格/框架】\n"
            "建立对应的结构框架（排序轴、分组框、对象-属性表等）。\n\n"
            "【条件推导】\n"
            "基于约束条件进行逻辑推导，传播条件。\n\n"
            "【选项代入】\n"
            "逐选项代入验证是否满足所有约束。\n\n"
            "【唯一性判断】\n"
            "确认只有一个选项满足所有约束。若不唯一，标注 analysis_only。\n\n"
            "【不确定性说明】\n"
            "列出任何导致不确定的因素，标注 analysis_only。"
        ),
        "uncertainty_policy": {
            "triggers": [
                "对象集合不完整 → analysis_only",
                "约束条件无法结构化 → analysis_only",
                "存在多个满足条件的 assignment → analysis_only",
                "多个选项代入均不矛盾 → analysis_only",
                "自然语言条件存在歧义 → analysis_only",
                "排序/分组/匹配框架无法唯一建立 → analysis_only",
            ],
        },
        "must_not_do": [
            "不得凭直觉跳过建表。",
            "不得只看一个条件就选答案。",
            "不得默认选择第一个选项。",
            "不得在多个 assignment 存在时强行选。",
            "不得忽略否定条件。",
            "不得忽略至少/至多/恰好。",
            "不得忽略选项代入验证。",
            "不得用题号、case_id 或标准答案写规则。",
        ],
    }


def get_logic_analysis_stage_order() -> list[str]:
    """Return the ordered thinking stages."""
    return build_logic_analysis_scaffold()["stage_order"]


def get_logic_analysis_structure_checklists() -> dict[str, Any]:
    """Return structure templates and constraint checklists."""
    scaffold = build_logic_analysis_scaffold()
    return {
        "problem_types": [
            t["type"] for t in scaffold["problem_type_router"]["types"]
        ],
        "frameworks": [
            t["framework"] for t in scaffold["problem_type_router"]["types"]
        ],
        "structure_templates": scaffold["structure_templates"],
        "constraints": scaffold["constraint_extraction"]["constraints"],
    }


def render_logic_analysis_prompt_template() -> str:
    """Return the prompt template for logic analysis reasoning."""
    return build_logic_analysis_scaffold()["response_template"]
