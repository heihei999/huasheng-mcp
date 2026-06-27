# Logic Reasoning v6.1 Translation Real-Case Audit

本阶段目标是在 `solve_logic_reasoning v6 translation reasoning v1` 基础上，用 16 道开放获取、已核验答案的真实翻译推理题复测，并做小范围通用兼容增强。

当前状态：`v6.1 real-case audited / tested`。不宣布 stable。

## Scope

本阶段只处理翻译推理：

- 条件链：如果/只要/若。
- 必要条件：只有/才。
- 除非/否则。
- 且命题否定、或命题、至少一支成立。
- 链式逆否。
- 反对命题的摩根等价表达。

不处理：

- 真假推理
- 分析推理
- 图形推理
- 定义判断
- 类比推理
- 论证类继续精修

## Method Cards

v6/v6.1 继续引用以下翻译推理相关 method_id：

- `lj_conclusion_translation_001`
- `lj_sufficient_necessary_001`
- `lj_translation_if_001`
- `lj_translation_only_001`
- `lj_translation_unless_001`
- `lj_inverse_contrapositive_001`
- `lj_or_and_negation_001`
- `lj_relation_quantifier_001`

## Synthetic Translation Set

目录：

```text
text-image/logic_translation_v1_cases/
```

结果：

- total: 12
- correct: 12
- wrong: 0
- null: 0

## Real Translation Audit Set

目录：

```text
text-image/logic_translation_real_cases_open_verified_v2/
```

文件：

- `questions_manifest.json`
- `ANSWER_KEY.md`
- `SOURCES.md`
- `AUDIT_NOTES.md`

结果：

- total: 16
- correct: 16
- wrong: 0
- null: 0
- `candidate_ready`: 16
- `结论推出 / 翻译推理`: 16

输出：

- `outputs/logic_reasoning_translation_real_v2_results.jsonl`
- `outputs/logic_reasoning_translation_real_v2_summary.md`

## Argument Regression

v6.1 复跑第二批 20 道论证类真实题：

- correct: 18
- wrong: 0
- null: 2
- `candidate_ready`: 18
- `analysis_only`: 2

输出：

- `outputs/logic_reasoning_lr2_v6_1_regression_results.jsonl`
- `outputs/logic_reasoning_lr2_v6_1_regression_summary.md`

第一批真实题回归测试仍通过，没有回退。

## Implementation Notes

- `version`: `v6.1`
- `solver_version`: `v6.1 translation real-case audit`
- 未修改 CLI/MCP 入参格式。
- 未新增 CLI 命令或 MCP tool。
- 未修改资料分析 solver。
- 未修改知识库。

v6.1 小范围增强：

- 翻译路由只看题干材料的翻译信号，避免选项里的“如果/只要”抢路由。
- 增加链式条件、且命题否定、必要条件、除非/否则、反对命题的真实题句式兼容。
- 保留 v5/v6 论证类回归门槛。

## Remaining Risks

- 当前仍是轻量规则型解题辅助，不是完整命题逻辑证明器。
- 更复杂的真假推理、分析推理、排列组合式逻辑仍需后续单独阶段。
- 后续新增真实题应先记录失败类型，再决定是否做通用增强。
