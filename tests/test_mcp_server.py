from pathlib import Path

from xingce_solver.mcp_server import (
    tool_classify_question,
    tool_get_method_card,
    tool_get_source_reference,
    tool_search_methods,
    tool_solve_data_analysis,
    tool_solve_logic_reasoning,
)


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"


def test_mcp_get_method_card() -> None:
    result = tool_get_method_card("da_share_change_004", KB_DIR)

    assert result["method_id"] == "da_share_change_004"
    assert result["card"]["id"] == "da_share_change_004"
    assert result["card"]["method_name"] == "比重差公式与秒杀法"


def test_mcp_search_methods() -> None:
    result = tool_search_methods("比重 增长率", top_k=5, kb_dir=KB_DIR)

    assert result["query"] == "比重 增长率"
    assert len(result["results"]) == 5
    assert all("method_id" in item for item in result["results"])
    assert all(isinstance(item["score"], float) for item in result["results"])


def test_mcp_classify_question() -> None:
    result = tool_classify_question(
        "2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？",
        kb_dir=KB_DIR,
    )

    first = result["matches"][0]
    assert first["module"] == "资料分析"
    assert first["question_type"] == "比重变化"
    assert first["priority_method_id"] == "da_share_change_004"
    assert first["matched_triggers"] == ["占比变化"]


def test_mcp_get_source_reference() -> None:
    result = tool_get_source_reference("da_share_change_004", KB_DIR)

    assert result["method_id"] == "da_share_change_004"
    assert result["source_file"]
    assert result["source_page"]
    assert result["confidence"] == 0.93
    assert result["need_review"] is False


def test_mcp_solve_data_analysis() -> None:
    result = tool_solve_data_analysis(
        "2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？",
        kb_dir=KB_DIR,
    )

    assert result["module"] == "资料分析"
    assert result["question_type"] == "比重变化"
    assert "da_share_change_004" in result["source_method_ids"]


def test_mcp_solve_logic_reasoning() -> None:
    result = tool_solve_logic_reasoning(
        "某研究认为，经常喝茶的人更健康。因此，喝茶可以提高健康水平。以下哪项最能削弱上述论证？A.健康的人更可能有喝茶习惯 B.喝茶的人通常也更爱运动 C.部分人喝茶后睡眠变差 D.茶叶价格逐年上涨",
        kb_dir=KB_DIR,
    )

    assert result["module"] == "判断推理"
    assert result["question_type"] == "削弱"
    assert "lj_weaken_evidence_conclusion_001" in result["source_method_ids"]
