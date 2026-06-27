from pathlib import Path

from xingce_solver.solvers import solve_logic_reasoning


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"


def _method_ids(result: dict) -> set[str]:
    return {method["method_id"] for method in result["recommended_methods"]}


def test_weaken_question_draft() -> None:
    result = solve_logic_reasoning(
        "某研究认为，经常喝茶的人更健康。因此，喝茶可以提高健康水平。以下哪项最能削弱上述论证？A.健康的人更可能有喝茶习惯 B.喝茶的人通常也更爱运动 C.部分人喝茶后睡眠变差 D.茶叶价格逐年上涨",
        kb_dir=KB_DIR,
    )

    assert result["module"] == "判断推理"
    assert result["question_type"] == "削弱"
    assert {"lj_weaken_evidence_conclusion_001", "lj_attribution_general_001"} & _method_ids(result)
    assert result["argument_structure"]["conclusion"]
    assert result["argument_structure"]["premises"]
    assert result["option_analysis"]


def test_strengthen_question_draft() -> None:
    result = solve_logic_reasoning(
        "某公司发现使用新培训系统的员工销售额更高。因此，新培训系统能提升销售能力。以下哪项最能加强上述论证？A.使用该系统的员工在培训前销售额与其他员工相近 B.该系统价格较高 C.部分员工不喜欢培训 D.公司今年扩大了办公面积",
        kb_dir=KB_DIR,
    )

    assert result["question_type"] == "加强"
    assert {"lj_support_general_001", "lj_support_bridge_001"} & _method_ids(result)
    assert result["option_analysis"]


def test_premise_question_draft() -> None:
    result = solve_logic_reasoning(
        "某地计划通过增加夜间公交班次来减少私家车出行。因此，该措施能缓解晚高峰拥堵。要使上述论证成立，必须补充以下哪项作为前提？A.夜间公交班次增加后会吸引原本开车的人乘坐公交 B.公交车颜色统一 C.该地白天游客较多 D.私家车车主都喜欢音乐",
        kb_dir=KB_DIR,
    )

    assert result["question_type"] == "前提假设"
    assert {"lj_premise_general_001", "lj_premise_bridge_001"} & _method_ids(result)
    rendered = " ".join(result["solving_plan"])
    assert "否定代入" in rendered or "必要条件" in rendered


def test_explanation_question_draft() -> None:
    result = solve_logic_reasoning(
        "某市共享单车投放量减少，但市民骑行共享单车的总次数却上升。以下哪项最能解释上述现象？A.剩余车辆被调度到需求更高的区域 B.该市地铁票价下降 C.共享单车颜色变多 D.部分道路正在维修",
        kb_dir=KB_DIR,
    )

    assert result["question_type"] == "解释说明"
    assert "lj_explanation_contradiction_001" in _method_ids(result)
    rendered = " ".join(result["solving_plan"])
    assert "解释矛盾" in rendered or "同时解释现象" in rendered
