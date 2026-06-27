# Logic Analysis Reasoning v8.0 Design

## 1. Goal

Build an isolated analysis reasoning core for "分析推理" / "朴素逻辑" questions in Chinese civil service exams.

## 2. Scope

v8.0 is an **isolated core audit** — NOT integrated into `solve_logic_reasoning`.

Supported question types:
- **Matching**: person-profession, person-skill, person-research direction
- **Ordering**: positional ordering with adjacency constraints
- **Grouping**: same-group / different-group assignments
- **Comparison**: "X比Y大/多/高" comparison constraints
- **Half-true-half-false**: each person's guess is half right
- **Selection**: selected / not selected / conditional selection

## 3. Core Structure

### Data Structures

- `AnalysisVariable`: name + domain (possible values)
- `AnalysisConstraint`: kind + left/right/relation/value
- `OptionClaim`: label + raw text + parsed assignments
- `AnalysisReasoningResult`: status + variables + constraints + assignments + option mapping

### Solver Pipeline

1. `classify_analysis_task()` — classify question type
2. `extract_variables_and_domains()` — extract entities and their possible values
3. `parse_constraints()` — extract logical constraints
4. `generate_assignments()` — enumerate all possible assignments
5. `filter_consistent_assignments()` — filter by constraints
6. `evaluate_option()` — evaluate options against consistent assignments
7. `solve_analysis_core()` — main entry point

### Search Limits

- Max variables: 7
- Max permutations: 5040 (7!)
- Max cartesian product: 20000
- Exceeding limits → analysis_only

## 4. Baseline Results (current solver)

Current `solve_logic_reasoning` does not handle analysis reasoning:
- 12 total, 0 correct, 0 wrong, 12 null
- All classified as 削弱/翻译推理/基础推出

## 5. Core Audit Results (v0.1)

- total: 12
- solved: 0
- ambiguous: 3
- inconsistent: 0
- analysis_only: 9

Main failure stages:
- entity_domain_extract: most cases fail here (variable/domain extraction incomplete)
- constraint_parse: some constraints not parsed
- option_mapping: not reached for most cases

## 6. Per-Case Results

| case_id | task_type | status | failure_stage |
|---|---|---|---|
| 001 | comparison | analysis_only | entity_domain_extract |
| 002 | ordering_adjacency | analysis_only | entity_domain_extract |
| 003 | grouping | analysis_only | entity_domain_extract |
| 004 | half_true_half_false | analysis_only | entity_domain_extract |
| 005 | matching | analysis_only | entity_domain_extract |
| 006 | half_true_half_false | analysis_only | entity_domain_extract |
| 007 | half_true_half_false | analysis_only | entity_domain_extract |
| 008 | ordering | analysis_only | entity_domain_extract |
| 009 | matching | analysis_only | entity_domain_extract |
| 010 | comparison | ambiguous | option_mapping |
| 011 | ordering | ambiguous | option_mapping |
| 012 | comparison | ambiguous | option_mapping |

## 7. Known Limitations

1. **Variable extraction**: Many cases use descriptive names (小华、小峰) or implicit variables (boxes, drawers). Current parser only handles simple patterns.
2. **Domain extraction**: Domains often need to be inferred from context (e.g., "五个盒子" → positions 1-5).
3. **Half-true-half-false**: Not implemented — requires truth assignment enumeration similar to truth_reasoning.
4. **Ordering constraints**: Position-based constraints need domain values to be integers.
5. **Complex constraints**: "每人只猜对了一半" requires per-person truth evaluation.

## 8. Regression Results

Existing capabilities unchanged:
- Truth reasoning: 4/12 correct, 0 wrong ✅
- Translation: 16/16 correct, 0 wrong ✅
- Argument: 18/20 correct, 0 wrong ✅

## 9. v8.0 → v8.1 Changes

### Improvements

1. **Variable extraction**: `_extract_names_from_text()` handles 甲乙丙丁, A-G星, 小X names, 梅兰竹菊
2. **Domain extraction**: `_extract_domain_from_text()` and `_extract_domain_from_options()` extract domain from question text and options
3. **Option-based domain**: When question text doesn't have explicit domain, extract from options
4. **Comparison constraints**: Improved parsing for "X比Y年龄大", "X在N人中年龄最小"
5. **Position constraints**: Handle "min"/"max" position values
6. **Option mapping**: Proper evaluation for "except" questions, "possible"/"must_true" question types
7. **Half-true-half-false**: Basic detection (not fully implemented)

### v8.1 Results

- total: 12
- solved: 0 (target was ≥2, not met)
- ambiguous: 9
- analysis_only: 3
- unique_supported: 0
- option_correct: 0
- option_wrong: 0

### Why target not met

The main bottleneck is **constraint precision**. Many cases have multiple consistent assignments because:
1. Comparison constraints (age ordering) aren't fully enforced
2. Half-true-half-false constraints aren't implemented
3. Domain values aren't always extracted correctly

### Recommendation

**Continue v8.2 core refinement** focusing on:
1. Position-based comparison constraints (age ordering)
2. Half-true-half-false constraint implementation
3. Option evaluation improvement for comparison-based options

### truth_reasoning_core v8.2 (constraint and option mapping refinement)

#### v8.2 improvements

1. **Half-true-half-false**: Full implementation of `_check_half_true()` with sub-constraint evaluation
2. **Speaker extraction**: Fixed pattern to handle "甲：statement1，statement2" format
3. **Variable extraction for box/color**: Extract box names and color names from question text
4. **Option parsing**: "X第Y" pattern (e.g., "四班第一") now parsed correctly
5. **Half-true detection**: Extended pattern to match "每人都只猜对了一种"
6. **Duplicate constraint removal**: Avoid adding duplicate constraints

#### v8.2 Results

- total: 12
- solved: **1** (004)
- ambiguous: 9
- inconsistent: 1 (007)
- analysis_only: 1 (003)
- unique_supported: 0
- option_correct: 1 (004→C)

#### v8.1 → v8.2 comparison

| metric | v8.1 | v8.2 |
|---|---|---|
| solved | 0 | **1** |
| ambiguous | 9 | 9 |
| inconsistent | 0 | 1 |
| analysis_only | 3 | 1 |
| option_correct | 0 | **1** |

#### Known issues

1. **005**: Variables are speakers instead of boxes; constraint parsing produces noise
2. **007**: Variables are noise; negation parsing produces noise constraints
3. **008, 009**: No variables extracted
4. **001, 010, 012**: Comparison constraints not enforced

#### Recommendation

**Continue v8.3** focusing on:
1. Fix variable extraction for box/color and tea matching questions
2. Fix constraint parsing noise
3. Improve comparison constraint enforcement

### v8.3-v8.4 (audit reconciliation and refinement)

#### Key fixes

1. **Option status bug**: Fixed unconditional override of option_status to "no_supported_option" (line 1096)
2. **Noise constraint filtering**: Filter "不=龙井" type noise from constraint parser
3. **Half-true sub-constraint**: Handle implicit subjects ("不是龙井" → not_equal with "_implicit_" subject)
4. **004 status fixed**: Now correctly shows unique_supported + predicted=C

#### v8.4 Results

- total: 12
- solved: **1** (004)
- ambiguous: 8
- inconsistent: 1 (007 — noise, not real inconsistency)
- analysis_only: 3 (003, 008, 009)
- unique_supported: **1** (004)
- option_correct: **1** (004→C)
- option_wrong: 0

#### v8.2 → v8.4 comparison

| metric | v8.2 | v8.4 |
|---|---|---|
| solved | 1 | 1 |
| ambiguous | 7 | 8 |
| inconsistent | 1 | 1 |
| analysis_only | 3 | 3 |
| unique_supported | 0 | **1** |
| option_correct | 1 | 1 |

#### Integration gate

**NOT met.** Requirements:
- unique_supported ≥ 2: ❌ (only 1)
- option_correct ≥ 2: ❌ (only 1)
- 007 inconsistent is noise: ❌ (not real inconsistency)

**Not integrating into solve_logic_reasoning.**

#### Recommendation

Continue v8.5 focusing on:
1. Fix 007 inconsistent (noise constraints)
2. Improve comparison constraint enforcement (001, 010, 012)
3. Improve variable extraction (005, 008, 009)

### v8.6 (conservative integration)

Met integration gate:
- unique_supported ≥ 2: ✅ (004, 005)
- option_correct ≥ 2: ✅
- option_wrong = 0: ✅
- 007 no longer inconsistent: ✅

Integrated into `solve_logic_reasoning` conservatively:
- Only `solved + unique_supported` → `candidate_ready`
- All other cases → `analysis_only`

Analysis integration: 2 correct, 0 wrong, 10 null.

### v8.7-v8.8 (guardrails and refinement)

#### Guardrail tests

Added `tests/test_logic_reasoning_analysis_integration.py` (13 tests):
- Detection: half-true, box/color, ordering, comparison, translation, truth
- Integration: 004 solved→candidate_ready, 005 solved→candidate_ready, 001 ambiguous→analysis_only, 003 analysis_only→analysis_only
- Non-interference: translation, weaken
- No-default-first

#### v8.8 improvements

1. **Domain extraction**: added skills, vehicles, positions, colors patterns
2. **Constraint parsing**: fixed "X会Y" pattern to require 1-2 char subject
3. **Comparison**: added "X在N人中最大/最小" pattern

#### v8.8 audit results

- total: 12
- solved: 2 (004, 005)
- ambiguous: 7
- analysis_only: 3 (003, 008, 009)
- unique_supported: 2
- option_correct: 2
- option_wrong: 0

#### v8.8 integration results

- correct: 2 (004, 005)
- wrong: 0
- null: 10

#### Regression

- Truth: 4/12 correct, 0 wrong ✅
- Translation: 16/16 correct, 0 wrong ✅
- Argument: 18/20 correct, 0 wrong ✅

#### Remaining issues

- 003, 008, 009: analysis_only (variable/domain extraction insufficient)
- 001, 010, 012: ambiguous (comparison constraints not enforced)
- 006, 007, 011: ambiguous (half-true constraints not specific enough)

#### Recommendation

**Continue v8.9** or **expand/clean analysis question pack**. Current 2/12 correct is a safe baseline but further improvement requires better constraint enforcement and variable extraction.

### v8.9-v9.0 (final core push)

#### v9.0 improvements

1. **Domain extraction**: added skills (编程/插花/绘画/书法) and vehicle types
2. **Domain noise filtering**: "分别研究X学、Y学、Z学" pattern now extracts clean domain
3. **009 improved**: from analysis_only to ambiguous (variables + domain extracted)

#### v9.0 audit results

- total: 12
- solved: 2 (004, 005)
- ambiguous: 8 (001, 002, 006, 007, 009, 010, 011, 012)
- analysis_only: 2 (003, 008)
- unique_supported: 2
- option_correct: 2
- option_wrong: 0

#### v8.8 → v9.0 comparison

| metric | v8.8 | v9.0 |
|---|---|---|
| solved | 2 | 2 |
| ambiguous | 7 | 8 |
| analysis_only | 3 | **2** |
| unique_supported | 2 | 2 |
| option_correct | 2 | 2 |

#### v9.0 integration results

- correct: 2 (004, 005)
- wrong: 0
- null: 10

#### Regression

- Truth: 4/12 correct, 0 wrong ✅
- Translation: 16/16 correct, 0 wrong ✅
- Argument: 18/20 correct, 0 wrong ✅

#### Stop gate judgment

**correct = 2, not improved from v8.8.**

Current 12 题包继续纯规则提升收益较低。主要障碍：
1. 比较约束需要 rank engine（001, 010, 012）
2. 排序约束需要 permutation filtering（002, 011）
3. 半真半假约束需要更完整的 parsing（006, 007）
4. 变量/域提取仍有噪声（003, 008）

**建议暂停当前题包规则堆叠，转题包清洗/扩充或其他题型。**
4. Target unique_supported ≥ 2 for integration gate
