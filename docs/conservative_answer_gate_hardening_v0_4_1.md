# Conservative Answer Gate Hardening v0.4.1

## Overview

v0.4.1 hardens the conservative answer gates in compose_xingce_answer_prompt and fixes a routing priority issue where person arrangement questions with "左边/右边" were incorrectly routed to graphic_reasoning.

## Fix 1: Person Arrangement Routing Priority

### Problem

"甲乙丙丁排成一排，甲不在两端，乙在丙左边" was routing to graphic_reasoning because "左边" triggered graphic_keywords before logic_analysis detection.

### Solution

Added person arrangement signal detection BEFORE weak graphic keywords:

- Person/object signals: 甲, 乙, 丙, 丁, 小王, 小李, 小张, 小赵, 张, 王, 李, 杨
- Position signals: 排成一排, 排列, 座位, 坐在, 站在, 相邻, 不相邻, 两端, 中间, 位置, 顺序
- Condition signals: 条件, 可能正确, 一定正确, 不可能, 至少, 至多, 左边, 右边, 前面, 后面

Logic:
- person + position → logic_analysis (strong)
- person + condition → logic_analysis (medium, includes 左边/右边 in logic context)

Strong graphic signals (图形, 展开图, 折叠, 纸盒, 立体图形, etc.) still take priority over arrangement signals.

### Verified

- "甲乙丙丁排成一排，乙在丙左边" → logic_analysis ✅
- "左边给定的是纸盒的展开图" → graphic_reasoning ✅

## Fix 2: Answer Gate for Missing Context

### Problem

compose_xingce_answer_prompt returned answer_allowed=true even when visual/table content was missing, relying only on the prompt to instruct Claude to return analysis_only.

### Solution

Added explicit answer gate controls that block answer_allowed when required context is missing:

#### New Parameters

```python
visual_description: str | None = None
material_present: bool = False
material_text: str | None = None
table_present: bool = False
```

#### Gate Logic

| Condition | answer_allowed | answer_block_reason |
|-----------|----------------|---------------------|
| graphic_reasoning + no image + no visual_description | false | missing_visual_content |
| graphic_reasoning + image_present=true | true | null |
| graphic_reasoning + visual_description ≥ 10 chars | true | null |
| data_analysis + no material + no table + no material_text | false | missing_table_or_material |
| data_analysis + material_present=true | true | null |
| data_analysis + table_present=true | true | null |
| data_analysis + material_text ≥ 10 chars | true | null |
| route_uncertain | false | route_uncertain_without_semantic_override |
| allow_answer=false | false | answer_mode_disabled |
| low/unknown confidence | false | low_confidence |

## Fix 3: New Return Fields

### answer_block_reason

```json
{
  "answer_block_reason": "missing_visual_content | missing_table_or_material | route_uncertain_without_semantic_override | answer_mode_disabled | low_confidence | null"
}
```

### context_requirements

```json
{
  "context_requirements": {
    "requires_visual": true,
    "requires_table_or_material": false,
    "image_present": false,
    "visual_description_present": false,
    "material_present": false,
    "table_present": false,
    "material_text_present": false
  }
}
```

## Answer Gate Section in Prompt

When answer_allowed=false, the prompt now includes:

```
## Answer Gate
answer_allowed = false
answer_block_reason = missing_visual_content

Because the actual figure image or sufficient visual description is missing, return mode = analysis_only and answer = null.
```

## Backward Compatibility

- Old calls without new parameters work as before (gate checks based on existing parameters)
- Version changed from "v0.4" to "v0.4.1"
- All existing tests updated to accept both versions

## Test Status

- MCP guidance tests: 198 passed (was 181, +17)
- Full pytest: 529 passed (was 512, +17)

## Safety

- No answer / selected_option / prediction in tool return
- No external LLM/API call
- No solver/scaffold/all_cards/cli modification
- No analyze_xingce_question developed

## Actual Claude Code MCP Regression (2026-06-16)

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
