# xingce-solver

> 注意：本项目不是独立自动答题器。MCP 负责题型路由、方法卡检索、解题脚手架、答题提示词约束和安全门控；最终读图、读表、计算、推理和选答案仍由接入的大模型完成。因此，实际答题正确率会受到接入模型能力影响。建议使用中文理解、多模态视觉、表格阅读和推理能力较强的大模型。

基于花生十三行测方法论的 MCP 解题辅助工具。为 Claude Code、Codex 等支持 MCP 协议的 LLM Agent 提供结构化的行测题型路由、方法检索和答题引导。

## 功能概述

- **题型路由**：自动识别题目所属模块（资料分析、逻辑判断、图形推理、定义判断、类比推理、数量关系、言语理解），返回置信度和推荐分析路径
- **方法检索**：从 292 张结构化方法卡片中检索匹配的解题方法
- **结构化求解**：资料分析和逻辑判断模块提供完整的解题草案
- **Scaffold 引导**：6 个模块的方法论脚手架，指导逐步分析
- **保守答题**：多层安全门控制，信息不足时自动降级为分析模式，不强行作答

## 架构

```
用户题目 → MCP Server（路由 + prompt 组合） → LLM 客户端执行 → 结构化答案
                ↓
        知识库（292张方法卡片 + 路由规则）
```

MCP Server 本身不调用外部 LLM，只生成严格约束的 prompt，由接入的 LLM Agent（如 Claude Code、Codex 等）执行解题。

## 安装

需要 Python 3.10+。

```bash
pip install -e .
```

验证安装：

```bash
python -c "import xingce_solver.mcp_server; print('ok')"
python smoke_test_core.py
```

## CLI 使用

```bash
# 搜索方法卡
xingce-solver search --query "比重 增长率"

# 查看方法卡详情
xingce-solver card --id da_share_change_004

# 资料分析求解
xingce-solver solve-data --text "2020年某产业收入为132亿元，同比增长10%，问2019年收入约为多少？ A.100亿元 B.110亿元 C.120亿元 D.132亿元"

# 逻辑判断求解
xingce-solver solve-logic --text "只有缴费，才可以报名。小王已经报名。根据上述信息，可以推出的是：A.小王没有缴费 B.缴费的人一定报名 C.小王已经缴费 D.没有报名的人一定没有缴费"
```

## MCP Server

```bash
xingce-solver-mcp
# 或
python -m xingce_solver.mcp_server
```

提供 15 个 MCP tool：

| 类别 | Tool | 说明 |
|------|------|------|
| 路由 | `route_xingce_question` | 题型路由，支持 module_hint/section_context |
| 路由 | `compose_xingce_analysis_prompt` | 组合分析提示词 |
| 路由 | `compose_xingce_answer_prompt` | 保守型答题提示词 |
| 知识 | `get_method_card` | 获取方法卡 |
| 知识 | `search_methods` | 搜索方法卡 |
| 知识 | `classify_question` | 轻量关键词路由 |
| 知识 | `get_source_reference` | 来源溯源 |
| 求解 | `solve_data_analysis` | 资料分析结构化求解 |
| 求解 | `solve_logic_reasoning` | 逻辑判断结构化求解 |
| 引导 | `get_graphic_reasoning_scaffold` | 图形推理方法论 |
| 引导 | `get_definition_judgement_scaffold` | 定义判断方法论 |
| 引导 | `get_analogy_reasoning_scaffold` | 类比推理方法论 |
| 引导 | `get_logic_analysis_scaffold` | 分析推理方法论 |
| 引导 | `get_quantity_relation_scaffold` | 数量关系方法论 |
| 引导 | `get_verbal_reasoning_scaffold` | 言语理解方法论 |

### 接入 LLM Agent

以 Claude Code 为例：

```bash
claude mcp add-json xingce-solver '{"type":"stdio","command":"python","args":["-m","xingce_solver.mcp_server"]}' --scope user
```

重启 Claude Code 后运行 `/mcp` 验证 tool 列表。

其他支持 MCP 协议的 Agent（如 Codex、Cline、opencode 等）可参照各自的 MCP 配置方式接入，server 启动命令相同。

## 与 LLM 的协作模式

1. LLM 调用 `route_xingce_question` 获取模块路由
2. LLM 调用 `compose_xingce_answer_prompt` 获取严格约束的答题 prompt
3. LLM 调用对应模块的 scaffold tool 获取方法论指导
4. LLM 基于 prompt + scaffold + 自身能力输出结构化答案

关键约束：MCP tool 永远不直接输出答案，只生成 prompt。答案由 LLM 严格遵循约束后输出。

## 安全机制

- **Answer Gate**：缺图片/缺材料/路由不确定/低置信度时阻止回答，自动降级为 analysis_only
- **13 条核心约束**：不猜测、不默认选 A、不编造视觉内容、不确定时不作答
- **Safety Contract**：tool 返回中不包含 answer/selected_option/prediction 字段
- **module_hint 安全优先**：强材料信号始终覆盖 module_hint，防止误路由导致错误作答

## 测试

```bash
# 冒烟测试
PYTHONPATH=src python smoke_test_core.py

# 完整测试（需安装 pytest）
python -m pytest
```

## 项目结构

```
src/xingce_solver/
├── mcp_server.py          # MCP Server 核心（路由 + prompt 组合 + tool 注册）
├── router.py              # 基于 YAML 规则的题型路由
├── kb.py                  # 知识库加载与检索
├── cli.py                 # CLI 接口
├── solvers/
│   ├── data_analysis.py   # 资料分析求解器
│   ├── logic_reasoning.py # 逻辑判断求解器
│   ├── truth_reasoning.py # 真假推理
│   └── logic_analysis_reasoning.py  # 分析推理
└── scaffolds/             # 6 个模块的方法论脚手架
    ├── graphic_reasoning_scaffold.py
    ├── definition_judgement_scaffold.py
    ├── analogy_reasoning_scaffold.py
    ├── logic_analysis_scaffold.py
    ├── quantity_relation_scaffold.py
    └── verbal_reasoning_scaffold.py

knowledge_base/
├── all_cards.jsonl        # 292 张方法卡片
├── global_router_rules.yaml  # 路由规则
├── module_map.yaml        # 模块映射
└── synonyms.yaml          # 同义词表
```

## 版本历史

- **v0.5.1**：module_hint 边界case修复，三年真题330/330路由验证通过
- **v0.5.0**：新增 module_hint/section_context 参数，支持中文模块名
- **v0.4.3**：文本排列题和定义判断路由覆盖增强
- **v0.4.2**：资料分析材料信号独立检测
- **v0.4.1**：保守答题门控强化
- **v0.4.0**：保守型答题 prompt 组合器

## 视觉能力说明

本 MCP Server 本身不具备视觉能力，不能直接识别图片。行测中的图形推理、资料分析（含图表）等需要看图的题型，依赖 LLM 客户端的多模态能力：

1. **客户端负责看图**：支持视觉的 LLM Agent 先识别图片内容，将图形特征、图表数据转写为文字描述
2. **MCP 负责结构化分析**：将转写后的文字描述传入 MCP tool，由路由和 scaffold 引导分析流程

推荐使用支持视觉的模型（如 Claude Sonnet/Opus、GPT-4o 等）作为客户端，以完整覆盖图形推理和资料分析等含图表的题型。纯文本模型只能处理文字类题型。

## 答题正确率说明

本仓库中的验证结果（三年真题 330/330 路由验证）衡量的是 MCP 路由/门控/脚手架的行为，而非独立的最终答案正确率。

最终答案质量取决于接入模型的能力，包括但不限于：

- 中文阅读理解能力
- 多模态视觉识别能力（图形推理、图表题）
- 表格/材料数据提取能力
- 计算准确性
- 多步推理稳定性

获得较好实际效果的建议：

- 已知考试模块时，始终传入 `module_hint` 或 `section_context`
- 图形推理题提供原始图片
- 资料分析题提供完整的表格/材料
- 涉及图形、图表、表格的题目，使用多模态大模型

## 限制

- 不做 OCR 或图片识别，视觉内容由 LLM 客户端转写
- 不调用外部 LLM/API
- 不重新解析 PDF 或重新生成知识卡片
- 知识库基于花生十三方法论，不含其他来源的方法

## License

MIT
