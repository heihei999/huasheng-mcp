# Verbal Reasoning Scaffold v0.1 Design

## 1. Background

言语理解卡片审计已完成，共 77 张卡，A_solver_first 为空。当前建议先做 verbal_reasoning_scaffold v0.1 isolated，不建议直接做强规则 solver。

## 2. Scope

本阶段新增：

- `src/xingce_solver/scaffolds/verbal_reasoning_scaffold.py`
- `tests/test_verbal_reasoning_scaffold.py`
- `docs/verbal_reasoning_v0_1_scaffold_design.md`
- `outputs/verbal_reasoning_scaffold_v0_1_smoke.md`
- `outputs/verbal_reasoning_scaffold_v0_1_output_audit.md`

本阶段不做：

- solver
- CLI
- MCP
- 真题包
- OCR/ML/外部 API

## 3. Design principle

- 大模型负责语义理解
- scaffold 负责题型识别、文段结构、逻辑关系、语境搭配、选项验证和不确定性约束
- wrong=0 优先
- 不唯一 analysis_only

## 4. Stage order

题型识别 → 问法识别 → 文段结构划分 → 主题句/重点句定位 → 逻辑关系识别 → 语境与词义检查 → 选项逐项验证 → 干扰项识别 → 衔接连贯检查 → 唯一性判断 → 不确定性约束

## 5. Question type router

覆盖 15 种题型（含"其他"），每种包含 signals、focus_points、preferred_method、risk、analysis_only_when、feasibility。

A_solver_first: 空
B_scaffold_first_solver_later: 语句排序、语句填入、标题填入、下文推断
C_scaffold_only: 主旨意图、中心理解、逻辑填空、成语辨析、实词辨析、干扰项识别
D_defer: 态度观点、细节理解

注意：这些只是 guidance，不表示 solver 已支持。

## 6. Method checklists

覆盖 15 种方法：主题句定位、关联词分析、转折关系、递进关系、因果关系、对策句、总分结构、干扰项排除、语境搭配、感情色彩、语义轻重、衔接连贯、排序线索、代词指代、主体词覆盖。

## 7. Uncertainty policy

题型无法稳定识别、问法目标不明确、文段结构无法稳定划分、主题句无法确认、多个选项均可解释、选项差异依赖强语感、逻辑填空语境不足、成语/实词语义无法可靠区分、语句排序存在多个连贯顺序、语句填入上下文指代不明时，必须 analysis_only。

## 8. Boundary

- no solver added
- no CLI/MCP integration
- no knowledge base modification
- no real-case package created
- no fabricated question
- no OCR/OpenCV/PIL/ML dependency
- no external LLM/API

## 9. Testing

新增测试覆盖：基础结构、顶层字段、stage_order、题型覆盖、方法覆盖、结构清单、prompt template、uncertainty_policy、must_not_do、no answer fields、forbidden dependency check。

## 10. Future work

后续可单独审批：

- verbal sub-scaffold split（如果需要）
- future user-provided real-case audit
- read-only MCP guidance integration
