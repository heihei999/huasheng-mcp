# Data Analysis v5 Final Summary

## 1. Version Conclusion

资料分析 v5 标记为当前稳定版本。

除非新的真实题图测试暴露通用缺口，否则暂停继续扩展资料分析 solver。

下一阶段建议启动 `solve_logic_reasoning v1`。

## 2. Supported Capabilities

资料分析 v5 当前支持：

- 基期量
- 现期量
- 增长率
- 增长量
- 本期比重
- 基期比重
- 比重变化
- 两个现期比重差 / 百分点差
- 逆向间隔增长率
- 多对象增长量排序
- 基期差值 / 前期差值
- 同增长率下的基期差值
- 时间分段后求倍数
- 分组求和后求倍数
- 多对象现期量 + 增长量反推增速排序
- 累计减新增 + 残差小类 + 基期占比
- 选项解析
- 选项差距判断
- 安全估算
- `answer_candidate` 匹配
- `needs_more_data` 和 `warnings`

## 3. Engineering Capabilities

当前资料分析模块已具备：

- CLI 调用
- MCP Server 调用
- `solve_data_analysis`
- `classify_question`
- `search_methods`
- `get_method_card`
- `get_source_reference`
- pytest 测试
- smoke test
- 多模态题图接入规范
- `current_question_payload` 传参规范
- 真实题图测试记录模板
- 失败类型分类文档

## 4. Real Image Test Results

真实题图测试：10/10 通过。

| case_id | 题型 | 核心能力 | 预期答案 | 实际结果 | 主要 method_id | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| DA-01 | 逆向间隔增长率 | 2021/2020 与 2021/2019 反推 2020/2019 | A | A | `da_growth_rate_interval_002` | 通过 |
| DA-02 | 本期比重 | 两个分项合计 / 总体 | C | C | `da_share_current_001` | 通过 |
| DA-03 | 增长量排序 | 多对象增长量估算排序 | D | D | `da_growth_amount_compare_002` | 通过 |
| DA-04 | 基期比重 | 分项还原基期后求比重 | C | C | `da_share_base_002` | 通过 |
| DA-05 | 基期差值 | 同增长率下现期差整体折回 | A | A | `da_abx_base_diff_003` | 通过 |
| DA-06 | 反推增速排序 | 现期量 + 增长量反推增长率排序 | D | D | `da_growth_rate_general_001` | 通过 |
| DA-07 | 比重差 / 百分点差 | 两个现期比重作差 | A | A | `da_share_change_004` | 通过 |
| DA-08 | 分组求和后倍数 | 两组数据分别求和后相除 | A | A | `da_truncate_division_001` | 通过 |
| DA-09 | 累计减新增 + 残差占比 | 上年累计、小类残差、占比 | D | D | `da_time_segments_001` / `da_share_current_001` | 通过 |
| DA-10 | 时间分段后倍数 | 1-3月累计减3月得到1-2月再求倍数 | A | A | `da_time_segments_001` | 通过 |

## 5. Multimodal Image Workflow

资料分析题图推荐流程：

```text
用户上传题图
↓
多模态客户端完整阅读图片
↓
根据当前题号筛选 current_question_payload
↓
不要把整篇共用材料全文直接传给 solve_data_analysis
↓
调用 classify_question
↓
调用 solve_data_analysis
↓
必要时调用 get_method_card / get_source_reference
↓
根据 method_id、solving_plan、computed_result、answer_candidate 输出讲解
```

共用材料题不能把整篇材料全文直接传给 solver。当前题无关数字应放入 `ignored_context`，不要混入 `question_text`。如果 solver 返回结果与题干口径不一致，客户端必须标记 `uncertain`，不能直接采信。

多模态客户端负责读图和结构化，MCP solver 负责方法论约束和解题辅助。

## 6. Current Boundaries

- 本项目不自己做 OCR。
- 本项目不自己做图像识别。
- 本项目不直接处理图片像素。
- 图片由多模态客户端读取。
- MCP solver 接收结构化后的 `current_question_payload`。
- 资料分析 v5 是考场估算/方法论辅助工具，不是数学精算器。
- 复杂表格题依赖多模态客户端转写质量。
- 如果新题暴露缺口，应先判断是否为通用题型缺口，不要写 case_id 硬编码。

## 7. Freeze Recommendation

资料分析 v5 作为当前稳定节点。

后续除非真实题图测试出现通用缺口，否则不再继续扩展资料分析 solver。

下一阶段建议优先开发 `solve_logic_reasoning v1`。

在开发新模块前，建议先做一次 git commit 或项目压缩备份。
