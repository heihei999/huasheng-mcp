# Logic Reasoning v2 Calibration Evaluation Plan

## 1. Current v1 MVP Status

`solve_logic_reasoning` v1 MVP has completed:

- CLI command: `xingce-solver solve-logic`
- MCP tool: `solve_logic_reasoning`
- basic structured output for argument-based logic judgment
- preliminary recognition for weakening, strengthening, premise assumption, explanation, and basic conclusion-inference questions
- rough conclusion, premise, argument gap, and option-analysis drafts
- conservative `answer_candidate: null` behavior

## 2. v2 Calibration Goal

v2 calibration does not aim to become a complete automatic solver. Its goal is to establish:

- real-question recording template
- evaluation plan
- failure taxonomy
- regression-test framework
- conservative-output policy for later answer-candidate work

## 3. Why v2 Does Not Expand To Translation / Truth / Analysis Reasoning Yet

Translation reasoning, truth-value reasoning, and analysis reasoning require more exact symbolic representations, stricter option validation, and many edge-case tests. Adding them before real-question calibration would blur failure causes.

v2 therefore keeps the scope on argument-based logic judgment and basic conclusion-inference recognition. Out-of-scope failures should be recorded, not immediately patched.

## 4. Real-Question Calibration Target

Use real or real-style logic judgment questions to evaluate:

- question-type routing
- conclusion extraction
- premise extraction
- argument-gap diagnosis
- option parsing
- option relation and strength draft
- method-card recall
- whether the solver stays conservative when the answer is uncertain

## 5. Coverage Scope

Recommended first calibration batch:

- weakening: 6 cases
- strengthening: 6 cases
- premise assumption: 5 cases
- explanation: 5 cases
- conclusion inference / cannot infer: 5 cases

Do not use external APIs, OCR, image recognition, or PDF parsing for this batch.

## 6. Success Criteria

For v2 calibration, a case is acceptable when:

- the broad question type is correct
- at least one relevant `method_id` is recalled
- A/B/C/D options are parsed when present
- the output explains the argument structure or clearly warns when it cannot
- `answer_candidate` remains `null` unless later v3 criteria are satisfied
- no old CLI, MCP, data-analysis tests, or smoke tests regress

## 7. Failure Taxonomy

- 题型识别错误
- 论点抽取错误
- 论据抽取错误
- 论证缺口判断错误
- 选项解析错误
- 选项力度排序错误
- method_id 召回不准
- 不该出答案却出答案
- 该出答案却没出答案
- 解释文本不符合考场思路
- 当前阶段范围外：翻译推理
- 当前阶段范围外：真假推理
- 当前阶段范围外：分析推理

## 8. Failures That Can Enter Regression Tests

Add a failure to regression tests when:

- it is a repeated general pattern, not a one-off wording issue
- it can be represented without copying a long external passage
- it does not require PDF/OCR/image input
- expected behavior is structural, such as type, method id, warnings, or conservative `answer_candidate`
- it does not force hardcoded final answers

## 9. Failures Not Fixed In v2

Do not fix these in v2:

- symbolic translation reasoning requiring exact formal proof
- truth-value and contradiction tables
- analysis reasoning with multi-person/multi-position constraints
- definition judgment, analogy reasoning, graphic reasoning
- failures caused only by poor transcription
- failures that require a specific real-question answer to be hardcoded

## 10. Draft Admission Criteria For v3 `answer_candidate`

v3 may consider outputting `answer_candidate` only when all conditions hold:

1. 题型识别明确。
2. 选项 A/B/C/D 完整解析。
3. 最高分唯一。
4. 最高分 >= 4。
5. 最高分与第二名差距 >= 2。
6. 没有 `high_risk_warning`。
7. 论点 / 论据 / 论证缺口至少有一个被稳定抽取。
8. `recommended_methods` 至少召回 1 个相关方法卡。

Otherwise, keep:

```json
{
  "answer_candidate": null
}
```

This is a documentation-only standard for v2. It is not implemented in v2 calibration.
