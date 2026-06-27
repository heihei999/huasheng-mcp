"""Graphic reasoning method scaffold for multi-modal LLM guidance.

This module constructs observation scaffolds for 图形推理 (graphic reasoning)
questions. It is NOT a solver. It does NOT recognize images. It does NOT
output answers. It only generates structured guidance for future multi-modal
LLM integration.

Version: v0.2.1 — visual grounding addendum
"""

from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_graphic_reasoning_scaffold() -> dict[str, Any]:
    """Build the complete graphic reasoning method scaffold.

    Returns a stable, testable dict containing stage order, composition
    router, visual checklists, response template, uncertainty policy,
    must-not-do constraints, specialized templates, visual transcription
    protocol, and anti-pattern guards.
    """
    return {
        "module": "graphic_reasoning",
        "version": "v0.2.1",
        "mode": "method_scaffold_only",
        "positioning": _build_positioning(),
        "stage_order": get_graphic_reasoning_stage_order(),
        "composition_router": _build_composition_router(),
        "visual_checklists": get_graphic_reasoning_visual_checklists(),
        "response_template": render_graphic_reasoning_prompt_template(),
        "uncertainty_policy": _build_uncertainty_policy(),
        "must_not_do": _build_must_not_do(),
        "specialized_templates": get_specialized_templates(),
        "visual_transcription_protocol": get_visual_transcription_protocol(),
        "anti_pattern_guards": get_anti_pattern_guards(),
        "black_white_operation_rules": get_black_white_operation_rules(),
        "falsification_protocol": get_falsification_protocol(),
        "spatial_verification_protocol": get_spatial_verification_protocol(),
        "uncertainty_reporting_protocol": get_uncertainty_reporting_protocol(),
    }


def get_graphic_reasoning_stage_order() -> list[str]:
    """Return the ten-layer observation order for graphic reasoning."""
    return [
        "命题形式",
        "组成关系",
        "属性规律",
        "数量规律",
        "位置规律",
        "样式规律",
        "特殊题型",
        "空间类题型",
        "选项验证",
        "不确定性约束",
    ]


def get_graphic_reasoning_visual_checklists() -> dict[str, Any]:
    """Return all visual checklists for graphic reasoning."""
    return {
        "命题形式": _checklist_proposition_form(),
        "属性规律": _checklist_attribute_rules(),
        "数量规律": _checklist_quantity_rules(),
        "位置规律": _checklist_position_rules(),
        "样式规律": _checklist_style_rules(),
        "图形间关系": _checklist_inter_figure_relations(),
        "功能元素": _checklist_functional_elements(),
        "黑白块": _checklist_black_white_blocks(),
        "汉字类": _checklist_chinese_characters(),
        "数字类": _checklist_digits(),
        "字母类": _checklist_letters(),
        "六面体展开图": _checklist_cube_net(),
        "截面图": _checklist_cross_section(),
        "三视图": _checklist_three_views(),
        "立体拼合": _checklist_solid_assembly(),
    }


def get_specialized_templates() -> dict[str, Any]:
    """Return the 7 specialized forced-verification templates.

    Each template enforces a mandatory verification procedure for a specific
    graphic reasoning sub-type. Models must follow these templates instead of
    relying on first-glance intuition.
    """
    return {
        "grid_black_shape": _template_grid_black_shape(),
        "complex_black_white_pattern": _template_complex_black_white_pattern(),
        "line_symbol_pattern": _template_line_symbol_pattern(),
        "three_views": _template_three_views(),
        "cube_net": _template_cube_net(),
        "solid_assembly": _template_solid_assembly(),
        "grouping_classification": _template_grouping_classification(),
    }


def get_visual_transcription_protocol() -> dict[str, Any]:
    """Return the mandatory visual transcription protocol.

    All graphic reasoning questions MUST complete visual transcription
    before any reasoning begins. If transcription is incomplete or key
    details are uncertain, the model should output analysis_only.
    """
    return {
        "mandatory": True,
        "timing": "在正式推理之前，必须先完成视觉转写",
        "required_fields": [
            "proposition_form",
            "image_present",
            "figure_count",
            "option_count",
            "given_figures_visual_facts",
            "options_visual_facts",
            "uncertain_visual_details",
        ],
        "field_descriptions": {
            "proposition_form": "命题形式：一组图/两组图/九宫格/分组分类/空间重构/其他",
            "image_present": "是否有图：true/false",
            "figure_count": "题干图形数量",
            "option_count": "选项数量（通常为 A/B/C/D 四个）",
            "given_figures_visual_facts": "每个已知图的视觉事实转写（行列/顶点/线段/面/颜色/方向等）",
            "options_visual_facts": "每个选项的视觉事实转写（A/B/C/D 逐个转写）",
            "uncertain_visual_details": "哪些视觉细节看不清或无法确认",
        },
        "grid_specific_requirements": {
            "coordinate_system": "网格题必须建立虚拟坐标系（行×列）",
            "black_cell_coordinates": "记录黑色块坐标集合，如 {(1,2), (2,3)}",
            "line_endpoint_coordinates": "记录线条端点坐标",
            "key_vertices": "记录关键顶点位置（如三角形顶点、L形拐点）",
            "diagonal_direction": "记录斜边方向（左上-右下 / 右上-左下）",
            "coverage_cells": "记录覆盖格数量和位置",
            "options_same_transcription": "A/B/C/D 选项也必须做同样转写",
        },
        "fallback_rule": (
            "如果视觉转写缺失或关键视觉事实不清楚，应输出 analysis_only。"
            "不得跳过视觉转写直接推理。"
        ),
    }


def get_anti_pattern_guards() -> list[dict[str, str]]:
    """Return anti-pattern guards that prevent common reasoning failures.

    Each guard identifies a forbidden pattern and its required alternative.
    """
    return [
        {
            "id": "no_first_glance",
            "forbidden": "不得只凭第一感觉或'看起来像'作答",
            "required": "必须逐条列出视觉证据，再推导候选规律",
        },
        {
            "id": "no_single_candidate",
            "forbidden": "不得只凭一个候选规律作答",
            "required": "除非 A/B/C/D 逐项验证后唯一选项满足，否则 analysis_only",
        },
        {
            "id": "grouping_needs_dimensions",
            "forbidden": "分组分类不得只列一个维度",
            "required": "至少列出 3 个候选分类维度，每个维度给出 ①-⑥ 特征表",
        },
        {
            "id": "spatial_needs逐格验证",
            "forbidden": "空间类不得跳过逐格/逐面/逐块验证",
            "required": "必须输出坐标/面/块的核验过程",
        },
        {
            "id": "bw_needs_component_split",
            "forbidden": "复杂黑白图不得跳过固定部件和移动部件拆分",
            "required": "必须分别标注固定部件、移动部件、黑色区域、白色缺口",
        },
        {
            "id": "grid_needs_position转写",
            "forbidden": "网格题不得跳过行列/顶点/覆盖格转写",
            "required": "必须记录每个已知图的黑色图形覆盖行列和关键顶点位置",
        },
        {
            "id": "unified_rule_required",
            "forbidden": "如果候选规律不能统一解释所有题干图形，必须 analysis_only",
            "required": "候选规律必须通过所有已知图的验证",
        },
        {
            "id": "unique_option_required",
            "forbidden": "如果两个及以上选项符合，必须 analysis_only",
            "required": "只有唯一选项满足规律时才能输出答案",
        },
    ]


def get_black_white_operation_rules() -> dict[str, Any]:
    """Return the black-white overlay operation rules.

    Each rule defines a specific overlay operation that can be applied to
    two figures at the same position to produce a third figure.
    """
    return {
        "applicability": "黑白叠加类图推题（九宫格、两组图、一组图中出现同位置黑白叠加）",
        "mandatory_process": [
            "1. 叠加类题必须选取同一行或同一列的前两个图形",
            "2. 建立候选运算规则表",
            "3. 逐格代入候选运算规则，验证是否能推出第三个图形",
            "4. 只有能完整推出第三个图形的规则才能采纳",
            "5. 不允许只说'像叠加'就作答",
        ],
        "operation_types": {
            "direct_overlay": {
                "name": "直接叠加",
                "rule": "黑+黑=黑，黑+白=黑，白+黑=黑，白+白=白",
                "description": "两个图形直接叠在一起，有黑则黑",
            },
            "xor_remove_same_keep_different": {
                "name": "去同存异（异或）",
                "rule": "黑+黑=白，黑+白=黑，白+黑=黑，白+白=白",
                "description": "相同颜色抵消，不同颜色保留",
            },
            "keep_same_remove_different": {
                "name": "去异存同",
                "rule": "黑+黑=黑，黑+白=白，白+黑=白，白+白=白",
                "description": "相同颜色保留，不同颜色消除",
            },
            "black_intersection": {
                "name": "黑色交集",
                "rule": "黑+黑=黑，黑+白=白，白+黑=白，白+白=白",
                "description": "只有两个都是黑色时才保留黑色",
            },
            "white_intersection": {
                "name": "白色交集",
                "rule": "黑+黑=黑，黑+白=黑，白+黑=黑，白+白=白",
                "description": "只有两个都是白色时才保留白色",
            },
            "color_inversion": {
                "name": "颜色反转",
                "rule": "对叠加结果取反：黑→白，白→黑",
                "description": "先叠加再整体反转颜色",
            },
            "line_overlay": {
                "name": "线条叠加",
                "rule": "线条覆盖：第一个图形的线条覆盖第二个图形的同位置线条",
                "description": "适用于线条图，上层线条优先显示",
            },
            "line_xor": {
                "name": "线条异或",
                "rule": "线条抵消：同位置线条抵消，无线条处产生线条",
                "description": "适用于线条图，相同线条抵消",
            },
        },
        "constraint": (
            "必须逐格代入验证，不能凭感觉判断运算类型。"
            "如果多个运算规则都能解释已知图，必须用问号图的选项做区分验证。"
        ),
    }


def get_falsification_protocol() -> dict[str, Any]:
    """Return the falsification protocol for graphic reasoning.

    The falsification protocol requires the model to actively try to disprove
    its own candidate rule before committing to an answer.
    """
    return {
        "mandatory": True,
        "timing": "在输出最终答案之前，必须完成证伪检查",
        "steps": [
            {
                "id": "unified_check",
                "requirement": "最终答案前必须检查当前规律能否解释所有已知图",
                "detail": "逐一验证每个已知图是否符合候选规律，不能跳过任何一个",
            },
            {
                "id": "option_elimination",
                "requirement": "必须 A/B/C/D 逐项排除",
                "detail": "对每个选项，说明符合或不符合的具体依据，不能只说'不符合'",
            },
            {
                "id": "competing_rule",
                "requirement": "必须尝试至少一个竞争规律",
                "detail": "提出一个可能的替代规律，检查它是否能解释已知图",
            },
            {
                "id": "conflict_check",
                "requirement": "如果竞争规律也能推出不同答案，必须说明冲突",
                "detail": "比较两个规律的预测差异，说明为什么选择当前规律",
            },
            {
                "id": "uniqueness_check",
                "requirement": "如果两个及以上选项都能解释，输出 analysis_only",
                "detail": "只有唯一选项满足规律时才能输出答案",
            },
        ],
        "forbidden": "不允许找到一个看似合理的规律就停止",
        "output_fields": [
            "current_rule_explains_all",
            "options_eliminated",
            "competing_rule_tried",
            "competing_rule_prediction",
            "conflict_explanation",
        ],
    }


def get_spatial_verification_protocol() -> dict[str, Any]:
    """Return the spatial verification protocol for three_views, cube_net,
    and solid_assembly questions."""
    return {
        "mandatory": True,
        "timing": "空间类题型必须在推理过程中输出坐标/面/块的核验过程",
        "three_views": {
            "required_steps": [
                "建立坐标/格子表",
                "转写俯视图每个格子是否有方块、颜色",
                "转写左视图各列/各行最大高度",
                "转写正视图各列最大高度",
                "建立高度矩阵",
                "标注颜色分布",
                "检查遮挡关系",
                "A/B/C/D 逐项验证",
            ],
            "required_output": [
                "坐标系描述（行×列）",
                "俯视图格子转写表",
                "左视图最大高度表",
                "正视图最大高度表",
                "高度矩阵",
                "颜色分布",
                "遮挡关系说明",
                "选项逐项验证过程",
            ],
        },
        "cube_net": {
            "required_steps": [
                "标记六个面",
                "判断相邻面",
                "判断相对面",
                "判断公共边",
                "判断公共点",
                "判断面内图案方向",
                "验证折叠后可见面",
                "A/B/C/D 逐项验证",
            ],
            "required_output": [
                "六个面的标记和图案描述",
                "相邻面关系表",
                "相对面关系表",
                "公共边位置",
                "公共点位置",
                "图案方向说明",
                "折叠后可见面组合",
                "选项逐项验证过程",
            ],
        },
        "solid_assembly": {
            "required_steps": [
                "数目标方块总数",
                "数颜色方块数",
                "数每个选项方块数和颜色数",
                "判断层数",
                "判断凹凸互补",
                "判断长短高低",
                "检查重叠",
                "检查多块/少块/颜色错位",
                "数量矛盾时回到视觉转写重新核对",
            ],
            "required_output": [
                "目标方块总数",
                "目标颜色数",
                "每个选项方块数",
                "每个选项颜色数",
                "层数分析",
                "凹凸互补分析",
                "长短高低分析",
                "重叠检查结果",
                "数量矛盾处理",
            ],
            "constraint": (
                "数量矛盾时必须回到视觉转写重新核对，不得硬解释。"
                "方块数或颜色数不匹配时，必须排除该选项。"
            ),
        },
    }


def get_uncertainty_reporting_protocol() -> dict[str, Any]:
    """Return the uncertainty reporting protocol.

    The uncertainty protocol requires the model to explicitly report
    its confidence level, risk points, and reasoning gaps before
    outputting a final answer.
    """
    return {
        "mandatory": True,
        "timing": "在输出最终答案或 analysis_only 之前，必须完成不确定性报告",
        "required_fields": [
            "confidence_level",
            "risk_points",
            "possible_competing_rule",
            "why_other_options_rejected",
        ],
        "field_descriptions": {
            "confidence_level": (
                "置信度等级：high / medium / low。"
                "high = 所有已知图验证通过，唯一选项满足，无竞争规律。"
                "medium = 所有已知图验证通过，但存在无法确认的视觉细节或弱竞争规律。"
                "low = 存在无法统一解释的已知图，或视觉转写不确定，或两个以上选项都可能满足。"
            ),
            "risk_points": (
                "风险点列表：列出所有可能导致答案错误的不确定因素。"
                "例如：'第3个图的黑色区域边界不清晰'、'无法确认是否有隐藏线条'。"
                "如果风险点涉及关键视觉事实，应输出 analysis_only。"
            ),
            "possible_competing_rule": (
                "可能的竞争规律：如果存在其他规律也能部分解释已知图，列出该规律及其解释范围。"
                "如果没有明显竞争规律，写'无'。"
            ),
            "why_other_options_rejected": (
                "排除其他选项的理由：对每个被排除的选项，给出具体排除依据。"
                "不能只说'不符合'，必须说明哪个视觉事实或规律导致排除。"
            ),
        },
        "analysis_only_triggers": [
            "confidence_level 为 low",
            "risk_points 涉及关键视觉事实",
            "possible_competing_rule 能推出不同答案",
            "无法对所有选项给出明确排除理由",
        ],
    }


def render_graphic_reasoning_prompt_template() -> str:
    """Render a prompt template for multi-modal LLM graphic reasoning.

    Updated in v0.2.1 to enforce falsification, competing rules,
    spatial verification, and uncertainty reporting.
    """
    return (
        "你是图形推理多模态观察助手。\n"
        "\n"
        "【MCP 路由结果】\n"
        "说明 MCP 路由给出的 module_guess、confidence 和 recommended_tool。\n"
        "如果存在 module_hint，说明 module_hint 和 module_hint_applied。\n"
        "\n"
        "【是否有图检查】\n"
        "确认 image_present 状态。如果无图且无 visual_description，应直接 analysis_only。\n"
        "\n"
        "【视觉转写】（必须出现）\n"
        "在推理之前，先完成视觉转写：\n"
        "- proposition_form：命题形式\n"
        "- figure_count：题干图形数量\n"
        "- option_count：选项数量\n"
        "- given_figures_visual_facts：每个已知图的视觉事实\n"
        "  - 网格题：建立虚拟坐标系，记录黑色块坐标集合、线条端点坐标、关键顶点、斜边方向、覆盖格\n"
        "  - 线条题：记录线段数、端点数、交点数、封闭区域数\n"
        "  - 空间题：记录坐标/面/块信息\n"
        "- options_visual_facts：A/B/C/D 选项也必须做同样转写\n"
        "- uncertain_visual_details：哪些视觉细节看不清或无法确认\n"
        "如果视觉转写缺失或关键视觉事实不清楚，应输出 analysis_only。\n"
        "\n"
        "【命题形式】\n"
        "说明是一组图、两组图、九宫格、分组分类、空间重构还是其他形式。\n"
        "\n"
        "【专项模板选择】\n"
        "根据题型特征，从以下专项模板中选择最匹配的一个：\n"
        "A. grid_black_shape — 网格内黑色三角形、黑白块、网格移动题\n"
        "B. complex_black_white_pattern — 复杂黑白风车状、黑白块组合、局部叠加题\n"
        "C. line_symbol_pattern — 抽象线条、符号、汉字/字母/数字图推\n"
        "D. three_views — 三视图、俯视图、左视图、正视图\n"
        "E. cube_net — 六面体展开图、两个正方体展开图\n"
        "F. solid_assembly — 立体拼合、拆分组合、除哪项外\n"
        "G. grouping_classification — 六图分两类\n"
        "说明选择理由。如果不符合任何专项模板，使用通用流程。\n"
        "\n"
        "【组成判断】\n"
        "说明图形组成是相同、相似、不同，还是特殊图形。\n"
        "\n"
        "【候选规律 1】\n"
        "提出第一个候选规律，说明为什么成立。\n"
        "候选规律必须能统一解释所有题干图形。\n"
        "叠加类必须展示运算规则代入过程。\n"
        "\n"
        "【候选规律 2 / 竞争规律】\n"
        "提出至少一个竞争规律，说明它是否也能解释已知图。\n"
        "如果竞争规律能推出不同答案，必须说明冲突。\n"
        "如果没有明显竞争规律，写'无明显竞争规律'。\n"
        "不允许只凭一个候选规律直接给答案。\n"
        "\n"
        "【证伪检查】（必须出现）\n"
        "- 当前规律是否能解释所有已知图？\n"
        "- A/B/C/D 逐项排除依据\n"
        "- 竞争规律是否尝试过？结果如何？\n"
        "- 如果两个及以上选项都能解释，输出 analysis_only\n"
        "\n"
        "【选项逐项验证】（必须出现）\n"
        "逐一验证 A/B/C/D 是否符合候选规律：\n"
        "- A：是否符合，具体依据\n"
        "- B：是否符合，具体依据\n"
        "- C：是否符合，具体依据\n"
        "- D：是否符合，具体依据\n"
        "空间类必须输出坐标/面/块的核验过程。\n"
        "分组分类必须输出候选维度表（至少 3 个维度）。\n"
        "叠加类必须展示运算规则代入。\n"
        "\n"
        "【唯一性判断】\n"
        "如果唯一，输出答案；如果不唯一，输出 analysis_only。\n"
        "只有唯一选项满足规律时才能输出答案。\n"
        "不唯一时输出 analysis_only，不得强行猜答案。\n"
        "\n"
        "【风险点与置信度】\n"
        "- confidence_level：high / medium / low\n"
        "- risk_points：列出所有不确定因素\n"
        "- possible_competing_rule：是否存在竞争规律\n"
        "- why_other_options_rejected：排除其他选项的具体理由\n"
        "如果风险点涉及关键视觉事实，应输出 analysis_only。\n"
        "不得默认选择第一个选项。\n"
        "不得只说'看起来像'，必须指出视觉依据。\n"
        "\n"
        "【最终答案或 analysis_only】\n"
        "根据以上分析，输出最终答案或 analysis_only。\n"
    )


# ---------------------------------------------------------------------------
# Specialized templates (v0.2)
# ---------------------------------------------------------------------------


def _template_grid_black_shape() -> dict[str, Any]:
    """Template A: grid black shape / black-white block / grid movement."""
    return {
        "id": "grid_black_shape",
        "name": "网格黑图专项模板",
        "usage": "网格内黑色三角形、黑白块、网格移动题",
        "mandatory_recording": [
            "每个已知图的黑色图形覆盖行列",
            "关键顶点位置（如三角形顶点所在格）",
            "斜边方向（左上-右下 / 右上-左下）",
            "面积/覆盖格数量",
            "是否平移、旋转、翻转、移动路径",
            "选项 A/B/C/D 也要做同样转写",
        ],
        "verification_steps": [
            "1. 转写每个已知图的黑块覆盖格坐标（行,列）",
            "2. 记录每个黑块的形状（三角形方向、正方形、L形等）",
            "3. 检查行方向移动规律（左移/右移/固定列）",
            "4. 检查列方向移动规律（上移/下移/固定行）",
            "5. 检查旋转规律（顺时针/逆时针/角度）",
            "6. 检查翻转规律（左右/上下/对角）",
            "7. 逐选项验证：A/B/C/D 的覆盖格是否符合推导出的规律",
        ],
        "constraint": (
            "不能只凭'朝向像旋转'直接给答案。"
            "必须记录行列坐标和覆盖格数量，用数据验证规律。"
        ),
    }


def _template_complex_black_white_pattern() -> dict[str, Any]:
    """Template B: complex black-white windmill / block combination / overlay."""
    return {
        "id": "complex_black_white_pattern",
        "name": "复杂黑白图案专项模板",
        "usage": "复杂黑白风车状、黑白块组合、局部叠加题",
        "mandatory_decomposition": [
            "固定部件 — 不随图形序列变化的部分",
            "移动部件 — 随图形序列变化的部分",
            "黑色区域 — 黑色填充的部分",
            "白色缺口 — 白色留空的部分",
            "整体旋转 — 整个图形是否旋转",
            "局部翻转 — 某个部件是否翻转",
            "黑白运算 — 同位置黑白叠加规则",
        ],
        "verification_steps": [
            "1. 将每个已知图拆分为固定部件和移动部件",
            "2. 标注每个部件的颜色（黑/白/灰）",
            "3. 检查固定部件是否真的不变（位置、大小、方向）",
            "4. 检查移动部件的变化规律（平移/旋转/翻转/替换）",
            "5. 检查黑色区域的变化规律（扩大/缩小/移动/翻转）",
            "6. 检查白色缺口的变化规律",
            "7. 逐选项验证：A/B/C/D 的部件拆分是否符合规律",
        ],
        "constraint": (
            "不能只说'整体旋转'，必须指出哪个局部在变。"
            "必须分别标注固定部件和移动部件。"
        ),
    }


def _template_line_symbol_pattern() -> dict[str, Any]:
    """Template C: abstract lines, symbols, Chinese/digit/letter figures."""
    return {
        "id": "line_symbol_pattern",
        "name": "线条符号专项模板",
        "usage": "抽象线条、符号、汉字/字母/数字图推",
        "mandatory_checks": [
            "线段数",
            "端点数",
            "交点数",
            "封闭区域数",
            "平行线",
            "垂直线",
            "横/竖/斜方向",
            "开闭性",
            "曲直性",
        ],
        "verification_steps": [
            "1. 数每个已知图的线段数（直线段和曲线段分别计数）",
            "2. 数端点数（线段的端点，不含交点）",
            "3. 数交点数（线段之间的交叉点）",
            "4. 数封闭区域数（完全围合的区域）",
            "5. 检查平行线组数",
            "6. 检查垂直线组数",
            "7. 检查线段方向分布（横线/竖线/斜线各多少）",
            "8. 检查开闭性（开放/封闭/半开半闭）",
            "9. 检查曲直性（全曲线/全直线/曲直混合）",
            "10. 逐选项验证：A/B/C/D 各项指标是否符合规律",
        ],
        "constraint": (
            "不能只用'开放/封闭'一个指标定答案。"
            "必须至少检查线段数、端点数、交点数、封闭区域数中的两个以上指标。"
        ),
    }


def _template_three_views() -> dict[str, Any]:
    """Template D: three-view drawings (俯视图/左视图/正视图)."""
    return {
        "id": "three_views",
        "name": "三视图专项模板",
        "usage": "三视图、俯视图、左视图、正视图",
        "mandatory_procedure": [
            "建立坐标/格子表",
            "转写俯视图每个格子是否有方块、颜色",
            "转写左视图各列/各行最大高度",
            "逐项验证 A/B/C/D 的高度、颜色、遮挡是否兼容",
            "任何高度/颜色矛盾必须排除",
        ],
        "verification_steps": [
            "1. 建立俯视图坐标系（行×列的格子表）",
            "2. 转写俯视图：每个格子是否有方块，颜色是什么",
            "3. 从正视图获取：每列的最大高度",
            "4. 从左视图获取：每行的最大高度",
            "5. 建立高度矩阵：每个格子的高度 = min(正视图列高, 左视图行高) 或实际堆叠",
            "6. 逐选项验证：A/B/C/D 的俯视图是否与题干一致",
            "7. 逐选项验证：A/B/C/D 的高度是否与正视图/左视图一致",
            "8. 逐选项验证：A/B/C/D 的颜色/遮挡是否与题干一致",
            "9. 任何矛盾必须排除该选项",
        ],
        "constraint": (
            "不能凭直观看'哪个像'直接选。"
            "必须建立坐标/格子表，逐格验证高度和颜色。"
        ),
    }


def _template_cube_net() -> dict[str, Any]:
    """Template E: cube net (六面体展开图)."""
    return {
        "id": "cube_net",
        "name": "展开图专项模板",
        "usage": "六面体展开图、两个正方体展开图",
        "mandatory_procedure": [
            "标记六个面",
            "判断相邻面",
            "判断相对面",
            "判断公共边",
            "判断公共点",
            "判断面内图案方向",
            "验证折叠后哪些面能同时可见",
        ],
        "verification_steps": [
            "1. 标记展开图的六个面（编号 ①-⑥ 或用图案描述）",
            "2. 判断哪些面是相邻面（有公共边的面）",
            "3. 判断哪些面是相对面（不可能同时看到的面）",
            "4. 标注公共边：相邻面的公共边位置",
            "5. 标注公共点：三个或更多面的公共顶点",
            "6. 判断面内图案方向（折叠后图案朝向哪个方向）",
            "7. 用相对面排除法：选项中相对面关系是否与展开图一致",
            "8. 用公共边排除法：选项中公共边位置是否与展开图一致",
            "9. 用时针法验证：绕公共点的面序是否一致",
            "10. 逐选项验证：A/B/C/D 是否能由展开图折叠而成",
        ],
        "constraint": (
            "不能只看'有没有黑块/斜线/三角形'。"
            "必须验证相邻面、相对面、公共边、公共点和图案方向。"
        ),
    }


def _template_solid_assembly() -> dict[str, Any]:
    """Template F: solid assembly / disassembly / 'which one doesn't fit'."""
    return {
        "id": "solid_assembly",
        "name": "立体拼合专项模板",
        "usage": "立体拼合、拆分组合、除哪项外",
        "mandatory_procedure": [
            "先数目标方块总数",
            "数颜色方块数",
            "数每个选项方块数和颜色数",
            "判断层数、凹凸、长短、高低",
            "逐组合验证是否多块、少块、重叠、颜色错位",
        ],
        "verification_steps": [
            "1. 数目标立体的方块总数",
            "2. 数目标立体中各颜色方块数",
            "3. 数每个选项的方块总数",
            "4. 数每个选项中各颜色方块数",
            "5. 检查方块总数是否匹配（目标 = 选项之和 或 目标 = 选项之差）",
            "6. 检查颜色数是否匹配",
            "7. 检查层数是否一致",
            "8. 检查凹凸是否互补",
            "9. 检查长短、高低是否一致",
            "10. 逐组合验证：拼合后是否多块、少块、重叠、颜色错位",
        ],
        "constraint": (
            "如果数量矛盾，必须回到视觉转写重新核对，不得硬解释。"
            "方块数或颜色数不匹配时，必须排除该选项。"
        ),
    }


def _template_grouping_classification() -> dict[str, Any]:
    """Template G: grouping classification (六图分两类)."""
    return {
        "id": "grouping_classification",
        "name": "分组分类专项模板",
        "usage": "六图分两类",
        "mandatory_procedure": [
            "至少列出 3 个候选分类维度",
            "每个维度都要给 ①②③④⑤⑥ 的特征表",
            "再用 A/B/C/D 选项反推验证",
            "只有能同时解释两组内部共同点和组间差异的分法才能输出",
        ],
        "candidate_dimensions": [
            "是否含三角形",
            "封闭区域数",
            "黑块数量",
            "黑块位置",
            "黑块相邻/距离关系",
            "对称性",
            "曲直性",
            "开闭性",
            "图形间关系",
            "面积/边数/交点数",
            "功能元素位置",
        ],
        "verification_steps": [
            "1. 列出至少 3 个候选分类维度",
            "2. 对每个维度，标注 ①-⑥ 各图的特征值",
            "3. 检查每个维度是否能将六图分为两组（每组内部特征相同）",
            "4. 检查候选维度是否能同时解释两组内部共同点和组间差异",
            "5. 用 A/B/C/D 选项反推：选项给出的分组是否与推导出的维度一致",
            "6. 只有能同时解释两组内部共同点和组间差异的分法才能输出",
            "7. 如果多个维度都能解释，需要进一步区分或 analysis_only",
        ],
        "constraint": (
            "不能看到一个看似合理的特征就定答案。"
            "必须至少列出 3 个候选维度，逐维度验证后再选择。"
        ),
    }


# ---------------------------------------------------------------------------
# Internal builders
# ---------------------------------------------------------------------------


def _build_positioning() -> dict[str, str]:
    """Build the positioning description."""
    return {
        "is_solver": False,
        "is_image_recognizer": False,
        "outputs_answer": False,
        "description": (
            "本模块不是 solver，不识别图像，不直接输出答案。"
            "本模块用于约束多模态大模型按图推方法论观察、说明视觉证据、"
            "验证选项，并在无法唯一时 analysis_only。"
        ),
    }


def _build_composition_router() -> dict[str, dict[str, Any]]:
    """Build the composition-based routing rules."""
    return {
        "组成相同": {
            "priority": "位置规律",
            "patterns": ["平移", "旋转", "翻转", "移动路径", "方向变化", "内外位置变化"],
            "constraint": "组成相同时，不要一上来数点线面；优先检查位置变化。",
        },
        "组成相似": {
            "priority": "样式规律",
            "patterns": ["遍历", "加减同异", "去同存异", "去异存同", "黑白运算", "局部替换"],
            "constraint": "组成相似时，不要一上来数数量；优先检查样式变化。",
        },
        "组成不同": {
            "priority": "属性和数量",
            "patterns": ["点", "线", "面", "角", "素", "一笔画", "封闭开放", "对称", "曲直"],
            "constraint": "组成不同时，再系统检查属性和数量。",
        },
        "特殊图形": {
            "priority": "专项检查",
            "patterns": [
                "黑白块", "汉字", "数字", "字母", "功能元素",
                "六面体展开图", "截面图", "三视图", "立体拼合",
            ],
            "constraint": "特殊图形优先触发专项检查。",
        },
    }


def _build_uncertainty_policy() -> dict[str, str]:
    """Build the uncertainty policy."""
    return {
        "rule_not_unified": "规律无法统一解释题干图形 → analysis_only",
        "multiple_options_match": "两个及以上选项都符合候选规律 → analysis_only",
        "unreliable_detail": "必须依赖无法确认的小图细节 → analysis_only",
        "unreliable_recognition": "图形识别结果不可靠 → analysis_only",
        "fold_ambiguous": "空间折叠无法唯一排除 → analysis_only",
        "bw_table_uncertain": "黑白运算表无法唯一确定 → analysis_only",
    }


def _build_must_not_do() -> list[str]:
    """Build the must-not-do constraints."""
    return [
        "不得默认选择第一个选项",
        "不得在无法唯一排除时强行给答案",
        "不得用题号、case_id 或标准答案写规则",
        "不得跳过视觉证据说明",
        "不得只说'看起来像'，必须指出视觉依据",
        "不得把图推 scaffold 当成本地图像 solver",
        "不得引入 OCR、OpenCV、PIL 或机器学习依赖",
    ]


# ---------------------------------------------------------------------------
# Visual checklists
# ---------------------------------------------------------------------------


def _checklist_proposition_form() -> dict[str, Any]:
    """Proposition form checklist."""
    return {
        "forms": ["一组图", "两组图", "九宫格", "分组分类", "类比式图推", "空间重构"],
        "guidance": {
            "一组图": "按从左到右寻找递推、周期、数量或位置变化。",
            "两组图": "先看第一组内部规律，再迁移到第二组。",
            "九宫格": "优先横向看，再纵向看，必要时看 S 型、米字型或中心对称关系。",
            "分组分类": "先找每组内部共同点，再找两组之间差异点。",
            "空间重构": "优先看相对面、公共边、公共点和选项可排除点。",
        },
    }


def _checklist_attribute_rules() -> dict[str, Any]:
    """Attribute rules checklist."""
    return {
        "对称性": {
            "types": ["轴对称", "中心对称", "轴对称 + 中心对称"],
            "checks": ["对称轴数量", "对称轴方向", "对称轴与图形中线条/点/面的关系"],
            "hint_shapes": ["Z", "S", "风车", "太极", "平行四边形", "正三角形", "田字格", "五角星", "正六边形"],
        },
        "开闭性": {
            "types": ["开放图形", "封闭图形", "半开半闭图形"],
            "checks": ["封闭区域是否存在缺口", "图形是否完全围成封闭空间"],
        },
        "曲直性": {
            "types": ["全曲线", "全直线", "曲线 + 直线"],
            "checks": ["内部曲直", "外部曲直", "曲直交替", "曲线数量", "直线数量"],
        },
    }


def _checklist_quantity_rules() -> dict[str, Any]:
    """Quantity rules checklist."""
    return {
        "点": {
            "types": ["交点", "端点", "切点", "出头点", "曲直交点", "内部交点", "外框交点", "公共点", "功能点"],
            "notes": [
                "出头点不一定都算交点，需要看题组是否统一。",
                "端点是否计数要结合题组规律。",
                "点数量题常与一笔画、线段、功能元素结合。",
            ],
        },
        "线": {
            "types": [
                "直线数量", "曲线数量", "线段数量", "横线", "竖线", "斜线",
                "平行线", "平行线组", "垂直线", "公共边", "公共线",
                "连接线", "延伸线", "组成封闭面的线", "图形间相交于线",
            ],
        },
        "面": {
            "types": [
                "封闭面总数", "最大面形状", "最大面面积", "最大面属性",
                "最大面与外框是否相似", "部分面数量", "三角形面数量",
                "四边形面数量", "特殊形状面数量",
            ],
        },
        "角": {
            "types": ["角总数", "直角数", "锐角数", "钝角数", "最大角", "最小角", "角方向"],
            "hint": "电话卡、垂线、三角形、折线图形常提示直角数。",
        },
        "素": {
            "types": [
                "元素种类", "元素个数", "相同元素数量", "不同元素数量",
                "元素间数量换算", "内部元素", "外部元素", "元素位置",
                "元素方向", "元素大小",
            ],
        },
        "一笔画": {"checks": ["奇点数量", "是否连通", "是否一笔画"]},
        "部分数": {"checks": ["连通区域数量"]},
    }


def _checklist_position_rules() -> dict[str, Any]:
    """Position rules checklist."""
    return {
        "平移": {
            "checks": ["移动主体", "移动方向", "移动路径", "移动步数", "是否循环", "是否反弹"],
            "directions": ["上下", "左右", "斜向", "顺时针", "逆时针", "内外移动", "绕圈移动"],
            "step_patterns": ["固定步数", "递增步数", "递减步数", "交替步数"],
            "paths": ["直线路径", "环形路径", "宫格路径", "外圈路径", "内圈路径", "蛇形路径", "反弹路径"],
        },
        "旋转": {
            "checks": ["旋转中心", "旋转方向", "旋转角度", "每步旋转角度是否固定"],
            "common_angles": ["45°", "90°", "135°", "180°"],
        },
        "翻转": {
            "checks": ["左右翻转", "上下翻转", "沿斜轴翻转", "翻转后是否再旋转", "局部翻转", "整体翻转"],
        },
    }


def _checklist_style_rules() -> dict[str, Any]:
    """Style rules checklist."""
    return {
        "遍历": {
            "types": ["颜色遍历", "形状遍历", "数量遍历", "位置遍历", "方向遍历", "元素种类遍历"],
        },
        "加减同异": {
            "types": ["相加", "相减", "去同存异", "去异存同", "叠加后变色", "叠加后抵消", "同位置运算"],
            "constraints": [
                "必须逐位置比较。",
                "必须先从已知图推出统一规则。",
                "不能凭单个位置猜运算结果。",
                "若运算表不能统一解释已知图，应 analysis_only。",
            ],
        },
        "黑白运算": {
            "process": [
                "1. 判断是否为同位置黑白叠加。",
                "2. 建立黑+黑、黑+白、白+黑、白+白的运算表。",
                "3. 用至少一组已知图验证运算表。",
                "4. 运算表一致后再代入问号图。",
                "5. 若题干无法推出唯一运算表，不强行选择。",
            ],
            "constraint": "不同题的黑白运算表可能不同，不能预设固定运算规则。",
        },
    }


def _checklist_inter_figure_relations() -> dict[str, Any]:
    """Inter-figure relations checklist."""
    return {
        "relations": [
            "相离", "相交于点", "相交于线", "相交于面",
            "包含", "内外关系", "公共边", "公共点",
            "公共区域", "重叠面积", "连接方式",
        ],
    }


def _checklist_functional_elements() -> dict[str, Any]:
    """Functional elements checklist."""
    return {
        "标记点": ["交点", "端点", "切点", "中心点", "外框点", "内部点", "曲直交点"],
        "标记线": ["直线", "曲线", "最长线", "最短线", "平行线", "垂直线", "公共边", "连接线"],
        "标记面": ["最大面", "最小面", "相交面", "阴影面", "直线面", "曲线面", "内部面", "外部面"],
        "标记角": ["最大角", "最小角", "直角", "锐角", "钝角", "内角", "外角"],
        "相对位置": ["上", "下", "左", "右", "内", "外", "中心", "边上", "角上", "交点上", "端点上"],
        "特殊关系": [
            "黑点连线与原图线条是否平行、垂直或重合。",
            "标记点是否落在最大面、最小面或特殊面内。",
            "箭头是否指向特殊点、特殊线、特殊面或特殊角。",
            "阴影是否标记最大区域、最小区域或相交区域。",
        ],
    }


def _checklist_black_white_blocks() -> dict[str, Any]:
    """Black-white blocks checklist."""
    return {
        "checks": [
            "整体对称", "黑白面积", "黑块数量", "白块数量",
            "黑块位置", "白块位置", "黑块连通", "白块连通",
            "黑块相邻关系", "黑白相邻关系", "同位置运算",
            "局部平移", "局部旋转",
        ],
        "recommended_order": [
            "1. 先看整体对称性。",
            "2. 再看黑白面积比例。",
            "3. 再看黑块数量是否递增、递减或恒定。",
            "4. 再看黑块是否连通，连通块数量是否变化。",
            "5. 再看黑块是否相邻，边相邻还是角相邻。",
            "6. 再看同位置黑白运算。",
            "7. 最后看局部位置移动。",
        ],
        "constraints": [
            "黑白块题不能只看黑块数量；若数量无规律，应继续检查连通、相邻、对称、运算和位置。",
            "不同题的黑白运算表可能不同，不能预设固定运算规则。",
            "必须从已知图推出统一运算表。",
        ],
    }


def _checklist_chinese_characters() -> dict[str, Any]:
    """Chinese character checklist."""
    return {
        "checks": [
            "结构", "上下结构", "左右结构", "包围结构",
            "封闭面", "曲直性", "开闭性", "笔画数",
            "部分数", "交点数", "元素数量", "部首位置",
            "相同部件", "汉字读音", "声母韵母", "偏旁遍历",
        ],
        "emphasis": "汉字图推优先当作图形看，不优先当作语文题。",
    }


def _checklist_digits() -> dict[str, Any]:
    """Digit visual classification checklist."""
    return {
        "checks": [
            "对称性", "曲直性", "开闭性", "封闭面数量",
            "数字大小", "奇偶性", "递增递减", "数字运算", "排列顺序",
        ],
        "classifications": {
            "常见轴对称数字": ["0", "3", "6", "8", "9"],
            "全曲数字": ["0", "3", "6", "8", "9"],
            "全直数字": ["1", "4", "7"],
            "曲直混合数字": ["2", "5"],
            "开放图形": ["1", "2", "3", "5", "7"],
            "全封闭图形": ["0", "8"],
            "半封闭图形": ["4", "6", "9"],
            "0个面": ["1", "2", "3", "5", "7"],
            "1个面": ["0", "4", "6", "9"],
            "2个面": ["8"],
        },
        "note": "数字题可以同时考图形属性和数字本身运算，必须先判断题目是在考'图形化数字'还是'数字运算'。",
    }


def _checklist_letters() -> dict[str, Any]:
    """Letter visual classification checklist."""
    return {
        "checks": [
            "字母表顺序", "对称性", "中心对称", "曲直性",
            "开闭性", "封闭面数量", "大小写形式", "字母本身算法",
        ],
        "classifications": {
            "轴对称字母": list("ABCDEHIKMOTUVWXY"),
            "中心对称字母": list("NSZ"),
            "全曲": list("COSU"),
            "全直": list("AEFHIKLMNTVWXYZ"),
            "曲直混合": list("BDGJPQR"),
            "开放图形": list("CEFGHIJKLMNSTUVWXYZ"),
            "全封闭图形": list("BDO"),
            "半封闭图形": list("APQR"),
            "0个面": list("CEFGHIJKLMNSTUVWXYZ"),
            "1个面": list("ADOPR"),
            "2个面": list("B"),
        },
        "notes": [
            "字母分类默认基于常见大写印刷体。",
            "若题干字体特殊，以题干视觉形态为准。",
            "若出现小写字母，不能直接套用大写表。",
        ],
    }


def _checklist_cube_net() -> dict[str, Any]:
    """Cube net (六面体展开图) checklist."""
    return {
        "net_types": ["1-4-1", "2-3-1", "2-2-2", "0-3-3"],
        "note": "六面体展开图常见 4 类 11 种结构。",
        "checks": [
            "相对面排除",
            "公共边验证",
            "公共点验证",
            "时针方向",
            "面内图案方向",
            "特殊面",
            "选项排除",
        ],
        "constraints": [
            "若仅靠相对面无法排除，应继续使用公共边、公共点、时针法，不能直接猜。",
        ],
    }


def _checklist_cross_section() -> dict[str, Any]:
    """Cross section (截面图) checklist."""
    return {
        "checks": [
            "立体类型", "切入位置", "切割方向",
            "截面边数", "截面形状", "能否截出选项形状", "是否存在不可能截面",
        ],
        "rules": [
            "六面体一般最多可截出六边形。",
            "六面体不能截出正五边形。",
            "圆柱常见截面包括圆、椭圆、矩形等。",
            "圆锥常见截面包括圆、椭圆、三角形等。",
            "圆锥通常不能截出四边形。",
        ],
        "constraint": "如果选项形状需要曲面参与，必须确认原立体是否有曲面。",
    }


def _checklist_three_views() -> dict[str, Any]:
    """Three views (三视图) checklist."""
    return {
        "views": ["主视图", "俯视图", "左视图"],
        "rules": ["长对正", "高平齐", "宽相等"],
        "checks": ["可见线", "不可见线", "遮挡关系", "曲面交接"],
        "core_rules": [
            "有线就有线，没线就没线。",
            "被遮挡部分不可见。",
            "曲面平滑交接处一般无线。",
        ],
    }


def _checklist_solid_assembly() -> dict[str, Any]:
    """Solid assembly (立体拼合) checklist."""
    return {
        "checks": [
            "块数", "体积", "占地面积", "最大块", "特殊块",
            "凹凸关系", "长短关系", "高低关系", "分层结构", "严丝合缝",
        ],
        "process": [
            "1. 先数小方块总数。",
            "2. 再找占地面积大的特殊块。",
            "3. 按层画图或按层想象。",
            "4. 检查凸凹是否互补。",
            "5. 检查长短、高低是否一致。",
            "6. 检查拼合后是否多块、少块或重叠。",
        ],
        "constraint": "若某个选项不能严丝合缝，或需要重叠/穿插才能成立，应排除。",
    }
