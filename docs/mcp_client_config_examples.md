# MCP Client Configuration Examples

## 1. Baseline

- Baseline before v0.2: fed079f
- HEAD after v0.2 hardening: 55938e6
- Previous final closure tag: stable-final-claude-code-mcp-closure-fed079f
- tests: 441 passed with PYTHONPATH=src

## 2. General stdio MCP configuration pattern

The xingce-solver MCP server uses stdio transport. Configuration pattern:

```json
{
  "mcpServers": {
    "xingce-solver": {
      "command": "python",
      "args": ["-m", "xingce_solver.mcp_server"],
      "cwd": "E:\\project\\xingce-solver-migration-final\\xingce-solver",
      "env": {
        "PYTHONPATH": "E:\\project\\xingce-solver-migration-final\\xingce-solver\\src"
      }
    }
  }
}
```

Key points:

- `command`: Python interpreter path
- `args`: Module execution command
- `cwd`: Project root directory (where `src/` is located)
- `env.PYTHONPATH`: Must include `src` directory for src-layout imports

## 3. Claude Desktop style example (Windows)

Add to Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "xingce-solver": {
      "command": "C:\\Users\\<username>\\.venv\\Scripts\\python.exe",
      "args": ["-m", "xingce_solver.mcp_server"],
      "cwd": "E:\\project\\xingce-solver-migration-final\\xingce-solver",
      "env": {
        "PYTHONPATH": "E:\\project\\xingce-solver-migration-final\\xingce-solver\\src"
      }
    }
  }
}
```

Replace `<username>` and Python path as needed.

## 4. Claude Code style example

For Claude Code CLI, use project-level MCP configuration:

```json
{
  "mcpServers": {
    "xingce-solver": {
      "command": "python",
      "args": ["-m", "xingce_solver.mcp_server"],
      "cwd": "E:\\project\\xingce-solver-migration-final\\xingce-solver",
      "env": {
        "PYTHONPATH": "E:\\project\\xingce-solver-migration-final\\xingce-solver\\src"
      }
    }
  }
}
```

## 5. Cursor / generic MCP client example

Generic stdio MCP configuration:

```json
{
  "mcpServers": {
    "xingce-solver": {
      "command": "python",
      "args": ["-m", "xingce_solver.mcp_server"],
      "cwd": "E:\\project\\xingce-solver-migration-final\\xingce-solver",
      "env": {
        "PYTHONPATH": "E:\\project\\xingce-solver-migration-final\\xingce-solver\\src"
      }
    }
  }
}
```

## 6. Recommended user prompt

After MCP is connected, use this prompt:

```text
请先调用 route_xingce_question 判断题型，再调用 compose_xingce_analysis_prompt 生成分析提示词。严格按提示词逐项核验选项；如果无法唯一确定，请输出 analysis_only，不要强行选择。
```

## 7. Tool usage examples

Use minimal synthetic signal strings:

### Graphic reasoning signal

```text
图形推理 规律 选择最合适的一项
```

### Definition judgement signal

```text
以下属于上述定义的是
```

### Analogy reasoning signal

```text
类比推理 关系 最相似
```

### Quantity relation signal

```text
工程问题 甲乙合作几天
```

### Verbal reasoning signal

```text
这段文字的主旨是什么
```

### Unknown signal

```text
abc123 random
```

## 8. Boundary reminder

- `route_xingce_question` does not answer
- `compose_xingce_analysis_prompt` does not answer
- `get_*_scaffold` only returns method scaffold
- No direct answer selection in route/compose tools
- No solver call in route/compose tools

## 9. Actual Claude Code MCP inventory

Verified after Claude Code restart (2026-06-16):

- Total visible MCP tools: 14
- Core practical tools: 8 (route_xingce_question, compose_xingce_analysis_prompt, 6 scaffold tools)
- Additional legacy/base knowledge tools: 4 (classify_question, search_methods, get_method_card, get_source_reference)
- Solver candidate tools: 2 (solve_data_analysis, solve_logic_reasoning)

v0.2 did not add new MCP tools. The 14 tools were the actual Claude Code visible inventory after restart.

## 10. Routing hardening v0.2

True-question routing hardening applied:

- Analogy relation symbol `∶` supported
- Economic/proportion quantity relation signals supported
- Person-month-city arrangement logic analysis signals supported
- Route_uncertain hardening preserved
- Safety fields maintained (no answer/selected_option/prediction)

### v0.2 actual Claude Code MCP regression (2026-06-16)

- Actual visible MCP tools: 14 (not 12)
- solve_data_analysis: visible
- solve_logic_reasoning: visible
- All v0.2 routing scenarios verified in actual client

## 11. Model-in-the-loop routing review v0.3

MCP route is now advisory, not final. Claude must review the question type using full semantics and can override the route if semantic evidence conflicts.

### New route fields

- `possible_modules`: list of candidate modules with reasons
- `model_review_required`: boolean indicating if Claude must review
- `override_allowed`: boolean (always true) allowing Claude to override
- `review_instruction`: advisory text for Claude
- `conflict_signals`: list of detected conflict signals

### Improved edge case routing

- Sentence ordering ("重新排列") → verbal_reasoning
- Sentence insertion ("填入文中哪个位置") → verbal_reasoning
- Main idea ("主要介绍/讲/说明") → verbal_reasoning
- Three-part analogy ("感想∶主观性∶体会") → analogy_reasoning
- Data analysis extended ("占全国/比重/同比增长/上述资料") → data_analysis

### Safety

- No new MCP tools added
- No automatic answer execution
- No answer/selected_option/prediction in route/compose
