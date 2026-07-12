# 花生十三 · 行测解题 MCP 助手

📚 基于花生十三行测知识库，**442 张方法卡片**覆盖资料分析、数量关系、判断推理、言语理解四大模块。搭配 AI 助手（Claude Desktop 等），随时随地智能解题。

## 🚀 一分钟快速上手

### 第一步：安装

```powershell
pip install xingce-solver[sse]
```

> 如果你没有 Python，先安装 [Python 3.10+](https://www.python.org/downloads/)，安装时勾选"Add Python to PATH"。

### 第二步：启动服务

```powershell
xingce-solver-mcp-sse
```

看到 `Uvicorn running on http://0.0.0.0:8000` 即启动成功 👌

### 第三步：连接 AI 助手

**Claude Desktop 用户**，在配置文件（`%APPDATA%\Claude\claude_desktop_config.json`）中加入：

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

连接成功后，你可以在对话框里直接这样说：

> 「帮我解一道资料分析题：2020 年某产业收入为 132 亿元，同比增长 10%，问 2019 年收入约为多少？A.100 亿元 B.110 亿元 C.120 亿元 D.132 亿元」

AI 助手会自动调用 `solve_data_analysis` 工具，返回分析过程和答案。

也可以这样说：

> 「搜索一下关于增长率比较的解题方法」

AI 助手会调用 `search_methods` 工具，从 442 张方法卡片中找到相关内容。

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
| **v0.7.0** | 知识库大扩容 292→442 张卡片，新增 SSE 服务器，新手友好 |
| **v0.6.0** | 图形推理框架 v0.2.1，8 种反模式，662 项测试全部通过 |

---

> 💡 **有问题？** 在 [GitHub Issues](https://github.com/heihei999/huasheng-mcp/issues) 提出
