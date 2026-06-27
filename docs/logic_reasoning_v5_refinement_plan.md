# solve_logic_reasoning v5 refinement plan

## v4 基线结果

当前可信基线：

```text
4fef9d8 improve solve_logic_reasoning v4 argument generalization
```

v4 第一批有效真实题 9 道：

- correct: 9
- wrong: 0
- null: 0

v4 第二批 20 道：

- correct: 14
- wrong: 0
- null: 6
- decision_status:
  - `candidate_ready`: 14
  - `analysis_only`: 6

## v4 第二批 6 个 null 归因

v4 的 6 个 `answer_candidate=null` 样本为：02、11、12、13、19、20。

通用归因：

- 02：削弱题中“价格过高阻碍消费欲望”属于替代解释，但 v4 同时高估了健康危害类无关项。
- 11：解释题题干事实含“除了等待别无他法”，v4 误当成选非问法，导致错误阻断。
- 12：加强题 B/C 同分，v4 没有区分“本题主体机制”与“类比外部因素”。
- 13：削弱题 A/B/C 同分，v4 没有区分“未实行也增长”的直接反例与背景/他因。
- 19：排程安排题接近分析推理边界，当前论证类 solver 不处理。
- 20：鸟类声音景观题需要更细的气候变化机制与物种迁移语义，v4 保持保守。

## v5 修改范围

v5 只做论证类逻辑判断 refinement：

- 输出版本更新为 `version: v5`。
- 保留 CLI / MCP 入参兼容。
- 保留 `return_debug=True`。
- 增强反向问法识别，尤其是 `以下除哪项外` 这类语义嵌套。
- 为选项增加：
  - `tie_break_score`
  - `selection_score`
  - `evidence_tags`
  - `risk_tags`
- 候选选择从单纯 `score` 改为基于 `selection_score`。
- 低风险 warning 不直接阻断 candidate。

## v5 不做事项

- 不做翻译推理。
- 不做真假推理。
- 不做分析推理。
- 不做图形推理、定义判断、类比推理。
- 不修改资料分析 solver。
- 不修改知识库。
- 不 OCR、不读取图片、不联网、不调用外部 LLM/API。
- 不按 case_id、题号、文件名或标准答案硬编码。

## 反向问法增强策略

v5 将反向问法限定在任务问句附近识别，避免把题干事实里的“除了”误判为选非。

覆盖表达包括：

- `不能支持`
- `无法支持`
- `不能加强`
- `不能解释`
- `无法解释`
- `不能推出`
- `无法推出`
- `最不能削弱`
- `不能质疑`
- `没有质疑`
- `除哪项外`
- `以下哪项除外`
- `不正确的是`
- `不符合的是`
- `哪项不是`

## 同分排序增强策略

v5 不改变原始 `score` 的含义，而是在其后增加可解释 tie-break：

```text
selection_score = score + tie_break_score - risk_penalty
```

示例标签：

- `direct_counterexample`
- `alternative_cause`
- `matches_conclusion_variable`
- `subject_mechanism_bridge`
- `climate_migration_mechanism`
- `necessary_bridge`
- `explains_counterintuitive_effect`
- `off_topic_health`
- `analogous_external_factor`
- `broad_background`

## answer_candidate 准入调整

v5 沿用谨慎准入，但使用 `selection_score` 判断候选领先程度：

- 选项完整；
- 题型已识别；
- 候选项 `selection_score` 明显领先；
- 没有严重方向冲突；
- 低风险 warning 只降置信度，不直接阻断。

## 风险控制

以下情况仍保持 `analysis_only`：

- 选项不完整；
- 题型未知；
- 严重并列；
- 方向冲突；
- 输入异常；
- 明显属于当前 solver 不支持的分析推理边界题。

## v5 复测结果

第二批 20 道：

- correct: 18
- wrong: 0
- null: 2
- decision_status:
  - `candidate_ready`: 18
  - `analysis_only`: 2

第一批有效真实题 9 道：

- correct: 9
- wrong: 0
- null: 0

v4 的 6 个 null 中，v5 解决了 4 个：02、11、12、13。

## 剩余失败类型

- 19：排程安排题，属于分析推理边界，当前阶段不支持。
- 20：鸟类声音景观题仍存在气候机制与社群组成之间的细粒度语义比较，v5 保持 `analysis_only`。

## 状态

v5 当前状态为 refined / tested，不宣称 stable。
