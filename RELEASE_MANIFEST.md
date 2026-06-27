# xingce-solver Release Manifest

## Release Information

- **Release Version**: v0.6.0
- **Package Version**: 0.6.0
- **Component**: graphic_reasoning_scaffold v0.2.2 error-driven addendum
- **Local Source Commit**: 4e40a2f
- **Date**: 2026-06-27
- **Note**: final GitHub release commit may be recalibrated by Hermes on Linux server

## Runtime Packages

| Package | Filename | Size |
|---------|----------|------|
| clean_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_2_error_driven_4e40a2f_clean_runtime.zip | TBD |
| online_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_2_error_driven_4e40a2f_online_runtime.zip | TBD |
| offline_wheelhouse_runtime | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_2_error_driven_4e40a2f_offline_wheelhouse_runtime.zip | TBD |

## Test Results

| Test File | Result |
|-----------|--------|
| tests/test_graphic_reasoning_scaffold.py | 178 passed |
| tests/test_mcp_guidance_tools_preview.py | 261 passed |
| Full pytest | 747 passed, 0 failed |

## Included Major Changes

### graphic_reasoning_scaffold v0.2 (commit b168656)

- **specialized_templates**: 7 specialized forced-verification templates
- **visual_transcription_protocol**: Mandatory visual transcription before reasoning
- **anti_pattern_guards**: 8 guards against common reasoning failures

### graphic_reasoning_scaffold v0.2.1 (commit 9e8fb30)

- **black_white_operation_rules**: 8 overlay operation types
- **falsification_protocol**: 5-step falsification before final answer
- **spatial_verification_protocol**: Verification for three_views, cube_net, solid_assembly
- **uncertainty_reporting_protocol**: Confidence level, risk points, competing rules
- **visual_transcription_protocol enhanced**: Grid-specific coordinate requirements

### graphic_reasoning_scaffold v0.2.2 (commit 4e40a2f)

- **dot_grid_coordinate_protocol**: Dot/circle grid coordinate set protocol with 6 set operations
- **nine_grid_fallback_protocol**: Nine-grid rule fallback when quantity/overlay fails
- **cross_section**: Cross-section geometric guards in spatial_verification_protocol
- **residual_check**: Residual vector validation in solid_assembly template
- **forced_dimensions_by_type**: Forced candidate dimensions for line/polygon and B/W block grouping
- **5 new anti-pattern guards**: no_intuitive_cross_section_rejection, no_color_count_assumption, no_fuzzy_face_count, no_single_dimension_grouping, no_failed_rule_persistence
- **prompt template updated**: Dot-grid coordinates, nine-grid fallback, cross-section guards, residual check, forced dimensions

## Package Contents

All packages contain:
- src/ (Python source)
- tests/ (test suite)
- docs/ (documentation)
- knowledge_base/ (292 cards)
- README.md
- README_FINAL_MCP.md
- RELEASE_MANIFEST.md
- pyproject.toml
- smoke_test.ps1
- smoke_test_core.py
- install_claude_code_mcp.ps1

## Package Differences

| Package | Additional Content |
|---------|-------------------|
| clean_runtime | None |
| online_runtime | INSTALL_ONLINE.md, install_dependencies.ps1 |
| offline_wheelhouse_runtime | INSTALL_OFFLINE.md, install_dependencies_offline.ps1, wheels/, WHEELHOUSE_MANIFEST.txt |

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
- MCP provides: question routing, method card retrieval, solving scaffold, prompt constraints, and safety gates
- Images are still read by the connected multi-modal LLM
- This release does NOT include image tests
- We do NOT claim graphic reasoning accuracy reaches any specific percentage
