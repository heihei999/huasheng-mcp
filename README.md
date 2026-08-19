# 花生十三 · 行测解题 MCP 助手

📚 基于花生十三行测知识库，**442 张方法卡片**覆盖资料分析、数量关系、判断推理、言语理解四大模块。搭配 AI 助手（Claude Desktop 等），随时随地智能解题。

## 🚀 一分钟快速上手

### 方法一：让 Agent 帮你安装（最省事）

如果你是 **Claude Code**、**Codex CLI**、**Cursor**、**Windsurf** 等 AI 编程工具的用户，直接把下面这句话发给它：

> **「帮我安装一下 https://github.com/heihei999/huasheng-mcp 这个 MCP 服务器」**

Agent 会自动完成下载、安装、配置全部步骤，你什么都不用管。

### 方法二：自己动手安装

#### 第 1 步：安装

```powershell
pip install xingce-solver[sse]
```

> 如果没装 Python，先去 https://www.python.org/downloads/ 下载安装，勾选"Add Python to PATH"。

#### 第 2 步：启动服务

```powershell
xingce-solver-mcp-sse
```

看到 `Uvicorn running on http://0.0.0.0:8000` 即启动成功 👌

#### 第 3 步：连接 AI 助手

**Claude Desktop** 用户，在配置文件（`%APPDATA%\Claude\claude_desktop_config.json`）中加入：

```json
{
  "mcpServers": {
    "行测解题": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

保存后**重启 Claude Desktop**，对话框中就能直接调用行测解题工具了！

> **ChatGPT / 其他 AI 用户**：启动服务后，在支持 MCP SSE 的客户端中填入地址 `http://localhost:8000/sse` 即可。

---

## 📖 知识库总览

知识库共 **442 张方法卡片**，覆盖行测四大模块：

| 模块 | 卡片数 | 说明 |
|---|---|---|
| 📊 **资料分析** | 52 张 | 增长率、比重、倍数、平均数等 |
| 🔢 **数量关系** | 118 张 | 工程问题、行程问题、排列组合等 |
| 🧠 **判断推理** | 148 张 | 图形推理、逻辑判断、定义判断、类比推理 |
| 💬 **言语理解** | 95 张 | 主旨意图、语句表达、逻辑填空 |
| 🆕 **言语理解（新）** | 18 张 | 语句排序、细节判断等 |
| 🆕 **图形推理（新）** | 10 张 | 图形规律专项 |
| **合计** | **442 张** | 覆盖全部核心题型 |

---

## 🛠️ 可用解题工具（共 15 个）

连接成功后，AI 助手会自动识别以下工具：

| 工具 | 干什么用 |
|---|---|
| `solve_data_analysis` | 📊 解资料分析题 |
| `solve_logic_reasoning` | 🧠 解逻辑判断题 |
| `classify_question` | 🔍 识别题目属于哪个模块 |
| `search_methods` | 🔎 搜索解题方法 |
| `get_method_card` | 📇 查看某方法的详细内容 |
| `get_source_reference` | 📋 查看方法的来源出处 |
| `route_xingce_question` | 🧭 判断题型并推荐解法 |
| `compose_xingce_analysis_prompt` | 📝 组合分析提示词 |
| `compose_xingce_answer_prompt` | ✅ 生成保守型答题提示词 |
| `get_graphic_reasoning_scaffold` | 🎨 图形推理方法框架 |
| `get_definition_judgement_scaffold` | 📌 定义判断方法框架 |
| `get_analogy_reasoning_scaffold` | 🔗 类比推理方法框架 |
| `get_logic_analysis_scaffold` | ⚖️ 分析推理方法框架 |
| `get_quantity_relation_scaffold` | 🔢 数量关系方法框架 |
| `get_verbal_reasoning_scaffold` | 💬 言语理解方法框架 |

---

## 🎯 在 AI 助手里的使用示例

所有支持 MCP SSE 的 AI 助手都能接入（Claude Desktop、ChatGPT、**Cherry Studio** 等）。其中 **Cherry Studio** 会把每次工具调用过程可视化展示出来，新手能直观看到 AI 是怎么一步步调用知识库解题的，特别适合刚接触 MCP 的朋友。

### 方式一：直接发文字题目

连接成功后，直接打字问：

> 「帮我解一道资料分析题：2020 年某产业收入为 132 亿元，同比增长 10%，问 2019 年收入约为多少？A.100 亿元 B.110 亿元 C.120 亿元 D.132 亿元」

AI 助手会自动调用工具，返回分析过程和答案。

### 方式二：发截图让 AI 自己读题（强烈推荐）

> 你从练习 App、PDF 或网课上截一道题 → 直接把截图发给 AI 助手 → AI 用"眼睛"看图识字 → 自动调用解题工具 → 秒出答案

**支持多模态的 AI 助手都能这样用**（Claude Desktop、ChatGPT 等）。你不用手打字，拍照截图就行，特别适合手机端或平板端刷题。

### 方式三：搜索解题方法

> 「搜索一下关于增长率比较的解题方法」

AI 助手会调用 `search_methods` 工具，从 442 张方法卡片中找到匹配的解题技巧。

### 方式四：让 Agent 批量刷题

如果你在用 Claude Code、Codex 等编程 Agent，可以给它一个路径让它批量处理：

> 「读取这个文件夹里的所有行测题图片，逐个调用解题工具，把答案汇总到一个表格里」

适合考前突击刷题。

---

## 📝 实战验证的解题 Prompt

作者实战刷题验证过的解题 SOP，让 AI 严格按「路由 → 取脚手架 → 按规则解答」的链条调用 MCP 工具，避免 AI 跳过知识库直接凭感觉作答。把下面整段复制发给 AI 助手即可：

```text
你是一个专业的公考行测名师。每次解答行测题目时，你必须严格遵循以下 SOP（标准操作流程） 链条来使用你的 MCP 知识库，绝不能跳过或卡死在任何一步：
【强制解题步骤】
第一步：提取与路由
当你收到用户的题目（或图片）时，你必须首先调用路由工具 route_xingce_question。
question_text 参数：仅填入你提取出来的纯净"行测题目原文"（如果有图片，必须提取图片中的完整题目文字，绝不能只填用户的闲聊！）。
module_hint 参数：如果用户指定了方法（如"十字交叉法"），必须填入此处；若无指定则留空。
第二步：获取脚手架
路由工具会返回一个结果，其中包含 recommended_tool（例如 get_quantity_relation_scaffold）。看清楚推荐的工具名后，你必须立刻去调用那个推荐的工具，从而获取详细的解题规则和公式！
注意：初次解答时禁止重复调用第一步的路由工具。但如果用户后续反驳、补充条件或提出新方法，允许你再次调用路由工具重新查阅资料！
第三步：按规则解答
拿到脚手架规则后，严格按照知识库给出的模板和步骤，结合用户指定的思路，为用户深度解答。
【异常兜底】
如果在第一步返回 "unknown" 或无匹配，或者在任何一步发生错误，只需尝试 1 次。如果依然失败，请立刻彻底放弃调用工具，直接动用你的内部推理能力为用户解答！
```

---

## ⚙️ 高级设置

### 修改端口

默认端口是 8000，如果被占用可以改：

```powershell
set MCP_PORT=8080
xingce-solver-mcp-sse
```

### 局域网共享

想让同一局域网的其他设备也能用：

```powershell
set MCP_HOST=0.0.0.0
xingce-solver-mcp-sse
```

然后其他设备连接 `http://你的IP地址:8000/sse`。

---

## 🧪 测试状态

✅ **661 项测试通过，35 项跳过**，知识库 442 张方法卡片全部覆盖。

---

## 📋 版本历史

| 版本 | 亮点 |
|---|---|
| **v0.7.0** | 知识库 292→442 张卡片，新增 SSE 服务器，新手友好 |
| **v0.6.0** | 图形推理框架，8 种反模式 |
| **v0.5.1** | 模块上下文边界加固，330 道真题验证 |
| **v0.5.0** | 模块上下文手动覆盖 |
| **v0.4.3** | 保守路由加固，60 题压力测试 57/60 |
| **v0.4.2** | 资料材料信号识别 |
| **v0.4.1** | 答案门控安全加固 |
| **v0.4.0** | 首个 MCP 集成版本 |

---

> 💡 **有问题？** 在 [GitHub Issues](https://github.com/heihei999/huasheng-mcp/issues) 提出
