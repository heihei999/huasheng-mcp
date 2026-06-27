# 资料分析知识库 source audit 报告

- audit_time: 2026-06-08T05:55:51
- card_count: 33
- source_files: `【花生十三】资料分析思维导图.pdf`, `花生资料分析笔记.pdf`
- audit_scope: source_file/source_page 校验、命名不确定项修正、工程字段补充。
- output_files: `data_analysis_cards_audited.jsonl`, `data_analysis_methods_audited.md`, `data_analysis_router_rules_audited.yaml`, `data_analysis_uncertain_items_audited.md`.

## 校验结论

- 所有卡片均保留原始必需字段，并新增 `required_inputs`、`calculation_policy`、`solver_priority`、`output_constraints`。
- 未新增 PDF 中没有依据的方法；新增内容仅为工程调用所需元数据、路由描述和输出约束。
- `source_page` 均限定在原 PDF 页数范围内：思维导图 1-6 页，笔记 1-16 页。
- `da_base_terms_001` 的思维导图来源被移除，因为基础术语主要出现在笔记第3页。
- `da_fraction_compare_difference_001` 的正式方法名已修正为“常用分数大小比较法”；保留旧 id 以避免下游路由断裂。

## 发生变更的卡片

- `da_base_terms_001`：资料分析基础术语与审题四步 -> 资料分析基础术语与审题四步；变更字段：source_page/source_file, confidence
- `da_fraction_compare_difference_001`：分数比较差分法（待复核命名） -> 常用分数大小比较法；变更字段：method_name, need_review, confidence
- `da_capacity_overlap_001`：两集合占比容斥判断法 -> 两集合容斥边界判断法；变更字段：method_name

## 逐卡片 source audit 索引

- `da_base_terms_001` | 基础知识/统计术语与审题原则 | 资料分析基础术语与审题四步 | source: 花生资料分析笔记.pdf p.3 | confidence=0.95 | need_review=False
- `da_abx_base_direct_001` | 基期量/已知现期量B和增长率R求基期A | 基期量直接公式法 | source: 【花生十三】资料分析思维导图.pdf p.1；花生资料分析笔记.pdf p.7 | confidence=0.96 | need_review=False
- `da_abx_base_interval_002` | 基期量/隔年前期量 | 隔年前期先求间隔增长率法 | source: 【花生十三】资料分析思维导图.pdf p.1；花生资料分析笔记.pdf p.7,8 | confidence=0.95 | need_review=False
- `da_abx_base_diff_003` | 基期量/前期差值 | 前期差值比较法 | source: 【花生十三】资料分析思维导图.pdf p.1；花生资料分析笔记.pdf p.7 | confidence=0.9 | need_review=False
- `da_abx_current_001` | 现期量/已知基期量或增长量求现期 | 现期量列式与假设增量法 | source: 【花生十三】资料分析思维导图.pdf p.1；花生资料分析笔记.pdf p.7,8 | confidence=0.93 | need_review=False
- `da_growth_rate_general_001` | 增长率/一般增长率 | 一般增长率公式法 | source: 【花生十三】资料分析思维导图.pdf p.1；花生资料分析笔记.pdf p.7 | confidence=0.97 | need_review=False
- `da_growth_rate_interval_002` | 增长率/间隔增长率 | 间隔增长率及逆运用 | source: 【花生十三】资料分析思维导图.pdf p.1；花生资料分析笔记.pdf p.7,8 | confidence=0.96 | need_review=False
- `da_growth_rate_ratio_003` | 增长率/比值增长率 | 比值增长率公式法 | source: 【花生十三】资料分析思维导图.pdf p.1,6；花生资料分析笔记.pdf p.7,8,9 | confidence=0.95 | need_review=False
- `da_growth_rate_product_004` | 增长率/乘积增长率 | 乘积增长率公式法 | source: 【花生十三】资料分析思维导图.pdf p.1；花生资料分析笔记.pdf p.7 | confidence=0.9 | need_review=False
- `da_growth_amount_001` | 增长量/直接求增长量X | 增长量公式与方法选择 | source: 【花生十三】资料分析思维导图.pdf p.1；花生资料分析笔记.pdf p.7 | confidence=0.96 | need_review=False
- `da_growth_amount_compare_002` | 增长量/增长量大小比较 | B-R双大与N倍比较法 | source: 【花生十三】资料分析思维导图.pdf p.2；花生资料分析笔记.pdf p.12 | confidence=0.92 | need_review=False
- `da_share_current_001` | 比重/本期/单期比重 | 本期比重主体定位法 | source: 【花生十三】资料分析思维导图.pdf p.6；花生资料分析笔记.pdf p.9 | confidence=0.97 | need_review=False
- `da_share_base_002` | 比重/基期比重/前期比重 | 基期比重公式法 | source: 【花生十三】资料分析思维导图.pdf p.6；花生资料分析笔记.pdf p.9 | confidence=0.96 | need_review=False
- `da_share_trend_003` | 比重变化/两期比重升降判断 | 比重趋势比较增速法 | source: 【花生十三】资料分析思维导图.pdf p.6；花生资料分析笔记.pdf p.9,10 | confidence=0.97 | need_review=False
- `da_share_change_004` | 比重变化/比重差/百分点变化 | 比重差公式与秒杀法 | source: 【花生十三】资料分析思维导图.pdf p.6；花生资料分析笔记.pdf p.9,10 | confidence=0.93 | need_review=False
- `da_ratio_share_diff_005` | 比重变化/比值增长率/比重差/比值差辨析 | 三类分式变化辨析表 | source: 【花生十三】资料分析思维导图.pdf p.6；花生资料分析笔记.pdf p.9 | confidence=0.96 | need_review=False
- `da_average_general_001` | 平均数/一般平均值 | 一般平均值‘均前每后’法 | source: 【花生十三】资料分析思维导图.pdf p.3；花生资料分析笔记.pdf p.13 | confidence=0.95 | need_review=False
- `da_average_annual_growth_amount_002` | 平均数/年均增长量 | 年均增长量基期判断法 | source: 【花生十三】资料分析思维导图.pdf p.3；花生资料分析笔记.pdf p.13 | confidence=0.93 | need_review=False
- `da_average_annual_growth_rate_003` | 平均数/年均增长率 | 年均增长率幂次与近似法 | source: 【花生十三】资料分析思维导图.pdf p.3；花生资料分析笔记.pdf p.13 | confidence=0.92 | need_review=False
- `da_compare_ratio_growth_001` | 比较类/比值大小/增速大小比较 | 双线法与比值趋势法 | source: 【花生十三】资料分析思维导图.pdf p.2；花生资料分析笔记.pdf p.12 | confidence=0.88 | need_review=False
- `da_chart_lookup_001` | 图表查找比较/图表直接查找与排序 | 图表查找四坑校验法 | source: 【花生十三】资料分析思维导图.pdf p.2；花生资料分析笔记.pdf p.12 | confidence=0.94 | need_review=False
- `da_truncate_division_001` | 速算方法/除法截位与选项差距判断 | 截位直除法 | source: 【花生十三】资料分析思维导图.pdf p.4；花生资料分析笔记.pdf p.5 | confidence=0.92 | need_review=False
- `da_415_parts_001` | 速算方法/增长量速算 | 415份数法 | source: 【花生十三】资料分析思维导图.pdf p.4；花生资料分析笔记.pdf p.6 | confidence=0.96 | need_review=False
- `da_assumption_allocation_001` | 速算方法/增长量速算 | 假设分配法 | source: 【花生十三】资料分析思维导图.pdf p.4；花生资料分析笔记.pdf p.6 | confidence=0.88 | need_review=False
- `da_estimation_add_sub_mul_001` | 速算方法/加减乘速算 | 尾数-高位叠加-削峰填谷-乘法拆分法 | source: 【花生十三】资料分析思维导图.pdf p.4；花生资料分析笔记.pdf p.4,5 | confidence=0.91 | need_review=False
- `da_fraction_compare_difference_001` | 速算方法/分数大小比较 | 常用分数大小比较法 | source: 【花生十三】资料分析思维导图.pdf p.6；花生资料分析笔记.pdf p.5 | confidence=0.92 | need_review=False
- `da_salt_cross_001` | 盐水类/十字交叉法 | 十字交叉求分母之比 | source: 【花生十三】资料分析思维导图.pdf p.5；花生资料分析笔记.pdf p.11 | confidence=0.95 | need_review=False
- `da_salt_qualitative_002` | 盐水类/定性分析 | 混合值不居中定性判断法 | source: 【花生十三】资料分析思维导图.pdf p.5；花生资料分析笔记.pdf p.11 | confidence=0.89 | need_review=False
- `da_salt_quantitative_003` | 盐水类/定量分析 | 已知2R/3R与量之比反求R法 | source: 【花生十三】资料分析思维导图.pdf p.5；花生资料分析笔记.pdf p.11 | confidence=0.87 | need_review=False
- `da_time_segments_001` | 盐水类/时间分段 | 累计期与单月分段比较法 | source: 【花生十三】资料分析思维导图.pdf p.5；花生资料分析笔记.pdf p.11 | confidence=0.91 | need_review=False
- `da_ladong_contribution_001` | 特殊考点/拉动增长率与增量贡献率 | 拉动增长率/增量贡献率公式法 | source: 花生资料分析笔记.pdf p.14 | confidence=0.93 | need_review=False
- `da_capacity_overlap_001` | 特殊考点/容斥问题 | 两集合容斥边界判断法 | source: 花生资料分析笔记.pdf p.14 | confidence=0.94 | need_review=False
- `da_common_pitfalls_001` | 易错点/资料分析常见陷阱 | 资料分析常见陷阱清单 | source: 【花生十三】资料分析思维导图.pdf p.2,3,6；花生资料分析笔记.pdf p.3,9,12,13 | confidence=0.95 | need_review=False
