# xingce-solver

基于已经整理好的花生十三行测知识库，实现跨平台行测解题辅助工具。

## 当前状态

- 资料分析：`solve_data_analysis v5 stable` 已冻结。
- 逻辑判断：`solve_logic_reasoning v6.1 translation real-case audit` 已完成 real-case audited / tested。
- CLI：`xingce-solver`
- MCP Server：`xingce-solver-mcp`，stdio MCP server。
- 知识库：读取 `knowledge_base/all_cards.jsonl`，不重新解析 PDF，不重新生成卡片。
- 多模态题图：项目本身不做 OCR 或图像识别，由多模态客户端先转写题干、材料和选项，再调用 MCP/CLI。

## 基础命令

```powershell
xingce-solver search --query "比重 增长率"
xingce-solver card --id da_share_change_004
xingce-solver classify --question question.txt
xingce-solver source --method-id da_share_change_004
```

资料分析：

```powershell
xingce-solver solve-data --text "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？ A.100亿元 B.110亿元 C.120亿元 D.132亿元"
```

逻辑判断：

```powershell
xingce-solver solve-logic --text "只有缴费，才可以报名。小王已经报名。根据上述信息，可以推出的是：A.小王没有缴费 B.缴费的人一定报名 C.小王已经缴费 D.没有报名的人一定没有缴费"
```

## MCP Server

```powershell
xingce-solver-mcp
python -m xingce_solver.mcp_server
```

主要 tools (15)：

- `route_xingce_question` - 题型路由（advisory，v0.5.0 支持 module_hint/section_context）
- `compose_xingce_analysis_prompt` - 分析提示词组合（v0.5.0 支持 module_hint/section_context）
- `compose_xingce_answer_prompt` - 保守型答题提示词（v0.4 新增，v0.5.0 支持 module_hint/section_context）
- `get_graphic_reasoning_scaffold` - 图形推理 scaffold
- `get_definition_judgement_scaffold` - 定义判断 scaffold
- `get_analogy_reasoning_scaffold` - 类比推理 scaffold
- `get_logic_analysis_scaffold` - 分析推理 scaffold
- `get_quantity_relation_scaffold` - 数量关系 scaffold
- `get_verbal_reasoning_scaffold` - 言语理解 scaffold
- `get_method_card`
- `search_methods`
- `classify_question`
- `get_source_reference`
- `solve_data_analysis`
- `solve_logic_reasoning`

## 逻辑判断 v6.1

v6.1 在 v6 翻译推理 v1 基础上，用 16 道开放获取真实翻译推理题做审计复测并小范围增强：

- 支持链式条件、链式逆否。
- 支持只有/才、除非/否则。
- 支持且命题否定、或命题、至少一支成立。
- 支持反对命题的摩根等价表达。
- 保持论证类 v5/v6 回归能力。

真实翻译题 16 道结果：

- correct: 16
- wrong: 0
- null: 0

论证类第二批 20 题回归：

- correct: 18
- wrong: 0
- null: 2

相关文件：

- `docs/logic_reasoning_solver_usage.md`
- `docs/logic_reasoning_translation_v1_plan.md`
- `outputs/logic_reasoning_translation_real_v2_results.jsonl`
- `outputs/logic_reasoning_translation_real_v2_summary.md`
- `outputs/logic_reasoning_lr2_v6_1_regression_results.jsonl`
- `outputs/logic_reasoning_lr2_v6_1_regression_summary.md`

## 批量验证

```powershell
python scripts/run_logic_reasoning_real_cases.py --input text-image/logic_translation_real_cases_open_verified_v2/questions_manifest.json --output outputs/logic_reasoning_translation_real_v2_results.jsonl --summary outputs/logic_reasoning_translation_real_v2_summary.md
```

```powershell
python scripts/run_logic_reasoning_real_cases.py --input text-image/lr2_real_verified_20_images/lr2_real_verified_20_images/questions_manifest.json --output outputs/logic_reasoning_lr2_v6_1_regression_results.jsonl --summary outputs/logic_reasoning_lr2_v6_1_regression_summary.md
```

## 测试

```powershell
python -m pytest
powershell -ExecutionPolicy Bypass -File scripts/smoke_test.ps1
```

## 当前限制

- 不修改 `knowledge_base/all_cards.jsonl`。
- 不重新解析 PDF。
- 不重新生成知识卡片。
- 不做 OCR、图片识别、联网或外部 LLM/API 调用。
- 逻辑判断 v6.1 仍不支持真假推理、分析推理、图形推理、定义判断、类比推理。
- 资料分析 v5 已冻结，后续逻辑判断迭代不应修改资料分析 solver。

## v0.4 Actual Claude Code MCP Regression

- The actual Claude Code MCP client loaded v0.4 successfully.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible.
- The new tool returns answer_prompt / output_schema / safety_contract / analysis_only_required_if.
- The tool does not return answer / selected_option / prediction.
- route_xingce_question compatibility regression passed.
- route_uncertain remains conservative.
- No external LLM/API call.
- No analyze_xingce_question.
- Full regression report: `outputs/actual_claude_code_mcp_v0_4_regression.md`

## v0.4.1 Conservative Answer Gate Hardening

- Person arrangement "左边/右边" now correctly routes to logic_analysis (not graphic_reasoning).
- graphic_reasoning without image/visual_description → answer_allowed=false.
- data_analysis without material/table/material_text → answer_allowed=false.
- New return fields: answer_block_reason, context_requirements.
- MCP guidance tests: 198 passed (was 181, +17).
- Full pytest: 529 passed (was 512, +17).
- No external LLM/API call. No solver/scaffold modification.
- Actual Claude Code MCP client regression passed.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible.
- Full regression report: `outputs/actual_claude_code_mcp_v0_4_1_regression.md`

## v0.4.2 Data Material Gate Hardening

- Material/table/chart signals ("表中", "根据表格", "上述资料", "图中数据") now route to data_analysis.
- Independent material gate: even if route misroutes, material signals require material/table context.
- context_requirements.requires_table_or_material reflects material signal detection.
- MCP guidance tests: 210 passed (was 198, +12).
- Full pytest: 541 passed (was 529, +12).
- No external LLM/API call. No solver/scaffold modification.

## v0.4.3 Conservative Route Coverage Hardening

- Text-based arrangement questions (books, programs, contestants) now route to logic_analysis.
- Definition questions with "所谓...是指...下列体现" pattern now route to definition_judgement.
- Both require multiple signal types to prevent false positives.
- All v0.4.2 routing patterns and answer gates remain unchanged.
- MCP guidance tests: 220 passed (was 210, +10).
- Full pytest: 551 passed (was 541, +10).
- No external LLM/API call. No solver/scaffold modification.
- Actual Claude Code MCP v0.4.3 regression passed. Actual visible MCP tools: 15.
- ChatGPT-side 60-case pressure test: 57/60 exact route matches, 60/60 safety gate passed.
- Top-level answer/selected_option/prediction leakage: 0/60. No safety-level bug found.
- Full regression report: `outputs/actual_claude_code_mcp_v0_4_3_regression.md`
- Pressure test report: `outputs/v0_4_3_clean_candidate_60_case_pressure_eval_summary.md`
- Recommended next step: tag + backup + build final clean/online/offline runtime packages.

## v0.5.0 Module Context Override

- Added `module_hint` / `section_context` parameters to route_xingce_question, compose_xingce_analysis_prompt, compose_xingce_answer_prompt.
- Supports Chinese section names (类比推理, 言语理解, 资料分析, etc.) and prefixed variants (判断推理-类比推理).
- module_hint overrides weak keyword routing; strong material signals ("表中/根据表格/图中数据/上述资料") still take priority.
- Returns v0.5.0 fields: module_hint, section_context, module_hint_applied, module_hint_conflict, heuristic_module_guess.
- Safety gates unchanged: missing_visual_content, missing_table_or_material, route_uncertain, allow_answer=false.
- MCP guidance tests: 245 passed (was 220, +25).
- Full pytest: 576 passed (was 551, +25).
- No external LLM/API call. No solver/scaffold/all_cards/cli modification.

## v0.6.0 Graphic Reasoning Scaffold v0.2.2 Error-Driven Addendum

- Upgraded graphic_reasoning_scaffold from v0.2.1 to v0.2.2.
- New protocols: dot_grid_coordinate_protocol (6 set operations), nine_grid_fallback_protocol (rule fallback), cross_section_protocol (geometric guards), residual_check (solid assembly validation), forced_dimensions_by_type (grouping/classification).
- 5 new anti-pattern guards.
- 6 scaffold tools: get_graphic_reasoning_scaffold, get_definition_judgement_scaffold, get_analogy_reasoning_scaffold, get_logic_analysis_scaffold, get_quantity_relation_scaffold, get_verbal_reasoning_scaffold.
- Tests: 712 passed, 35 skipped, 0 failed.
- No OCR/OpenCV/PIL added. No image tests included.
- knowledge_base/all_cards.jsonl unchanged. data_analysis solver unchanged.

## v0.5.1 Module Context Edge-Case Hardening

- Fix 1: valid `module_hint` now overrides `insufficient_phrase_detected` — short questions with explicit hint no longer route to `unknown`.
- Fix 2: removed `"图中"` from strong material signals (too broad); `"图中数据"` retained. When `module_hint` is present, material signal check only examines question text, not options — prevents distractor options ("折线图/柱状图") from overriding `module_hint=定义判断`.
- Strong material signals in question text ("表中/根据表格/图中数据/统计图表/上述资料") still override any module_hint for safety.
- All safety gates unchanged.
- MCP guidance tests: 261 passed (was 245, +16).
- Full pytest: 592 passed (was 576, +16).
- No external LLM/API call. No solver/scaffold/all_cards/cli modification.

## v0.5.1 Three-Year Practical Validation

- Three consecutive national exam papers (2022-2024 行政执法卷) tested: 330 questions total.
- v0.5.1 with module_hint: 330/330 route/gate validation.
- Top-level answer/selected_option/prediction leakage: 0/330.
- This is route/gate/scaffold validation, not final answer accuracy benchmark.
- module_hint/section_context is required for full practical performance.
- Full validation report: `docs/v0_5_1_three_year_practical_validation.md`
