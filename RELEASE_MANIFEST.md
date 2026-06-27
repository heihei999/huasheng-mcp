# Release Manifest

## Release Information

- **Release Version**: v0.6.0
- **Package Version**: 0.6.0
- **Component**: graphic_reasoning_scaffold v0.2.2 error-driven addendum
- **GitHub Commit**: ef2537b
- **Tag**: stable-v0.6.0-graphic-scaffold-visual-grounding
- **Date**: 2026-06-27

## Runtime Packages

| Package | Filename |
|---------|----------|
| clean_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_2_error_driven_ef2537b_clean_runtime.zip |
| online_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_2_error_driven_ef2537b_online_runtime.zip |
| offline_wheelhouse_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_2_error_driven_ef2537b_offline_wheelhouse_runtime.zip |

## Test Results

| Test File | Result |
|-----------|--------|
| tests/test_graphic_reasoning_scaffold.py | 178 passed |
| tests/test_mcp_guidance_tools_preview.py | 261 passed |
| tests/test_logic_reasoning_truth_integration.py | 11 passed, 12 skipped |
| Full pytest | 712 passed, 35 skipped, 0 failed |

## Skipped Tests Explanation

Runtime release packages do NOT include external text-image real exam fixture directories. Tests that depend on these external fixtures will auto-skip when the fixtures are absent. This does NOT affect graphic reasoning scaffold tests or MCP guidance tests, which must always pass.

## Included Major Changes

### graphic_reasoning_scaffold v0.2

- specialized_templates: 7 specialized forced-verification templates
- visual_transcription_protocol: Mandatory visual transcription before reasoning
- anti_pattern_guards: 8 guards against common reasoning failures

### graphic_reasoning_scaffold v0.2.1

- black_white_operation_rules: 8 overlay operation types
- falsification_protocol: 5-step falsification before final answer
- spatial_verification_protocol: Verification for three_views, cube_net, solid_assembly
- uncertainty_reporting_protocol: Confidence level, risk points, competing rules

### graphic_reasoning_scaffold v0.2.2

- dot_grid_coordinate_protocol: Dot/circle grid coordinate set protocol with 6 set operations
- nine_grid_fallback_protocol: Nine-grid rule fallback when quantity/overlay fails
- cross_section_protocol: Cross-section geometric guards in spatial_verification_protocol
- residual_check: Residual vector validation in solid_assembly template
- forced_dimensions_by_type: Forced candidate dimensions for line/polygon and B/W block grouping
- 5 new anti-pattern guards

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
