# 第二批逻辑判断真实题验证记录

## 数据来源

- 图片与结构化文本目录：`text-image/lr2_real_verified_20_images/lr2_real_verified_20_images/`
- 结构化题目：`questions_manifest.json`
- 答案表：`ANSWER_KEY.md`
- 来源说明：`SOURCES.txt`
- 本阶段不读取图片、不做 OCR、不联网，只使用已人工核对的 manifest 文本。

## v3 结果

运行命令：

```powershell
python scripts/run_logic_reasoning_real_cases.py --input text-image/lr2_real_verified_20_images/lr2_real_verified_20_images/questions_manifest.json --output outputs/logic_reasoning_lr2_v3_results.jsonl --summary outputs/logic_reasoning_lr2_v3_summary.md
```

统计：

- total: 20
- correct: 2
- wrong: 0
- null: 18
- decision_status:
  - `analysis_only`: 18
  - `candidate_ready`: 2

结论：v3 没有产生错误答案，但对第二批更复杂表达过于保守，18/20 保持 `answer_candidate=null`。

## v4 结果

运行命令：

```powershell
python scripts/run_logic_reasoning_real_cases.py --input text-image/lr2_real_verified_20_images/lr2_real_verified_20_images/questions_manifest.json --output outputs/logic_reasoning_lr2_v4_results.jsonl --summary outputs/logic_reasoning_lr2_v4_summary.md
```

统计：

- total: 20
- correct: 14
- wrong: 0
- null: 6
- decision_status:
  - `candidate_ready`: 14
  - `analysis_only`: 6
- sub_type_actual:
  - `前提假设 / 必要前提`: 3
  - `削弱 / 削弱/质疑`: 8
  - `加强 / 支持加强`: 7
  - `解释说明 / 矛盾解释`: 2

v4 达到阶段目标：在不硬编码答案、不扩展翻译/真假/分析推理的前提下，把第二批真实题从 2/20 提升到 14/20，并保持错误候选为 0。

## 选非识别

v4 已覆盖并识别以下反向/选非表达：

- `除哪项外`
- `不能支持`
- `没有质疑`
- `除了`
- `不能质疑`

涉及题目中，LR2-04、LR2-08、LR2-09、LR2-10、LR2-15 均能在 `question_stem_analysis` 中标记为反向或选非方向。

## 剩余失败类型

v4 仍保留 6 道 `analysis_only`，主要原因：

- 个别削弱题多个选项同分，缺少稳定力度差。
- 个别加强题需要更细的机制/对象匹配，当前规则不贸然出答案。
- 个别解释题存在“除了”语义嵌套，简单选非规则无法稳定判断。
- 个别题接近分析推理或复杂比较，当前阶段不纳入 solver 能力。

## 下一步建议

第二批 v4 已达到小范围修复目标。建议先继续论证类 v5，重点做通用选项力度排序和“反向问法语义嵌套”处理；暂不建议马上进入翻译推理 v1。

## v5 结果

运行命令：

```powershell
python scripts/run_logic_reasoning_real_cases.py --input text-image/lr2_real_verified_20_images/lr2_real_verified_20_images/questions_manifest.json --output outputs/logic_reasoning_lr2_v5_results.jsonl --summary outputs/logic_reasoning_lr2_v5_summary.md
```

统计：

- total: 20
- correct: 18
- wrong: 0
- null: 2
- decision_status:
  - `candidate_ready`: 18
  - `analysis_only`: 2

与 v4 对比：

| version | correct | wrong | null |
|---|---:|---:|---:|
| v4 | 14 | 0 | 6 |
| v5 | 18 | 0 | 2 |

v5 解决了 v4 的 6 个 null 中的 4 个：02、11、12、13。

主要修复：

- 将 `以下除哪项外...` 识别为真正选非问法。
- 避免把题干事实中的“除了等待别无他法”误判为选非。
- 用 `selection_score`、`tie_break_score`、`evidence_tags`、`risk_tags` 做同分排序。
- 对削弱题中的直接反例、替代解释、题干变量命中做更细区分。
- 对加强题中的本题主体机制和类比外部因素做区分。

剩余 `analysis_only`：

- 19：排程安排题，属于分析推理边界。
- 20：鸟类声音景观题，涉及气候变化机制与社群组成的细粒度比较，当前仍保持保守。

v5 当前状态为 refined / tested，不宣称 stable。
