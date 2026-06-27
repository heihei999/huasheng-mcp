# Judgement Reasoning Scaffolds v0.1 Design

## 1. Background

定义判断、类比推理、分析推理三个模块在纯规则 solver 路线下遇到了明显瓶颈：

- **定义判断**：定义句的语义理解、必要条件与附加描述的区分、选是/选非极性反转，均难以用纯规则覆盖。
- **类比推理**：词项间的关系类型识别、关系方向判断、关系强弱比较，高度依赖语义理解。
- **分析推理**：题型多样（排序、分组、匹配、真假话、半真半假等），约束条件的结构化和条件传播需要灵活的推理能力。

这三个模块不适合继续硬堆 pure-rule solver，但非常适合转为 **method scaffold / LLM guidance** 模式：

- 大模型负责语义理解和灵活推理；
- scaffold 负责提供方法论约束、思考顺序和检查清单；
- 逐选项验证 + 不确定性约束保证输出质量。

## 2. Scope

本阶段新增：

- `definition_judgement_scaffold.py` — 定义判断方法脚手架
- `analogy_reasoning_scaffold.py` — 类比推理方法脚手架
- `logic_analysis_scaffold.py` — 分析推理方法脚手架
- `tests/test_judgement_reasoning_scaffolds.py` — 测试文件
- `docs/judgement_reasoning_scaffolds_v0_1_design.md` — 本设计文档

本阶段不接入：

- CLI
- MCP
- `solve_logic_reasoning`

## 3. Design principle

核心设计原则：

1. **大模型负责语义理解**：scaffold 不做语义判断，只提供结构化的方法论约束。
2. **scaffold 负责方法论约束**：每个模块提供固定的思考顺序（stage_order）、要素检查清单、选项验证步骤和不确定性触发条件。
3. **逐选项验证**：所有模块都要求逐选项检查，不能只看一个选项就决定。
4. **不唯一则 analysis_only**：当多个选项同时满足或不满足约束时，必须输出 analysis_only 而非强行选择。
5. **wrong = 0 优先于 correct 数量**：宁可不预测，也不能预测错误。

## 4. Definition judgement scaffold

### 4.1 思考顺序

```
问法识别 → 定义句定位 → 定义要素抽取 → 必要条件区分 → 选项逐项匹配 → 选是/选非校验 → 唯一性判断 → 不确定性约束
```

### 4.2 关键要素

- **问法极性**：先判断选是题还是选非题，选非题必须反向验证。
- **定义要素**：主体、客体、条件、方式、目的、结果、排除项、必要条件、附加描述等。
- **必要条件 vs 附加描述**：必要条件缺失时优先排除；附加描述不能当成必要条件。
- **选项逐项匹配**：逐选项检查是否满足每个必要条件。

### 4.3 不确定性约束

定义要素无法完整抽取、问法极性不明确、多个选项同时符合/不符合、必要条件与附加描述无法区分时，输出 analysis_only。

## 5. Analogy reasoning scaffold

### 5.1 思考顺序

```
题干形式识别 → 词性与结构检查 → 题干关系造句 → 关系类型识别 → 选项关系套入 → 横纵比较 → 最优关系判断 → 不确定性约束
```

### 5.2 关键要素

- **题干形式**：二词型、三词型、填空型、括号型、对应型。
- **关系类型**：近义、反义、种属、组成、功能、因果、工具-用途、职业-工具等 23 种。
- **关系验证**：用一句自然语言描述题干关系，同一句关系必须能套入选项。
- **横纵比较**：比较关系方向、词性一致性、语义层级、关系强弱。

### 5.3 不确定性约束

题干关系无法稳定造句、多个关系类型都能解释题干、多个选项关系同样成立、关系强弱无法区分时，输出 analysis_only。

## 6. Logic analysis scaffold

### 6.1 思考顺序

```
题型识别 → 对象集合抽取 → 属性集合抽取 → 约束条件抽取 → 结构框架建立 → 条件传播 → 选项代入验证 → 唯一性判断 → 不确定性约束
```

### 6.2 题型路由

| 题型 | 结构框架 |
|------|----------|
| 排序题 | 建排序轴 |
| 分组题 | 建分组框 |
| 匹配题 | 建对象-属性表 |
| 位置关系题 | 建位置槽 |
| 真假话题 | 建真假约束 |
| 半真半假题 | 拆分每句话的前半/后半 |
| 条件组合题 | 建条件列表并逐步传播 |
| 最大最小题 | 建边界条件和极值约束 |

### 6.3 约束条件

包括确定条件、否定条件、至少/至多/恰好、相邻/不相邻、在……之前/之后、同组/不同组、对应/不对应、条件推理（如果……那么……、只有……才……、除非……否则……）等。

### 6.4 不确定性约束

对象集合不完整、约束条件无法结构化、存在多个满足条件的 assignment、多个选项代入均不矛盾、自然语言条件存在歧义时，输出 analysis_only。

## 7. Boundary

本阶段确认：

- 不开发 solver
- 不修改已有 solver
- 不接入 CLI
- 不接入 MCP
- 不修改 `all_cards.jsonl`
- 不调用外部 LLM/API
- 不联网
- 不引入 OCR / OpenCV / PIL / ML 依赖

所有 scaffold 只使用 Python 标准库（`__future__.annotations`、`typing.Any`）。

## 8. Public functions

### definition_judgement_scaffold

| 函数 | 返回值 | 说明 |
|------|--------|------|
| `build_definition_judgement_scaffold()` | `dict` | 完整定义判断方法脚手架 |
| `get_definition_judgement_stage_order()` | `list[str]` | 思考阶段顺序 |
| `get_definition_judgement_element_checklists()` | `dict` | 定义要素检查清单 |
| `render_definition_judgement_prompt_template()` | `str` | 提示词模板 |

### analogy_reasoning_scaffold

| 函数 | 返回值 | 说明 |
|------|--------|------|
| `build_analogy_reasoning_scaffold()` | `dict` | 完整类比推理方法脚手架 |
| `get_analogy_reasoning_stage_order()` | `list[str]` | 思考阶段顺序 |
| `get_analogy_reasoning_relation_checklists()` | `dict` | 关系类型检查清单 |
| `render_analogy_reasoning_prompt_template()` | `str` | 提示词模板 |

### logic_analysis_scaffold

| 函数 | 返回值 | 说明 |
|------|--------|------|
| `build_logic_analysis_scaffold()` | `dict` | 完整分析推理方法脚手架 |
| `get_logic_analysis_stage_order()` | `list[str]` | 思考阶段顺序 |
| `get_logic_analysis_structure_checklists()` | `dict` | 结构模板和约束检查清单 |
| `render_logic_analysis_prompt_template()` | `str` | 提示词模板 |

## 9. Testing

新增 `tests/test_judgement_reasoning_scaffolds.py`，覆盖：

- 三个 scaffold 基础结构（返回 dict、module、version、mode）
- 顶层字段完整性
- stage_order 包含关键阶段
- 关键内容（要素、关系类型、题型等）
- prompt template 格式和关键节
- 禁止依赖检查（cv2、PIL、sklearn 等）
- 禁止 solver 行为（无 answer / selected_option / prediction 顶层字段）
- 不确定性策略一致性

## 10. Future work

未来可以单独做：

- MCP guidance tools preview integration（必须单独审批）
- 不能让 scaffold 直接输出答案
- 不能和 solver 自动解题混淆
- 可以为每个模块扩展更详细的 checklist 子项
- 可以根据实际使用反馈调整 stage_order 和 uncertainty_policy
