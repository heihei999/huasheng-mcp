from __future__ import annotations

from pathlib import Path
from typing import Any

from .kb import (
    get_method_card as kb_get_method_card,
    get_source_reference as kb_get_source_reference,
    search_method_matches,
)
from .router import classify_question as route_classify_question
from .scaffolds.graphic_reasoning_scaffold import build_graphic_reasoning_scaffold
from .scaffolds.definition_judgement_scaffold import build_definition_judgement_scaffold
from .scaffolds.analogy_reasoning_scaffold import build_analogy_reasoning_scaffold
from .scaffolds.logic_analysis_scaffold import build_logic_analysis_scaffold
from .scaffolds.quantity_relation_scaffold import build_quantity_relation_scaffold
from .scaffolds.verbal_reasoning_scaffold import build_verbal_reasoning_scaffold
from .solvers import (
    solve_data_analysis as solve_data_analysis_draft,
    solve_logic_reasoning as solve_logic_reasoning_draft,
)


def tool_get_method_card(
    method_id: str, kb_dir: str | Path | None = None
) -> dict[str, Any]:
    return {
        "method_id": method_id,
        "card": kb_get_method_card(method_id, kb_dir),
    }


def tool_search_methods(
    query: str,
    module: str | None = None,
    top_k: int = 5,
    kb_dir: str | Path | None = None,
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for match in search_method_matches(query, module=module, top_k=top_k, kb_dir=kb_dir):
        card = match["card"]
        results.append(
            {
                "method_id": card.get("id"),
                "method_name": card.get("method_name"),
                "module": card.get("module"),
                "question_type": card.get("question_type"),
                "score": float(match["score"]),
                "need_review": card.get("need_review", False),
            }
        )
    return {"query": query, "results": results}


def tool_classify_question(
    question_text: str,
    top_k: int = 5,
    kb_dir: str | Path | None = None,
) -> dict[str, Any]:
    matches = []
    for match in route_classify_question(question_text, kb_dir=kb_dir, top_k=top_k):
        matches.append(
            {
                "module": match.get("module"),
                "question_type": match.get("question_type"),
                "sub_type": match.get("sub_type"),
                "priority_method_id": match.get("priority_method_id"),
                "matched_triggers": match.get("matched_triggers", []),
            }
        )
    return {"matches": matches}


def tool_get_source_reference(
    method_id: str, kb_dir: str | Path | None = None
) -> dict[str, Any]:
    reference = kb_get_source_reference(method_id, kb_dir) or {}
    return {
        "method_id": method_id,
        "source_file": reference.get("source_file", []),
        "source_page": reference.get("source_page", []),
        "confidence": reference.get("confidence", 0.0),
        "need_review": reference.get("need_review", False),
    }


def tool_solve_data_analysis(
    question_text: str,
    options: list[str] | dict[str, str] | None = None,
    kb_dir: str | Path | None = None,
) -> dict[str, Any]:
    return solve_data_analysis_draft(question_text, options=options, kb_dir=kb_dir)


def tool_solve_logic_reasoning(
    question_text: str,
    options: dict[str, str] | list[str] | None = None,
    kb_dir: str | Path | None = None,
) -> dict[str, Any]:
    return solve_logic_reasoning_draft(question_text, options=options, kb_dir=kb_dir)


# ── Guidance-only scaffold tools (read-only, no solving) ──────────────


def tool_get_graphic_reasoning_scaffold() -> dict[str, Any]:
    return build_graphic_reasoning_scaffold()


def tool_get_definition_judgement_scaffold() -> dict[str, Any]:
    return build_definition_judgement_scaffold()


def tool_get_analogy_reasoning_scaffold() -> dict[str, Any]:
    return build_analogy_reasoning_scaffold()


def tool_get_logic_analysis_scaffold() -> dict[str, Any]:
    return build_logic_analysis_scaffold()


def tool_get_quantity_relation_scaffold() -> dict[str, Any]:
    return build_quantity_relation_scaffold()


def tool_get_verbal_reasoning_scaffold() -> dict[str, Any]:
    return build_verbal_reasoning_scaffold()


# ── Route-only question router (no solving, no answer) ───────────────

_VALID_HINTS = {
    "data_analysis", "logic_reasoning", "graphic_reasoning",
    "definition_judgement", "analogy_reasoning", "logic_analysis",
    "quantity_relation", "verbal_reasoning",
}

# ── Module hint alias normalization (v0.5.0) ──────────────────────────
_MODULE_HINT_ALIASES: dict[str, str] = {
    # Chinese section names
    "图形推理": "graphic_reasoning",
    "定义判断": "definition_judgement",
    "类比推理": "analogy_reasoning",
    "逻辑判断": "logic_reasoning",
    "分析推理": "logic_analysis",
    "排列组合式逻辑": "logic_analysis",
    "资料分析": "data_analysis",
    "数量关系": "quantity_relation",
    "言语理解": "verbal_reasoning",
    "言语理解与表达": "verbal_reasoning",
    # Section prefix variants: "判断推理-图形推理" etc.
    "判断推理-图形推理": "graphic_reasoning",
    "判断推理-定义判断": "definition_judgement",
    "判断推理-类比推理": "analogy_reasoning",
    "判断推理-逻辑判断": "logic_reasoning",
    # English module names (already canonical)
    "graphic_reasoning": "graphic_reasoning",
    "definition_judgement": "definition_judgement",
    "analogy_reasoning": "analogy_reasoning",
    "logic_reasoning": "logic_reasoning",
    "logic_analysis": "logic_analysis",
    "data_analysis": "data_analysis",
    "quantity_relation": "quantity_relation",
    "verbal_reasoning": "verbal_reasoning",
}


def _normalize_module_hint(
    module_hint: str | None,
    section_context: str | None = None,
) -> str | None:
    """Normalize module_hint / section_context to a canonical module name.

    Supports Chinese section names (e.g. "类比推理"), prefixed variants
    (e.g. "判断推理-类比推理"), and canonical English names.
    Returns None if neither input resolves to a valid module.
    """
    raw = (module_hint or "").strip()
    if not raw:
        raw = (section_context or "").strip()
    if not raw:
        return None
    # Direct alias lookup
    if raw in _MODULE_HINT_ALIASES:
        return _MODULE_HINT_ALIASES[raw]
    # Case-insensitive fallback for English names
    lower = raw.lower()
    if lower in _MODULE_HINT_ALIASES:
        return _MODULE_HINT_ALIASES[lower]
    # Try stripping prefix like "判断推理-" or "第四部分 "
    for sep in ["-", "—", " "]:
        if sep in raw:
            tail = raw.rsplit(sep, 1)[-1].strip()
            if tail in _MODULE_HINT_ALIASES:
                return _MODULE_HINT_ALIASES[tail]
    return None

# ── Data material strong signals (v0.4.2) ─────────────────────────────
# These keywords indicate the question explicitly references table/chart/material
# and should route to data_analysis even if quantity keywords are present.
_DATA_MATERIAL_STRONG_KW = [
    "表中", "表格", "根据表格", "根据下表", "下表", "上表", "统计表",
    "统计图", "统计图表", "图表", "根据图表", "图中数据", "图表数据",
    "折线图", "柱状图", "条形图", "饼状图",
    "材料显示", "根据材料", "上述材料", "上述资料", "根据上述资料", "资料显示",
]


def _has_data_material_signal(text: str) -> bool:
    """Return True when the question explicitly references table/chart/material/data context."""
    return any(kw in text for kw in _DATA_MATERIAL_STRONG_KW)

_SCAFFOLD_TOOLS = {
    "graphic_reasoning": "get_graphic_reasoning_scaffold",
    "definition_judgement": "get_definition_judgement_scaffold",
    "analogy_reasoning": "get_analogy_reasoning_scaffold",
    "logic_analysis": "get_logic_analysis_scaffold",
    "quantity_relation": "get_quantity_relation_scaffold",
    "verbal_reasoning": "get_verbal_reasoning_scaffold",
}


def tool_route_xingce_question(
    question_text: str,
    options: dict[str, str] | None = None,
    module_hint: str | None = None,
    section_context: str | None = None,
    image_present: bool = False,
    strict_mode: bool = True,
) -> dict[str, Any]:
    """Route a question to the recommended track without solving."""
    return _route_xingce_question_core(
        question_text=question_text,
        options=options,
        module_hint=module_hint,
        section_context=section_context,
        image_present=image_present,
        strict_mode=strict_mode,
    )


def _route_xingce_question_core(
    question_text: str,
    options: dict[str, str] | None = None,
    module_hint: str | None = None,
    section_context: str | None = None,
    image_present: bool = False,
    strict_mode: bool = True,
) -> dict[str, Any]:
    """Core routing logic shared by route and compose tools."""
    signals: list[str] = []
    warnings: list[str] = []
    module_guess = "unknown"
    confidence = "low"
    recommended_tool: str | None = None

    text = (question_text or "").strip()
    options_text = " ".join((options or {}).values()) if options else ""
    combined = text + " " + options_text

    # ── v0.5.0: normalize module_hint / section_context ─────────────
    normalized_hint = _normalize_module_hint(module_hint, section_context)
    module_hint_applied = False
    module_hint_conflict = False
    heuristic_module_guess: str | None = None

    # ── insufficient signal detection (strict_mode only) ─────────────
    def _make_uncertain_return(signals: list[str], warnings: list[str]) -> dict[str, Any]:
        """Helper to build route_uncertain return with v0.3 + v0.5.0 fields."""
        return {
            "mode": "route_only",
            "module_guess": "unknown",
            "confidence": "unknown",
            "recommended_track": "route_uncertain",
            "recommended_tool": None,
            "reasoning_signals": signals,
            "fallback_policy": "analysis_only_if_uncertain",
            "answer_policy": "do_not_answer_inside_router",
            "warnings": warnings,
            "possible_modules": [],
            "model_review_required": True,
            "override_allowed": True,
            "review_instruction": (
                "MCP route is advisory. Review the full question semantics "
                "before selecting a scaffold. If semantic evidence conflicts "
                "with the route, override it and explain why."
            ),
            "conflict_signals": [],
            # v0.5.0: module context override fields
            "module_hint": normalized_hint,
            "section_context": (section_context or "").strip() or None,
            "module_hint_applied": False,
            "module_hint_conflict": False,
            "heuristic_module_guess": None,
        }

    if strict_mode:
        _insufficient_phrases = [
            "条件不足", "信息不足", "题干不足", "看不出来",
            "无法判断", "不确定", "缺少选项", "缺少图片",
            "无明显题型信号", "不知道", "不清楚", "不明白",
        ]

        has_insufficient_phrase = any(phrase in text for phrase in _insufficient_phrases)
        is_too_short = len(text) < 4 and not image_present
        is_empty_or_blank = len(text) == 0
        has_no_options_no_signal = (not options or len(options) == 0) and len(text) < 8 and not image_present

        if is_empty_or_blank:
            signals.append("empty_question_text")
            warnings.append("insufficient_question_signal")
            return _make_uncertain_return(signals, warnings)

        if has_insufficient_phrase:
            if normalized_hint:
                # v0.5.1: valid module_hint overrides insufficient phrase
                signals.append("insufficient_phrase_detected")
                warnings.append("short_question_overridden_by_module_hint")
            else:
                signals.append("insufficient_phrase_detected")
                warnings.append("route_uncertain_due_to_insufficient_signal")
                return _make_uncertain_return(signals, warnings)

        if is_too_short and not normalized_hint and not image_present:
            signals.append("text_too_short")
            warnings.append("insufficient_question_signal")
            return _make_uncertain_return(signals, warnings)

        if has_no_options_no_signal and not normalized_hint:
            signals.append("no_options_no_strong_signal")
            warnings.append("route_uncertain_due_to_insufficient_signal")
            return _make_uncertain_return(signals, warnings)

    # ── conflict signal detection (for model review) ─────────────────
    conflict_signals: list[str] = []

    # Sentence ordering pattern: "重新排列"/"语序正确" → verbal, not quantity
    _sentence_order_patterns = ["重新排列", "语序正确", "语序恰当", "排列成语",
                                "排列句子", "句子排序", "句子排列"]
    has_sentence_order = any(p in text for p in _sentence_order_patterns)

    # Sentence insertion pattern: "填入文中哪个位置" → verbal, not logic_analysis
    _sentence_insertion_patterns = ["填入文中", "填入文中哪个位置", "最合适的位置",
                                    "填入哪个位置", "应填入", "插入文中"]
    has_sentence_insertion = any(p in text for p in _sentence_insertion_patterns)

    # Main idea pattern: "主要介绍/讲/说明"
    _main_idea_patterns = ["主要介绍", "主要讲", "主要说明", "主要论述",
                           "主要阐述", "主要分析", "主要探讨"]
    has_main_idea = any(p in text for p in _main_idea_patterns)

    # Data analysis extended signals (without "资料" prefix)
    _da_extended_patterns = ["占全国", "比重", "同比增长", "同比增长率",
                             "环比增长", "上述资料", "根据资料", "根据上述",
                             "能够从上述资料中推出", "占……的比重"]
    has_da_extended = any(p in text for p in _da_extended_patterns)

    # ── analogy reasoning (check before graphic to avoid "规律" false positive) ─
    has_analogy_structure = False
    if module_guess == "unknown":
        # Support ：, :, and ∶ (Chinese ratio symbol)
        _analogy_separators = ["：", ":", "∶"]
        for _sep in _analogy_separators:
            if _sep in text:
                parts = text.split(_sep)
                # Support 2 or 3 part analogy (e.g., "卫冕∶夺冠" or "酒器∶尊∶爵")
                if 2 <= len(parts) <= 3 and all(len(p.strip()) <= 8 for p in parts):
                    has_analogy_structure = True
                    break
        if has_analogy_structure and options:
            analogy_opts = sum(1 for v in options.values()
                              if any(s in v for s in _analogy_separators))
            if analogy_opts >= 2:
                signals.append("analogy_structure")
                module_guess = "analogy_reasoning"
                confidence = "high"
                conflict_signals.append("analogy_symbol_detected")

    # ── graphic reasoning ────────────────────────────────────────────
    if image_present:
        signals.append("image_present=true")
        module_guess = "graphic_reasoning"
        confidence = "high"

    # Strong graphic signals (should always route to graphic_reasoning)
    graphic_strong_kw = ["图形", "图形推理", "选择最合适的一项",
                         "折叠", "展开", "截面", "三视图", "拼合",
                         "展开图", "纸盒", "立体图形", "问号处"]
    # Weak graphic signals (方位词, may conflict with logic_analysis)
    graphic_weak_kw = ["左边", "右边", "规律"]

    has_graphic_strong = any(kw in combined for kw in graphic_strong_kw)
    has_graphic_weak = any(kw in combined for kw in graphic_weak_kw)

    # ── logic analysis (person arrangement with direction words) ───
    # Check BEFORE weak graphic signals to avoid "左边/右边" false positive
    # Person/object arrangement strong signals
    la_arrangement_person_kw = ["甲", "乙", "丙", "丁",
                                "小王", "小李", "小张", "小赵",
                                "张", "王", "李", "杨"]
    la_arrangement_position_kw = ["排成一排", "排列", "座位", "坐在", "站在",
                                  "相邻", "不相邻", "两端", "中间",
                                  "位置", "顺序"]
    la_arrangement_condition_kw = ["条件", "可能正确", "一定正确",
                                   "不可能", "至少", "至多",
                                   "左边", "右边", "前面", "后面"]

    has_arrangement_person = any(kw in combined for kw in la_arrangement_person_kw)
    has_arrangement_position = any(kw in combined for kw in la_arrangement_position_kw)
    has_arrangement_condition = any(kw in combined for kw in la_arrangement_condition_kw)

    # Strong arrangement: person + position signals
    has_strong_arrangement = has_arrangement_person and has_arrangement_position
    # Medium arrangement: person + condition signals (includes 左边/右边 in logic context)
    has_medium_arrangement = has_arrangement_person and has_arrangement_condition

    if module_guess == "unknown" and (has_strong_arrangement or has_medium_arrangement):
        signals.append("logic_arrangement_signals")
        module_guess = "logic_analysis"
        confidence = "high"

    # Text-based arrangement objects (books, programs, contestants, courses, etc.)
    # Must have BOTH object AND order/position signals to avoid false positives
    _arrangement_object_kw = [
        "书", "语文书", "数学书", "英语书", "课本",
        "节目", "舞蹈", "合唱", "小品", "歌曲",
        "选手", "队员", "学生", "老师", "选手",
        "课程", "会议", "车辆", "部门", "盒子",
    ]
    _arrangement_order_kw = [
        "从左到右", "从右到左", "从高到低", "从低到高",
        "依次", "顺序", "出场", "演出", "摆放", "排列", "安排",
        "可能为真", "可能正确", "一定为真", "一定正确",
        "早于", "晚于", "之前", "之后",
    ]

    has_arrangement_object = any(kw in combined for kw in _arrangement_object_kw)
    has_arrangement_order = any(kw in combined for kw in _arrangement_order_kw)

    # Text arrangement: object + order signals AND has direction/position context
    _text_arrangement_position_kw = ["左边", "右边", "最左边", "最右边",
                                     "前面", "后面", "相邻", "不相邻",
                                     "两端", "中间", "位置"]
    has_text_arrangement_position = any(kw in combined for kw in _text_arrangement_position_kw)
    has_text_arrangement = (has_arrangement_object and has_arrangement_order and
                           has_text_arrangement_position)

    if module_guess == "unknown" and has_text_arrangement:
        signals.append("text_arrangement_signals")
        module_guess = "logic_analysis"
        confidence = "high"

    # Now check graphic reasoning
    if module_guess == "unknown" and has_graphic_strong:
        signals.append("graphic_strong_keywords")
        module_guess = "graphic_reasoning"
        confidence = "high"
    elif module_guess == "unknown" and has_graphic_weak:
        signals.append("graphic_keywords")
        module_guess = "graphic_reasoning"
        confidence = "high"

    # ── definition judgement ─────────────────────────────────────────
    def_kw = ["定义", "符合上述定义", "不符合上述定义", "属于", "不属于",
              "以下属于", "以下不属于"]

    # Definition intro + question pattern: "所谓...是指...下列/体现"
    _definition_intro_kw = ["所谓", "是指", "指的是", "定义为", "是指在", "指在",
                            "概念", "定义", "称为"]
    _definition_question_kw = ["下列", "以下", "哪项", "属于", "不属于",
                               "符合", "不符合", "体现", "没有体现",
                               "最符合", "最不符合"]
    has_definition_intro = any(kw in text for kw in _definition_intro_kw)
    has_definition_question = any(kw in text for kw in _definition_question_kw)

    if module_guess == "unknown" and any(kw in combined for kw in def_kw):
        signals.append("definition_keywords")
        module_guess = "definition_judgement"
        confidence = "high"
    elif module_guess == "unknown" and has_definition_intro and has_definition_question:
        signals.append("definition_intro_question_pattern")
        module_guess = "definition_judgement"
        confidence = "high"

    # ── verbal reasoning (check before quantity for priority) ────────
    # Sentence ordering: "重新排列"/"语序正确" → verbal_reasoning
    if module_guess == "unknown" and has_sentence_order:
        signals.append("sentence_order_pattern")
        module_guess = "verbal_reasoning"
        confidence = "high"
        conflict_signals.append("contains_排列_but_sentence_order_pattern")

    # Sentence insertion: "填入文中哪个位置" → verbal_reasoning
    if module_guess == "unknown" and has_sentence_insertion:
        signals.append("sentence_insertion_pattern")
        module_guess = "verbal_reasoning"
        confidence = "high"
        conflict_signals.append("contains_位置_but_sentence_insertion_pattern")

    # Main idea pattern → verbal_reasoning
    if module_guess == "unknown" and has_main_idea:
        signals.append("main_idea_pattern")
        module_guess = "verbal_reasoning"
        confidence = "high"

    # ── data analysis (check before quantity to avoid "多少" overlap) ─
    da_kw = ["资料", "材料", "同比", "环比", "增长率", "比重",
             "百分点", "统计"]
    if module_guess == "unknown" and any(kw in combined for kw in da_kw):
        signals.append("data_analysis_keywords")
        module_guess = "data_analysis"
        confidence = "high"

    # Data analysis extended patterns (without "资料" prefix)
    # Check before logic_reasoning to avoid "推出" false positive
    if module_guess == "unknown" and has_da_extended:
        signals.append("data_analysis_extended_pattern")
        module_guess = "data_analysis"
        confidence = "medium"

    # Data material strong signals (v0.4.2): "表中/表格/图表/材料/资料/图中数据"
    # These should route to data_analysis even if quantity keywords are present
    # Check before quantity_relation to prevent "表中...增长量" being misrouted
    if module_guess == "unknown" and _has_data_material_signal(combined):
        signals.append("data_material_strong_signal")
        module_guess = "data_analysis"
        confidence = "high"

    # ── logic reasoning (argument) ───────────────────────────────────
    lr_kw = ["支持", "加强", "削弱", "质疑", "前提", "假设", "结论",
             "推出", "可以推出", "不能推出", "必然为真", "最能解释",
             "以下哪项为真", "以下哪项不为真"]
    if module_guess == "unknown" and any(kw in combined for kw in lr_kw):
        signals.append("logic_reasoning_keywords")
        module_guess = "logic_reasoning"
        confidence = "high"

    # ── logic analysis (requires stronger structural signals) ────────
    la_strong_kw = ["甲乙丙", "甲乙丙丁", "真假", "命题",
                    "如果那么", "只有才", "除非否则", "谁说真话", "谁说假话",
                    "条件组合", "逻辑推理"]
    la_structure_kw = ["条件", "甲", "乙", "丙", "丁"]
    # Person-month-city arrangement signals
    la_person_kw = ["张", "王", "李", "杨", "甲", "乙", "丙", "丁"]
    la_time_kw = ["月", "1月", "2月", "3月", "4月", "5月", "6月",
                  "每月", "每个月", "周", "每周"]
    la_place_kw = ["城市", "上海", "苏州", "杭州", "南京", "北京", "广州",
                   "地点", "调研"]
    la_arrange_kw = ["安排", "排布", "对应", "均不同", "不同", "不可能",
                     "一定", "至少", "至多"]

    if module_guess == "unknown":
        has_strong_la = any(kw in combined for kw in la_strong_kw)
        # Need at least 3 structure keywords to avoid false positive
        # (e.g., "甲乙" alone is common in quantity problems)
        structure_count = sum(1 for kw in la_structure_kw if kw in combined)
        has_structure_la = structure_count >= 3 and "条件" in combined

        # Person-month-city arrangement detection
        has_person = any(kw in combined for kw in la_person_kw)
        has_time = any(kw in combined for kw in la_time_kw)
        has_place = any(kw in combined for kw in la_place_kw)
        has_arrange = any(kw in combined for kw in la_arrange_kw)
        has_arrangement = has_person and (has_time or has_place) and has_arrange

        if has_strong_la or has_structure_la or has_arrangement:
            signals.append("logic_analysis_keywords")
            module_guess = "logic_analysis"
            confidence = "high"

    # ── quantity relation ────────────────────────────────────────────
    qr_kw = ["多少", "几人", "几天", "几小时", "工程", "速度", "路程", "利润", "浓度",
             "组合", "概率", "至少", "最多", "余数", "倍数",
             "甲乙", "相遇", "追及"]
    # Economic/proportion keywords (require number context to avoid false positive)
    qr_econ_kw = ["收入", "支出", "盈余", "成本", "万元", "元",
                  "上半年", "下半年", "全年", "比例", "百分比",
                  "比去年", "比上年", "增长", "下降"]
    has_qr_basic = any(kw in combined for kw in qr_kw)
    has_qr_econ = any(kw in combined for kw in qr_econ_kw)
    # Economic keywords need number context
    _has_number = any(c.isdigit() for c in combined)
    if module_guess == "unknown" and (has_qr_basic or (has_qr_econ and _has_number)):
        signals.append("quantity_keywords")
        module_guess = "quantity_relation"
        confidence = "high"

    # ── verbal reasoning (general keywords) ──────────────────────────
    vr_kw = ["主旨", "意在说明", "中心", "标题", "下文", "填入",
             "词语", "成语", "语句", "文段", "作者意图", "以下说法正确",
             "以下说法不正确"]
    if module_guess == "unknown" and any(kw in combined for kw in vr_kw):
        signals.append("verbal_keywords")
        module_guess = "verbal_reasoning"
        confidence = "high"

    # ── v0.5.0: module_hint override (after heuristic, before return) ─
    # Save heuristic result for conflict reporting
    heuristic_module_guess = module_guess

    # Strong material signals ("表中/根据表格/图中数据/上述资料") always
    # force data_analysis regardless of module_hint — safety gate.
    # v0.5.1: When module_hint is present, only check question text (not options)
    # to avoid distractor options like "折线图/柱状图" overriding definition_judgement.
    _material_check_text = text if normalized_hint else combined
    if normalized_hint and _has_data_material_signal(_material_check_text):
        # Strong material signal detected in question text: override hint for safety
        if module_guess != "data_analysis":
            signals.append("data_material_strong_signal_overrides_hint")
            module_guess = "data_analysis"
            confidence = "high"
        module_hint_applied = False
        if normalized_hint != "data_analysis":
            warnings.append(
                f"module_hint '{normalized_hint}' overridden by strong "
                f"material signal; routed to data_analysis"
            )
            module_hint_conflict = True
    elif normalized_hint:
        # module_hint takes priority over weak keyword routing
        if module_guess == "unknown":
            signals.append(f"module_hint_override={normalized_hint}")
            module_guess = normalized_hint
            confidence = "high"
            module_hint_applied = True
        elif module_guess == normalized_hint:
            signals.append(f"module_hint_confirms={normalized_hint}")
            confidence = "high"
            module_hint_applied = True
        else:
            # Conflict: hint overrides heuristic keyword route
            signals.append(f"module_hint_override={normalized_hint}")
            warnings.append(
                f"module_hint '{normalized_hint}' overrides heuristic "
                f"route '{module_guess}'"
            )
            module_guess = normalized_hint
            confidence = "high"
            module_hint_applied = True
            module_hint_conflict = True

    # ── recommended track & tool ─────────────────────────────────────
    if module_guess in _SCAFFOLD_TOOLS:
        recommended_track = "scaffold_guidance"
        recommended_tool = _SCAFFOLD_TOOLS[module_guess]
    elif module_guess in ("data_analysis", "logic_reasoning"):
        recommended_track = "solver_candidate"
        recommended_tool = None
        warnings.append(
            f"route only; solver not called in MCP route tool for {module_guess}"
        )
    elif module_guess == "unknown":
        recommended_track = "route_uncertain"
        recommended_tool = None
        confidence = "unknown"
    else:
        recommended_track = "route_uncertain"
        recommended_tool = None

    if not signals:
        signals.append("no_strong_signal")

    # ── build possible_modules for model review ─────────────────────
    possible_modules: list[dict[str, Any]] = []

    # Always add the primary guess
    if module_guess != "unknown":
        possible_modules.append({
            "module": module_guess,
            "reason": signals[0] if signals else "primary_guess",
            "priority": "primary",
        })

    # Add conflicting candidates if conflict signals exist
    if has_sentence_order and module_guess != "verbal_reasoning":
        possible_modules.append({
            "module": "verbal_reasoning",
            "reason": "sentence_order_pattern_detected",
            "priority": "conflict_candidate",
        })
    if has_sentence_insertion and module_guess != "verbal_reasoning":
        possible_modules.append({
            "module": "verbal_reasoning",
            "reason": "sentence_insertion_pattern_detected",
            "priority": "conflict_candidate",
        })
    if has_main_idea and module_guess != "verbal_reasoning":
        possible_modules.append({
            "module": "verbal_reasoning",
            "reason": "main_idea_pattern_detected",
            "priority": "conflict_candidate",
        })
    if has_da_extended and module_guess != "data_analysis":
        possible_modules.append({
            "module": "data_analysis",
            "reason": "data_analysis_extended_pattern_detected",
            "priority": "conflict_candidate",
        })

    # ── model review settings ───────────────────────────────────────
    # model_review_required: true for medium/unknown/uncertain/conflict
    model_review_required = (
        confidence in ("medium", "unknown")
        or recommended_track == "route_uncertain"
        or len(conflict_signals) > 0
    )

    # override_allowed: always true to let Claude use semantic judgment
    override_allowed = True

    # review_instruction: always provide advisory guidance
    review_instruction = (
        "MCP route is advisory. Review the full question semantics "
        "before selecting a scaffold. If semantic evidence conflicts "
        "with the route, override it and explain why."
    )

    return {
        "mode": "route_only",
        "module_guess": module_guess,
        "confidence": confidence,
        "recommended_track": recommended_track,
        "recommended_tool": recommended_tool,
        "reasoning_signals": signals,
        "fallback_policy": "analysis_only_if_uncertain",
        "answer_policy": "do_not_answer_inside_router",
        "warnings": warnings,
        "possible_modules": possible_modules,
        "model_review_required": model_review_required,
        "override_allowed": override_allowed,
        "review_instruction": review_instruction,
        "conflict_signals": conflict_signals,
        # v0.5.0: module context override fields
        "module_hint": normalized_hint,
        "section_context": (section_context or "").strip() or None,
        "module_hint_applied": module_hint_applied,
        "module_hint_conflict": module_hint_conflict,
        "heuristic_module_guess": heuristic_module_guess,
    }


# ── Prompt-composition tool (no solving, no answer) ──────────────────

_MODULE_NAMES = {
    "graphic_reasoning": "图形推理",
    "definition_judgement": "定义判断",
    "analogy_reasoning": "类比推理",
    "logic_reasoning": "逻辑判断",
    "logic_analysis": "分析推理",
    "quantity_relation": "数量关系",
    "verbal_reasoning": "言语理解",
    "data_analysis": "资料分析",
    "unknown": "未知模块",
}


def tool_compose_xingce_analysis_prompt(
    question_text: str,
    options: dict[str, str] | None = None,
    module_hint: str | None = None,
    section_context: str | None = None,
    image_present: bool = False,
    strict_mode: bool = True,
    include_scaffold_summary: bool = True,
) -> dict[str, Any]:
    """Compose a structured analysis prompt without solving."""
    route = _route_xingce_question_core(
        question_text=question_text,
        options=options,
        module_hint=module_hint,
        section_context=section_context,
        image_present=image_present,
        strict_mode=strict_mode,
    )
    warnings: list[str] = list(route.get("warnings", []))
    module_guess = route["module_guess"]
    recommended_track = route["recommended_track"]
    recommended_tool = route["recommended_tool"]
    module_cn = _MODULE_NAMES.get(module_guess, "未知模块")

    # ── build prompt_text ─────────────────────────────────────────────
    parts: list[str] = []

    # section 0: model review notice (v0.3)
    parts.append(
        "## ⚠️ 题型复核提示\n"
        "MCP route is advisory, not final.\n"
        "First review the question type using the full question text and options.\n"
        "If the MCP route conflicts with semantic evidence, override it.\n"
        "If overriding, explicitly state:\n"
        "  - original MCP module_guess\n"
        "  - corrected module\n"
        "  - reason for override\n"
        "Then use the corresponding scaffold or reasoning strategy.\n"
        "Do not output answer unless the conclusion is unique.\n"
        "If not unique, return analysis_only.\n"
        "Do not invent missing visual/table content."
    )

    # section 1: question summary
    opt_str = ""
    if options:
        opt_str = "\n".join(f"  {k}. {v}" for k, v in options.items())
    opt_section = ("选项:\n" + opt_str) if opt_str else ""
    img_tag = "[含图片]" if image_present else ""
    parts.append(
        "## 题目输入摘要\n"
        f"模块猜测: {module_cn} ({module_guess})\n"
        f"置信度: {route['confidence']}\n"
        f"题干: {question_text[:200] if question_text else '(空)'}\n"
        f"{opt_section}\n"
        f"{img_tag}"
    )

    # section 2: route result (v0.3: include new fields)
    possible_modules_str = ", ".join(
        f"{pm['module']}({pm['priority']})" for pm in route.get('possible_modules', [])
    )
    conflict_signals_str = ", ".join(route.get('conflict_signals', [])) or "none"
    parts.append(
        f"## 路由结果\n"
        f"- recommended_track: {recommended_track}\n"
        f"- recommended_tool: {recommended_tool or 'null'}\n"
        f"- reasoning_signals: {', '.join(route['reasoning_signals'])}\n"
        f"- fallback_policy: {route['fallback_policy']}\n"
        f"- answer_policy: {route['answer_policy']}\n"
        f"- possible_modules: {possible_modules_str or 'none'}\n"
        f"- model_review_required: {route.get('model_review_required', False)}\n"
        f"- override_allowed: {route.get('override_allowed', True)}\n"
        f"- conflict_signals: {conflict_signals_str}"
    )

    # section 3: analysis steps by track
    if recommended_track == "scaffold_guidance" and recommended_tool:
        scaffold_note = ""
        if include_scaffold_summary:
            scaffold_note = (
                f"\n请先参考 `{recommended_tool}` 返回的 scaffold 内容，"
                f"按该模块的 stage_order、checklists 和 uncertainty_policy 分析。"
            )
        parts.append(
            f"## 分析步骤（scaffold_guidance）\n"
            f"1. 获取 `{recommended_tool}` scaffold 内容{scaffold_note}\n"
            f"2. 按 scaffold 的思考顺序逐步分析\n"
            f"3. 逐项核验选项 A/B/C/D\n"
            f"4. 检查是否唯一支持某个选项\n"
            f"5. 若不唯一或信息不足，输出 analysis_only"
        )
    elif recommended_track == "solver_candidate":
        parts.append(
            f"## 分析步骤（solver_candidate）\n"
            f"1. 本 compose tool 不调用 solver\n"
            f"2. 当前模块为 {module_cn}，solver 尚未以 MCP guidance 形式暴露\n"
            f"3. 请大模型基于自身能力进行受约束分析\n"
            f"4. 逐项核验选项 A/B/C/D\n"
            f"5. 不能把 solver_candidate 等同于直接答案\n"
            f"6. 若信息不足或不唯一，输出 analysis_only"
        )
    else:
        parts.append(
            f"## 分析步骤（route_uncertain）\n"
            f"1. 模块不确定，不要直接作答\n"
            f"2. 优先要求用户补充模块/题面/图片/选项\n"
            f"3. 如仍需分析，只能 analysis_only\n"
            f"4. 逐项核验选项 A/B/C/D"
        )

    # section 4: option verification
    parts.append(
        "## 选项逐项核验要求\n"
        "对 A/B/C/D 每个选项，分别检查：\n"
        "- 是否回应问法\n"
        "- 是否覆盖文段/题干核心信息\n"
        "- 是否存在偷换概念/以偏概全/无中生有\n"
        "- 是否与已知条件矛盾\n"
        "若多个选项均可解释，标注 analysis_only。\n\n"
        f"**Review instruction**: {route.get('review_instruction', 'N/A')}"
    )

    # section 5: uncertainty policy
    parts.append(
        "## 不确定性策略\n"
        "- 信息不足 → analysis_only\n"
        "- 多个选项均可解释 → analysis_only\n"
        "- 需要外部专业知识且无法确认 → analysis_only\n"
        "- 不得默认选择第一个选项\n"
        "- 不得用题号、case_id 或标准答案写规则"
    )

    # section 6: must not do
    parts.append(
        "## 禁止事项\n"
        "- 不要跳步\n"
        "- 不要只凭关键词选答案\n"
        "- 不要默认选择第一个选项\n"
        "- 不要在多个选项都可解释时强选\n"
        "- 必须逐项核验 A/B/C/D\n"
        "- 若信息不足或不唯一，输出 analysis_only\n"
        f"{'- 图形推理由大模型看图，MCP 不做视觉识别' if module_guess == 'graphic_reasoning' else ''}"
    )

    # section 7: output format
    parts.append(
        "## 输出格式要求\n"
        "请按以下结构输出：\n"
        "1. analysis: 你的分析过程\n"
        "2. option_checks: 对每个选项的核验结果\n"
        "3. unique_support: 是否唯一支持某个选项\n"
        "4. final_mode: answer_if_unique_else_analysis_only\n"
        "5. uncertainty_notes: 不确定因素列表"
    )

    prompt_text = "\n\n".join(parts)

    return {
        "mode": "prompt_composition",
        "route": {
            "mode": "route_only",
            "module_guess": module_guess,
            "confidence": route["confidence"],
            "recommended_track": recommended_track,
            "recommended_tool": recommended_tool,
            "fallback_policy": route["fallback_policy"],
            "answer_policy": route["answer_policy"],
            "warnings": warnings,
            "possible_modules": route.get("possible_modules", []),
            "model_review_required": route.get("model_review_required", False),
            "override_allowed": route.get("override_allowed", True),
            "review_instruction": route.get("review_instruction", ""),
            "conflict_signals": route.get("conflict_signals", []),
            # v0.5.0: module context override fields
            "module_hint": route.get("module_hint"),
            "section_context": route.get("section_context"),
            "module_hint_applied": route.get("module_hint_applied", False),
            "module_hint_conflict": route.get("module_hint_conflict", False),
            "heuristic_module_guess": route.get("heuristic_module_guess"),
        },
        "prompt_text": prompt_text,
        "prompt_contract": {
            "must_verify_options": True,
            "must_not_force_answer": True,
            "analysis_only_if_uncertain": True,
            "no_answer_inside_tool": True,
        },
        "expected_response_schema": {
            "analysis": "string",
            "option_checks": "object",
            "unique_support": "boolean",
            "final_mode": "answer_if_unique_else_analysis_only",
            "uncertainty_notes": "list",
        },
        "warnings": warnings,
    }


# ── Conservative answer prompt composer (v0.4) ────────────────────


_ANALYSIS_ONLY_REQUIRED_IF = [
    "missing_visual_content",
    "missing_table_or_material",
    "incomplete_options",
    "ambiguous_module",
    "multiple_plausible_options",
    "low_confidence",
    "route_uncertain_without_semantic_override",
    "calculation_not_reproducible",
    "option_text_too_sparse",
]

_OUTPUT_SCHEMA = {
    "mode": "answer | analysis_only",
    "module": (
        "data_analysis | quantity_relation | verbal_reasoning | "
        "graphic_reasoning | definition_judgement | analogy_reasoning | "
        "logic_reasoning | logic_analysis | unknown"
    ),
    "route_module_guess": "string",
    "route_overridden": "boolean",
    "corrected_module": "string | null",
    "answer": "A/B/C/D/null",
    "confidence": "high | medium | low",
    "reasoning_summary": "string",
    "eliminated_options": "list",
    "risk_flags": "list",
    "analysis_only_reason": "string | null",
    "safety_checks": {
        "read_full_question": "boolean",
        "read_all_options": "boolean",
        "module_reviewed": "boolean",
        "missing_visual_or_table": "boolean",
        "options_complete": "boolean",
        "unique_option_justified": "boolean",
        "no_guessing": "boolean",
    },
}

_SAFETY_CONTRACT = {
    "no_answer_field_in_tool_return": True,
    "no_selected_option_field_in_tool_return": True,
    "no_prediction_field_in_tool_return": True,
    "no_solver_call": True,
    "no_external_llm_api": True,
    "answer_only_when_unique": True,
    "analysis_only_when_uncertain": True,
    "no_default_to_first_option": True,
    "no_case_id_or_source_answer": True,
    "no_invented_visual_or_table": True,
    "wrong_zero_priority": True,
}


def _build_answer_prompt(
    route: dict[str, Any],
    question_text: str,
    options: dict[str, str] | None,
    allow_answer: bool,
    answer_block_reason: str | None = None,
) -> str:
    """Build the conservative answer prompt text."""
    module_guess = route["module_guess"]
    confidence = route["confidence"]
    recommended_track = route["recommended_track"]
    recommended_tool = route.get("recommended_tool")

    # Module-specific constraints
    module_constraints: dict[str, str] = {
        "graphic_reasoning": (
            "If the actual figure image or a sufficiently detailed figure "
            "description is missing, return analysis_only.\n"
            "Do not invent visual features."
        ),
        "data_analysis": (
            "If the table, chart, paragraph material, or required numeric "
            "data is missing, return analysis_only.\n"
            "All calculations must be reproducible from the visible data."
        ),
        "verbal_reasoning": (
            "For main idea, sentence ordering, insertion, and logical "
            "fill-in questions, avoid over-interpreting.\n"
            "If two options are semantically close and cannot be uniquely "
            "separated, return analysis_only."
        ),
        "analogy_reasoning": (
            "Identify the relationship in the stem before comparing options.\n"
            "If multiple relation dimensions are plausible and not uniquely "
            "resolved, return analysis_only."
        ),
        "definition_judgement": (
            "Extract necessary definition conditions first.\n"
            "Compare each option against the conditions.\n"
            "If the definition boundary is unclear, return analysis_only."
        ),
        "logic_reasoning": (
            "Identify conclusion, premise, assumption, strengthen/weaken "
            "direction first.\n"
            "Do not select an option only because it sounds relevant."
        ),
        "quantity_relation": (
            "Set variables explicitly.\n"
            "Calculation must be reproducible.\n"
            "If the problem type or equation is uncertain, return analysis_only."
        ),
        "logic_analysis": (
            "List constraints explicitly.\n"
            "If possible, verify options by constraint checking.\n"
            "If constraints are insufficient for a unique answer, "
            "return analysis_only."
        ),
    }

    parts: list[str] = []

    # Section 1: core constraints
    parts.append(
        "## Core Answer Constraints\n"
        "1. MCP route is advisory, not final.\n"
        "2. First review the full question semantics and options.\n"
        "3. You may override the MCP route if semantic evidence conflicts "
        "with the route.\n"
        "4. Use the corresponding scaffold/method constraints.\n"
        "5. You may output an answer only if exactly one option is justified.\n"
        "6. If the question lacks required visual/table/material context, "
        "output analysis_only.\n"
        "7. If the options are incomplete or ambiguous, output analysis_only.\n"
        "8. If multiple options remain plausible, output analysis_only.\n"
        "9. Do not guess.\n"
        "10. Do not default to A or the first option.\n"
        "11. Do not use case_id, source answer, or hidden labels.\n"
        "12. Do not invent missing visual/table content.\n"
        "13. Wrong = 0 has higher priority than more correct answers."
    )

    # Section 2: route context
    possible_modules_str = ", ".join(
        f"{pm['module']}({pm['priority']})"
        for pm in route.get("possible_modules", [])
    )
    conflict_signals_str = ", ".join(route.get("conflict_signals", [])) or "none"
    route_context_parts = [
        "## Route Context",
        f"- module_guess: {module_guess}",
        f"- confidence: {confidence}",
        f"- recommended_track: {recommended_track}",
        f"- recommended_tool: {recommended_tool or 'null'}",
        f"- possible_modules: {possible_modules_str or 'none'}",
        f"- model_review_required: {route.get('model_review_required', False)}",
        f"- override_allowed: {route.get('override_allowed', True)}",
        f"- conflict_signals: {conflict_signals_str}",
        f"- review_instruction: {route.get('review_instruction', 'N/A')}",
    ]
    # v0.5.0: module context override info
    if route.get("module_hint_applied"):
        hint_label = route.get("module_hint", "")
        heuristic = route.get("heuristic_module_guess", "")
        route_context_parts.append(
            f"- module_hint: {hint_label} (applied)"
        )
        if route.get("module_hint_conflict"):
            route_context_parts.append(
                f"- heuristic_module_guess: {heuristic} (overridden)"
            )
            route_context_parts.append(
                "- module_hint_conflict: true"
            )
            route_context_parts.append(
                "- The route is guided by explicit exam section context. "
                "If the visual/table/material context is missing, do not answer. "
                "If model observation conflicts with the module hint, explain the "
                "conflict and return analysis_only unless the override is justified."
            )
        else:
            route_context_parts.append(
                "- module_hint_conflict: false"
            )
    parts.append("\n".join(route_context_parts))

    # Section 3: question and options
    opt_str = ""
    if options:
        opt_str = "\n".join(f"  {k}. {v}" for k, v in options.items())
        opt_str = f"\nOptions:\n{opt_str}"
    parts.append(
        "## Question\n"
        f"{question_text[:500] if question_text else '(empty)'}"
        f"{opt_str}"
    )

    # Section 4: module-specific constraints
    mod_constraint = module_constraints.get(module_guess, "")
    if mod_constraint:
        parts.append(
            f"## Module-Specific Constraints ({module_guess})\n"
            f"{mod_constraint}"
        )

    # Section 5: output schema
    parts.append(
        "## Required Output Schema\n"
        "You must output a JSON object with the following fields:\n"
        "```json\n"
        '{\n'
        '  "mode": "answer | analysis_only",\n'
        '  "module": "<module_name>",\n'
        '  "route_module_guess": "<from route>",\n'
        '  "route_overridden": false,\n'
        '  "corrected_module": null,\n'
        '  "answer": "A/B/C/D/null",\n'
        '  "confidence": "high | medium | low",\n'
        '  "reasoning_summary": "...",\n'
        '  "eliminated_options": [],\n'
        '  "risk_flags": [],\n'
        '  "analysis_only_reason": null,\n'
        '  "safety_checks": {\n'
        '    "read_full_question": true,\n'
        '    "read_all_options": true,\n'
        '    "module_reviewed": true,\n'
        '    "missing_visual_or_table": false,\n'
        '    "options_complete": true,\n'
        '    "unique_option_justified": true,\n'
        '    "no_guessing": true\n'
        '  }\n'
        '}\n'
        "```\n\n"
        "Rules:\n"
        "- mode = answer: answer must be A/B/C/D.\n"
        "- mode = analysis_only: answer must be null.\n"
        "- confidence = low: mode must be analysis_only.\n"
        "- missing_visual_or_table = true: mode must be analysis_only.\n"
        "- unique_option_justified = false: mode must be analysis_only."
    )

    # Section 6: answer gate
    if not allow_answer:
        block_reason_text = {
            "missing_visual_content": (
                "Because the actual figure image or sufficient visual description "
                "is missing, return mode = analysis_only and answer = null."
            ),
            "missing_table_or_material": (
                "Because the table/material/chart data required for calculation "
                "is missing, return mode = analysis_only and answer = null."
            ),
            "route_uncertain_without_semantic_override": (
                "Because the route is uncertain and no semantic override is provided, "
                "return mode = analysis_only and answer = null."
            ),
            "answer_mode_disabled": (
                "The caller has disabled answer mode.\n"
                "You must return mode = analysis_only regardless of confidence."
            ),
            "low_confidence": (
                "Because the routing confidence is low, "
                "return mode = analysis_only and answer = null."
            ),
        }
        reason_explanation = block_reason_text.get(
            answer_block_reason,
            "You must return mode = analysis_only and answer = null."
        )
        parts.append(
            "## Answer Gate\n"
            f"answer_allowed = false\n"
            f"answer_block_reason = {answer_block_reason or 'unknown'}\n\n"
            f"{reason_explanation}"
        )

    return "\n\n".join(parts)


def tool_compose_xingce_answer_prompt(
    question_text: str,
    options: dict[str, str] | None = None,
    module_hint: str | None = None,
    section_context: str | None = None,
    image_present: bool = False,
    strict_mode: bool = True,
    allow_answer: bool = True,
    visual_description: str | None = None,
    material_present: bool = False,
    material_text: str | None = None,
    table_present: bool = False,
) -> dict[str, Any]:
    """Compose a conservative answer prompt for LLM-in-the-loop answering."""
    route = _route_xingce_question_core(
        question_text=question_text,
        options=options,
        module_hint=module_hint,
        section_context=section_context,
        image_present=image_present,
        strict_mode=strict_mode,
    )

    # ── Context availability gate ──────────────────────────────────
    module_guess = route["module_guess"]
    answer_block_reason: str | None = None

    # Independent data material signal detection (v0.4.2)
    # Even if route is not data_analysis, if the question has material signals,
    # we should still require material/table context
    # v0.5.1: When module_hint is present, only check question text to avoid
    # distractor options like "折线图/柱状图" triggering false material gate.
    combined_text = (question_text or "") + " " + " ".join((options or {}).values())
    _hint_applied = route.get("module_hint_applied", False)
    _material_gate_text = question_text if _hint_applied else combined_text
    requires_table_or_material = (
        module_guess == "data_analysis"
        or _has_data_material_signal(_material_gate_text)
    )

    # Graphic reasoning: requires visual content
    if module_guess == "graphic_reasoning":
        has_visual = image_present or (visual_description and len(visual_description.strip()) >= 10)
        if not has_visual:
            answer_block_reason = "missing_visual_content"

    # Data analysis / material signal: requires material/table/chart data
    if requires_table_or_material:
        has_material = material_present or table_present or (material_text and len(material_text.strip()) >= 10)
        if not has_material:
            answer_block_reason = "missing_table_or_material"

    # Route uncertain: always block
    if route["recommended_track"] == "route_uncertain":
        answer_block_reason = "route_uncertain_without_semantic_override"

    # allow_answer=false: always block (highest priority)
    if not allow_answer:
        answer_block_reason = "answer_mode_disabled"

    # Determine answer_allowed
    answer_allowed = allow_answer and answer_block_reason is None

    # Force analysis_only for low/unknown confidence
    if route["confidence"] in ("low", "unknown"):
        answer_allowed = False
        if answer_block_reason is None:
            answer_block_reason = "low_confidence"

    answer_prompt = _build_answer_prompt(
        route=route,
        question_text=question_text,
        options=options,
        allow_answer=answer_allowed,
        answer_block_reason=answer_block_reason,
    )

    analysis_only_required_if: list[str] = list(_ANALYSIS_ONLY_REQUIRED_IF)

    # Context requirements
    context_requirements = {
        "requires_visual": module_guess == "graphic_reasoning",
        "requires_table_or_material": requires_table_or_material,
        "image_present": image_present,
        "visual_description_present": bool(visual_description and len(visual_description.strip()) >= 10),
        "material_present": material_present,
        "table_present": table_present,
        "material_text_present": bool(material_text and len(material_text.strip()) >= 10),
    }

    return {
        "tool": "compose_xingce_answer_prompt",
        "version": "v0.5.0",
        "route": {
            "mode": "route_only",
            "module_guess": route["module_guess"],
            "confidence": route["confidence"],
            "recommended_track": route["recommended_track"],
            "recommended_tool": route.get("recommended_tool"),
            "possible_modules": route.get("possible_modules", []),
            "model_review_required": route.get("model_review_required", False),
            "override_allowed": route.get("override_allowed", True),
            "review_instruction": route.get("review_instruction", ""),
            "conflict_signals": route.get("conflict_signals", []),
            "reasoning_signals": route.get("reasoning_signals", []),
            "warnings": route.get("warnings", []),
            # v0.5.0: module context override fields
            "module_hint": route.get("module_hint"),
            "section_context": route.get("section_context"),
            "module_hint_applied": route.get("module_hint_applied", False),
            "module_hint_conflict": route.get("module_hint_conflict", False),
            "heuristic_module_guess": route.get("heuristic_module_guess"),
        },
        "answer_prompt": answer_prompt,
        "output_schema": _OUTPUT_SCHEMA,
        "safety_contract": _SAFETY_CONTRACT,
        "answer_allowed": answer_allowed,
        "answer_block_reason": answer_block_reason,
        "analysis_only_required_if": analysis_only_required_if,
        "context_requirements": context_requirements,
        "model_review_required": route.get("model_review_required", False),
        "override_allowed": route.get("override_allowed", True),
    }


def create_mcp_server() -> Any:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError(
            "The MCP SDK is not installed. Run `python -m pip install -e .` first."
        ) from exc

    server = FastMCP("xingce-solver")

    @server.tool()
    def get_method_card(method_id: str) -> dict[str, Any]:
        """Return a full method card by method_id."""

        return tool_get_method_card(method_id)

    @server.tool()
    def search_methods(
        query: str, module: str | None = None, top_k: int = 5
    ) -> dict[str, Any]:
        """Search method cards in the Xingce knowledge base."""

        return tool_search_methods(query=query, module=module, top_k=top_k)

    @server.tool()
    def classify_question(question_text: str) -> dict[str, Any]:
        """Route a question stem to preliminary modules and method cards."""

        return tool_classify_question(question_text=question_text)

    @server.tool()
    def get_source_reference(method_id: str) -> dict[str, Any]:
        """Return source files, pages, confidence, and review flag for a method."""

        return tool_get_source_reference(method_id)

    @server.tool()
    def solve_data_analysis(
        question_text: str, options: list[str] | dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Build a structured data-analysis solving draft, not a final answer."""

        return tool_solve_data_analysis(question_text=question_text, options=options)

    @server.tool()
    def solve_logic_reasoning(
        question_text: str, options: dict[str, str] | list[str] | None = None
    ) -> dict[str, Any]:
        """Build a structured logic-reasoning solving draft, not a final answer."""

        return tool_solve_logic_reasoning(question_text=question_text, options=options)

    @server.tool()
    def get_graphic_reasoning_scaffold() -> dict[str, Any]:
        """Return the read-only method scaffold for graphic reasoning. This tool provides visual observation order, visual checklists, response template, and uncertainty policy. It does not inspect images, solve questions, or select an answer."""

        return tool_get_graphic_reasoning_scaffold()

    @server.tool()
    def get_definition_judgement_scaffold() -> dict[str, Any]:
        """Return the read-only method scaffold for definition judgement. This tool provides question polarity routing, definition element checklists, option verification template, and uncertainty policy. It does not solve questions or select an answer."""

        return tool_get_definition_judgement_scaffold()

    @server.tool()
    def get_analogy_reasoning_scaffold() -> dict[str, Any]:
        """Return the read-only method scaffold for analogy reasoning. This tool provides relation-type checklists, relation verification steps, option comparison guidance, and uncertainty policy. It does not solve questions or select an answer."""

        return tool_get_analogy_reasoning_scaffold()

    @server.tool()
    def get_logic_analysis_scaffold() -> dict[str, Any]:
        """Return the read-only method scaffold for logic analysis reasoning. This tool provides problem-type routing, structure templates, constraint extraction checklist, option verification guidance, and uncertainty policy. It does not solve questions or select an answer."""

        return tool_get_logic_analysis_scaffold()

    @server.tool()
    def get_quantity_relation_scaffold() -> dict[str, Any]:
        """Return the read-only method scaffold for quantity relation reasoning. This tool provides problem-type routing, quantity extraction guidance, unit normalization checks, method checklists, option verification guidance, and uncertainty policy. It does not solve questions, compute final answers, or select an option."""

        return tool_get_quantity_relation_scaffold()

    @server.tool()
    def get_verbal_reasoning_scaffold() -> dict[str, Any]:
        """Return the read-only method scaffold for verbal reasoning. This tool provides question-type routing, discourse-structure analysis guidance, cloze-context checks, sentence-expression checks, option verification guidance, and uncertainty policy. It does not solve questions, compute final answers, or select an option."""

        return tool_get_verbal_reasoning_scaffold()

    @server.tool()
    def route_xingce_question(
        question_text: str,
        options: dict[str, str] | None = None,
        module_hint: str | None = None,
        section_context: str | None = None,
        image_present: bool = False,
        strict_mode: bool = True,
    ) -> dict[str, Any]:
        """Route a question to the recommended module or scaffold without solving. Supports module_hint / section_context to guide routing by exam section context. Returns module guess, confidence, recommended tool/track, and reasoning signals. Does not answer questions or select options."""

        return tool_route_xingce_question(
            question_text=question_text,
            options=options,
            module_hint=module_hint,
            section_context=section_context,
            image_present=image_present,
            strict_mode=strict_mode,
        )

    @server.tool()
    def compose_xingce_analysis_prompt(
        question_text: str,
        options: dict[str, str] | None = None,
        module_hint: str | None = None,
        section_context: str | None = None,
        image_present: bool = False,
        strict_mode: bool = True,
        include_scaffold_summary: bool = True,
    ) -> dict[str, Any]:
        """Compose a structured analysis prompt from question and route result. Supports module_hint / section_context to guide routing by exam section context. Does not solve questions, compute answers, or select options. Returns prompt_text for LLM consumption."""

        return tool_compose_xingce_analysis_prompt(
            question_text=question_text,
            options=options,
            module_hint=module_hint,
            section_context=section_context,
            image_present=image_present,
            strict_mode=strict_mode,
            include_scaffold_summary=include_scaffold_summary,
        )

    @server.tool()
    def compose_xingce_answer_prompt(
        question_text: str,
        options: dict[str, str] | None = None,
        module_hint: str | None = None,
        section_context: str | None = None,
        image_present: bool = False,
        strict_mode: bool = True,
        allow_answer: bool = True,
        visual_description: str | None = None,
        material_present: bool = False,
        material_text: str | None = None,
        table_present: bool = False,
    ) -> dict[str, Any]:
        """Compose a conservative answer prompt for LLM-in-the-loop answering. Supports module_hint / section_context to guide routing by exam section context. Returns answer_prompt with strict constraints, output schema, and safety contract. Does not answer questions, call external LLM, or select options."""

        return tool_compose_xingce_answer_prompt(
            question_text=question_text,
            options=options,
            module_hint=module_hint,
            section_context=section_context,
            image_present=image_present,
            strict_mode=strict_mode,
            allow_answer=allow_answer,
            visual_description=visual_description,
            material_present=material_present,
            material_text=material_text,
            table_present=table_present,
        )

    return server


def main() -> None:
    create_mcp_server().run()


if __name__ == "__main__":
    main()
