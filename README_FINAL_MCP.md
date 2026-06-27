# xingce-solver MCP Server — Final Release Notes

## Overview

xingce-solver is a guidance-only MCP server for 行测 (civil service exam) question analysis. It provides structured scaffolds, routing, and prompt composition for LLM-assisted question solving.

**Important**: This MCP server does NOT output final answers. It only provides structured guidance for multi-modal LLM integration.

## MCP Tools

The server registers 15 MCP tools:

### Core Tools (9)
- `route_xingce_question` — Route questions to appropriate modules
- `compose_xingce_analysis_prompt` — Compose analysis prompts
- `compose_xingce_answer_prompt` — Compose conservative answer prompts
- `get_graphic_reasoning_scaffold` — Graphic reasoning scaffold
- `get_definition_judgement_scaffold` — Definition judgement scaffold
- `get_analogy_reasoning_scaffold` — Analogy reasoning scaffold
- `get_logic_analysis_scaffold` — Logic analysis scaffold
- `get_quantity_relation_scaffold` — Quantity relation scaffold
- `get_verbal_reasoning_scaffold` — Verbal reasoning scaffold

### Knowledge Tools (4)
- `classify_question` — Classify question type
- `search_methods` — Search knowledge base methods
- `get_method_card` — Get specific method card
- `get_source_reference` — Get source reference

### Solver Tools (2)
- `solve_data_analysis` — Data analysis solver
- `solve_logic_reasoning` — Logic reasoning solver

## Recent Changes

### graphic_reasoning_scaffold v0.2 (b168656)
- 7 specialized forced-verification templates
- Visual transcription protocol
- Anti-pattern guards

### graphic_reasoning_scaffold v0.2.1 (9e8fb30)
- Black-white operation rules (8 operation types)
- Falsification protocol
- Spatial verification protocol
- Uncertainty reporting protocol
- Enhanced visual transcription protocol

## Installation

See `pyproject.toml` for dependencies. Set `PYTHONPATH=src` before running.

## Testing

```bash
# Set PYTHONPATH
$env:PYTHONPATH="src"  # PowerShell
export PYTHONPATH=src   # Linux/Mac

# Run graphic reasoning tests
python -m pytest tests/test_graphic_reasoning_scaffold.py -q

# Run MCP guidance tests
python -m pytest tests/test_mcp_guidance_tools_preview.py -q

# Run full test suite
python -m pytest -q
```

## Known Issues

- Some legacy tests depend on external `text-image/` fixture directories containing real exam questions. These directories are NOT included in focused release packages. The affected tests will automatically skip when the fixtures are not present.
- This is by design: the release package focuses on MCP server functionality, not on external test data.
