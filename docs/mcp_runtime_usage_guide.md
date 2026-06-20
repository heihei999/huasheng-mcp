# MCP Runtime Usage Guide

## 1. Stable baseline

- Baseline before v0.2: fed079f
- HEAD after v0.2 hardening: 55938e6
- Previous final closure tag: stable-final-claude-code-mcp-closure-fed079f
- tests: 441 passed with PYTHONPATH=src

## 2. What this MCP provides

The xingce-solver MCP server exposes tools to the client.

**Actual Claude Code client inventory (verified after restart 2026-06-16):**

- Total visible MCP tools: 14
- Core practical tools: 8
- Additional legacy/base knowledge tools: 4
- Solver candidate tools: 2

### Core practical tools: 8

These are the primary tools developed and verified in the current migration phase:

- `route_xingce_question`
- `compose_xingce_analysis_prompt`
- `get_graphic_reasoning_scaffold`
- `get_definition_judgement_scaffold`
- `get_analogy_reasoning_scaffold`
- `get_logic_analysis_scaffold`
- `get_quantity_relation_scaffold`
- `get_verbal_reasoning_scaffold`

### Additional legacy/base knowledge tools: 4

These tools exist in the server codebase and are visible to the client:

- `classify_question`
- `search_methods`
- `get_method_card`
- `get_source_reference`

### Solver candidate tools: 2

These tools are registered in the server and visible to the client:

- `solve_data_analysis`
- `solve_logic_reasoning`

## 3. Tool positioning

### route_xingce_question

- route-only
- read-only
- guidance-router
- accepts question_text / options / module_hint / image_present / strict_mode
- returns route / module_guess / confidence / recommended_track / recommended_tool / warnings
- does not return answer / selected_option / prediction
- does not call solver

### compose_xingce_analysis_prompt

- prompt-composition-only
- read-only
- guidance-oriented
- accepts question_text / options / module_hint / image_present / strict_mode / include_scaffold_summary
- returns route / prompt_text / prompt_contract / expected_response_schema / warnings
- does not return answer / selected_option / prediction
- does not call solver

### get_*_scaffold (6 tools)

- scaffold-only
- read-only
- returns method scaffold dict
- no question input
- no option input
- no image input
- no answer / selected_option / prediction
- no solver call

## 4. What this MCP does not do

Explicitly:

- does not directly solve all questions
- does not return answer / selected_option / prediction from route or compose tools
- does not call solver inside route/compose tools
- does not process images/OCR
- does not use external LLM/API
- does not fabricate questions

## 5. Recommended workflow

1. User provides question text/options/image context to LLM.
2. LLM calls `route_xingce_question` to determine module and recommended track.
3. LLM calls `compose_xingce_analysis_prompt` to generate structured analysis prompt.
4. LLM follows `prompt_text` and, if needed, calls relevant scaffold tool.
5. LLM analyzes with option verification (A/B/C/D).
6. If not unique, output `analysis_only`.

## 6. Environment setup

The project uses src-layout. PYTHONPATH must be set to `src` directory.

### PowerShell runtime example

```powershell
cd E:\project\xingce-solver-migration-final\xingce-solver
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -c "import xingce_solver; print(xingce_solver.__file__)"
python -c "import xingce_solver.cli; print('cli import ok')"
```

## 7. Test command

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m pytest -q
```

Expected:

```text
441 passed
```

## 8. Safety policy

- wrong=0 first
- do not force answer
- analysis_only if uncertain
- no default first option
- no answer leakage
- no case_id-based rules
- no fabricated real cases

## 9. Troubleshooting

### ModuleNotFoundError: No module named 'xingce_solver'

Cause:

- src-layout path not exposed to subprocess.

Fix for local PowerShell:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
```

### MCP client cannot see tools

Check:

- command path
- working directory
- PYTHONPATH env
- Python interpreter
- server startup logs

## 10. Recommended next stage

Only after runtime usage is verified:

- guarded MCP client smoke
- optional compose prompt polish
- do not jump directly to automatic analyzer

## 11. Routing hardening history

### v0.1 route_uncertain hardening

- "条件不足" routes to route_uncertain
- Empty/blank text routes to route_uncertain
- Too short text (< 4 chars) routes to route_uncertain
- Strong logic_analysis signals preserved

### v0.2 true-question routing hardening

- Analogy relation symbol `∶` supported (e.g., "卫冕∶夺冠", "酒器∶尊∶爵")
- Economic/proportion quantity relation signals supported (收入/支出/盈余/成本 with number context)
- Person-month-city arrangement logic analysis signals supported (张王李杨/月份/城市/调研/不同)
- Route_uncertain hardening preserved
- Safety fields maintained (no answer/selected_option/prediction)

### v0.2 actual Claude Code MCP regression (2026-06-16)

- Actual visible MCP tools: 14 (not 12)
- solve_data_analysis: visible
- solve_logic_reasoning: visible
- v0.2 did not add new MCP tools
- The 14 tools were the actual Claude Code visible inventory after restart
- All v0.2 routing scenarios verified in actual client

### v0.3 model-in-the-loop routing review

- MCP route is now advisory, not final
- Claude must review the question type using full semantics
- Claude can override the route if semantic evidence conflicts
- New route fields: possible_modules, model_review_required, override_allowed, review_instruction, conflict_signals
- Improved edge case routing:
  - Sentence ordering ("重新排列") → verbal_reasoning (was quantity_relation)
  - Sentence insertion ("填入文中哪个位置") → verbal_reasoning (was logic_analysis)
  - Main idea ("主要介绍/讲/说明") → verbal_reasoning
  - Three-part analogy ("感想∶主观性∶体会") → analogy_reasoning
  - Data analysis extended ("占全国/比重/同比增长/上述资料") → data_analysis
- Compose prompt now includes model review instructions
- No new MCP tools added
- No automatic answer execution
