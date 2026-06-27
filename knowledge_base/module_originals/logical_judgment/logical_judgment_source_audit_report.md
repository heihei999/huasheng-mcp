# 判断推理-逻辑判断 source audit report

## 审计时间

2026-06-08 06:34:49

## 输入源文件

1. `【判断推理】逻辑基本知识.pdf`
2. `【判断推理】支持、前提假设、比例、解释说明.pdf`
3. `【判断推理】质疑类.pdf`
4. `花生判断笔记总结.pdf`

## 输出文件

- `logical_judgment_cards_audited.jsonl`
- `logical_judgment_methods_audited.md`
- `logical_judgment_router_rules_audited.yaml`
- `logical_judgment_uncertain_items_audited.md`
- `logical_judgment_source_audit_report.md`

## 卡片统计

- 总卡片数：42
- need_review=true：5
- 已补充工程字段：
  - `required_inputs`
  - `calculation_policy`
  - `solver_priority`
  - `output_constraints`
  - `argument_structure`
  - `strength_order`

## 来源页审计

| 来源文件 | 使用页码 | 用途 |
|---|---:|---|
| `【判断推理】逻辑基本知识.pdf` | 1 | 充分/必要条件、命题真假、逆否命题、五种命题、推理方式 |
| `【判断推理】支持、前提假设、比例、解释说明.pdf` | 1 | 支持类、前提假设、比例类、解释说明 |
| `【判断推理】质疑类.pdf` | 1 | 归因类、一般质疑、实验特殊、样本无效、严格逻辑削弱 |
| `花生判断笔记总结.pdf` | 3-19 | 归因论证、一般质疑、支持与前提、比例解释、推出类、分析类 |
| `花生判断笔记总结.pdf` | 20-32 | 范围外，未纳入本轮逻辑判断卡片 |

## 字段审计

### 1. `argument_structure`

所有卡片均已包含该字段。对非论证型卡片，如翻译推理、真假分析，也用“claim/evidence/link”描述该题型中的判断对象、题干依据和推理关系，便于后续统一调用。

### 2. `strength_order`

所有卡片均已包含该字段；加强/削弱/前提/解释类卡片提供了具体力度顺序。形式逻辑和分析推理类卡片若无力度比较需求，则保留为空数组。

### 3. `router_rules.yaml`

已区分以下路由：

- 加强
- 削弱
- 前提假设
- 解释说明
- 评价论证
- 结论推出
- 比例类
- 归因类削弱
- 对比实验
- 真假分析
- 范畴分析
- 日常分析

所有 `priority_method_id` 与 `backup_method_id` 均已校验存在于 `cards.jsonl`。

## 命名与合并审计

- 将“支持类”“前提假设”中重复出现的“断点搭桥”拆成两张卡：支持场景 `lj_support_bridge_001` 与前提场景 `lj_premise_bridge_001`，因为判定标准不同：支持看“更可信”，前提看“没它不行”。
- 将“比例类论证”归入削弱优先路径，同时保留其作为独立路由，避免后续 AI 只比较分子。
- 将“实验特殊”拆为初始状态、缺少对照组、样本无效、构成对比实验，便于后续精确调用。
- 将“评价论证”作为工程化路由卡处理，来源依据为论证结构拆解与主体话题一致原则，但标记 `need_review=true`。

## 删除/未纳入内容

- 未纳入定义判断、类比推理、图形推理内容。
- 未纳入原 PDF 中看不清的具体例题选项文本。
- 未新增 PDF 中没有依据的具体方法；对用户要求但原文未独立成章的“评价论证”，仅做论证结构层面的通用路由框架，并标记复核。

## 质量校验

- JSONL：逐行 JSON 可解析。
- 字段：所有卡片包含规定字段与新增工程字段。
- 路由：所有引用的 method_id 均存在。
- 溯源：每张卡片均包含 `source_file` 与 `source_page`。
