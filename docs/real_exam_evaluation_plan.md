# Real Exam-Style Evaluation Plan

This plan describes how to evaluate `xingce-solver` against real exam-style data-analysis cases.

## Step 1: Run Text Rewrite Tests

Run:

```powershell
python -m pytest tests/test_data_analysis_real_exam_style.py
```

These tests use:

```text
tests/fixtures/data_analysis_real_exam_style_cases.jsonl
```

They verify:

- module is `资料分析`
- at least one expected method id is recommended
- non-gap cases can produce an answer candidate or approximate computed result
- known-gap cases remain documented without failing the current solver

## Step 2: Upload Real Question Images To A Multimodal Client

Use the B-class manual entry points in `docs/real_exam_data_analysis_cases.md`.

The multimodal client should first transcribe the image according to:

```text
docs/multimodal_question_reading_prompt.md
```

The MCP server should receive structured text, not images.

## Step 3: Observe Image Transcription Quality

Record whether the client correctly extracts:

- material text
- table headers
- chart titles
- units
- years and months
- subjects
- numbers
- rates
- percentage points
- A/B/C/D options
- uncertain or blurry values

## Step 4: Observe MCP Tool Call Order

Expected tool flow:

```text
classify_question
solve_data_analysis
get_method_card or get_source_reference as needed
```

For non-data-analysis questions, current-stage clients should only use `search_methods` and `get_method_card` for assisted explanation.

## Step 5: Record Method And Answer Quality

For each case, record:

- whether the selected `method_id` is appropriate
- whether `question_type` is appropriate
- whether `computed_result` is filled only when safe
- whether `answer_candidate` is correct when options are parseable
- whether `needs_more_data` and `warnings` are useful when information is missing

## Step 6: Categorize Errors

Classify each failure into one of these buckets:

- image transcription error
- routing error
- method-card retrieval error
- solver capability gap
- output format problem

## Step 7: Feed Gaps Into Future Stages

Previously known gaps addressed by v3:

- interval / inverse growth-rate reasoning
- multi-object growth amount sorting
- base-period share after separate base-period recovery
- base-period values and difference, such as trade surplus

Additional gaps addressed by v4 small enhancement:

- DA-07 style two current-share ratios and percentage-point difference
- DA-10 style cumulative-period split followed by a ratio

Additional gaps addressed by v5 small enhancement:

- DA-06 style reverse growth-rate ranking from current amounts and growth amounts
- DA-08 style named group sums followed by a ratio
- DA-09 style cumulative minus new, residual small category, then base-period share

Remaining or likely future gaps include:

- chart trend matching from images
- noisy multimodal transcription of tables and charts
- more complex multi-step average, share-difference, and mixed-unit calculations

These should be addressed in later solver stages without changing the knowledge base files.

## Final v5 Evaluation Conclusion

第一批 10 道真实题图已全部通过，当前记录为 `10/10 passed`。

已解决的真实题图缺口包括：

- 两个现期比重差
- 时间分段后求倍数
- 多对象反推增速排序
- 分组求和后求倍数
- 累计减新增 + 残差小类 + 基期占比

后续新增测试题时，应继续使用失败分类：

- 图片转写错误
- `current_question_payload` 筛选错误
- 路由错误
- `method_id` 推荐错误
- solver 能力缺口
- `answer_candidate` 匹配错误
- 客户端绕过 MCP
