# v0.5.1 Three-Year Practical Validation

## 1. Validation scope

This report documents the route/gate/scaffold practical validation of xingce-solver MCP v0.5.1 across three consecutive national civil service exam (国考) papers.

**This is a route/gate/scaffold validation, not a final answer accuracy benchmark.**

The MCP server does not solve the question by itself. Claude Code / the connected LLM remains responsible for visual reading, table reading, calculation, reasoning, and final answer selection.

## 2. Candidate package information

| Field | Value |
|-------|-------|
| Source HEAD | b37bd07 |
| Commit | harden module context edge cases |
| Package name | xingce-solver_mcp_final_v0_5_1_b37bd07_clean_runtime_candidate.zip |
| SHA256 | A180EDB1ABB41CF5F54023436495035CD4276B9EAD960DD5F6F11B1F3CFA9560 |
| Size | 629,215 bytes |
| Entries | 87 |
| Zip clean | passed |
| MCP tools | 15 |
| Knowledge base cards | 292 |
| Source MCP guidance tests | 261 passed |
| Source full pytest | 592 passed |
| Actual Claude Code MCP regression | passed |

## 3. Three-year paper coverage

| Paper | Questions | Range | Module scope |
|-------|-----------|-------|--------------|
| 2024 国考《行测》行政执法卷 | 110 | 21—130 | 言语理解, 数量关系, 判断推理(图形/定义/类比/逻辑), 资料分析 |
| 2023 国考《行测》行政执法卷 | 110 | 21—130 | 言语理解, 数量关系, 判断推理(图形/定义/类比/逻辑), 资料分析 |
| 2022 国考《行测》行政执法卷 | 110 | 21—130 | 言语理解, 数量关系, 判断推理(图形/定义/类比/逻辑), 资料分析 |
| **Total** | **330** | | |

## 4. Module coverage

All major exam modules are covered:

- 言语理解 (verbal_reasoning)
- 数量关系 (quantity_relation)
- 判断推理-图形推理 (graphic_reasoning)
- 判断推理-定义判断 (definition_judgement)
- 判断推理-类比推理 (analogy_reasoning)
- 判断推理-逻辑判断 (logic_reasoning)
- 资料分析 (data_analysis)

## 5. v0.4.3 / v0.5.0 / v0.5.1 comparison

### 2024 国考行政执法卷 (110 questions)

| Version | module_hint | Route result |
|---------|-------------|--------------|
| v0.4.3 | no | 55 / 110 |
| v0.5.0 | yes | 108 / 110 |
| v0.5.1 | yes | 110 / 110 |

### Improvement analysis

- v0.4.3 → v0.5.0: +53 questions (from 55 to 108). module_hint/section_context resolves most keyword-ambiguous cases.
- v0.5.0 → v0.5.1: +2 questions (from 108 to 110). Edge-case fixes for insufficient_phrase_detected and distractor option interference.
- v0.5.1 total: 110 / 110 on 2024, and extended to 330 / 330 across three years.

## 6. Three-year aggregate result

| Paper | Route with module_hint | Compose route | Answer gate (complete context) | Leakage |
|-------|------------------------|---------------|-------------------------------|---------|
| 2024 | 110 / 110 | 110 / 110 | 110 / 110 | 0 |
| 2023 | 110 / 110 | 110 / 110 | 110 / 110 | 0 |
| 2022 | 110 / 110 | 110 / 110 | 110 / 110 | 0 |
| **Total** | **330 / 330** | **330 / 330** | **330 / 330** | **0 / 330** |

- Route with module_hint: 330 / 330
- Compose route: 330 / 330
- Answer gate under complete-context simulation: 330 / 330
- Top-level answer / selected_option / prediction leakage: 0 / 330

## 7. Safety checks

| Check | Result |
|-------|--------|
| Top-level answer field in MCP output | 0 / 330 |
| Top-level selected_option field in MCP output | 0 / 330 |
| Top-level prediction field in MCP output | 0 / 330 |
| MCP server error | 0 |
| External LLM/API call | none |
| OCR/ML dependency | none |
| Solver/scaffold/knowledge_base modification | none |

## 8. Interpretation

### What this validates

1. **module_hint / section_context design is effective**: When the LLM provides the exam section name, route accuracy improves from 55/110 (v0.4.3 without hint) to 110/110 (v0.5.1 with hint) on the 2024 paper.

2. **v0.5.1 edge-case fixes work**: The two specific fixes (insufficient_phrase override and distractor option scope tightening) resolved the remaining 2 failures from v0.5.0.

3. **Three-year generalization**: The 330/330 result across 2022-2024 reduces the risk that v0.5.1 only overfits a single paper.

4. **Safety gates are intact**: No answer/selected_option/prediction leakage across all 330 cases.

### What this does NOT validate

1. **Final answer correctness**: MCP route/gate validation is not answer accuracy testing. The connected LLM is responsible for final answer selection.

2. **Visual/table reading**: This test uses complete-context simulation. Real-world multimodal scenarios depend on the LLM's visual reading capability.

3. **Edge cases beyond national exams**: Provincial exams, mock exams, or non-standard question formats may still contain untested patterns.

## 9. Limitations

1. **module_hint is required**: Without module_hint, the system remains conservative and keyword-based routing is intentionally not optimized as a standalone classifier. v0.4.3 without module_hint achieves 55/110 on the 2024 paper.

2. **Route accuracy ≠ answer accuracy**: A correct route provides the right scaffold/method, but the LLM must still apply it correctly.

3. **Complete-context simulation**: This test assumes the LLM has full access to the question, options, and material. Real-world scenarios with missing or corrupted context may behave differently.

4. **Three papers only**: While 330 questions across 3 years is substantial, it does not cover all possible question patterns.

## 10. Release recommendation

Based on the three-year practical validation:

- v0.5.1 achieves 330/330 route/gate validation across three consecutive national exam papers.
- Safety gates are intact with 0/330 leakage.
- The module_hint/section_context design is validated as effective.

**Recommendation**: Proceed to v0.5.1 final release packaging (tag + clean/online/offline runtime packages).
