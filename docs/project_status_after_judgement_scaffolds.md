# Project Status After Judgement Reasoning Scaffolds

## 1. Stable point

- HEAD: `ba6549a`
- commit: `add judgement reasoning method scaffolds`
- pytest result: 286 passed
- judgement scaffold tests: 48 passed
- graphic scaffold tests: 23 passed
- git status: 4 untracked text-image directories only

## 2. Completed before this stage

- 资料分析：solve_data_analysis v5 stable，已冻结
- 论证类逻辑推理：已接入，18 correct / 0 wrong / 2 null
- 翻译推理：已接入，16 correct / 0 wrong / 0 null
- 真假推理：已保守接入，4 correct / 0 wrong / 8 null
- 分析推理：已保守接入，2 correct / 0 wrong / 10 null
- 定义判断：isolated core 已完成，未接入主 solver
- 类比推理：isolated core 已完成，未接入主 solver
- 图形推理：v0.1 isolated method scaffold 已完成并审计通过

## 3. Judgement reasoning scaffold current status

- definition_judgement_scaffold 已完成
- analogy_reasoning_scaffold 已完成
- logic_analysis_scaffold 已完成
- judgement_reasoning_scaffolds output audit: Passed
- minor concerns: none
- blocking issues: none
- 未接入 CLI
- 未接入 MCP
- 未接入 solve_logic_reasoning
- 未修改已有 solver

## 4. Judgement scaffold files added

- `src/xingce_solver/scaffolds/definition_judgement_scaffold.py`
- `src/xingce_solver/scaffolds/analogy_reasoning_scaffold.py`
- `src/xingce_solver/scaffolds/logic_analysis_scaffold.py`
- `tests/test_judgement_reasoning_scaffolds.py`
- `docs/judgement_reasoning_scaffolds_v0_1_design.md`
- `outputs/judgement_reasoning_scaffolds_output_audit.md`

## 5. Public functions

### definition_judgement

- `build_definition_judgement_scaffold()`
- `get_definition_judgement_stage_order()`
- `get_definition_judgement_element_checklists()`
- `render_definition_judgement_prompt_template()`

### analogy_reasoning

- `build_analogy_reasoning_scaffold()`
- `get_analogy_reasoning_stage_order()`
- `get_analogy_reasoning_relation_checklists()`
- `render_analogy_reasoning_prompt_template()`

### logic_analysis

- `build_logic_analysis_scaffold()`
- `get_logic_analysis_stage_order()`
- `get_logic_analysis_structure_checklists()`
- `render_logic_analysis_prompt_template()`

## 6. Top-level fields

### definition_judgement (11 fields)

module, version, mode, positioning, stage_order, question_polarity, definition_elements, option_verification, response_template, uncertainty_policy, must_not_do

### analogy_reasoning (12 fields)

module, version, mode, positioning, stage_order, question_forms, relation_types, relation_verification, option_comparison, response_template, uncertainty_policy, must_not_do

### logic_analysis (12 fields)

module, version, mode, positioning, stage_order, problem_type_router, structure_templates, constraint_extraction, option_verification, response_template, uncertainty_policy, must_not_do

## 7. Boundary guarantees

- no solver integration
- no CLI integration
- no MCP integration
- no external LLM/API
- no network
- no OCR
- no OpenCV
- no PIL/Pillow
- no cv2
- no pytesseract
- no ML dependency
- no automatic answer selection
- no answer / selected_option / prediction top-level field
- analysis_only required when not unique

## 8. Protected files unchanged

- `src/xingce_solver/solvers/data_analysis.py` unchanged
- `src/xingce_solver/solvers/logic_reasoning.py` unchanged
- `src/xingce_solver/solvers/definition_judgement.py` unchanged
- `src/xingce_solver/solvers/analogy_reasoning.py` unchanged
- `src/xingce_solver/solvers/logic_analysis_reasoning.py` unchanged
- `knowledge_base/all_cards.jsonl` unchanged
- `src/xingce_solver/cli.py` unchanged
- `src/xingce_solver/mcp_server.py` unchanged
- `src/xingce_solver/scaffolds/graphic_reasoning_scaffold.py` unchanged

## 9. Current architecture

### Stable solver track

- solve_data_analysis
- solve_logic_reasoning 中的翻译推理
- solve_logic_reasoning 中的论证类逻辑推理
- solve_logic_reasoning 中的真假推理保守接入
- solve_logic_reasoning 中的分析推理保守接入

### Guidance scaffold track

- graphic_reasoning_scaffold
- definition_judgement_scaffold
- analogy_reasoning_scaffold
- logic_analysis_scaffold

## 10. Remaining untracked local test data

These directories remain untracked and should not be added to git:

- `text-image/analogy_reasoning_real_cases_open_verified_v1/`
- `text-image/analogy_reasoning_strong_relations_open_verified_v2/`
- `text-image/definition_judgement_real_cases_open_verified_v1/`
- `text-image/logic_analysis_real_cases_open_verified_v1/`

## 11. Recommended next steps

1. 不要继续堆定义判断 / 类比推理 / 分析推理 pure-rule solver。
2. 不要把 scaffold 当 solver。
3. 下一步可以考虑统一 MCP guidance tools preview integration，但必须另开任务、单独审批。
4. MCP guidance tools 只能 read-only 返回 scaffold，不直接解题、不自动选答案。
5. 数量关系和言语理解仍未开始，属于后续独立大任务。
6. 真假推理 v7.2 小范围 refinement 可作为可选规则增强任务，但 wrong 必须保持 0。

## 12. Current conclusion

judgement_reasoning_scaffolds v0.1 are complete, audited, and ready as isolated LLM guidance components for future MCP preview integration. They should remain isolated until a separate MCP/CLI integration task is explicitly approved.
