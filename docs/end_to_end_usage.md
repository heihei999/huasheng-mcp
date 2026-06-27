# End-To-End MCP Usage

This project now provides:

- CLI knowledge-base access
- stdio MCP server
- method-card lookup
- keyword method search
- preliminary question classification
- source PDF/page lookup
- minimum data-analysis solving drafts through `solve_data_analysis`
- pytest and smoke-test coverage

The project still does not parse PDFs, regenerate cards, perform OCR, or provide full automatic answer engines.

For uploaded question images, see:

- `docs/multimodal_question_reading_prompt.md`
- `docs/multimodal_client_workflow.md`
- `docs/multimodal_data_analysis_examples.md`

## Start The MCP Server

From the project root after installing with `python -m pip install -e .`:

```powershell
xingce-solver-mcp
```

Alternative:

```powershell
python -m xingce_solver.mcp_server
```

This is a stdio MCP server. A terminal may look idle because the server waits for an MCP client over stdin/stdout.

If your client starts from a different working directory, set:

```text
XINGCE_KB_DIR=D:\database\xingce-solver\knowledge_base
```

## How Clients Should Call Tools

When the user inputs an exam question, the AI client should follow this flow:

1. Call `classify_question` with the full question text.
2. If the first useful match is `资料分析`, call `solve_data_analysis`.
3. Read `recommended_methods`, `source_method_ids`, `solving_plan`, `warnings`, and `needs_more_data`.
4. Call `get_method_card` for the primary method id when explaining the method.
5. Call `get_source_reference` when source files/pages should be shown.
6. Use `search_methods` when the route is uncertain or when additional supporting method cards are useful.

For images, the client must first transcribe the image into structured text. The MCP server receives text; it does not do OCR or image recognition.

## Recommended AI Prompt

```text
遇到行测题时，请先调用 xingce-solver MCP 的 classify_question。
如果识别为资料分析，请调用 solve_data_analysis，并按返回的 method_id、solving_plan、warnings 组织答案。
不要直接凭模型常识作答。不要进行五六位数暴力长除。不要伪造最终答案。
如果 needs_more_data=true，请说明缺少哪些数据，并只给出结构化解题草案。
如果不是资料分析题，当前阶段只能用 search_methods 和 get_method_card 辅助讲解，不要假装已有完整解题器。
```

## Data-Analysis Output Format

For data-analysis questions, the AI response should include:

- 题型判断
- 调用方法 and method ids
- 关键要素
- 解题步骤草案
- 考场速算策略
- 警告/缺失信息
- 来源 method_id
- a clear note that this is a structured draft, not a guaranteed final answer

## Test Case: Base-Period Amount

Question:

```text
2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？
```

Expected tool behavior:

- `classify_question`: `资料分析 / 基期量`
- `solve_data_analysis`: recommends `da_abx_base_direct_001`
- `solving_plan`: includes `A = B/(1+R)`
- output should not fabricate a final answer
- output should say it is a structured solving draft

## Test Case: Share Change

Question:

```text
2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？
```

Expected tool behavior:

- `classify_question`: `资料分析 / 比重变化`
- `solve_data_analysis`: recommends `da_share_change_004`
- `solving_plan`: mentions first judging direction, percentage points, and share difference
- output should not use brute-force long division

## Current Limits

- No image OCR.
- No full automatic final-answer solver.
- No graphic-reasoning visual recognition.
- No verbal, logic, quantity, or graphic solver tools yet.
- `solve_data_analysis` is a structured draft generator, not a complete calculation engine.
