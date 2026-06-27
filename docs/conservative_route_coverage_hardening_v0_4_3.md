# Conservative Route Coverage Hardening v0.4.3

## Overview

v0.4.3 is a conservative route coverage enhancement that fixes two coverage gaps identified in the v0.4.2 60-case pressure test. This is NOT a safety gate fix - it does not relax any answer gates or introduce new answering capabilities.

## Changes

### 1. Text-based Arrangement/Sequencing → logic_analysis

**Problem**: Text-based arrangement questions like "四本书从左到右摆放" were misclassified as `graphic_reasoning` because "左边" hit graphic keywords. This blocked legitimate text-based questions from being processed by the logic analysis scaffold.

**Solution**: Added new detection logic for text-based arrangement scenarios with three keyword categories:

- **Object keywords**: Books (书, 语文书, 数学书, 英语书), Programs (节目, 舞蹈, 合唱, 小品), People (选手, 队员, 学生, 老师), Items (课程, 会议, 车辆, 部门)
- **Order keywords**: Direction (从左到右, 从右到左), Sequence (依次, 顺序, 出场, 演出, 摆放), Conditions (可能为真, 可能正确, 一定为真, 一定正确)
- **Position keywords**: 左边, 右边, 最左边, 最右边, 前面, 后面, 相邻, 不相邻, 两端, 中间, 位置

**Detection logic**: All three signal types (object + order + position) must be present to route to `logic_analysis`. This prevents false positives from partial matches.

**Examples**:
- "四本书从左到右摆放，语文书不在最左边，数学书在英语书左边" → logic_analysis
- "A、B、C、D四名选手按顺序出场，A早于C，B不相邻D" → logic_analysis
- "五个节目依次演出，舞蹈在合唱前面，小品不在最后" → logic_analysis

### 2. Definition Judgement Coverage Enhancement

**Problem**: Clear definition questions like "所谓机会成本，是指...下列体现" were routed to `route_uncertain` because the definition pattern was not recognized by existing keywords.

**Solution**: Added new detection logic with two keyword categories:

- **Definition intro keywords**: 所谓, 是指, 指的是, 定义为, 是指在, 指在, 概念, 定义, 称为
- **Definition question keywords**: 下列, 以下, 哪项, 属于, 不属于, 符合, 不符合, 体现, 没有体现, 最符合, 最不符合

**Detection logic**: Both definition_intro AND definition_question must be present to route to `definition_judgement`. This prevents false positives from generic "是指" usage without question context.

**Examples**:
- "所谓机会成本，是指为了得到某种东西而放弃的其他选择中价值最高者。下列体现机会成本的是？" → definition_judgement
- "概念界定：信息茧房是指人们只接触自己感兴趣的信息。下列属于信息茧房的是？" → definition_judgement
- "行政许可是指行政机关根据公民、法人或者其他组织的申请...下列属于行政许可的是？" → definition_judgement

## What This Does NOT Change

1. **No safety gate relaxation**: All answer gates (missing_visual_content, missing_table_or_material, route_uncertain, answer_mode_disabled) remain unchanged.
2. **No new answering capabilities**: MCP server still does not call external LLM/API or produce final answers.
3. **No solver/scaffold/knowledge base modification**: Only routing logic in mcp_server.py was modified.
4. **No regression in existing behaviors**: All v0.4.2 routing patterns (data_analysis, quantity_relation, graphic_reasoning) remain intact.

## Technical Details

**Modified files**:
- `src/xingce_solver/mcp_server.py` - Added text arrangement and definition detection logic
- `tests/test_mcp_guidance_tools_preview.py` - Added 10 new test cases

**Test results**:
- tests/test_mcp_guidance_tools_preview.py: 220 passed (was 210, +10)
- python -m pytest: 551 passed (was 541, +10)

**Commit**: bfa00f9
**Previous HEAD**: a8f7cae

## Actual Claude Code MCP v0.4.3 Regression

- Claude Code was restarted before testing.
- xingce-solver MCP status: Connected.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible.
- MCP server error: none.

### Route coverage regression passed

All 6 new route samples verified:
- Text arrangement questions → logic_analysis (3 samples)
- Definition questions → definition_judgement (3 samples)

### Non-regression passed

All 4 existing route samples verified:
- graphic_reasoning, data_analysis, quantity_relation (2 samples)

### Answer gate regression passed

All 4 gate scenarios verified:
- missing_visual_content
- missing_table_or_material
- route_uncertain_without_semantic_override
- answer_mode_disabled

### Safety check

No answer / selected_option / prediction top-level output.

Full regression report: `outputs/actual_claude_code_mcp_v0_4_3_regression.md`

## ChatGPT-side 60-case Pressure Test

- Package: xingce-solver_mcp_final_v0_4_3_bfa00f9_clean_runtime_candidate.zip
- Total cases: 60
- Exact route matches: 57 / 60
- Safety gate passed: 60 / 60
- Top-level answer/selected_option/prediction leakage: 0 / 60
- No safety-level bug found
- Remaining 3 route issues are conservative route_uncertain cases

Full report: `outputs/v0_4_3_clean_candidate_60_case_pressure_eval_summary.md`

## Next Step

Recommended: tag + backup + build final clean/online/offline runtime packages.
