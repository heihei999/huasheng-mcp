# Data Analysis v3 Release Notes

`solve_data_analysis` v3 is the current frozen stable version for data-analysis draft solving.

## Supported Capabilities

The v3 solver can generate structured solving drafts for:

- base-period amount (`基期量`)
- growth rate (`增长率`)
- growth amount (`增长量`)
- current share (`本期比重`)
- share change / percentage-point change (`比重变化`)
- base-period share (`基期比重`)
- inverse interval growth rate (`逆向间隔增长率`)
- multi-object growth amount ranking (`多对象增长量排序`)
- multi-component base-period share (`多分项基期比重`)
- base-period difference with equal growth rates (`同增长率基期差值`)

It also supports:

- A/B/C/D option parsing
- option-gap analysis
- safe exam-style estimation
- `answer_candidate` matching
- `needs_more_data`
- `warnings`
- method id output through `recommended_methods` and `source_method_ids`

## Output Contract

The solver returns a structured dictionary including:

```text
module
question_type
sub_type
needs_more_data
matched_routes
recommended_methods
extracted_elements
option_gap_analysis
formula_plan
estimation_plan
solving_plan
sub_calculations
ranking_result
formula_notes
computed_result
answer_candidate
source_method_ids
warnings
```

## Limits

- It does not directly process images.
- It does not perform OCR.
- Uploaded images must be read by a multimodal client.
- MCP tools process structured question text, material text, options, and extracted table/chart content.
- Complex table questions depend heavily on transcription quality from the multimodal model.
- Results are exam-style estimates and solving aids, not a mathematical exact-calculation engine.
- It does not implement verbal, logic, quantity, or graphic-reasoning solvers.

## Freeze Note

This version should be used as the stable baseline for real image testing. During image tests, record failures first. Do not immediately patch the solver unless a repeated, well-scoped pattern is confirmed.

Later small enhancements are documented separately. See `docs/data_analysis_v5_release_notes.md` for the v5 additions discovered from DA-06, DA-08, and DA-09 real-image tests.
