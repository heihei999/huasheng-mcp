"""
Definition judgement method scaffold (guidance only, NOT a solver).

Provides structured thinking order, element checklists, option verification
templates, and uncertainty constraints for future LLM-based reasoning.

This module does NOT output answers. It does NOT integrate with CLI/MCP.
"""
from __future__ import annotations

from typing import Any


def build_definition_judgement_scaffold() -> dict[str, Any]:
    """Build the complete definition judgement method scaffold."""
    return {
        "module": "definition_judgement",
        "version": "v0.1",
        "mode": "method_scaffold_only",
        "positioning": (
            "本模块不是 solver。"
            "本模块不直接判断答案。"
            "本模块用于约束大模型按定义判断方法抽取定义要素、逐项验证选项，并在无法唯一时 analysis_only。"
        ),
        "stage_order": [
            "问法识别",
            "定义句定位",
            "定义要素抽取",
            "必要条件区分",
            "选项逐项匹配",
            "选是/选非校验",
            "唯一性判断",
            "不确定性约束",
        ],
        "question_polarity": {
            "positive_forms": [
                "符合定义",
                "属于",
                "正确",
                "选是",
            ],
            "negative_forms": [
                "不符合定义",
                "不属于",
                "错误",
                "选非",
            ],
            "rule": (
                "先识别问法正负极性。"
                "选非题必须反向验证，不能按符合定义直接选择。"
            ),
        },
        "definition_elements": {
            "elements": [
                "主体",
                "客体",
                "条件",
                "方式",
                "目的",
                "结果",
                "原因",
                "时间",
                "地点",
                "对象范围",
                "排除项",
                "例外项",
                "必要条件",
                "附加描述",
            ],
            "rules": [
                "必要条件缺失时优先排除。",
                "附加描述不能当成必要条件。",
                "词面不一致不等于语义不一致。",
                "语义等价时不得因关键词不重合直接排除。",
            ],
        },
        "option_verification": {
            "steps": [
                "逐选项列出是否满足主体、客体、条件、方式、目的、结果、排除项。",
                "先找核心必要条件。",
                "再看附加条件。",
                "再处理选是/选非。",
                "若多个选项都满足或都不满足，analysis_only。",
            ],
        },
        "response_template": (
            "【问法极性】\n"
            "明确本题是选是题还是选非题，写出极性判断依据。\n\n"
            "【定义要素】\n"
            "从定义句中抽取主体、客体、条件、方式、目的、结果、排除项等要素。\n\n"
            "【必要条件】\n"
            "列出核心必要条件，区分必要条件与附加描述。\n\n"
            "【选项核验】\n"
            "逐选项检查是否满足每个必要条件。\n\n"
            "【排除理由】\n"
            "对不满足的选项给出具体排除理由。\n\n"
            "【唯一性判断】\n"
            "确认只有一个选项满足所有必要条件。若不唯一，标注 analysis_only。\n\n"
            "【不确定性说明】\n"
            "列出任何导致不确定的因素，标注 analysis_only。"
        ),
        "uncertainty_policy": {
            "triggers": [
                "定义要素无法完整抽取 → analysis_only",
                "问法极性不明确 → analysis_only",
                "多个选项同时符合 → analysis_only",
                "多个选项同时不符合 → analysis_only",
                "选项语义需要外部专业知识且无法确认 → analysis_only",
                "必要条件与附加描述无法区分 → analysis_only",
            ],
        },
        "must_not_do": [
            "不得只按关键词重合判断。",
            "不得忽略选是/选非。",
            "不得把例子当定义。",
            "不得把附加描述当必要条件。",
            "不得在多个选项都可解释时强行选。",
            "不得默认选择第一个选项。",
            "不得用题号、case_id 或标准答案写规则。",
        ],
    }


def get_definition_judgement_stage_order() -> list[str]:
    """Return the ordered thinking stages."""
    return build_definition_judgement_scaffold()["stage_order"]


def get_definition_judgement_element_checklists() -> dict[str, Any]:
    """Return definition element checklists."""
    scaffold = build_definition_judgement_scaffold()
    return {
        "elements": scaffold["definition_elements"]["elements"],
        "rules": scaffold["definition_elements"]["rules"],
        "option_verification": scaffold["option_verification"]["steps"],
    }


def render_definition_judgement_prompt_template() -> str:
    """Return the prompt template for definition judgement reasoning."""
    return build_definition_judgement_scaffold()["response_template"]
