# codex_handoff_spec.md

## 总目标

基于 `xingce_huasheng_final_kb/` 实现一个跨平台行测解题工具：

```text
xingce-solver
```

要求支持：

- CLI
- MCP Server
- Claude Code Skill 适配
- Codex AGENTS.md 适配
- opencode AGENTS.md 适配

## Codex 不要做的事情

1. 不要重新解析 PDF。
2. 不要重新生成知识卡片。
3. 不要修改 `all_cards.jsonl` 的内容。
4. 不要把全部知识库一次性塞进提示词。
5. 不要让大模型自由发挥做题。
6. 不要在资料分析题中直接暴力长除。
7. 不要在图形推理题中凭感觉猜规律。
8. 不要忽略 `need_review=true`。
9. 不要跳过 `anti_conditions`。
10. 不要只凭题干关键词定答案，必须读取方法卡片。

## 需要实现的核心工具

```text
classify_question
search_methods
get_method_card
solve_data_analysis
solve_graphic_reasoning
solve_logic_reasoning
solve_verbal
solve_quantitative
get_source_reference
```

## CLI 示例

```bash
xingce-solver search --query "比重 增长率"
xingce-solver classify --question question.txt
xingce-solver solve --question question.txt
xingce-solver source --method-id da_share_change_004
```

## 推荐数据加载策略

1. 启动时加载 `all_cards.jsonl`，建立 `method_id -> card` 索引。
2. 加载 `global_router_rules.yaml`，建立 route 索引。
3. 加载 `synonyms.yaml`，用于 query expansion。
4. 加载 `module_map.yaml`，用于模块/题型导航。
5. 加载 `method_manifest.json`，用于管理界面或调试。

## MCP 工具设计

### 1. classify_question

**description**：识别题目所属模块、题型、子题型和候选方法。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "question": {"type": "string"},
    "options": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["question"]
}
```

**output_schema**：

```json
{
  "type": "object",
  "properties": {
    "module": {"type": "string"},
    "question_type": {"type": "string"},
    "sub_type": {"type": "string"},
    "matched_route_ids": {"type": "array", "items": {"type": "string"}},
    "priority_method_ids": {"type": "array", "items": {"type": "string"}},
    "confidence": {"type": "number"},
    "need_review": {"type": "boolean"}
  }
}
```

**调用流程**：先用题干关键词和选项特征匹配 `global_router_rules.yaml`，再用 `synonyms.yaml` 扩展检索，最后返回候选方法。

### 2. search_methods

**description**：按关键词、模块、题型检索方法卡片。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "query": {"type": "string"},
    "module": {"type": "string"},
    "question_type": {"type": "string"},
    "top_k": {"type": "integer", "default": 5},
    "include_need_review": {"type": "boolean", "default": false}
  },
  "required": ["query"]
}
```

**output_schema**：

```json
{
  "type": "object",
  "properties": {
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "method_id": {"type": "string"},
          "method_name": {"type": "string"},
          "module": {"type": "string"},
          "question_type": {"type": "string"},
          "score": {"type": "number"},
          "need_review": {"type": "boolean"}
        }
      }
    }
  }
}
```

**调用流程**：用 BM25/关键词召回，再按 `solver_priority.rank`、`need_review`、模块匹配度重排。

### 3. get_method_card

**description**：根据 method_id 返回完整方法卡片。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "method_id": {"type": "string"}
  },
  "required": ["method_id"]
}
```

**output_schema**：返回 `all_cards.jsonl` 中对应 JSON card。

**调用流程**：直接查 `method_id -> card` 索引；不存在则返回错误和相近 ID。

### 4. solve_data_analysis

**description**：使用资料分析方法卡片解题，强调公式识别、选项差距和速算。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "question": {"type": "string"},
    "material": {"type": "string"},
    "options": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["question", "material", "options"]
}
```

**output_schema**：

```json
{
  "type": "object",
  "properties": {
    "answer": {"type": "string"},
    "method_id": {"type": "string"},
    "calculation_steps": {"type": "array", "items": {"type": "string"}},
    "estimation_policy": {"type": "string"},
    "source_reference": {"type": "object"}
  }
}
```

**调用流程**：分类 → 读取方法卡 → 抽取现期/基期/增长率/比重等输入 → 判断选项差距 → 使用截位/估算/公式 → 输出。

### 5. solve_graphic_reasoning

**description**：图形推理解题，必须按观察顺序验证，不凭感觉猜规律。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "question_description": {"type": "string"},
    "image_reference": {"type": "string"},
    "options": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["question_description"]
}
```

**output_schema**：

```json
{
  "type": "object",
  "properties": {
    "answer": {"type": "string"},
    "method_id": {"type": "string"},
    "observed_rule": {"type": "string"},
    "verification_steps": {"type": "array", "items": {"type": "string"}},
    "rejected_rules": {"type": "array", "items": {"type": "string"}}
  }
}
```

**调用流程**：优先调用 `gr_total_flow_001` → 判断组成相同/相似/不同 → 按位置、样式、属性、数量、空间重构逐层验证 → 选项验证。

### 6. solve_logic_reasoning

**description**：逻辑判断题，必须拆论点、论据、论证关系。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "question": {"type": "string"},
    "options": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["question", "options"]
}
```

**output_schema**：

```json
{
  "type": "object",
  "properties": {
    "answer": {"type": "string"},
    "method_id": {"type": "string"},
    "claim": {"type": "string"},
    "evidence": {"type": "string"},
    "argument_link": {"type": "string"},
    "strength_analysis": {"type": "array", "items": {"type": "string"}}
  }
}
```

**调用流程**：识别加强/削弱/假设/解释/评价/推出 → 拆论点论据 → 读取方法卡 strength_order → 比较选项力度。

### 7. solve_verbal

**description**：言语理解题，必须分析文段结构和选项错误类型。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "question": {"type": "string"},
    "passage": {"type": "string"},
    "options": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["question", "passage", "options"]
}
```

**output_schema**：

```json
{
  "type": "object",
  "properties": {
    "answer": {"type": "string"},
    "method_id": {"type": "string"},
    "passage_structure": {"type": "string"},
    "key_sentence": {"type": "string"},
    "option_elimination": {"type": "array", "items": {"type": "string"}}
  }
}
```

**调用流程**：识别主旨/意图/标题/下文/填入/排序/逻辑填空 → 读取方法卡 → 分析结构或语境提示 → 排除干扰项。

### 8. solve_quantitative

**description**：数量关系题，按题型方法卡进行模型化、赋值、方程或枚举。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "question": {"type": "string"},
    "options": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["question"]
}
```

**output_schema**：

```json
{
  "type": "object",
  "properties": {
    "answer": {"type": "string"},
    "method_id": {"type": "string"},
    "model": {"type": "string"},
    "steps": {"type": "array", "items": {"type": "string"}}
  }
}
```

**调用流程**：识别工程/行程/排列组合/最值/容斥等 → 调用卡片 → 使用公式、赋值、代入排除或方程。

### 9. get_source_reference

**description**：返回方法卡片的来源文件和 PDF 物理页码。

**input_schema**：

```json
{
  "type": "object",
  "properties": {
    "method_id": {"type": "string"}
  },
  "required": ["method_id"]
}
```

**output_schema**：

```json
{
  "type": "object",
  "properties": {
    "method_id": {"type": "string"},
    "source_file": {"type": "array"},
    "source_page": {"type": "array"},
    "need_review": {"type": "boolean"}
  }
}
```

**调用流程**：查 card，直接返回 `source_file/source_page`。

## 推荐开发顺序

1. 先实现读取 `all_cards.jsonl`。
2. 再实现 `method_id` 查询。
3. 再实现关键词/BM25 检索。
4. 再实现 `global_router_rules.yaml` 路由。
5. 再实现资料分析 `solve_data_analysis`。
6. 再实现其他模块的检索增强解题。
7. 最后封装 MCP Server。
