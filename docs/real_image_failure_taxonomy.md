# Real Image Failure Taxonomy

Use these categories when recording real image tests.

## 1. Image Transcription Error

- Definition: The multimodal client incorrectly reads text from the image.
- Judgment: Material, question stem, or options differ from the image.
- Fix direction: Improve prompt, ask for clearer image, or require manual text confirmation.

## 2. Table / Chart Reading Error

- Definition: Rows, columns, chart labels, or values are read incorrectly.
- Judgment: Extracted table/chart structure does not match the image.
- Fix direction: Strengthen table extraction prompt; ask user to crop or upload higher-resolution image.

## 3. Unit Omission

- Definition: Units such as `亿元`, `%`, or `个百分点` are missing.
- Judgment: Extracted values lack units needed for solving.
- Fix direction: Require explicit unit extraction and unit cross-check.

## 4. Year / Time Range Error

- Definition: Years, months, base period, current period, or time ranges are wrong.
- Judgment: Formula variables use the wrong period.
- Fix direction: Add time-expression validation before MCP calls.

## 5. Option Omission

- Definition: One or more A/B/C/D options are not extracted.
- Judgment: MCP cannot match answer candidate due to missing options.
- Fix direction: Require option extraction as a separate checklist item.

## 6. Routing Error

- Definition: `classify_question` returns the wrong module or question type.
- Judgment: Expected data-analysis type is not surfaced in matches.
- Fix direction: Add router rule examples or improve question text passed to MCP.

## 7. Method ID Recommendation Error

- Definition: The solver recommends an unsuitable method card.
- Judgment: `recommended_methods` misses the expected method id.
- Fix direction: Adjust solver routing or method selection rules after repeated evidence.

## 8. Solver Extraction Error

- Definition: MCP receives correct text but solver extracts variables incorrectly.
- Judgment: `formula_plan.variables` or `extracted_elements` is wrong.
- Fix direction: Improve regex/rule extraction with a focused regression test.

## 9. Estimation Strategy Not Exam-Style

- Definition: The process uses unsuitable precision or long brute-force calculation.
- Judgment: Output ignores option gaps or violates method-card constraints.
- Fix direction: Update estimation policy and warnings.

## 10. Answer Candidate Match Error

- Definition: Computed result is reasonable but matched option is wrong.
- Judgment: `answer_candidate` does not correspond to nearest valid option.
- Fix direction: Improve option parsing, unit normalization, or matching rules.

## 11. Client Did Not Call MCP

- Definition: The AI client answers without calling tools.
- Judgment: No MCP tool call trace appears.
- Fix direction: Strengthen assistant prompt and client workflow instructions.

## 12. Client Bypassed MCP And Answered Directly

- Definition: The client uses model memory or visual intuition instead of MCP results.
- Judgment: Final explanation lacks MCP-derived method ids and fields.
- Fix direction: Enforce the assistant prompt and reject direct-answer behavior.

## 13. Output Does Not Cite Method ID

- Definition: Final answer omits `method_id` references.
- Judgment: Explanation lacks `recommended_methods` or `source_method_ids`.
- Fix direction: Require method id citation in final answer format.

## 14. full_material_variable_noise

- Definition: The client passes the full shared data-analysis material into `solve_data_analysis`, causing the solver to extract numbers unrelated to the current question.
- Judgment: `computed_result` uses numbers not referenced by the current question; classification is disturbed by trigger words from other paragraphs; or `method_id` is broadly plausible but `formula_plan.variables` has the wrong subject, time, part/whole, or export/import scope.
- Fix direction: The multimodal client must filter current-question fields first, put unrelated material into `ignored_context`, and pass only current-question key fields to the solver.

## 15. current_question_field_filter_missing

- Definition: The multimodal client does not filter material by current question number before tool calls, so solver input is too long or contains mixed variables.
- Judgment: `question_text` includes multiple questions, options from another question, or many unrelated numbers/rates; `material_key_text` is indistinguishable from the full shared material.
- Fix direction: Strengthen `multimodal_question_reading_prompt`; require `current_question_payload`; before MCP calls, check that `options`, `numbers`, and `rates` are relevant to the current question.
