# Multimodal Data-Analysis Examples

These examples show how a multimodal AI client should read a question image, convert it to text, and then call MCP tools.

## Example 1: Base-Period Amount

User uploads an image. The multimodal model should transcribe it as:

```text
2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？
A.100亿元 B.110亿元 C.120亿元 D.132亿元
```

Then call:

```text
classify_question
solve_data_analysis
```

Expected:

- question type: `资料分析 / 基期量`
- method_id: `da_abx_base_direct_001`
- formula: `A = B/(1+R)`
- computed_result: `120`
- answer_candidate: `C`

The final explanation should say this is a structured solving draft based on the transcribed image and method card.

## Example 2: Growth Rate

Image transcription:

```text
某地区2020年产值为120亿元，2019年为100亿元，问2020年同比增长率约为多少？
A.10% B.15% C.20% D.25%
```

Expected:

- method_id: `da_growth_rate_general_001`
- formula: `R = (B-A)/A`
- computed_result: `20%`
- answer_candidate: `C`

The client should explain that this is a simple safe estimate, not a large-number brute-force calculation.

## Example 3: Share Change

Image transcription:

```text
2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？
```

Expected:

- method_id: `da_share_change_004`
- no brute-force long division
- emphasize percentage points, share difference, and direction judgment
- if the question directly gives `提高0.3个百分点`, do not force an unnecessary calculation

The client should cite `da_share_change_004` and state that the key issue is recognizing percentage-point change, not treating it as a growth rate.
