from pathlib import Path

from xingce_solver.mcp_server import tool_solve_data_analysis
from xingce_solver.solvers import solve_data_analysis


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"


def _method_ids(result: dict) -> set[str]:
    return {method["method_id"] for method in result["recommended_methods"]}


def test_share_change_draft() -> None:
    result = solve_data_analysis(
        "2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？",
        kb_dir=KB_DIR,
    )

    assert result["module"] == "资料分析"
    assert result["question_type"] == "比重变化"
    assert "da_share_change_004" in _method_ids(result)
    assert any("先判断方向" in step or "百分点" in step for step in result["solving_plan"])


def test_growth_rate_draft() -> None:
    result = solve_data_analysis(
        "某地区2020年产值为120亿元，2019年为100亿元，问2020年同比增长率约为多少？",
        kb_dir=KB_DIR,
    )

    assert "da_growth_rate_general_001" in _method_ids(result)
    assert any("120" in number for number in result["extracted_elements"]["numbers"])
    assert any("100" in number for number in result["extracted_elements"]["numbers"])
    assert any("R = X / A" in step or "(B-A)/A" in step for step in result["solving_plan"])


def test_base_amount_draft() -> None:
    result = solve_data_analysis(
        "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？",
        kb_dir=KB_DIR,
    )

    assert result["question_type"] == "基期量"
    assert "da_abx_base_direct_001" in _method_ids(result)
    assert any("A = B/(1+R)" in step for step in result["solving_plan"])
    assert result["formula_plan"]["formula"] == "A = B/(1+R)"
    assert result["computed_result"] == 120.0


def test_insufficient_share_change_has_warnings() -> None:
    result = solve_data_analysis(
        "某产业占比提高了0.3个百分点，问该产业比重变化是多少？",
        kb_dir=KB_DIR,
    )

    assert result["warnings"]
    assert "recommended_methods" in result
    rendered = " ".join(result["warnings"] + result["solving_plan"])
    assert "部分量" not in rendered or "缺少" in rendered
    assert result["computed_result"] is None


def test_mcp_solve_data_analysis_tool() -> None:
    result = tool_solve_data_analysis(
        "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？",
        kb_dir=KB_DIR,
    )

    assert result["module"] == "资料分析"
    assert result["question_type"] == "基期量"
    assert "da_abx_base_direct_001" in result["source_method_ids"]


def test_base_amount_with_options_matches_c() -> None:
    result = solve_data_analysis(
        "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？ A.100亿元 B.110亿元 C.120亿元 D.132亿元",
        kb_dir=KB_DIR,
    )

    assert "da_abx_base_direct_001" in _method_ids(result)
    assert "A = B/(1+R)" in result["formula_plan"]["formula"]
    assert abs(result["computed_result"] - 120) < 0.01
    assert result["answer_candidate"]["label"] == "C"
    assert result["option_gap_analysis"]["has_options"] is True


def test_growth_rate_with_options_matches_c() -> None:
    result = solve_data_analysis(
        "某地区2020年产值为120亿元，2019年为100亿元，问2020年同比增长率约为多少？ A.10% B.15% C.20% D.25%",
        kb_dir=KB_DIR,
    )

    assert "da_growth_rate_general_001" in _method_ids(result)
    assert result["formula_plan"]["formula"] == "R = (B-A)/A"
    assert abs(result["computed_result"] - 20) < 0.01
    assert result["answer_candidate"]["label"] == "C"


def test_current_share_with_options_matches_b() -> None:
    result = solve_data_analysis(
        "某地区第一产业增加值为200亿元，地区生产总值为1000亿元，第一产业占比为多少？ A.10% B.20% C.30% D.40%",
        kb_dir=KB_DIR,
    )

    assert "da_share_current_001" in _method_ids(result)
    assert result["formula_plan"]["formula"] == "部分 / 整体"
    assert abs(result["computed_result"] - 20) < 0.01
    assert result["answer_candidate"]["label"] == "B"


def test_growth_amount_draft_uses_parts_estimation() -> None:
    result = solve_data_analysis(
        "2020年某产业收入为132亿元，同比增长10%，问同比增加了多少亿元？",
        kb_dir=KB_DIR,
    )

    assert "da_growth_amount_001" in _method_ids(result)
    assert result["formula_plan"]["formula"] == "X = B × R / (1+R)"
    assert abs(result["computed_result"] - 12) < 0.01
    assert any("11份" in step or "132/11" in step for step in result["estimation_plan"])


def test_direct_share_change_does_not_force_calculation() -> None:
    result = solve_data_analysis(
        "2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？",
        kb_dir=KB_DIR,
    )

    assert "da_share_change_004" in _method_ids(result)
    assert result["percentage_points"] if "percentage_points" in result else result["extracted_elements"]["percentage_points"]
    assert result["computed_result"] is None
    assert any("百分点" in step for step in result["solving_plan"] + result["estimation_plan"])


def test_insufficient_share_change_sets_needs_more_data() -> None:
    result = solve_data_analysis("某产业占比发生变化，问变化多少？", kb_dir=KB_DIR)

    assert result["needs_more_data"] is True
    assert result["warnings"]
    assert result["computed_result"] is None


def test_interval_inverse_growth_estimate() -> None:
    result = solve_data_analysis(
        "2021年，某类商品出口额为1702.8亿美元，同比增长24.0%，且比2019年增长16.0%。问2020年该类商品出口额比2019年约为：A.下降不到10% B.下降10%以上 C.增长不到10% D.增长10%以上",
        kb_dir=KB_DIR,
    )

    assert "da_growth_rate_interval_002" in _method_ids(result)
    assert "R2 = (1 + R间)/(1 + R1) - 1" == result["formula_plan"]["formula"]
    assert abs(result["computed_result"] - (-6.5)) <= 0.5
    assert result["answer_candidate"]["label"] == "A"


def test_interval_inverse_growth_accepts_jiao_expression() -> None:
    result = solve_data_analysis(
        "2021年，某类商品出口额为1702.8亿美元，同比增长24.0%，且较2019年增长16.0%。问2020年该类商品出口额比2019年约为：A.下降不到10% B.下降10%以上 C.增长不到10% D.增长10%以上",
        kb_dir=KB_DIR,
    )

    assert result["sub_type"] == "间隔增长率/逆向增长率"
    assert "da_growth_rate_interval_002" in _method_ids(result)
    assert result["formula_plan"]["formula"] == "R2 = (1 + R间)/(1 + R1) - 1"
    assert abs(result["computed_result"] - (-6.5)) <= 0.5
    assert result["answer_candidate"]["label"] == "A"


def test_growth_amount_ranking_matches_d() -> None:
    result = solve_data_analysis(
        "2021年，某国对四个地区出口额分别为：①563.5亿美元，同比增长4.0%；②491.2亿美元，同比增长24.9%；③469.9亿美元，同比下降11.1%；④200.3亿美元，同比下降7.2%。按2021年同比增量从高到低排序，正确的是：A.①②③④ B.①②④③ C.②①③④ D.②①④③",
        kb_dir=KB_DIR,
    )

    assert "da_growth_amount_compare_002" in _method_ids(result)
    assert [item["label"] for item in result["ranking_result"]] == ["②", "①", "④", "③"]
    assert result["answer_candidate"]["label"] == "D"


def test_growth_amount_ranking_accepts_pailie_expression() -> None:
    result = solve_data_analysis(
        "2021年，某国对四个地区出口额分别为：①563.5亿美元，同比增长4.0%；②491.2亿美元，同比增长24.9%；③469.9亿美元，同比下降11.1%；④200.3亿美元，同比下降7.2%。按2021年同比增量从高到低排列，正确的是：A.①②③④ B.①②④③ C.②①③④ D.②①④③",
        kb_dir=KB_DIR,
    )

    assert result["sub_type"] == "增长量比较"
    assert "da_growth_amount_compare_002" in _method_ids(result)
    assert [item["label"] for item in result["ranking_result"]] == ["②", "①", "④", "③"]
    assert result["answer_candidate"]["label"] == "D"


def test_base_share_two_components_matches_c() -> None:
    result = solve_data_analysis(
        "2021年，某类产品A出口额为129.5亿美元，同比下降76.0%；除A外的其他同类产品出口额为517.2亿美元，同比增长27.5%。问2020年A在该类产品总出口额中的占比约为：A.33% B.45% C.57% D.72%",
        kb_dir=KB_DIR,
    )

    assert "da_share_base_002" in _method_ids(result)
    assert result["formula_plan"]["formula"] == "基期比重 = A基期 / (A基期 + 其他基期)"
    assert abs(result["computed_result"] - 57) <= 1
    assert result["answer_candidate"]["label"] == "C"


def test_base_difference_same_growth_rate_matches_a() -> None:
    result = solve_data_analysis(
        "2021年，某国对某区域出口额为1137.9亿美元，同比增长24.5%；自该区域进口额为131.6亿美元，同比增长24.5%。问2020年该国对该区域贸易顺差约为多少亿美元？A.808 B.1006 C.1129 D.1253",
        kb_dir=KB_DIR,
    )

    assert "da_abx_base_diff_003" in _method_ids(result)
    assert result["formula_plan"]["formula"].startswith("基期差值")
    assert abs(result["computed_result"] - 808) <= 1
    assert result["answer_candidate"]["label"] == "A"


def test_current_share_difference_matches_a() -> None:
    result = solve_data_analysis(
        "热线电话投诉304498件，投诉总件数556063件；热线电话举报61021件，举报总件数263129件。问热线电话投诉占投诉总件数的比重，比热线电话举报占举报总件数的比重高/低多少？A.高20个百分点以上 B.低20个百分点以上 C.高不到20个百分点 D.低不到20个百分点",
        kb_dir=KB_DIR,
    )

    assert {"da_share_change_004", "da_ratio_share_diff_005"} & _method_ids(result)
    assert result["sub_type"] == "两个现期比重差/百分点差"
    assert abs(result["computed_result"] - 31.6) <= 0.5
    assert result["answer_candidate"]["label"] == "A"
    rendered = " ".join(result["solving_plan"] + result["estimation_plan"])
    assert "百分点" in rendered


def test_time_segment_ratio_matches_a() -> None:
    result = solve_data_analysis(
        "2023年3月，工业机器人完成产量4.4万套，服务机器人完成产量70万套；2023年1-3月累计，工业机器人完成产量10.4万套，服务机器人完成产量145万套。问2023年1-2月，服务机器人完成产量约是工业机器人完成产量的多少倍？A.12.5 B.14.0 C.15.9 D.18.1",
        kb_dir=KB_DIR,
    )

    assert "da_time_segments_001" in _method_ids(result)
    assert result["sub_type"] == "时间分段后求倍数"
    assert abs(result["computed_result"] - 12.5) <= 0.1
    assert result["answer_candidate"]["label"] == "A"
    rendered = " ".join(result["solving_plan"] + result["estimation_plan"])
    assert "1-3月累计 - 3月单月" in rendered


def test_reverse_growth_rate_ranking_matches_d() -> None:
    result = solve_data_analysis(
        "投诉55.6万件，比上年增加14.0万件；举报26.3万件，增加8.9万件；咨询138.5万件，增加16.0万件。按2022年同比增速从高到低排序，正确的是：A.投诉量、举报量、咨询量 B.咨询量、投诉量、举报量 C.举报量、咨询量、投诉量 D.举报量、投诉量、咨询量",
        kb_dir=KB_DIR,
    )

    assert "da_growth_rate_general_001" in _method_ids(result)
    assert result["sub_type"] == "多对象现期量+增长量反推增速排序"
    assert [item["label"] for item in result["ranking_result"]] == ["举报", "投诉", "咨询"]
    assert result["answer_candidate"]["label"] == "D"
    rendered = " ".join(result["solving_plan"] + result["estimation_plan"])
    assert "增长率 = 增长量 / (现期量 - 增长量)" in rendered


def test_group_sum_ratio_matches_a() -> None:
    result = solve_data_analysis(
        "中部六省新增恢复灌溉面积分别为安徽27.6万亩、江西15.0万亩、河南11.2万亩、湖北26.2万亩、湖南27.0万亩、山西6.3万亩；东北三省分别为辽宁1.8万亩、吉林9.4万亩、黑龙江13.4万亩。问中部六省新增恢复灌溉面积是东北三省的多少倍？A.4.5-5倍之间 B.4-4.5倍之间 C.不到4倍 D.5倍以上",
        kb_dir=KB_DIR,
    )

    assert "da_truncate_division_001" in _method_ids(result)
    assert result["sub_type"] == "分组求和后求倍数"
    assert abs(result["computed_result"] - 4.6) <= 0.1
    assert result["answer_candidate"]["label"] == "A"
    rendered = " ".join(result["solving_plan"] + result["estimation_plan"])
    assert "中部六省合计" in rendered
    assert "东北三省合计" in rendered


def test_cumulative_new_residual_share_matches_d() -> None:
    result = solve_data_analysis(
        "截至2022年末，全国累计投运电站472座，其中大型26座、中型275座。2022年新增投运电站194座，其中大型19座、中型114座。问截至2021年末，小型电站数量占比约为多少？A.20% B.30% C.35% D.40%",
        kb_dir=KB_DIR,
    )

    assert {"da_time_segments_001", "da_share_current_001"} <= _method_ids(result)
    assert result["sub_type"] == "累计减新增+残差小类基期占比"
    assert abs(result["computed_result"] - 39.6) <= 0.5
    assert result["answer_candidate"]["label"] == "D"
    rendered = " ".join(result["solving_plan"] + result["estimation_plan"])
    assert "累计 - 新增" in rendered
    assert "小型 = 总数 - 大型 - 中型" in rendered
