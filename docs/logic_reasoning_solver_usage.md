# Logic Reasoning Solver Usage

`solve_logic_reasoning` 是逻辑判断解题辅助工具。它不是完整自动解题器，目标是基于知识库方法卡片生成结构化解题草案，并在证据足够时谨慎给出 `answer_candidate`。

## Version Status

- v5 argument refinement：第二批 20 道论证类真实题达到 18 正确 / 0 错误 / 2 null。
- v6 translation reasoning v1：新增翻译推理基础能力。
- v6.1 translation real-case audit：用 16 道开放获取真实翻译推理题复测并小范围增强，当前为 real-case audited / tested，不宣布 stable。

## Supported Question Types

当前支持：

- 削弱题
- 加强题
- 前提假设题
- 解释说明题
- 结论推出题基础识别
- 翻译推理 v1/v6.1

翻译推理当前支持：

- 如果/只要/若
- 只有/才
- 除非/否则
- 所有/都、并非所有
- 要么/要么
- 且命题否定、或命题、至少一支成立
- 链式逆否
- 反对命题的摩根等价表达
- 不能推出、无法推出、不一定为真

当前仍不支持：

- 真假推理
- 分析推理
- 图形推理
- 定义判断
- 类比推理

## Python API

```python
from xingce_solver.solvers import solve_logic_reasoning

result = solve_logic_reasoning(
    "只有缴费，才可以报名。小王已经报名。根据上述信息，可以推出的是："
    "A.小王没有缴费 B.缴费的人一定报名 C.小王已经缴费 D.没有报名的人一定没有缴费"
)
```

调试：

```python
result = solve_logic_reasoning(question_text, return_debug=True)
print(result["debug"]["candidate_selection"])
print(result["debug"].get("translation_reasoning"))
```

## CLI

```powershell
xingce-solver solve-logic --text "某研究认为，经常喝茶的人更健康。因此，喝茶可以提高健康水平。以下哪项最能削弱上述论证？A.健康的人更可能有喝茶习惯 B.喝茶的人通常也更爱运动 C.部分人喝茶后睡眠变差 D.茶叶价格逐年上涨"
```

```powershell
xingce-solver solve-logic --question question.txt
```

## MCP Tool

Tool name:

```text
solve_logic_reasoning
```

Input:

```json
{
  "question_text": "只有缴费，才可以报名。小王已经报名。根据上述信息，可以推出的是：A.小王没有缴费 B.缴费的人一定报名 C.小王已经缴费 D.没有报名的人一定没有缴费",
  "options": null
}
```

Output 与 Python API 返回结构一致。

## Output Fields

关键字段：

- `module`
- `version`
- `solver_version`
- `question_type`
- `sub_type`
- `recommended_methods`
- `argument_structure`
- `question_stem_analysis`
- `option_analysis`
- `answer_candidate`
- `decision_status`
- `confidence`
- `high_risk_warnings`
- `solving_plan`
- `source_method_ids`
- `warnings`

`decision_status`：

- `candidate_ready`：已给出谨慎候选答案。
- `analysis_only`：已完成结构化分析，但未达到出答案门槛。
- `needs_manual_review`：题干或选项存在明显阻断，需要人工复核。

## Batch Runner

翻译推理 12 道结构化样例：

```powershell
python scripts/run_logic_reasoning_real_cases.py --input text-image/logic_translation_v1_cases/questions_manifest.json --output outputs/logic_reasoning_translation_v1_results.jsonl --summary outputs/logic_reasoning_translation_v1_summary.md
```

翻译推理 16 道真实题审计：

```powershell
python scripts/run_logic_reasoning_real_cases.py --input text-image/logic_translation_real_cases_open_verified_v2/questions_manifest.json --output outputs/logic_reasoning_translation_real_v2_results.jsonl --summary outputs/logic_reasoning_translation_real_v2_summary.md
```

论证类第二批 20 题回归：

```powershell
python scripts/run_logic_reasoning_real_cases.py --input text-image/lr2_real_verified_20_images/lr2_real_verified_20_images/questions_manifest.json --output outputs/logic_reasoning_lr2_v6_1_regression_results.jsonl --summary outputs/logic_reasoning_lr2_v6_1_regression_summary.md
```

## Current Results

翻译推理真实题 16 道：

- correct: 16
- wrong: 0
- null: 0
- `candidate_ready`: 16

论证类第二批 20 道：

- correct: 18
- wrong: 0
- null: 2

## Current Limits

- v6.1 不是完整逻辑判断自动解题器。
- 不做 OCR、图片识别、联网或外部 LLM/API 调用。
- 不根据 case_id、文件名或标准答案硬编码。
- 仍不支持真假推理、分析推理、图形推理、定义判断、类比推理。
- 资料分析 v5 已冻结，逻辑判断 solver 不修改资料分析逻辑。
