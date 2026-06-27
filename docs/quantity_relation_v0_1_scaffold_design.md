# Quantity Relation Scaffold v0.1 Design

## 1. Background

数量关系卡片审计已完成，共 65 张卡，覆盖 22 种题型。当前建议先做 quantity_relation_scaffold v0.1 isolated，再考虑 small solver core。

## 2. Scope

本阶段新增：

- `src/xingce_solver/scaffolds/quantity_relation_scaffold.py`
- `tests/test_quantity_relation_scaffold.py`
- `docs/quantity_relation_v0_1_scaffold_design.md`
- `outputs/quantity_relation_scaffold_v0_1_smoke.md`

本阶段不做：

- solver
- CLI
- MCP
- 真题包
- OCR/ML/外部 API

## 3. Design principle

- 大模型负责自然语言建模与计算
- scaffold 负责题型识别、单位约束、方法选择、选项验证和不确定性约束
- wrong=0 优先
- 不唯一 analysis_only

## 4. Stage order

题型识别 → 问法识别 → 已知量抽取 → 未知量设定 → 单位统一 → 方法选择 → 模型建立 → 计算/代入验证 → 量级检查 → 唯一性判断 → 不确定性约束

## 5. Problem type router

覆盖 23 种题型（含"其他"），每种包含 signals、modeling_focus、preferred_method、risk、analysis_only_when、feasibility。

A_solver_first: 工程、利润、鸡兔同笼、盈亏、日期、特征余数、植树、浓度、比赛、方阵、数列、牛吃草
B_scaffold_first_solver_later: 基础行程、容斥、数论、不定方程
C_scaffold_only: 排列组合、概率、最值、统筹、几何构造、年龄
D_defer: 抽屉原理

注意：这些只是 guidance，不表示 solver 已支持。

## 6. Method checklists

覆盖 12 种方法：代入排除、特值法、方程法、赋值法、枚举法、十字交叉法、比例法、图表辅助、公式法、构造极端、估算量级、分类讨论。

## 7. Uncertainty policy

题型无法稳定识别、问法目标不明确、已知量或单位无法完整抽取、存在多个建模方式且结果不同、多个选项均满足条件、计算结果不在选项中且模型不确定、题干存在歧义、涉及复杂排列组合/概率/几何构造且无法可靠建模时，必须 analysis_only。

## 8. Boundary

- no solver added
- no CLI/MCP integration
- no knowledge base modification
- no real-case package created
- no fabricated question
- no OCR/OpenCV/PIL/ML dependency
- no external LLM/API

## 9. Testing

新增测试覆盖：基础结构、顶层字段、stage_order、题型覆盖、方法覆盖、prompt template、uncertainty_policy、must_not_do、no answer fields、forbidden dependency check。

## 10. Future work

后续可单独审批：

- quantity_relation_solver_core v0.1 isolated
- future user-provided real-case audit
- guarded CLI/MCP integration
