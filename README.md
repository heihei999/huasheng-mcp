<div align="center">

# 🥜 花生十三 · 行测解题 MCP

**基于花生十三方法论的行测智能解题辅助工具**

为 Claude Code、Codex 等支持 MCP 协议的 AI 助手提供结构化行测解题能力

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/许可证-MIT-green)](LICENSE)
[![MCP](https://img.shields.io/badge/协议-MCP%201.0-purple?logo=modelcontextprotocol)](https://modelcontextprotocol.io/)
[![测试](https://img.shields.io/badge/测试-592%20通过-brightgreen?logo=pytest&logoColor=white)](#测试)
[![版本](https://img.shields.io/badge/最新版本-v0.5.1-orange)](https://github.com/heihei999/huasheng-mcp/releases)

</div>

---

## 📌 这是什么？

这不是一个"自动答题器"。它是一套 **解题方法论脚手架**，帮你告诉 AI：

> "这道题应该用什么方法、按什么步骤分析、注意哪些陷阱"

最终的读题、推理和选答案，仍然由接入的大模型完成。

**一句话总结**：AI 负责思考，它负责教 AI 怎么思考。

---

## ✨ 核心能力

<table>
<tr>
<td width="50%">

### 🧭 智能路由
自动识别题目所属模块（资料分析、逻辑判断、图形推理等），返回置信度和推荐分析路径

</td>
<td width="50%">

### 📚 方法检索
从 **292 张结构化方法卡片** 中精准匹配解题方法，覆盖行测全部核心题型

</td>
</tr>
<tr>
<td>

### 🏗️ 脚手架引导
6 大模块的逐步分析脚手架，像老师一样带着你拆解每一道题

</td>
<td>

### 🔒 安全门控
信息不足时自动降级为分析模式，**绝不强行作答**，杜绝胡编乱造

</td>
</tr>
</table>

---

## 🚀 三步开始使用

### 方案零：一句话让 AI 自己装（推荐）

直接在 **Claude Code** 或 **Codex** 对话中发送：

```
请帮我安装并配置花生十三行测解题 MCP：https://github.com/heihei999/huasheng-mcp
```

AI 会自动完成克隆、安装和配置，无需任何手动操作。

### 方案一：手动安装

```bash
git clone https://github.com/heihei999/huasheng-mcp.git
cd huasheng-mcp
pip install -e .
```

### 方案二：接入 Claude Code

```bash
claude mcp add-json huasheng-mcp '{"type":"stdio","command":"python","args":["-m","xingce_solver.mcp_server"]}' --scope user
```

---

## 🛠️ 15 个 MCP 工具一览

<div align="center">

| 类别 | 工具名 | 功能说明 |
|:---:|--------|----------|
| 🔀 路由 | `route_xingce_question` | 题型智能路由 |
| 🔀 路由 | `compose_xingce_analysis_prompt` | 组合分析提示词 |
| 🔀 路由 | `compose_xingce_answer_prompt` | 保守型答题提示词 |
| 📖 知识 | `get_method_card` | 获取单张方法卡 |
| 📖 知识 | `search_methods` | 关键词搜索方法卡 |
| 📖 知识 | `classify_question` | 轻量关键词分类 |
| 📖 知识 | `get_source_reference` | 方法来源溯源 |
| 🧮 求解 | `solve_data_analysis` | 资料分析结构化求解 |
| 🧮 求解 | `solve_logic_reasoning` | 逻辑判断结构化求解 |
| 🏗️ 引导 | `get_graphic_reasoning_scaffold` | 图形推理方法论 |
| 🏗️ 引导 | `get_definition_judgement_scaffold` | 定义判断方法论 |
| 🏗️ 引导 | `get_analogy_reasoning_scaffold` | 类比推理方法论 |
| 🏗️ 引导 | `get_logic_analysis_scaffold` | 分析推理方法论 |
| 🏗️ 引导 | `get_quantity_relation_scaffold` | 数量关系方法论 |
| 🏗️ 引导 | `get_verbal_reasoning_scaffold` | 言语理解方法论 |

</div>

---

## 🧠 工作原理

```
┌─────────────┐     ┌──────────────────────────┐     ┌─────────────┐
│  用户输入题目  │ ──▶ │  花生十三 MCP Server       │ ──▶ │  AI 大模型    │
│  （含图片/文字）│     │  路由 → 检索 → 脚手架组合    │     │  分析 → 作答   │
└─────────────┘     └──────────────────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │  知识库       │
                    │  292张方法卡  │
                    │  路由规则集   │
                    └─────────────┘
```

**核心约束**：MCP 工具永远不直接输出答案，只生成引导 prompt。答案由 AI 严格遵循约束后输出。

---

## 🔒 安全机制

<div align="center">

| 级别 | 机制 | 说明 |
|:---:|------|------|
| 🚫 硬门控 | 缺少图片/视觉描述 | 图形推理直接禁止作答 |
| 🚫 硬门控 | 缺少表格/材料上下文 | 资料分析直接禁止作答 |
| 🚫 硬门控 | 路由不确定 | 自动降级为分析模式 |
| ⚠️ 提示词约束 | 不猜测、不默认选A | 13 条核心行为约束 |
| ⚠️ 提示词约束 | 证据不足不作答 | 引导 AI 诚实输出 |

</div>

---

## 📊 项目结构

```
花生十三-mcp/
├── src/xingce_solver/
│   ├── mcp_server.py            # MCP 服务核心
│   ├── router.py                # 基于规则的题型路由
│   ├── kb.py                    # 知识库加载与检索
│   ├── cli.py                   # 命令行接口
│   ├── solvers/                 # 求解器（资料分析/逻辑判断）
│   └── scaffolds/               # 6 大模块方法论脚手架
├── knowledge_base/
│   ├── all_cards.jsonl          # 292 张方法卡片
│   └── global_router_rules.yaml # 路由规则
└── tests/                       # 自动化测试
```

---

## ✅ 测试

```bash
# 运行全部测试
python -m pytest

# 快速验证安装
python smoke_test_core.py
```

---

## 📋 路由验证

- 三年国考真题（2022-2024 行政执法卷）：**330 题全部路由正确**
- 安全门控泄漏检测：**0/330**（无答案/选项/预测泄露）
- 详细验证报告：`docs/v0_5_1_three_year_practical_validation.md`

---

## ⚠️ 已知限制

- 不做 OCR 或图片识别，图片由 AI 客户端先转写为文字描述
- 不调用外部 LLM 或 API
- 不重新解析 PDF 或重新生成知识卡片
- 知识库基于花生十三方法论，不含其他来源
- 逻辑判断暂不支持真假推理、分析推理、图形推理、定义判断、类比推理

---

## 📜 版本历史

| 版本 | 更新内容 |
|:---:|---------|
| **v0.5.1** | 边界 case 修复，三年真题 330/330 路由验证通过 |
| **v0.5.0** | 新增 `module_hint`/`section_context` 参数，支持中文模块名 |
| **v0.4.3** | 文本排列题和定义判断路由覆盖增强 |
| **v0.4.2** | 资料分析材料信号独立检测 |
| **v0.4.1** | 保守答题门控强化 |
| **v0.4.0** | 保守型答题 prompt 组合器 |

---

<div align="center">


MIT License · 2024-2026

</div>
