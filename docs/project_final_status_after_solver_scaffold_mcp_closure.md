# Project Final Status After Solver / Scaffold / MCP Closure

## 1. Stable point

- HEAD: `02cfe35`
- tag: `stable-verbal-reasoning-mcp-guidance-02cfe35`
- commit: document project status after verbal reasoning MCP guidance
- pytest result: 371 passed
- git status: 4 untracked text-image directories only

## 2. Overall conclusion

当前项目已完成三条主线：

- **stable solver track**：资料分析 + 判断推理（翻译/论证/真假/分析）已接入
- **method scaffold track**：6 个 scaffold（图形/定义/类比/分析/数量/言语）已完成
- **read-only MCP guidance preview track**：6 个 MCP guidance tools 已接入

附加确认：

- no CLI integration for scaffold tools
- no automatic answer selection for scaffold tools
- no external LLM/API
- no OCR/ML dependency
- no fabricated real-case package

## 3. Solver track status

### 资料分析

- solve_data_analysis v5 stable
- frozen
- 不建议继续修改

### 判断推理 - 逻辑判断

- 翻译推理：16 correct / 0 wrong / 0 null
- 论证类逻辑推理：18 correct / 0 wrong / 2 null
- 真假推理：4 correct / 0 wrong / 8 null，保守接入
- 分析推理：2 correct / 0 wrong / 10 null，保守接入

原则：

- wrong=0 first
- 不唯一 analysis_only/null
- 不继续硬堆规则

## 4. Scaffold track status

| Scaffold | Status | Audited | Mode | Solver behavior | Auto-select |
|----------|--------|---------|------|----------------|-------------|
| graphic_reasoning_scaffold | complete | yes | method_scaffold_only | no | no |
| definition_judgement_scaffold | complete | yes | method_scaffold_only | no | no |
| analogy_reasoning_scaffold | complete | yes | method_scaffold_only | no | no |
| logic_analysis_scaffold | complete | yes | method_scaffold_only | no | no |
| quantity_relation_scaffold | complete | yes | method_scaffold_only | no | no |
| verbal_reasoning_scaffold | complete | yes | method_scaffold_only | no | no |

## 5. MCP guidance preview status

6 个 read-only MCP guidance tools：

- get_graphic_reasoning_scaffold
- get_definition_judgement_scaffold
- get_analogy_reasoning_scaffold
- get_logic_analysis_scaffold
- get_quantity_relation_scaffold
- get_verbal_reasoning_scaffold

统一 contract：

- no question input
- no option input
- no image input
- returns scaffold dict only
- no answer / selected_option / prediction
- no solver call
- no CLI integration
- guidance-only

## 6. Knowledge base status

- all_cards.jsonl 未修改
- total cards: 292
- module count: 9

模块分布：

- 数量关系：65
- 判断推理-逻辑判断：42
- 判断推理-图形推理：39
- 资料分析：33
- 言语理解-主旨意图：32
- 言语理解-语句表达：25
- 判断推理-类比推理：23
- 言语理解-逻辑填空：20
- 判断推理-定义判断：13

scope audit 已完成：

- 数量关系：65 张卡，推荐 scaffold_first
- 言语理解：77 张卡，A_solver_first 为空，推荐 scaffold_first

## 7. Test baseline

- tests/test_mcp_guidance_tools_preview.py -q: 40 passed
- tests/test_verbal_reasoning_scaffold.py -q: 23 passed
- tests/test_quantity_relation_scaffold.py -q: 22 passed
- tests/test_graphic_reasoning_scaffold.py -q: 23 passed
- tests/test_judgement_reasoning_scaffolds.py -q: 48 passed
- python -m pytest -q: 371 passed

## 8. Current untracked local test data

- text-image/analogy_reasoning_real_cases_open_verified_v1/
- text-image/analogy_reasoning_strong_relations_open_verified_v2/
- text-image/definition_judgement_real_cases_open_verified_v1/
- text-image/logic_analysis_real_cases_open_verified_v1/

## 9. Boundary guarantees

- no solver added in final audit
- no scaffold added in final audit
- no MCP/CLI modification in final audit
- no knowledge base modification
- no real-case package created
- no fabricated questions
- no web search
- no OCR
- no OpenCV/PIL/ML dependency
- no external LLM/API
- no git commit

## 10. Remaining work

### Optional future tasks

- quantity_relation small solver core v0.1 isolated
- future user-provided real-case audit packages
- possible verbal sub-scaffold split
- possible CLI integration only after separate approval

### Not recommended now

- hard-rule verbal reasoning solver
- direct automatic solver for graphic/definition/analogy/verbal reasoning
- adding self-made real-case packages
- expanding rules by answer leakage or case_id

## 11. Recommendation

建议当前先停止扩展功能，保存此稳定点。后续如果继续，必须按 isolated task 单独推进。

---

## 12. Final Claude Code MCP Stable Point

**Updated**: 2026-06-16

### Stable point

- HEAD: `d596e89`
- tag: `stable-actual-claude-code-mcp-inventory-d596e89`
- commit: document actual Claude Code MCP inventory
- parent functional hardening commit: `743208d` harden route-uncertain MCP fallback
- backup zip: `E:\project\xingce-solver-migration-final\backups\xingce-solver_d596e89_actual_claude_code_mcp_inventory_tracked.zip`
- backup note: `E:\project\xingce-solver-migration-final\backups\xingce-solver_d596e89_actual_claude_code_mcp_inventory_backup_note.md`

### Test status

- tests/test_mcp_guidance_tools_preview.py: 99 passed
- full pytest: 430 passed

### Actual Claude Code MCP client status

- Claude Code MCP configured at user scope
- Server: xingce-solver (python -m xingce_solver.mcp_server)
- Status: ✔ Connected

### MCP tool inventory

Actual visible MCP tools in Claude Code: **14** (verified 2026-06-16 after restart)

**Core practical MCP tools: 8**

- route_xingce_question
- compose_xingce_analysis_prompt
- get_graphic_reasoning_scaffold
- get_definition_judgement_scaffold
- get_analogy_reasoning_scaffold
- get_logic_analysis_scaffold
- get_quantity_relation_scaffold
- get_verbal_reasoning_scaffold

**Additional legacy/base knowledge tools: 4**

- classify_question
- search_methods
- get_method_card
- get_source_reference

**Solver candidate tools: 2**

- solve_data_analysis
- solve_logic_reasoning

v0.2 did not add new MCP tools. The 14 tools were the actual Claude Code visible inventory after restart.

### route_uncertain hardening verified

- route_uncertain hardening verified in actual Claude Code client
- "条件不足" now routes to route_uncertain (was incorrectly routing to logic_analysis)
- Strong logic_analysis signal "甲乙丙 排序 位置 条件" still routes to logic_analysis with high confidence
- route/compose do not return answer / selected_option / prediction
- route/compose do not call solver

### Important note

Do not jump directly to analyze_xingce_question automatic answer executor unless planned as a separate high-risk stage.

---

## 13. True-question Routing Hardening v0.2

**Updated**: 2026-06-16

### HEAD

- Baseline before v0.2: fed079f
- HEAD after v0.2 hardening: 55938e6
- Previous stable tag: stable-final-claude-code-mcp-closure-fed079f

### Problems found in true-question coverage testing

1. Analogy symbol `∶` was not recognized
2. Economic/proportion quantity relation questions were not recognized
3. Person-month-city arrangement logic analysis questions were not recognized

### Fixes applied

**Analogy reasoning**: Added `∶` (Chinese ratio symbol) support. Now recognizes:
- "卫冕∶夺冠"
- "酒器∶尊∶爵"

**Quantity relation**: Added economic/proportion keywords with number context requirement:
- 收入, 支出, 盈余, 成本, 万元, 元
- 上半年, 下半年, 全年, 比例, 百分比
- 比去年, 比上年, 增长, 下降

**Logic analysis**: Added person-month-city arrangement detection:
- Person: 张, 王, 李, 杨
- Time: 月, 每月, 每个月
- Place: 城市, 上海, 苏州, 杭州, 南京
- Arrange: 安排, 排布, 对应, 均不同, 不同, 不可能

### Route_uncertain preservation

- "条件不足" → route_uncertain (preserved)
- "条件" → route_uncertain (not high confidence logic_analysis)

### Test status

- tests/test_mcp_guidance_tools_preview.py: 110 passed (was 99)
- full pytest: 441 passed (was 430)

### Safety fields

All route/compose results confirmed:
- No `answer` field
- No `selected_option` field
- No `prediction` field
- No solver call

### Actual Claude Code MCP regression (2026-06-16)

- Actual visible MCP tools: **14** (not 12)
- solve_data_analysis: visible
- solve_logic_reasoning: visible
- v0.2 did not add new MCP tools
- The 14 tools were the actual Claude Code visible inventory after restart
- All v0.2 routing scenarios verified in actual client:
  - "卫冕∶夺冠" → analogy_reasoning / high
  - "酒器∶尊∶爵" → analogy_reasoning / high
  - 经济比例题 → quantity_relation / high
  - 人员-月份-城市排布题 → logic_analysis / high
  - "条件不足" → route_uncertain (preserved)
  - "条件" → route_uncertain (preserved)
  - "甲乙丙 排序 位置 条件" → logic_analysis / high (preserved)

## 14. Model-in-the-Loop Routing Review v0.3

**Updated**: 2026-06-16

### HEAD

- Baseline before v0.3: a0fb94c
- v0.2 code hardening commit: 55938e6
- HEAD after v0.3 model-in-the-loop routing review: 10d0709
- Previous stable tag: stable-v0.2-true-question-routing-mcp-a0fb94c

### Core principle

MCP route is now advisory, not final. Claude must review the question type using full semantics and can override the route if semantic evidence conflicts.

### New route fields

- `possible_modules`: list of candidate modules with reasons and priority
- `model_review_required`: boolean indicating if Claude must review the route
- `override_allowed`: boolean (always true) allowing Claude to override the route
- `review_instruction`: advisory text for Claude
- `conflict_signals`: list of detected conflict signals

### Improved edge case routing

**Sentence ordering**: "重新排列"/"语序正确" → verbal_reasoning (was quantity_relation)
- conflict_signals: contains_排列_but_sentence_order_pattern

**Sentence insertion**: "填入文中哪个位置" → verbal_reasoning (was logic_analysis)
- conflict_signals: contains_位置_but_sentence_insertion_pattern

**Main idea**: "主要介绍/讲/说明" → verbal_reasoning

**Three-part analogy**: "感想∶主观性∶体会" → analogy_reasoning
- conflict_signals: analogy_symbol_detected

**Data analysis extended**: "占全国/比重/同比增长/上述资料" → data_analysis
- Checked before logic_reasoning to avoid "推出" false positive

### Compose prompt changes

- Added "题型复核提示" section at the beginning
- Added possible_modules, model_review_required, override_allowed, conflict_signals to route result
- Added review_instruction to option verification section

### Test status

- tests/test_mcp_guidance_tools_preview.py: 145 passed (was 110, +35)
- full pytest: 476 passed (was 441, +35)

### Safety

- No analyze_xingce_question developed
- No external LLM/API/OCR/ML dependency added
- No all_cards.jsonl modification
- No solver modification
- No scaffold source modification
- No CLI integration
- No new MCP tool added
- No automatic answer execution

## 10. v0.3.1 Analogy Priority Bugfix

### Issue

`感想∶主观性∶体会` was incorrectly routed to `graphic_reasoning` because option A "规律∶客观性∶发现" contained "规律" which triggered graphic_keywords before analogy structure detection.

### Root cause

graphic_keywords check ran before analogy structure detection. The `combined = text + options_text` included "规律" from options, causing graphic_keywords to match first.

### Fix

Moved analogy structure detection to before graphic_keywords check. Analogy structure detection now has priority over graphic keywords for clear A∶B / A∶B∶C patterns with analogy-structured options.

**Modified file**: `src/xingce_solver/mcp_server.py`
- Moved analogy reasoning check block to before graphic reasoning check
- No logic changes, only ordering change

### Verified cases

**Analogy routing (should be analogy_reasoning)**:
- 感想∶主观性∶体会 (options with 规律) → analogy_reasoning ✅
- 卫冕∶夺冠 → analogy_reasoning ✅
- 酒器∶尊∶爵 → analogy_reasoning ✅

**Graphic routing (should be graphic_reasoning)**:
- 从所给四个选项中，选择最合适的一个，使之呈现一定规律。 → graphic_reasoning ✅
- 黑白块位置变化 → graphic_reasoning ✅
- 图形推理：哪一项与题干图形规律一致？ → graphic_reasoning ✅

### Test status

- tests/test_mcp_guidance_tools_preview.py: 153 passed (was 145, +8)
- full pytest: 484 passed (was 476, +8)

### Safety

- No answer / selected_option / prediction fields
- route/compose do not call solver
- no automatic answer executor
- no new MCP tool
- no CLI integration
- no solver modification
- no scaffold modification
- no all_cards.jsonl modification

### Actual Claude Code MCP regression after restart (2026-06-16)

- Claude Code was restarted before regression testing.
- xingce-solver MCP status: Connected.
- Actual visible tools: 14.
- "感想∶主观性∶体会" → analogy_reasoning / high / get_analogy_reasoning_scaffold. Not misrouted to graphic_reasoning.
- "从所给四个选项中，选择最合适的一个，使之呈现一定规律。" → graphic_reasoning / high / get_graphic_reasoning_scaffold.
- v0.3 fields preserved: possible_modules, model_review_required, override_allowed, review_instruction, conflict_signals.
- No answer / selected_option / prediction in any result.
- No MCP server error.
- No file modified during regression.
- v0.3.1 passed actual Claude Code MCP regression after restart.

## 15. Conservative Answer Prompt Mode v0.4

**Updated**: 2026-06-16

### HEAD

- Baseline before v0.4: 6bc28ed
- HEAD after v0.4: c47b633

### New MCP tool

- `compose_xingce_answer_prompt`: Generates conservative answer prompt for LLM-in-the-loop answering.

### Key design

1. MCP server does not call external LLM/API.
2. Claude Code is the LLM executor.
3. compose_xingce_answer_prompt only creates a strict answer prompt.
4. The prompt allows answer only when exactly one option is justified.
5. Otherwise the model must return analysis_only.
6. This is still not a pure local rule-based solver.
7. This is not a hidden answer generator.

### MCP tool inventory

After v0.4, total visible MCP tools: **15**

- 8 core practical tools
- 4 legacy/base knowledge tools
- 2 solver candidate tools
- 1 answer prompt composer (new)

### Test status

- tests/test_mcp_guidance_tools_preview.py: 181 passed (was 153, +28)
- full pytest: 512 passed (was 484, +28)

### Safety

- No external LLM/API calls
- No solver/scaffold/knowledge base modification
- No `answer`/`selected_option`/`prediction` in tool output
- No `analyze_xingce_question` developed

### Actual Claude Code MCP regression (2026-06-16)

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

## 16. Conservative Answer Gate Hardening v0.4.1

**Updated**: 2026-06-16

### HEAD

- Baseline before v0.4.1: cfcefed
- HEAD after v0.4.1: 395d2f3

### Changes

1. **Person arrangement routing priority**: "左边/右边" in person arrangement context (甲乙丙丁排成一排) now correctly routes to logic_analysis instead of graphic_reasoning.

2. **Answer gate for missing context**:
   - graphic_reasoning without image/visual_description → answer_allowed=false
   - data_analysis without material/table/material_text → answer_allowed=false

3. **New parameters**: visual_description, material_present, material_text, table_present

4. **New return fields**: answer_block_reason, context_requirements

### Test status

- tests/test_mcp_guidance_tools_preview.py: 198 passed (was 181, +17)
- full pytest: 529 passed (was 512, +17)

### Safety

- No answer / selected_option / prediction in tool return
- No external LLM/API call
- No solver/scaffold/all_cards/cli modification
- No analyze_xingce_question developed

### Actual Claude Code MCP regression (2026-06-16)

- Claude Code was restarted before testing.
- xingce-solver MCP status: Connected.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible.
- MCP server error: none.

Route regression:
- "甲乙丙丁排成一排，乙在丙左边" → logic_analysis (not graphic_reasoning) ✅
- "左边给定的是纸盒的展开图" → graphic_reasoning ✅

Answer gate regression:
- graphic_reasoning without image → answer_allowed=false, missing_visual_content ✅
- graphic_reasoning with image → answer_allowed=true ✅
- data_analysis without material → answer_allowed=false, missing_table_or_material ✅
- data_analysis with material → answer_allowed=true ✅
- route_uncertain → answer_allowed=false, route_uncertain_without_semantic_override ✅
- allow_answer=false → answer_allowed=false, answer_mode_disabled ✅

Safety:
- No answer / selected_option / prediction top-level output
- No external LLM/API call
- No analyze_xingce_question

v0.4.1 passed actual Claude Code MCP client regression.

See `outputs/actual_claude_code_mcp_v0_4_1_regression.md` for full regression report.

## 17. Data Material Gate Hardening v0.4.2

**Updated**: 2026-06-16

### HEAD

- Baseline before v0.4.2: 23d4dd1
- HEAD after v0.4.2: a8f7cae

### Problem

Questions with explicit material/table/chart signals (like "表中", "根据表格", "上述资料") were being routed to quantity_relation instead of data_analysis, bypassing the missing_table_or_material gate.

### Fix

1. Added `_DATA_MATERIAL_STRONG_KW` list with explicit material signals
2. Added `_has_data_material_signal()` helper function
3. Updated routing to check material signals BEFORE quantity_relation
4. Added independent material gate in compose_xingce_answer_prompt
5. Updated context_requirements.requires_table_or_material

### Test Status

- tests/test_mcp_guidance_tools_preview.py: 210 passed (was 198, +12)
- python -m pytest: 541 passed (was 529, +12)

### Safety

- No answer / selected_option / prediction in tool return
- No external LLM/API call
- No solver/scaffold/all_cards/cli modification
- No analyze_xingce_question developed

See `docs/data_material_gate_hardening_v0_4_2.md` for full details.

## 18. Conservative Route Coverage Hardening v0.4.3

**Updated**: 2026-06-16

### HEAD

- Baseline before v0.4.3: a8f7cae
- HEAD after v0.4.3: bfa00f9

### Problem

1. Text-based arrangement questions (e.g., "四本书从左到右摆放") were misclassified as graphic_reasoning due to "左边" hitting graphic keywords.
2. Clear definition questions (e.g., "所谓机会成本，是指...下列体现") were routed to route_uncertain.

### Fix

1. Added text-based arrangement detection with object + order + position keywords
2. Added definition intro + question pattern detection
3. Both require multiple signal types to prevent false positives

### Test Status

- tests/test_mcp_guidance_tools_preview.py: 220 passed (was 210, +10)
- python -m pytest: 551 passed (was 541, +10)

### Safety

- No answer / selected_option / prediction in tool return
- No external LLM/API call
- No solver/scaffold/all_cards/cli modification
- No analyze_xingce_question developed
- No answer gate relaxation

### Actual Claude Code MCP v0.4.3 Regression

- Claude Code was restarted before testing.
- xingce-solver MCP status: Connected.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible.
- MCP server error: none.
- Route coverage regression: 10/10 passed.
- Answer gate regression: 4/4 passed.
- Safety check: 0/14 answer/selected_option/prediction leakage.
- v0.4.3 passed actual Claude Code MCP client regression.

See `outputs/actual_claude_code_mcp_v0_4_3_regression.md` for full regression report.

### ChatGPT-side 60-case Pressure Test

- Package: xingce-solver_mcp_final_v0_4_3_bfa00f9_clean_runtime_candidate.zip
- Total cases: 60
- Exact route matches: 57 / 60
- Safety gate passed: 60 / 60
- Top-level answer/selected_option/prediction leakage: 0 / 60
- No safety-level bug found
- Remaining 3 route issues are conservative route_uncertain cases, not unsafe answer release
- v0.4.3 clean candidate passed the 60-case pressure test

See `outputs/v0_4_3_clean_candidate_60_case_pressure_eval_summary.md` for full report.

### Next Step

Recommended: tag + tracked backup + build final clean/online/offline runtime packages.

See `docs/conservative_route_coverage_hardening_v0_4_3.md` for full details.

## 19. Module Context Override v0.5.0

### Overview

- Feature: module_hint / section_context override for MCP route tools
- Baseline before v0.5.0: d256bc5
- HEAD after v0.5.0: (pending commit)

### Problem

In real exam scenarios, LLMs typically see the exam section structure (e.g., "第三部分 数量关系", "第四部分 判断推理 - 三、类比推理"). Without module context, isolated question routing can fail:
- Verbal questions with "构图/图像" may misroute to graphic_reasoning
- Quantity questions with "占比/比例" may misroute to data_analysis
- Short analogy word groups may route to route_uncertain

### Fix

1. Added `_normalize_module_hint()` function supporting Chinese section names, prefixed variants, and English canonical names
2. Added `section_context` parameter to route_xingce_question, compose_xingce_analysis_prompt, compose_xingce_answer_prompt
3. module_hint overrides weak keyword routing; strong material signals ("表中/根据表格/图中数据/上述资料") still take priority
4. Returns v0.5.0 fields: module_hint, section_context, module_hint_applied, module_hint_conflict, heuristic_module_guess

### Test Status

- tests/test_mcp_guidance_tools_preview.py: 245 passed (was 220, +25)
- python -m pytest: 576 passed (was 551, +25)

### Safety

- No answer / selected_option / prediction in tool return
- No external LLM/API call
- No solver/scaffold/all_cards/cli modification
- No analyze_xingce_question developed
- No answer gate relaxation

See `docs/module_context_override_v0_5_0.md` for full details.

---

## 13. v0.5.1 Module Context Edge-Case Hardening

### Problems

1. **module_hint blocked by insufficient_phrase_detected**: Short questions like "作者接下来最可能论述的是：" with `module_hint=言语理解` were routed to `unknown` because `insufficient_phrase_detected` triggered an early return before the module_hint override logic ran.

2. **Distractor options override module_hint**: Questions about "人际关系图" with `module_hint=定义判断` were routed to `data_analysis` because the options contained "折线图/柱状图/统计表" which are strong material signals. The material signal check was applied to combined text (question + options).

### Fixes

1. **module_hint overrides insufficient_phrase**: When `normalized_hint` is valid, the insufficient phrase check records the signal as a warning but does NOT early-return to `route_uncertain`. The module_hint override proceeds normally.

2. **Tightened material signal scope**:
   - Removed `"图中"` from `_DATA_MATERIAL_STRONG_KW` (too broad — matches "图中显示了人际关系图").
   - Added `"统计图"`, `"统计图表"`, `"条形图"`, `"图表数据"` (specific data analysis signals).
   - When `module_hint` is present and applied, `_has_data_material_signal()` only checks **question text**, not combined question+options text. This prevents distractor options from overriding a valid module_hint.

### Test Status

- tests/test_mcp_guidance_tools_preview.py: 261 passed (was 245, +16)
- python -m pytest: 592 passed (was 576, +16)

### Safety

- No answer / selected_option / prediction in tool return
- No external LLM/API call
- No solver/scaffold/all_cards/cli modification
- No analyze_xingce_question developed
- No answer gate relaxation
- Strong material signals in question text ("表中/根据表格/图中数据/统计图表/上述资料") still override any module_hint

See `docs/module_context_edge_case_hardening_v0_5_1.md` for full details.

## 20. v0.5.1 Three-Year Practical Validation

**Updated**: 2026-06-20

### Validation

- HEAD: b37bd07
- Package: xingce-solver_mcp_final_v0_5_1_b37bd07_clean_runtime_candidate.zip
- SHA256: A180EDB1ABB41CF5F54023436495035CD4276B9EAD960DD5F6F11B1F3CFA9560

### Three-year result

| Paper | Route with module_hint | Compose route | Answer gate | Leakage |
|-------|------------------------|---------------|-------------|---------|
| 2024 国考行政执法卷 | 110 / 110 | 110 / 110 | 110 / 110 | 0 |
| 2023 国考行政执法卷 | 110 / 110 | 110 / 110 | 110 / 110 | 0 |
| 2022 国考行政执法卷 | 110 / 110 | 110 / 110 | 110 / 110 | 0 |
| **Total** | **330 / 330** | **330 / 330** | **330 / 330** | **0 / 330** |

### Key findings

- module_hint/section_context is required for full practical performance.
- Without module_hint, keyword-based routing is intentionally conservative (55/110 on 2024 paper).
- Three-year validation (330/330) reduces overfitting risk.
- Safety gates intact: 0/330 answer/selected_option/prediction leakage.

### Recommendation

Proceed to v0.5.1 final release packaging.

See `docs/v0_5_1_three_year_practical_validation.md` for full details.
