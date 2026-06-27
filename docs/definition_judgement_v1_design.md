# Definition Judgement v1 Design

## 1. Goal

Build an isolated definition judgement core for "定义判断" questions in Chinese civil service exams.

## 2. Scope

v1.0-v1.1 is an **isolated core audit** — NOT integrated into `solve_logic_reasoning`.

Supported question types:
- **Single definition match**: "下列属于X的是"
- **Single definition not match**: "下列不属于X的是"
- **Multi-definition with target**: "下列属于限性遗传的是"
- **Classification**: "下列导语与其分类对应正确的是"
- **Except questions**: "以下除哪项外均属于X"

## 3. Core Structure

### Data Structures

- `DefinitionElement`: kind (subject/object/condition/method/purpose/result/exclusion/action/attribute/keyword) + text + required + polarity
- `DefinitionRule`: term + elements + raw_definition
- `OptionCase`: label + text
- `OptionAssessment`: label + status (matches/violates/unknown) + matched/missing/violated elements + score
- `DefinitionJudgementResult`: status + polarity + definitions + options + assessments + option_status + predicted_label

### Solver Pipeline

1. `detect_question_polarity()` — positive/negative/except_positive/except_negative
2. `parse_definitions()` — extract definitions from question text
3. `extract_elements()` — extract definition elements (subject, method, purpose, etc.)
4. `parse_options()` — parse options from dict
5. `assess_option()` — assess each option against definition
6. `solve_definition_judgement_core()` — main entry point

## 4. Baseline Results (current solver)

Current `solve_logic_reasoning` misclassifies definition questions as 削弱/质疑:
- 12 total, 1 correct, 1 wrong, 10 null

## 5. v1.0-v1.1 Core Audit Results

- total: 12
- solved: 0
- ambiguous: 9
- analysis_only: 3 (008, 010, 011)
- unique_supported: 0
- option_correct: 0
- option_wrong: 0

## 6. Known Limitations

1. **Element extraction**: Too simplistic — misses key attributes like "体小量微" (small in size/quantity)
2. **Option matching**: Pure text matching can't handle semantic relationships (e.g., "毛发、衣物纤维" matches "体小量微")
3. **Multi-definition**: Only handles simple target selection, not complex classification
4. **Polarity detection**: Some edge cases not handled (008, 010, 011)

## 7. Regression Results

Existing capabilities unchanged:
- Truth: 4/12 correct, 0 wrong ✅
- Translation: 16/16 correct, 0 wrong ✅
- Argument: 18/20 correct, 0 wrong ✅
- Analysis: 2/12 correct, 0 wrong ✅

## 8. Recommendation

**Continue v1.2 refinement** focusing on:
1. Better element extraction (key attributes, exclusions)
2. Semantic option matching (keyword overlap, concept matching)
3. Multi-definition classification support

### v1.2-v1.4 (refinement and conditional integration gate)

#### v1.4 improvements

1. **Polarity detection**: added "说法正确/错误", "与定义相符/不符" patterns
2. **Definition parsing**: added ":" format support
3. **Term parsing**: fixed non-greedy regex to not include trailing "是"
4. **Element extraction**: shortened patterns to extract 2-6 char phrases
5. **Option assessment**: switched to phrase-based scoring with definition term + punctuation-split phrases
6. **Score-based selection**: positive questions use highest score, negative questions use violations

#### v1.4 audit results

- total: 12
- solved: 0
- ambiguous: 9
- analysis_only: 2 (006, 010)
- inconsistent: 0
- unique_supported: 0
- option_correct: 0
- option_wrong: 0

#### v1.1 → v1.4 comparison

| metric | v1.1 | v1.4 |
|---|---|---|
| solved | 0 | 0 |
| ambiguous | 9 | 9 |
| analysis_only | 3 | 2 |
| unique_supported | 0 | 0 |

#### Integration gate

**NOT met.** Requirements:
- correct ≥ 3: ❌ (0)
- wrong = 0: ✅
- unique_supported ≥ 3: ❌ (0)

**Not integrating into solve_logic_reasoning.**

#### Why 0 correct

Definition judgement requires **semantic understanding** that pure pattern matching cannot provide. The definition describes abstract concepts (e.g., "微量鉴定" = analyzing trace evidence), and the options describe concrete scenarios (e.g., "analyzing blood alcohol content"). The connection is semantic, not lexical.

Current keyword-based scoring produces 0.00 for all options because the definition vocabulary ("检材", "体小量微", "定性分析") doesn't overlap with option vocabulary ("驾驶人", "血液", "酒精").

#### Recommendation

**Suspend definition judgement** for this question pack. Pure rule-based approach cannot solve definition judgement. Options:
1. Expand/clean the question pack with more structurally clear cases
2. Wait for NLP capability improvement (semantic similarity)
3. Move to other question types (类比推理, etc.)
4. Polarity detection edge cases
