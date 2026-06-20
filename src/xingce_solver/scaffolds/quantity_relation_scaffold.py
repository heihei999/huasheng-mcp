"""
Quantity relation method scaffold (guidance only, NOT a solver).

Provides structured thinking order, problem-type routing, method checklists,
option verification templates, and uncertainty constraints for future
LLM-based reasoning.

This module does NOT output answers. It does NOT integrate with CLI/MCP.
"""
from __future__ import annotations

from typing import Any


def build_quantity_relation_scaffold() -> dict[str, Any]:
    """Build the complete quantity relation method scaffold."""
    return {
        "module": "quantity_relation",
        "version": "v0.1",
        "mode": "method_scaffold_only",
        "positioning": (
            "本模块不是 solver。"
            "本模块不直接计算答案。"
            "本模块不直接选择选项。"
            "本模块用于约束大模型按数量关系方法识别题型、抽取已知量/未知量、统一单位、建立模型、验证选项，并在无法唯一时 analysis_only。"
        ),
        "stage_order": [
            "题型识别",
            "问法识别",
            "已知量抽取",
            "未知量设定",
            "单位统一",
            "方法选择",
            "模型建立",
            "计算/代入验证",
            "量级检查",
            "唯一性判断",
            "不确定性约束",
        ],
        "problem_type_router": {
            "工程问题": {
                "signals": ["工作总量", "效率", "时间", "合作", "交替", "休息"],
                "modeling_focus": "工作总量=效率×时间，赋值法设总量为效率公倍数",
                "preferred_method": "赋值法/方程法",
                "risk": "多人交替工作模式复杂、效率变化规则不明确",
                "analysis_only_when": ["效率变化规则不明确", "多人交替工作模式复杂", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "行程问题": {
                "signals": ["路程", "速度", "时间", "相遇", "追及", "流水", "扶梯", "过桥"],
                "modeling_focus": "路程=速度×时间，比例法，速度和/差",
                "preferred_method": "比例法/方程法",
                "risk": "变形题多（8子类型），自然语言建模复杂",
                "analysis_only_when": ["变形题型超出基础模型", "多次相遇条件复杂", "约束不足"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "经济利润问题": {
                "signals": ["成本", "售价", "利润", "折扣", "利润率", "打折"],
                "modeling_focus": "利润率=(售价-成本)/成本，列方程",
                "preferred_method": "方程法",
                "risk": "多批销售条件复杂",
                "analysis_only_when": ["多批销售条件复杂", "资金往来路径不明确", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "浓度/溶液混合问题": {
                "signals": ["浓度", "溶质", "溶液", "混合", "蒸发", "加水"],
                "modeling_focus": "溶质守恒，十字相乘求比例",
                "preferred_method": "方程法/十字交叉法",
                "risk": "多次混合条件复杂",
                "analysis_only_when": ["多次混合条件复杂", "浓度变化规则不明确", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "比例/倍数问题": {
                "signals": ["比例", "倍数", "占", "是...的", "比...多/少"],
                "modeling_focus": "设未知数为1份，利用比例关系",
                "preferred_method": "比例法/赋值法",
                "risk": "多层比例嵌套",
                "analysis_only_when": ["多层比例嵌套", "约束不足"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "年龄问题": {
                "signals": ["年龄", "几岁", "过去", "将来", "年龄差"],
                "modeling_focus": "年龄差不变，时间平移",
                "preferred_method": "方程法",
                "risk": "单卡覆盖有限",
                "analysis_only_when": ["条件不足", "多代人关系复杂"],
                "feasibility": "C_scaffold_only",
            },
            "容斥/集合问题": {
                "signals": ["至少", "至多", "都", "都不", "有的", "圈"],
                "modeling_focus": "A∪B=A+B-A∩B，三集合扩展",
                "preferred_method": "图表辅助/公式法",
                "risk": "最值容斥需构造",
                "analysis_only_when": ["三集合以上条件复杂", "最值容斥无法构造", "约束不足"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "排列组合": {
                "signals": ["排列", "组合", "选", "排", "种", "多少种方法"],
                "modeling_focus": "有序排列P，无序组合C，分类加法分步乘法",
                "preferred_method": "分类讨论/公式法",
                "risk": "自然语言建模复杂，组合爆炸",
                "analysis_only_when": ["排列组合类型不明确", "约束条件复杂", "无法可靠建模"],
                "feasibility": "C_scaffold_only",
            },
            "概率问题": {
                "signals": ["概率", "可能性", "机会", "抽到", "选中"],
                "modeling_focus": "符合情况/所有可能情况，几何概型用面积比",
                "preferred_method": "公式法/枚举法",
                "risk": "依赖排列组合建模",
                "analysis_only_when": ["概率模型不明确", "依赖复杂排列组合", "约束不足"],
                "feasibility": "C_scaffold_only",
            },
            "几何问题": {
                "signals": ["面积", "体积", "周长", "边长", "圆", "三角形", "对称"],
                "modeling_focus": "公式计算，对称展开，极值构造",
                "preferred_method": "公式法/构造极端",
                "risk": "几何最值和一笔画需特殊构造",
                "analysis_only_when": ["几何构造复杂", "需要图形理解", "约束不足"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "数列问题": {
                "signals": ["第n项", "前n项和", "公差", "公比", "递推"],
                "modeling_focus": "等差/等比/递推公式",
                "preferred_method": "公式法",
                "risk": "递推数列规律识别",
                "analysis_only_when": ["规律不明确", "非标准数列", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "方程/不定方程": {
                "signals": ["方程", "未知数", "整数解", "正整数"],
                "modeling_focus": "列方程，奇偶/整除/代入筛选",
                "preferred_method": "方程法/枚举法",
                "risk": "不定方程整数解筛选",
                "analysis_only_when": ["方程组无唯一解", "不定方程筛选条件不足", "约束不足"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "最值问题": {
                "signals": ["最多", "最少", "最大", "最小", "至多", "至少"],
                "modeling_focus": "构造极端，和定最值，最不利构造",
                "preferred_method": "构造极端",
                "risk": "构造性强，需极端思维",
                "analysis_only_when": ["构造方式不唯一", "约束条件复杂", "无法可靠构造"],
                "feasibility": "C_scaffold_only",
            },
            "牛吃草": {
                "signals": ["牛", "草", "生长", "原有"],
                "modeling_focus": "原有草+生长草=牛吃草，三步法",
                "preferred_method": "公式法",
                "risk": "条件变形",
                "analysis_only_when": ["条件变形超出标准模型", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "鸡兔同笼": {
                "signals": ["鸡兔同笼", "头", "脚", "理论最大值", "实际值"],
                "modeling_focus": "假设全为一种，差值法",
                "preferred_method": "公式法/代入排除",
                "risk": "多于两种动物",
                "analysis_only_when": ["多于两种动物", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "日期星期问题": {
                "signals": ["星期", "日期", "天数", "闰年", "平年"],
                "modeling_focus": "粗算修正日期差法",
                "preferred_method": "公式法",
                "risk": "闰年判断",
                "analysis_only_when": ["日期条件复杂", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "抽屉原理": {
                "signals": ["至少", "保证", "鸽巢", "抽屉"],
                "modeling_focus": "最不利构造+1",
                "preferred_method": "构造极端",
                "risk": "当前无卡片覆盖",
                "analysis_only_when": ["条件复杂", "无法可靠构造"],
                "feasibility": "D_defer",
            },
            "统筹优化": {
                "signals": ["最优", "最少时间", "最短路径", "统筹", "安排"],
                "modeling_focus": "低耗优先，等待时间最小化",
                "preferred_method": "构造极端/枚举法",
                "risk": "策略性强，需统筹思维",
                "analysis_only_when": ["统筹条件复杂", "无法可靠建模"],
                "feasibility": "C_scaffold_only",
            },
            "特征余数": {
                "signals": ["除以", "余", "余同", "和同", "差同"],
                "modeling_focus": "余同取余/和同加和/差同减差口诀",
                "preferred_method": "公式法",
                "risk": "不满足口诀特征时需转枚举",
                "analysis_only_when": ["不满足口诀特征", "范围条件不足"],
                "feasibility": "A_solver_first",
            },
            "盈亏问题": {
                "signals": ["盈", "亏", "多出", "不足"],
                "modeling_focus": "盈数亏数除以分配标准差",
                "preferred_method": "公式法",
                "risk": "条件变形",
                "analysis_only_when": ["条件变形超出标准模型", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "方阵问题": {
                "signals": ["方阵", "最外层", "层人数"],
                "modeling_focus": "最外层边长平方与层人数公式",
                "preferred_method": "公式法",
                "risk": "多层方阵",
                "analysis_only_when": ["多层方阵条件复杂", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "植树问题": {
                "signals": ["植树", "两端", "一端", "环形", "间隔"],
                "modeling_focus": "两端/一端/环形/两端不植树公式",
                "preferred_method": "公式法",
                "risk": "重合问题",
                "analysis_only_when": ["重合条件复杂", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "比赛问题": {
                "signals": ["比赛", "循环赛", "淘汰赛", "轮空", "场次"],
                "modeling_focus": "循环赛/淘汰赛/轮空规则",
                "preferred_method": "公式法",
                "risk": "轮空规则复杂",
                "analysis_only_when": ["轮空规则复杂", "约束不足"],
                "feasibility": "A_solver_first",
            },
            "其他": {
                "signals": [],
                "modeling_focus": "按具体题型分析",
                "preferred_method": "按具体题型选择",
                "risk": "题型不确定",
                "analysis_only_when": ["题型无法识别", "约束不足"],
                "feasibility": "C_scaffold_only",
            },
        },
        "problem_type_checklists": {
            "工程问题": {
                "signals": ["工作总量", "效率", "时间", "合作", "交替", "休息"],
                "quantities_to_extract": ["工作总量", "每人效率", "工作时间", "合作方式"],
                "modeling_steps": [
                    "设工作总量为效率公倍数（赋值法）",
                    "计算每人效率",
                    "根据合作方式列方程",
                    "求解时间或工作量",
                ],
                "verification": ["回代题干检查效率×时间=总量", "检查合作方式是否正确"],
                "analysis_only_when": ["效率变化规则不明确", "多人交替工作模式复杂"],
            },
            "行程问题": {
                "signals": ["路程", "速度", "时间", "相遇", "追及", "流水", "扶梯", "过桥"],
                "quantities_to_extract": ["路程", "速度", "时间", "方向"],
                "modeling_steps": [
                    "判断基础行程/相遇/追及/流水/扶梯/过桥",
                    "列路程=速度×时间",
                    "相遇用速度和，追及用速度差",
                    "流水用船速±水速",
                ],
                "verification": ["回代题干检查路程=速度×时间", "检查方向是否正确"],
                "analysis_only_when": ["变形题型超出基础模型", "多次相遇条件复杂"],
            },
            "经济利润问题": {
                "signals": ["成本", "售价", "利润", "折扣", "利润率"],
                "quantities_to_extract": ["成本", "售价", "利润", "利润率", "折扣"],
                "modeling_steps": [
                    "列利润率=(售价-成本)/成本",
                    "根据折扣调整售价",
                    "列方程求解",
                ],
                "verification": ["回代检查利润率公式", "检查折扣计算"],
                "analysis_only_when": ["多批销售条件复杂", "资金往来路径不明确"],
            },
            "浓度/溶液混合问题": {
                "signals": ["浓度", "溶质", "溶液", "混合", "蒸发"],
                "quantities_to_extract": ["浓度", "溶质质量", "溶液质量"],
                "modeling_steps": [
                    "列溶质守恒方程",
                    "或用十字相乘求比例",
                    "求解未知量",
                ],
                "verification": ["回代检查溶质守恒", "检查浓度计算"],
                "analysis_only_when": ["多次混合条件复杂", "浓度变化规则不明确"],
            },
            "容斥/集合问题": {
                "signals": ["至少", "至多", "都", "都不", "有的"],
                "quantities_to_extract": ["集合A人数", "集合B人数", "交集人数", "并集人数"],
                "modeling_steps": [
                    "画韦恩图或列公式",
                    "A∪B=A+B-A∩B",
                    "三集合扩展公式",
                ],
                "verification": ["回代检查集合关系", "检查人数合理性"],
                "analysis_only_when": ["三集合以上条件复杂", "最值容斥无法构造"],
            },
            "排列组合": {
                "signals": ["排列", "组合", "选", "排", "种"],
                "quantities_to_extract": ["元素个数", "选取个数", "顺序要求", "限制条件"],
                "modeling_steps": [
                    "判断有序排列还是无序组合",
                    "分类讨论或分步计算",
                    "处理相邻/不相邻/定序等特殊条件",
                ],
                "verification": ["检查是否遗漏分类", "检查排列组合公式"],
                "analysis_only_when": ["排列组合类型不明确", "约束条件复杂"],
            },
            "概率问题": {
                "signals": ["概率", "可能性", "抽到", "选中"],
                "quantities_to_extract": ["总情况数", "符合条件情况数", "概率模型"],
                "modeling_steps": [
                    "确定概率模型（古典/几何）",
                    "计算符合条件情况数",
                    "计算概率",
                ],
                "verification": ["检查概率在0-1之间", "检查情况数计算"],
                "analysis_only_when": ["概率模型不明确", "依赖复杂排列组合"],
            },
            "鸡兔同笼": {
                "signals": ["鸡兔同笼", "头", "脚", "理论最大值"],
                "quantities_to_extract": ["总头数", "总脚数", "每种动物脚数"],
                "modeling_steps": [
                    "假设全为一种动物",
                    "计算差值",
                    "求解另一种动物数量",
                ],
                "verification": ["回代检查头数和脚数"],
                "analysis_only_when": ["多于两种动物", "约束不足"],
            },
            "日期星期问题": {
                "signals": ["星期", "日期", "天数", "闰年"],
                "quantities_to_extract": ["起始日期", "目标日期", "天数差"],
                "modeling_steps": [
                    "计算天数差",
                    "除以7取余",
                    "推算星期",
                ],
                "verification": ["检查闰年判断", "检查天数计算"],
                "analysis_only_when": ["日期条件复杂", "约束不足"],
            },
            "特征余数": {
                "signals": ["除以", "余", "余同", "和同", "差同"],
                "quantities_to_extract": ["除数列表", "余数列表", "范围条件"],
                "modeling_steps": [
                    "判断余同/和同/差同特征",
                    "求除数LCM",
                    "写表达式M*n+常数",
                    "结合范围求解",
                ],
                "verification": ["检查余数条件", "检查范围条件"],
                "analysis_only_when": ["不满足口诀特征", "范围条件不足"],
            },
            "牛吃草": {
                "signals": ["牛", "草", "生长", "原有"],
                "quantities_to_extract": ["牛数", "天数", "原有草量", "生长速度"],
                "modeling_steps": [
                    "列原有草+生长草=牛吃草",
                    "用两组条件求生长速度",
                    "求原有草量",
                    "计算目标天数或牛数",
                ],
                "verification": ["回代检查草量守恒"],
                "analysis_only_when": ["条件变形超出标准模型"],
            },
        },
        "method_checklists": {
            "代入排除": {
                "scenarios": ["选项为具体数值", "题干条件可用选项验证"],
                "steps": ["逐项代入选项", "检查是否满足全部条件", "排除不满足的选项"],
                "verification": ["回代题干验证"],
                "risk": ["代入时计算错误"],
                "analysis_only_when": ["多个选项同时满足", "无选项满足"],
            },
            "特值法": {
                "scenarios": ["工程问题设总量", "比例问题设份数", "利润问题设成本"],
                "steps": ["选取方便计算的特殊值", "代入模型求解", "验证结果"],
                "verification": ["检查特殊值是否合理"],
                "risk": ["特殊值选取不当导致计算复杂"],
                "analysis_only_when": ["无法确定合适的特殊值"],
            },
            "方程法": {
                "scenarios": ["已知量和未知量关系明确", "可列等式"],
                "steps": ["设未知数", "列方程", "解方程", "验证"],
                "verification": ["回代题干验证"],
                "risk": ["方程列错", "多解"],
                "analysis_only_when": ["方程无唯一解", "方程组无解"],
            },
            "赋值法": {
                "scenarios": ["工程问题设总量", "比例问题设份数"],
                "steps": ["选取方便计算的赋值", "计算各量", "求解目标"],
                "verification": ["检查赋值是否合理"],
                "risk": ["赋值不当导致计算复杂"],
                "analysis_only_when": ["无法确定合适的赋值"],
            },
            "枚举法": {
                "scenarios": ["候选值有限", "不定方程整数解"],
                "steps": ["列出所有候选值", "逐个验证条件", "筛选满足条件的解"],
                "verification": ["检查是否遗漏候选值"],
                "risk": ["候选值过多导致枚举不完整"],
                "analysis_only_when": ["候选值过多无法完整枚举"],
            },
            "十字交叉法": {
                "scenarios": ["浓度混合", "平均数混合", "比例混合"],
                "steps": ["画十字交叉", "计算比例", "求解"],
                "verification": ["检查比例计算"],
                "risk": ["混合类型判断错误"],
                "analysis_only_when": ["混合类型不明确"],
            },
            "比例法": {
                "scenarios": ["行程问题速度比例", "工程问题效率比例"],
                "steps": ["找出比例关系", "利用比例求解", "验证"],
                "verification": ["检查比例关系是否正确"],
                "risk": ["比例关系识别错误"],
                "analysis_only_when": ["比例关系不明确"],
            },
            "图表辅助": {
                "scenarios": ["容斥问题画韦恩图", "行程问题画线段图"],
                "steps": ["画图辅助理解", "标注已知量", "推导未知量"],
                "verification": ["检查图与题干是否一致"],
                "risk": ["图画错导致推导错误"],
                "analysis_only_when": ["无法可靠画图"],
            },
            "公式法": {
                "scenarios": ["有明确公式可用", "鸡兔同笼/植树/余数等"],
                "steps": ["识别可用公式", "代入已知量", "求解未知量"],
                "verification": ["回代题干验证"],
                "risk": ["公式误套"],
                "analysis_only_when": ["公式适用条件不明确"],
            },
            "构造极端": {
                "scenarios": ["最值问题", "最不利构造", "几何最值"],
                "steps": ["分析极端情况", "构造极端方案", "验证最优性"],
                "verification": ["检查是否确实是最优"],
                "risk": ["构造方式不唯一"],
                "analysis_only_when": ["构造方式不唯一", "无法确定最优"],
            },
            "估算量级": {
                "scenarios": ["选项差距大", "计算复杂"],
                "steps": ["估算结果量级", "排除明显不合理的选项", "精确计算验证"],
                "verification": ["检查估算是否合理"],
                "risk": ["估算不精确导致误排"],
                "analysis_only_when": ["选项差距小无法估算", "估算结果不确定"],
            },
            "分类讨论": {
                "scenarios": ["排列组合", "多种情况"],
                "steps": ["确定分类标准", "逐类计算", "汇总结果"],
                "verification": ["检查是否遗漏分类", "检查各类是否互斥"],
                "risk": ["分类标准不当导致遗漏或重复"],
                "analysis_only_when": ["分类标准不明确", "类别过多无法完整讨论"],
            },
        },
        "option_verification": {
            "steps": [
                "逐项代入 A/B/C/D",
                "检查是否满足题干全部条件",
                "检查单位是否一致",
                "检查问法是否对应最终量",
                "检查是否有多个选项同时满足",
                "检查计算结果是否在选项范围内",
                "检查估算量级是否合理",
                "多个选项都可解释则 analysis_only",
                "无选项满足且模型不确定则 analysis_only",
            ],
        },
        "response_template": (
            "【题型识别】\n"
            "判断本题属于哪种数量关系题型（工程、行程、利润、浓度、容斥、排列组合、概率、几何、鸡兔同笼、日期、余数、牛吃草等）。\n\n"
            "【问法目标】\n"
            "明确题目要求求什么（时间、数量、概率、方案等）。\n\n"
            "【已知量】\n"
            "从题干中抽取所有已知数值和条件。\n\n"
            "【未知量】\n"
            "设定需要求解的未知量。\n\n"
            "【单位统一】\n"
            "检查所有量的单位是否一致，必要时进行换算。\n\n"
            "【方法选择】\n"
            "根据题型选择合适的方法（代入排除、特值法、方程法、赋值法、枚举法、比例法等）。\n\n"
            "【模型建立】\n"
            "根据题型和方法建立数学模型，列出方程或关系式。\n\n"
            "【计算/代入验证】\n"
            "求解模型，将结果代入题干验证是否满足全部条件。\n\n"
            "【量级检查】\n"
            "检查计算结果的量级是否合理，排除明显不合理的选项。\n\n"
            "【唯一性判断】\n"
            "确认只有一个选项满足所有条件。若不唯一，标注 analysis_only。\n\n"
            "【不确定性说明】\n"
            "列出任何导致不确定的因素，标注 analysis_only。"
        ),
        "uncertainty_policy": {
            "triggers": [
                "题型无法稳定识别 → analysis_only",
                "问法目标不明确 → analysis_only",
                "已知量或单位无法完整抽取 → analysis_only",
                "存在多个建模方式且结果不同 → analysis_only",
                "多个选项均满足条件 → analysis_only",
                "计算结果不在选项中且模型不确定 → analysis_only",
                "题干存在歧义或缺少必要条件 → analysis_only",
                "涉及复杂排列组合/概率/几何构造且无法可靠建模 → analysis_only",
            ],
        },
        "must_not_do": [
            "不得看见数字就硬套公式。",
            "不得忽略单位。",
            "不得忽略问法。",
            "不得忽略选项范围。",
            "不得默认选择第一个选项。",
            "不得只算一个式子不回代题干。",
            "不得在多个模型都能解释时强行选。",
            "不得把 scaffold 当 solver。",
            "不得用题号、case_id 或标准答案写规则。",
            "不得生成或引用自造真题。",
        ],
    }


def get_quantity_relation_stage_order() -> list[str]:
    """Return the ordered thinking stages."""
    return build_quantity_relation_scaffold()["stage_order"]


def get_quantity_relation_problem_type_checklists() -> dict[str, Any]:
    """Return problem type checklists."""
    scaffold = build_quantity_relation_scaffold()
    return {
        "router": scaffold["problem_type_router"],
        "checklists": scaffold["problem_type_checklists"],
    }


def get_quantity_relation_method_checklists() -> dict[str, Any]:
    """Return method checklists."""
    return build_quantity_relation_scaffold()["method_checklists"]


def render_quantity_relation_prompt_template() -> str:
    """Return the prompt template for quantity relation reasoning."""
    return build_quantity_relation_scaffold()["response_template"]
