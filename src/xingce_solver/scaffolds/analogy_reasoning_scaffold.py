"""
Analogy reasoning method scaffold (guidance only, NOT a solver).

Provides structured thinking order, relation checklists, option comparison
templates, and uncertainty constraints for future LLM-based reasoning.

This module does NOT output answers. It does NOT integrate with CLI/MCP.
"""
from __future__ import annotations

from typing import Any


def build_analogy_reasoning_scaffold() -> dict[str, Any]:
    """Build the complete analogy reasoning method scaffold."""
    return {
        "module": "analogy_reasoning",
        "version": "v0.1",
        "mode": "method_scaffold_only",
        "positioning": (
            "本模块不是 solver。"
            "本模块不直接选择答案。"
            "本模块用于约束大模型先识别词项结构，再造句验证关系，再逐项比较选项，无法唯一时 analysis_only。"
        ),
        "stage_order": [
            "题干形式识别",
            "词性与结构检查",
            "题干关系造句",
            "关系类型识别",
            "选项关系套入",
            "横纵比较",
            "最优关系判断",
            "不确定性约束",
        ],
        "question_forms": [
            "二词型",
            "三词型",
            "填空型",
            "括号型",
            "对应型",
        ],
        "relation_types": [
            "近义关系",
            "反义关系",
            "种属关系",
            "组成关系",
            "整体-部分",
            "功能关系",
            "属性关系",
            "因果关系",
            "条件关系",
            "目的关系",
            "工具-用途",
            "职业-工具",
            "地点-行为",
            "主体-动作",
            "动作-对象",
            "原材料-成品",
            "作品-作者",
            "象征关系",
            "并列关系",
            "顺承关系",
            "程度关系",
            "必然关系",
            "或然关系",
        ],
        "relation_verification": {
            "steps": [
                "用一句自然语言描述题干关系。",
                "同一句关系必须能套入选项。",
                "检查关系方向是否一致。",
                "检查词性是否一致。",
                "检查语义层级是否一致。",
                "检查关系强弱是否一致。",
                "检查必然关系还是或然关系。",
            ],
            "rules": [
                "能说通不等于最优。",
                "类比题要找与题干关系最一致的选项。",
            ],
        },
        "option_comparison": {
            "steps": [
                "先排除词性不一致。",
                "再排除关系方向不一致。",
                "再排除关系类型不一致。",
                "再比较关系强弱。",
                "再比较具体/抽象层级。",
                "如果多个选项都成立，analysis_only。",
            ],
        },
        "response_template": (
            "【题干形式】\n"
            "判断本题是二词型、三词型、填空型、括号型还是对应型。\n\n"
            "【词性结构】\n"
            "分析题干词项的词性和语法结构。\n\n"
            "【题干造句】\n"
            "用一句自然语言描述题干关系。\n\n"
            "【关系类型】\n"
            "识别题干关系属于哪种类型。\n\n"
            "【选项套入】\n"
            "将题干关系套入每个选项，检查是否成立。\n\n"
            "【横纵比较】\n"
            "比较选项间的关系强弱、方向、层级差异。\n\n"
            "【唯一性判断】\n"
            "确认只有一个选项与题干关系最一致。若不唯一，标注 analysis_only。\n\n"
            "【不确定性说明】\n"
            "列出任何导致不确定的因素，标注 analysis_only。"
        ),
        "uncertainty_policy": {
            "triggers": [
                "题干关系无法稳定造句 → analysis_only",
                "多个关系类型都能解释题干 → analysis_only",
                "多个选项关系同样成立 → analysis_only",
                "词义依赖专业常识且无法确认 → analysis_only",
                "关系强弱无法区分 → analysis_only",
                "题干方向与选项方向无法比较 → analysis_only",
            ],
        },
        "must_not_do": [
            "不得只凭两个词'有关'就判断。",
            "不得只看常识熟悉度。",
            "不得忽略关系方向。",
            "不得忽略词性一致性。",
            "不得忽略具体/抽象层级。",
            "不得在多个选项都能说通时强行选。",
            "不得默认选择第一个选项。",
            "不得用题号、case_id 或标准答案写规则。",
        ],
    }


def get_analogy_reasoning_stage_order() -> list[str]:
    """Return the ordered thinking stages."""
    return build_analogy_reasoning_scaffold()["stage_order"]


def get_analogy_reasoning_relation_checklists() -> dict[str, Any]:
    """Return relation type checklists and verification steps."""
    scaffold = build_analogy_reasoning_scaffold()
    return {
        "relation_types": scaffold["relation_types"],
        "verification_steps": scaffold["relation_verification"]["steps"],
        "verification_rules": scaffold["relation_verification"]["rules"],
        "comparison_steps": scaffold["option_comparison"]["steps"],
    }


def render_analogy_reasoning_prompt_template() -> str:
    """Return the prompt template for analogy reasoning."""
    return build_analogy_reasoning_scaffold()["response_template"]
