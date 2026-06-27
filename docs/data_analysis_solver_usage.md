# Data Analysis Solver Draft

`solve_data_analysis` is a minimum viable data-analysis solving assistant. It does not produce a guaranteed final answer. It builds a structured solving draft from the existing knowledge base and route rules.

## Scope

Supported in this stage:

- preliminary route classification
- data-analysis subtype detection
- simple extraction of time, numbers, rates, units, metrics, subjects, and options
- recommended method cards
- structured solving plan
- calculation policy and forbidden mistakes
- warnings when information is missing

Not supported in this stage:

- full automatic answer solving
- OCR or image recognition
- PDF parsing
- remote API calls
- non-data-analysis solvers
- long, brute-force division over large numbers

## Python API

```python
from xingce_solver.solvers import solve_data_analysis

result = solve_data_analysis(
    "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？"
)
```

## CLI

Read from a file:

```powershell
xingce-solver solve-data --question question.txt
```

Pass text directly:

```powershell
xingce-solver solve-data --text "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？"
```

The CLI prints 题型判断、调用方法、关键要素、解题步骤草案、考场速算策略、警告/缺失信息 and 来源 method_id.

## MCP Tool

Tool name:

```text
solve_data_analysis
```

Input:

```json
{
  "question_text": "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？",
  "options": null
}
```

Output is the same structured dictionary returned by the Python API.

## Current Behavior Examples

For a base-period question:

```text
2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？
```

Expected draft:

- module: `资料分析`
- question_type: `基期量`
- recommended method includes `da_abx_base_direct_001`
- solving plan includes `A = B/(1+R)`
- formula plan includes `A = B/(1+R)`
- simple computed result can be `120`
- with options `A.100亿元 B.110亿元 C.120亿元 D.132亿元`, answer candidate should be `C`

For incomplete data:

```text
某产业占比提高了0.3个百分点，问该产业比重变化是多少？
```

The solver must not invent missing part/whole values or growth rates. It may still identify a share-change draft, but warnings must explain what needs to be checked.

## V2 Fields

The v2 result adds:

```text
option_gap_analysis
formula_plan
estimation_plan
computed_result
answer_candidate
```

`computed_result` is filled only for simple, safe estimates such as `132 / 1.1 = 120`, `(120-100)/100 = 20%`, or `200/1000 = 20%`. If the data is incomplete, it remains `null` and `warnings` explains the missing data.

## V3 Real Exam-Style Enhancements

The v3 draft solver adds small, general rules for several real exam-style patterns:

- inverse interval growth rate: `R2 = (1 + R间)/(1 + R1) - 1`
- multi-object growth amount ranking: `X = B × R / (1 + R)`, with negative growth treated as negative increment
- two-component base-period share: recover each base-period component before calculating share
- base-period difference under equal growth rates: calculate current difference, then divide by `1 + R`

These remain safe estimate drafts. They are not a full data-analysis answer engine and should still cite method ids and warnings.

## V4 Small Enhancements

The v4 small enhancement adds two general real-image patterns:

- current share difference / percentage-point difference: calculate `part1/whole1 - part2/whole2`, output in percentage points, and match options such as `高20个百分点以上`.
- time-segment ratio: split cumulative data first, such as `1-2月 = 1-3月累计 - 3月单月`, then calculate the ratio between two split-period objects.

Example current-share difference:

```text
热线电话投诉304498件，投诉总件数556063件；热线电话举报61021件，举报总件数263129件。
问热线电话投诉占投诉总件数的比重，比热线电话举报占举报总件数的比重高/低多少？
```

Expected draft:

- recommended methods include `da_share_change_004` and `da_ratio_share_diff_005`
- `computed_result` is about `31.6`
- answer candidate is `A.高20个百分点以上`

Example time-segment ratio:

```text
2023年3月，工业机器人完成产量4.4万套，服务机器人完成产量70万套；
2023年1-3月累计，工业机器人完成产量10.4万套，服务机器人完成产量145万套。
问2023年1-2月，服务机器人完成产量约是工业机器人完成产量的多少倍？
```

Expected draft:

- recommended methods include `da_time_segments_001`
- `computed_result` is about `12.5`
- answer candidate is `A.12.5`

## V5 Small Enhancements

The v5 small enhancement adds three general real-image patterns:

- multi-object current amount plus growth amount, then reverse growth-rate ranking: `增长率 = 增长量 / (现期量 - 增长量)`.
- group-sum ratio: sum each named group first, then calculate `分子组合计 / 分母组合计`.
- cumulative minus new, residual small category, then share: recover the prior-period total and known categories, infer the residual small category, then calculate share.

Expected real-image outcomes:

- `DA-06_2024_exec_Q111_growth_rate_ranking`: answer candidate `D`.
- `DA-08_2024_exec_Q116_ratio_average`: answer candidate `A`.
- `DA-09_2024_exec_Q121_share_base`: answer candidate `D`.

These are generic text-structure rules. They do not depend on case ids or image filenames.
