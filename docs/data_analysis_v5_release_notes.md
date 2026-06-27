# Data Analysis v5 Small Enhancement Notes

`solve_data_analysis` v5 keeps the v3/v4 solver architecture and adds three narrow, general rules found during real-image testing. It does not modify the knowledge base and does not add OCR, image recognition, network calls, or non-data-analysis solvers.

## New Capabilities

1. Multi-object current amount plus growth amount, then reverse growth-rate ranking.
   - Pattern: each object has current amount `B` and growth amount `X`.
   - Formula: `base = B - X`, `growth_rate = X / base`.
   - Example result: complaint/report/consultation growth-rate ranking can match `举报 > 投诉 > 咨询`.

2. Group-sum ratio.
   - Pattern: two named groups each contain several values, and the question asks how many times one group is another.
   - Formula: `ratio = sum(group A) / sum(group B)`.
   - Example result: `中部六省合计 / 东北三省合计 ≈ 4.6`.

3. Cumulative minus new, residual small category, then base-period share.
   - Pattern: current year-end cumulative data and current-year new data are both given; known large and medium categories are listed; the question asks prior year-end small-category share.
   - Formula: `prior_total = cumulative_total - new_total`; `small = prior_total - prior_large - prior_medium`; `share = small / prior_total`.
   - Example result: `(278 - 7 - 161) / 278 ≈ 39.6%`.

## Real-Image Case Status

| case_id | v5 focus | expected v5 result |
| --- | --- | --- |
| `DA-06_2024_exec_Q111_growth_rate_ranking` | reverse growth-rate ranking from current amount and growth amount | answer candidate `D` |
| `DA-08_2024_exec_Q116_ratio_average` | group sums followed by ratio | answer candidate `A` |
| `DA-09_2024_exec_Q121_share_base` | cumulative-new residual small-category share | answer candidate `D` |

## Freeze Status

资料分析 v5 已通过 10 道真实题图测试。

当前标记为 `stable`。

后续只在新真实题暴露通用缺口时再进入 v6。

## Limits

- These rules require clean structured text from the multimodal client.
- They are not tied to image filenames or case ids.
- They remain exam-style estimation helpers, not a full mathematical proof engine.
- Existing v3/v4 capabilities and MCP/CLI behavior are retained.
