# Project Status After Quantity Relation MCP Guidance

## 1. Stable point

- HEAD: `6593690`
- commit: `update MCP guidance smoke for quantity relation`
- pytest result: 342 passed
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
- 数量关系 MCP guidance：get_quantity_relation_scaffold 已接入并完成 smoke 文档修正

## 3. MCP guidance tools current status

当前 MCP guidance preview 已暴露 5 个 read-only tools：

- get_graphic_reasoning_scaffold
- get_definition_judgement_scaffold
- get_analogy_reasoning_scaffold
- get_logic_analysis_scaffold
- get_quantity_relation_scaffold

其中 get_quantity_relation_scaffold：

- returns build_quantity_relation_scaffold()
- accepts no question/option/image input
- does not return answer / selected_option / prediction
- does not call solver
- remains guidance-only

## 4. Files changed in quantity MCP guidance stage

- `src/xingce_solver/mcp_server.py`
- `tests/test_mcp_guidance_tools_preview.py`
- `docs/mcp_guidance_tools_preview_v0_1_design.md`
- `outputs/mcp_guidance_tools_preview_smoke.md`
- `docs/mcp_guidance_tools_quantity_relation_update_v0_1.md`
- `outputs/mcp_guidance_tools_quantity_relation_update_smoke.md`

## 5. Test coverage

- tests/test_mcp_guidance_tools_preview.py: 34 passed
- tests/test_quantity_relation_scaffold.py: 22 passed
- tests/test_graphic_reasoning_scaffold.py: 23 passed
- tests/test_judgement_reasoning_scaffolds.py: 48 passed
- full pytest: 342 passed

## 6. Boundary guarantees

- no CLI integration
- no solver modification
- no scaffold source modification
- no knowledge base modification
- no real-case package created
- no fabricated questions
- no OCR/OpenCV/PIL/ML dependency
- no external LLM/API
- no network
- no automatic answer selection

## 7. Current architecture

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

- get_graphic_reasoning_scaffold
- get_definition_judgement_scaffold
- get_analogy_reasoning_scaffold
- get_logic_analysis_scaffold
- get_quantity_relation_scaffold

## 8. Remaining untracked local test data

- text-image/analogy_reasoning_real_cases_open_verified_v1/
- text-image/analogy_reasoning_strong_relations_open_verified_v2/
- text-image/definition_judgement_real_cases_open_verified_v1/
- text-image/logic_analysis_real_cases_open_verified_v1/

## 9. Recommended next steps

1. 先备份 6593690 稳定点。
2. 下一大模块建议进入言语理解 verbal scope audit。
3. 言语理解建议先 scaffold，不建议直接强规则 solver。
4. 数量关系 solver core 可以后续另开 isolated small solver 任务。
5. 任何真题包必须由用户提供，不能由 Claude/Codex 查找或杜撰。

## 10. Current conclusion

Quantity relation MCP guidance integration is complete and tested. The project now exposes five read-only MCP guidance tools. These tools remain guidance-only and do not perform solving or answer selection.
