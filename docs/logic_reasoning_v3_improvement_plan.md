# solve_logic_reasoning v3 改进计划

## v3 实施状态

本计划已进入实现：`solve_logic_reasoning v3 cautious answer selection` 已加入代码，并新增真实题回归测试 `tests/test_logic_reasoning_v3_real_cases.py`。

当前 v3 回归结果：

- 有效真实题样本：9
- answer_candidate 正确：9
- answer_candidate 错误：0
- answer_candidate 为 null：0
- LR-004：已识别“除哪项外”为选非方向，候选为 D
- LR-008：已识别“除哪项外”为选非方向，候选为 B
- LR-005、LR-006：仍识别为前提假设题
- LR-009、LR-010：仍识别为结论推出题

本轮实现只覆盖论证类逻辑判断的谨慎候选选择，不扩展到翻译推理、真假推理、分析推理或其他判断推理模块。

## v2 Calibration 当前结论

`solve_logic_reasoning v2 calibration` 已能完成论证类逻辑判断题的基础结构化：题型初判、论点/论据/缺口草案、选项分析框架和 method_id 召回。第一批 LR-001 ~ LR-010 中，LR-007 因图片错放/疑似重复被排除，实际有效校准样本为 9 道。

v2 的核心问题不是工具不可用，而是仍偏向“结构化分析器”：能给方法和草案，但普遍不输出 `answer_candidate`，且标准答案选项突出度不足。

## 第一批 9 道有效样本评估摘要

- 有效样本数：9
- 削弱/质疑：2
- 加强/支持：2
- 前提假设：2
- 解释说明：1
- 结论推出：2
- answer_candidate 正确：0
- answer_candidate 错误：0
- answer_candidate 为 null：9

主要失败类型：

- 标准答案选项未突出：9
- 选项力度排序错误：7
- method_id 召回不准：2
- 论点抽取错误：2
- 论证缺口判断过泛：2
- 选非方向识别不足：2
- 题型识别错误：2

## v3 目标

从“结构化分析器”升级为“谨慎出答案的论证类逻辑判断 solver”。v3 应在高置信场景下给出答案候选，在低置信或高风险场景下明确保持草案状态。

## v3 不做什么

- 不做翻译推理。
- 不做真假推理。
- 不做分析推理。
- 不做图形推理。
- 不做定义判断。
- 不做类比推理。
- 不扩展到资料分析，资料分析 v5 保持冻结。

## v3 必做

- 已完成：增加 `decision_status`，区分 `candidate_ready`、`analysis_only`、`needs_manual_review`。
- 已完成：增加 `confidence`。
- 已完成：增加 `high_risk_warnings`，标记选非题、选项不完整、结构不稳定等风险。
- 已完成：建立 `answer_candidate` 准入门槛。
- 已完成：强化选非题识别，覆盖“除哪项外”“不能支持”“不能削弱”“无法解释”等。
- 已完成：增强标准答案选项突出机制，识别直接攻击、直接支持、必要桥梁、保守推出、无关项。
- 已完成：增加失败案例回归测试，覆盖 LR-001 ~ LR-006、LR-008 ~ LR-010。

## v3 Answer Candidate 准入建议

只有同时满足以下条件时才输出 `answer_candidate`：

- 题型识别明确。
- A/B/C/D 选项完整解析。
- 非选非题：最高分唯一，且与第二名分差足够。
- 选非题：最低支持项、无法解释项或不能支持项唯一，且分差足够。
- 没有 `high_risk_warning`。
- 方法卡召回至少 1 张相关卡。

如果不满足准入条件，应保持 `answer_candidate: null`，并通过 `decision_status` 说明原因。

## v3 测试准入

- 已满足：9 道有效真实题中，v3 在高置信样本上输出候选答案。
- 已保留：低置信样本通过 `decision_status` 和 `confidence` 保持谨慎准入。
- 已满足：选非题能识别方向，覆盖 LR-004 和 LR-008。
- 已满足：结论推出题优先保守推出，覆盖 LR-009 和 LR-010。
- `python -m pytest` 必须通过。
- `powershell -ExecutionPolicy Bypass -File scripts/smoke_test.ps1` 必须通过。
