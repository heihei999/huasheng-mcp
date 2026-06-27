# graphic_reasoning_scaffold v0.2 hardening

## 概述

本次更新将图推 scaffold 从"通用检查清单"升级为"专项强制验算模板"。

**重要说明**：
- 本次不是增加本地图像识别能力
- MCP 仍然不看图、不输出最终答案
- 本次是把图推 scaffold 从通用检查清单增强为专项强制验算模板
- 最终正确率仍取决于接入多模态模型的视觉识别和推理能力
- 本次不得宣称图推正确率提升到某个百分比

## 背景

最近用 10 道图推题测试，现有 scaffold 覆盖了一组图、九宫格、三视图、展开图、立体拼合、分组分类等大类，但模型仍容易：

1. 网格黑图只凭"旋转感"误判
2. 复杂黑白图案不拆固定部件和移动部件
3. 线条图只看开闭性，漏看端点、交点、平行垂直
4. 三视图不建立坐标/高度表
5. 展开图只看关键图案，不验证相邻面/相对面
6. 立体拼合出现数量矛盾仍继续硬解释
7. 分组分类只抓一个候选特征就选答案

## 新增字段

### 1. specialized_templates

7 个专项强制验算模板：

| ID | 名称 | 用途 |
|----|------|------|
| grid_black_shape | 网格黑图专项模板 | 网格内黑色三角形、黑白块、网格移动题 |
| complex_black_white_pattern | 复杂黑白图案专项模板 | 复杂黑白风车状、黑白块组合、局部叠加题 |
| line_symbol_pattern | 线条符号专项模板 | 抽象线条、符号、汉字/字母/数字图推 |
| three_views | 三视图专项模板 | 三视图、俯视图、左视图、正视图 |
| cube_net | 展开图专项模板 | 六面体展开图、两个正方体展开图 |
| solid_assembly | 立体拼合专项模板 | 立体拼合、拆分组合、除哪项外 |
| grouping_classification | 分组分类专项模板 | 六图分两类 |

每个模板包含：
- mandatory_recording / mandatory_procedure：必须记录/执行的步骤
- verification_steps：逐项验证步骤
- constraint：约束条件（不得做什么）

### 2. visual_transcription_protocol

视觉转写协议，要求所有图推题在正式推理前必须先做视觉转写：

- proposition_form：命题形式
- image_present：是否有图
- figure_count：题干图形数量
- option_count：选项数量
- given_figures_visual_facts：每个已知图的视觉事实转写
- options_visual_facts：每个选项的视觉事实转写
- uncertain_visual_details：哪些视觉细节看不清

如果视觉转写缺失或关键细节不可确认，应提示 analysis_only。

### 3. anti_pattern_guards

反模式守卫，防止常见推理失败：

| ID | 禁止行为 | 要求行为 |
|----|----------|----------|
| no_first_glance | 不得只凭第一感觉或"看起来像"作答 | 必须逐条列出视觉证据 |
| no_single_candidate | 不得只凭一个候选规律作答 | 除非 A/B/C/D 逐项验证唯一 |
| grouping_needs_dimensions | 分组分类不得只列一个维度 | 至少列出 3 个候选维度 |
| spatial_needs逐格验证 | 空间类不得跳过逐格/逐面/逐块验证 | 必须输出坐标/面/块核验 |
| bw_needs_component_split | 复杂黑白图不得跳过部件拆分 | 必须标注固定/移动部件 |
| grid_needs_position转写 | 网格题不得跳过行列/顶点转写 | 必须记录覆盖行列和顶点 |
| unified_rule_required | 候选规律不能统一解释时必须 analysis_only | 规律必须通过所有已知图验证 |
| unique_option_required | 两个及以上选项符合时必须 analysis_only | 只有唯一选项满足才能输出答案 |

## 更新的模板

render_graphic_reasoning_prompt_template() 更新为包含以下结构：

1. 【MCP 路由结果】
2. 【是否有图检查】
3. 【视觉转写】（必须出现）
4. 【命题形式】
5. 【专项模板选择】
6. 【组成判断】
7. 【优先规律】
8. 【视觉证据】
9. 【候选规律】
10. 【选项逐项验证】（必须出现）
11. 【唯一性判断】
12. 【不确定性说明】

## 保留的原有知识点

所有原有字段和知识点均已保留：

- 属性规律（对称性、开闭性、曲直性）
- 数量规律（点、线、面、角、素、一笔画、部分数）
- 位置规律（平移、旋转、翻转）
- 样式规律（遍历、加减同异、黑白运算）
- 图形间关系
- 功能元素
- 黑白块
- 汉字类
- 数字类
- 字母类
- 六面体展开图
- 截面图
- 三视图
- 立体拼合

## 测试覆盖

新增测试断言：

- build_graphic_reasoning_scaffold() 返回 specialized_templates
- specialized_templates 包含全部 7 个模板
- visual_transcription_protocol 存在且 mandatory=True
- anti_pattern_guards 存在且至少 8 个
- prompt template 包含"视觉转写""专项模板选择""选项逐项验证""A/B/C/D""analysis_only"
- three_views 模板包含"坐标""高度""俯视图""左视图""正视图"
- cube_net 模板包含"相邻面""相对面""公共边""公共点""图案方向"
- solid_assembly 模板包含"方块总数""颜色数""层数""重叠""数量矛盾"
- grouping_classification 模板包含"至少 3 个候选维度"和"选项反推验证"
- 不出现任何硬编码答案序列

## 不变的部分

- MCP 工具数量：15 个（未变）
- MCP 工具名称：未变
- knowledge_base/all_cards.jsonl：未修改
- solvers/data_analysis.py：未修改
- 无新依赖引入（不引入 OCR/OpenCV/PIL/sklearn/torch/tensorflow）
