# MCP Acceptance Checklist

Use this checklist after installing the project with:

```powershell
python -m pip install -e .
```

## Server Startup

- Start the stdio MCP server:

```powershell
xingce-solver-mcp
```

- Alternative module form:

```powershell
python -m xingce_solver.mcp_server
```

Expected result: the process starts and waits for an MCP client over stdio. It may appear idle in a terminal because stdio MCP servers do not print a web URL.

## Client Discovery

- Configure Claude Code, Codex, or opencode with a local stdio MCP server.
- Use the examples in `docs/client_configs/` as templates.
- Confirm the client discovers these 5 tools:

```text
get_method_card
search_methods
classify_question
get_source_reference
solve_data_analysis
```

## Tool Checks

### get_method_card

Input:

```json
{
  "method_id": "da_share_change_004"
}
```

Expected:

- `method_id` is `da_share_change_004`
- `card.id` is `da_share_change_004`
- `card.method_name` is `比重差公式与秒杀法`
- `card.module` is `资料分析`

### search_methods

Input:

```json
{
  "query": "比重 增长率",
  "module": null,
  "top_k": 5
}
```

Expected:

- `query` is `比重 增长率`
- `results` contains up to 5 method cards
- each result includes `method_id`, `method_name`, `module`, `question_type`, `score`, and `need_review`
- expected top-5 method ids in the current knowledge base:

```text
da_ratio_share_diff_005
da_share_base_002
da_growth_rate_ratio_003
da_share_trend_003
da_growth_rate_product_004
```

### classify_question

Input:

```json
{
  "question_text": "2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？"
}
```

Expected first match:

```json
{
  "module": "资料分析",
  "question_type": "比重变化",
  "sub_type": "比重差/百分点变化",
  "priority_method_id": "da_share_change_004",
  "matched_triggers": ["占比变化"]
}
```

### get_source_reference

Input:

```json
{
  "method_id": "da_share_change_004"
}
```

Expected:

- `method_id` is `da_share_change_004`
- `source_file` includes `【花生十三】资料分析思维导图.pdf` and `花生资料分析笔记.pdf`
- `source_page` includes pages from those sources
- `confidence` is `0.93`
- `need_review` is `false`

### solve_data_analysis

Input:

```json
{
  "question_text": "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？",
  "options": null
}
```

Expected:

- `module` is `资料分析`
- `question_type` is `基期量`
- `source_method_ids` includes `da_abx_base_direct_001`
- `solving_plan` includes `A = B/(1+R)`
- result is a solving draft, not a final answer

## Stage Boundary

This MCP server is for knowledge base retrieval, source lookup, preliminary question routing, and a minimum data-analysis solving draft. It does not include:

```text
solve_graphic_reasoning
solve_logic_reasoning
solve_verbal
solve_quantitative
```

`solve_data_analysis` is intentionally limited to a structured draft generator, not a complete answer engine.
