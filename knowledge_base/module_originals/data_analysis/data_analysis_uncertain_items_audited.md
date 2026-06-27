# data_analysis_uncertain_items（source audit 清洗版）

## item_001

- source_file: 花生资料分析笔记.pdf
- source_page: [15, 16]
- uncertainty_type: 页面内容不确定 / 可能为空白页
- observed_content: 渲染结果仅显示页码样式的“9”“10”，未识别到有效方法内容。
- why_uncertain: PDF目录页列出第09、10条为空；第15、16页未呈现可抽取知识点。
- suggested_review: 人工确认原PDF第15、16页是否为空白、缺页或仅为占位页。
- related_card_id: null
- need_review: true

## item_002

- source_file: 【花生十三】资料分析思维导图.pdf
- source_page: [4]
- uncertainty_type: 手写图示细节不确定
- observed_content: 假设分配法右侧存在若干手写分配树和修正数字，主干步骤可识别，但个别手写数值细节较小。
- why_uncertain: 这些数值用于例题演算，不影响“假设分配法”的方法抽取，但若要复刻例题完整计算过程需人工复核。
- suggested_review: 若后续要建立例题库，请单独复核思维导图第4页右侧手写分配树的数字。
- related_card_id: da_assumption_allocation_001
- need_review: true

## item_003

- source_file: 花生资料分析笔记.pdf
- source_page: [13]
- uncertainty_type: 口诀边界不确定
- observed_content: 年均增长率处写有“当选项极不正常的时候用公式”及近似 `末期/基期 ≈ 1+nR`。
- why_uncertain: “选项极不正常”的判定边界没有量化，不能转为稳定机器规则。
- suggested_review: 后续规则库中可将其保留为人工提示，不作为自动路由硬条件。
- related_card_id: da_average_annual_growth_rate_003
- need_review: true

## item_004

- source_file: 花生资料分析笔记.pdf
- source_page: [6]
- uncertainty_type: 手写批注边界不确定
- observed_content: 415份数法与假设分配法中有粉色重点、蓝红手写分配示意和若干比例经验，如R在不同区间对应A:X比例。
- why_uncertain: 主公式和步骤清楚，但经验比例属于速算经验，适用边界依赖选项差距，不能当作严格数学公式。
- suggested_review: 后续如果要做自动求解器，应把这些比例设为“估算策略”，不要设为唯一解法。
- related_card_id:
  - da_415_parts_001
  - da_assumption_allocation_001
- need_review: true

## item_005

- source_file: 【花生十三】资料分析思维导图.pdf
- source_page: [1]
- uncertainty_type: 例题细节不完整
- observed_content: ABRX页包含多个小字号例题框，部分数字可读但完整题干较密集。
- why_uncertain: 方法主干可稳定抽取，但不适合把所有例题完整转写为训练样例。
- suggested_review: 若后续要抽取“例题库”，建议对思维导图第1页分块放大后人工校对。
- related_card_id:
  - da_abx_base_direct_001
  - da_growth_amount_001
  - da_growth_rate_interval_002
- need_review: true

## resolved_item_001

- source_file:
  - 【花生十三】资料分析思维导图.pdf
  - 花生资料分析笔记.pdf
- source_page:
  - {file: 【花生十三】资料分析思维导图.pdf, pages: [6]}
  - {file: 花生资料分析笔记.pdf, pages: [5]}
- previous_uncertainty_type: 方法命名不确定
- resolution: 原卡片 `da_fraction_compare_difference_001` 保留原id以兼容旧路由，但 method_name 已从“分数比较差分法（待复核命名）”修正为“常用分数大小比较法”，need_review 改为 false。PDF中未把该方法明确命名为“差分法”，因此清洗版不再使用“差分法”作为正式方法名。
- related_card_id: da_fraction_compare_difference_001
- need_review: false
