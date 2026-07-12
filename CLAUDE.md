# xingce-solver Claude Code Rules

This project is a rule-based MCP / CLI solver for Huasheng Shisan 行测 methodology.

Do not use machine learning. Do not import sklearn, torch, tensorflow, statsmodels.
Do not hardcode case IDs or entity-specific rules.
Do not modify knowledge_base/all_cards.jsonl.
Do not modify data_analysis.py.
Do not modify CLI or MCP input schemas.
Do not re-parse PDFs. Do not OCR. Do not call external LLM APIs.
Do not use file diffs. Show full file content when reviewing.
Commit only after tests pass.

For logic_reasoning:
- v5 argument reasoning must not regress.
- v6.1 translation reasoning must not regress.
- truth reasoning must be conservative.
- If truth assignments are not unique, return analysis_only.
- If multiple candidates tie, return analysis_only.
- Never choose the first candidate by list order.
- Never lower thresholds just to answer more cases.

For compose_xingce_answer_prompt (v0.4):
- MCP server does not call external LLM/API.
- Claude Code is the LLM executor.
- The tool only generates a strict answer prompt.
- Answer only when exactly one option is justified.
- Otherwise return analysis_only.
- Do not invent missing visual/table content.
- Do not guess. Do not default to A.
- Wrong = 0 has higher priority than more correct answers.
- v0.4 actual Claude Code MCP client regression passed.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible and works as intended.
- No answer / selected_option / prediction in tool output.
- Full regression report: outputs/actual_claude_code_mcp_v0_4_regression.md

For v0.4.1 conservative answer gate hardening:
- Person arrangement "左边/右边" now routes to logic_analysis (not graphic_reasoning).
- graphic_reasoning without image/visual_description blocks answer_allowed.
- data_analysis without material/table/material_text blocks answer_allowed.
- route_uncertain blocks answer_allowed.
- allow_answer=false always blocks answer_allowed.
- Blocked cases produce analysis_only.
- MCP still does not output final answer.
- No external LLM/API call.
- v0.4.1 actual Claude Code MCP client regression passed.
- Actual visible MCP tools: 15.
- compose_xingce_answer_prompt is visible and works as intended.
- No answer / selected_option / prediction in tool output.
- Full regression report: outputs/actual_claude_code_mcp_v0_4_1_regression.md

For v0.4.2 data material gate hardening:
- Material/table/chart signals ("表中", "根据表格", "上述资料") route to data_analysis.
- Independent material gate: material signals require material/table context.
- context_requirements.requires_table_or_material reflects material signal.
- No external LLM/API call. No solver/scaffold modification.

For v0.4.3 conservative route coverage hardening:
- Text-based arrangement questions (books, programs, contestants) route to logic_analysis.
- Definition questions with "所谓...是指...下列体现" pattern route to definition_judgement.
- Both require multiple signal types to prevent false positives.
- All v0.4.2 routing patterns and answer gates remain unchanged.
- No external LLM/API call. No solver/scaffold modification.
- Actual Claude Code MCP v0.4.3 regression passed. Actual visible MCP tools: 15.
- ChatGPT-side 60-case pressure test: 57/60 exact route matches, 60/60 safety gate passed.
- Top-level answer/selected_option/prediction leakage: 0/60. No safety-level bug found.
- Full regression report: outputs/actual_claude_code_mcp_v0_4_3_regression.md
- Pressure test report: outputs/v0_4_3_clean_candidate_60_case_pressure_eval_summary.md

For v0.5.0 module context override:
- Added module_hint / section_context parameters to route and compose tools.
- Supports Chinese section names (类比推理, 言语理解, 资料分析, etc.).
- module_hint overrides weak keyword routing; strong material signals still take priority.
- Returns v0.5.0 fields: module_hint, section_context, module_hint_applied, module_hint_conflict, heuristic_module_guess.
- Safety gates unchanged: missing_visual_content, missing_table_or_material, route_uncertain, allow_answer=false.
- MCP guidance tests: 245 passed (was 220, +25). Full pytest: 576 passed (was 551, +25).
- No external LLM/API call. No solver/scaffold/all_cards/cli modification.

For v0.5.1 module context edge-case hardening:
- Fix 1: valid module_hint overrides insufficient_phrase_detected; short questions with hint no longer route to unknown.
- Fix 2: removed "图中" from strong material signals; material check uses question text only when hint is present.
- Strong material signals in question text ("表中/图中数据/统计图表/上述资料") still override hint for safety.
- MCP guidance tests: 261 passed (was 245, +16). Full pytest: 592 passed (was 576, +16).
- No external LLM/API call. No solver/scaffold/all_cards/cli modification.
- Three-year practical validation (2022-2024 行政执法卷): 330/330 route/gate. Leakage: 0/330.
- module_hint/section_context is required for full practical performance.
- Full validation report: docs/v0_5_1_three_year_practical_validation.md
