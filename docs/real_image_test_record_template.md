# Real Image Test Record Template

Use one row per question image.

| field | value |
| --- | --- |
| case_id |  |
| image_name |  |
| source |  |
| expected_question_type |  |
| expected_answer |  |
| expected_method_id |  |
| material_scope | full_material / current_question_only / current_question_with_key_material |
| current_question_payload_quality | good / partial / poor |
| ignored_context_present | true / false |
| irrelevant_numbers_passed_to_solver | true / false |
| solver_input_quality | good / noisy / incomplete |
| full_material_variable_noise | true / false |
| transcribed_question_text |  |
| transcribed_options |  |
| transcription_quality | good / partial / poor |
| tool_calls |  |
| classified_module |  |
| classified_question_type |  |
| recommended_method_ids |  |
| computed_result |  |
| answer_candidate |  |
| final_answer |  |
| is_correct | true / false / unknown |
| problem_type |  |
| problem_detail |  |
| fix_suggestion |  |

## Suggested JSON Form

```json
{
  "case_id": "",
  "image_name": "",
  "source": "",
  "expected_question_type": "",
  "expected_answer": "",
  "expected_method_id": "",
  "material_scope": "",
  "current_question_payload_quality": "",
  "ignored_context_present": false,
  "irrelevant_numbers_passed_to_solver": false,
  "solver_input_quality": "",
  "full_material_variable_noise": false,
  "transcribed_question_text": "",
  "transcribed_options": {},
  "transcription_quality": "",
  "tool_calls": [],
  "classified_module": "",
  "classified_question_type": "",
  "recommended_method_ids": [],
  "computed_result": null,
  "answer_candidate": null,
  "final_answer": "",
  "is_correct": null,
  "problem_type": "",
  "problem_detail": "",
  "fix_suggestion": ""
}
```

## Field Notes

- `material_scope`: use `full_material`, `current_question_only`, or `current_question_with_key_material`.
- `solver_input_quality`: use `good`, `noisy`, or `incomplete`.
- If `irrelevant_numbers_passed_to_solver=true`, first fix the client transcription/filtering workflow instead of immediately changing solver rules.

## V4 Record Notes

- `DA-07_2024_exec_Q112_share_change`: before v4, method direction was correct but automatic calculation was incomplete; v4 should record `computed_result≈31.6`, `answer_candidate=A`, and problem type empty when current-question payload is clean.
- `DA-10_2024_exec_Q126_time_segment_ratio`: before v4, `classify_question` found `da_time_segments_001` but `solve_data_analysis` did not complete the split ratio; v4 should record `computed_result=12.5`, `answer_candidate=A`, and recommended methods containing `da_time_segments_001`.

## V5 Record Notes

- `DA-06_2024_exec_Q111_growth_rate_ranking`: before v5, this was a solver capability gap; v5 should record ranking `举报 > 投诉 > 咨询`, `answer_candidate=D`, and recommended methods containing `da_growth_rate_general_001`.
- `DA-08_2024_exec_Q116_ratio_average`: before v5, this was a group-sum ratio gap; v5 should record `computed_result≈4.6`, `answer_candidate=A`, and estimation notes showing both group totals.
- `DA-09_2024_exec_Q121_share_base`: before v5, this was a cumulative-new residual share gap; v5 should record `computed_result≈39.6`, `answer_candidate=D`, and estimation notes showing `累计 - 新增` plus `小型 = 总数 - 大型 - 中型`.

## Completed 10-Case Summary

| case_id | focus | expected_answer | actual_answer | status |
| --- | --- | --- | --- | --- |
| DA-01 | 逆向间隔增长率 | A | A | passed |
| DA-02 | 本期比重 | C | C | passed |
| DA-03 | 多对象增长量排序 | D | D | passed |
| DA-04 | 基期比重 | C | C | passed |
| DA-05 | 基期差值 | A | A | passed |
| DA-06 | 多对象现期量 + 增长量反推增速排序 | D | D | passed |
| DA-07 | 两个现期比重差 / 百分点差 | A | A | passed |
| DA-08 | 分组求和后求倍数 | A | A | passed |
| DA-09 | 累计减新增 + 残差小类 + 基期占比 | D | D | passed |
| DA-10 | 累计期拆分后求倍数 | A | A | passed |
