# RELEASE MANIFEST

## Release Identity

- Release Version: huasheng-mcp v0.6.0
- Python Package Version: 0.6.0
- Graphic Reasoning Scaffold: v0.2.1 visual grounding baseline
- Source Baseline Commit: 148400a
- Runtime Package Kind: clean

## Scope

This release uses the original graphic_reasoning_scaffold v0.2.1 visual grounding baseline.

Included v0.2.1 fields:
- specialized_templates
- visual_transcription_protocol
- anti_pattern_guards
- black_white_operation_rules
- falsification_protocol
- spatial_verification_protocol
- uncertainty_reporting_protocol

Not included:
- v0.2.2 error-driven addendum
- v0.2.3 answer decision policy
- v0.2.4 final answer fallback policy
- v0.2.5 controlled fallback rollback
- text-image external real exam fixtures
- image test assets
- OCR/OpenCV/PIL outputs

## Test Policy

Runtime packages do not include external text-image real exam fixtures.
Tests depending on unavailable external fixtures should be skipped, not failed.

Known clean-runtime self-test baseline for original v0.2.1 package:
- tests/test_graphic_reasoning_scaffold.py: 128 passed
- tests/test_mcp_guidance_tools_preview.py: 261 passed
- full pytest: 662 passed, 35 skipped, 0 failed

Skipped reason:
- external text-image real exam fixtures are not included in runtime packages.

## Protection

- knowledge_base/all_cards.jsonl unchanged
- src/xingce_solver/solvers/data_analysis.py unchanged
- No solver business logic changes
- No OCR/OpenCV/PIL/sklearn/torch/tensorflow added
- No hardcoded real exam answers

## Archive Checksums

Archive SHA256 and final archive sizes are listed outside the zip in:

RELEASE_CHECKSUMS_v0.6.0.txt

This internal manifest intentionally does not record the SHA256 of its containing zip to avoid self-referential checksum invalidation.
