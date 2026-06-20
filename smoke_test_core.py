# -*- coding: utf-8 -*-
"""Smoke test for xingce-solver v0.5.1 release."""

import sys
from pathlib import Path

def main():
    print(f"Python version: {sys.version}")

    import xingce_solver
    print(f"xingce_solver: {xingce_solver.__file__}")

    import xingce_solver.mcp_server
    print("mcp_server import ok")

    from xingce_solver.mcp_server import tool_route_xingce_question, tool_compose_xingce_answer_prompt
    print("core tool imports ok")

    # Test 1: short verbal with module_hint
    r = tool_route_xingce_question(
        question_text="作者接下来最可能论述的是：",
        options={"A": "问题产生的原因", "B": "具体解决措施", "C": "相关历史背景", "D": "不同观点比较"},
        strict_mode=True,
        module_hint="言语理解"
    )
    print(f"short verbal route: {r.get('module_guess')} module_hint_applied={r.get('module_hint_applied')}")
    assert r.get("module_guess") == "verbal_reasoning"
    assert r.get("module_hint_applied") == True

    # Test 2: relationship graph with module_hint
    r = tool_route_xingce_question(
        question_text="人际关系图是指用节点和连线表示个体之间关系的一种图示方法。下列属于人际关系图的是：",
        options={"A": "用点表示人员、用线表示朋友关系的图", "B": "某地区年度GDP统计表", "C": "某产品销售额折线图", "D": "某班考试成绩柱状图"},
        strict_mode=True,
        module_hint="定义判断"
    )
    print(f"relationship graph route: {r.get('module_guess')} module_hint_applied={r.get('module_hint_applied')}")
    assert r.get("module_guess") == "definition_judgement"
    assert r.get("module_hint_applied") == True

    # Test 3: chart data with strong material signal
    r = tool_compose_xingce_answer_prompt(
        question_text="图中数据显示，第三季度销售额占全年销售额的比重约为多少？",
        options={"A": "18%", "B": "24%", "C": "31%", "D": "39%"},
        strict_mode=True,
        allow_answer=True,
        image_present=False,
        visual_description="",
        material_present=False,
        material_text="",
        table_present=False,
        module_hint="数量关系"
    )
    print(f"chart data answer_allowed: {r.get('answer_allowed')}")
    print(f"block: {r.get('answer_block_reason')}")
    print(f"requires_material: {r.get('context_requirements', {}).get('requires_table_or_material')}")
    assert r.get("answer_allowed") == False
    assert r.get("answer_block_reason") == "missing_table_or_material"
    assert r.get("context_requirements", {}).get("requires_table_or_material") == True

    # Test 4: plain graph with module_hint
    r = tool_compose_xingce_answer_prompt(
        question_text="下图是一种关系图示，用于说明概念之间的包含关系。下列符合上述定义的是：",
        options={"A": "用圆圈表示概念范围", "B": "用表格统计产量", "C": "用折线展示增长率", "D": "用柱状图比较销量"},
        strict_mode=True,
        allow_answer=True,
        image_present=False,
        visual_description="",
        material_present=False,
        material_text="",
        table_present=False,
        module_hint="定义判断"
    )
    print(f"plain graph answer_allowed: {r.get('answer_allowed')}")
    print(f"block: {r.get('answer_block_reason')}")
    print(f"requires_material: {r.get('context_requirements', {}).get('requires_table_or_material')}")
    assert r.get("answer_allowed") == True
    assert r.get("context_requirements", {}).get("requires_table_or_material") == False

    # Knowledge base check
    cards = sum(1 for _ in Path("knowledge_base/all_cards.jsonl").open(encoding="utf-8"))
    print(f"cards: {cards}")
    assert cards == 292

    print("\n=== ALL SMOKE TESTS PASSED ===")

if __name__ == "__main__":
    main()
