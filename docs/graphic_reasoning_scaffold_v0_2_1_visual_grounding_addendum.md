# graphic_reasoning_scaffold v0.2.1 visual grounding addendum

## 概述

本次在 v0.2 基础上继续补强图推 scaffold 的执行层约束。

**重要说明**：
- 本次不是增加图像识别能力
- MCP 仍然不负责看图
- 图片仍由接入的多模态大模型读取
- 本次增强的是图推 scaffold 的运算规则、证伪机制、空间核验和不确定性输出
- 本次只做文本结构测试，不做图片测试
- 不能宣称图推正确率达到某个百分比
- 最终正确率仍取决于接入模型的视觉识别和空间推理能力

## v0.2 已有内容

- specialized_templates（7 个专项模板）
- visual_transcription_protocol（视觉转写协议）
- anti_pattern_guards（反模式守卫）
- 更新的 prompt template

## v0.2.1 新增/补强内容

### 1. black_white_operation_rules

黑白/线条叠加运算规则，包含 8 种运算类型：

| ID | 名称 | 规则 |
|----|------|------|
| direct_overlay | 直接叠加 | 黑+黑=黑，黑+白=黑，白+黑=黑，白+白=白 |
| xor_remove_same_keep_different | 去同存异（异或） | 黑+黑=白，黑+白=黑，白+黑=黑，白+白=白 |
| keep_same_remove_different | 去异存同 | 黑+黑=黑，黑+白=白，白+黑=白，白+白=白 |
| black_intersection | 黑色交集 | 黑+黑=黑，黑+白=白，白+黑=白，白+白=白 |
| white_intersection | 白色交集 | 黑+黑=黑，黑+白=黑，白+黑=黑，白+白=白 |
| color_inversion | 颜色反转 | 先叠加再整体反转颜色 |
| line_overlay | 线条叠加 | 上层线条优先显示 |
| line_xor | 线条异或 | 同位置线条抵消 |

mandatory_process 要求：
- 叠加类题必须选取同一行或同一列的前两个图形
- 逐格代入候选运算规则
- 只有能完整推出第三个图形的规则才能采纳
- 不允许只说"像叠加"就作答

### 2. falsification_protocol

证伪机制，要求模型在输出答案前主动尝试证伪：

- unified_check：检查当前规律能否解释所有已知图
- option_elimination：A/B/C/D 逐项排除
- competing_rule：尝试至少一个竞争规律
- conflict_check：如果竞争规律也能推出不同答案，必须说明冲突
- uniqueness_check：如果两个及以上选项都能解释，输出 analysis_only

### 3. spatial_verification_protocol

空间题核验协议，覆盖 three_views、cube_net、solid_assembly 三类：

**three_views**：
- 坐标/高度表
- 俯视图格子转写
- 左视图/正视图最大高度
- 颜色
- 遮挡关系
- A/B/C/D 逐项验证

**cube_net**：
- 标记六个面
- 相邻面/相对面
- 公共边/公共点
- 图案方向
- 折叠后可见面

**solid_assembly**：
- 目标方块总数
- 颜色数
- 每个选项方块数和颜色数
- 层数
- 凹凸互补
- 长短高低
- 重叠
- 数量矛盾时必须回到视觉转写重新核对，不得硬解释

### 4. uncertainty_reporting_protocol

不确定性报告协议：

- confidence_level：high / medium / low
- risk_points：列出所有不确定因素
- possible_competing_rule：是否存在竞争规律
- why_other_options_rejected：排除其他选项的具体理由

analysis_only 触发条件：
- confidence_level 为 low
- risk_points 涉及关键视觉事实
- possible_competing_rule 能推出不同答案
- 无法对所有选项给出明确排除理由

### 5. visual_transcription_protocol 增强

新增 grid_specific_requirements：

- coordinate_system：网格题必须建立虚拟坐标系
- black_cell_coordinates：记录黑色块坐标集合
- line_endpoint_coordinates：记录线条端点坐标
- key_vertices：记录关键顶点
- diagonal_direction：记录斜边方向
- coverage_cells：记录覆盖格
- options_same_transcription：A/B/C/D 选项也必须做同样转写

### 6. prompt template 更新

新增输出结构：

- 【候选规律 1】
- 【候选规律 2 / 竞争规律】
- 【证伪检查】
- 【风险点与置信度】
- 【最终答案或 analysis_only】

## 测试覆盖

新增测试断言：

- scaffold 返回 black_white_operation_rules
- scaffold 返回 falsification_protocol
- scaffold 返回 spatial_verification_protocol
- scaffold 返回 uncertainty_reporting_protocol
- visual_transcription_protocol 包含坐标、端点、关键顶点、斜边方向、覆盖格
- black_white_operation_rules 包含 8 种运算类型
- falsification_protocol 包含竞争规律、A/B/C/D 逐项排除、analysis_only
- spatial_verification_protocol.three_views 包含坐标、高度、俯视图、左视图、正视图、遮挡
- spatial_verification_protocol.cube_net 包含相邻面、相对面、公共边、公共点、图案方向
- spatial_verification_protocol.solid_assembly 包含方块总数、颜色数、层数、凹凸、重叠、数量矛盾
- uncertainty_reporting_protocol 包含 confidence_level、risk_points、possible_competing_rule、why_other_options_rejected
- prompt template 包含视觉转写、专项模板选择、竞争规律、证伪检查、选项逐项验证、风险点与置信度、analysis_only
- 不出现任何硬编码答案序列
- 不新增图片 fixture
- 不使用 OCR/OpenCV/PIL

## 不变的部分

- MCP 工具数量：15 个（未变）
- MCP 工具名称：未变
- knowledge_base/all_cards.jsonl：未修改
- solvers/data_analysis.py：未修改
- 无新依赖引入
