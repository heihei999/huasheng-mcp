# Multimodal Client Workflow

This document describes how Claude Code, Codex, opencode, or another multimodal AI client should use `xingce-solver` when the user uploads an exam-question image.

## Workflow

1. Start the MCP server:

```powershell
xingce-solver-mcp
```

Alternative:

```powershell
python -m xingce_solver.mcp_server
```

2. Configure the client with the local stdio MCP server.
3. Load or follow `docs/assistant_prompt_for_mcp_usage.md`.
4. If the user uploads an image, first transcribe the image content into structured text.
5. Pass the transcribed question text to MCP tools.
6. Use MCP results to organize the final response.

## Image-To-MCP Flow

```text
user uploads question image
↓
multimodal model reads image content, but does not solve directly
↓
model extracts material, question stem, options, units, years, tables/charts
↓
model calls classify_question
↓
if data analysis, model calls solve_data_analysis
↓
model uses method_id, solving_plan, computed_result, answer_candidate, warnings
↓
model explains the structured draft to the user
```

## Real Image Recommended Workflow V2

For real data-analysis images with shared material:

```text
1. Read the full question image.
2. Identify the current test question number.
3. Extract that question's stem and options.
4. Filter the shared material down to fields relevant to that question.
5. Put unrelated material into ignored_context.
6. Call classify_question.
7. Call solve_data_analysis.
8. If the result scope does not match the question, return to step 4 and filter fields again.
9. Output method_id, calculation draft, answer candidate, and pitfalls.
```

Do not send the full shared material directly to `solve_data_analysis` when the current question only needs a few fields. The preferred solver input is:

```text
material_key_text + question_text + options
```

## Data Analysis v5 Stable Workflow

For data-analysis v5, the stable workflow is:

1. Read the image first.
2. Build `current_question_payload` for the current question.
3. Call MCP tools after the payload is structured.
4. Do not pass the entire shared material directly to `solve_data_analysis`.
5. The final explanation must cite `method_id`.
6. If `answer_candidate` exists, it can be used as the candidate answer, but the client must still check the question stem, unit, time range, and subject scope.
7. If `warnings` says the input contains too many numbers, return to the field-filtering step and rebuild `current_question_payload`.

The `current_question_payload` should keep unrelated material in `ignored_context`, not inside `question_text`. If the MCP result does not match the stem's scope, mark the result as `uncertain` and do not directly trust the answer candidate.

## Suggested Final Answer Format

```text
题型判断：
调用方法：
图片转写关键信息：
考场解题思路：
估算/计算过程：
答案候选：
易错提醒：
依据 method_id：
```

## Current Limits

- This project does not perform OCR.
- This project does not perform image recognition.
- The multimodal model is responsible for reading the image.
- MCP provides method constraints, retrieval, routing, and structured solving assistance.
- If the image is blurry, cropped, or missing key values, the client must ask the user to upload a clearer image or paste the text.
- Current solver support is strongest for data-analysis drafts. It does not include full visual graphic-reasoning recognition.
