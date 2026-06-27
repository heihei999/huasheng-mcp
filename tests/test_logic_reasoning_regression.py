import subprocess
import sys
from pathlib import Path

from xingce_solver.mcp_server import (
    tool_classify_question,
    tool_get_method_card,
    tool_get_source_reference,
    tool_search_methods,
    tool_solve_data_analysis,
    tool_solve_logic_reasoning,
)
from xingce_solver.solvers import solve_logic_reasoning


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"


def _method_ids(result: dict) -> set[str]:
    return {method["method_id"] for method in result["recommended_methods"]}


def test_logic_reasoning_stable_structure_and_conservative_answer() -> None:
    result = solve_logic_reasoning(
        "某研究认为，经常喝茶的人更健康。因此，喝茶可以提高健康水平。以下哪项最能削弱上述论证？A.健康的人更可能有喝茶习惯 B.喝茶的人通常也更爱运动 C.部分人喝茶后睡眠变差 D.茶叶价格逐年上涨",
        kb_dir=KB_DIR,
    )

    for key in [
        "module",
        "question_type",
        "sub_type",
        "recommended_methods",
        "argument_structure",
        "question_stem_analysis",
        "option_analysis",
        "answer_candidate",
        "source_method_ids",
        "warnings",
    ]:
        assert key in result
    assert result["answer_candidate"] is None
    assert result["recommended_methods"]
    assert result["source_method_ids"]


def test_logic_reasoning_sub_type_coverage() -> None:
    cases = [
        (
            "削弱",
            "某调查显示，使用电子书的学生阅读量更高。因此，电子书能提升阅读兴趣。以下哪项最能削弱上述论证？A.阅读兴趣高的学生更愿意使用电子书 B.电子书价格下降 C.纸质书仍受欢迎 D.学校图书馆延长开放时间",
        ),
        (
            "加强",
            "某公司发现使用新培训系统的员工销售额更高。因此，新培训系统能提升销售能力。以下哪项最能加强上述论证？A.使用该系统的员工在培训前销售额与其他员工相近 B.系统界面是蓝色 C.公司换了门牌 D.部分员工请假",
        ),
        (
            "前提假设",
            "某地计划通过增加夜间公交班次来减少私家车出行。因此，该措施能缓解晚高峰拥堵。要使上述论证成立，必须补充以下哪项作为前提？A.夜间公交会吸引原本开车的人 B.公交车颜色统一 C.白天游客较多 D.司机喜欢音乐",
        ),
        (
            "解释说明",
            "某市共享单车投放量减少，但市民骑行共享单车的总次数却上升。以下哪项最能解释上述现象？A.剩余车辆被调度到需求更高的区域 B.地铁票价下降 C.单车颜色变多 D.道路维修",
        ),
        (
            "结论推出",
            "所有参加培训的人都通过了测试，小王参加了培训。由此可以推出哪项？A.小王通过了测试 B.小王没有参加测试 C.所有人都参加培训 D.没有人通过测试",
        ),
    ]

    for expected_type, text in cases:
        result = solve_logic_reasoning(text, kb_dir=KB_DIR)
        assert result["question_type"] == expected_type
        assert result["sub_type"]
        assert result["recommended_methods"]


def test_cannot_infer_is_conclusion_inference_direction() -> None:
    result = solve_logic_reasoning(
        "有些甲是乙，所有乙都是丙。根据上述信息，以下哪项不能推出？A.有些甲是丙 B.所有甲都是丙 C.有些乙是丙 D.乙都属于丙",
        kb_dir=KB_DIR,
    )

    assert result["question_type"] == "结论推出"
    assert result["sub_type"] == "基础推出"
    assert "lj_conclusion_translation_001" in _method_ids(result)
    assert result["answer_candidate"] is None


def test_options_parameter_parsing_and_method_fields() -> None:
    result = solve_logic_reasoning(
        "某研究显示，常运动的人睡眠更好。因此，运动可以改善睡眠。以下哪项最能支持上述论证？",
        options={
            "A": "运动前两组人的睡眠质量相近",
            "B": "运动服价格较高",
            "C": "部分人不喜欢运动",
            "D": "该研究地点在南方",
        },
        kb_dir=KB_DIR,
    )

    assert [item["label"] for item in result["option_analysis"]] == ["A", "B", "C", "D"]
    assert "lj_support_general_001" in _method_ids(result)
    assert result["source_method_ids"]


def test_old_cli_solve_data_and_solve_logic_still_run() -> None:
    solve_data = subprocess.run(
        [
            sys.executable,
            "-m",
            "xingce_solver.cli",
            "solve-data",
            "--text",
            "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？ A.100亿元 B.110亿元 C.120亿元 D.132亿元",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert solve_data.returncode == 0
    assert "题型判断" in solve_data.stdout

    solve_logic = subprocess.run(
        [
            sys.executable,
            "-m",
            "xingce_solver.cli",
            "solve-logic",
            "--text",
            "某研究认为，经常喝茶的人更健康。因此，喝茶可以提高健康水平。以下哪项最能削弱上述论证？A.健康的人更可能有喝茶习惯 B.喝茶的人通常也更爱运动 C.部分人喝茶后睡眠变差 D.茶叶价格逐年上涨",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert solve_logic.returncode == 0
    assert "选项分析" in solve_logic.stdout


def test_mcp_old_tools_and_logic_tool_still_exist() -> None:
    assert tool_get_method_card("da_share_change_004", KB_DIR)["card"]["id"] == "da_share_change_004"
    assert tool_search_methods("比重 增长率", kb_dir=KB_DIR)["results"]
    assert tool_classify_question("占比变化", kb_dir=KB_DIR)["matches"]
    assert tool_get_source_reference("da_share_change_004", KB_DIR)["source_file"]
    assert tool_solve_data_analysis("2020年收入132亿元，同比增长10%，问2019年收入？", kb_dir=KB_DIR)

    logic = tool_solve_logic_reasoning(
        "某研究认为，经常喝茶的人更健康。因此，喝茶可以提高健康水平。以下哪项最能削弱上述论证？A.健康的人更可能有喝茶习惯 B.喝茶的人通常也更爱运动 C.部分人喝茶后睡眠变差 D.茶叶价格逐年上涨",
        kb_dir=KB_DIR,
    )
    assert logic["question_type"] == "削弱"
