# 知识库说明

## 文件结构

```
knowledge_base/
├── all_cards.jsonl            # 全库方法卡片（292张），一行一张
├── global_router_rules.yaml   # 全局题型路由规则
├── method_manifest.json       # 方法清单，按模块统计
├── module_map.yaml            # 模块 → 题型 → 子题型 → method_id
├── synonyms.yaml              # 检索同义词、触发词
└── knowledge_base_readme.md   # 本文件
```

## 各文件用途

- **all_cards.jsonl**：核心数据文件，每行一个 JSON 方法卡片，包含 id、module、question_type、method_name、steps、formulas、pitfalls 等字段
- **global_router_rules.yaml**：路由规则定义，每条规则包含 stem_triggers、option_features、negative_triggers、priority_method_id
- **method_manifest.json**：按模块统计的方法清单
- **module_map.yaml**：模块到方法 ID 的映射关系
- **synonyms.yaml**：同义词表，用于知识检索时的词项扩展

## 卡片结构

每张卡片包含以下核心字段：

- `id`：唯一标识
- `module`：所属模块（如 data_analysis、logic_reasoning）
- `question_type`：题型
- `method_name`：方法名称
- `trigger_conditions`：触发条件
- `anti_conditions`：排除条件（什么时候不该用这张卡）
- `steps`：解题步骤
- `formulas`：公式
- `pitfalls`：常见陷阱
- `output_constraints`：输出约束
- `confidence`：置信度
- `source_file` / `source_page`：来源追溯

## 使用方式

知识库通过 `kb.py` 加载，支持加权文本检索。MCP Server 和 CLI 均通过 `KnowledgeBase` 类访问。
