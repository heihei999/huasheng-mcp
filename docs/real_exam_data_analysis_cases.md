# Real Exam-Style Data Analysis Cases

This document records real exam-style data-analysis cases for evaluating `solve_data_analysis v2`.

These are not full re-publications of official exam materials. The A-class cases are short rewritten prompts based on publicly checkable national civil-service data-analysis question types. They preserve the question type, numerical relationship, and expected method direction, but avoid copying long original passages.

## A-Class: Text Rewrites For Automated Tests

The automated fixture is:

```text
tests/fixtures/data_analysis_real_exam_style_cases.jsonl
```

Each case includes:

- `case_id`
- `source_note`
- `question_text`
- expected module and question type
- acceptable method ids
- expected answer or approximate result when current v2 can reasonably handle it
- `expected_gap`
- `gap_reason`

Current cases:

| case_id | focus | expected_gap |
| --- | --- | --- |
| `case_2023_exec_126_interval_growth_clothing` | interval / inverse growth rate | false |
| `case_2023_exec_127_current_share` | current share | false |
| `case_2023_exec_128_growth_amount_compare` | growth amount comparison | false |
| `case_2023_exec_129_base_share_mask` | base-period share after separate base values | false |
| `case_2023_exec_130_base_trade_surplus` | base-period values and difference | false |

`expected_gap=true` means the case is a known enhancement target. The test checks module and method direction, but does not force the current solver to produce the official answer.

Current v2 focuses on recognizing the question type and selecting method cards. It does not aim to cover every complex calculation pattern.

Stage 7 / v3 added narrow general rules for the four earlier known gaps above, so the automated text-rewrite cases currently all run as `expected_gap=false`. Future real-image tests may still expose transcription or solver gaps.

Stage 8 / v4 small enhancement records two real-image gaps that are now covered by general text-input tests:

| case_id | focus | v4 status |
| --- | --- | --- |
| `DA-07_2024_exec_Q112_share_change` | two current shares and percentage-point difference | v4 computes about `31.6` percentage points and matches `A` |
| `DA-10_2024_exec_Q126_time_segment_ratio` | cumulative period split, then ratio | v4 computes `12.5` and matches `A` |

Before v4, both cases had correct method direction but incomplete automatic calculation. DA-07 routed to share-change methods without computing the two current shares. DA-10 routed to time-segment logic but did not complete the cumulative-period split and ratio calculation.

Stage 9 / v5 small enhancement records three additional real-image gaps that are now covered by general text-input tests:

| case_id | focus | v5 status |
| --- | --- | --- |
| `DA-06_2024_exec_Q111_growth_rate_ranking` | current amount plus growth amount, then reverse growth-rate ranking | v5 ranks `举报 > 投诉 > 咨询` and matches `D` |
| `DA-08_2024_exec_Q116_ratio_average` | group sums followed by ratio | v5 computes about `4.6` and matches `A` |
| `DA-09_2024_exec_Q121_share_base` | cumulative minus new, residual small category, then share | v5 computes about `39.6%` and matches `D` |

Before v5, DA-06 was misread as a simple two-period growth-rate calculation, DA-08 was not stably routed to data analysis, and DA-09 identified the broad method direction but did not complete the cumulative-new residual share calculation.

## B-Class: Multimodal Manual Image/PDF Entry Points

These are intended for later manual tests with uploaded real question images or PDF pages. They are not automated in this stage.

### 2023 Exec 111-115: Integrated Circuit

```text
case_group: 2023_exec_111_115_integrated_circuit
input_type: image_or_pdf_page
expected_focus:
  - 表格读取
  - 年份增速判断
  - 现期比重
  - 年均增长率
  - 增量趋势
current_stage: multimodal_manual_test_only
```

Question-type coverage:

- count years exceeding a growth-rate threshold
- current share
- count objects exceeding a growth-rate threshold
- annual average growth-rate ranking
- year-on-year increment trend chart selection

### 2023 Exec 116-120: Traffic Compliance

```text
case_group: 2023_exec_116_120_traffic_compliance
input_type: image_or_pdf_page
expected_focus:
  - 表格读取
  - 百分点变化
  - 平均值变化
  - 多指标大小关系
current_stage: multimodal_manual_test_only
```

Question-type coverage:

- number of cities with indicators higher than the previous quarter
- percentage-point change interval
- arithmetic average change
- multi-indicator comparison
- bar-chart matching

### 2023 Exec 121-125: Wood Import

```text
case_group: 2023_exec_121_125_wood_import
input_type: image_or_pdf_page
expected_focus:
  - 累计求和
  - 平均数/单价
  - 现期比重
  - 比重差
  - 增量趋势
current_stage: multimodal_manual_test_only
```

Question-type coverage:

- multi-year cumulative sum
- average unit-price comparison
- current share interval
- share difference / percentage points
- year-on-year increment trend chart
