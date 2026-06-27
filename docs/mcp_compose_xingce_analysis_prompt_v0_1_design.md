# MCP compose_xingce_analysis_prompt v0.1 Design

## 1. Baseline

- HEAD before change: 9ddbd7e
- tag: stable-route-only-mcp-question-router-9ddbd7e

## 2. Scope

This update adds one prompt-composition MCP tool:

- `compose_xingce_analysis_prompt`

## 3. Purpose

The tool composes a structured analysis prompt from:

- question_text
- options
- module_hint
- image_present
- strict_mode
- route result

It does not solve questions.

## 4. Relationship with existing MCP tools

- `route_xingce_question`: route-only
- `get_*_scaffold`: scaffold-only
- `compose_xingce_analysis_prompt`: prompt-composition-only

## 5. Input schema

- `question_text: str`
- `options: dict[str, str] | None`
- `module_hint: str | None`
- `image_present: bool`
- `strict_mode: bool`
- `include_scaffold_summary: bool`

## 6. Output schema

- `mode: "prompt_composition"`
- `route`: routing result dict
- `prompt_text`: structured analysis prompt for LLM
- `prompt_contract`: safety constraints
- `expected_response_schema`: expected LLM output format
- `warnings`: list of warnings

Excluded top-level fields: answer, selected_option, prediction.

## 7. Prompt contract

- must verify options
- must not force answer
- analysis_only if uncertain
- no answer inside tool
- no solver call
- no CLI integration

## 8. Behavior by route track

- scaffold_guidance: prompt references recommended_tool scaffold
- solver_candidate: prompt notes solver not called, requires LLM analysis
- route_uncertain: prompt requests user clarification, analysis_only only

### 8.1 route_uncertain handling

When `route.recommended_track = route_uncertain`, the compose tool:
- Generates analysis_only-oriented prompt_text
- Includes "模块不确定，不要直接作答"
- Recommends "优先要求用户补充模块/题面/图片/选项"
- Still includes option verification steps for constrained analysis
- prompt_contract.analysis_only_if_uncertain = true

This ensures that insufficient signal inputs (e.g., "条件不足", empty text, too short text) produce safe analysis-only prompts.

## 9. Safety contract

- prompt-composition-only
- no solver call
- no answer selection
- no CLI integration
- no knowledge base modification
- no OCR/OpenCV/PIL/ML dependency
- no external LLM/API
- no fabricated questions

## 10. Testing

25 tests covering: existence, return dict, mode, route, prompt_text, prompt_contract, no answer fields, routing for all 9 modules, prompt content verification, no solver call.

## 11. Future work

Only in separate approved tasks:

- guarded analyze_xingce_question
- CLI integration
- runtime MCP client examples
