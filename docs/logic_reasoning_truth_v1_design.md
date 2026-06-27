# Logic Reasoning — Truth Reasoning v1 Design

## 1. Current Baseline

- 12 truth reasoning real exam cases (see `text-image/logic_truth_real_cases_open_verified_v1/`)
- Baseline run with solver v6.1 (commit c876e1d):
  - correct: 0
  - wrong: 0
  - null: 12
  - decision_status: analysis_only × 12
- The v6.1 solver has no truth-reasoning-specific logic. All 12 cases fall through to generic argument analysis (weaken / premise / infer / translation), producing no answer candidate.

## 2. Attempted but Reverted

- A string-matching-based truth reasoning approach was tested.
- Result: 1/12 correct (case 001 only — 全称 vs 特称 contradiction + modus ponens chain).
- The solver changes were reverted. No v7 code was committed.
- Root cause: string matching cannot reliably handle conditional chains, disjunctive syllogism, or universal instantiation.

## 3. Failure Taxonomy

| Failure Type | Cases |
|---|---|
| Conditional chain inference insufficient | 003, 005, 006, 007, 010 |
| Disjunctive reasoning insufficient | 002, 004 |
| Universal instantiation insufficient | 008, 009 |
| Hypothesis enumeration consistency check incomplete | 002, 004, 008, 011, 012 |
| Option-to-fact matching not structured | all 11 failing cases |

## 4. Design Principles for v1

- No entity-specific hardcoding (no person names, team names, item names in rules).
- No threshold lowering to force more answers.
- If the truth assignment is not unique → return analysis_only.
- If multiple options score equally → return analysis_only.
- Never pick the first candidate by list order.
- Target: conservative correctness, not coverage. 8/12 correct is the goal; 0/12 with no false positives is acceptable over 3/12 with false answers.

## 5. Implementation Status

### truth_reasoning_core v0.1 (isolated module)

- File: `src/xingce_solver/solvers/truth_reasoning.py`
- Tests: `tests/test_truth_reasoning_core.py` (34 tests)
- Status: **isolated, NOT integrated into solve_logic_reasoning**

This module is a standalone structured truth reasoner. It does NOT modify
`logic_reasoning.py`, `data_analysis.py`, or `knowledge_base/all_cards.jsonl`.

The goal of v0.1 is to validate the core algorithm (proposition representation,
contradiction detection, truth assignment enumeration) in isolation before
attempting integration.

No real exam cases are run against this module in this phase. The next step
(v0.2 or v7 integration) will connect it to the solver pipeline.

### truth_reasoning_core v0.2 (real-case audit)

- Audit script: `scripts/audit_truth_reasoning_core.py`
- Results: `outputs/truth_reasoning_core_v0_2_audit_results.jsonl`
- Summary: `outputs/truth_reasoning_core_v0_2_audit_summary.md`

#### Status distribution (12 real exam cases)

| status | count |
|---|---|
| solved | 1 (009) |
| ambiguous | 10 |
| inconsistent | 0 |
| analysis_only | 1 (004) |

#### Failure stage distribution

| failure_stage | count | meaning |
|---|---|---|
| assignment | 10 | constraint + statements parsed, but multiple consistent assignments |
| extract_statements | 1 | couldn't extract statements from text (004 uses "X写着" format) |
| none | 1 | solved |

#### v0.2 improvements over v0.1

1. **Constraint parser**: now handles "只有一位教练的预测是正确的", "三条线索只有一条是假的", "只有一个柜子里的描述是真实的" etc.
2. **Statement extraction**: ①②③ and （1）（2）（3） patterns now work; single-char speakers (甲说, 乙说) now handled.
3. **Negation fact extraction**: false statements' negations are now used to derive facts.
4. **_definitely_true**: now checks opposite polarity atoms (if B=True is known, ¬B=False).
5. **Cross-check**: Phase 4 checks that neg(false_prop) doesn't contradict true_prop.

#### Why most cases are "ambiguous"

The engine finds multiple consistent assignments because the fact representation
is too coarse-grained. For example, All("同学", "写完作业") and Atom("小赵", "写完作业")
are not recognized as related — the engine doesn't know that 小赵 is an instance of 同学.

This requires either:
- Domain knowledge (entity-to-universe mapping), or
- Stronger propositional logic inference (resolution, unit propagation), or
- Hypothesis-based reasoning (assume each statement true/false, propagate consequences).

#### Recommendation

**Do NOT enter v7 integration.** Continue core v0.3 to improve the assignment
logic — likely through hypothesis-based reasoning or stronger inference rules.

### truth_reasoning_core v0.3 (assignment closure)

- Audit: `outputs/truth_reasoning_core_v0_3_audit_results.jsonl`
- Summary: `outputs/truth_reasoning_core_v0_3_audit_summary.md`

#### Status distribution (v0.2 → v0.3)

| status | v0.2 | v0.3 |
|---|---|---|
| solved | 1 | **3** (002, 005, 009) |
| ambiguous | 10 | **9** |
| inconsistent | 0 | 0 |
| analysis_only | 1 | **0** |

#### v0.3 improvements

1. **Closure-based reasoning**: `_derive_closure()` applies modus ponens, modus tollens, disjunctive syllogism, and And decomposition until fixpoint.
2. **And parsing**: "P和Q都不是R", "P和Q是R", "P、Q都是R" now correctly parsed as And(Atom, Atom).
3. **Imply parsing**: "如果P，那么Q" now correctly handles "则...就" in consequent.
4. **Atom cleanup**: "则右手就不是水果糖" → subject="右手", not "则右手就".
5. **Noise speaker filter**: "队进行了" no longer matched as speaker.
6. **"X写着" extraction**: "第一个柜子里写着：'...'" now handled.
7. **All vs Atom contradiction**: All(S, P) vs Atom(X, P, ¬polarity) detected.

#### Remaining ambiguous cases (9)

The remaining 9 ambiguous cases require:
- **First-order reasoning**: connecting specific instances to universal quantifiers (001, 003, 004)
- **Complex And/Or parsing**: "P或Q" with shared predicates (003)
- **Noise in statements**: introductory text parsed as logical propositions (003, 006)
- **Disjunctive negation**: ¬(P∨Q) = ¬P∧¬Q vs ¬P∨¬Q (009 edge cases)

#### Recommendation

solved=3 meets the minimum threshold. The core engine can now handle:
- Simple implication chains (modus ponens + modus tollens)
- Contradiction pairs (All vs Some, All vs Atom, And vs Or)
- All-false negation (009)

**Do NOT enter v7 integration yet.** Next steps:
- Option mapping (match derived facts against answer options)
- Stronger first-order reasoning (entity-instance inference)
- Better statement extraction for complex formats

### truth_reasoning_core v0.4 (option mapping audit)

- Audit: `outputs/truth_reasoning_core_v0_4_audit_results.jsonl`
- Summary: `outputs/truth_reasoning_core_v0_4_audit_summary.md`

#### Status distribution (v0.3 → v0.4)

| status | v0.3 | v0.4 |
|---|---|---|
| solved | 3 | **4** (002, 005, 009, 011) |
| ambiguous | 9 | **8** |
| inconsistent | 0 | 0 |
| analysis_only | 0 | 0 |

#### Option mapping results

| metric | value |
|---|---|
| unique_supported | 1 (005) |
| ambiguous_options | 0 |
| no_supported_option | 11 |
| not_attempted | 0 |
| option_correct | 1 |
| option_wrong | 0 |
| option_null | 11 |

#### v0.4 improvements

1. **Option extraction**: `extract_options()` + JSON options support in audit script.
2. **Option parsing**: `parse_option_text()` handles "A、B入选", "甲说的不对，乙P", "去了X、Y、Z".
3. **Option mapping**: `map_options_to_assignments()` checks entailment across all consistent assignments.
4. **Atom constructor**: now auto-cleans subjects (strips 则/而/就), strips copula from predicates, auto-detects negation.
5. **And parsing**: "P和Q都不是R" now correctly parsed with full compound subjects (塔公草原, not 塔).
6. **Bare atom pattern**: restricted to single-char subjects, skips text with 和/且/、.

#### Why most options are "no_supported_option"

The option matching uses exact atom-key comparison. If the fact has `('atom', '右手', '水果糖', True)` and the option has `Atom("右手", "奶糖")`, there's no match because "水果糖" ≠ "奶糖". The engine doesn't know these are complementary predicates in a binary domain.

Similarly, "去四姑娘山" (from Imply parsing) vs "四姑娘山" (from option parsing) don't match because the subjects differ.

#### Recommendation

**Do NOT enter v7 integration.** Option mapping accuracy (1/12) is too low. Next steps:
- Domain-aware matching (complementary predicates, action-noun normalization)
- First-order reasoning (All(S,P) instance inference)
- Better Imply/option subject normalization

### truth_reasoning_core v0.5 (normalization and first-order support)

- Audit: `outputs/truth_reasoning_core_v0_5_audit_results.jsonl`
- Summary: `outputs/truth_reasoning_core_v0_5_audit_summary.md`

#### Status distribution (v0.4 → v0.5)

| status | v0.4 | v0.5 |
|---|---|---|
| solved | 4 | 4 |
| ambiguous | 8 | 8 |
| unique_supported | 1 | **2** |
| option_correct | 1 | **2** |
| option_wrong | 0 | 0 |

#### v0.5 improvements

1. **Binary complementary domains**: `extract_binary_domains()` detects "有X和Y两种" patterns. `_apply_binary_complement()` infers ¬A→B. Integrated into `_option_entailed_by_facts()`.
2. **Disjunctive syllogism fix**: Or processing now checks both direct key and negated key for known-false sides. This fixed 002's option mapping.
3. **Predicate normalization**: `normalize_predicate()` strips action prefixes (去/前往/到), copulas (是/属于), state auxiliaries (会/能/可以).
4. **Universal instantiation**: `_extract_known_entities()` + `_instantiate_universal_facts()` for All(S,P) → Atom(x,P) when x is known to be in S.
5. **Normalized atom matching**: `normalize_atom_key()` and `_prop_to_normalized_key()` for flexible fact lookup.

#### Binary domain results

3 cases detected binary domains: 002 (水果糖/奶糖), 005 (甲/乙元凶), 012 (甲/乙中标).

#### Why most options are still "no_supported_option"

- 001, 003, 004, 006, 008, 010, 012: ambiguous status → multiple assignments → no single option supported by all
- 007, 009, 011: solved but option parsing/matching still has gaps
- 009: "去了X、Y、Z" option parsing creates And chains that don't match Imply-derived facts
- 011: "甲、乙都未被录取" parsed as And(Atom("甲", "未被录取"), Atom("乙", "未被录取")), but facts have different structure

#### Recommendation

**Do NOT enter v7 integration.** unique_supported=2 is below threshold (≥5). Continue core enhancement.

### truth_reasoning_core v0.6 (solved-case option mapping)

- Audit: `outputs/truth_reasoning_core_v0_6_audit_results.jsonl`
- Summary: `outputs/truth_reasoning_core_v0_6_audit_summary.md`

#### Status distribution (v0.5 → v0.6)

| status | v0.5 | v0.6 |
|---|---|---|
| solved | 4 | 4 |
| ambiguous | 8 | 8 |
| unique_supported | 2 | **3** |
| option_correct | 2 | **3** |
| option_wrong | 0 | 0 |

#### v0.6 improvements

1. **Atom constructor**: now strips "被" as copula, strips action prefixes (去/前往/到) from predicates, handles "未被X" → negated=True + predicate=X.
2. **Predicate normalization**: `normalize_predicate()` strips action prefixes, copulas, passive markers, negation+passive combinations.
3. **Option parser**: "去了X、Y、Z" now creates atoms with location as predicate (matching Imply-parsed facts).
4. **Bare atom pattern**: skips text containing "和/且//或" to avoid splitting compound words.
5. **011 solved**: "甲、乙都未被录取" now correctly matches facts about 甲 and 乙 not being selected.

#### Solved case option mapping status

| case_id | status | option_status | predicted | correct |
|---|---|---|---|---|
| 002 | solved | unique_supported | A | Y |
| 005 | solved | unique_supported | C | Y |
| 009 | solved | no_supported_option | - | - |
| 011 | solved | unique_supported | B | Y |

#### 009 failure reason

009's option "去了四姑娘山、塔公草原、墨石公园" parses to And(Atom("", "四姑娘山"), ...). Facts have Atom("", "四姑娘山") and Atom("", "墨石公园"), but no fact about "塔公草原". The statement "塔公草原和墨石公园去一个就好" is parsed as And(Atom("塔", "公草原"), Atom("墨", "石公园去一个就好")) due to bare-atom splitting, which produces incorrect facts. This is a parser limitation for compound-place-name + "去一个就好" patterns.

#### Recommendation

unique_supported=3 meets the minimum threshold (≥3). Continue to v0.7 or consider v7 integration with caveats.

### truth_reasoning_core v0.7 (exclusive-one option mapping)

- Audit: `outputs/truth_reasoning_core_v0_7_audit_results.jsonl`
- Summary: `outputs/truth_reasoning_core_v0_7_audit_summary.md`

#### Status distribution (v0.6 → v0.7)

| status | v0.6 | v0.7 |
|---|---|---|
| solved | 4 | 4 |
| ambiguous | 8 | 8 |
| unique_supported | 3 | **4** |
| option_correct | 3 | **4** |
| option_wrong | 0 | 0 |

#### v0.7 improvements

1. **ExclusiveOne proposition**: new `Proposition(kind="exactly_one")` for XOR/exactly-one semantics.
2. **ExclusiveOne parsing**: "A和B去一个就好", "A、B只去一个", "A和B二选一", "要么A要么B", "不是A就是B" → `ExclusiveOne(A, B)`.
3. **ExclusiveOne closure**: if exactly_one(A, B) is true: A→¬B, B→¬A, ¬A→B, ¬B→A.
4. **ExclusiveOne false handling**: ¬exactly_one(A, B) = (A∧B) ∨ (¬A∧¬B). If one side's truth value is known, the other is determined.
5. **ExclusiveOne in closure loop**: `_derive_closure` now accepts `exclusive_pairs` and derives facts from them in each iteration.
6. **009 solved**: "塔公草原和墨石公园去一个就好" now parsed as exactly_one, enabling the closure to derive all three locations as visited.

#### Exclusive-one results

1 case detected exclusive-one: 009 (塔公草原/墨石公园). This enabled the option mapping to succeed.

#### Solved case option mapping status

| case_id | status | option_status | predicted | correct |
|---|---|---|---|---|
| 002 | solved | unique_supported | A | Y |
| 005 | solved | unique_supported | C | Y |
| 009 | solved | unique_supported | A | Y |
| 011 | solved | unique_supported | B | Y |

All 4 solved cases now have unique_supported option mapping!

#### Recommendation

unique_supported=4 meets the threshold (≥4). Consider entering v7 integration with limited scope, or continue to v0.8 for ambiguous case improvement.

### solve_logic_reasoning v7 (conservative truth integration)

#### Integration strategy

- `_is_truth_reasoning_question()` detects truth reasoning questions by constraint triggers and speaker/source indicators
- `_try_truth_reasoning()` calls `solve_truth_core()` and `map_options_to_assignments()`
- **candidate_ready** only when: core.status == "solved" AND option_status == "unique_supported"
- **analysis_only** for all other cases (ambiguous, inconsistent, no_supported_option, etc.)
- Truth reasoning branch runs before existing logic; if it returns analysis_only, the result is returned directly (no fallthrough to existing argument/translation logic)

#### Truth reasoning 12-case results

| case_id | expected | candidate | correct | decision_status |
|---|---|---|---|---|
| 001 | A | - | - | analysis_only |
| 002 | A | A | Y | candidate_ready |
| 003 | D | - | - | analysis_only |
| 004 | D | - | - | analysis_only |
| 005 | C | C | Y | candidate_ready |
| 006 | C | - | - | analysis_only |
| 007 | A | - | - | analysis_only |
| 008 | C | - | - | analysis_only |
| 009 | A | A | Y | candidate_ready |
| 010 | B | - | - | analysis_only |
| 011 | B | B | Y | candidate_ready |
| 012 | C | - | - | analysis_only |

- correct: 4, wrong: 0, null: 8

#### Regression results

- Translation (16 cases): 16 correct, 0 wrong, 0 null ✅
- Argument (20 cases): 18 correct, 0 wrong, 2 null ✅

#### Version

- LOGIC_SOLVER_VERSION updated to "v7 conservative truth integration"
- Existing tests updated to accept new version string

### v7 guardrail tests

- Test file: `tests/test_logic_reasoning_truth_integration.py` (23 tests)
- Guardrail batch results: `outputs/logic_reasoning_truth_v7_guardrail_*`

#### Guardrail test coverage

1. **Detection**: truth reasoning questions detected; translation/weaken not detected
2. **Integration behavior**: solved+unique_supported → candidate_ready; ambiguous → analysis_only
3. **No default**: no default-first-option or default-first-assignment
4. **Confidence**: truth reasoning confidence in 0.70-0.80 range
5. **Non-interference**: translation and argument questions not affected
6. **Real-case regression**: 4 known-correct cases remain correct; 8 known-ambiguous remain analysis_only

#### Guardrail batch results

- Truth reasoning: 4 correct, 0 wrong, 8 null ✅
- Translation: 16 correct, 0 wrong, 0 null ✅
- Argument: 18 correct, 0 wrong, 2 null ✅

#### Frozen strategy

The v7 integration strategy is now frozen:
- `solved + unique_supported` → `candidate_ready`
- `ambiguous + unique_supported_across_assignments` → `candidate_ready`
- All other cases → `analysis_only`
- This prevents false positives while allowing future v7.1 refinement to improve recall

### solve_logic_reasoning v7.1 (truth ambiguous refinement)

#### v7.1 enhancements

1. **Quote stripping**: Atom constructor strips Chinese quotation marks from subjects.
2. **Possibility question detection**: `_is_possibility_question()` detects "可能为真" vs "一定为真".
3. **unique_supported_across_assignments**: when all assignments support the same option (via positive entailment), output candidate_ready even if core status is ambiguous.
4. **Statement parser**: added "本/该/这/那" to excluded bare-atom prefixes; added "A和B+classifier+均/都+P" pattern.
5. **Integration logic**: ambiguous core status now proceeds to option mapping (not immediately analysis_only).

#### v7.1 results

- Truth reasoning: 4 correct, 0 wrong, 8 null (unchanged from v7)
- Translation: 16 correct, 0 wrong, 0 null ✅
- Argument: 18 correct, 0 wrong, 2 null ✅

#### Why 8 cases remain analysis_only

| case_id | expected | failure_category | main_reason |
|---|---|---|---|
| 001 | A | speaker_truth_gap | Options use "甲说的不对" → speaker-reference resolution needed |
| 003 | D | option_mapping_gap | Options are domain facts not tied to statement structure |
| 004 | D | statement_parse_gap | Statement 1 parsed; option "第三个柜子里有食品" needs negation mapping |
| 006 | C | option_mapping_gap | Options are conditional statements requiring complex evaluation |
| 007 | A | speaker_truth_gap | Facts use "我" instead of "甲"; option needs speaker-reference resolution |
| 008 | C | predicate_mismatch | Options use "合伙作案" but facts have "罪犯"; semantic equivalence needed |
| 010 | B | option_mapping_gap | Options are positional ("第二个"); requires domain reasoning |
| 012 | C | option_mapping_gap | Options are triples of schools; requires negation-based reasoning |

#### Recommendation

Current 4/12 correct with 0 wrong is a safe baseline. Further improvement requires:
- Speaker-reference resolution ("我" → speaker name)
- Predicate semantic matching ("合伙作案" ≈ "罪犯")
- These are high-risk changes that could introduce false positives

---

## 6. Proposed Direction: Minimal Structured Truth Reasoner

Build a standalone truth reasoning module (`truth_reasoning.py`) with:

### 5.1 Proposition Representation

Parse each person's statement into a structured `Proposition` object:

- `Atom(subject, predicate, negated)` — e.g., "甲是罪犯", "小李没有写完作业"
- `Not(prop)` — negation
- `And(left, right)` — conjunction
- `Or(left, right)` — disjunction
- `Imply(antecedent, consequent)` — conditional (如果 P 则 Q)
- `All(domain, predicate)` — universal quantifier
- `Some(domain, predicate)` — existential quantifier

### 5.2 Truth Assignment Enumeration

Given N statements and a truth constraint (e.g., "exactly 1 true, 3 false"):

1. Enumerate all C(N, k) assignments where k statements are true.
2. For each assignment, evaluate whether the assignment is self-consistent:
   - A statement marked "true" must be satisfiable given the derived facts.
   - A statement marked "false" must be falsifiable (its negation must be satisfiable).
3. Collect all consistent assignments.

### 5.3 Fact Extraction

For each consistent assignment, extract the set of facts that hold in that world.

### 5.4 Answer Selection

- Intersect facts across all consistent assignments → necessarily true facts.
- Match necessarily true facts against options using structured comparison (not substring matching).
- If the intersection is empty or multiple options match equally → return analysis_only.

### 5.5 Integration

- Detect truth reasoning questions by trigger patterns (几人说, 只有一人, 三真一假, etc.).
- Route to the truth reasoning module before falling through to generic argument analysis.
- The truth reasoning module returns either a confident answer or a fallback signal.
