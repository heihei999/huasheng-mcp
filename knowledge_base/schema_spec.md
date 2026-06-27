# schema_spec.md

## 1. all_cards.jsonl 总体说明

`all_cards.jsonl` 是全库统一方法卡片文件。每一行是一张 JSON 方法卡片，适用于 RAG、MCP Tool、Claude Code Skill、Codex / opencode 读取。

每张卡片必须包含以下字段：

| 字段 | 含义 |
|---|---|
| `id` | 方法卡片唯一 ID。全库唯一，不应随意修改。 |
| `module` | 标准化后的模块名称，例如 `资料分析`、`判断推理-逻辑判断`。 |
| `question_type` | 题型名称，例如 `增长率`、`削弱`、`标题填入`。 |
| `sub_type` | 子题型或方法分支。 |
| `method_name` | 人可读的方法名称。 |
| `aliases` | 明确存在的别名、旧名或同义方法名；无则为空数组。 |
| `tags` | 检索标签。 |
| `trigger_conditions` | 题干或材料中触发该方法的条件。 |
| `anti_conditions` | 不应调用该方法的条件。 |
| `required_inputs` | 解题前必须从题干、材料、选项或图形中抽取的信息。 |
| `reasoning_policy` | 推理型题目的调用策略；若原卡片只有 `calculation_policy`，已复制一份用于兼容。 |
| `calculation_policy` | 计算型题目的速算、估算、精算约束；非计算题可为空对象。 |
| `solver_priority` | 方法调用优先级对象，详见下节。 |
| `steps` | 结构化解题步骤。 |
| `formulas` | 公式列表；非公式型卡片允许 `formulas=[]`。 |
| `examples` | 例题方法抽象，不是全文复刻。 |
| `pitfalls` | 易错点。 |
| `forbidden` | 禁止行为，例如凭感觉选、跳过结构分析等。 |
| `output_constraints` | 输出约束数组，可包含字符串或结构化对象。 |
| `source_file` | 来源 PDF 文件名数组。 |
| `source_page` | 来源 PDF 物理页码数组或结构化页码对象。 |
| `confidence` | 抽取置信度，0 到 1。 |
| `need_review` | 是否需要人工复核。 |

部分模块保留额外字段，例如 `passage_structure`、`option_elimination`、`argument_structure`、`definition_elements`、`relation_type`、`ordering_clues`、`semantic_clues` 等。这些字段来自对应 audited 模块，用于增强解题器约束。

## 2. solver_priority

`solver_priority` 统一为对象：

```json
{
  "tier": "core_method",
  "rank": 1,
  "fallback_method_ids": []
}
```

含义：

- `tier`：方法层级。常见值包括 `precheck`、`core_method`、`verification`、`fallback` 等。
- `rank`：排序优先级。数值越小，越优先调用。
- `fallback_method_ids`：备用方法 ID。主方法无法判断或触发反条件时调用。

## 3. reasoning_policy 与 calculation_policy 的兼容逻辑

本库同时覆盖资料分析、数量关系等计算题，也覆盖言语、判断、图推等推理题。

标准化规则：

1. 原卡片只有 `calculation_policy` 时，复制一份到 `reasoning_policy`。
2. 原卡片只有 `reasoning_policy` 时，保留它，并将 `calculation_policy` 设为 `{}`。
3. 两者都有时均保留。

MCP 工具可按模块选择读取：

- 资料分析、数量关系：优先读取 `calculation_policy`。
- 言语理解、判断推理、图形推理：优先读取 `reasoning_policy`。
- 通用检索与路由：两者都可作为约束字段参与提示词构造。

## 4. need_review=true 的使用规则

`need_review=true` 表示该卡片存在来源识别、手写批注、公式、命名或规则边界上的不确定性。

使用规则：

1. 不删除该卡片。
2. 默认检索可返回，但应降权。
3. 自动解题不应优先调用该卡片。
4. 若必须调用，应在输出中提示“该方法卡片需要人工复核”。
5. 后续人工复核后，可在模块 audited zip 中修正，再重新合并全库。

## 5. source_page 说明

`source_page` 表示 PDF 物理页码，不是 PDF 内部印刷页码。

如果来源页码是复杂结构，应保留原结构。例如：

```json
[
  {"file":"花生判断笔记总结.pdf","pages":[20,21]}
]
```

MCP 的 `get_source_reference` 应返回 source_file 与 source_page，供用户回查。

## 6. 非公式型卡片

言语理解、定义判断、类比推理、图形推理等卡片可能没有数学公式，此时必须保留：

```json
"formulas": []
```

不得删除字段。

## 7. MCP 读取建议

MCP Server 应按以下顺序读取字段：

1. `global_router_rules.yaml` 初步识别模块与题型。
2. 用 `priority_method_id` 读取 `all_cards.jsonl` 中的卡片。
3. 校验 `trigger_conditions` 与 `anti_conditions`。
4. 读取 `required_inputs`，从题干或材料中抽取必要输入。
5. 按 `steps` 执行解题。
6. 按 `output_constraints` 约束答案格式。
7. 用 `source_file/source_page` 返回可溯源依据。
