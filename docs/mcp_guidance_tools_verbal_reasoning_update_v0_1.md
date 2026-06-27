# MCP Guidance Tools Verbal Reasoning Update v0.1

## 1. Baseline

- HEAD before change: 1a28f69
- tag: stable-verbal-reasoning-scaffold-1a28f69

## 2. Scope

This update adds one read-only MCP guidance tool:

- `get_verbal_reasoning_scaffold`

## 3. Tool contract

The tool:

- returns `build_verbal_reasoning_scaffold()`
- accepts no question input
- accepts no option input
- accepts no image input
- does not solve verbal reasoning questions
- does not compute final answers
- does not select an option
- does not return answer / selected_option / prediction
- does not call solver
- does not modify knowledge base

## 4. Boundary

Confirm:

- no CLI integration
- no solver modification
- no scaffold source modification
- no real-case package
- no fabricated questions
- no OCR/OpenCV/PIL/ML dependency
- no external LLM/API
- no network

## 5. Testing

Record:

- tests/test_mcp_guidance_tools_preview.py -q
- tests/test_verbal_reasoning_scaffold.py -q
- tests/test_quantity_relation_scaffold.py -q
- tests/test_graphic_reasoning_scaffold.py -q
- tests/test_judgement_reasoning_scaffolds.py -q
- python -m pytest -q

## 6. Recommendation

The tool can be committed as a read-only MCP guidance update. It must remain guidance-only and disconnected from solver/CLI unless a separate guarded integration task is approved.
