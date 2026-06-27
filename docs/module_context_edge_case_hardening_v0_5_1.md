# Module Context Edge-Case Hardening v0.5.1

## Overview

v0.5.1 is a targeted edge-case fix for v0.5.0 module context override, addressing two boundary issues found during 2024 national exam practical retest.

## Fix 1: module_hint overrides insufficient_phrase_detected

**Problem**: When the question text is short (e.g. "作者接下来最可能论述的是："), the `insufficient_phrase_detected` check triggers an early return to `route_uncertain` BEFORE the `module_hint` override logic gets a chance to run.

**Fix**: When `normalized_hint` is valid (non-None), the insufficient phrase check still records the signal as a warning but does NOT early-return to `route_uncertain`. The module_hint override proceeds normally.

**Behavior**:
- `module_hint=言语理解` + short question → `verbal_reasoning` (was: `unknown`)
- `module_hint` absent + "条件不足" → still `route_uncertain` (unchanged)

## Fix 2: tighten data material strong signals

**Problem A**: `"图中"` was in `_DATA_MATERIAL_STRONG_KW`, causing any text containing "图中" (e.g. "图中显示了人际关系图") to trigger data_analysis routing.

**Fix A**: Removed `"图中"` from the strong signal list. `"图中数据"` (specific to data analysis charts) remains.

**Problem B**: Even after removing `"图中"`, options containing `"折线图"` / `"柱状图"` / `"统计表"` as distractors still triggered `_has_data_material_signal(combined)` because `combined = question + options`.

**Fix B**: When `module_hint` is present and applied, the material signal check only examines the **question text**, not the combined question+options text. This prevents distractor options from overriding a valid `module_hint=定义判断`.

**Strong material signals retained** (must appear in question text when hint is present):
- 表中, 表格, 根据表格, 根据下表, 下表, 上表, 统计表
- 统计图, 统计图表, 图表, 根据图表, 图中数据, 图表数据
- 折线图, 柱状图, 条形图, 饼状图
- 材料显示, 根据材料, 上述材料, 上述资料, 根据上述资料, 资料显示

**NOT strong material signals** (removed or never included):
- 图中 (removed - too broad)
- 图, 图形, 下图, 上图, 关系图, 人际关系图, 示意图, 流程图, 结构图

## Priority rules (unchanged from v0.5.0)

1. Strong material signals in question text → `data_analysis` (safety gate)
2. Valid `module_hint` / `section_context` → override weak keyword routing
3. Heuristic keyword routing → only when no `module_hint`
4. `insufficient_phrase_detected` → only when no valid `module_hint`

## Safety gates (NOT relaxed)

- `graphic_reasoning` + no image → `answer_allowed=false` (`missing_visual_content`)
- `data_analysis` + no material → `answer_allowed=false` (`missing_table_or_material`)
- Strong material signal + no material → `answer_allowed=false` (`missing_table_or_material`)
- `route_uncertain` → `answer_allowed=false`
- `allow_answer=false` → `answer_allowed=false`

## What did NOT change

- MCP route is advisory
- MCP does not call external LLM/API
- MCP does not output final answer / selected_option / prediction
- No `analyze_xingce_question`
- No solver/scaffold/knowledge_base modification
- No new MCP tools

## Three-Year Practical Validation

v0.5.1 was validated across three consecutive national exam papers (2022-2024 行政执法卷):

| Paper | Route with module_hint | Leakage |
|-------|------------------------|---------|
| 2024 | 110 / 110 | 0 |
| 2023 | 110 / 110 | 0 |
| 2022 | 110 / 110 | 0 |
| **Total** | **330 / 330** | **0 / 330** |

This validates that v0.5.1 generalizes across multiple exam papers, not just the 2024 paper used during development.

See `docs/v0_5_1_three_year_practical_validation.md` for full details.
