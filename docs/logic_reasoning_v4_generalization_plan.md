# solve_logic_reasoning v4 泛化修复记录

## 背景

`solve_logic_reasoning v3 cautious answer selection` 在第一批 9 道有效真实题上表现稳定，但第二批 20 道真实题暴露出过度保守问题：

- v3 第二批 correct: 2
- v3 第二批 wrong: 0
- v3 第二批 null: 18
- `decision_status=analysis_only`: 18
- `decision_status=candidate_ready`: 2

v3 的问题不是乱猜，而是候选准入过严、真实题干表达泛化不足、选非方向处理仍偏保守。

## v3 失败分析

第二批 20 题中，`answer_candidate=null` 的题目为：01、02、04、05、06、07、08、09、10、12、13、14、15、16、17、18、19、20。

同一批题中，`decision_status=analysis_only` 的题目也是上述 18 题。

按题型看：

- 削弱题：常见失败来自他因、因果倒置、方案无效、可绕过、样本/统计不可靠、比较口径不同等表达未充分覆盖。
- 加强题：常见失败来自搭桥、机制证据、排除他因、正向证据表达泛化不足。
- 前提假设题：常见失败来自必要桥梁、指标预测目标、时间桥梁等关键词不足。
- 解释说明题：常见失败来自需要同时解释矛盾两面或识别对象/时间/口径差异。
- 选非题：v3 能发现部分反向问法，但候选选择仍过于保守。

主要原因：

- 选项评分特征过稀疏。
- 候选阈值与分差要求偏高。
- 反向/选非题最低分选择机制不够稳定。
- 部分 high risk warning 只是提示风险，却过度阻断 candidate。

## v4 修复范围

v4 只做论证类小范围泛化修复，不实现新大题型：

- 更新输出版本为 `version: v4`。
- 保留 `decision_status`、`confidence`、`high_risk_warnings`。
- 增加可选 `return_debug=True`，输出 candidate selection trace。
- 扩展削弱、加强、前提、解释、结论推出和选非问法触发词。
- 扩展选项评分特征。
- 对反向/选非题使用更稳定的最低支持项选择。
- 谨慎放宽候选准入，控制错误候选数量。

## v4 第二批结果

运行结果见：

- `outputs/logic_reasoning_lr2_v4_results.jsonl`
- `outputs/logic_reasoning_lr2_v4_summary.md`

统计：

- total: 20
- correct: 14
- wrong: 0
- null: 6
- decision_status:
  - `candidate_ready`: 14
  - `analysis_only`: 6

与 v3 对比：

| version | correct | wrong | null |
|---|---:|---:|---:|
| v3 | 2 | 0 | 18 |
| v4 | 14 | 0 | 6 |

## 当前边界

v4 仍不支持：

- 翻译推理
- 真假推理
- 分析推理
- 图形推理
- 定义判断
- 类比推理

v4 输出仍是结构化解题辅助，不承诺所有真实题自动给出最终答案。低置信度题仍会保持 `analysis_only`。

## 后续建议

建议继续做论证类 v5，而不是立刻进入翻译推理 v1。v5 可以重点处理：

- 反向问法语义嵌套。
- 多选项同分时的力度排序。
- 更细的论证对象、时间、口径匹配。
- 可解释的 option score trace。
