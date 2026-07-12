# Xingce Solver Project Instructions

本项目目标是基于已经整理好的花生十三行测知识库，实现一个跨平台行测解题工具 xingce-solver。

## 核心要求

- 不要重新解析 PDF。
- 不要重新生成知识卡片。
- 不要修改 all_cards.jsonl 的内容。
- 不要把全部知识库一次性塞进提示词。
- 先实现工程基础能力，再实现 MCP 和具体解题器。
- 第一阶段只做读取、检索、分类和 CLI，不做复杂解题器。

## 当前知识库

最终知识库压缩包位于：

input/xingce_huasheng_final_kb_v1_3.zip

请先解压到：

knowledge_base/

解压后应包含：

- all_cards.jsonl
- global_router_rules.yaml
- method_manifest.json
- module_map.yaml
- synonyms.yaml
- schema_spec.md
- codex_handoff_spec.md
- validation_report.md

## 第一阶段目标

请实现：

1. 读取 knowledge_base/all_cards.jsonl。
2. 按 method_id 查询卡片。
3. 关键词检索方法卡片。
4. 基于 global_router_rules.yaml 做题型初步分类。
5. 查询 method_id 的来源信息。
6. 实现 CLI 命令：

```bash
xingce-solver search --query "比重 增长率"
xingce-solver card --id da_share_change_004
xingce-solver classify --question question.txt
xingce-solver source --method-id da_share_change_004