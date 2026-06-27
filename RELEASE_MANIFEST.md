# Release Manifest

## Package Info

| Field | Value |
|-------|-------|
| Release Version | v0.6.0 |
| Component | graphic_reasoning_scaffold v0.2.1 visual grounding |
| Package Name | xingce-solver_mcp_v0_6_0_graphic_scaffold_v0_2_1_visual_grounding |
| Tag | stable-v0.6.0-graphic-scaffold-visual-grounding |
| Commit | (see final commit below) |
| Date | 2026-06-27 |

## Runtime Packages

| Package | Size | SHA256 |
|---------|------|--------|
| clean_runtime.zip | 1,126,685 bytes | (see SHA256SUMS) |
| online_runtime.zip | 1,127,179 bytes | (see SHA256SUMS) |
| offline_wheelhouse_runtime.zip | 16,181,684 bytes | (see SHA256SUMS) |

## Included Major Changes

### graphic_reasoning_scaffold v0.2 (commit b168656)

- **specialized_templates**: 7 specialized forced-verification templates
  - grid_black_shape
  - complex_black_white_pattern
  - line_symbol_pattern
  - three_views
  - cube_net
  - solid_assembly
  - grouping_classification
- **visual_transcription_protocol**: Mandatory visual transcription before reasoning
- **anti_pattern_guards**: 8 guards against common reasoning failures

### graphic_reasoning_scaffold v0.2.1 (commit 9e8fb30)

- **black_white_operation_rules**: 8 overlay operation types
- **falsification_protocol**: 5-step falsification before final answer
- **spatial_verification_protocol**: Verification for three_views, cube_net, solid_assembly
- **uncertainty_reporting_protocol**: Confidence level, risk points, competing rules
- **visual_transcription_protocol enhanced**: Grid-specific coordinate requirements
- **prompt template updated**: Competing rules, falsification, risk & confidence sections

### Release Packaging Fix (commit 181bfdf, f8af87e, 148400a)

- Added skip logic for tests depending on external text-image fixtures
- Added README_FINAL_MCP.md and RELEASE_MANIFEST.md
- Fixed truth integration test skip for missing external fixture

## Practical Boundary

- MCP server is NOT an independent auto-solver
- MCP provides: question routing, method card retrieval, solving scaffold, prompt constraints, and safety gates
- Images are still read by the connected multi-modal LLM
- This release does NOT include image tests
- We do NOT claim graphic reasoning accuracy reaches any specific percentage

## Test Results (external validation on runtime package)

| Test File | Result |
|-----------|--------|
| tests/test_graphic_reasoning_scaffold.py | 128 passed |
| tests/test_mcp_guidance_tools_preview.py | 261 passed |
| tests/test_logic_reasoning_truth_integration.py | 11 passed, 12 skipped |
| Full pytest | 662 passed, 35 skipped, 0 failed |

## Skipped Tests Explanation

Runtime release packages do NOT include external text-image real exam fixture directories. Tests that depend on these external fixtures will auto-skip when the fixtures are absent. Affected test files:

- test_logic_reasoning_v4_real_cases.py
- test_logic_reasoning_v5_real_cases.py
- test_logic_reasoning_v6_1_real_cases.py
- test_logic_reasoning_translation_v1.py
- test_logic_reasoning_truth_integration.py (TestRealCaseRegression class)

This does NOT affect graphic reasoning scaffold tests or MCP guidance tests, which must always pass.

## Safety Checks

- No image tests included
- No OCR/OpenCV/PIL/sklearn/torch/tensorflow introduced
- knowledge_base/all_cards.jsonl: unchanged
- data_analysis solver: unchanged
- MCP tool count: 15 (unchanged)
- No hardcoded answer sequences
