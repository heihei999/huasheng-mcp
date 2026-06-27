# v0.5.0 Module Context Override

## Overview

v0.5.0 adds `module_hint` / `section_context` support to the MCP route tools. When a large language model knows the exam section context (e.g., "类比推理", "资料分析", "言语理解"), the MCP route prioritizes that context over weak keyword-based routing.

## Motivation

In real exam scenarios, LLMs typically see the exam structure:

```text
第三部分 数量关系
第四部分 判断推理
  一、图形推理
  二、定义判断
  三、类比推理
  四、逻辑判断
第五部分 资料分析
```

Without module context, isolated question routing can fail:
- Verbal questions with "构图/图像" may misroute to `graphic_reasoning`
- Quantity questions with "占比/比例" may misroute to `data_analysis`
- Short analogy word groups may route to `route_uncertain`

v0.5.0 solves this by allowing the caller to pass explicit exam section context.

## New Parameters

### `module_hint: str | None`

Explicit module identifier from the caller. Supports:
- Chinese section names: "类比推理", "言语理解", "资料分析", etc.
- Prefixed variants: "判断推理-类比推理"
- English canonical names: "analogy_reasoning", "verbal_reasoning", etc.

### `section_context: str | None`

Raw section text from the exam, e.g., "第四部分 资料分析". The system extracts and normalizes the tail.

## Normalization

The `_normalize_module_hint()` function maps aliases to canonical module names:

| Input | Canonical |
|-------|-----------|
| 图形推理 / 判断推理-图形推理 / graphic_reasoning | graphic_reasoning |
| 定义判断 / 判断推理-定义判断 / definition_judgement | definition_judgement |
| 类比推理 / 判断推理-类比推理 / analogy_reasoning | analogy_reasoning |
| 逻辑判断 / 判断推理-逻辑判断 / logic_reasoning | logic_reasoning |
| 分析推理 / 排列组合式逻辑 / logic_analysis | logic_analysis |
| 资料分析 / data_analysis | data_analysis |
| 数量关系 / quantity_relation | quantity_relation |
| 言语理解 / 言语理解与表达 / verbal_reasoning | verbal_reasoning |

## Routing Behavior

### Priority Order

1. **Strong material signals** ("表中/根据表格/图中数据/上述资料") always force `data_analysis`, regardless of `module_hint`
2. **module_hint** overrides weak keyword-based routing
3. **Heuristic keyword routing** is preserved as `heuristic_module_guess` for audit

### New Return Fields

All route results now include:

```json
{
  "module_guess": "verbal_reasoning",
  "module_hint": "verbal_reasoning",
  "section_context": "言语理解与表达",
  "module_hint_applied": true,
  "module_hint_conflict": false,
  "heuristic_module_guess": "graphic_reasoning",
  "reasoning_signals": ["module_hint_override=verbal_reasoning"],
  "warnings": ["module_hint 'verbal_reasoning' overrides heuristic route 'graphic_reasoning'"]
}
```

## Safety Gates (Unchanged)

`module_hint` does NOT relax any safety gate:

- `graphic_reasoning` + no image/description → `answer_allowed=false, reason=missing_visual_content`
- `data_analysis` + no material/table/text → `answer_allowed=false, reason=missing_table_or_material`
- Strong material signal + no material → `answer_allowed=false, reason=missing_table_or_material`
- `route_uncertain` → `answer_allowed=false`
- `allow_answer=false` → `answer_allowed=false`

## Design Principles

1. **module_hint is advisory** — MCP route is always advisory, not final
2. **Strong signals override hints** — Material signals are safety-critical
3. **No external LLM/API** — No new dependencies or API calls
4. **No answer leakage** — Route results never contain answer/selected_option/prediction
5. **Audit trail** — `heuristic_module_guess` preserves the keyword-based route for review

## Examples

### Analogy with short word group

```python
route_xingce_question("石头∶雕刻∶雕塑", module_hint="类比推理")
# → module_guess: analogy_reasoning, module_hint_applied: True
```

### Verbal with "构图" keyword

```python
route_xingce_question("这段文字通过分析艺术作品的构图方式...", module_hint="言语理解")
# → module_guess: verbal_reasoning (not graphic_reasoning)
```

### Quantity with "占比" keyword

```python
route_xingce_question("某班男生占比40%...", module_hint="数量关系")
# → module_guess: quantity_relation (not data_analysis)
```

### Strong material signal overrides hint

```python
route_xingce_question("表中2018—2022年...", module_hint="数量关系")
# → module_guess: data_analysis (material signal wins)
```

## No Changes To

- solver business logic
- scaffold content
- knowledge_base / all_cards.jsonl
- cli.py
- No new MCP tools (still 15)
- No external LLM/API dependencies

---

## v0.5.1 Edge-Case Fixes

See `docs/module_context_edge_case_hardening_v0_5_1.md` for full details.

### Fix 1: module_hint overrides insufficient_phrase_detected

- Short questions with valid `module_hint` no longer route to `unknown`.
- `insufficient_phrase_detected` is recorded as a warning, not an early return.

### Fix 2: tightened material signal scope

- Removed `"图中"` from strong material signals (too broad).
- When `module_hint` is present, material signal check only examines question text.
- Prevents distractor options ("折线图/柱状图") from overriding `module_hint=定义判断`.
