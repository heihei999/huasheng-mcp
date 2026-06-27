# Conservative Answer Prompt Mode v0.4

## Overview

v0.4 adds `compose_xingce_answer_prompt`, a new MCP tool that generates a conservative answer prompt for LLM-in-the-loop answering.

## Key Design Principles

1. **MCP server does not call external LLM/API.** The tool only generates a prompt.
2. **Claude Code is the LLM executor.** The prompt is consumed by Claude Code itself.
3. **compose_xingce_answer_prompt only creates a strict answer prompt.** It does not solve questions or select options.
4. **The prompt allows answer only when exactly one option is justified.** Otherwise the model must return `analysis_only`.
5. **This is still not a pure local rule-based solver.** It leverages LLM reasoning under strict constraints.
6. **This is not a hidden answer generator.** The tool returns no `answer`, `selected_option`, or `prediction` fields.

## New MCP Tool

### compose_xingce_answer_prompt

**Purpose**: Generate a conservative answer prompt with strict constraints, output schema, and safety contract.

**Parameters**:
- `question_text` (str): The question stem
- `options` (dict, optional): Answer options {A: "...", B: "...", ...}
- `module_hint` (str, optional): Hint for module routing
- `image_present` (bool): Whether the question has an image
- `strict_mode` (bool): Enable strict signal detection
- `allow_answer` (bool): Whether answer mode is allowed (default True)

**Returns**:
- `tool`: "compose_xingce_answer_prompt"
- `version`: "v0.4"
- `route`: Route result with v0.3 fields
- `answer_prompt`: The conservative answer prompt text
- `output_schema`: Required JSON output schema for Claude
- `safety_contract`: Safety constraints
- `answer_allowed`: Whether answer mode is permitted
- `analysis_only_required_if`: List of conditions requiring analysis_only
- `model_review_required`: Whether Claude must review the route
- `override_allowed`: Whether Claude can override the route

**Forbidden fields**: `answer`, `selected_option`, `prediction`

## answer_prompt Core Constraints

The generated prompt includes:

1. MCP route is advisory, not final.
2. First review the full question semantics and options.
3. You may override the MCP route if semantic evidence conflicts with the route.
4. Use the corresponding scaffold/method constraints.
5. You may output an answer only if exactly one option is justified.
6. If the question lacks required visual/table/material context, output analysis_only.
7. If the options are incomplete or ambiguous, output analysis_only.
8. If multiple options remain plausible, output analysis_only.
9. Do not guess.
10. Do not default to A or the first option.
11. Do not use case_id, source answer, or hidden labels.
12. Do not invent missing visual/table content.
13. Wrong = 0 has higher priority than more correct answers.

## Output Schema

Claude must output a JSON object:

```json
{
  "mode": "answer | analysis_only",
  "module": "<module_name>",
  "route_module_guess": "<from route>",
  "route_overridden": false,
  "corrected_module": null,
  "answer": "A/B/C/D/null",
  "confidence": "high | medium | low",
  "reasoning_summary": "...",
  "eliminated_options": [],
  "risk_flags": [],
  "analysis_only_reason": null,
  "safety_checks": {
    "read_full_question": true,
    "read_all_options": true,
    "module_reviewed": true,
    "missing_visual_or_table": false,
    "options_complete": true,
    "unique_option_justified": true,
    "no_guessing": true
  }
}
```

### Schema Rules

- `mode = answer`: `answer` must be A/B/C/D
- `mode = analysis_only`: `answer` must be null
- `confidence = low`: `mode` must be `analysis_only`
- `missing_visual_or_table = true`: `mode` must be `analysis_only`
- `unique_option_justified = false`: `mode` must be `analysis_only`

## analysis_only_required_if

The tool returns a list of conditions that require `analysis_only`:

- `missing_visual_content`
- `missing_table_or_material`
- `incomplete_options`
- `ambiguous_module`
- `multiple_plausible_options`
- `low_confidence`
- `route_uncertain_without_semantic_override`
- `calculation_not_reproducible`
- `option_text_too_sparse`

## Module-Specific Constraints

### Graphic Reasoning
- If the actual figure image or a sufficiently detailed figure description is missing, return analysis_only.
- Do not invent visual features.

### Data Analysis
- If the table, chart, paragraph material, or required numeric data is missing, return analysis_only.
- All calculations must be reproducible from the visible data.

### Verbal Reasoning
- For main idea, sentence ordering, insertion, and logical fill-in questions, avoid over-interpreting.
- If two options are semantically close and cannot be uniquely separated, return analysis_only.

### Analogy Reasoning
- Identify the relationship in the stem before comparing options.
- If multiple relation dimensions are plausible and not uniquely resolved, return analysis_only.

### Definition Judgement
- Extract necessary definition conditions first.
- Compare each option against the conditions.
- If the definition boundary is unclear, return analysis_only.

### Logic Reasoning
- Identify conclusion, premise, assumption, strengthen/weaken direction first.
- Do not select an option only because it sounds relevant.

### Quantity Relation
- Set variables explicitly.
- Calculation must be reproducible.
- If the problem type or equation is uncertain, return analysis_only.

### Logic Analysis
- List constraints explicitly.
- If possible, verify options by constraint checking.
- If constraints are insufficient for a unique answer, return analysis_only.

## MCP Tool Inventory

After v0.4, the total MCP tools count is **15**:

- 8 core practical tools (route, compose analysis, 6 scaffolds)
- 4 legacy/base knowledge tools
- 2 solver candidate tools
- 1 answer prompt composer (new in v0.4)

## Test Status

- tests/test_mcp_guidance_tools_preview.py: 181 passed (was 153, +28)
- python -m pytest: 512 passed (was 484, +28)

## Safety

- No external LLM/API calls
- No solver modification
- No scaffold modification
- No knowledge base modification
- No `answer`/`selected_option`/`prediction` in tool output
- No `analyze_xingce_question` developed

## v0.4.1 Conservative Answer Gate Hardening

**Updated**: 2026-06-16

### Changes

1. **Person arrangement routing priority**: "左边/右边" in person arrangement context (甲乙丙丁排成一排) now correctly routes to logic_analysis instead of graphic_reasoning.

2. **Answer gate for missing context**:
   - graphic_reasoning without image/visual_description → answer_allowed=false
   - data_analysis without material/table/material_text → answer_allowed=false

3. **New parameters**:
   - visual_description: str | None
   - material_present: bool
   - material_text: str | None
   - table_present: bool

4. **New return fields**:
   - answer_block_reason: str | None
   - context_requirements: dict

### Test Status (v0.4.1)

- tests/test_mcp_guidance_tools_preview.py: 198 passed (was 181, +17)
- python -m pytest: 529 passed (was 512, +17)

### Safety (v0.4.1)

- No answer / selected_option / prediction in tool return
- No external LLM/API call
- No solver/scaffold/all_cards/cli modification
- No analyze_xingce_question developed

See `docs/conservative_answer_gate_hardening_v0_4_1.md` for full details.

## Actual Claude Code MCP Regression (2026-06-16)

- The actual Claude Code MCP client loaded v0.4 successfully.
- xingce-solver MCP status: Connected.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible.
- The new tool returns answer_prompt / output_schema / safety_contract / analysis_only_required_if.
- The tool does not return answer / selected_option / prediction.
- route_xingce_question compatibility regression passed.
- route_uncertain remains conservative.
- No external LLM/API call.
- No analyze_xingce_question.
- No MCP server error.
- v0.4 passed actual Claude Code MCP client regression.

See `outputs/actual_claude_code_mcp_v0_4_regression.md` for full regression report.

## v0.4.1 Actual Claude Code MCP Regression (2026-06-16)

- Claude Code was restarted before testing.
- xingce-solver MCP status: Connected.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible.
- MCP server error: none.

### Route regression

- "甲乙丙丁排成一排，乙在丙左边" → logic_analysis (not graphic_reasoning) ✅
- "左边给定的是纸盒的展开图" → graphic_reasoning ✅

### Answer gate regression

- graphic_reasoning without image → answer_allowed=false, missing_visual_content ✅
- graphic_reasoning with image → answer_allowed=true ✅
- data_analysis without material → answer_allowed=false, missing_table_or_material ✅
- data_analysis with material → answer_allowed=true ✅
- route_uncertain → answer_allowed=false, route_uncertain_without_semantic_override ✅
- allow_answer=false → answer_allowed=false, answer_mode_disabled ✅

### Safety

- No answer / selected_option / prediction top-level output
- No external LLM/API call
- No analyze_xingce_question

v0.4.1 passed actual Claude Code MCP client regression.

See `outputs/actual_claude_code_mcp_v0_4_1_regression.md` for full regression report.

## v0.4.2 Data Material Gate Hardening

**Updated**: 2026-06-16

### Problem

Questions with explicit material/table/chart signals (like "表中", "根据表格", "上述资料") were being routed to quantity_relation instead of data_analysis, bypassing the missing_table_or_material gate.

### Fix

1. Added `_DATA_MATERIAL_STRONG_KW` list with explicit material signals
2. Added `_has_data_material_signal()` helper function
3. Updated routing to check material signals BEFORE quantity_relation
4. Added independent material gate in compose_xingce_answer_prompt
5. Updated context_requirements.requires_table_or_material

### Test Status (v0.4.2)

- tests/test_mcp_guidance_tools_preview.py: 210 passed (was 198, +12)
- python -m pytest: 541 passed (was 529, +12)

See `docs/data_material_gate_hardening_v0_4_2.md` for full details.

## v0.4.3 Conservative Route Coverage Hardening

**Updated**: 2026-06-16

### Problem

1. Text-based arrangement questions (e.g., "四本书从左到右摆放") were misclassified as graphic_reasoning due to "左边" hitting graphic keywords.
2. Clear definition questions (e.g., "所谓机会成本，是指...下列体现") were routed to route_uncertain.

### Fix

1. Added text-based arrangement detection with object + order + position keywords
2. Added definition intro + question pattern detection
3. Both require multiple signal types to prevent false positives

### Test Status (v0.4.3)

- tests/test_mcp_guidance_tools_preview.py: 220 passed (was 210, +10)
- python -m pytest: 551 passed (was 541, +10)

See `docs/conservative_route_coverage_hardening_v0_4_3.md` for full details.
