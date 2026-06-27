# Project Status After Quantity Relation Scaffold

## 1. Stable point

- HEAD: `ae4902b`
- commit: `add quantity relation method scaffold`
- previous tag: `stable-mcp-guidance-tools-3ba360e`
- pytest result: 336 passed
- git status: 4 untracked text-image directories only

## 2. Completed before this stage

- 资料分析：solve_data_analysis v5 stable，已冻结
- 论证类逻辑推理：已接入，18 correct / 0 wrong / 2 null
- 翻译推理：已接入，16 correct / 0 wrong / 0 null
- 真假推理：已保守接入，4 correct / 0 wrong / 8 null
- 分析推理：已保守接入，2 correct / 0 wrong / 10 null
- 图形推理 scaffold：已完成、审计、MCP guidance preview 接入
- 定义判断 scaffold：已完成、审计、MCP guidance preview 接入
- 类比推理 scaffold：已完成、审计、MCP guidance preview 接入
- 分析推理 scaffold：已完成、审计、MCP guidance preview 接入
- 数量关系 scope audit：已完成，65 张卡，推荐 scaffold_first

## 3. Quantity relation scaffold current status

- quantity_relation_scaffold v0.1 已完成
- output audit: Passed
- minor concerns: none
- blocking issues: none
- tests/test_quantity_relation_scaffold.py: 22 passed
- 未接入 solver
- 未接入 CLI
- 未接入 MCP
- 未创建真题包
- 未修改知识库

## 4. Files added in quantity scaffold stage

- `src/xingce_solver/scaffolds/quantity_relation_scaffold.py`
- `tests/test_quantity_relation_scaffold.py`
- `docs/quantity_relation_v0_1_scaffold_design.md`
- `outputs/quantity_relation_scaffold_v0_1_smoke.md`
- `outputs/quantity_relation_scaffold_v0_1_output_audit.md`

## 5. Public functions

- `build_quantity_relation_scaffold()`
- `get_quantity_relation_stage_order()`
- `get_quantity_relation_problem_type_checklists()`
- `get_quantity_relation_method_checklists()`
- `render_quantity_relation_prompt_template()`

## 6. Top-level fields

module, version, mode, positioning, stage_order, problem_type_router, problem_type_checklists, method_checklists, option_verification, response_template, uncertainty_policy, must_not_do

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

### MCP guidance preview track

当前已接入：get_graphic_reasoning_scaffold, get_definition_judgement_scaffold, get_analogy_reasoning_scaffold, get_logic_analysis_scaffold

尚未接入：get_quantity_relation_scaffold

## 9. Remaining untracked local test data

- text-image/analogy_reasoning_real_cases_open_verified_v1/
- text-image/analogy_reasoning_strong_relations_open_verified_v2/
- text-image/definition_judgement_real_cases_open_verified_v1/
- text-image/logic_analysis_real_cases_open_verified_v1/

## 10. Recommended next steps

1. 先备份 ae4902b 稳定点。
2. 下一步可单独做 MCP guidance preview update，新增 get_quantity_relation_scaffold。
3. 暂时不要做数量关系 solver，除非另开 isolated small solver core 任务。
4. 言语理解仍未开始，后续建议先做 verbal scope audit 和 scaffold。
5. 任何真题包必须由用户提供，不能由 Claude/Codex 查找或杜撰。

## 11. Current conclusion

quantity_relation_scaffold v0.1 is complete, audited, and ready as an isolated LLM guidance component. It should remain disconnected from solver, CLI, and MCP until a separate integration task is explicitly approved.
