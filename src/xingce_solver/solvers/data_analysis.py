from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..kb import get_method_card, search_methods
from ..router import classify_question


DATA_ANALYSIS_MODULE = "资料分析"


TYPE_RULES = [
    {
        "question_type": "比重变化",
        "sub_type": "比重差/百分点变化",
        "triggers": [
            "占比变化",
            "比重变化",
            "占比发生变化",
            "比重发生变化",
            "提高几个百分点",
            "下降几个百分点",
            "占比提高",
            "占比下降",
            "百分点",
        ],
        "method_ids": ["da_share_change_004", "da_share_trend_003", "da_ratio_share_diff_005"],
        "plan": [
            "第一步：先判断方向，比较部分增速和整体增速；若题干已直接给出占比提高/下降，也要先确认方向。",
            "第二步：判断题目是否要求具体百分点变化；涉及百分点时，不得把百分点和百分数混淆。",
            "第三步：需要估算时优先用比重差小于增速差、选项差距和近似比重判断，不做五六位数暴力长除。",
        ],
        "forbidden": ["禁止把百分点当成增长率百分数。", "禁止未确认部分属于整体就套比重差。", "禁止直接暴力长除。"],
    },
    {
        "question_type": "比重",
        "sub_type": "本期比重",
        "triggers": ["部分占整体", "占比", "比重", "占"],
        "method_ids": ["da_share_current_001", "da_truncate_division_001"],
        "plan": [
            "第一步：明确分子是部分量、分母是整体量，并确认二者属于同一时间和同一口径。",
            "第二步：核对单位是否一致，必要时先统一单位。",
            "第三步：根据选项差距决定截位直除或精算；选项差距大时优先截位估算。",
        ],
        "forbidden": ["禁止部分和整体口径不一致时直接相除。", "禁止忽略单位。", "禁止无视选项差距做复杂长除。"],
    },
    {
        "question_type": "增长量",
        "sub_type": "增长量",
        "triggers": ["增长量", "增量", "增加多少", "增加了多少", "减少多少", "减少了多少", "多多少", "少多少", "同比增加"],
        "method_ids": ["da_growth_amount_001", "da_growth_amount_compare_002", "da_415_parts_001", "da_assumption_allocation_001"],
        "plan": [
            "第一步：判断给的是现期量B、基期量A还是增长率R，先确定增长量公式来源。",
            "第二步：若R接近常用分数，优先考虑415份数法；R较小且选项差距大时可用假设分配法。",
            "第三步：输出前检查单位和正负方向。",
        ],
        "forbidden": ["禁止把 B × R 当作精确增长量。", "禁止忽略增长或下降方向。"],
    },
    {
        "question_type": "基期量",
        "sub_type": "已知现期量和增长率求基期",
        "triggers": ["上年", "去年", "前期", "基期"],
        "method_ids": ["da_abx_base_direct_001", "da_abx_base_interval_002", "da_415_parts_001"],
        "plan": [
            "第一步：判断是单期基期还是隔年基期；本题若已知现期B和同比增长率R，优先按单期基期处理。",
            "第二步：增长时使用 A = B/(1+R)，下降时使用 A = B/(1-R)。",
            "第三步：结合选项差距决定估算精度；选项差距大时可用分数化或截位估算。",
        ],
        "forbidden": ["禁止增长时除以 1-R。", "禁止下降时除以 1+R。", "禁止不看选项差距盲目精算。"],
    },
    {
        "question_type": "增长率",
        "sub_type": "一般增长率",
        "triggers": ["增长率", "增速", "同比增长", "比上年增长"],
        "method_ids": ["da_growth_rate_general_001", "da_growth_rate_interval_002", "da_growth_rate_ratio_003"],
        "plan": [
            "第一步：先区分普通增长率、间隔增长率、比值增长率；平均数增长率应转入比值增长率。",
            "第二步：普通增长率使用 R = X / A = (B-A)/A，其中A为基期量，B为现期量。",
            "第三步：结合选项差距选择估算或精算，注意增长量不能除以现期量。",
        ],
        "forbidden": ["禁止用增长量除以现期量。", "禁止把平均数增长率当普通增长率。"],
    },
    {
        "question_type": "平均数",
        "sub_type": "平均数",
        "triggers": ["平均", "人均", "每", "单位", "年均"],
        "method_ids": [
            "da_average_general_001",
            "da_average_annual_growth_amount_002",
            "da_average_annual_growth_rate_003",
            "da_growth_rate_ratio_003",
        ],
        "plan": [
            "第一步：判断是一般平均数、平均数增长率、年均增长量还是年均增长率。",
            "第二步：一般平均数按总量/份数处理；平均数增长率调用比值增长率。",
            "第三步：年均增长量和年均增长率必须区分，不能混用公式。",
        ],
        "forbidden": ["禁止把年均增长量和年均增长率混用。", "禁止忽略分子分母单位。"],
    },
]


TIME_RE = re.compile(r"\d{4}年|\d{1,2}月|上年|去年|前期|基期|本期|同比|环比")
RATE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:%|％|个百分点)")
PERCENTAGE_POINT_RE = re.compile(r"\d+(?:\.\d+)?\s*个百分点")
NUMBER_UNIT_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:亿美元|万美元|美元|万亿元|亿元|万元|元|亿件|万件|件|万套|套|万亩|亩|座|万人|万人次|人|万吨|吨|公里|平方公里|%|％|个百分点)?"
)
AMOUNT_RE = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>亿美元|万美元|美元|万亿元|亿元|万元|元|亿件|万件|件|万套|套|万亩|亩|座|万人|万人次|人|万吨|吨|公里|平方公里)"
)
OPTION_RE = re.compile(
    r"(?:^|[\s；;，,:：?？])([A-D])(?:[\.、:：])\s*(.*?)(?=\s*[A-D](?:[\.、:：])|$)"
)
OPTION_VALUE_RE = re.compile(
    r"(?P<value>-?\d+(?:\.\d+)?)\s*(?P<unit>亿美元|万美元|美元|万亿元|亿元|万元|元|亿件|万件|件|万套|套|万亩|亩|座|万人|万人次|人|万吨|吨|公里|平方公里|%|％|个百分点|倍)?"
)
METRIC_WORDS = [
    "生产总值",
    "产值",
    "收入",
    "比重",
    "占比",
    "增长率",
    "增速",
    "增长量",
    "平均",
    "人均",
    "年均",
]
SUBJECT_RE = re.compile(r"(?<!\d)(某地区|某产业|第一产业|第二产业|第三产业|[\u4e00-\u9fa5]{2,12}(?:地区|产业|行业|企业|单位))")
YEAR_COMPARISON_PREFIX = r"(?:比\s*\d{4}年|较\s*\d{4}年|相比\s*\d{4}年|相较\s*\d{4}年|与\s*\d{4}年\s*相比)"
YEAR_COMPARISON_RATE_RE = re.compile(
    YEAR_COMPARISON_PREFIX + r"\s*(?P<direction>增长|下降)\s*(?P<rate>\d+(?:\.\d+)?)\s*(?:%|％)"
)
GROWTH_AMOUNT_RANKING_RE = re.compile(r"排序|排列|从高到低|从低到高|由大到小|由小到大|按.*?(?:排序|排列)")
GROWTH_RATE_RANKING_RE = re.compile(r"同比增速|增长率|增速")


def solve_data_analysis(
    question_text: str,
    options: list[str] | dict[str, str] | None = None,
    kb_dir: str | Path | None = None,
) -> dict[str, Any]:
    matched_routes = classify_question(question_text, kb_dir=kb_dir, top_k=8)
    data_routes = [route for route in matched_routes if route.get("module") == DATA_ANALYSIS_MODULE]
    if not data_routes and _looks_like_data_analysis_solver_pattern(question_text):
        data_routes = [
            {
                "module": DATA_ANALYSIS_MODULE,
                "question_type": "资料分析结构题",
                "sub_type": "solver_internal_rule",
                "priority_method_id": "",
                "matched_triggers": ["solver_internal_rule"],
            }
        ]
    if not data_routes:
        return _empty_result(
            matched_routes=matched_routes,
            warnings=["题干未初步路由到资料分析模块，当前 solve_data_analysis 仅处理资料分析。"],
            needs_more_data=True,
        )

    elements = extract_elements(question_text, options)
    profile = _select_type_rule(question_text, data_routes)
    recommended_methods = _build_recommended_methods(profile["method_ids"], kb_dir)
    warnings = _build_warnings(profile["question_type"], question_text, elements)
    if _looks_like_full_material_input(question_text, elements):
        warnings.append("输入包含大量数字，可能是整段材料全文；建议先筛选当前题相关字段后再调用 solve_data_analysis。")
    option_gap_analysis = analyze_option_gaps(elements["options"])
    formula_plan = _build_formula_plan(profile["question_type"], question_text, elements)
    computed_result, estimation_plan, sub_calculations, ranking_result, formula_notes = _compute_safe_estimate(
        profile["question_type"], question_text, elements, formula_plan
    )
    answer_candidate = _match_answer_candidate(
        computed_result, elements["options"], ranking_result=ranking_result
    )
    if computed_result is None and not any("无法" in warning or "缺少" in warning for warning in warnings):
        if profile["question_type"] in {"比重", "增长率", "增长量", "基期量"}:
            warnings.append("当前题干未能抽取出完整可计算变量，只提供结构化解题草案。")
    needs_more_data = _needs_more_data(
        profile["question_type"], question_text, elements, warnings, formula_plan, computed_result
    )
    source_method_ids = [item["method_id"] for item in recommended_methods]

    return {
        "module": DATA_ANALYSIS_MODULE,
        "question_type": profile["question_type"],
        "sub_type": profile["sub_type"],
        "needs_more_data": needs_more_data,
        "matched_routes": data_routes,
        "recommended_methods": recommended_methods,
        "extracted_elements": elements,
        "option_gap_analysis": option_gap_analysis,
        "formula_plan": formula_plan,
        "estimation_plan": estimation_plan,
        "solving_plan": profile["plan"],
        "sub_calculations": sub_calculations,
        "ranking_result": ranking_result,
        "formula_notes": formula_notes,
        "calculation_policy": {
            "allow_exact_calculation": False,
            "prefer_estimation": True,
            "must_check_option_gap": True,
            "forbidden": profile["forbidden"],
        },
        "exam_style_explanation_draft": _build_explanation(
            profile, needs_more_data, warnings, computed_result, answer_candidate
        ),
        "computed_result": computed_result,
        "answer_candidate": answer_candidate,
        "source_method_ids": source_method_ids,
        "warnings": warnings,
    }


def extract_elements(
    question_text: str, options: list[str] | dict[str, str] | None = None
) -> dict[str, Any]:
    rates = _unique(match.group(0).replace("％", "%").replace(" ", "") for match in RATE_RE.finditer(question_text))
    percentage_points = _unique(
        match.group(0).replace(" ", "") for match in PERCENTAGE_POINT_RE.finditer(question_text)
    )
    numbers = _unique(match.group(0).strip() for match in NUMBER_UNIT_RE.finditer(question_text))
    units = _unique(unit for unit in ["亿元", "亿件", "万元", "元", "百分点", "%", "％"] if unit in question_text)
    parsed_options = _extract_options(question_text, options)
    return {
        "time": _unique(match.group(0) for match in TIME_RE.finditer(question_text)),
        "subject": _unique(match.group(0) for match in SUBJECT_RE.finditer(question_text)),
        "metrics": _unique(word for word in METRIC_WORDS if word in question_text),
        "numbers": numbers,
        "rates": rates,
        "percentage_points": percentage_points,
        "units": units,
        "options": parsed_options,
        "option_values": [option["raw"] for option in parsed_options],
    }


def _looks_like_full_material_input(question_text: str, elements: dict[str, Any]) -> bool:
    return (
        len(elements.get("numbers", [])) > 12
        and len(elements.get("rates", [])) > 4
        and (question_text.count("。") + question_text.count("；") + question_text.count(";")) >= 3
    )


def _select_type_rule(question_text: str, data_routes: list[dict[str, Any]]) -> dict[str, Any]:
    if _looks_like_interval_inverse_growth(question_text):
        return _custom_rule(
            "增长率",
            "间隔增长率/逆向增长率",
            ["da_growth_rate_interval_002", "da_growth_rate_general_001"],
            [
                "第一步：识别已知末期相对中间期增长率R1，以及末期相对基期的间隔增长率R间。",
                "第二步：使用 1 + R间 = (1 + R2) × (1 + R1)，反推 R2 = (1 + R间)/(1 + R1) - 1。",
                "第三步：先判断正负和是否超过10%，再匹配选项，不做复杂长除。",
            ],
            ["禁止把2021相对2019的间隔增长率直接当作2020相对2019。"],
        )
    if _looks_like_reverse_growth_rate_ranking(question_text):
        return _custom_rule(
            "增长率",
            "多对象现期量+增长量反推增速排序",
            ["da_growth_rate_general_001", "da_compare_ratio_growth_001"],
            [
                "第一步：逐个对象提取现期量B和增长量X，不能直接比较现期量或增长量。",
                "第二步：用 基期量 = 现期量 - 增长量，增长率 = 增长量 / 基期量 反推各对象增速。",
                "第三步：按题目要求从高到低或从低到高排序，再匹配选项。",
            ],
            ["禁止直接比较增长量。", "禁止直接比较现期量。"],
        )
    if _looks_like_group_sum_ratio(question_text):
        return _custom_rule(
            "平均数/倍数",
            "分组求和后求倍数",
            ["da_truncate_division_001", "da_average_general_001", "da_chart_lookup_001"],
            [
                "第一步：按题目指定的两个分组分别汇总组内多个数值。",
                "第二步：用 分子组合计 / 分母组合计 求倍数，确保没有漏项。",
                "第三步：结合选项区间匹配答案，不拿单个对象直接相除。",
            ],
            ["禁止漏掉分组内项目。", "禁止拿单个省份或单个对象直接相除。"],
        )
    if _looks_like_cumulative_new_residual_share(question_text):
        return _custom_rule(
            "比重",
            "累计减新增+残差小类基期占比",
            ["da_time_segments_001", "da_share_current_001", "da_truncate_division_001"],
            [
                "第一步：用本年末累计 - 本年新增，得到上年末累计总数和已知大类数量。",
                "第二步：用 小类 = 总数 - 已知大类1 - 已知大类2 反推残差小类。",
                "第三步：按 小类 / 总数 求上年末占比，再匹配选项。",
            ],
            ["禁止直接使用本年末占比。", "禁止忽略新增大类数据。"],
        )
    if _looks_like_current_share_difference(question_text):
        return _custom_rule(
            "比重变化",
            "两个现期比重差/百分点差",
            ["da_share_change_004", "da_ratio_share_diff_005", "da_truncate_division_001"],
            [
                "第一步：分别定位两组现期部分量和整体量，列出 share1 = part1/whole1、share2 = part2/whole2。",
                "第二步：计算 diff = (share1 - share2) × 100，结果单位是百分点。",
                "第三步：先判断高低方向，再按选项判断是否超过阈值，不把两个原始量直接相减。",
            ],
            ["禁止把两个原始量直接相减。", "禁止把百分点当成百分数增长率。"],
        )
    if _looks_like_growth_amount_ranking(question_text):
        return _custom_rule(
            "增长量",
            "增长量比较",
            ["da_growth_amount_compare_002", "da_growth_amount_001", "da_415_parts_001"],
            [
                "第一步：逐个对象提取现期量B和增长率R；下降时R为负。",
                "第二步：用 X = B × R / (1 + R) 估算各对象同比增量。",
                "第三步：先按正负和数量级排序，再匹配排序选项。",
            ],
            ["禁止只按现期量大小排序。", "禁止忽略下降时增量为负。"],
        )
    if _looks_like_time_segment_ratio(question_text):
        return _custom_rule(
            "平均数/倍数",
            "时间分段后求倍数",
            ["da_time_segments_001", "da_average_general_001", "da_truncate_division_001"],
            [
                "第一步：先把累计期拆分为目标时间段，例如 1-2月 = 1-3月累计 - 3月单月。",
                "第二步：两个对象分别完成同一时间段拆分，确保时间口径一致。",
                "第三步：按 对象A分段值 / 对象B分段值 求倍数，并结合选项匹配。",
            ],
            ["禁止直接用累计期相除。", "禁止直接用单月值相除。"],
        )
    if _looks_like_base_share(question_text):
        return _custom_rule(
            "比重",
            "基期比重",
            ["da_share_base_002", "da_abx_base_direct_001", "da_share_current_001"],
            [
                "第一步：分别求部分和其他部分的基期量，下降时除以1-R。",
                "第二步：基期总量 = 部分基期量 + 其他部分基期量。",
                "第三步：基期比重 = 部分基期量 / 基期总量，再匹配选项。",
            ],
            ["禁止把现期比重当作基期比重。", "禁止下降76%时除以1+76%。"],
        )
    if _looks_like_base_difference(question_text):
        return _custom_rule(
            "基期量",
            "前期差值",
            ["da_abx_base_diff_003", "da_abx_base_direct_001"],
            [
                "第一步：识别差值结构，例如贸易顺差 = 出口 - 进口。",
                "第二步：若两个指标增长率相同，先算现期差，再整体折回基期。",
                "第三步：若增长率不同，则分别求基期量后相减。",
            ],
            ["禁止直接用现期差当基期差。"],
        )
    if _looks_like_base_amount(question_text):
        return _rule_by_type("基期量")

    for rule in TYPE_RULES:
        if any(trigger in question_text for trigger in rule["triggers"]):
            return rule

    first_route = data_routes[0]
    route_type = first_route.get("question_type")
    for rule in TYPE_RULES:
        if route_type and route_type in {rule["question_type"], rule["sub_type"]}:
            return rule
    return _fallback_rule_from_search(question_text)


def _custom_rule(
    question_type: str,
    sub_type: str,
    method_ids: list[str],
    plan: list[str],
    forbidden: list[str],
) -> dict[str, Any]:
    return {
        "question_type": question_type,
        "sub_type": sub_type,
        "triggers": [],
        "method_ids": method_ids,
        "plan": plan,
        "forbidden": forbidden,
    }


def _looks_like_data_analysis_solver_pattern(question_text: str) -> bool:
    return any(
        [
            _looks_like_reverse_growth_rate_ranking(question_text),
            _looks_like_group_sum_ratio(question_text),
            _looks_like_cumulative_new_residual_share(question_text),
        ]
    )


def _looks_like_interval_inverse_growth(question_text: str) -> bool:
    return bool(
        re.search(r"同比(?:增长|下降)?\s*\d+(?:\.\d+)?\s*(?:%|％)", question_text)
        and YEAR_COMPARISON_RATE_RE.search(question_text)
        and re.search(r"问\s*\d{4}年.*" + YEAR_COMPARISON_PREFIX, question_text)
    )


def _looks_like_reverse_growth_rate_ranking(question_text: str) -> bool:
    return bool(
        GROWTH_AMOUNT_RANKING_RE.search(question_text)
        and GROWTH_RATE_RANKING_RE.search(question_text)
        and len(_parse_reverse_growth_rate_items(question_text)) >= 2
    )


def _looks_like_group_sum_ratio(question_text: str) -> bool:
    return bool(
        ("倍" in question_text)
        and ("分别" in question_text or "合计" in question_text)
        and _parse_group_sum_ratio(question_text)
    )


def _looks_like_cumulative_new_residual_share(question_text: str) -> bool:
    return bool(
        "累计" in question_text
        and "新增" in question_text
        and ("小型" in question_text or "小类" in question_text)
        and ("大型" in question_text and "中型" in question_text)
        and ("占比" in question_text or "比重" in question_text or "占" in question_text)
        and _parse_cumulative_new_residual_share(question_text)
    )


def _looks_like_growth_amount_ranking(question_text: str) -> bool:
    return bool(
        GROWTH_AMOUNT_RANKING_RE.search(question_text)
        and ("增量" in question_text or "增长量" in question_text or "同比增量" in question_text)
        and len(_parse_ranked_growth_items(question_text)) >= 2
    )


def _looks_like_current_share_difference(question_text: str) -> bool:
    return bool(
        len(_amount_values(question_text)) >= 4
        and ("占" in question_text or "比重" in question_text)
        and ("百分点" in question_text or "高" in question_text or "低" in question_text)
        and ("比" in question_text or "差" in question_text)
    )


def _looks_like_time_segment_ratio(question_text: str) -> bool:
    return bool(
        "累计" in question_text
        and "3月" in question_text
        and ("1-2月" in question_text or "1~2月" in question_text or "1至2月" in question_text)
        and ("1-3月" in question_text or "1~3月" in question_text or "1至3月" in question_text)
        and ("倍" in question_text or "是" in question_text)
        and _parse_time_segment_ratio(question_text)
    )


def _looks_like_base_share(question_text: str) -> bool:
    return bool(
        ("占比" in question_text or "比重" in question_text or "中的占" in question_text)
        and re.search(r"问\s*\d{4}年", question_text)
        and len(_parse_amount_rate_items(question_text)) >= 2
    )


def _looks_like_base_difference(question_text: str) -> bool:
    return bool(
        ("贸易顺差" in question_text or "差值" in question_text or "差额" in question_text)
        and len(_parse_amount_rate_items(question_text)) >= 2
    )


def _looks_like_base_amount(question_text: str) -> bool:
    years = [int(value[:-1]) for value in re.findall(r"\d{4}年", question_text)]
    asks_prior_year = bool(re.search(r"问\s*\d{4}年", question_text))
    has_current_and_rate = bool(re.search(r"同比(?:增长|下降)?\s*\d+(?:\.\d+)?\s*(?:%|％)", question_text))
    if re.search(r"问\s*\d{4}年.*比\s*\d{4}年", question_text):
        return False
    if "基期" in question_text or "上年" in question_text or "去年" in question_text or "前期" in question_text:
        return True
    return asks_prior_year and len(set(years)) >= 2 and has_current_and_rate


def _rule_by_type(question_type: str) -> dict[str, Any]:
    for rule in TYPE_RULES:
        if rule["question_type"] == question_type:
            return rule
    return TYPE_RULES[0]


def _fallback_rule_from_search(question_text: str) -> dict[str, Any]:
    results = search_methods(question_text, module=DATA_ANALYSIS_MODULE, top_k=1)
    if results:
        question_type = results[0].get("question_type")
        for rule in TYPE_RULES:
            if question_type == rule["question_type"]:
                return rule
    return TYPE_RULES[0]


def _build_recommended_methods(
    method_ids: list[str], kb_dir: str | Path | None = None
) -> list[dict[str, Any]]:
    methods = []
    for index, method_id in enumerate(method_ids):
        card = get_method_card(method_id, kb_dir)
        methods.append(
            {
                "method_id": method_id,
                "method_name": card.get("method_name") if card else "",
                "reason": "优先方法" if index == 0 else "辅助校验或备选方法",
                "need_review": bool(card.get("need_review", False)) if card else False,
            }
        )
    return methods


def _build_warnings(
    question_type: str, question_text: str, elements: dict[str, Any]
) -> list[str]:
    warnings: list[str] = []
    if question_type == "比重变化":
        if _looks_like_current_share_difference(question_text):
            return warnings
        if "百分点" in question_text:
            warnings.append("注意百分点和百分数不能混淆。")
        if not ("占比提高" in question_text or "占比下降" in question_text or "比重提高" in question_text or "比重下降" in question_text):
            warnings.append("缺少明确上升/下降方向，需比较部分增速和整体增速。")
        if len(elements["rates"]) < 2 and not re.search(r"(提高|下降|降低)\s*\d+(?:\.\d+)?\s*个百分点", question_text):
            warnings.append("缺少部分增速或整体增速，无法从公式推导比重变化方向。")
    elif question_type == "比重":
        if len(elements["numbers"]) < 2:
            warnings.append("缺少部分量和整体量，无法计算本期比重。")
        if len(elements["units"]) < 1:
            warnings.append("缺少或未识别单位，需先检查单位一致。")
    elif question_type == "增长率":
        if len(elements["numbers"]) < 2:
            warnings.append("缺少现期量和基期量，无法计算增长率。")
    elif question_type == "增长量":
        if len(elements["numbers"]) < 1 or len(elements["rates"]) < 1:
            warnings.append("缺少现期量/基期量或增长率，无法判断增长量计算方法。")
    elif question_type == "基期量":
        if len(elements["numbers"]) < 1:
            warnings.append("缺少现期量B，无法计算基期量。")
        if len(elements["rates"]) < 1:
            warnings.append("缺少增长率R，无法使用 A = B/(1±R)。")
    elif question_type == "平均数":
        if len(elements["numbers"]) < 2:
            warnings.append("缺少总量和份数，无法计算平均数。")
    return warnings


def _needs_more_data(
    question_type: str,
    question_text: str,
    elements: dict[str, Any],
    warnings: list[str],
    formula_plan: dict[str, Any],
    computed_result: float | None,
) -> bool:
    if question_type == "比重变化" and re.search(r"(提高|下降|降低)\s*\d+(?:\.\d+)?\s*个百分点", question_text):
        return False
    if computed_result is not None:
        return False
    if formula_plan.get("missing_variables"):
        return True
    if question_type == "增长率":
        return len(elements["numbers"]) < 2
    if question_type == "基期量":
        return len(elements["numbers"]) < 1 or len(elements["rates"]) < 1
    if question_type == "比重":
        return len(elements["numbers"]) < 2
    if question_type == "增长量":
        return len(elements["numbers"]) < 1 or len(elements["rates"]) < 1
    if question_type == "平均数":
        return len(elements["numbers"]) < 2
    return bool(warnings)


def _build_explanation(
    profile: dict[str, Any],
    needs_more_data: bool,
    warnings: list[str],
    computed_result: float | None,
    answer_candidate: dict[str, Any] | None,
) -> str:
    base = (
        f"本题初步按资料分析的{profile['question_type']}处理，优先调用"
        f"{'、'.join(profile['method_ids'])}。"
    )
    if needs_more_data:
        return base + " 当前题干信息不足，只能形成方法草案，不能给出精确答案。"
    if computed_result is not None and answer_candidate:
        return (
            base
            + f" 已完成简单考场估算，结果约为{computed_result:g}，最接近选项{answer_candidate['label']}；仍应按选项差距复核。"
        )
    if computed_result is not None:
        return base + f" 已完成简单考场估算，结果约为{computed_result:g}；这不是复杂精算结论。"
    if warnings:
        return base + " 题干可形成考场解题方向，但仍需按警告项核对口径和单位。"
    return base + " 可按步骤先定题型和口径，再结合选项差距选择估算策略。"


def _empty_result(
    matched_routes: list[dict[str, Any]], warnings: list[str], needs_more_data: bool
) -> dict[str, Any]:
    return {
        "module": DATA_ANALYSIS_MODULE,
        "question_type": "",
        "sub_type": "",
        "needs_more_data": needs_more_data,
        "matched_routes": matched_routes,
        "recommended_methods": [],
        "extracted_elements": {
            "time": [],
            "subject": [],
            "metrics": [],
            "numbers": [],
            "rates": [],
            "percentage_points": [],
            "units": [],
            "options": [],
            "option_values": [],
        },
        "option_gap_analysis": {
            "has_options": False,
            "gap_level": "unknown",
            "gap_notes": [],
            "recommended_precision": "unknown",
        },
        "formula_plan": {
            "formula": "",
            "variables": {},
            "missing_variables": [],
        },
        "estimation_plan": [],
        "solving_plan": [],
        "calculation_policy": {
            "allow_exact_calculation": False,
            "prefer_estimation": True,
            "must_check_option_gap": True,
            "forbidden": [],
        },
        "exam_style_explanation_draft": "",
        "computed_result": None,
        "answer_candidate": None,
        "source_method_ids": [],
        "warnings": warnings,
    }


def _extract_options(
    question_text: str, options: list[str] | dict[str, str] | None
) -> list[dict[str, Any]]:
    if isinstance(options, dict):
        return [_parse_option(str(key), str(value)) for key, value in options.items()]
    if isinstance(options, list):
        return [
            _parse_option(chr(ord("A") + index), str(value))
            for index, value in enumerate(options)
        ]
    parsed = [_parse_option(match.group(1), match.group(2).strip()) for match in OPTION_RE.finditer(question_text)]
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for option in parsed:
        key = f"{option['label']}:{option['raw']}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(option)
    return unique


def _parse_option(label: str, raw: str) -> dict[str, Any]:
    raw = raw.strip().rstrip("。；;，,")
    match = OPTION_VALUE_RE.search(raw)
    value = float(match.group("value")) if match else None
    unit = match.group("unit").replace("％", "%") if match and match.group("unit") else ""
    return {"label": label.upper(), "raw": raw, "value": value, "unit": unit}


def analyze_option_gaps(options: list[dict[str, Any]]) -> dict[str, Any]:
    numeric_options = [option for option in options if option.get("value") is not None]
    if len(numeric_options) < 2:
        return {
            "has_options": bool(options),
            "gap_level": "unknown",
            "gap_notes": ["选项不足或无法解析数值，暂不能判断选项差距。"] if options else [],
            "recommended_precision": "unknown",
        }

    values = sorted(float(option["value"]) for option in numeric_options)
    adjacent_gaps = [b - a for a, b in zip(values, values[1:]) if b >= a]
    min_gap = min(adjacent_gaps) if adjacent_gaps else 0.0
    span = values[-1] - values[0]
    baseline = max(abs(values[-1]), 1.0)
    relative_min_gap = min_gap / baseline
    if relative_min_gap >= 0.08 or span / baseline >= 0.3:
        return {
            "has_options": True,
            "gap_level": "large",
            "gap_notes": ["选项差距较大，可优先估算或截位。"],
            "recommended_precision": "2-3 significant digits",
        }
    if relative_min_gap <= 0.03:
        return {
            "has_options": True,
            "gap_level": "small",
            "gap_notes": ["选项差距较小，估算后需要更谨慎复核。"],
            "recommended_precision": "higher precision required",
        }
    return {
        "has_options": True,
        "gap_level": "medium",
        "gap_notes": ["选项差距中等，可先估算再按需要补算。"],
        "recommended_precision": "2-3 significant digits",
    }


def _build_formula_plan(
    question_type: str, question_text: str, elements: dict[str, Any]
) -> dict[str, Any]:
    amount_values = _amount_values(question_text)
    rate = _first_rate(question_text)
    variables: dict[str, Any] = {}
    missing: list[str] = []
    formula = ""

    if _looks_like_interval_inverse_growth(question_text):
        formula = "R2 = (1 + R间)/(1 + R1) - 1"
        rates = _extract_interval_inverse_rates(question_text)
        variables.update(rates)
        for key in ["R1", "R_interval"]:
            if key not in variables:
                missing.append(key)
    elif _looks_like_current_share_difference(question_text):
        formula = "两个现期比重差 = part1/whole1 - part2/whole2"
        shares = _parse_current_share_difference(question_text)
        if shares:
            variables.update(shares)
        else:
            missing.extend(["part1", "whole1", "part2", "whole2"])
    elif _looks_like_reverse_growth_rate_ranking(question_text):
        formula = "增长率 = 增长量 / (现期量 - 增长量)，按增长率排序"
        items = _parse_reverse_growth_rate_items(question_text)
        if items:
            variables["items"] = items
        else:
            missing.append("items")
    elif _looks_like_group_sum_ratio(question_text):
        formula = "分组倍数 = 分子组合计 / 分母组合计"
        grouped = _parse_group_sum_ratio(question_text)
        if grouped:
            variables.update(grouped)
        else:
            missing.extend(["分子组", "分母组"])
    elif _looks_like_cumulative_new_residual_share(question_text):
        formula = "基期残差小类占比 = (基期总数 - 基期大类 - 基期中类) / 基期总数"
        residual = _parse_cumulative_new_residual_share(question_text)
        if residual:
            variables.update(residual)
        else:
            missing.extend(["累计总数", "新增总数", "累计大类", "新增大类"])
    elif _looks_like_growth_amount_ranking(question_text):
        formula = "X = B × R / (1 + R)，按X从高到低排序"
        items = _parse_ranked_growth_items(question_text)
        if items:
            variables["items"] = items
        else:
            missing.append("items")
    elif _looks_like_base_share(question_text):
        formula = "基期比重 = A基期 / (A基期 + 其他基期)"
        items = _parse_amount_rate_items(question_text)
        if len(items) >= 2:
            variables["part"] = items[0]
            variables["other"] = items[1]
        else:
            missing.extend(["part", "other"][len(items) :])
    elif _looks_like_base_difference(question_text):
        formula = "基期差值 = (现期出口 - 现期进口)/(1 + R)；若R不同则分别求基期后相减"
        items = _parse_amount_rate_items(question_text)
        if len(items) >= 2:
            variables["left"] = items[0]
            variables["right"] = items[1]
        else:
            missing.extend(["left", "right"][len(items) :])
    elif _looks_like_time_segment_ratio(question_text):
        formula = "分段倍数 = (对象A累计 - 对象A单月) / (对象B累计 - 对象B单月)"
        segment = _parse_time_segment_ratio(question_text)
        if segment:
            variables.update(segment)
        else:
            missing.extend(["对象A累计", "对象A单月", "对象B累计", "对象B单月"])
    elif question_type == "基期量":
        formula = "A = B/(1+R)"
        if amount_values:
            variables["B"] = amount_values[0]
        else:
            missing.append("B")
        if rate is not None:
            variables["R"] = rate
        else:
            missing.append("R")
    elif question_type == "增长率":
        formula = "R = (B-A)/A"
        if len(amount_values) >= 2:
            variables["B"] = amount_values[0]
            variables["A"] = amount_values[1]
        else:
            missing.extend(["B", "A"][len(amount_values) :])
    elif question_type == "增长量":
        formula = "X = B × R / (1+R)"
        if amount_values:
            variables["B"] = amount_values[0]
        else:
            missing.append("B")
        if rate is not None:
            variables["R"] = rate
        else:
            missing.append("R")
    elif question_type == "比重":
        formula = "部分 / 整体"
        if "合计" in question_text and "总" in question_text and len(amount_values) >= 3:
            variables["part"] = {
                "value": sum(item["value"] for item in amount_values[1:3]),
                "unit": amount_values[1]["unit"],
                "raw": f"{amount_values[1]['raw']}+{amount_values[2]['raw']}",
            }
            variables["whole"] = amount_values[0]
        elif len(amount_values) >= 2:
            variables["part"] = amount_values[0]
            variables["whole"] = amount_values[1]
        else:
            missing.extend(["part", "whole"][len(amount_values) :])
    elif question_type == "比重变化":
        formula = "比重差 = 本期比重 - 基期比重；方向先看部分增速 vs 整体增速"
        if elements["percentage_points"]:
            variables["direct_percentage_point_change"] = elements["percentage_points"][0]
        else:
            missing.extend(["部分增速", "整体增速"])
    elif question_type == "平均数":
        formula = "平均数 = 总量 / 份数"
        if len(amount_values) >= 2:
            variables["total"] = amount_values[0]
            variables["count"] = amount_values[1]
        else:
            missing.extend(["total", "count"][len(amount_values) :])

    return {"formula": formula, "variables": variables, "missing_variables": missing}


def _compute_safe_estimate(
    question_type: str,
    question_text: str,
    elements: dict[str, Any],
    formula_plan: dict[str, Any],
) -> tuple[float | None, list[str], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    variables = formula_plan.get("variables", {})
    sub_calculations: list[dict[str, Any]] = []
    ranking_result: list[dict[str, Any]] = []
    formula_notes: list[str] = []
    if formula_plan.get("missing_variables"):
        if question_type == "比重变化" and variables.get("direct_percentage_point_change"):
            return None, [
                f"题干已直接给出{variables['direct_percentage_point_change']}，重点是识别百分点变化而非增长率。"
            ], sub_calculations, ranking_result, formula_notes
        return None, [], sub_calculations, ranking_result, formula_notes

    if _looks_like_interval_inverse_growth(question_text):
        r1 = variables["R1"]
        r_interval = variables["R_interval"]
        result = ((1 + r_interval) / (1 + r1) - 1) * 100
        result = _round_estimate(result)
        formula_notes.append("已知末期相对中间期增长率和末期相对基期增长率，反推中间期相对基期增长率。")
        sub_calculations.append({"name": "R2", "formula": "(1+R间)/(1+R1)-1", "value": result, "unit": "%"})
        return result, [
            f"按 R2 = (1+R间)/(1+R1)-1：1+R间={1+r_interval:g}，1+R1={1+r1:g}，估算约{result:g}%。"
        ], sub_calculations, ranking_result, formula_notes

    if _looks_like_current_share_difference(question_text):
        part1 = variables["part1"]["value"]
        whole1 = variables["whole1"]["value"]
        part2 = variables["part2"]["value"]
        whole2 = variables["whole2"]["value"]
        if whole1 == 0 or whole2 == 0:
            return None, ["整体量为0，不能计算比重差。"], sub_calculations, ranking_result, formula_notes
        share1 = part1 / whole1 * 100
        share2 = part2 / whole2 * 100
        diff = share1 - share2
        result = _round_estimate(diff)
        sub_calculations.extend(
            [
                {"name": "share1", "formula": "part1/whole1", "value": _round_estimate(share1), "unit": "%"},
                {"name": "share2", "formula": "part2/whole2", "value": _round_estimate(share2), "unit": "%"},
                {"name": "diff_pp", "formula": "share1-share2", "value": result, "unit": "百分点"},
            ]
        )
        formula_notes.append("两个现期比重作差，结果单位是百分点；先判高低方向，再匹配选项阈值。")
        direction = "高" if result >= 0 else "低"
        return result, [
            f"{part1:g}/{whole1:g}≈{_round_estimate(share1):g}%。",
            f"{part2:g}/{whole2:g}≈{_round_estimate(share2):g}%。",
            f"二者相差约{abs(result):g}个百分点，前者{direction}于后者。",
        ], sub_calculations, ranking_result, formula_notes

    if _looks_like_reverse_growth_rate_ranking(question_text):
        for item in variables["items"]:
            base = item["amount"] - item["growth_amount"]
            if base == 0:
                return None, [f"{item['label']}基期量为0，不能计算增长率。"], sub_calculations, ranking_result, formula_notes
            rate = item["growth_amount"] / base * 100
            sub_calculations.append(
                {
                    "label": item["label"],
                    "formula": "增长量/(现期量-增长量)",
                    "amount": item["amount"],
                    "growth_amount": item["growth_amount"],
                    "base": _round_estimate(base),
                    "value": _round_estimate(rate),
                    "unit": "%",
                }
            )
        reverse = _asks_ascending(question_text)
        ranking_result = sorted(sub_calculations, key=lambda item: item["value"], reverse=not reverse)
        sequence = " > ".join(item["label"] for item in ranking_result)
        formula_notes.append("给出现期量和增长量时，先反推基期量，再比较增长率；不能直接比较增长量。")
        return None, [
            "逐个对象用 增长率 = 增长量 / (现期量 - 增长量) 反推同比增速。",
            f"排序结果约为：{sequence}。",
        ], sub_calculations, ranking_result, formula_notes

    if _looks_like_group_sum_ratio(question_text):
        numerator = variables["numerator"]
        denominator = variables["denominator"]
        if denominator["sum"] == 0:
            return None, ["分母组合计为0，不能计算倍数。"], sub_calculations, ranking_result, formula_notes
        result = _round_estimate(numerator["sum"] / denominator["sum"])
        sub_calculations.extend(
            [
                {
                    "name": f"{numerator['name']}合计",
                    "formula": "组内项目求和",
                    "value": _round_estimate(numerator["sum"]),
                    "items": numerator["items"],
                    "unit": numerator["unit"],
                },
                {
                    "name": f"{denominator['name']}合计",
                    "formula": "组内项目求和",
                    "value": _round_estimate(denominator["sum"]),
                    "items": denominator["items"],
                    "unit": denominator["unit"],
                },
                {"name": "倍数", "formula": "分子组合计/分母组合计", "value": result},
            ]
        )
        formula_notes.append("分组求和后再求倍数，重点检查组内项目是否漏读。")
        return result, [
            f"{numerator['name']}合计≈{_format_sum_items(numerator['items'])}={_round_estimate(numerator['sum']):g}。",
            f"{denominator['name']}合计≈{_format_sum_items(denominator['items'])}={_round_estimate(denominator['sum']):g}。",
            f"倍数≈{_round_estimate(numerator['sum']):g}/{_round_estimate(denominator['sum']):g}≈{result:g}。",
        ], sub_calculations, ranking_result, formula_notes

    if _looks_like_cumulative_new_residual_share(question_text):
        total_base = variables["total_cumulative"] - variables["total_new"]
        large_base = variables["large_cumulative"] - variables["large_new"]
        medium_base = variables["medium_cumulative"] - variables["medium_new"]
        residual = total_base - large_base - medium_base
        if total_base == 0:
            return None, ["基期总数为0，不能计算占比。"], sub_calculations, ranking_result, formula_notes
        result = _round_estimate(residual / total_base * 100)
        sub_calculations.extend(
            [
                {"name": "基期总数", "formula": "累计总数-新增总数", "value": _round_estimate(total_base)},
                {"name": "基期大型", "formula": "累计大型-新增大型", "value": _round_estimate(large_base)},
                {"name": "基期中型", "formula": "累计中型-新增中型", "value": _round_estimate(medium_base)},
                {"name": "基期小型", "formula": "总数-大型-中型", "value": _round_estimate(residual)},
                {"name": "小型占比", "formula": "小型/总数", "value": result, "unit": "%"},
            ]
        )
        formula_notes.append("先用累计减新增还原上年末口径，再用残差得到小型数量。")
        return result, [
            f"基期总数 = 累计 - 新增 ≈ {variables['total_cumulative']:g}-{variables['total_new']:g}={_round_estimate(total_base):g}。",
            f"基期大型≈{variables['large_cumulative']:g}-{variables['large_new']:g}={_round_estimate(large_base):g}，基期中型≈{variables['medium_cumulative']:g}-{variables['medium_new']:g}={_round_estimate(medium_base):g}。",
            f"小型 = 总数 - 大型 - 中型 ≈ {_round_estimate(total_base):g}-{_round_estimate(large_base):g}-{_round_estimate(medium_base):g}={_round_estimate(residual):g}。",
            f"占比≈{_round_estimate(residual):g}/{_round_estimate(total_base):g}≈{result:g}%。",
        ], sub_calculations, ranking_result, formula_notes

    if _looks_like_growth_amount_ranking(question_text):
        for item in variables["items"]:
            r = item["rate"]
            value = item["amount"] * r / (1 + r)
            sub_calculations.append(
                {
                    "label": item["label"],
                    "formula": "B×R/(1+R)",
                    "B": item["amount"],
                    "R": r,
                    "value": _round_estimate(value),
                }
            )
        ranking_result = sorted(sub_calculations, key=lambda item: item["value"], reverse=True)
        sequence = "".join(item["label"] for item in ranking_result)
        formula_notes.append("下降对象的R按负数处理，增长量为负；排序先看正负，再看数量级。")
        return None, [
            "逐个对象用 X = B×R/(1+R) 估算同比增量。",
            f"从高到低排序约为：{sequence}。",
        ], sub_calculations, ranking_result, formula_notes

    if _looks_like_base_share(question_text):
        part = variables["part"]
        other = variables["other"]
        part_base = part["amount"] / (1 + part["rate"])
        other_base = other["amount"] / (1 + other["rate"])
        total_base = part_base + other_base
        result = part_base / total_base * 100 if total_base else None
        if result is None:
            return None, ["基期总量为0，不能计算基期比重。"], sub_calculations, ranking_result, formula_notes
        result = _round_estimate(result)
        sub_calculations.extend(
            [
                {"name": "A基期", "formula": "A现期/(1+RA)", "value": _round_estimate(part_base)},
                {"name": "其他基期", "formula": "其他现期/(1+R其他)", "value": _round_estimate(other_base)},
                {"name": "基期比重", "formula": "A基期/(A基期+其他基期)", "value": result, "unit": "%"},
            ]
        )
        formula_notes.append("这是基期比重，必须先分别还原分项基期量，不能直接用现期比重。")
        return result, [
            f"A基期≈{part['amount']:g}/(1{part['rate']:+g})≈{_round_estimate(part_base):g}。",
            f"其他基期≈{other['amount']:g}/(1{other['rate']:+g})≈{_round_estimate(other_base):g}。",
            f"基期比重≈{_round_estimate(part_base):g}/({_round_estimate(part_base):g}+{_round_estimate(other_base):g})≈{result:g}%。",
        ], sub_calculations, ranking_result, formula_notes

    if _looks_like_base_difference(question_text):
        left = variables["left"]
        right = variables["right"]
        if abs(left["rate"] - right["rate"]) < 1e-9:
            current_diff = left["amount"] - right["amount"]
            result = current_diff / (1 + left["rate"])
            sub_calculations.extend(
                [
                    {"name": "现期差", "formula": "现期左值-现期右值", "value": _round_estimate(current_diff)},
                    {"name": "基期差", "formula": "现期差/(1+R)", "value": _round_estimate(result)},
                ]
            )
            formula_notes.append("两个指标增长率相同，可先算现期差，再整体折回基期。")
            return _round_estimate(result), [
                f"现期差≈{left['amount']:g}-{right['amount']:g}={_round_estimate(current_diff):g}。",
                f"基期差≈{_round_estimate(current_diff):g}/(1+{left['rate']:g})≈{_round_estimate(result):g}。",
            ], sub_calculations, ranking_result, formula_notes
        left_base = left["amount"] / (1 + left["rate"])
        right_base = right["amount"] / (1 + right["rate"])
        result = left_base - right_base
        formula_notes.append("两个指标增长率不同，分别求基期量后相减。")
        return _round_estimate(result), [
            f"左值基期≈{_round_estimate(left_base):g}，右值基期≈{_round_estimate(right_base):g}，差值≈{_round_estimate(result):g}。"
        ], sub_calculations, ranking_result, formula_notes

    if _looks_like_time_segment_ratio(question_text):
        numerator = variables["numerator"]
        denominator = variables["denominator"]
        numerator_segment = numerator["cumulative"] - numerator["single"]
        denominator_segment = denominator["cumulative"] - denominator["single"]
        if denominator_segment == 0:
            return None, ["分母对象分段值为0，不能计算倍数。"], sub_calculations, ranking_result, formula_notes
        result = _round_estimate(numerator_segment / denominator_segment)
        sub_calculations.extend(
            [
                {
                    "name": f"{denominator['subject']}分段值",
                    "formula": "1-3月累计 - 3月单月",
                    "value": _round_estimate(denominator_segment),
                    "unit": denominator["unit"],
                },
                {
                    "name": f"{numerator['subject']}分段值",
                    "formula": "1-3月累计 - 3月单月",
                    "value": _round_estimate(numerator_segment),
                    "unit": numerator["unit"],
                },
                {"name": "倍数", "formula": "对象A分段值/对象B分段值", "value": result},
            ]
        )
        formula_notes.append("累计期先拆分到同一时间段，再求倍数。")
        return result, [
            f"{denominator['subject']}1-2月 = 1-3月累计 - 3月单月 ≈ {denominator['cumulative']:g}-{denominator['single']:g}={_round_estimate(denominator_segment):g}。",
            f"{numerator['subject']}1-2月 = 1-3月累计 - 3月单月 ≈ {numerator['cumulative']:g}-{numerator['single']:g}={_round_estimate(numerator_segment):g}。",
            f"倍数≈{_round_estimate(numerator_segment):g}/{_round_estimate(denominator_segment):g}≈{result:g}。",
        ], sub_calculations, ranking_result, formula_notes

    if question_type == "基期量":
        b = variables["B"]["value"]
        r = variables["R"]
        result = b / (1 + r)
        return _round_estimate(result), [f"按 A = B/(1+R)：{b:g}/(1+{r:g})，得到约{_round_estimate(result):g}。"], sub_calculations, ranking_result, formula_notes
    if question_type == "增长率":
        b = variables["B"]["value"]
        a = variables["A"]["value"]
        if a == 0:
            return None, ["基期量为0，不能计算增长率。"], sub_calculations, ranking_result, formula_notes
        result = (b - a) / a * 100
        return _round_estimate(result), [f"按 R = (B-A)/A：({b:g}-{a:g})/{a:g}，得到约{_round_estimate(result):g}%。"], sub_calculations, ranking_result, formula_notes
    if question_type == "增长量":
        b = variables["B"]["value"]
        r = variables["R"]
        result = b * r / (1 + r)
        plan = [f"按 X = B × R/(1+R)：{b:g}×{r:g}/(1+{r:g})，得到约{_round_estimate(result):g}。"]
        if abs(r - 0.1) < 0.005:
            plan.append(f"10%接近1/10，本期约11份，增长量可估为{b:g}/11≈{_round_estimate(b / 11):g}。")
        return _round_estimate(result), plan, sub_calculations, ranking_result, formula_notes
    if question_type == "比重":
        part = variables["part"]["value"]
        whole = variables["whole"]["value"]
        if whole == 0:
            return None, ["整体量为0，不能计算比重。"], sub_calculations, ranking_result, formula_notes
        result = part / whole * 100
        return _round_estimate(result), [f"按 部分/整体：{part:g}/{whole:g}，得到约{_round_estimate(result):g}%。"], sub_calculations, ranking_result, formula_notes
    if question_type == "比重变化" and variables.get("direct_percentage_point_change"):
        return None, [
            f"题干已直接给出比重提高/下降{variables['direct_percentage_point_change']}，不需要强行计算。"
        ], sub_calculations, ranking_result, formula_notes
    return None, [], sub_calculations, ranking_result, formula_notes


def _match_answer_candidate(
    computed_result: float | None,
    options: list[dict[str, Any]],
    ranking_result: list[dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    if ranking_result:
        sequence = "".join(item["label"] for item in ranking_result)
        normalized_sequence = _normalize_sequence_text(sequence)
        for option in options:
            normalized_raw = _normalize_sequence_text(option.get("raw", ""))
            if sequence in option.get("raw", "") or normalized_sequence in normalized_raw:
                return {
                    "label": option["label"],
                    "raw": option["raw"],
                    "value": option.get("value"),
                    "unit": option.get("unit", ""),
                    "reason": f"与排序结果 {sequence} 一致",
                }
    if computed_result is None:
        return None
    share_diff = _match_share_difference_option(computed_result, options)
    if share_diff:
        return share_diff
    interval = _match_interval_option(computed_result, options)
    if interval:
        return interval
    directional = _match_directional_percent_option(computed_result, options)
    if directional:
        return directional
    numeric_options = [option for option in options if option.get("value") is not None]
    if not numeric_options:
        return None
    best = min(numeric_options, key=lambda option: abs(float(option["value"]) - computed_result))
    return {
        "label": best["label"],
        "raw": best["raw"],
        "value": best["value"],
        "unit": best["unit"],
        "reason": f"与估算结果 {computed_result:g} 最接近",
    }


def _match_interval_option(computed_result: float, options: list[dict[str, Any]]) -> dict[str, Any] | None:
    for option in options:
        raw = option.get("raw", "")
        numbers = [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", raw)]
        if "以上" in raw and numbers and computed_result >= numbers[0]:
            reason = f"估算结果约为{computed_result:g}，落在{numbers[0]:g}以上"
        elif ("不到" in raw or "以下" in raw) and numbers and computed_result < numbers[0]:
            reason = f"估算结果约为{computed_result:g}，属于不到{numbers[0]:g}"
        elif len(numbers) >= 2 and ("之间" in raw or "-" in raw or "—" in raw or "~" in raw):
            low, high = sorted(numbers[:2])
            if not (low <= computed_result <= high):
                continue
            reason = f"估算结果约为{computed_result:g}，落在{low:g}-{high:g}之间"
        else:
            continue
        return {
            "label": option["label"],
            "raw": raw,
            "value": option.get("value"),
            "unit": option.get("unit", ""),
            "reason": reason,
        }
    return None


def _match_share_difference_option(
    computed_result: float, options: list[dict[str, Any]]
) -> dict[str, Any] | None:
    magnitude = abs(computed_result)
    direction = "高" if computed_result >= 0 else "低"
    opposite = "低" if direction == "高" else "高"
    for option in options:
        raw = option.get("raw", "")
        value = option.get("value")
        if value is None or "百分点" not in raw or opposite in raw or direction not in raw:
            continue
        if "以上" in raw and magnitude >= float(value):
            reason = f"估算结果约为{computed_result:g}个百分点，属于{direction}{value:g}个百分点以上"
        elif ("不到" in raw or "以内" in raw) and magnitude < float(value):
            reason = f"估算结果约为{computed_result:g}个百分点，属于{direction}不到{value:g}个百分点"
        else:
            continue
        return {
            "label": option["label"],
            "raw": raw,
            "value": value,
            "unit": option.get("unit", ""),
            "reason": reason,
        }
    return None


def _match_directional_percent_option(
    computed_result: float, options: list[dict[str, Any]]
) -> dict[str, Any] | None:
    for option in options:
        raw = option.get("raw", "")
        if computed_result < 0 and abs(computed_result) < 10 and "下降不到10" in raw:
            reason = f"估算结果约为{computed_result:g}%，属于下降不到10%"
        elif computed_result < 0 and abs(computed_result) >= 10 and "下降10" in raw and "以上" in raw:
            reason = f"估算结果约为{computed_result:g}%，属于下降10%以上"
        elif computed_result > 0 and abs(computed_result) < 10 and "增长不到10" in raw:
            reason = f"估算结果约为{computed_result:g}%，属于增长不到10%"
        elif computed_result > 0 and abs(computed_result) >= 10 and "增长10" in raw and "以上" in raw:
            reason = f"估算结果约为{computed_result:g}%，属于增长10%以上"
        else:
            continue
        return {
            "label": option["label"],
            "raw": raw,
            "value": option.get("value"),
            "unit": option.get("unit", ""),
            "reason": reason,
        }
    return None


def _amount_values(question_text: str) -> list[dict[str, Any]]:
    return [
        {"value": float(match.group("value")), "unit": match.group("unit"), "raw": match.group(0)}
        for match in AMOUNT_RE.finditer(question_text)
    ]


def _parse_reverse_growth_rate_items(question_text: str) -> list[dict[str, Any]]:
    text = _strip_options(question_text)
    clauses = re.split(r"[；;。]", text)
    pattern = re.compile(
        r"(?P<label>[\u4e00-\u9fa5A-Za-z]{1,12}?)\s*"
        r"(?P<amount>\d+(?:\.\d+)?)\s*"
        r"(?P<unit>亿美元|万美元|美元|万亿元|亿元|万元|元|亿件|万件|件|万套|套|万亩|亩|座|万人|万人次|人|万吨|吨|公里|平方公里)"
        r"[^；;。]*?(?P<direction>增加|增长|减少|下降)\s*"
        r"(?P<growth>\d+(?:\.\d+)?)\s*(?P=unit)"
    )
    items: list[dict[str, Any]] = []
    for clause in clauses:
        for match in pattern.finditer(clause):
            growth_amount = float(match.group("growth"))
            if match.group("direction") in {"减少", "下降"}:
                growth_amount = -growth_amount
            label = _clean_subject_label(match.group("label"))
            items.append(
                {
                    "label": label,
                    "amount": float(match.group("amount")),
                    "growth_amount": growth_amount,
                    "unit": match.group("unit"),
                    "raw": match.group(0),
                }
            )
    return items


def _parse_group_sum_ratio(question_text: str) -> dict[str, Any]:
    group_names = _extract_group_ratio_names(question_text)
    if not group_names:
        return {}
    numerator_name, denominator_name = group_names
    material_text = _strip_options(question_text).split("问", 1)[0]
    numerator = _parse_group_items(material_text, numerator_name)
    denominator = _parse_group_items(material_text, denominator_name)
    if not numerator or not denominator:
        return {}
    return {
        "numerator": {"name": numerator_name, **numerator},
        "denominator": {"name": denominator_name, **denominator},
    }


def _extract_group_ratio_names(question_text: str) -> tuple[str, str] | None:
    match = re.search(
        r"问.*?([\u4e00-\u9fa5]{2,12}?[一二三四五六七八九十]?省)[\u4e00-\u9fa5]*?是"
        r".*?([\u4e00-\u9fa5]{2,12}?[一二三四五六七八九十]?省).*?(?:多少|几)倍",
        question_text,
    )
    if match:
        return _trim_group_name(match.group(1)), _trim_group_name(match.group(2))
    return None


def _trim_group_name(name: str) -> str:
    for known in ["中部六省", "东北三省"]:
        if known in name:
            return known
    return name.strip("，,。；;：: 的")


def _parse_group_items(material_text: str, group_name: str) -> dict[str, Any]:
    clauses = [clause for clause in re.split(r"[；;。]", material_text) if group_name in clause]
    if not clauses:
        return {}
    values = _amount_values(clauses[0])
    if not values:
        return {}
    unit = values[0]["unit"]
    items = [{"raw": value["raw"], "value": value["value"], "unit": value["unit"]} for value in values]
    return {"items": items, "sum": sum(item["value"] for item in items), "unit": unit}


def _parse_cumulative_new_residual_share(question_text: str) -> dict[str, Any]:
    material_text = _strip_options(question_text)
    split_match = re.search(r"\d{4}年\s*新增", material_text)
    if not split_match:
        return {}
    cumulative_text = material_text[: split_match.start()]
    new_text = material_text[split_match.start() :]
    total_cumulative = _first_amount_value(cumulative_text)
    total_new = _first_amount_value(new_text)
    large_cumulative = _amount_after_keyword(cumulative_text, "大型")
    medium_cumulative = _amount_after_keyword(cumulative_text, "中型")
    large_new = _amount_after_keyword(new_text, "大型")
    medium_new = _amount_after_keyword(new_text, "中型")
    if None in {total_cumulative, total_new, large_cumulative, medium_cumulative, large_new, medium_new}:
        return {}
    return {
        "total_cumulative": total_cumulative,
        "total_new": total_new,
        "large_cumulative": large_cumulative,
        "large_new": large_new,
        "medium_cumulative": medium_cumulative,
        "medium_new": medium_new,
    }


def _first_amount_value(text: str) -> float | None:
    values = _amount_values(text)
    if not values:
        return None
    return values[0]["value"]


def _amount_after_keyword(text: str, keyword: str) -> float | None:
    match = re.search(
        re.escape(keyword)
        + r"[^。；;，,]*?(?P<value>\d+(?:\.\d+)?)\s*(?:座|万件|件|万套|套|万亩|亩|亿元|亿美元)",
        text,
    )
    if not match:
        return None
    return float(match.group("value"))


def _strip_options(question_text: str) -> str:
    return re.split(r"\s*A(?:[\.、:：])", question_text, maxsplit=1)[0]


def _clean_subject_label(label: str) -> str:
    label = re.sub(r"^.*?(投诉|举报|咨询)$", r"\1", label)
    return label.strip("，,。；;：: 的其中")


def _asks_ascending(question_text: str) -> bool:
    return "从低到高" in question_text or "由小到大" in question_text


def _format_sum_items(items: list[dict[str, Any]]) -> str:
    return "+".join(f"{item['value']:g}" for item in items)


def _normalize_sequence_text(text: str) -> str:
    return re.sub(r"[\s、，,；;。:：.]+", "", text).replace("量", "")


def _parse_current_share_difference(question_text: str) -> dict[str, Any]:
    values = _amount_values(question_text)
    if len(values) < 4:
        return {}
    return {
        "part1": values[0],
        "whole1": values[1],
        "part2": values[2],
        "whole2": values[3],
    }


def _parse_time_segment_ratio(question_text: str) -> dict[str, Any]:
    subjects = _extract_ratio_subjects(question_text)
    if not subjects:
        return {}
    numerator_subject, denominator_subject = subjects
    single_text, cumulative_text = _split_single_and_cumulative_text(question_text)
    numerator_single = _amount_for_subject(single_text, numerator_subject)
    denominator_single = _amount_for_subject(single_text, denominator_subject)
    numerator_cumulative = _amount_for_subject(cumulative_text, numerator_subject)
    denominator_cumulative = _amount_for_subject(cumulative_text, denominator_subject)
    if not all([numerator_single, denominator_single, numerator_cumulative, denominator_cumulative]):
        return {}
    return {
        "numerator": {
            "subject": numerator_subject,
            "single": numerator_single["value"],
            "cumulative": numerator_cumulative["value"],
            "unit": numerator_single["unit"],
        },
        "denominator": {
            "subject": denominator_subject,
            "single": denominator_single["value"],
            "cumulative": denominator_cumulative["value"],
            "unit": denominator_single["unit"],
        },
    }


def _extract_ratio_subjects(question_text: str) -> tuple[str, str] | None:
    match = re.search(
        r"问.*?([\u4e00-\u9fa5A-Za-z]+?机器人).*?是.*?([\u4e00-\u9fa5A-Za-z]+?机器人).*?(?:多少|几)倍",
        question_text,
    )
    if match:
        return _normalize_robot_subject(match.group(1)), _normalize_robot_subject(match.group(2))
    return None


def _normalize_robot_subject(subject: str) -> str:
    for known in ["服务机器人", "工业机器人"]:
        if known in subject:
            return known
    return subject.split("的")[-1]


def _split_single_and_cumulative_text(question_text: str) -> tuple[str, str]:
    parts = re.split(r"\d{4}年\s*1\s*[-~至]\s*3月[^。；;]*?累计", question_text, maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    before, _, after = question_text.partition("累计")
    return before, after


def _amount_for_subject(text: str, subject: str) -> dict[str, Any] | None:
    pattern = re.compile(
        re.escape(subject)
        + r"[^。；;，,]*?(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>万套|套|亿美元|万美元|美元|万亿元|亿元|万元|元|亿件|万件|件|万人|万人次|人|万吨|吨|公里|平方公里)"
    )
    match = pattern.search(text)
    if not match:
        return None
    return {"value": float(match.group("value")), "unit": match.group("unit"), "raw": match.group(0)}


def _parse_amount_rate_items(question_text: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"(?P<name>[^；;。]*?)(?P<amount>\d+(?:\.\d+)?)\s*(?P<unit>亿美元|万美元|美元|万亿元|亿元|万元|元|亿件|万件|件|万人|万人次|人|万吨|吨|公里|平方公里)"
        r"[^；;。]*?同比(?P<direction>增长|下降)\s*(?P<rate>\d+(?:\.\d+)?)\s*(?:%|％)"
    )
    items = []
    for index, match in enumerate(pattern.finditer(question_text), start=1):
        signed_rate = float(match.group("rate")) / 100
        if match.group("direction") == "下降":
            signed_rate = -signed_rate
        items.append(
            {
                "label": str(index),
                "name": match.group("name").strip("，,：: "),
                "amount": float(match.group("amount")),
                "unit": match.group("unit"),
                "rate": signed_rate,
                "direction": match.group("direction"),
                "raw": match.group(0),
            }
        )
    return items


def _parse_ranked_growth_items(question_text: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"(?P<label>[①②③④⑤⑥])\s*(?P<amount>\d+(?:\.\d+)?)\s*(?P<unit>亿美元|万美元|美元|万亿元|亿元|万元|元|亿件|万件|件|万人|万人次|人|万吨|吨|公里|平方公里)"
        r"[^；;。]*?同比(?P<direction>增长|下降)\s*(?P<rate>\d+(?:\.\d+)?)\s*(?:%|％)"
    )
    items = []
    for match in pattern.finditer(question_text):
        signed_rate = float(match.group("rate")) / 100
        if match.group("direction") == "下降":
            signed_rate = -signed_rate
        items.append(
            {
                "label": match.group("label"),
                "amount": float(match.group("amount")),
                "unit": match.group("unit"),
                "rate": signed_rate,
                "direction": match.group("direction"),
                "raw": match.group(0),
            }
        )
    return items


def _extract_interval_inverse_rates(question_text: str) -> dict[str, float]:
    rates: dict[str, float] = {}
    r1_match = re.search(
        r"同比(?P<direction>增长|下降)?\s*(?P<rate>\d+(?:\.\d+)?)\s*(?:%|％)",
        question_text,
    )
    interval_match = YEAR_COMPARISON_RATE_RE.search(question_text)
    if r1_match:
        rates["R1"] = _signed_rate_from_match(r1_match)
    if interval_match:
        rates["R_interval"] = _signed_rate_from_match(interval_match)
    return rates


def _signed_rate_from_match(match: re.Match[str]) -> float:
    rate = float(match.group("rate")) / 100
    if match.groupdict().get("direction") == "下降":
        return -rate
    return rate


def _first_rate(question_text: str) -> float | None:
    for match in RATE_RE.finditer(question_text):
        raw = match.group(0).replace("％", "%").replace(" ", "")
        if raw.endswith("个百分点"):
            continue
        if raw.endswith("%"):
            return float(raw[:-1]) / 100
    return None


def _round_estimate(value: float) -> float:
    rounded = round(value, 4)
    if abs(rounded - round(rounded)) < 1e-9:
        return float(round(rounded))
    return rounded


def _unique(values: Any) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result
