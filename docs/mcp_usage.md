# Xingce Solver MCP Server

This MCP server exposes the phase-1 Xingce Solver capabilities as tools:

- read method cards from `knowledge_base/all_cards.jsonl`
- search method cards by keywords
- classify a question stem with `global_router_rules.yaml`
- return source PDF and page references for a method card

It does not parse PDFs, regenerate cards, modify the knowledge base, or solve full exam questions.

## Install

From the project root:

```powershell
python -m pip install -e .
```

This installs the CLI command `xingce-solver` and the MCP server command `xingce-solver-mcp`.

## Start The MCP Server

Use stdio transport:

```powershell
xingce-solver-mcp
```

Equivalent module form:

```powershell
python -m xingce_solver.mcp_server
```

Run these commands from the project root, or set `XINGCE_KB_DIR` to the absolute path of `knowledge_base`.

## Client Configuration

Claude Code, Codex, and opencode can connect to this server as a stdio MCP server. The exact config file path differs by client, but the command shape is:

```json
{
  "mcpServers": {
    "xingce-solver": {
      "command": "xingce-solver-mcp",
      "args": []
    }
  }
}
```

If the console script is not on `PATH`, use Python directly:

```json
{
  "mcpServers": {
    "xingce-solver": {
      "command": "python",
      "args": ["-m", "xingce_solver.mcp_server"]
    }
  }
}
```

If the client launches from another working directory, set the knowledge base path:

```json
{
  "mcpServers": {
    "xingce-solver": {
      "command": "python",
      "args": ["-m", "xingce_solver.mcp_server"],
      "env": {
        "XINGCE_KB_DIR": "D:\\database\\xingce-solver\\knowledge_base"
      }
    }
  }
}
```

## Tools

### get_method_card

Input:

```json
{
  "method_id": "da_share_change_004"
}
```

Output:

```json
{
  "method_id": "da_share_change_004",
  "card": {}
}
```

### search_methods

Input:

```json
{
  "query": "比重 增长率",
  "module": null,
  "top_k": 5
}
```

Output:

```json
{
  "query": "比重 增长率",
  "results": [
    {
      "method_id": "da_share_base_002",
      "method_name": "基期比重公式法",
      "module": "资料分析",
      "question_type": "比重",
      "score": 80.0,
      "need_review": false
    }
  ]
}
```

### classify_question

Input:

```json
{
  "question_text": "2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？"
}
```

Output:

```json
{
  "matches": [
    {
      "module": "资料分析",
      "question_type": "比重变化",
      "sub_type": "比重差/百分点变化",
      "priority_method_id": "da_share_change_004",
      "matched_triggers": ["占比变化"]
    }
  ]
}
```

### get_source_reference

Input:

```json
{
  "method_id": "da_share_change_004"
}
```

Output:

```json
{
  "method_id": "da_share_change_004",
  "source_file": [],
  "source_page": [],
  "confidence": 0.93,
  "need_review": false
}
```

### solve_data_analysis

Input:

```json
{
  "question_text": "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？",
  "options": null
}
```

Output:

```json
{
  "module": "资料分析",
  "question_type": "基期量",
  "sub_type": "已知现期量和增长率求基期",
  "needs_more_data": false,
  "recommended_methods": [],
  "extracted_elements": {
    "options": [],
    "option_values": []
  },
  "option_gap_analysis": {
    "has_options": false,
    "gap_level": "unknown",
    "gap_notes": [],
    "recommended_precision": "unknown"
  },
  "formula_plan": {
    "formula": "A = B/(1+R)",
    "variables": {},
    "missing_variables": []
  },
  "estimation_plan": [],
  "solving_plan": [],
  "exam_style_explanation_draft": "",
  "computed_result": 120,
  "answer_candidate": null,
  "source_method_ids": ["da_abx_base_direct_001"],
  "warnings": []
}
```

This tool creates a structured solving draft only. It does not claim to compute a final answer.

## End-To-End Tool Call Examples

After an AI client connects to the stdio MCP server, it should call tools instead of answering from model memory.

Recommended call sequence:

1. Call `classify_question` with the user's question text.
2. If it is a data-analysis question, call `solve_data_analysis`.
3. Use `source_method_ids` or recommended method ids to call `get_method_card`.
4. Call `get_source_reference` for cited method ids when source attribution is needed.
5. Use `search_methods` when the route is uncertain or when supporting method cards are needed.

### Base-Period Amount Example

Question:

```text
2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？
```

Expected `classify_question` result:

- module: `资料分析`
- question_type: `基期量`

Expected `solve_data_analysis` result:

- recommended/source method includes `da_abx_base_direct_001`
- `solving_plan` includes `A = B/(1+R)`
- `formula_plan.formula` is `A = B/(1+R)`
- `computed_result` may be `120` for the simple estimate `132 / 1.1`
- the response should say this is a structured solving draft
- the response should not pretend it has produced a guaranteed final answer

Useful follow-up tool calls:

```json
{
  "method_id": "da_abx_base_direct_001"
}
```

for both `get_method_card` and `get_source_reference`.

### Share-Change Example

Question:

```text
2019年某地区生产总值同比增长8.5%，其中第一产业占比提高0.3个百分点。问占比变化情况？
```

Expected `classify_question` result:

- module: `资料分析`
- question_type: `比重变化`

Expected `solve_data_analysis` result:

- recommended/source method includes `da_share_change_004`
- `solving_plan` mentions first judging direction, percentage points, and share difference
- the response should not perform brute-force long division
- the response should explain that this is a structured solving draft

Useful supporting search:

```json
{
  "query": "占比变化 百分点",
  "module": "资料分析",
  "top_k": 5
}
```

## Current Stage Boundary

This phase intentionally does not expose these future full solver tools:

- `solve_graphic_reasoning`
- `solve_logic_reasoning`
- `solve_verbal`
- `solve_quantitative`

The MCP server wraps retrieval, source lookup, preliminary route classification, and a minimum data-analysis solving draft.
