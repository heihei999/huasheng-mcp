# MCP route_xingce_question v0.1 Design

## 1. Baseline

- HEAD before change: 6fcf83e
- tag: stable-final-solver-scaffold-mcp-closure-6fcf83e

## 2. Scope

This update adds one route-only MCP tool:

- `route_xingce_question`

## 3. Purpose

The tool provides conservative routing from question text/options/module hints to either:

- scaffold guidance tool
- solver_candidate track
- route_uncertain

It does not solve questions.

## 4. Input schema

- `question_text: str` — question stem
- `options: dict[str, str] | None` — answer options
- `module_hint: str | None` — optional module hint
- `image_present: bool` — whether image is present
- `strict_mode: bool` — whether to use strict routing

## 5. Output schema

- `mode: "route_only"`
- `module_guess: str` — one of 9 valid module guesses
- `confidence: "high" | "medium" | "low" | "unknown"`
- `recommended_track: "scaffold_guidance" | "solver_candidate" | "route_uncertain"`
- `recommended_tool: str | None` — MCP tool name or null
- `reasoning_signals: list[str]` — signals that led to the guess
- `fallback_policy: "analysis_only_if_uncertain"`
- `answer_policy: "do_not_answer_inside_router"`
- `warnings: list[str]` — any warnings

Excluded fields: answer, selected_option, prediction.

## 6. Routing rules

- graphic_reasoning: image_present or graphic keywords
- definition_judgement: definition keywords
- analogy_reasoning: analogy structure (A：B pattern)
- logic_reasoning: argument keywords → solver_candidate
- logic_analysis: strong structural signals (甲乙丙, 排序, 位置, 真假, 命题, 如果那么, 只有才, 除非否则, 谁说真话, 条件组合) → scaffold
- quantity_relation: quantity keywords → scaffold
- verbal_reasoning: verbal keywords → scaffold
- data_analysis: data analysis keywords → solver_candidate
- unknown: no strong signal → route_uncertain

### 6.1 route_uncertain hardening (strict_mode only)

When `strict_mode=True`, the router now checks for insufficient signals before keyword matching:

1. **Empty/blank text**: Returns route_uncertain immediately
2. **Insufficient phrases**: "条件不足", "信息不足", "题干不足", "看不出来", "无法判断", "不确定", "缺少选项", "缺少图片", "无明显题型信号", "不知道", "不清楚", "不明白"
3. **Too short text** (< 4 chars): Returns route_uncertain unless image_present or module_hint provided
4. **No options + short text** (< 8 chars): Returns route_uncertain unless image_present or module_hint provided

### 6.2 logic_analysis weak trigger fix

Previously, single "条件" keyword could trigger high-confidence logic_analysis routing. Now requires:
- Strong keywords: 甲乙丙, 甲乙丙丁, 排序, 位置, 真假, 命题, 如果那么, 只有才, 除非否则, 谁说真话, 谁说假话, 条件组合, 逻辑推理
- OR at least 3 structure keywords (条件, 甲, 乙, 丙, 丁) with "条件" present

This prevents "条件不足" from being misrouted to logic_analysis.

## 7. Safety contract

- route-only
- no solver call
- no answer selection
- no CLI integration
- no knowledge base modification
- no OCR/OpenCV/PIL/ML dependency
- no external LLM/API
- no fabricated questions

## 8. Testing

Tests added covering: existence, return dict, mode, answer_policy, no answer fields, routing for all 9 modules, hint confirmation, hint conflict, hint unknown, no solver call.

## 9. Future work

Only in separate approved tasks:

- compose_xingce_analysis_prompt
- guarded analyze_xingce_question
- CLI integration
