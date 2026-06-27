# Project Status After Verbal Reasoning Scaffold

## 1. Stable point

- HEAD: `e84f42f`
- commit: `add verbal reasoning method scaffold`
- previous tag: `stable-quantity-relation-mcp-guidance-78a7ee6`
- pytest result: 365 passed
- git status: 4 untracked text-image directories only

## 2. Completed before this stage

- 资料分析：solve_data_analysis v5 stable，已冻结
- 论证类逻辑推理：已接入，18 correct / 0 wrong / 2 null
- 翻译推理：已接入，16 correct / 0 wrong / 0 null
- 真假推理：已保守接入，4 correct / 0 wrong / 8 null
- 分析推理：已保守接入，2 correct / 0 wrong / 10 null
- 图形推理 scaffold：已完成、审计、MCP guidance 接入
- 定义判断 scaffold：已完成、审计、MCP guidance 接入
- 类比推理 scaffold：已完成、审计、MCP guidance 接入
- 分析推理 scaffold：已完成、审计、MCP guidance 接入
- 数量关系 scope audit：已完成，65 张卡，推荐 scaffold_first
- 数量关系 scaffold：已完成、审计、记录、备份
- 数量关系 MCP guidance：get_quantity_relation_scaffold 已接入、记录、备份
- 言语理解 scope audit：已完成，77 张卡，A_solver_first 为空，推荐 scaffold_first

## 3. Verbal reasoning scaffold current status

- verbal_reasoning_scaffold v0.1 已完成
- output audit: Passed
- minor concerns: none
- blocking issues: none
- tests/test_verbal_reasoning_scaffold.py: 23 passed
- full pytest: 365 passed
- 未接入 solver
- 未接入 CLI
- 未接入 MCP
- 未创建真题包
- 未修改知识库

## 4. Files added in verbal scaffold stage

- `src/xingce_solver/scaffolds/verbal_reasoning_scaffold.py`
- `tests/test_verbal_reasoning_scaffold.py`
- `docs/verbal_reasoning_v0_1_scaffold_design.md`
- `outputs/verbal_reasoning_scaffold_v0_1_smoke.md`
- `outputs/verbal_reasoning_scaffold_v0_1_output_audit.md`

## 5. Public functions

- `build_verbal_reasoning_scaffold()`
- `get_verbal_reasoning_stage_order()`
- `get_verbal_reasoning_question_type_checklists()`
- `get_verbal_reasoning_method_checklists()`
- `render_verbal_reasoning_prompt_template()`

## 6. Top-level fields

module, version, mode, positioning, stage_order, question_type_router, question_type_checklists, discourse_structure_checklists, cloze_context_checklists, sentence_expression_checklists, method_checklists, option_verification, response_template, uncertainty_policy, must_not_do

## 7. Boundary guarantees

- no solver added
- no MCP integration
- no CLI integration
- no knowledge base modification
- no real-case package created
- no fabricated questions
- no answer / selected_option / prediction top-level field
- no OCR/OpenCV/PIL/ML dependency
- no external LLM/API
- no network

## 8. Current architecture

### Stable solver track

- solve_data_analysis
- solve_logic_reasoning.translation
- solve_logic_reasoning.argument_reasoning
- solve_logic_reasoning.truth_reasoning_guarded
- solve_logic_reasoning.logic_analysis_guarded

### Scaffold track

- graphic_reasoning_scaffold
- definition_judgement_scaffold
- analogy_reasoning_scaffold
- logic_analysis_scaffold
- quantity_relation_scaffold
- verbal_reasoning_scaffold

### MCP guidance preview track

当前已接入：get_graphic_reasoning_scaffold, get_definition_judgement_scaffold, get_analogy_reasoning_scaffold, get_logic_analysis_scaffold, get_quantity_relation_scaffold

尚未接入：get_verbal_reasoning_scaffold

## 9. Remaining untracked local test data

- text-image/analogy_reasoning_real_cases_open_verified_v1/
- text-image/analogy_reasoning_strong_relations_open_verified_v2/
- text-image/definition_judgement_real_cases_open_verified_v1/
- text-image/logic_analysis_real_cases_open_verified_v1/

## 10. Recommended next steps

1. 先备份 e84f42f 稳定点。
2. 下一步可单独做 MCP guidance preview update，新增 get_verbal_reasoning_scaffold。
3. 暂时不要做言语理解强规则 solver。
4. 如果未来拆分 verbal 子 scaffold，应另开独立任务。
5. 任何真题包必须由用户提供，不能由 Claude/Codex 查找或杜撰。

## 11. Current conclusion

verbal_reasoning_scaffold v0.1 is complete, audited, and ready as an isolated LLM guidance component. It should remain disconnected from solver, CLI, and MCP until a separate integration task is explicitly approved.
