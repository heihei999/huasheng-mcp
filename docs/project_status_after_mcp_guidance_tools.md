# Project Status After MCP Guidance Tools Preview

## 1. Stable point

- HEAD: `36b40ef`
- commit: `add MCP guidance tools preview`
- previous stable tag: `stable-judgement-scaffolds-81355ce`
- pytest result: 314 passed
- MCP guidance tests: 28 passed
- graphic scaffold tests: 23 passed
- judgement scaffold tests: 48 passed
- git status: 4 untracked text-image directories only

## 2. Completed before this stage

- 资料分析：solve_data_analysis v5 stable，已冻结
- 论证类逻辑推理：已接入，18 correct / 0 wrong / 2 null
- 翻译推理：已接入，16 correct / 0 wrong / 0 null
- 真假推理：已保守接入，4 correct / 0 wrong / 8 null
- 分析推理：已保守接入，2 correct / 0 wrong / 10 null
- 图形推理：v0.1 isolated method scaffold 已完成、审计、记录、备份
- 定义判断 scaffold：已完成、审计、记录
- 类比推理 scaffold：已完成、审计、记录
- 分析推理 scaffold：已完成、审计、记录

## 3. MCP guidance tools current status

本阶段新增 4 个 read-only MCP guidance tools：

- `get_graphic_reasoning_scaffold`
- `get_definition_judgement_scaffold`
- `get_analogy_reasoning_scaffold`
- `get_logic_analysis_scaffold`

每个 tool 只返回对应 scaffold dict：

- `get_graphic_reasoning_scaffold` → `build_graphic_reasoning_scaffold()`
- `get_definition_judgement_scaffold` → `build_definition_judgement_scaffold()`
- `get_analogy_reasoning_scaffold` → `build_analogy_reasoning_scaffold()`
- `get_logic_analysis_scaffold` → `build_logic_analysis_scaffold()`

确认：

- tools do not receive question input
- tools do not receive option input
- tools do not receive image input
- tools do not return answer / selected_option / prediction
- tools do not call solver
- tools do not perform automatic answer selection
- tools are guidance-only

## 4. Files added or modified in MCP guidance stage

- `src/xingce_solver/mcp_server.py` (modified)
- `tests/test_mcp_guidance_tools_preview.py` (new)
- `docs/mcp_guidance_tools_preview_v0_1_design.md` (new)
- `outputs/mcp_guidance_tools_preview_smoke.md` (new)

## 5. Test coverage

新增测试覆盖：

- mcp_server import
- 4 个 MCP guidance tool 名称存在
- 4 个 tool 返回 dict
- module 字段正确
- mode == method_scaffold_only
- no answer / selected_option / prediction top-level field
- uncertainty_policy / must_not_do 存在
- analysis_only 存在
- forbidden dependency check
- no solver call in guidance tools

## 6. Boundary guarantees

- no CLI integration
- no solver modification
- no scaffold source modification
- no knowledge base modification
- no image recognition
- no OCR
- no OpenCV
- no PIL/Pillow
- no cv2
- no pytesseract
- no ML dependency
- no external LLM/API
- no network
- no automatic answer selection

## 7. Protected files unchanged

- `src/xingce_solver/solvers/data_analysis.py` unchanged
- `src/xingce_solver/solvers/logic_reasoning.py` unchanged
- `src/xingce_solver/solvers/definition_judgement.py` unchanged
- `src/xingce_solver/solvers/analogy_reasoning.py` unchanged
- `src/xingce_solver/solvers/logic_analysis_reasoning.py` unchanged
- `src/xingce_solver/scaffolds/graphic_reasoning_scaffold.py` unchanged
- `src/xingce_solver/scaffolds/definition_judgement_scaffold.py` unchanged
- `src/xingce_solver/scaffolds/analogy_reasoning_scaffold.py` unchanged
- `src/xingce_solver/scaffolds/logic_analysis_scaffold.py` unchanged
- `knowledge_base/all_cards.jsonl` unchanged
- `src/xingce_solver/cli.py` unchanged

## 8. Current architecture

### Stable solver track

- solve_data_analysis
- solve_logic_reasoning.translation
- solve_logic_reasoning.argument_reasoning
- solve_logic_reasoning.truth_reasoning_guarded
- solve_logic_reasoning.logic_analysis_guarded

### Isolated scaffold track

- graphic_reasoning_scaffold
- definition_judgement_scaffold
- analogy_reasoning_scaffold
- logic_analysis_scaffold

### MCP guidance preview track

- get_graphic_reasoning_scaffold
- get_definition_judgement_scaffold
- get_analogy_reasoning_scaffold
- get_logic_analysis_scaffold

## 9. Remaining untracked local test data

These directories remain untracked and should not be added to git:

- `text-image/analogy_reasoning_real_cases_open_verified_v1/`
- `text-image/analogy_reasoning_strong_relations_open_verified_v2/`
- `text-image/definition_judgement_real_cases_open_verified_v1/`
- `text-image/logic_analysis_real_cases_open_verified_v1/`

## 10. Recommended next steps

1. 不要把 MCP guidance tools 改成 solver。
2. 不要让 guidance tools 直接接收题目并输出答案。
3. 可以先为 36b40ef 创建 tag 和 tracked-files backup。
4. 数量关系仍未开始，后续可以作为独立大任务。
5. 言语理解仍未开始，后续建议优先 scaffold，不建议直接强规则 solver。
6. 真假推理 v7.2 小范围 refinement 可选，但 wrong 必须保持 0。
7. CLI preview command 如果要做，必须另开任务单独审批。

## 11. Current conclusion

MCP guidance tools preview v0.1 is complete and tested. The project now exposes the completed graphic reasoning, definition judgement, analogy reasoning, and logic analysis scaffolds as read-only MCP guidance tools. These tools are not solvers and must remain guidance-only unless a separate integration task is explicitly approved.
