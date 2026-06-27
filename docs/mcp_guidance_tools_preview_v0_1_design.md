# MCP Guidance Tools Preview v0.1 Design

## 1. Background

项目已经形成 solver track + scaffold track 双轨结构。稳定 solver 负责可规则化题型（资料分析、翻译推理、论证类逻辑推理、真假推理、分析推理）；scaffold 用于语义/视觉依赖强、纯规则不稳定的题型（图形推理、定义判断、类比推理、分析推理）。

4 个 scaffold 已完成并通过 output audit。本阶段将其暴露为 MCP read-only guidance tools，供大模型在解题时获取方法论约束。

## 2. Scope

本阶段把以下 6 个 scaffold 暴露为 MCP read-only guidance tools，并新增 1 个 route-only tool：

- `get_graphic_reasoning_scaffold`
- `get_definition_judgement_scaffold`
- `get_analogy_reasoning_scaffold`
- `get_logic_analysis_scaffold`
- `get_quantity_relation_scaffold`
- `get_verbal_reasoning_scaffold`
- `route_xingce_question` (route-only, not a scaffold tool)

## 3. Non-scope

本阶段不做：

- solver 开发
- 自动解题
- 图像识别
- CLI 接入
- 外部 LLM/API 调用
- 知识库修改
- 数量关系
- 言语理解

## 4. Tool behavior

每个 tool：

- 不接收题目
- 不接收选项
- 不接收图片
- 只返回对应 scaffold dict
- 不返回 answer / selected_option / prediction
- 不进行自动选择
- 不唯一时由 scaffold 约束大模型 analysis_only

## 5. Tool list

### get_graphic_reasoning_scaffold

返回图形推理视觉观察顺序、组成路由、15 项视觉检查清单、响应模板、不确定性策略。

### get_definition_judgement_scaffold

返回定义判断问法极性、14 项定义要素、必要条件/附加描述区分规则、选项核验步骤、选是/选非校验、不确定性策略。

### get_analogy_reasoning_scaffold

返回类比推理 5 种题干形式、23 种关系类型、造句验证步骤、横纵比较步骤、不确定性策略。

### get_logic_analysis_scaffold

返回分析推理 8 种题型路由、8 种结构模板、20 种约束条件、选项代入验证步骤、不确定性策略。

### get_quantity_relation_scaffold

返回数量关系 23 种题型路由、12 种方法清单、11 步思考顺序、选项代入验证步骤、不确定性策略。

### get_verbal_reasoning_scaffold

返回言语理解 15 种题型路由、15 种方法清单、11 步思考顺序、文段结构/逻辑填空/语句表达三类检查清单、选项验证步骤、不确定性策略。

## 6. Boundary guarantees

- read-only
- guidance only
- no answer selection
- no solver integration
- no CLI integration
- no image recognition
- no OCR/OpenCV/PIL
- no ML dependency
- no external LLM/API
- no network

## 7. Testing

新增 `tests/test_mcp_guidance_tools_preview.py`，覆盖：

- mcp_server import
- 6 个 tool 名存在
- 返回 dict
- module/mode 正确
- no answer fields
- uncertainty_policy / must_not_do 存在
- analysis_only 存在
- forbidden dependency check
- no solver call in guidance tools

## 8. Future work

后续可以单独审批：

- CLI preview command
- MCP smoke with actual client
- 数量关系 scaffold/solver
- 言语理解 scaffold
- 真假推理 v7.2 refinement

但这些不属于本阶段。
