from __future__ import annotations

from pathlib import Path

from xingce_solver.solvers import solve_logic_reasoning


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"


REAL_CASES = [
    (
        "LR-001",
        "D",
        "削弱",
        "某网络安全团队提出一种新方案：在软件系统中主动加入大量“良性漏洞”，让攻击者在扫描时被大量无害信息干扰，从而减少真正危险漏洞被利用的概率。研究人员据此认为，这种方案可以显著提高系统安全性。以下哪项如果为真，最能削弱上述观点？"
        "A. 添加良性漏洞需要额外的开发与维护成本。"
        "B. 不同类型的软件系统对安全防护的需求并不相同。"
        "C. 有些企业在部署新系统前会进行第三方安全评估。"
        "D. 经验丰富的攻击者通常能够快速识别并忽略良性漏洞，继续针对真正危险的漏洞发起攻击。",
    ),
    (
        "LR-002",
        "A",
        "削弱",
        "某机构宣传称，市场上标注为“儿童食品”的产品比普通食品更适合儿童，也更营养健康。因此，家长在为孩子挑选食品时，应优先购买儿童食品。以下哪项如果为真，最能质疑上述观点？"
        "A. 多项检测显示，不少所谓儿童食品在营养成分上与普通同类食品差别并不明显，部分产品甚至糖和盐含量更高。"
        "B. 儿童食品的外包装通常更加鲜艳，更容易吸引孩子注意。"
        "C. 一些家长购买儿童食品时会更关注品牌知名度。"
        "D. 儿童食品在销售渠道上通常集中在大型商超和电商平台。",
    ),
    (
        "LR-003",
        "A",
        "加强",
        "有研究者认为，人类的嗅觉能力在漫长进化过程中不断减弱，现代人的嗅觉已经明显不如远古时期敏锐。以下哪项如果为真，最能支持上述观点？"
        "A. 与远古人类相比，现代人负责气味识别和处理的某些相关脑区与基因功能出现了明显退化迹象。"
        "B. 现代社会中，人们识别气味的场景远比古代更加多样化。"
        "C. 一些哺乳动物的嗅觉能力明显强于现代人类。"
        "D. 嗅觉在不同文化中的重要性存在较大差异。",
    ),
    (
        "LR-004",
        "D",
        "加强",
        "考古研究者认为，丹尼索瓦人很可能曾长期生活在青藏高原地区。以下各项如果为真，除哪项外，均能支持上述观点？"
        "A. 在青藏高原相关遗址中发现了与丹尼索瓦人基因特征高度吻合的人类遗骸信息。"
        "B. 当地现代居民中存在可追溯到古人群的高原低氧适应基因，而该基因与丹尼索瓦人有关。"
        "C. 高原地区发现的部分古人类活动遗迹，其年代与丹尼索瓦人已知活动时期相吻合。"
        "D. 青藏高原地区生态环境复杂多样，适合多种古人类和动物群体活动与迁徙。",
    ),
    (
        "LR-005",
        "D",
        "前提假设",
        "有学者认为，生物对苦味的敏感感知是一种重要的防御机制，因为它能够帮助个体在摄入食物前对潜在有害物质发出预警。上述论证若要成立，最需要假设以下哪项？"
        "A. 生物对甜味和咸味的感知同样具有适应意义。"
        "B. 苦味感知能力在不同物种之间存在明显差异。"
        "C. 许多无毒食物也可能带有一定苦味。"
        "D. 自然界中大量有毒或有害物质都具有苦味特征，苦味能够在一定程度上提示风险。",
    ),
    (
        "LR-006",
        "D",
        "前提假设",
        "某研究团队开发出一种人工智能系统，可以通过分析受检者的视网膜图像来识别潜在心血管风险。研究者据此认为，这种技术未来有望改变传统心脏病筛查方式。上述论证若要成立，最需要假设以下哪项？"
        "A. 视网膜图像采集设备的成本会逐步降低。"
        "B. 医疗机构愿意尝试使用人工智能辅助诊断工具。"
        "C. 受检者对无创筛查技术的接受度普遍较高。"
        "D. 视网膜中的某些特征变化能够稳定、有效地反映心血管疾病风险，因而可用于可靠筛查。",
    ),
    (
        "LR-008",
        "B",
        "解释说明",
        "调查显示，某地区0—6个月婴儿纯母乳喂养率明显偏低，相关部门希望找出导致这一现象的原因。以下各项如果为真，除哪项外，均能解释上述现象？"
        "A. 一些新手母亲担心自己泌乳不足，较早添加了配方奶。"
        "B. 大多数母亲都认同母乳喂养对婴儿生长发育有益。"
        "C. 部分用人单位缺乏完善的哺乳支持措施，影响了母亲持续母乳喂养。"
        "D. 一些家庭成员认为婴儿只喝母乳不够“有营养”，从而建议尽早添加其他食物。",
    ),
    (
        "LR-009",
        "A",
        "结论推出",
        "研究者在比较不同年代人群的智力测验结果时发现，近几十年来，多国人群在同类测验中的平均得分普遍高于更早时期的对应人群。这种长期出现的平均分提升现象被称为“弗林效应”。根据上述信息，可以推出的是："
        "A. 在相同或相近类型的智力测验中，后期人群的平均成绩整体上往往高于早期人群。"
        "B. 弗林效应说明所有国家居民的智力水平都在持续快速上升。"
        "C. 经济越发达的国家，智力测验平均分一定越高。"
        "D. 只要一个国家教育投入增加，该国居民平均智商就必然上升。",
    ),
    (
        "LR-010",
        "C",
        "结论推出",
        "某市规定，对每个投入使用的一次性塑料餐盒统一征收2元处理费。统计显示，近三年来，该市一次性塑料餐盒的使用数量持续下降。根据上述信息，可以推出的是："
        "A. 近三年来，餐饮企业的整体利润一定持续下降。"
        "B. 近三年来，市民对堂食的偏好一定显著提高。"
        "C. 如果其他条件不变，近三年来该市因一次性塑料餐盒征收的处理费收入总体上趋于下降。"
        "D. 近三年来，可重复使用餐盒的使用量一定同比例上升。",
    ),
]


def test_v3_real_cases_cautious_answer_selection() -> None:
    results = {
        case_id: solve_logic_reasoning(text, kb_dir=KB_DIR)
        for case_id, _answer, _expected_type, text in REAL_CASES
    }

    null_count = 0
    correct_count = 0
    wrong_count = 0
    for case_id, answer, _expected_type, _text in REAL_CASES:
        candidate = results[case_id]["answer_candidate"]
        if candidate is None:
            null_count += 1
        elif candidate["label"] == answer:
            correct_count += 1
        else:
            wrong_count += 1

    assert null_count < len(REAL_CASES)
    assert correct_count >= 4
    assert wrong_count <= 2


def test_v3_real_cases_type_and_reverse_direction() -> None:
    results = {
        case_id: solve_logic_reasoning(text, kb_dir=KB_DIR)
        for case_id, _answer, _expected_type, text in REAL_CASES
    }

    assert results["LR-004"]["question_stem_analysis"]["is_reverse_question"] is True
    assert results["LR-004"]["question_stem_analysis"]["reverse_question_type"] == "except"
    assert results["LR-008"]["question_stem_analysis"]["is_reverse_question"] is True
    assert results["LR-008"]["question_stem_analysis"]["reverse_question_type"] == "except"

    assert results["LR-005"]["question_type"] == "前提假设"
    assert results["LR-006"]["question_type"] == "前提假设"
    assert results["LR-009"]["question_type"] == "结论推出"
    assert results["LR-010"]["question_type"] == "结论推出"


def test_v3_output_fields_are_stable() -> None:
    result = solve_logic_reasoning(REAL_CASES[0][3], kb_dir=KB_DIR)

    assert result["version"] == "v6.1"
    assert result["solver_version"] == "v7 conservative truth integration"
    assert result["decision_status"] in {"candidate_ready", "analysis_only", "needs_manual_review"}
    assert isinstance(result["confidence"], float)
    assert isinstance(result["high_risk_warnings"], list)
