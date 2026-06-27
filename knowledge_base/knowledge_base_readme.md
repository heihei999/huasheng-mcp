# knowledge_base_readme.md

## 1. 知识库目标

本知识库是“花生十三行测方法论解题系统”的最终合并包，目标是把已经完成 source audit 的模块知识库，统一成可供 RAG、MCP、Skill、Codex、Claude Code、opencode 调用的结构化方法库。

本轮只做合并、字段标准化、索引生成和工程交接，不重新解析 PDF，不重新抽取资料。

## 2. 文件结构

```text
xingce_huasheng_final_kb/
├── all_cards.jsonl
├── global_router_rules.yaml
├── method_manifest.json
├── module_map.yaml
├── synonyms.yaml
├── schema_spec.md
├── knowledge_base_readme.md
├── codex_handoff_spec.md
├── claude_skill_draft.md
├── agents_md_draft.md
├── validation_report.md
├── source_audit_summary.md
└── module_originals/
```

`module_originals/` 保留七个模块 zip 中的原始 audited 文件，方便回查。

## 3. 各文件用途

| 文件 | 用途 |
|---|---|
| `all_cards.jsonl` | 全库方法卡片，一行一张卡片。 |
| `global_router_rules.yaml` | 全局题型路由规则。 |
| `method_manifest.json` | 方法清单，按模块统计卡片。 |
| `module_map.yaml` | 模块 → 题型 → 子题型 → method_id。 |
| `synonyms.yaml` | 检索同义词、触发词、题干关键词。 |
| `schema_spec.md` | 字段 schema 与读取规则。 |
| `codex_handoff_spec.md` | 交给 Codex 的工程实现说明。 |
| `claude_skill_draft.md` | Claude Code Skill 草稿。 |
| `agents_md_draft.md` | Codex / opencode 的 AGENTS.md 草稿。 |
| `validation_report.md` | 全库校验结果。 |
| `source_audit_summary.md` | 全库来源审计汇总。 |

## 4. 如何用于 RAG / MCP / Skill

推荐调用链：

1. 输入题目。
2. 先用 `global_router_rules.yaml` 和 `synonyms.yaml` 识别模块与题型。
3. 读取候选 `method_id`。
4. 用 `all_cards.jsonl` 获取方法卡片。
5. 按卡片 `required_inputs` 抽取题干要素。
6. 按 `steps`、`reasoning_policy`、`calculation_policy` 执行。
7. 用 `output_constraints` 控制输出。
8. 用 `source_file/source_page` 返回可追溯来源。

## 5. 如何更新某个模块

1. 先在单模块层面生成新的 `*_knowledge_base_audited.zip`。
2. 替换 `module_originals` 来源 zip。
3. 重新执行全库合并脚本。
4. 查看 `validation_report.md`。
5. 确认 id 不冲突、路由引用有效后发布新包。

## 6. 如何处理 need_review 卡片

`need_review=true` 卡片保留，但自动解题时应降权。

建议策略：

- 普通检索：可展示。
- 自动解题：不作为首选。
- 需要调用：提示用户此卡片需要复核。
- 人工复核后：更新模块 audited 包，再合并。

## 7. 如何追溯来源 PDF

每张卡片包含：

- `source_file`
- `source_page`

其中 `source_page` 是 PDF 物理页码。工具可通过 `get_source_reference(method_id)` 返回该信息。

## 8. 如何给 Codex 使用

直接把整个 `xingce_huasheng_final_kb/` 目录交给 Codex，并让它优先阅读：

1. `schema_spec.md`
2. `codex_handoff_spec.md`
3. `validation_report.md`
4. `all_cards.jsonl`
5. `global_router_rules.yaml`

Codex 不需要也不应该重新解析 PDF。
