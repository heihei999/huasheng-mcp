# 言语理解-主旨意图不确定项记录

## audit_summary

本轮只抽取“主旨意图/中心理解/标题选择/选项分析”相关内容。`花生言语理解笔记.pdf` 中下文推断、语句填入、语句排序、细节判断、逻辑填空、词语辨析等内容未纳入本模块卡片，避免跨模块混入。

## uncertain_001

- source_file: 花生言语理解笔记.pdf
- source_page: [4, 6, 7, 9, 11, 13]
- uncertainty_type: 手写批注/OCR不完整
- observed_content: 页面包含较多蓝色手写批注和例题解析。
- why_uncertain: 手写批注能够辅助理解，但个别字迹和箭头指向无法完全逐字确认。
- handling: 只抽取页面中能稳定确认的方法结构，不把无法确认的手写细节写入卡片。
- related_card_id:
  - vr_mi_total_flow_001
  - vr_mi_topic_sentence_001
  - vr_mi_eliminate_source_001
- need_review: true

## uncertain_002

- source_file: 【言语理解与表达】主旨意图.pdf
- source_page: [1]
- uncertainty_type: 思维导图密集排版
- observed_content: 该 PDF 为单页高密度思维导图，内容覆盖大量结构、例题和选项分析。
- why_uncertain: 单页信息极密，部分例题细节不适合逐项拆成独立卡片。
- handling: 保留“结构分析/选项排除/题型路由”等稳定方法，不单独复刻每一道例题。
- related_card_id:
  - vr_mi_problem_solution_001
  - vr_mi_parallel_001
  - vr_mi_eliminate_scope_001
- need_review: true

## uncertain_003

- source_file: 花生言语理解笔记.pdf
- source_page: [4]
- uncertainty_type: 方法边界不确定
- observed_content: 笔记总览页列有转折、递进等关联词，但递进关系在本轮资料中展开程度少于转折、因果、对策结构。
- why_uncertain: “递进后重点法”有明确依据，但具体例题展开较少。
- handling: 已建立 `vr_mi_progression_001`，confidence 设为 0.78，并要求必须回到整体结构复核。
- related_card_id:
  - vr_mi_progression_001
- need_review: true
