# graphic_reasoning_scaffold v0.2.2 error-driven addendum

## 概述

本次基于新一批 10 道图推题的错误类型，对图推 scaffold 做小范围增量补强。

**重要说明**：
- 本次不是增加图像识别能力
- MCP 仍然不负责看图
- 图片仍由接入的多模态大模型读取
- 本次补强的是图推 scaffold 的坐标集合协议、九宫格规律切换、截面图几何守卫、立体拼合残差校验、分组分类维度
- 本次只做文本结构测试，不做图片测试
- 不能宣称图推正确率达到某个百分比
- 最终正确率仍取决于接入模型的视觉识别和空间推理能力

## 实测错误分析

基于 10 道图推题实测，正确率 5/10，错第 4、6、7、9、10 题：

| 错题 | 题型 | 错误类型 |
|------|------|----------|
| 第 4 题 | 九宫格（网格圆圈/叠加/数量） | 数量/叠加规律局部失效后继续硬套 |
| 第 6 题 | 立体图形（截面图/切面形状） | 凭直觉排除规则截面图形（矩形、梯形等） |
| 第 7 题 | 立体图形（拼合/数量守恒/凹凸互补） | 未计算残差，假设每个组件必须含颜色块 |
| 第 9 题 | 分组分类（线条/部分数/一笔画） | 未检查面数/部分数/一笔画/奇点数等强制维度 |
| 第 10 题 | 分组分类（黑白块/最大面/对称性） | 未检查面积占比/重心/接边/接角等强制维度 |

## v0.2.1 已有内容

- specialized_templates（7 个专项模板）
- visual_transcription_protocol（视觉转写协议）
- anti_pattern_guards（8 个反模式守卫）
- black_white_operation_rules（8 种叠加运算规则）
- falsification_protocol（证伪机制）
- spatial_verification_protocol（空间题核验）
- uncertainty_reporting_protocol（不确定性报告）
- 更新的 prompt template

## v0.2.2 新增/补强内容

### 1. dot_grid_coordinate_protocol

点阵/圆圈网格坐标集合协议，适用于蜂窝状黑白圆圈、网格圆圈、九宫格黑白圆圈、黑白点阵移动/叠加/对称题。

核心要求：
- coordinate_system_required：必须建立虚拟坐标系
- black_point_set_required：必须输出每个已知图的黑点坐标集合（集合形式）
- option_black_point_set_required：必须输出 A/B/C/D 每个选项的黑点坐标集合
- coordinate_set_operations：6 种坐标集合运算
  - direct_overlay（直接叠加/并集）
  - xor_remove_same_keep_different（去同存异）
  - intersection（交集）
  - complement_or_inversion（补集/反转）
  - row_or_column_translation（行列平移）
  - rotation_or_reflection（旋转/翻转）
- movement_trace_check：移动轨迹验证
- symmetry_check：对称性验证
- fallback_to_analysis_only：无法建立统一规律时输出 analysis_only

### 2. nine_grid_fallback_protocol

九宫格规律切换机制，当数量/叠加规律失效时强制切换到其他候选规律。

核心要求：
- horizontal_first：必须优先横向看
- vertical_second：必须再纵向看
- failure_detection：数量/叠加在任一行/列失效即视为失败
- mandatory_switch_targets：必须切换到的候选规律
  - 整体轴对称
  - 中心对称
  - 黑点移动轨迹
  - 黑点重心变化
  - 坐标集合映射
- no_failed_rule_persistence：不得在局部失效后继续硬套
- competing_rule_output：多个规律都能解释时输出 analysis_only

### 3. cross_section（补强 spatial_verification_protocol）

截面图几何守卫，补强 spatial_verification_protocol 的 cross_section 子类型。

核心要求：
- required_steps：8 个必要步骤
  - 判断立体类型
  - 判断切面方向和位置
  - 检查切面是否平行于某个侧面
  - 检查切面是否平行于底面
  - 检查切面是否经过同一高度层
  - 检查切面是否穿过相邻面形成直角边
  - 检查三点确定的平面是否可能形成规则截面
  - A/B/C/D 逐项验证截面可行性
- required_output：6 个必要输出
- geometric_guards：6 个几何守卫
  - parallel_to_side：切面平行于侧面时，矩形/正方形可能成立
  - parallel_to_base：切面平行于底面时，截面形状与底面相同
  - same_height_layer：经过同一高度层时，截面边数由该层决定
  - adjacent_face_intersection：穿过相邻面时，梯形和矩形都可能成立
  - three_point_plane：三点确定平面，需要具体分析
  - no_intuitive_rejection：不得凭直觉排除规则图形
- constraint：不得凭直觉排除，不确定时输出 analysis_only

### 4. solid_assembly residual_check（补强 solid_assembly 模板）

立体拼合残差校验，补强 solid_assembly 专项模板。

核心要求：
- required_calculations：6 个必要计算
  - 目标总块数
  - 目标颜色块数量
  - 已知组件块数和颜色块数
  - remaining_total_blocks = 目标总块数 - 已知组件总块数
  - remaining_color_blocks = 目标颜色块数 - 已知组件颜色块数
  - remaining_white_blocks = remaining_total_blocks - remaining_color_blocks
- constraints：4 个约束
  - 已知组件颜色块数 = 目标颜色块数时，待选组件可全白
  - 不得默认每个组件必须含某种颜色块
  - 视觉转写无法确认时输出 analysis_only
  - 必须同时检查凹凸互补、层数、重叠、多块、少块、颜色错位
- keywords：10 个关键词

### 5. forced_dimensions_by_type（补强 grouping_classification 模板）

分组分类维度扩展，补强 grouping_classification 专项模板。

**线条/多边形分组强制维度**：
- 封闭区域数/面数（精确数字，禁止模糊描述）
- 部分数
- 一笔画/奇点数
- 端点数
- 交点数
- 平行线组数
- 直角数
- 最大面的形状
- 是否有相同构件

precision_requirement：数面数时必须使用封闭区域定义，输出具体数字（如：图1=3面，图2=4面），禁止使用"较多/较少""大概"等模糊描述。

**黑白块/黑白面分组强制维度**：
- 黑块面积占比
- 黑块重心位置
- 最大黑色区域形状
- 黑块是否接边
- 黑块是否接角
- 黑块是否形成轴对称或中心对称
- 黑白区域是否分割成相同部分数
- 最大面/最大黑块与外框的位置关系

### 6. 新增 anti_pattern_guards（5 个）

| ID | forbidden | required |
|----|-----------|----------|
| no_intuitive_cross_section_rejection | 截面图不得凭直觉排除矩形、梯形、三角形等规则图形 | 必须验证切面与侧面/底面平行关系 |
| no_color_count_assumption | 立体拼合不得假设每个组件都必须包含某种颜色块 | 必须计算残差，允许待选组件全白 |
| no_fuzzy_face_count | 分组分类数面时不得使用"较多/较少""大概"等模糊描述 | 必须输出精确封闭区域数 |
| no_single_dimension_grouping | 分组分类不得只凭一个维度作答 | 必须列多个候选维度并证伪 |
| no_failed_rule_persistence | 九宫格中数量/叠加规律失效后不得继续硬套 | 必须切换到对称性、移动轨迹等候选规律 |

### 7. prompt template 更新

新增或强化的要求：
- 点阵/圆圈网格题必须输出黑点坐标集合
- 九宫格题若数量/叠加失败，必须检查对称性、移动轨迹、重心变化
- 截面图必须验证切面与侧面/底面平行关系
- 立体拼合必须输出目标块数、已知组件块数、待选组件残差
- 分组分类必须按题型列强制候选维度
- 最终答案前必须说明被排除选项为何不成立
- 如果关键视觉事实不清楚，输出 analysis_only

## 测试覆盖

新增测试断言：

- scaffold 包含 dot_grid_coordinate_protocol
- dot_grid_coordinate_protocol 包含坐标集合、黑点坐标、选项黑点、移动轨迹、对称
- scaffold 包含 nine_grid_fallback_protocol
- nine_grid_fallback_protocol 包含横看、竖看、数量、叠加、轴对称、中心对称、移动轨迹、重心
- scaffold 包含 cross_section（spatial_verification_protocol 的子类型）
- cross_section 包含截面图、切面、平行于侧面、平行于底面、三点确定平面、矩形、梯形、不得凭直觉排除
- solid_assembly 模板包含残差、目标总块数、颜色数、已知组件、待选组件、全白、数量守恒
- grouping_classification 模板包含面数、部分数、一笔画、奇点数、黑块面积占比、重心、最大黑色区域、接边、接角
- anti_pattern_guards 包含 no_intuitive_cross_section_rejection、no_color_count_assumption、no_fuzzy_face_count、no_failed_rule_persistence
- prompt template 包含黑点坐标集合、截面图、残差、候选维度、analysis_only
- 不出现硬编码答案序列 D A C B D B A C C D
- 不新增图片 fixture
- 不使用 OCR/OpenCV/PIL

## 不变的部分

- MCP 工具数量：15 个（未变）
- MCP 工具名称：未变
- knowledge_base/all_cards.jsonl：未修改
- solvers/data_analysis.py：未修改
- 无新依赖引入
- 无图片测试
- 无硬编码答案
