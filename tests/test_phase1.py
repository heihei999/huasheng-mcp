from pathlib import Path

from xingce_solver import (
    classify_question,
    get_method_card,
    get_source_reference,
    load_cards,
    search_methods,
)


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"


def test_all_cards_can_be_loaded() -> None:
    cards = load_cards(KB_DIR)

    assert cards
    assert len(cards) == 292


def test_get_method_card_by_id() -> None:
    card = get_method_card("da_share_change_004", KB_DIR)

    assert card is not None
    assert card["id"] == "da_share_change_004"
    assert card["module"] == "资料分析"


def test_search_methods_returns_relevant_cards() -> None:
    results = search_methods("比重 增长率", top_k=5, kb_dir=KB_DIR)

    assert results
    assert any(card["module"] == "资料分析" for card in results)
    assert any(
        "比重" in " ".join(
            [
                str(card.get("question_type", "")),
                str(card.get("sub_type", "")),
                str(card.get("method_name", "")),
                " ".join(card.get("tags", [])),
            ]
        )
        for card in results
    )


def test_classify_question_by_keywords() -> None:
    cases = [
        ("某项占比比上年提高，且给出部分增长率和整体增长率。", "资料分析"),
        ("材料问增长率为多少，已知现期和基期。", "资料分析"),
        ("以下哪项最能削弱上述论证？", "判断推理-逻辑判断"),
        ("这段文字的主旨是？", "言语理解-主旨意图"),
    ]

    for question, expected_module in cases:
        matches = classify_question(question, KB_DIR)
        modules = {match["module"] for match in matches}
        assert expected_module in modules


def test_get_source_reference() -> None:
    reference = get_source_reference("da_share_change_004", KB_DIR)

    assert reference is not None
    assert reference["id"] == "da_share_change_004"
    assert reference["source_file"]
    assert reference["source_page"]
