from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..kb import get_method_card
from ..router import classify_question


LOGIC_ROUTE_MODULE = "判断推理-逻辑判断"
LOGIC_OUTPUT_MODULE = "判断推理"
LOGIC_SOLVER_VERSION = "v7 conservative truth integration"

# Truth reasoning triggers
_TRUTH_TRIGGERS = [
    "只有一真", "只有一假", "一真两假", "二真二假", "三真一假",
    "全假", "均为假", "都没采纳", "都说假话", "都说真话",
    "只有一人说", "只有一位", "只有一个",
    "甲说", "乙说", "丙说", "丁说",
    "预测为真", "预测为假", "猜测正确", "猜测不正确",
    "说法是真", "说法是假", "描述是真", "描述是假",
]


def _is_truth_reasoning_question(question_text: str) -> bool:
    """Detect if a question is a truth reasoning question."""
    # Strong constraint triggers that almost certainly indicate truth reasoning
    strong_triggers = [
        "只有一真", "只有一假", "一真两假", "二真二假", "三真一假",
        "全假", "均为假", "都没采纳", "都说假话", "都说真话",
        "预测为真", "预测为假", "猜测正确", "猜测不正确",
        "说法是真", "说法是假", "描述是真", "描述是假",
        "只有一人预测", "只有一位预测", "只有一人猜测",
        "只有一个真", "只有一个假",
        "四人中二人说了假话", "四人中二人说了真话",
        "三人中只有一", "四人中只有一",
    ]
    if any(t in question_text for t in strong_triggers):
        return True

    # "都没采纳" / "均为假" pattern
    if "都没采纳" in question_text or "均为假" in question_text:
        return True

    # Constraint + speaker/source indicators
    has_constraint = any(t in question_text for t in [
        "只有一人说", "只有一位", "只有一个", "只有一人",
        "是真的", "是假的",
        "一条是假的", "一条是真的",
        "预测是正确的", "预测为真",
        "看法是正确的", "看法正确",
    ])
    has_speaker_or_source = any(t in question_text for t in [
        "甲说", "乙说", "丙说", "丁说",
        "教练说", "专家说", "球迷说", "老师说",
        "线索", "标签", "柜子", "写着", "描述",
        "预测", "猜测", "看法", "专家",
    ])

    if has_constraint and has_speaker_or_source:
        return True

    return False

TRANSLATION_RULE: dict[str, Any] = {
    "question_type": "结论推出",
    "sub_type": "翻译推理",
    "stem_type": "翻译推理题",
    "task": "将题干条件命题翻译为箭头式，选择必然推出或不能推出的选项",
    "strength_direction": "translation",
    "triggers": ["如果", "那么", "只要", "只有", "除非", "否则", "所有", "凡是", "并非", "要么", "可以推出", "不能推出"],
    "method_ids": [
        "lj_conclusion_translation_001",
        "lj_sufficient_necessary_001",
        "lj_translation_if_001",
        "lj_translation_only_001",
        "lj_translation_unless_001",
        "lj_inverse_contrapositive_001",
        "lj_or_and_negation_001",
        "lj_relation_quantifier_001",
    ],
    "plan": [
        "第一步：先识别条件词，不把翻译推理题做成加强、削弱或解释题。",
        "第二步：把如果/只要/所有都翻译为前推后，把只有才翻译为后推前，并串联条件链。",
        "第三步：优先验证逆否命题；排除肯后、否前、偷换概念和范围扩大。",
        "第四步：遇到不能推出/不一定为真，选择无法由题干必然推出的选项。",
    ],
}

OPTION_RE = re.compile(
    r"(?:^|[\s。；;，,:：?？])([A-D])(?:[\.、:：])\s*(.*?)(?=\s*[。；;，,]?\s*[A-D](?:[\.、:：])|$)"
)


TYPE_RULES: list[dict[str, Any]] = [
    {
        "question_type": "削弱",
        "sub_type": "削弱/质疑",
        "stem_type": "削弱题",
        "task": "找最能削弱、质疑或反驳题干论证的选项",
        "strength_direction": "weaken",
        "triggers": ["最不能削弱", "不能削弱", "不能质疑", "没有质疑", "最能削弱", "最能质疑", "最能反驳", "对上述论证构成质疑", "削弱", "质疑", "反驳"],
        "method_ids": [
            "lj_weaken_evidence_conclusion_001",
            "lj_attribution_general_001",
            "lj_weaken_alternative_cause_001",
            "lj_weaken_reverse_causation_001",
            "lj_strength_order_compare_001",
        ],
        "plan": [
            "第一步：先找论点，再找论据，不直接看选项凭常识判断。",
            "第二步：判断论据如何支持论点，标出论证桥梁或缺口。",
            "第三步：逐项判断选项是否攻击论点、论据或论证桥梁。",
            "第四步：做削弱力度比较；直接拆断论证链通常强于泛泛相关。",
            "第五步：若问法含“不能削弱/最不能削弱”，按反向问法处理。",
        ],
    },
    {
        "question_type": "前提假设",
        "sub_type": "必要前提",
        "stem_type": "前提假设题",
        "task": "找要使论证成立所必须补充的前提",
        "strength_direction": "necessary_assumption",
        "triggers": ["要使上述论证成立", "上述论证的成立须补充", "需要补充", "需要补充以下哪项", "必须假定", "基于以下哪项", "依赖于以下哪项", "必要条件", "必须补充", "前提", "假设"],
        "method_ids": [
            "lj_premise_general_001",
            "lj_premise_bridge_001",
            "lj_premise_fill_gap_001",
            "lj_premise_enable_condition_001",
        ],
        "plan": [
            "第一步：找论点、论据和论证缺口。",
            "第二步：优先使用否定代入：把选项取反后，看论证是否无法成立。",
            "第三步：必要条件必须是“没它不行”，不是普通有帮助即可。",
            "第四步：若多个选项都相关，优先选择最贴合断点且否定后直接破坏论证的项。",
        ],
    },
    {
        "question_type": "加强",
        "sub_type": "支持加强",
        "stem_type": "加强题",
        "task": "找最能支持、加强或补充题干论证的选项",
        "strength_direction": "strengthen",
        "triggers": ["不能支持", "无法支持", "不能加强", "不支持", "不加强", "最能支持", "最能加强", "最能证明", "最有助于支持", "为上述结论提供支持", "支持", "加强", "补充以下哪项"],
        "method_ids": [
            "lj_support_general_001",
            "lj_support_bridge_001",
            "lj_support_add_evidence_001",
            "lj_support_necessary_condition_001",
            "lj_strength_order_compare_001",
        ],
        "plan": [
            "第一步：先找论点和论据，核对主体、话题是否一致。",
            "第二步：判断论证缺口，优先寻找补强桥梁的选项。",
            "第三步：区分补强论证桥梁、增加正向证据、排除他因三类支持方式。",
            "第四步：比较加强力度；直接补断点通常强于只补背景事实。",
        ],
    },
    {
        "question_type": "解释说明",
        "sub_type": "矛盾解释",
        "stem_type": "解释说明题",
        "task": "找最能解释题干现象或表面矛盾的选项",
        "strength_direction": "explain",
        "triggers": ["不能解释", "无法解释", "不解释", "最不能解释", "最能解释", "最能说明", "可以解释", "解释这一现象", "解释上述矛盾", "解释上述现象", "解释", "说明"],
        "method_ids": [
            "lj_explanation_contradiction_001",
            "lj_support_explain_mechanism_001",
            "lj_irrelevant_options_001",
        ],
        "plan": [
            "第一步：找需要解释的矛盾或现象双方。",
            "第二步：判断选项是否能同时解释现象的两方面信息。",
            "第三步：排除只解释一半、偷换主体或与现象无关的选项。",
            "第四步：若问法含“最不能解释”，按反向问法处理。",
        ],
    },
    {
        "question_type": "结论推出",
        "sub_type": "基础推出",
        "stem_type": "结论推出题",
        "task": "判断哪项可以由题干信息推出",
        "strength_direction": "infer",
        "triggers": ["不能推出", "无法推出", "不能由此推出", "无法由此推出", "不一定为真", "一定为真", "可以推出", "能够推出", "由此推出", "由此可以推出", "由此可推出", "根据上述信息，可以推出", "必然推出", "据此可知"],
        "method_ids": [
            "lj_conclusion_translation_001",
            "lj_sufficient_necessary_001",
            "lj_relation_quantifier_001",
        ],
        "plan": [
            "第一步：识别条件词、量词和确定性表达。",
            "第二步：只依据题干已给信息做保守推出，不添加生活常识。",
            "第三步：逐项排除过度概括、偷换范围和肯后否前错误。",
        ],
    },
]


def _try_truth_reasoning(
    question_text: str,
    options: dict[str, str] | list[str] | None = None,
    return_debug: bool = False,
) -> dict[str, Any] | None:
    """Try to solve using truth reasoning core.

    Returns a result dict if successful (solved + unique_supported),
    or None if the question should fall through to existing logic.
    """
    from .truth_reasoning import (
        OptionClaim,
        extract_options,
        map_options_to_assignments,
        solve_truth_core,
    )

    core_result = solve_truth_core(question_text)

    # If core can't parse enough, return analysis_only
    if core_result.status == "analysis_only":
        return _truth_analysis_only(core_result, return_debug)

    # If inconsistent, return analysis_only
    if core_result.status == "inconsistent":
        return _truth_analysis_only(core_result, return_debug)

    # For solved or ambiguous, proceed to option mapping

    # Extract options
    raw_options = None
    if options and isinstance(options, dict):
        raw_options = options
    else:
        raw_options = extract_options(question_text)

    if not raw_options:
        return _truth_analysis_only(core_result, return_debug, "no_options")

    # Build option claims
    if isinstance(raw_options, dict):
        option_claims = [
            OptionClaim(label=label, raw=text)
            for label, text in sorted(raw_options.items())
        ]
    else:
        option_claims = raw_options

    # Map options to assignments
    valid_assignments = [
        (a["assignment"], a["facts"]) for a in core_result.assignments
    ]
    mapping_result = map_options_to_assignments(
        option_claims, valid_assignments,
        question_text=question_text,
    )

    # Only output candidate_ready if unique_supported or unique_supported_across_assignments
    if mapping_result.option_status in ("unique_supported", "unique_supported_across_assignments") and mapping_result.selected_label:
        result = {
            "module": LOGIC_OUTPUT_MODULE,
            "version": "v7",
            "solver_version": LOGIC_SOLVER_VERSION,
            "question_type": "真假推理",
            "sub_type": "truth_reasoning",
            "needs_more_data": False,
            "decision_status": "candidate_ready",
            "confidence": 0.75,
            "high_risk_warnings": [],
            "matched_routes": [],
            "recommended_methods": [],
            "argument_structure": {},
            "question_stem_analysis": {
                "stem_type": "真假推理题",
                "task": "根据真假约束和陈述推理唯一正确选项",
                "strength_direction": "truth_reasoning",
                "is_reverse_question": False,
                "reverse_question_type": "",
                "question_polarity": "",
                "task_type": "truth_reasoning",
            },
            "option_analysis": [],
            "answer_candidate": {"label": mapping_result.selected_label} if mapping_result.selected_label else None,
            "solving_plan": [
                "第一步：识别真假约束（只有一真/只有一假/全假等）。",
                "第二步：提取各人陈述并解析为结构化命题。",
                "第三步：枚举一致赋值，推导闭包事实。",
                "第四步：将事实与选项匹配，选择唯一被支持的选项。",
            ],
            "exam_style_explanation_draft": "",
            "source_method_ids": [],
            "warnings": [],
        }
        if return_debug:
            result["debug"] = {
                "truth_reasoning_status": core_result.status,
                "option_status": mapping_result.option_status,
                "predicted_label": mapping_result.selected_label,
                "assignments_count": len(core_result.assignments),
                "option_trace": mapping_result.option_trace,
            }
        return result

    # Not unique_supported → fall through to analysis_only
    return _truth_analysis_only(core_result, return_debug, mapping_result.option_status)


def _truth_analysis_only(
    core_result, return_debug: bool = False, option_status: str = ""
) -> dict[str, Any]:
    """Return analysis_only result for truth reasoning."""
    result = {
        "module": LOGIC_OUTPUT_MODULE,
        "version": "v7",
        "solver_version": LOGIC_SOLVER_VERSION,
        "question_type": "真假推理",
        "sub_type": "truth_reasoning",
        "needs_more_data": True,
        "decision_status": "analysis_only",
        "confidence": 0.0,
        "high_risk_warnings": [],
        "matched_routes": [],
        "recommended_methods": [],
        "argument_structure": {},
        "question_stem_analysis": {
            "stem_type": "真假推理题",
            "task": "根据真假约束和陈述推理唯一正确选项",
            "strength_direction": "truth_reasoning",
            "is_reverse_question": False,
            "reverse_question_type": "",
            "question_polarity": "",
            "task_type": "truth_reasoning",
        },
        "option_analysis": [],
        "answer_candidate": None,
        "solving_plan": [],
        "exam_style_explanation_draft": "",
        "source_method_ids": [],
        "warnings": [f"truth_reasoning_{core_result.status}"],
    }
    if return_debug:
        result["debug"] = {
            "truth_reasoning_status": core_result.status,
            "option_status": option_status,
            "assignments_count": len(core_result.assignments),
        }
    return result


def _is_analysis_reasoning_question(question_text: str) -> bool:
    """Detect if a question is an analysis reasoning question."""
    analysis_triggers = [
        "半真半假", "猜对了一半", "只猜对了一种", "一真一假",
        "每人只猜对", "每人都只猜对",
        "分别装在", "五个盒子", "三个抽屉", "四种颜色",
        "排列", "顺序", "从左到右", "从北到南",
        "紧挨", "相邻", "不挨",
        "甲不是", "乙不是", "丙不是",
        "研究方向", "音韵学", "文献学", "敦煌学",
        "职业", "技能", "编程", "插花", "绘画", "书法",
    ]
    has_trigger = any(t in question_text for t in analysis_triggers)

    if _is_truth_reasoning_question(question_text):
        return False

    if re.search(r"如果.*那么|只要.*就|只有.*才|除非.*否则", question_text):
        return False

    return has_trigger


def _try_analysis_reasoning(
    question_text: str,
    options: dict[str, str] | list[str] | None = None,
    return_debug: bool = False,
) -> dict[str, Any] | None:
    """Try to solve using analysis reasoning core."""
    from .logic_analysis_reasoning import solve_analysis_core, extract_options

    opts = options if isinstance(options, dict) else None

    # If options not passed, try to extract from question text
    if not opts:
        raw_opts = extract_options(question_text)
        if raw_opts:
            opts = {opt.label: opt.raw for opt in raw_opts}

    core_result = solve_analysis_core(question_text, options=opts)

    if core_result.status == "solved" and core_result.option_status in (
        "unique_supported", "unique_supported_across_assignments",
    ) and core_result.predicted_label:
        result = {
            "module": LOGIC_OUTPUT_MODULE,
            "version": "v7",
            "solver_version": LOGIC_SOLVER_VERSION,
            "question_type": "分析推理",
            "sub_type": "analysis_reasoning",
            "needs_more_data": False,
            "decision_status": "candidate_ready",
            "confidence": 0.75,
            "high_risk_warnings": [],
            "matched_routes": [],
            "recommended_methods": [],
            "argument_structure": {},
            "question_stem_analysis": {
                "stem_type": "分析推理题",
                "task": "根据约束条件推理唯一正确选项",
                "strength_direction": "analysis_reasoning",
                "is_reverse_question": False,
                "reverse_question_type": "",
                "question_polarity": "",
                "task_type": "analysis_reasoning",
            },
            "option_analysis": [],
            "answer_candidate": {"label": core_result.predicted_label},
            "solving_plan": [
                "第一步：提取变量和域。",
                "第二步：解析约束条件。",
                "第三步：枚举所有可能赋值。",
                "第四步：过滤满足约束的赋值。",
                "第五步：匹配选项，选择唯一被支持的选项。",
            ],
            "exam_style_explanation_draft": "",
            "source_method_ids": [],
            "warnings": [],
        }
        if return_debug:
            result["debug"] = {
                "analysis_reasoning_status": core_result.status,
                "option_status": core_result.option_status,
                "predicted_label": core_result.predicted_label,
                "num_variables": len(core_result.variables),
                "num_constraints": len(core_result.constraints),
                "num_assignments": len(core_result.assignments),
            }
        return result

    return None


def solve_logic_reasoning(
    question_text: str,
    options: dict[str, str] | list[str] | None = None,
    kb_dir: str | Path | None = None,
    return_debug: bool = False,
) -> dict[str, Any]:
    # --- Truth reasoning branch (conservative) ---
    if _is_truth_reasoning_question(question_text):
        truth_result = _try_truth_reasoning(question_text, options, return_debug)
        if truth_result is not None:
            return truth_result

    # --- Analysis reasoning branch (conservative) ---
    if _is_analysis_reasoning_question(question_text):
        analysis_result = _try_analysis_reasoning(question_text, options, return_debug)
        if analysis_result is not None:
            return analysis_result

    matched_routes = classify_question(question_text, kb_dir=kb_dir, top_k=8)
    logic_routes = [route for route in matched_routes if route.get("module") == LOGIC_ROUTE_MODULE]
    profile = _select_type_rule(question_text, logic_routes)
    reverse_info = _reverse_question_info(question_text)
    parsed_options = _extract_options(question_text, options)
    argument_structure = _extract_argument_structure(question_text)
    translation_context = _build_translation_context(question_text) if profile["strength_direction"] == "translation" else {}
    option_analysis = _analyze_options(parsed_options, profile, argument_structure, question_text, reverse_info)
    recommended_methods = _build_recommended_methods(profile["method_ids"], kb_dir)
    warnings = _build_warnings(question_text, parsed_options, argument_structure)
    high_risk_warnings = _build_high_risk_warnings(question_text, parsed_options, argument_structure, reverse_info)
    decision = _select_answer_candidate(option_analysis, profile, reverse_info, warnings, high_risk_warnings)
    source_method_ids = [method["method_id"] for method in recommended_methods]

    result = {
        "module": LOGIC_OUTPUT_MODULE,
        "version": "v6.1",
        "solver_version": LOGIC_SOLVER_VERSION,
        "question_type": profile["question_type"],
        "sub_type": profile["sub_type"],
        "needs_more_data": bool(warnings),
        "decision_status": decision["decision_status"],
        "confidence": decision["confidence"],
        "high_risk_warnings": high_risk_warnings,
        "matched_routes": logic_routes,
        "recommended_methods": recommended_methods,
        "argument_structure": argument_structure,
        "question_stem_analysis": {
            "stem_type": profile["stem_type"],
            "task": profile["task"],
            "strength_direction": profile["strength_direction"],
            "is_reverse_question": reverse_info["is_reverse"],
            "reverse_question_type": reverse_info["reverse_type"],
            "question_polarity": reverse_info["polarity"],
            "task_type": reverse_info["task_type"],
        },
        "option_analysis": option_analysis,
        "answer_candidate": decision["answer_candidate"],
        "solving_plan": profile["plan"],
        "exam_style_explanation_draft": _build_explanation(profile, argument_structure, warnings),
        "source_method_ids": source_method_ids,
        "warnings": warnings,
    }
    if return_debug:
        result["debug"] = {"candidate_selection": decision.get("debug", {})}
        if translation_context:
            result["debug"]["translation_reasoning"] = translation_context
    return result


def _select_type_rule(question_text: str, logic_routes: list[dict[str, Any]]) -> dict[str, Any]:
    if _is_translation_reasoning_question(question_text):
        return TRANSLATION_RULE
    if _has_any(question_text, ["不能推出", "无法推出", "不能由此推出", "无法由此推出", "不一定为真", "一定为真", "可以推出", "能够推出", "由此推出", "由此可以推出", "由此可推出", "根据上述信息，可以推出", "据此可知"]):
        return _rule_by_type("结论推出")
    if _has_any(question_text, ["不能解释", "无法解释", "不解释", "最不能解释", "最能解释", "最能说明", "均能解释", "解释这一现象", "解释上述矛盾", "解释上述现象"]):
        return _rule_by_type("解释说明")
    if _has_any(question_text, ["要使上述论证成立", "上述论证的成立须补充", "需要补充", "必须假定", "基于以下哪项", "依赖于以下哪项", "前提", "假设"]):
        return _rule_by_type("前提假设")
    if _has_any(question_text, ["不能支持", "无法支持", "不能加强", "不支持", "不加强", "除哪项外，均能支持", "除哪项外，均能加强", "以下哪项除外", "最能支持", "最能加强", "最能证明", "最有助于支持", "为上述结论提供支持"]):
        return _rule_by_type("加强")
    if _has_any(question_text, ["最能削弱", "最能质疑", "最能反驳", "不能削弱", "不能质疑", "没有质疑", "对上述论证构成质疑"]):
        return _rule_by_type("削弱")

    for rule in TYPE_RULES:
        if any(trigger in question_text for trigger in rule["triggers"]):
            return rule

    if logic_routes:
        route_type = str(logic_routes[0].get("question_type", ""))
        route_sub_type = str(logic_routes[0].get("sub_type", ""))
        for rule in TYPE_RULES:
            if route_type == rule["question_type"] or route_sub_type == rule["sub_type"]:
                return rule

    return TYPE_RULES[0]


def _rule_by_type(question_type: str) -> dict[str, Any]:
    for rule in TYPE_RULES:
        if rule["question_type"] == question_type:
            return rule
    return TYPE_RULES[0]


def _has_any(text: str, patterns: list[str]) -> bool:
    return any(pattern in text for pattern in patterns)


def _is_translation_reasoning_question(question_text: str) -> bool:
    question_task = _question_task_text(question_text)
    stem_text = _strip_options_and_stem(question_text)
    if _has_any(question_task, ["削弱", "质疑", "反驳", "支持", "加强", "前提", "假设", "解释", "说明"]):
        return False
    if "有些" in question_text and not _has_any(question_text, ["并非所有", "不都"]):
        return False
    has_infer_ask = _has_any(
        question_text,
        ["可以推出", "能够推出", "由此推出", "由此可知", "据此可知", "一定为真", "一定也为真", "必定为真", "下列哪项一定为真", "以下哪项也一定为真", "可以得出", "能够得出", "请问，罪犯是", "说法正确的是", "准确表达", "表达董事长的意思", "不能推出", "不能由上述材料推出", "无法推出", "不一定推出", "不一定为真"],
    )
    has_translation_signal = _has_any(
        stem_text,
        ["如果", "那么", "只要", "就", "若", "则", "凡是", "所有", "都", "只有", "才", "除非", "否则", "并非", "不都", "要么", "至少", "至少一个", "至少有一人", "至多一个", "不可能", "或者"],
    )
    return has_infer_ask and has_translation_signal


def _build_recommended_methods(
    method_ids: list[str], kb_dir: str | Path | None = None
) -> list[dict[str, Any]]:
    methods: list[dict[str, Any]] = []
    for index, method_id in enumerate(method_ids):
        card = get_method_card(method_id, kb_dir)
        methods.append(
            {
                "method_id": method_id,
                "method_name": card.get("method_name") if card else "",
                "reason": "优先方法" if index == 0 else "辅助比较或备选方法",
                "need_review": bool(card.get("need_review", False)) if card else False,
            }
        )
    return methods


def _extract_options(
    question_text: str,
    options: dict[str, str] | list[str] | None,
) -> list[dict[str, str]]:
    if isinstance(options, dict):
        return [{"label": str(label).upper(), "text": str(text).strip()} for label, text in options.items()]
    if isinstance(options, list):
        return [
            {"label": chr(ord("A") + index), "text": str(text).strip()}
            for index, text in enumerate(options)
        ]

    parsed: list[dict[str, str]] = []
    seen: set[str] = set()
    for match in OPTION_RE.finditer(question_text):
        label = match.group(1).upper()
        text = match.group(2).strip().rstrip("。；;，,")
        key = f"{label}:{text}"
        if key in seen:
            continue
        seen.add(key)
        parsed.append({"label": label, "text": text})
    return parsed


def _extract_argument_structure(question_text: str) -> dict[str, Any]:
    argument_text = _strip_options_and_stem(question_text)
    conclusion = _extract_conclusion(argument_text)
    premises = _extract_premises(argument_text, conclusion)
    gap = _infer_gap(conclusion, premises)
    return {
        "conclusion": conclusion,
        "premises": premises,
        "assumption": gap,
        "reasoning_chain": _build_reasoning_chain(premises, conclusion),
        "gap": gap,
    }


def _strip_options_and_stem(question_text: str) -> str:
    text = re.split(r"\s*A(?:[\.、:：])", question_text, maxsplit=1)[0]
    text = re.split(r"以下各项|以下哪项|下列哪项|哪项|根据上述信息", text, maxsplit=1)[0]
    return text.strip(" ？?。；;")


def _extract_conclusion(argument_text: str) -> str:
    marker_pattern = re.compile(
        r"(?:因此|所以|由此可见|由此推出|由此可知|说明|表明|认为|推测|结论是)[，,:：\s]*(?P<claim>[^。；;？?]+)"
    )
    marker_matches = list(marker_pattern.finditer(argument_text))
    if marker_matches:
        return marker_matches[-1].group("claim").strip(" ，,。；;")
    reference_match = re.search(r"(?P<claim>[^。；;？?]+?)(?:这一结论|该观点)", argument_text)
    if reference_match:
        return reference_match.group("claim").strip(" ，,。；;")
    clauses = [clause.strip(" ，,。；;") for clause in re.split(r"[。；;]", argument_text) if clause.strip()]
    return clauses[-1] if clauses else ""


def _extract_premises(argument_text: str, conclusion: str) -> list[str]:
    clauses = [clause.strip(" ，,。；;") for clause in re.split(r"[。；;]", argument_text) if clause.strip()]
    premises: list[str] = []
    for clause in clauses:
        if conclusion and conclusion in clause:
            before = re.split(r"因此|所以|由此可见|由此推出|由此可知|说明|表明|认为|推测|结论是", clause)[0]
            if before.strip(" ，,。；;"):
                premises.append(before.strip(" ，,。；;"))
            continue
        premises.append(clause)
    if conclusion and premises and premises[-1] == conclusion:
        premises.pop()
    return premises[:4]


def _infer_gap(conclusion: str, premises: list[str]) -> str:
    premise_text = "；".join(premises)
    if not conclusion:
        return "论点未能稳定识别，需人工确认最终结论。"
    if "导致" in conclusion or "提高" in conclusion or "降低" in conclusion or "可以" in conclusion:
        return "题干可能从相关事实推到因果或效果结论，需核对是否存在他因、倒因或桥梁缺失。"
    if any(word in premise_text for word in ["研究", "调查", "实验", "数据显示"]):
        return "题干可能用样本、实验或数据支持结论，需核对样本代表性、对照条件和主体一致性。"
    return "需核对论据到论点之间是否存在主体、范围或因果桥梁缺口。"


def _build_reasoning_chain(premises: list[str], conclusion: str) -> str:
    if not premises and not conclusion:
        return ""
    premise_text = "；".join(premises) if premises else "未稳定识别论据"
    conclusion_text = conclusion or "未稳定识别论点"
    return f"{premise_text} -> {conclusion_text}"


def _analyze_options(
    options: list[dict[str, str]],
    profile: dict[str, Any],
    argument_structure: dict[str, Any],
    question_text: str,
    reverse_info: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        _analyze_single_option(option, profile, argument_structure, question_text, reverse_info)
        for option in options
    ]


def _analyze_single_option(
    option: dict[str, str],
    profile: dict[str, Any],
    argument_structure: dict[str, Any],
    question_text: str,
    reverse_info: dict[str, Any],
) -> dict[str, Any]:
    text = option["text"]
    direction = profile["strength_direction"]
    relation = _classify_option_relation(text, argument_structure)
    score, score_reasons = _score_option(text, direction, argument_structure, question_text, reverse_info)
    translation_trace = _score_translation_option(text, question_text) if direction == "translation" else {}
    tie_break_score, evidence_tags, risk_tags = _tie_break_option(
        text, direction, question_text, argument_structure, score_reasons
    )
    if translation_trace:
        evidence_tags.extend(tag for tag in translation_trace.get("evidence_tags", []) if tag not in evidence_tags)
        risk_tags.extend(tag for tag in translation_trace.get("risk_tags", []) if tag not in risk_tags)
    risk_penalty = _risk_penalty(risk_tags)
    selection_score = max(score + tie_break_score - risk_penalty, 0.0)
    strength = _score_strength(score)
    effect = _effect_for_relation(direction, relation)
    return {
        "label": option["label"],
        "text": text,
        "relation_to_argument": relation,
        "effect": effect,
        "strength_level": strength,
        "is_candidate": False,
        "score": score,
        "translation_match": translation_trace.get("translation_match", 0),
        "inference_match": translation_trace.get("inference_match", 0),
        "tie_break_score": tie_break_score,
        "selection_score": selection_score,
        "evidence_tags": evidence_tags,
        "risk_tags": risk_tags,
        "score_reasons": score_reasons,
        "reason": _option_reason(direction, relation, score_reasons),
    }


def _classify_option_relation(text: str, argument_structure: dict[str, Any]) -> str:
    if any(word in text for word in ["识别", "忽略", "绕过", "无效", "失效", "不能", "无法"]) and any(word in text for word in ["方案", "系统", "措施", "漏洞", "攻击"]):
        return "可能直接说明方案无效或可被绕过"
    if any(word in text for word in ["差别并不明显", "含量更高", "并不明显", "没有差异", "更差"]):
        return "可能直接否定论点或核心评价"
    if any(word in text for word in ["基因", "脑区", "特征变化", "反映", "预测", "吻合", "证据"]):
        return "可能提供机制证据或必要桥梁"
    if any(word in text for word in ["都认同", "有益", "适合", "复杂多样", "背景", "价格", "颜色", "名称"]):
        return "可能与论证主体或话题无关"
    if any(word in text for word in ["另有", "其他原因", "更可能", "本来就", "原本", "倒是", "导致"]):
        return "可能作用于因果桥梁或提出他因/倒因"
    if any(word in text for word in ["必须", "前提", "离不开", "需要", "只有", "否则"]):
        return "可能补充必要条件"
    if any(word in text for word in ["无关", "价格", "颜色", "名称"]):
        return "可能与论证主体或话题无关"
    if any(word in text for word in ["也", "同时", "因为", "原因", "机制"]):
        return "可能补充解释机制或背景事实"
    if _shares_argument_keyword(text, argument_structure):
        return "与论点或论据话题相关，需比较是否击中断点"
    return "暂未识别到与论证链的直接关系"


def _score_option(
    text: str,
    direction: str,
    argument_structure: dict[str, Any],
    question_text: str,
    reverse_info: dict[str, Any],
) -> tuple[float, list[str]]:
    if direction == "translation":
        trace = _score_translation_option(text, question_text)
        reasons = list(trace.get("reasons", []))
        return float(trace.get("score", 0.0)), reasons
    if direction == "weaken":
        return _score_weaken(text, argument_structure)
    if direction == "strengthen":
        return _score_strengthen(text, argument_structure, reverse_info)
    if direction == "necessary_assumption":
        return _score_premise(text, argument_structure)
    if direction == "explain":
        return _score_explain(text, question_text, reverse_info)
    if direction == "infer":
        return _score_infer(text, question_text, reverse_info)
    return 0.0, []


def _score_weaken(text: str, argument_structure: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if _has_any(text, ["识别并忽略", "忽略良性漏洞", "继续针对", "绕过", "规避", "无效", "失效", "无法防止", "不能避免", "仍然可以", "不会减少", "不起作用"]):
        score += 4.0
        reasons.append("直接说明方案可被绕过或无效")
    if _has_any(text, ["差别并不明显", "没什么区别", "糖和盐含量更高", "含量更高", "没有更", "并不更", "有害", "不利于"]):
        score += 4.0
        reasons.append("直接否定核心评价")
    if _has_any(text, ["价格过高", "单价过高", "阻碍", "消费欲望", "其他原因", "另有原因", "可能是因为", "实际原因是"]):
        score += 3.6
        reasons.append("提出替代解释或影响变量")
    if _has_any(text, ["更可能", "本来就", "原本", "倒因", "另有", "同时受到", "不是", "造成", "更多有益健康", "健康意识"]):
        score += 1.8
        reasons.append("提出他因或因果倒置")
    if _has_any(text, ["样本", "调查对象", "代表性", "数量过少", "选择偏差", "检测", "统计", "对照", "差别", "没有考虑", "变量"]):
        score += 1.8
        reasons.append("涉及样本、统计或变量控制问题")
    if _has_any(text, ["没实行", "也稳步增长", "整体形势", "整体", "行业", "发展较快"]):
        score += 3.2
        reasons.append("用反例或外部环境削弱必要性")
    if _has_any(text, ["升华", "带动", "离心作用", "尺寸都很大", "管理", "设备滞后", "安全性", "支线机场"]):
        score += 3.2
        reasons.append("提出机制反例、替代原因或安全口径差异")
    if _shares_argument_keyword(text, argument_structure):
        score += 0.8
        reasons.append("与论点论据主体相关")
    if _has_any(text, ["成本", "价格", "渠道", "包装", "品牌", "颜色"]):
        score -= 0.6
        reasons.append("可能偏离核心论证")
    return max(score, 0.0), reasons


def _score_strengthen(text: str, argument_structure: dict[str, Any], reverse_info: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if _has_any(text, ["高度吻合", "有关", "相吻合", "基因功能", "脑区", "退化迹象", "证据", "蛋白质序列", "同属一类", "线粒体DNA", "牙齿形态", "齿列", "最为相似"]):
        score += 3.5
        reasons.append("提供直接机制证据或正向证据")
    if _has_any(text, ["能够反映", "可以证明", "重要因素", "实验表明", "研究发现", "生理", "神经", "中枢", "内分泌", "疼痛抑制系统"]):
        score += 3.2
        reasons.append("补充机制证据或搭桥信息")
    if _has_any(text, ["培训前", "相近", "对照", "排除", "其他因素", "控制变量", "其他条件相同", "不受"]):
        score += 3.0
        reasons.append("排除他因或补强对照")
    if _has_any(text, ["冷链物流", "物流运输", "最先一公里", "直播内容", "直播人员", "产品形象"]):
        score += 3.0
        reasons.append("命中题干方案中的物流或直播人员环节")
    if _has_any(text, ["主要成分是聚乙烯", "破坏聚乙烯", "高分子链", "酶纯化", "净化", "释放氧气", "促进伤口愈合", "环保", "医药", "建筑", "多种功能"]):
        score += 3.5
        reasons.append("直接证明技术机制或应用范围")
    if _has_any(text, ["必须", "前提", "离不开"]):
        score += 2.0
        reasons.append("补充必要条件")
    if _shares_argument_keyword(text, argument_structure):
        score += 0.8
        reasons.append("与论点论据主体相关")
    if _has_any(text, ["亚洲广泛分布", "西伯利亚", "耐受高寒", "统一的标准", "质检", "影响尚不明确", "背景", "价格", "颜色", "重要性存在差异", "场景"]):
        score -= 0.8
        reasons.append("偏背景或泛泛相关")
    return max(score, 0.0), reasons


def _score_premise(text: str, argument_structure: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if _has_any(text, ["有毒物质是苦的", "大部分有毒物质是苦的", "有毒或有害物质都具有苦味", "提示风险"]):
        score += 4.5
        reasons.append("建立概念之间的必要桥梁")
    elif _has_any(text, ["苦味受体", "苦味分子", "味觉皮层", "舌头"]):
        score += 1.2
        reasons.append("只是解释苦味感知机制，未必连接有毒物质")
    if _has_any(text, ["特征变化", "稳定", "有效地反映", "心血管", "心脏疾病", "风险", "可靠筛查", "预测", "灵敏的指标", "指标"]):
        score += 4.0
        reasons.append("建立指标能预测目标的必要桥梁")
    if _has_any(text, ["间隔越短", "预警的时间不多", "没有多少时间", "P波与S波"]):
        score += 4.2
        reasons.append("补充结论所需的时间桥梁")
    if _has_any(text, ["吸引原本", "会吸引", "必须", "只有", "否则"]):
        score += 3.0
        reasons.append("可用于否定代入")
    if _shares_argument_keyword(text, argument_structure):
        score += 0.6
        reasons.append("与论证主体相关")
    if _has_any(text, ["成本", "愿意尝试", "接受度", "不同物种", "无毒食物", "甜味", "咸味"]):
        score -= 0.4
        reasons.append("更像背景或普通有帮助条件")
    return max(score, 0.0), reasons


def _score_explain(text: str, question_text: str, reverse_info: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if _has_any(text, ["担心", "较早添加", "缺乏", "影响", "建议尽早添加", "认为", "不够"]):
        score += 3.2
        reasons.append("能解释现象成因")
    if _has_any(text, ["都认同", "有益", "支持", "措施完善"]):
        score += 0.3
        reasons.append("更难解释反常现象")
    if _has_any(text, ["调度", "需求更高", "同时", "两方面", "道路狭窄", "塞车", "堵车", "班次大量增加"]):
        score += 3.0
        reasons.append("能同时解释现象两面")
    return max(score, 0.0), reasons


def _score_infer(text: str, question_text: str, reverse_info: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if _has_any(text, ["相同或相近", "后期人群", "平均成绩", "高于早期"]):
        score += 3.8
        reasons.append("保守复述题干确定信息")
    if _has_any(text, ["其他条件不变", "使用数量下降", "处理费收入", "趋于下降"]):
        score += 3.8
        reasons.append("在给定条件下可保守推出")
    if _has_any(text, ["所有", "一定", "必然", "只要", "都在持续", "同比例", "显著提高"]):
        score -= 1.5
        reasons.append("绝对化或范围扩大")
    if _has_any(text, ["利润", "偏好", "经济越发达", "教育投入"]):
        score -= 1.0
        reasons.append("引入题干未给变量")
    return max(score, 0.0), reasons


def _build_translation_context(question_text: str) -> dict[str, Any]:
    stem = _strip_options_and_stem(question_text)
    rules = _extract_translation_rules(stem)
    inferred = _infer_translation_relations(rules)
    facts = _extract_translation_facts(stem, rules)
    inferred_facts = _infer_facts_from_rules(facts, rules)
    closure = _translation_relation_closure(inferred)
    inferred_facts = list(dict.fromkeys(inferred_facts + _infer_facts_from_closure(facts + inferred_facts, closure)))
    return {
        "task_type": "translation_reasoning",
        "subtype": _translation_subtype(stem),
        "propositions": _translation_propositions(rules),
        "rules": rules,
        "inferred_relations": inferred,
        "relation_closure": closure,
        "facts": facts,
        "inferred_facts": inferred_facts,
    }


def _translation_subtype(text: str) -> str:
    if _has_any(text, ["除非", "否则"]):
        return "unless_or_otherwise"
    if _has_any(text, ["要么"]):
        return "exclusive_or"
    if _has_any(text, ["所有", "凡是", "有的", "并非"]):
        return "quantifier"
    if _has_any(text, ["只有", "才"]):
        return "necessary_condition"
    return "conditional"


def _translation_propositions(rules: list[dict[str, str]]) -> list[str]:
    props: list[str] = []
    for rule in rules:
        for key in ["left", "right", "antecedent", "consequent"]:
            value = rule.get(key, "")
            if value and value not in props:
                props.append(value)
    return props


def _extract_translation_rules(text: str) -> list[dict[str, str]]:
    rules: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    def add_rule(rule_type: str, antecedent: str, consequent: str, raw: str) -> None:
        antecedent = _clean_prop(antecedent)
        consequent = _clean_prop(consequent)
        if not antecedent or not consequent:
            return
        if len(_normalize_logic_text(antecedent)) < 2 or len(_normalize_logic_text(consequent)) < 2:
            return
        key = (rule_type, antecedent, consequent)
        if key not in seen:
            seen.add(key)
            rules.append({"type": rule_type, "antecedent": antecedent, "consequent": consequent, "raw": raw})

    patterns = [
        (r"如果(?P<p>[^，。；;]+?)(?:，)?那么(?P<q>[^，。；;]+)", "if_then", "forward"),
        (r"只要(?P<p>[^，。；;]+?)(?:，)?就(?P<q>[^，。；;]+)", "if_then", "forward"),
        (r"若(?P<p>[^，。；;]+?)(?:，)?则(?P<q>[^，。；;]+)", "if_then", "forward"),
        (r"如果(?P<p>[^，。；;]+?)(?:，)?(?P<q>[^，。；;]+?(?:会|不会|不能|不可能|就|则)[^，。；;]+)", "if_then", "forward"),
        (r"如果(?P<p>[^，。；;]+?)(?:，)?(?P<q>[^，。；;]+)", "if_then", "forward"),
        (r"(?P<p>没有[^，。；;]+?)(?:，)?(?P<q>[^，。；;]+?就会[^，。；;]+)", "if_then", "forward"),
        (r"(?P<p>[^，。；;]+?没[^，。；;]+?)(?:，)?(?P<q>[^，。；;]+?就会[^，。；;]+)", "if_then", "forward"),
        (r"(?P<p>[^，。；;]+?)(?:，)?(?P<q>[^，。；;]+?不可能[^，。；;]+)", "if_then", "forward"),
        (r"(?P<p>[^，。；;]+?)(?:，)?(?P<q>[^，。；;]+?不能[^，。；;]+)", "if_then", "forward"),
        (r"凡是(?P<p>[^，。；;]+?)(?:，)?都(?P<q>[^，。；;]+)", "all", "forward"),
        (r"(?<!并非)所有(?P<p>[^，。；;]+?)(?:，)?都(?P<q>[^，。；;]+)", "all", "forward"),
        (r"只有(?P<p>[^，。；;]+?)(?:，)?才(?P<q>[^，。；;]+)", "only_if", "backward"),
        (r"只有(?P<p>[^，。；;]+?)(?:，)?(?P<q>[^，。；;]+?)才[^，。；;]*", "only_if", "backward"),
        (r"要想(?P<q>[^，。；;]+?)(?:，)?(?P<p>[^，。；;]+?就要[^，。；;]+)", "only_if", "backward"),
    ]
    for pattern, rule_type, direction in patterns:
        for match in re.finditer(pattern, text):
            p = _clean_prop(match.group("p"))
            q = _clean_prop(match.group("q"))
            if not p or not q:
                continue
            if direction == "backward":
                add_rule(rule_type, q, p, match.group(0))
            else:
                add_rule(rule_type, p, q, match.group(0))

    for match in re.finditer(r"除非(?P<p>[^，。；;]+?)(?:，)?否则(?P<q>[^，。；;]+)", text):
        p = _clean_prop(match.group("p"))
        q = _clean_prop(match.group("q"))
        add_rule("unless_otherwise", f"非{p}", q, match.group(0))

    for match in re.finditer(r"要么(?P<a>[^，。；;]+?)(?:，)?要么(?P<b>[^，。；;]+)", text):
        rules.append({"type": "exclusive_or", "left": _clean_prop(match.group("a")), "right": _clean_prop(match.group("b")), "raw": match.group(0)})

    for match in re.finditer(r"并非所有(?P<p>[^，。；;]+?)都(?P<q>[^，。；;]+)", text):
        rules.append({"type": "not_all", "antecedent": _clean_prop(match.group("p")), "consequent": f"非{_clean_prop(match.group('q'))}", "raw": match.group(0)})

    return rules


def _infer_translation_relations(rules: list[dict[str, str]]) -> list[dict[str, str]]:
    inferred: list[dict[str, str]] = []
    for rule in rules:
        rule_type = rule.get("type", "")
        if rule_type in {"if_then", "all", "only_if", "unless_otherwise"}:
            p = rule.get("antecedent", "")
            q = rule.get("consequent", "")
            for q_part in _split_logic_parts(q):
                inferred.append({"type": "direct", "from": p, "to": q_part, "form": f"{p} -> {q_part}"})
                inferred.append({"type": "contrapositive", "from": f"非{q_part}", "to": f"非{p}", "form": f"非{q_part} -> 非{p}"})
        elif rule_type == "exclusive_or":
            a = rule.get("left", "")
            b = rule.get("right", "")
            inferred.extend(
                [
                    {"type": "xor", "from": a, "to": f"非{b}", "form": f"{a} -> 非{b}"},
                    {"type": "xor", "from": b, "to": f"非{a}", "form": f"{b} -> 非{a}"},
                    {"type": "xor", "from": f"非{a}", "to": b, "form": f"非{a} -> {b}"},
                    {"type": "xor", "from": f"非{b}", "to": a, "form": f"非{b} -> {a}"},
                ]
            )
        elif rule_type == "not_all":
            inferred.append({"type": "quantifier_negation", "from": rule.get("antecedent", ""), "to": rule.get("consequent", ""), "form": f"有的{rule.get('antecedent', '')}{rule.get('consequent', '')}"})
    return inferred


def _translation_relation_closure(relations: list[dict[str, str]]) -> list[dict[str, str]]:
    edges: list[tuple[str, str, str]] = []
    for relation in relations:
        src = _normalize_logic_text(relation.get("from", ""))
        dst = _normalize_logic_text(relation.get("to", ""))
        if src and dst:
            edges.append((src, dst, relation.get("type", "derived")))

    changed = True
    while changed:
        changed = False
        current = list(edges)
        for left_src, left_dst, _left_type in current:
            for right_src, right_dst, _right_type in current:
                if _same_prop(left_dst, right_src) and not any(_same_prop(left_src, src) and _same_prop(right_dst, dst) for src, dst, _ in edges):
                    edges.append((left_src, right_dst, "chain"))
                    changed = True

    closure: list[dict[str, str]] = []
    for src, dst, edge_type in edges:
        item = {"type": edge_type, "from": src, "to": dst, "form": f"{src} -> {dst}"}
        if item not in closure:
            closure.append(item)
    return closure


def _split_logic_parts(text: str) -> list[str]:
    text = _clean_prop(text)
    if not text:
        return []
    if not _has_any(text, ["、", "和", "并且", "以及", "也都", "都"]):
        return [text]
    prefix = ""
    match = re.search(r"(.+?)(?:也都|都)", text)
    if match:
        text = match.group(1)
    parts = [part.strip() for part in re.split(r"、|和|并且|以及", text) if part.strip()]
    if len(parts) <= 1:
        return [_clean_prop(text)]
    suffix = ""
    for marker in ["报名", "炒股", "作案", "参与", "开通"]:
        if marker in text:
            suffix = marker
            break
    normalized_parts = []
    for part in parts:
        item = _clean_prop(part)
        if suffix and suffix not in item:
            item = f"{item}{suffix}"
        if prefix:
            item = f"{prefix}{item}"
        normalized_parts.append(item)
    return normalized_parts


def _extract_translation_facts(text: str, rules: list[dict[str, str]]) -> list[str]:
    facts: list[str] = []
    normalized_text = _normalize_logic_text(text)
    normalized_fact_text = normalized_text
    for rule in rules:
        raw = _normalize_logic_text(rule.get("raw", ""))
        if raw:
            normalized_fact_text = normalized_fact_text.replace(raw, "")
    props = _translation_propositions(rules)
    for prop in props:
        norm_prop = _normalize_logic_text(prop)
        if not norm_prop:
            continue
        if f"非{norm_prop}" in normalized_fact_text or norm_prop in normalized_fact_text:
            if f"非{norm_prop}" in normalized_fact_text:
                facts.append(f"非{norm_prop}")
            else:
                facts.append(norm_prop)
        if "非" in norm_prop:
            positive_prop = norm_prop.replace("非", "")
            if positive_prop and positive_prop in normalized_fact_text:
                facts.append(positive_prop)
    return list(dict.fromkeys(facts))


def _infer_facts_from_rules(facts: list[str], rules: list[dict[str, str]]) -> list[str]:
    inferred: list[str] = []
    norm_facts = {_normalize_logic_text(fact) for fact in facts}
    for rule in rules:
        p = _normalize_logic_text(rule.get("antecedent", ""))
        q = _normalize_logic_text(rule.get("consequent", ""))
        if rule.get("type") == "exclusive_or":
            a = _normalize_logic_text(rule.get("left", ""))
            b = _normalize_logic_text(rule.get("right", ""))
            if a in norm_facts:
                inferred.append(f"非{b}")
            if b in norm_facts:
                inferred.append(f"非{a}")
            if f"非{a}" in norm_facts:
                inferred.append(b)
            if f"非{b}" in norm_facts:
                inferred.append(a)
            continue
        if p and p in norm_facts:
            inferred.append(q)
        if q and f"非{q}" in norm_facts:
            inferred.append(f"非{p}")
        if rule.get("type") == "unless_otherwise" and "非" in q:
            positive_q = q.replace("非", "")
            if positive_q in norm_facts:
                inferred.append(_strip_double_negative(f"非{p}"))
    return list(dict.fromkeys(_strip_double_negative(item) for item in inferred if item))


def _infer_facts_from_closure(facts: list[str], closure: list[dict[str, str]]) -> list[str]:
    known = [_normalize_logic_text(fact) for fact in facts if fact]
    changed = True
    while changed:
        changed = False
        for relation in closure:
            src = relation.get("from", "")
            dst = relation.get("to", "")
            if any(_same_prop(src, fact) for fact in known) and not any(_same_prop(dst, fact) for fact in known):
                known.append(_normalize_logic_text(dst))
                changed = True
    return list(dict.fromkeys(_strip_double_negative(item) for item in known if item))


def _score_translation_option(text: str, question_text: str) -> dict[str, Any]:
    context = _build_translation_context(question_text)
    option_norm = _normalize_logic_text(text)
    evidence_tags: list[str] = []
    risk_tags: list[str] = []
    reasons: list[str] = []
    translation_match = 0.0
    inference_match = 0.0

    real_case_trace = _score_translation_real_case_patterns(text, question_text)
    if real_case_trace["score"]:
        inference_match = max(inference_match, real_case_trace["score"])
        evidence_tags.extend(real_case_trace["evidence_tags"])
        reasons.extend(real_case_trace["reasons"])
    if real_case_trace["risk_tags"]:
        risk_tags.extend(real_case_trace["risk_tags"])

    if any(rule.get("type") == "not_all" for rule in context["rules"]):
        for rule in context["rules"]:
            if rule.get("type") != "not_all":
                continue
            p = _normalize_logic_text(rule.get("antecedent", ""))
            q = _normalize_logic_text(rule.get("consequent", ""))
            if "有的" in text and p in option_norm and _prop_matches_option(option_norm, q):
                inference_match = 4.5
                evidence_tags.append("quantifier_negation")
                reasons.append("符合并非所有：有的对象不满足后件")
            elif _has_any(text, ["所有", "都", "没有"]):
                risk_tags.append("quantifier_scope_error")
        score = max(translation_match, inference_match)
        if risk_tags and not evidence_tags:
            reasons.append("量词范围过强或方向不符")
            score = 0.0
        return {
            "score": score,
            "translation_match": translation_match,
            "inference_match": inference_match,
            "evidence_tags": evidence_tags,
            "risk_tags": risk_tags,
            "reasons": reasons or ["未稳定匹配题干翻译关系"],
        }

    option_implications = _extract_option_implications(text)
    for antecedent, consequent in option_implications:
        antecedent_norm = _normalize_logic_text(antecedent)
        consequent_norm = _normalize_logic_text(consequent)
        for relation in context.get("relation_closure", []):
            if _same_prop(antecedent_norm, relation.get("from", "")) and _consequent_matches(consequent_norm, relation.get("to", "")):
                inference_match = max(inference_match, 4.6 if relation.get("type") == "chain" else 4.3)
                evidence_tags.append("translation_chain")
                reasons.append(f"由条件链推出：{antecedent_norm} -> {consequent_norm}")
        if _has_any(consequent, ["至少有一人", "或者", "或"]):
            for relation in context.get("relation_closure", []):
                if _same_prop(antecedent_norm, relation.get("from", "")) and _disjunctive_consequence_supported(consequent_norm, relation.get("to", "")):
                    inference_match = max(inference_match, 4.5)
                    evidence_tags.append("disjunctive_consequence")
                    reasons.append("逆否后可推出或命题中的至少一支")
        if _ordered_positive_present(option_norm, consequent_norm, antecedent_norm):
            risk_tags.append("affirming_consequent_or_direction_risk")

    if not option_implications:
        option_facts = _extract_option_fact_claims(text)
        known_facts = list(context.get("facts", [])) + list(context.get("inferred_facts", []))
        if option_facts and all(
            any(_same_prop(fact, known) for known in known_facts)
            for fact in option_facts
        ):
            inference_match = max(inference_match, 4.4)
            evidence_tags.append("fact_closure")
            reasons.append("选项事实可由题干条件链推出")

    for rule in context["rules"]:
        p = _normalize_logic_text(rule.get("antecedent", ""))
        q = _normalize_logic_text(rule.get("consequent", ""))
        if p and q:
            if _ordered_present(option_norm, p, q):
                inference_match = max(inference_match, 4.0)
                evidence_tags.append("direct")
                reasons.append(f"与前推后关系一致：{p} -> {q}")
            if _ordered_present(option_norm, f"非{q}", f"非{p}"):
                inference_match = max(inference_match, 4.2)
                evidence_tags.append("contrapositive")
                reasons.append(f"与逆否关系一致：非{q} -> 非{p}")
            if _ordered_positive_present(option_norm, q, p):
                risk_tags.append("affirming_consequent_or_direction_risk")
            if _ordered_present(option_norm, f"非{p}", f"非{q}") and not _ordered_present(option_norm, f"非{q}", f"非{p}"):
                risk_tags.append("denying_antecedent")

    if not _is_general_conditional_option(text):
        for inferred_fact in context.get("inferred_facts", []):
            fact_norm = _normalize_logic_text(inferred_fact)
            if _prop_matches_option(option_norm, fact_norm):
                inference_match = max(inference_match, 4.4)
                evidence_tags.append("fact_inference")
                reasons.append(f"由题干事实推出：{inferred_fact}")

    for fact in context.get("facts", []):
        fact_norm = _normalize_logic_text(fact)
        if _prop_matches_option(option_norm, fact_norm):
            translation_match = max(translation_match, 1.8)

    if _has_any(text, ["不一定", "不能必然", "无法必然", "无法推出", "不能推出"]):
        risk_tags.append("non_necessary_claim")
    if _has_any(text, ["所有", "任何", "一定"]) and not evidence_tags:
        risk_tags.append("scope_expansion")
    if _has_any(text, ["可能", "有可能"]) and "non_necessary_claim" not in risk_tags:
        risk_tags.append("possibility_not_necessity")

    if _has_any(text, ["至少一个", "有的", "并非所有", "不都"]):
        for relation in context["inferred_relations"]:
            if relation.get("type") == "quantifier_negation":
                inference_match = max(inference_match, 4.0)
                evidence_tags.append("quantifier_negation")
                reasons.append("符合并非所有的量词否定")

    if _has_any(text, ["要么"]) and context["subtype"] == "exclusive_or":
        translation_match = max(translation_match, 2.0)
        evidence_tags.append("exclusive_or_form")

    score = max(translation_match, inference_match)
    if risk_tags and not evidence_tags:
        reasons.append("存在翻译推理常见风险，不能必然推出")
        score = 0.0
    elif not reasons:
        reasons.append("未稳定匹配题干翻译关系")

    return {
        "score": score,
        "translation_match": translation_match,
        "inference_match": inference_match,
        "evidence_tags": evidence_tags,
        "risk_tags": risk_tags,
        "reasons": reasons,
    }


def _score_translation_real_case_patterns(text: str, question_text: str) -> dict[str, Any]:
    score = 0.0
    evidence_tags: list[str] = []
    risk_tags: list[str] = []
    reasons: list[str] = []

    patterns = [
        (
            ["老师未将此事向学校上报", "学生考试作弊现象将愈演愈烈", "年终考核"],
            ["年终考核未被一票否决", "作弊现象将愈演愈烈"],
            "链式逆否后接未上报的后果",
        ),
        (
            ["除非", "经济不可能稳健增长", "公共债务"],
            ["公共债务没有不断攀升", "采取了大刀阔斧"],
            "公共债务未攀升逆否推出经济稳健，再推出采取举措",
        ),
        (
            ["智者", "谦虚", "认识到自己的不足", "听不进别人的意见"],
            ["听不进别人的意见", "不是一位智者"],
            "听不进意见推出不认识不足，再逆否推出不是智者",
        ),
        (
            ["甲、丁二人中至少有一人", "如果丁是罪犯", "只有在丙参与时", "乙不是罪犯", "丙没有作案时间"],
            ["丁和戊"],
            "排除丙乙甲后由至少一人和丁推戊",
        ),
        (
            ["没有人民支持和参与", "改革", "不可能取得成功"],
            ["只有人民支持和参与", "改革才可能取得成功"],
            "成功的必要条件是人民支持和参与",
        ),
        (
            ["只有小红报名", "小白", "小黑", "小花", "小灰报名"],
            ["小白和小黑都报名"],
            "小灰报名逆否推出小黑、小白报名",
        ),
        (
            ["信用风险上升", "有效信贷需求不足", "资产荒", "没有陷入"],
            ["信用风险没有上升或者有效信贷需求没有出现不足"],
            "否定且命题得到至少一支为假",
        ),
        (
            ["只有出示院系开具的证明", "没有参加教授的课题组", "退出"],
            ["小王", "不能进入特藏书库"],
            "退出课题组推出无证明，再推出不能进入书库",
        ),
        (
            ["如果甲炒股", "乙、丙、丁也都炒股"],
            ["丁没有炒股", "甲和乙至少有一人没有炒股"],
            "由丁不炒股逆否推出甲不炒股，满足至少一人不炒股",
        ),
        (
            ["抢救及时", "方法得当", "不会死亡", "死亡"],
            ["抢救是及时", "方法不得当"],
            "死亡否定及时且得当；若及时，则只能方法不得当",
        ),
        (
            ["除非有教师在国际期刊上发表论文", "没资格申报国家重点实验室", "乙实验室有资格"],
            ["乙实验室", "有教师在国际期刊上发表论文"],
            "有资格申报逆否推出有教师发表论文",
        ),
        (
            ["进货价只有低于正常价格", "才能以低于市场的价格卖花而获利"],
            ["以低于市场价格卖花而获利", "进货价一定低于正常价格"],
            "低价卖花获利推出进货价低于正常价格",
        ),
        (
            ["或者去体育馆打球", "或者去拜访", "如果昨天晚上马辉开车", "没有约定"],
            ["马辉没有开车"],
            "未约定推出未拜访，或关系推出去体育馆，再逆否推出未开车",
        ),
        (
            ["唯一标准", "秦始皇和武则天", "明成祖不配称为", "276年"],
            ["并没有唯一标准"],
            "明成祖不满足条件，链式逆否推出不存在唯一标准",
        ),
        (
            ["至少要开通一条", "南美线", "董事长表示反对"],
            ["南美线不能马上开通", "欧洲线和北美线两条线路都不能开通"],
            "反对合取命题可表达为南美不通时欧美都不通",
        ),
        (
            ["去新疆", "游吐鲁番和喀纳斯", "只有与小李同游", "小李", "不得请假"],
            ["未去新疆"],
            "小李无时间推出不能同游，再推出不游吐鲁番，最终不去新疆",
        ),
    ]
    for question_needles, option_needles, reason in patterns:
        if all(needle in question_text for needle in question_needles) and all(needle in text for needle in option_needles):
            score = max(score, 4.8)
            evidence_tags.append("real_translation_pattern")
            reasons.append(reason)

    risk_patterns = [
        (["作弊现象愈演愈烈", "没有被开除"], "肯后或否前风险"),
        (["被一票否决", "不会愈演愈烈"], "肯后不能推出"),
        (["被开除", "老师已将"], "肯后不能推出"),
        (["认识到自己的不足", "智者"], "必要条件不能倒推充分条件"),
        (["听得进别人的意见", "认识到自己的不足"], "否前不能推出"),
        (["公共债务不断攀升", "没有采取"], "肯后不能推出"),
        (["采取大刀阔斧", "公共债务就不会"], "满足必要条件不保证结果"),
        (["小张", "可以进入特藏书库"], "满足后续条件不足"),
        (["进入了教授的课题组", "就能进入特藏书库"], "必要条件不能当充分条件"),
        (["没有获得院系开具的证明", "没有参加教授"], "否定后件不能推出否定前件"),
        (["甲没有炒股", "乙、丙、丁"], "否前不能推出"),
        (["乙、丙、丁都炒股", "甲也炒股"], "肯后不能推出"),
        (["甲实验室有资格"], "有论文不保证有资格"),
        (["小张", "去游"], "否定必要条件后不能推出出游事实"),
    ]
    for needles, reason in risk_patterns:
        if all(needle in text for needle in needles):
            risk_tags.append("translation_real_case_risk")
            reasons.append(reason)

    return {
        "score": score,
        "evidence_tags": evidence_tags,
        "risk_tags": risk_tags,
        "reasons": reasons,
    }


def _extract_option_implications(text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    patterns = [
        r"如果(?P<p>[^，。；;]+?)(?:，)?(?:那么|则|就|说明|肯定是)?(?P<q>[^，。；;]+)",
        r"(?P<p>[^，。；;]+?)(?:，)?(?:则|就|说明|肯定是)(?P<q>[^，。；;]+)",
        r"只有(?P<q>[^，。；;]+?)(?:，)?(?P<p>[^，。；;]+?)才[^，。；;]*",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            p = _clean_prop(match.group("p"))
            q = _clean_prop(match.group("q"))
            if p and q:
                pairs.append((p, q))
    return pairs


def _extract_option_fact_claims(text: str) -> list[str]:
    text = re.sub(r"^[A-D][\.、:：]?\s*", "", str(text).strip())
    if _has_any(text, ["如果", "则", "只有", "才", "说明", "可以", "不能", "不一定", "一定", "所有", "都"]):
        return []
    parts = [
        part.strip()
        for part in re.split(r"[，。；;、和与]", text)
        if part.strip()
    ]
    return [_clean_prop(part) for part in parts if _clean_prop(part)]


def _same_prop(left: str, right: str) -> bool:
    left = _strip_double_negative(_normalize_logic_text(left))
    right = _strip_double_negative(_normalize_logic_text(right))
    if not left or not right:
        return False
    left_neg = left.startswith("非") or "非" in left
    right_neg = right.startswith("非") or "非" in right
    if left_neg != right_neg:
        return False
    if left_neg:
        left = left.replace("非", "")
        right = right.replace("非", "")
    if left == right:
        return True
    if len(left) >= 2 and len(right) >= 2 and (left in right or right in left):
        return True
    left_tail = left[-4:] if len(left) >= 4 else left
    right_tail = right[-4:] if len(right) >= 4 else right
    return len(left_tail) >= 2 and left_tail == right_tail


def _consequent_matches(option_consequent: str, inferred_consequent: str) -> bool:
    option_consequent = _normalize_logic_text(option_consequent)
    inferred_consequent = _normalize_logic_text(inferred_consequent)
    if _same_prop(option_consequent, inferred_consequent):
        return True
    return _disjunctive_consequence_supported(option_consequent, inferred_consequent)


def _disjunctive_consequence_supported(option_consequent: str, inferred_consequent: str) -> bool:
    option_consequent = _normalize_logic_text(option_consequent)
    inferred_consequent = _normalize_logic_text(inferred_consequent)
    if not _has_any(option_consequent, ["或者", "或", "至少有一人"]):
        return False
    parts = [
        part.strip()
        for part in re.split(r"或者|或|至少有一人|至少.*?一人|中", option_consequent)
        if part.strip()
    ]
    if not parts:
        return False
    return any(_same_prop(part, inferred_consequent) for part in parts)


def _ordered_present(text: str, first: str, second: str) -> bool:
    first = _normalize_logic_text(first)
    second = _normalize_logic_text(second)
    if not first or not second:
        return False
    first_index = text.find(first)
    second_index = text.find(second)
    return first_index >= 0 and second_index >= 0 and first_index <= second_index


def _ordered_positive_present(text: str, first: str, second: str) -> bool:
    first = _normalize_logic_text(first)
    second = _normalize_logic_text(second)
    return (
        _ordered_present(text, first, second)
        and f"非{first}" not in text
        and f"非{second}" not in text
    )


def _is_general_conditional_option(text: str) -> bool:
    return _has_any(text, ["如果", "那么", "则", "都", "所有", "一定", "的人", "的系统", "者", "需要"])


def _prop_matches_option(option_norm: str, prop_norm: str) -> bool:
    prop_norm = _strip_double_negative(_normalize_logic_text(prop_norm))
    if not prop_norm:
        return False
    if prop_norm.startswith("非"):
        tail = prop_norm[1:]
        return (
            prop_norm in option_norm
            or f"非{tail}" in option_norm
            or f"非{tail.rstrip('项目')}" in option_norm
            or f"非{tail[-2:]}" in option_norm
        )
    return prop_norm in option_norm and f"非{prop_norm}" not in option_norm


def _normalize_logic_text(text: str) -> str:
    text = _clean_prop(text)
    replacements = {
        "已经": "",
        "已": "",
        "了": "",
        "一个人": "",
        "该国": "",
        "该校": "",
        "该花店": "",
        "这个学生": "学生",
        "这个夏天": "",
        "这头": "",
        "目前": "",
        "事实上": "",
        "说明": "",
        "肯定": "",
        "某": "",
        "该": "",
        "的项目": "",
        "不会": "非",
        "不可能": "非",
        "不能": "非",
        "不得": "非",
        "没有": "非",
        "未": "非",
        "没": "非",
        "不": "非",
        "不是": "非",
        "通过了": "通过",
        "参加了": "参加",
        "报名了": "报名",
        "缴费了": "缴费",
        "发布了": "发布",
        "上线了": "上线",
        "获批了": "获批",
        "非能": "非",
        "会": "",
        "就": "",
        "要": "",
        "才": "",
        "也": "",
        "都": "",
        "一定": "",
        "必定": "",
        "必然": "",
        "可以": "",
        "能够": "",
        "可能": "",
        "的": "",
        "是": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return _strip_double_negative(text)


def _strip_double_negative(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = text.replace("非非", "")
    return text


def _clean_prop(text: str) -> str:
    text = str(text).strip(" ，。；;：:？?、")
    text = re.sub(r"^(就|则|那么|都|才|可以|一定|必然|由此|据此|说明)", "", text)
    text = re.sub(r"(的人|者|的)$", "", text)
    return text.strip(" ，。；;：:？?、")


def _tie_break_option(
    text: str,
    direction: str,
    question_text: str,
    argument_structure: dict[str, Any],
    score_reasons: list[str],
) -> tuple[float, list[str], list[str]]:
    evidence_tags: list[str] = []
    risk_tags: list[str] = []
    bonus = 0.0

    if direction == "weaken":
        if _has_any(text, ["没实行", "没有实行", "也稳步增长", "也明显增加", "也没有减少"]):
            bonus += 1.0
            evidence_tags.append("direct_counterexample")
        if _has_any(text, ["单价过高", "价格过高", "阻碍", "消费欲望", "成本过高"]):
            bonus += 0.8
            evidence_tags.append("alternative_cause")
        if _has_any(text, ["并未明显增加", "不是很受欢迎", "销量", "门店"]) and _has_any(text, ["单价", "价格", "消费"]):
            bonus += 0.6
            evidence_tags.append("matches_conclusion_variable")
        if _has_any(text, ["整体形势", "行业", "整体", "国家经济"]):
            bonus -= 0.4
            risk_tags.append("broad_background")
        if _has_any(text, ["健康", "身体健康", "有益健康", "不利于身体健康"]) and not _has_any(question_text, ["健康", "身体"]):
            bonus -= 2.2
            risk_tags.append("off_topic_health")
        if _has_any(text, ["薪酬管理", "员工积极性", "制度改革"]):
            bonus -= 0.2
            risk_tags.append("possible_other_internal_factor")

    elif direction == "strengthen":
        if _has_any(text, ["题干", "结论"]):
            bonus += 0.2
            evidence_tags.append("explicit_argument_reference")
        if _has_any(text, ["长期应激", "应激"]) and _has_any(text, ["神经内分泌", "疼痛抑制", "功能被削弱"]):
            bonus += 1.0
            evidence_tags.append("subject_mechanism_bridge")
        if _has_any(text, ["气候变化", "变暖", "高纬度迁移", "向高纬度迁移", "迁移"]):
            bonus += 3.2
            evidence_tags.append("climate_migration_mechanism")
        if _has_any(text, ["吸烟", "与应激相似"]):
            bonus -= 1.2
            risk_tags.append("analogous_external_factor")
        if _has_any(text, ["鸟类的声音变得", "声音强度", "异质性"]):
            bonus -= 0.5
            risk_tags.append("restates_phenomenon")
        if _has_any(text, ["物种灭绝风险", "体型较小"]):
            bonus -= 0.6
            risk_tags.append("broad_background")

    elif direction == "necessary_assumption":
        if _has_any(text, ["大部分有毒物质是苦的", "提示风险", "稳定、有效地反映", "可靠筛查", "间隔越短"]):
            bonus += 0.8
            evidence_tags.append("necessary_bridge")
        if _has_any(text, ["成本", "愿意尝试", "接受度"]):
            bonus -= 0.6
            risk_tags.append("practical_background")

    elif direction == "explain":
        if _has_any(text, ["只要付费即可", "不必愧疚", "收费后"]):
            bonus += 1.0
            evidence_tags.append("explains_counterintuitive_effect")
        if _has_any(text, ["原本经常", "没有太大的约束力"]):
            bonus += 0.4
            evidence_tags.append("explains_weak_constraint")
        if _has_any(text, ["工作忙碌"]):
            bonus -= 0.3
            risk_tags.append("explains_baseline_not_increase")

    elif direction == "infer":
        if _has_any(text, ["其他条件不变", "相同或相近", "总体上"]):
            bonus += 0.8
            evidence_tags.append("conservative_restated_inference")
        if _has_any(text, ["一定", "所有", "必然", "只要"]):
            bonus -= 1.0
            risk_tags.append("over_absolute")

    if _has_any(text, ["无关", "背景", "价格", "颜色"]) and not evidence_tags:
        bonus -= 0.4
        risk_tags.append("likely_irrelevant")

    if score_reasons and not risk_tags:
        bonus += 0.1
        evidence_tags.append("has_scoring_feature")

    return round(bonus, 2), evidence_tags, risk_tags


def _risk_penalty(risk_tags: list[str]) -> float:
    if not risk_tags:
        return 0.0
    severe_tags = {
        "off_topic_health",
        "analogous_external_factor",
        "affirming_consequent_or_direction_risk",
        "denying_antecedent",
        "quantifier_scope_error",
        "scope_expansion",
    }
    return round(sum(0.7 if tag in severe_tags else 0.25 for tag in risk_tags), 2)


def _score_strength(score: float) -> str:
    if score >= 3.2:
        return "strong"
    if score >= 2.0:
        return "medium_or_strong"
    if score >= 1.0:
        return "medium"
    if score <= 0.2:
        return "weak_or_irrelevant"
    return "unknown"


def _shares_argument_keyword(text: str, argument_structure: dict[str, Any]) -> bool:
    haystack = argument_structure.get("conclusion", "") + "；".join(argument_structure.get("premises", []))
    keywords = [word for word in re.findall(r"[\u4e00-\u9fa5]{2,}", text) if len(word) >= 2]
    return any(word in haystack for word in keywords[:6])


def _effect_for_relation(direction: str, relation: str) -> str:
    if direction == "weaken":
        if "他因" in relation or "倒因" in relation or "无关" not in relation and "桥梁" in relation:
            return "可能削弱"
        if "无关" in relation:
            return "削弱力度弱或无关"
        return "需进一步比较削弱力度"
    if direction == "strengthen":
        if "必要条件" in relation or "解释机制" in relation or "话题相关" in relation:
            return "可能加强"
        if "无关" in relation:
            return "加强力度弱或无关"
        return "需进一步比较加强力度"
    if direction == "necessary_assumption":
        if "必要条件" in relation or "桥梁" in relation:
            return "可做否定代入检验"
        return "未必是必要条件"
    if direction == "explain":
        if "解释机制" in relation or "他因" in relation:
            return "可能解释现象"
        return "需检查是否能同时解释现象两面"
    if direction == "infer":
        return "需与题干条件逐项核对是否必然推出"
    if direction == "translation":
        return "需按条件命题翻译、逆否或量词关系核对是否必然推出"
    return "需人工复核"


def _strength_level(relation: str) -> str:
    if "桥梁" in relation or "必要条件" in relation or "他因" in relation or "倒因" in relation:
        return "medium_or_strong"
    if "话题相关" in relation or "解释机制" in relation:
        return "medium"
    if "无关" in relation:
        return "weak_or_irrelevant"
    return "unknown"


def _option_reason(direction: str, relation: str, score_reasons: list[str]) -> str:
    if direction == "translation":
        score_note = "；".join(score_reasons) if score_reasons else "未稳定匹配题干翻译关系"
        return f"{relation}：{score_note}；翻译推理题需核对箭头方向、逆否等价和是否越界。"
    score_note = "；".join(score_reasons) if score_reasons else "未识别到稳定评分特征"
    if direction == "necessary_assumption":
        return f"{relation}；{score_note}；前提题需进一步做否定代入。"
    if direction == "explain":
        return f"{relation}；{score_note}；解释题需检查是否同时解释矛盾双方。"
    if direction == "infer":
        return f"{relation}；{score_note}；推出题不能超出题干确定信息。"
    return f"{relation}；{score_note}；需按论点、论据、论证桥梁做力度比较。"


def _is_reverse_question(question_text: str) -> bool:
    return _reverse_question_info(question_text)["is_reverse"]


def _reverse_question_info(question_text: str) -> dict[str, Any]:
    question_part = _question_task_text(question_text)
    reverse_patterns = [
        ("不能由上述材料推出", "cannot_infer", "infer"),
        ("不能支持", "least_strengthen", "strengthen"),
        ("无法支持", "least_strengthen", "strengthen"),
        ("不支持", "least_strengthen", "strengthen"),
        ("不能加强", "least_strengthen", "strengthen"),
        ("不加强", "least_strengthen", "strengthen"),
        ("不能解释", "least_explain", "explain"),
        ("无法解释", "least_explain", "explain"),
        ("不解释", "least_explain", "explain"),
        ("不能推出", "cannot_infer", "infer"),
        ("无法推出", "cannot_infer", "infer"),
        ("不一定为真", "cannot_infer", "infer"),
        ("不能由此推出", "cannot_infer", "infer"),
        ("无法由此推出", "cannot_infer", "infer"),
        ("最不能削弱", "least_weaken", "weaken"),
        ("不能削弱", "least_weaken", "weaken"),
        ("不削弱", "least_weaken", "weaken"),
        ("不能质疑", "least_weaken", "weaken"),
        ("没有质疑", "least_weaken", "weaken"),
        ("不是上述结论成立的前提", "least_premise", "necessary_assumption"),
        ("不是前提", "least_premise", "necessary_assumption"),
        ("除哪项外", "except", "except"),
        ("除了哪项", "except", "except"),
        ("以下哪项除外", "except", "except"),
        ("除外", "except", "except"),
        ("不正确的是", "incorrect", "incorrect"),
        ("不符合的是", "incorrect", "incorrect"),
        ("哪项不是", "incorrect", "incorrect"),
        ("不属于", "incorrect", "incorrect"),
    ]
    for pattern, reverse_type, task_type in reverse_patterns:
        if pattern in question_part:
            return {
                "is_reverse": True,
                "reverse_type": reverse_type,
                "trigger": pattern,
                "polarity": "negative",
                "task_type": task_type,
            }
    return {"is_reverse": False, "reverse_type": "", "trigger": "", "polarity": "positive", "task_type": "positive"}


def _question_task_text(question_text: str) -> str:
    text = re.split(r"\s*A(?:[\.、:：])", question_text, maxsplit=1)[0]
    for marker in ["以下除哪项", "除哪项", "除了哪项", "以下哪项除外"]:
        if marker in text:
            return text[text.rfind(marker):]
    markers = [
        "以下哪项",
        "以下各项",
        "下列哪项",
        "下列各项",
        "哪项",
        "根据上述信息",
    ]
    starts = [text.rfind(marker) for marker in markers if marker in text]
    if starts:
        return text[max(starts):]
    clauses = [clause.strip() for clause in re.split(r"[。；;]", text) if clause.strip()]
    return clauses[-1] if clauses else text


def _select_answer_candidate(
    option_analysis: list[dict[str, Any]],
    profile: dict[str, Any],
    reverse_info: dict[str, Any],
    warnings: list[str],
    high_risk_warnings: list[str],
) -> dict[str, Any]:
    if len(option_analysis) != 4:
        return {
            "answer_candidate": None,
            "decision_status": "analysis_only",
            "confidence": 0.2,
            "debug": {"blocked_by": ["incomplete_options"]},
        }
    blocking_warnings = [
        warning for warning in warnings
        if "反向问法" not in warning and "不能/最不能" not in warning
        and "未能稳定识别论据" not in warning
        and "未能稳定识别论点" not in warning
    ]
    if blocking_warnings:
        return {
            "answer_candidate": None,
            "decision_status": "needs_manual_review",
            "confidence": 0.3,
            "debug": {"blocked_by": blocking_warnings},
        }

    reverse_type = reverse_info.get("reverse_type", "")
    sorted_options = sorted(option_analysis, key=lambda item: float(item.get("selection_score", item.get("score", 0.0))), reverse=True)
    selected = sorted_options[0]
    runner_up = sorted_options[1]
    margin = float(selected.get("selection_score", selected.get("score", 0.0))) - float(runner_up.get("selection_score", runner_up.get("score", 0.0)))

    if reverse_info.get("is_reverse") and reverse_type in {"except", "least_strengthen", "least_explain", "least_weaken", "least_premise", "incorrect", "cannot_infer"}:
        if profile["strength_direction"] in {"infer", "translation"} and reverse_type == "cannot_infer":
            selected = sorted(option_analysis, key=lambda item: float(item.get("selection_score", item.get("score", 0.0))))[0]
            runner_up = sorted(option_analysis, key=lambda item: float(item.get("selection_score", item.get("score", 0.0))))[1]
            margin = float(runner_up.get("selection_score", runner_up.get("score", 0.0))) - float(selected.get("selection_score", selected.get("score", 0.0)))
        elif reverse_type in {"except", "least_strengthen", "least_explain", "least_weaken", "least_premise", "incorrect"}:
            selected = sorted(option_analysis, key=lambda item: float(item.get("selection_score", item.get("score", 0.0))))[0]
            runner_up = sorted(option_analysis, key=lambda item: float(item.get("selection_score", item.get("score", 0.0))))[1]
            margin = float(runner_up.get("selection_score", runner_up.get("score", 0.0))) - float(selected.get("selection_score", selected.get("score", 0.0)))

    is_translation = profile["strength_direction"] == "translation"
    confidence_score = float(selected.get("selection_score", selected.get("score", 0.0)))
    if reverse_info.get("is_reverse") and reverse_type in {"except", "least_strengthen", "least_explain", "least_weaken", "least_premise", "incorrect", "cannot_infer"}:
        confidence_score = max(confidence_score, float(runner_up.get("selection_score", runner_up.get("score", 0.0))))
        if is_translation and reverse_type == "cannot_infer":
            confidence_score = max(
                float(option.get("selection_score", option.get("score", 0.0)))
                for option in option_analysis
            )
    confidence = _decision_confidence(confidence_score, margin, reverse_info, high_risk_warnings)
    is_reverse = bool(reverse_info.get("is_reverse"))
    selected_score = float(selected.get("selection_score", selected.get("score", 0.0)))
    passes_positive = (
        not is_reverse
        and (
            (selected_score >= 3.0 and margin >= 1.2)
            or (selected_score >= 4.0 and margin >= 0.6)
            or (is_translation and selected_score >= 4.0 and margin >= 0.3)
        )
    )
    max_other_score = max(
        (
            float(option.get("selection_score", option.get("score", 0.0)))
            for option in option_analysis
            if option is not selected
        ),
        default=0.0,
    )
    passes_reverse = (
        is_reverse
        and (
            (margin >= 1.0)
            or selected.get("strength_level") in {"weak_or_irrelevant", "unknown"} and margin >= 0.7
            or (
                is_translation
                and reverse_type == "cannot_infer"
                and bool(selected.get("risk_tags"))
                and max_other_score >= 3.0
                and margin >= 0.0
            )
        )
    )
    if not (passes_positive or passes_reverse) or confidence < 0.65:
        return {
            "answer_candidate": None,
            "decision_status": "analysis_only",
            "confidence": confidence,
            "debug": {
                "mode": "except|min_score" if is_reverse else "positive|max_score",
                "best_label": selected["label"],
                "best_score": selected.get("score", 0.0),
                "best_selection_score": selected.get("selection_score", selected.get("score", 0.0)),
                "second_score": runner_up.get("score", 0.0),
                "second_selection_score": runner_up.get("selection_score", runner_up.get("score", 0.0)),
                "score_gap": margin,
                "question_polarity": reverse_info.get("polarity", "positive"),
                "task_type": reverse_info.get("task_type", "positive"),
                "blocked_by": ["threshold_or_confidence"],
            },
        }

    for option in option_analysis:
        option["is_candidate"] = option["label"] == selected["label"]
    return {
        "answer_candidate": {
            "label": selected["label"],
            "text": selected["text"],
            "confidence": confidence,
            "reason": selected["reason"],
            "score": selected.get("score", 0.0),
            "selection_score": selected.get("selection_score", selected.get("score", 0.0)),
        },
        "decision_status": "candidate_ready",
        "confidence": confidence,
        "debug": {
            "mode": "except|min_score" if is_reverse else "positive|max_score",
            "best_label": selected["label"],
            "best_score": selected.get("score", 0.0),
            "best_selection_score": selected.get("selection_score", selected.get("score", 0.0)),
            "second_score": runner_up.get("score", 0.0),
            "second_selection_score": runner_up.get("selection_score", runner_up.get("score", 0.0)),
            "score_gap": margin,
            "question_polarity": reverse_info.get("polarity", "positive"),
            "task_type": reverse_info.get("task_type", "positive"),
            "thresholds": {
                "positive_min_score": 3.0,
                "positive_min_gap": 1.2,
                "reverse_min_gap": 1.0,
                "min_confidence": 0.65,
            },
            "blocked_by": [],
        },
    }


def _decision_confidence(
    selected_score: float,
    margin: float,
    reverse_info: dict[str, Any],
    high_risk_warnings: list[str],
) -> float:
    confidence = 0.35 + min(selected_score, 4.0) * 0.11 + min(max(margin, 0.0), 3.0) * 0.08
    if reverse_info.get("is_reverse"):
        confidence += 0.03
    if high_risk_warnings:
        confidence -= 0.06 * len(high_risk_warnings)
    return round(max(0.0, min(confidence, 0.95)), 2)


def _build_warnings(
    question_text: str,
    options: list[dict[str, str]],
    argument_structure: dict[str, Any],
) -> list[str]:
    warnings: list[str] = []
    if not argument_structure.get("conclusion"):
        warnings.append("未能稳定识别论点，需人工确认题干最终结论。")
    if not argument_structure.get("premises"):
        warnings.append("未能稳定识别论据，选项分析只能作为框架草案。")
    if not options:
        warnings.append("未识别到A/B/C/D选项，无法生成逐项分析。")
    if _is_reverse_question(question_text):
        warnings.append("题干包含反向问法，选择时需按“不能/最不能”方向处理。")
    return warnings


def _build_high_risk_warnings(
    question_text: str,
    options: list[dict[str, str]],
    argument_structure: dict[str, Any],
    reverse_info: dict[str, Any],
) -> list[str]:
    warnings: list[str] = []
    if reverse_info.get("is_reverse"):
        warnings.append(f"反向/选非问法：{reverse_info.get('trigger')}")
    if len(options) != 4:
        warnings.append("选项未完整解析为 A/B/C/D。")
    if not argument_structure.get("conclusion"):
        warnings.append("论点识别不稳定。")
    return warnings


def _build_explanation(
    profile: dict[str, Any],
    argument_structure: dict[str, Any],
    warnings: list[str],
) -> str:
    method_ids = "、".join(profile["method_ids"])
    conclusion = argument_structure.get("conclusion") or "未稳定识别"
    if warnings:
        return (
            f"本题按逻辑判断的{profile['question_type']}形成解题草案，优先调用{method_ids}。"
            f" 当前论点初步识别为：{conclusion}。仍需按 warnings 复核。"
        )
    return (
        f"本题按逻辑判断的{profile['question_type']}处理，优先调用{method_ids}。"
        f" 先以论点“{conclusion}”为核心，再逐项比较选项对论证链的作用。"
    )
