# Real Image Test Plan

This plan prepares real data-analysis question-image testing for the frozen `solve_data_analysis` v3.

## General Rules

- Select 10 data-analysis question images.
- The multimodal client reads images and transcribes structured text.
- MCP receives only text and options.
- Record failures before changing solver logic.
- Do not add OCR or image recognition to this project.

## Test Set

| case_id | image_name | source | expected_question_type | expected_answer | expected_method_id | table_transcription_needed | multi_material_needed | possible_risks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| img_da_001_base_amount | `img_da_001_base_amount.png` | public national-exam data-analysis image | 基期量 | TBD | `da_abx_base_direct_001` | yes | no | year and growth-rate transcription; unit consistency |
| img_da_002_growth_rate | `img_da_002_growth_rate.png` | public national-exam data-analysis image | 增长率 | TBD | `da_growth_rate_general_001` | yes | no | confusing current value with base value |
| img_da_003_growth_amount | `img_da_003_growth_amount.png` | public national-exam data-analysis image | 增长量 | TBD | `da_growth_amount_001` | yes | no | growth vs decline sign; option gap |
| img_da_004_current_share | `img_da_004_current_share.png` | public national-exam data-analysis image | 本期比重 | TBD | `da_share_current_001` | yes | no | part/whole identification; unit omission |
| img_da_005_share_change | `img_da_005_share_change.png` | public national-exam data-analysis image | 比重变化 | TBD | `da_share_change_004` | yes | no | percentage-point vs percent confusion |
| img_da_006_base_share | `img_da_006_base_share.png` | public national-exam data-analysis image | 基期比重 | TBD | `da_share_base_002` | yes | yes | separate base-period recovery for multiple components |
| img_da_007_average | `img_da_007_average.png` | public national-exam data-analysis image | 平均数 | TBD | `da_average_general_001` | yes | no | total/count unit mismatch |
| img_da_008_chart_lookup | `img_da_008_chart_lookup.png` | public national-exam data-analysis image | 图表查找 | TBD | `da_chart_lookup_001` | yes | no | wrong row/column lookup; chart label omission |
| img_da_009_growth_amount_compare | `img_da_009_growth_amount_compare.png` | public national-exam data-analysis image | 增长量比较 | TBD | `da_growth_amount_compare_002` | yes | yes | multi-object parsing; negative growth handling |
| img_da_010_comprehensive_judgment | `img_da_010_comprehensive_judgment.png` | public national-exam data-analysis image | 综合判断 | TBD | `da_common_pitfalls_001` | yes | yes | multiple statements; requires several method cards |

## Procedure

1. Save each image with the planned `image_name`.
2. Ask the multimodal client to transcribe using `docs/multimodal_question_reading_prompt.md`.
3. Verify the extracted material, tables, units, years, numbers, rates, and options.
4. Call `classify_question`.
5. If classified as data analysis, call `solve_data_analysis`.
6. Record results with `docs/real_image_test_record_template.md`.
7. Classify failures with `docs/real_image_failure_taxonomy.md`.
