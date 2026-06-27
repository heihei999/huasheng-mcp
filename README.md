# 花生十三-mcp 🥜

> 基于花生十三行测方法论的 MCP 解题辅助工具 — 为 Claude Code、Codex 等 LLM Agent 提供结构化的行测题型路由、292 张方法卡检索、解题脚手架和安全门控。

---

## ⚠️ 重要说明

**本 MCP 不是独立自动答题器。**

MCP Server 负责：题型路由 → 方法卡检索 → 解题脚手架 → 答题提示词约束 → 安全门控。最终的读图、读表、计算、推理和选答案由接入的大模型完成。

因此，实际答题正确率取决于两个方面：

1. MCP 的路由 / 脚手架 / 安全门控约束
2. **接入大模型的能力和指令遵循程度**

> 💡 建议使用中文理解、多模态视觉、表格阅读和推理能力较强的大模型（如 Claude Sonnet/Opus、GPT-4o 等）。

---

## ✨ 功能亮点

- **🔀 题型路由**：自动识别题目所属模块（资料分析、逻辑判断、图形推理、定义判断、类比推理、数量关系、言语理解），返回置信度和推荐分析路径
- **📚 方法检索**：从 **292 张**结构化方法卡片中检索匹配的解题方法，覆盖行测全部核心题型
- **🧩 结构化求解**：资料分析和逻辑判断模块提供完整的解题草案
- **🏗️ Scaffold 引导**：6 个模块的方法论脚手架，指导逐步分析和推理
- **🛡️ 安全门控**：多层安全控制，信息不足时自动降级为分析模式，不强行作答

---

## 🚀 快速开始（3 步搞定）

### 第一步：安装

需要 **Python 3.10+** 和 **git**。

```bash
# 克隆项目
git clone https://github.com/heihei999/huasheng-mcp.git
cd huasheng-mcp

# 安装（会自动下载依赖）
pip install -e .
```

### 第二步：接入 AI 助手

> 以下三个方案**选一个即可**，不需要都装。

#### 方案零：让 AI 自己安装（最省事 🎯）

如果你已经在用 Claude Code 或 Codex，直接在会话中发一条消息：

> 请帮我安装这个项目的 MCP 服务：https://github.com/heihei999/huasheng-mcp

AI 会自动克隆仓库、安装依赖、配置 MCP，全程自动完成。

#### 方案一：Claude Code（推荐）

**一条命令搞定：**

```bash
claude mcp add huasheng-mcp --scope user -- python -m xingce_solver.mcp_server
```

**或手动配置 JSON：** 编辑 `~/.claude.json`，添加：

```json
{
  "mcpServers": {
    "huasheng-mcp": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "xingce_solver.mcp_server"]
    }
  }
}
```

> ⚠️ 如果 Python 不在系统 PATH 中，将 `"python"` 替换为完整路径（如 `"/usr/local/bin/python3"`）。

#### 方案二：Codex

**一条命令搞定：**

```bash
codex mcp add huasheng-mcp -- python -m xingce_solver.mcp_server
```

**或手动配置 TOML：** 编辑 `~/.codex/config.toml`，添加：

```toml
[mcp_servers.huasheng-mcp]
command = "python"
args = ["-m", "xingce_solver.mcp_server"]
```

### 第三步：验证

```bash
claude mcp list   # 确认 huasheng-mcp 旁边有 ✓ Connected
```

然后发送测试问题：

> 帮我路由这道题：资料分析，某市 2023 年 GDP 为 5.2 万亿元，同比增长 8.5%，其中第二产业增加值 2.1 万亿元，同比增长 6.3%。问第二产业增加值占 GDP 比重与上年相比如何变化？

如果能给出路由结果并开始分析，说明接入成功 ✅

---

## 🛠️ MCP 工具一览

共 **15 个** MCP 工具，按功能分为 4 类：

| 类别 | 工具名 | 说明 |
|:----:|--------|------|
| 🔀 路由 | `route_xingce_question` | 题型路由，支持 module_hint / section_context |
| 🔀 路由 | `compose_xingce_analysis_prompt` | 组合分析提示词 |
| 🔀 路由 | `compose_xingce_answer_prompt` | 保守型答题提示词 |
| 📚 知识 | `get_method_card` | 获取指定方法卡 |
| 📚 知识 | `search_methods` | 搜索方法卡 |
| 📚 知识 | `classify_question` | 轻量关键词路由 |
| 📚 知识 | `get_source_reference` | 来源溯源 |
| 🧩 求解 | `solve_data_analysis` | 资料分析结构化求解 |
| 🧩 求解 | `solve_logic_reasoning` | 逻辑判断结构化求解 |
| 🏗️ 引导 | `get_graphic_reasoning_scaffold` | 图形推理方法论 |
| 🏗️ 引导 | `get_definition_judgement_scaffold` | 定义判断方法论 |
| 🏗️ 引导 | `get_analogy_reasoning_scaffold` | 类比推理方法论 |
| 🏗️ 引导 | `get_logic_analysis_scaffold` | 分析推理方法论 |
| 🏗️ 引导 | `get_quantity_relation_scaffold` | 数量关系方法论 |
| 🏗️ 引导 | `get_verbal_reasoning_scaffold` | 言语理解方法论 |

> 📌 关键约束：MCP 工具**永远不直接输出答案**，只生成严格约束的 prompt。答案由 LLM 严格遵循约束后输出。

---

## 🏗️ 架构

```
┌─────────────┐     ┌──────────────────────────┐     ┌─────────────┐
│  用户题目    │────▶│      MCP Server          │────▶│  LLM 客户端  │
└─────────────┘     │  ┌────────────────────┐  │     │  (Claude /   │
                    │  │ 路由引擎 (YAML规则)  │  │     │   Codex)    │
                    │  └────────────────────┘  │     └──────┬──────┘
                    │  ┌────────────────────┐  │            │
                    │  │ 知识库 (292张方法卡) │  │     ┌──────▼──────┐
                    │  └────────────────────┘  │     │  结构化答案   │
                    │  ┌────────────────────┐  │     └─────────────┘
                    │  │ 安全门控 + Prompt   │  │
                    │  └────────────────────┘  │
                    └──────────────────────────┘
```

MCP Server 本身**不调用外部 LLM**，只生成严格约束的 prompt，由接入的 LLM Agent 执行解题。

---

## 🔒 安全机制

本 MCP 采用**硬门控 + 提示词约束**双重安全体系。

### 硬门控（代码层面）

以下检查由 MCP 工具返回值强制执行。触发时 `compose_xingce_answer_prompt` 返回 `answer_allowed = false`：

| 触发条件 | `answer_block_reason` |
|----------|----------------------|
| 图形推理缺少图片或视觉描述 | `missing_visual_content` |
| 资料分析缺少表格/材料上下文 | `missing_table_or_material` |
| 路由不确定且无语义覆盖 | `route_uncertain_without_semantic_override` |
| 显式禁用答题模式 | `answer_mode_disabled` |

### 提示词约束（Prompt 层面）

以下约束嵌入在生成的答题 prompt 中，由 LLM 客户端遵循：

- 按模块对应的解题脚手架进行分析
- 逐项核验选项
- 证据不足时不猜测，不默认选 A
- 无法唯一确定答案时返回 `analysis_only`
- 题目内容与 `module_hint` / `section_context` 冲突时说明原因
- 在需要时使用提供的图片、表格或材料

> ⚠️ 提示词约束由 LLM 自主遵循，最终执行程度取决于接入模型。

---

## 📋 CLI 使用

```bash
# 搜索方法卡
huasheng-mcp search --query "比重 增长率"

# 查看方法卡详情
huasheng-mcp card --id da_share_change_004

# 资料分析求解
huasheng-mcp solve-data --text

# 逻辑判断求解
huasheng-mcp solve-logic --text
```

---

## 🧪 测试

```bash
# 冒烟测试
PYTHONPATH=src python smoke_test_core.py

# 完整测试（需安装 pytest）
python -m pytest
```

---

## 📁 项目结构

```
huasheng-mcp/
├── src/xingce_solver/
│   ├── mcp_server.py              # MCP Server 核心（路由 + prompt 组合 + tool 注册）
│   ├── router.py                  # 基于 YAML 规则的题型路由
│   ├── kb.py                      # 知识库加载与检索
│   ├── cli.py                     # CLI 接口
│   ├── solvers/
│   │   ├── data_analysis.py       # 资料分析求解器
│   │   ├── logic_reasoning.py     # 逻辑判断求解器
│   │   ├── truth_reasoning.py     # 真假推理
│   │   └── logic_analysis_reasoning.py  # 分析推理
│   └── scaffolds/                 # 6 个模块的方法论脚手架
│       ├── graphic_reasoning_scaffold.py
│       ├── definition_judgement_scaffold.py
│       ├── analogy_reasoning_scaffold.py
│       ├── logic_analysis_scaffold.py
│       ├── quantity_relation_scaffold.py
│       └── verbal_reasoning_scaffold.py
│
├── knowledge_base/
│   ├── all_cards.jsonl            # 292 张方法卡片
│   ├── global_router_rules.yaml   # 路由规则
│   ├── module_map.yaml            # 模块映射
│   └── synonyms.yaml              # 同义词表
│
└── smoke_test_core.py             # 冒烟测试脚本
```

---

## 📊 验证结果

| 指标 | 结果 |
|------|------|
| 三年真题路由验证 | **330 / 330** ✅ |
| 单元测试 | **592 tests passed** ✅ |

> 以上验证结果衡量的是 MCP 路由 / 门控 / 脚手架的行为正确性，而非独立的最终答案正确率。

---

## 📦 Release 下载说明

每个 Release 提供三种打包方式：

| 包名 | 大小 | 需要联网 | 适用场景 |
|------|------|:--------:|---------|
| `clean_runtime.zip` | ~160 KB | ✅ | 开发者 / 已有 Python 环境 |
| `online_runtime.zip` | ~140 KB | ✅ | 普通用户，有网络环境 |
| `offline_wheelhouse_runtime.zip` | ~14 MB | ❌ | 内网 / 无网络环境 |

### clean_runtime（纯源码包）

只包含项目源码、知识库和文档，不含任何依赖。

```powershell
cd xingce-solver_v0.5.1_clean_runtime
pip install -e .
.\smoke_test.ps1
.\install_claude_code_mcp.ps1   # 自动配置 Claude Code MCP
```

### online_runtime（在线安装包）

在 clean_runtime 基础上增加了一键安装脚本。

```powershell
cd xingce-solver_v0.5.1_online_runtime
.\install_dependencies.ps1      # 自动 pip install
.\smoke_test.ps1
.\install_claude_code_mcp.ps1   # 自动配置 Claude Code MCP
```

### offline_wheelhouse_runtime（离线安装包）

包含完整源码 + 31 个预编译 Python wheel 文件（Python 3.11 / Windows），无需联网。

```powershell
cd xingce-solver_v0.5.1_offline_wheelhouse_runtime
.\install_dependencies_offline.ps1   # 从本地 wheels 安装
.\smoke_test.ps1
.\install_claude_code_mcp.ps1        # 自动配置 Claude Code MCP
```

> 💡 **不确定选哪个？** 能上网就用 `online_runtime.zip`，不能上网就用 `offline_wheelhouse_runtime.zip`。Wheel 文件为 **Windows + Python 3.11** 版本。

---

## 📝 版本历史

| 版本 | 更新内容 |
|------|---------|
| **v0.5.1** | module_hint 边界 case 修复，三年真题 330/330 路由验证通过 |
| **v0.5.0** | 新增 module_hint / section_context 参数，支持中文模块名 |
| **v0.4.3** | 文本排列题和定义判断路由覆盖增强 |
| **v0.4.2** | 资料分析材料信号独立检测 |
| **v0.4.1** | 保守答题门控强化 |
| **v0.4.0** | 保守型答题 prompt 组合器 |

---

## 📄 License

MIT License