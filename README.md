     1|# 花生十三-mcp
     2|
     3|> 注意：本项目不是独立自动答题器。MCP 负责题型路由、方法卡检索、解题脚手架、答题提示词约束和安全门控；最终读图、读表、计算、推理和选答案仍由接入的大模型完成。因此，实际答题正确率会受到接入模型能力影响。建议使用中文理解、多模态视觉、表格阅读和推理能力较强的大模型。
     4|
     5|基于花生十三行测方法论的 MCP 解题辅助工具。为 Claude Code、Codex 等支持 MCP 协议的 LLM Agent 提供结构化的行测题型路由、方法检索和答题引导。
     6|
     7|## Important: what this MCP does and does not guarantee
     8|
     9|本 MCP **不是**独立自动答题器。
    10|
    11|它提供题型路由、方法卡检索、解题脚手架、答题提示词约束和安全门控，服务于接入的 LLM Agent（如 Claude Code、Codex 等）。接入的大模型负责读图、读表、理解题意、计算、逐步推理和选择最终答案。
    12|
    13|因此，最终答题正确率取决于：
    14|
    15|1. MCP 的路由 / 脚手架 / 安全门控约束，以及
    16|2. 接入大模型的能力和指令遵循程度。
    17|
    18|为获得较好实际效果，客户端应在已知考试模块时传入 `module_hint` 或 `section_context`，例如：
    19|
    20|- `言语理解`
    21|- `数量关系`
    22|- `图形推理`
    23|- `定义判断`
    24|- `类比推理`
    25|- `逻辑判断`
    26|- `资料分析`
    27|
    28|图形推理题需要原始图片或可靠的文字描述。资料分析题需要完整的表格、图表或材料上下文。
    29|
    30|## 功能概述
    31|
    32|- **题型路由**：自动识别题目所属模块（资料分析、逻辑判断、图形推理、定义判断、类比推理、数量关系、言语理解），返回置信度和推荐分析路径
    33|- **方法检索**：从 292 张结构化方法卡片中检索匹配的解题方法
    34|- **结构化求解**：资料分析和逻辑判断模块提供完整的解题草案
    35|- **Scaffold 引导**：6 个模块的方法论脚手架，指导逐步分析
    36|- **保守答题**：多层安全门控制，信息不足时自动降级为分析模式，不强行作答
    37|
    38|## 架构
    39|
    40|```
    41|用户题目 → MCP Server（路由 + prompt 组合） → LLM 客户端执行 → 结构化答案
    42|                ↓
    43|        知识库（292张方法卡片 + 路由规则）
    44|```
    45|
    46|MCP Server 本身不调用外部 LLM，只生成严格约束的 prompt，由接入的 LLM Agent（如 Claude Code、Codex 等）执行解题。
    47|
    48|## 安装
    49|
    50|需要 Python 3.10+。
    51|
    52|```bash
    53|pip install -e .
    54|```
    55|
    56|验证安装：
    57|
    58|```bash
    59|python -c "import xingce_solver.mcp_server; print('ok')"
    60|python smoke_test_core.py
    61|```
    62|
    63|## 快速部署指南（傻瓜式接入）
    64|
    65|> 本节面向不熟悉命令行的同学。跟着步骤一步步来，10 分钟内就能跑通。
    66|
    67|### 一键克隆安装
    68|
    69|打开终端（Windows 用户打开 PowerShell，Mac/Linux 用户打开 Terminal），依次输入以下三条命令：
    70|
    71|```bash
    72|# 第一步：把项目下载到本地
    73|git clone https://github.com/heihei999/huasheng-mcp.git
    74|
    75|# 第二步：进入项目文件夹
    76|cd huasheng-mcp
    77|
    78|# 第三步：安装项目（会自动下载所有依赖）
    79|pip install -e .
    80|```
    81|
    82|安装完成后，你可以选择 **Claude Code** 或 **Codex** 作为你的 AI 助手平台。三个方案选一个即可，不需要都装。
    83|
    84|### 方案零：让 AI 自己安装（最省事）
    85|
    86|如果你已经在用 Claude Code 或 Codex，可以直接在会话中发一条消息，让 AI 自己读取仓库、安装项目、配置 MCP，全程自动完成。
    87|
    88|#### Claude Code 用户
    89|
    90|启动 Claude Code 后，直接发送：
    91|
    92|> 请帮我安装这个项目的 MCP 服务：https://github.com/heihei999/huasheng-mcp
    93|
    94|Claude Code 会自动克隆仓库、安装依赖、配置 MCP，并告诉你结果。
    95|
    96|#### Codex 用户
    97|
    98|启动 Codex 后，直接发送：
    99|
   100|> 请帮我安装这个项目的 MCP 服务：https://github.com/heihei999/huasheng-mcp
   101|
   102|Codex 会自动完成全部流程。
   103|
   104|### 前置条件
   105|
   106|在接入之前，请确认你的电脑满足以下条件：
   107|
   108|| 条件 | 说明 |
   109||------|------|
   110|| Python 3.10 或更高版本 | 终端输入 `python --version` 查看。如果版本低于 3.10，需要先升级 Python |
   111|| git | 用来下载项目代码。终端输入 `git --version` 检查是否已安装 |
   112|| Claude Code **或** Codex（二选一） | 分别参考下方的「方案一」或「方案二」 |
   113|
   114|> 💡 **怎么查看 Python 版本？** 打开终端，输入 `python --version`，如果显示 `Python 3.10.x` 或 `3.11.x`、`3.12.x` 等就是合格的。如果显示 `3.9.x` 或更低，需要去 [python.org](https://www.python.org) 下载最新版本。
   115|
   116|### 方案一：Claude Code 接入
   117|
   118|如果你已经安装了 Claude Code（Anthropic 官方的命令行 AI 助手），选择这个方案。
   119|
   120|#### 方法 A：一条命令搞定（推荐）
   121|
   122|在终端中输入：
   123|
   124|```bash
   125|claude mcp add huasheng-mcp --scope user -- python -m xingce_solver.mcp_server
   126|```
   127|
   128|执行完毕后重启 Claude Code 即可。
   129|
   130|#### 方法 B：手动配置 JSON 文件
   131|
   132|如果命令行方式不生效，可以手动编辑配置文件：
   133|
   134|1. 找到配置文件：在项目根目录创建 `.mcp.json`，或者编辑用户目录下的 `~/.claude.json`
   135|2. 添加以下内容（`~/.claude.json` 文件中找到或新建 `mcpServers` 字段）：
   136|
   137|```json
   138|{
   139|  "mcpServers": {
   140|    "huasheng-mcp": {
   141|      "type": "stdio",
   142|      "command": "python",
   143|      "args": ["-m", "xingce_solver.mcp_server"]
   144|    }
   145|  }
   146|}
   147|```
   148|
   149|> ⚠️ 如果你的 Python 安装路径不在系统 PATH 中，需要把 `"python"` 替换为完整的 Python 路径，例如 `"/usr/local/bin/python3"` 或 `"C:\\Python312\\python.exe"`。
   150|
   151|#### 验证 Claude Code 接入
   152|
   153|1. 重启 Claude Code
   154|2. 输入 `/mcp` 查看 MCP 服务列表，应该能看到 `huasheng-mcp` 旁边显示 ✓ Connected
   155|3. 也可以在终端输入 `claude mcp list` 检查状态
   156|
   157|### 方案二：Codex 接入
   158|
   159|如果你使用的是 OpenAI Codex CLI，选择这个方案。
   160|
   161|#### 方法 A：一条命令搞定（推荐）
   162|
   163|在终端中输入：
   164|
   165|```bash
   166|codex mcp add huasheng-mcp -- python -m xingce_solver.mcp_server
   167|```
   168|
   169|执行完毕后重启 Codex 即可。
   170|
   171|#### 方法 B：手动编辑 TOML 配置文件
   172|
   173|1. 打开或创建配置文件 `~/.codex/config.toml`
   174|2. 添加以下内容：
   175|
   176|```toml
   177|[mcp_servers.huasheng-mcp]
   178|command = "python"
   179|args = ["-m", "xingce_solver.mcp_server"]
   180|```
   181|
   182|> ⚠️ 同样，如果 Python 不在系统 PATH 中，需要把 `"python"` 替换为完整路径。
   183|
   184|#### 验证 Codex 接入
   185|
   186|1. 启动 Codex 会话
   187|2. 输入 `/mcp` 查看 MCP 服务列表，确认 `huasheng-mcp` 已连接
   188|
   189|### 验证连接
   190|
   191|接入完成后，试一试下面的操作来确认一切正常：
   192|
   193|**Claude Code 用户：**
   194|
   195|1. 打开终端，输入 `claude mcp list`，确认 `huasheng-mcp` 旁边有 ✓ Connected 标记
   196|2. 启动 Claude Code 会话，发送以下测试问题：
   197|
   198|```
   199|帮我路由这道题：资料分析，某市2023年GDP为5.2万亿元，同比增长8.5%，其中第二产业增加值2.1万亿元，同比增长6.3%。问第二产业增加值占GDP比重与上年相比如何变化？
   200|```
   201|
   202|3. 如果 Claude 能给出路由结果（识别为"资料分析"模块）并开始分析，说明接入成功 ✅
   203|
   204|**Codex 用户：**
   205|
   206|1. 启动 Codex 会话，输入 `/mcp` 确认连接状态
   207|2. 发送类似的测试问题，确认 Codex 能正常调用 MCP 工具并返回分析结果
   208|
   209|### 常见问题
   210|
   211|#### ❌ 报错 "command not found: claude" 或 "command not found: codex"
   212|
   213|**原因：** 你还没有安装对应的 AI 助手工具。
   214|
   215|**解决：** 
   216|- Claude Code：参考 [Anthropic 官方文档](https://docs.anthropic.com/en/docs/claude-code) 安装
   217|- Codex：参考 [OpenAI 官方文档](https://platform.openai.com/docs) 安装
   218|
   219|#### ❌ 报错 "ModuleNotFoundError: No module named 'xingce_solver'"
   220|
   221|**原因：** 项目还没有安装到你的 Python 环境中。
   222|
   223|**解决：** 回到项目文件夹，重新运行安装命令：
   224|
   225|```bash
   226|cd huasheng-mcp
   227|pip install -e .
   228|```
   229|
   230|#### ❌ 连接失败 / MCP 工具不出现
   231|
   232|**原因：** 可能是以下几种情况之一：
   233|
   234|1. **Python 版本太低** — 请确认 `python --version` 显示 3.10 或更高版本
   235|2. **配置文件路径错误** — 重新检查 JSON/TOML 配置文件的内容和路径是否正确
   236|3. **会话没有重启** — 每次修改 MCP 配置后，必须关闭并重新打开 Claude Code 或 Codex 会话
   237|
   238|#### ❌ 工具列表里看不到花生成相关的 tool
   239|
   240|**解决：** 添加 MCP 配置后，一定要**完全退出并重新启动**会话（不是开新对话，而是退出程序重新打开）。然后输入 `/mcp` 检查状态。
   241|
   242|#### ❌ Windows 用户 Python 命令找不到
   243|
   244|**解决：** Windows 上有时需要用 `python3` 或完整路径。在 PowerShell 中运行：
   245|
   246|```powershell
   247|# 查看 Python 安装位置
   248|where.exe python
   249|
   250|# 如果上面没结果，试试
   251|where.exe python3
   252|```
   253|
   254|找到路径后，在配置中把 `"command": "python"` 改为完整路径，例如：
   255|
   256|```json
   257|"command": "C:\\Users\\你的用户名\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
   258|```
   259|
   260|> 💡 **万能解决方法：** 如果遇到奇怪的问题，最简单的方式是删掉已有的 MCP 配置，重新跑一遍上面的"一条命令"。对于 Claude Code 可以先执行 `claude mcp remove huasheng-mcp`，然后再执行 `claude mcp add`。
   261|
   262|## CLI 使用
   263|
   264|```bash
   265|# 搜索方法卡
   266|huasheng-mcp search --query "比重 增长率"
   267|
   268|# 查看方法卡详情
   269|huasheng-mcp card --id da_share_change_004
   270|
   271|# 资料分析求解
   272|huasheng-mcp solve-data --text
   273|
   274|# 逻辑判断求解
   275|huasheng-mcp solve-logic --text
   276|```
   277|
   278|## MCP Server
   279|
   280|```bash
   281|huasheng-mcp-server
   282|# 或
   283|python -m xingce_solver.mcp_server
   284|```
   285|
   286|提供 15 个 MCP tool：
   287|
   288|| 类别 | Tool | 说明 |
   289||------|------|------|
   290|| 路由 | `route_xingce_question` | 题型路由，支持 module_hint/section_context |
   291|| 路由 | `compose_xingce_analysis_prompt` | 组合分析提示词 |
   292|| 路由 | `compose_xingce_answer_prompt` | 保守型答题提示词 |
   293|| 知识 | `get_method_card` | 获取方法卡 |
   294|| 知识 | `search_methods` | 搜索方法卡 |
   295|| 知识 | `classify_question` | 轻量关键词路由 |
   296|| 知识 | `get_source_reference` | 来源溯源 |
   297|| 求解 | `solve_data_analysis` | 资料分析结构化求解 |
   298|| 求解 | `solve_logic_reasoning` | 逻辑判断结构化求解 |
   299|| 引导 | `get_graphic_reasoning_scaffold` | 图形推理方法论 |
   300|| 引导 | `get_definition_judgement_scaffold` | 定义判断方法论 |
   301|| 引导 | `get_analogy_reasoning_scaffold` | 类比推理方法论 |
   302|| 引导 | `get_logic_analysis_scaffold` | 分析推理方法论 |
   303|| 引导 | `get_quantity_relation_scaffold` | 数量关系方法论 |
   304|| 引导 | `get_verbal_reasoning_scaffold` | 言语理解方法论 |
   305|
   306|### 接入 LLM Agent
   307|
   308|以 Claude Code 为例：
   309|
   310|```bash
   311|claude mcp add-json huasheng-mcp '{"type":"stdio","command":"python","args":["-m","xingce_solver.mcp_server"]}' --scope user
   312|```
   313|
   314|重启 Claude Code 后运行 `/mcp` 验证 tool 列表。
   315|
   316|其他支持 MCP 协议的 Agent（如 Codex、Cline、opencode 等）可参照各自的 MCP 配置方式接入，server 启动命令相同。
   317|
   318|## 与 LLM 的协作模式
   319|
   320|1. LLM 调用 `route_xingce_question` 获取模块路由
   321|2. LLM 调用 `compose_xingce_answer_prompt` 获取严格约束的答题 prompt
   322|3. LLM 调用对应模块的 scaffold tool 获取方法论指导
   323|4. LLM 基于 prompt + scaffold + 自身能力输出结构化答案
   324|
   325|关键约束：MCP tool 永远不直接输出答案，只生成 prompt。答案由 LLM 严格遵循约束后输出。
   326|
   327|## 安全机制
   328|
   329|- **Answer Gate**：缺图片/缺材料/路由不确定/低置信度时阻止回答，自动降级为 analysis_only
   330|- **13 条核心约束**：不猜测、不默认选 A、不编造视觉内容、不确定时不作答
   331|- **Safety Contract**：tool 返回中不包含 answer/selected_option/prediction 字段
   332|- **module_hint 安全优先**：强材料信号始终覆盖 module_hint，防止误路由导致错误作答
   333|
   334|## Hard gates vs prompt constraints
   335|
   336|本 MCP 使用两类约束：代码层面的硬门控（hard gates）和提示词层面的约束（prompt-level constraints）。
   337|
   338|### 代码层面的硬门控
   339|
   340|以下检查由 MCP tool 返回值强制执行。触发时，`compose_xingce_answer_prompt` 返回 `answer_allowed = false` 及对应的 `answer_block_reason`。
   341|
   342|当前硬门控包括：
   343|
   344|- 图形推理缺少图片或视觉描述：
   345|  - `answer_block_reason = missing_visual_content`
   346|
   347|- 资料分析缺少表格/材料上下文：
   348|  - `answer_block_reason = missing_table_or_material`
   349|
   350|- 路由不确定且无语义覆盖：
   351|  - `answer_block_reason = route_uncertain_without_semantic_override`
   352|
   353|- 显式禁用答题模式：
   354|  - `answer_block_reason = answer_mode_disabled`
   355|
   356|- 强材料信号（如 `表中`、`根据表格`、`图中数据`、`统计图表`、`上述资料`、`材料显示`）在未提供材料/表格时仍触发材料门控。
   357|
   358|合规的客户端在 `answer_allowed = false` 时不应要求 LLM 输出最终答案。
   359|
   360|### 提示词层面的约束
   361|
   362|部分约束表达在生成的答题 prompt 中，由接入的 LLM 客户端遵循。
   363|
   364|例如：
   365|
   366|- 按模块对应的解题脚手架进行分析；
   367|- 逐项核验选项；
   368|- 证据不足时不猜测；
   369|- 无法唯一确定答案时返回 `analysis_only`；
   370|- 题目内容与 `module_hint` / `section_context` 冲突时说明原因；
   371|- 在需要时使用提供的图片、表格或材料。
   372|
   373|这些提示词约束引导 LLM 的推理行为，但最终遵循程度取决于接入模型和客户端实现。
   374|
   375|## 测试
   376|
   377|```bash
   378|# 冒烟测试
   379|PYTHONPATH=src python smoke_test_core.py
   380|
   381|# 完整测试（需安装 pytest）
   382|python -m pytest
   383|```
   384|
   385|## 项目结构
   386|
   387|```
   388|src/xingce_solver/
   389|├── mcp_server.py          # MCP Server 核心（路由 + prompt 组合 + tool 注册）
   390|├── router.py              # 基于 YAML 规则的题型路由
   391|├── kb.py                  # 知识库加载与检索
   392|├── cli.py                 # CLI 接口
   393|├── solvers/
   394|│   ├── data_analysis.py   # 资料分析求解器
   395|│   ├── logic_reasoning.py # 逻辑判断求解器
   396|│   ├── truth_reasoning.py # 真假推理
   397|│   └── logic_analysis_reasoning.py  # 分析推理
   398|└── scaffolds/             # 6 个模块的方法论脚手架
   399|    ├── graphic_reasoning_scaffold.py
   400|    ├── definition_judgement_scaffold.py
   401|    ├── analogy_reasoning_scaffold.py
   402|    ├── logic_analysis_scaffold.py
   403|    ├── quantity_relation_scaffold.py
   404|    └── verbal_reasoning_scaffold.py
   405|
   406|knowledge_base/
   407|├── all_cards.jsonl        # 292 张方法卡片
   408|├── global_router_rules.yaml  # 路由规则
   409|├── module_map.yaml        # 模块映射
   410|└── synonyms.yaml          # 同义词表
   411|```
   412|
   413|## Release 下载说明
   414|
   415|每个 Release 提供三种打包方式，区别如下：
   416|
   417|| 包名 | 大小 | 需要联网 | 适用场景 |
   418||------|------|---------|---------|
   419|| `clean_runtime.zip` | ~160 KB | 是 | 开发者 / 已有 Python 环境 |
   420|| `online_runtime.zip` | ~140 KB | 是 | 普通用户，有网络环境 |
   421|| `offline_wheelhouse_runtime.zip` | ~14 MB | 否 | 内网 / 无网络环境 |
   422|
   423|### clean_runtime（纯源码包）
   424|
   425|只包含项目源码、知识库和文档，不含任何依赖。
   426|
   427|```powershell
   428|# 解压后进入目录
   429|cd xingce-solver_v0.5.1_clean_runtime
   430|pip install -e .
   431|.\smoke_test.ps1
   432|.\install_claude_code_mcp.ps1   # 自动配置 Claude Code MCP
   433|```
   434|
   435|适合已有 Python 开发环境的用户，需要自行联网安装依赖。
   436|
   437|### online_runtime（在线安装包）
   438|
   439|在 clean_runtime 基础上增加了一键安装脚本，自动完成依赖下载和 MCP 配置。
   440|
   441|```powershell
   442|cd xingce-solver_v0.5.1_online_runtime
   443|.\install_dependencies.ps1      # 自动 pip install
   444|.\smoke_test.ps1
   445|.\install_claude_code_mcp.ps1   # 自动配置 Claude Code MCP
   446|```
   447|
   448|适合有网络环境的普通用户，双击脚本即可完成安装。
   449|
   450|### offline_wheelhouse_runtime（离线安装包）
   451|
   452|包含完整源码 + 31 个预编译 Python wheel 文件（Python 3.11 / Windows），无需联网即可安装。
   453|
   454|```powershell
   455|cd xingce-solver_v0.5.1_offline_wheelhouse_runtime
   456|.\install_dependencies_offline.ps1   # 从本地 wheels 安装
   457|.\smoke_test.ps1
   458|.\install_claude_code_mcp.ps1        # 自动配置 Claude Code MCP
   459|```
   460|
   461|适合内网环境、无法访问 PyPI 的场景。注意：wheel 文件为 **Windows + Python 3.11** 版本，其他平台请使用 online 或 clean 方式安装。
   462|
   463|> 💡 **不确定选哪个？** 如果你能正常上网，直接用 `online_runtime.zip`，三行命令搞定。如果你的电脑不能上网（比如公司内网），用 `offline_wheelhouse_runtime.zip`。
   464|
   465|## 版本历史
   466|
   467|- **v0.5.1**：module_hint 边界case修复，三年真题330/330路由验证通过
   468|- **v0.5.0**：新增 module_hint/section_context 参数，支持中文模块名
   469|- **v0.4.3**：文本排列题和定义判断路由覆盖增强
   470|- **v0.4.2**：资料分析材料信号独立检测
   471|- **v0.4.1**：保守答题门控强化
   472|- **v0.4.0**：保守型答题 prompt 组合器
   473|
   474|## 视觉能力说明
   475|
   476|本 MCP Server 本身不具备视觉能力，不能直接识别图片。行测中的图形推理、资料分析（含图表）等需要看图的题型，依赖 LLM 客户端的多模态能力：
   477|
   478|1. **客户端负责看图**：支持视觉的 LLM Agent 先识别图片内容，将图形特征、图表数据转写为文字描述
   479|2. **MCP 负责结构化分析**：将转写后的文字描述传入 MCP tool，由路由和 scaffold 引导分析流程
   480|
   481|推荐使用支持视觉的模型（如 Claude Sonnet/Opus、GPT-4o 等）作为客户端，以完整覆盖图形推理和资料分析等含图表的题型。纯文本模型只能处理文字类题型。
   482|
   483|## 答题正确率说明
   484|
   485|本仓库中的验证结果（三年真题 330/330 路由验证）衡量的是 MCP 路由/门控/脚手架的行为，而非独立的最终答案正确率。
   486|
   487|最终答案质量取决于接入模型的能力，包括但不限于：
   488|
   489|- 中文阅读理解能力
   490|- 多模态视觉识别能力（图形推理、图表题）
   491|- 表格/材料数据提取能力
   492|- 计算准确性
   493|- 多步推理稳定性
   494|
   495|获得较好实际效果的建议：
   496|
   497|- 已知考试模块时，始终传入 `module_hint` 或 `section_context`
   498|- 图形推理题提供原始图片
   499|- 资料分析题提供完整的表格/材料
   500|- 涉及图形、图表、表格的题目，使用多模态大模型
   501|