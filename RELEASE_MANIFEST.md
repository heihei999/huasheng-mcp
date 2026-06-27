# Release Manifest

## Release Information

- **Release Version**: v0.6.0
- **Package Version**: 0.6.0
- **Component**: graphic_reasoning_scaffold v0.2.1 visual grounding baseline
- **Source Baseline**: 148400a
- **GitHub Commit**: e08340c
- **Tag**: stable-v0.6.0-graphic-scaffold-visual-grounding
- **Date**: 2026-06-27

## Runtime Packages

| Package | Filename |
|---------|----------|
| clean_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_1_visual_grounding_148400a_clean_runtime.zip |
| online_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_1_visual_grounding_148400a_online_runtime.zip |
| offline_wheelhouse_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_1_visual_grounding_148400a_offline_wheelhouse_runtime.zip |

## Test Results

| Test File | Result |
|-----------|--------|
| tests/test_graphic_reasoning_scaffold.py | 128 passed |
| Full pytest | 662 passed, 35 skipped, 0 failed |

## Verification Checklist

- [x] No image tests included
- [x] No OCR/OpenCV/PIL added
- [x] knowledge_base/all_cards.jsonl unchanged
- [x] data_analysis solver unchanged
- [x] No hardcoded answer sequences
- [x] No new dependencies introduced
- [x] MCP tool count: 15 (unchanged)

## Practical Boundary

- MCP server is NOT an independent auto-solver
- Images are still read by the connected multi-modal LLM
- This release does NOT include image tests
- We do NOT claim graphic reasoning accuracy reaches any specific percentage
