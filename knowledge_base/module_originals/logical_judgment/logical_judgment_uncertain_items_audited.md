# 判断推理-逻辑判断不确定项记录（audited）

## 总体说明

本文件只记录本轮“判断推理-逻辑判断”转换中的不确定项。凡 OCR 不清、图像页细节无法完全确认、来源页虽然相关但无法确认具体层级的内容，均不编造，相关卡片已标记 `need_review=true`。

---

## item_001：范畴关系细节层级不完全清晰

- source_file: `花生判断笔记总结.pdf`
- source_page: 18
- uncertainty_type: 图像页细节/OCR层级不确定
- observed_content: 页面包含“范畴分析”“一个小二画圈法”“所有画实圈，有些画不确定圈”等内容。
- why_uncertain: 页面为扫描图像，部分手写标注和示例选项细节不完全清晰。
- affected_card_id: `lj_category_analysis_001`
- handling: 保留“文氏图、所有/有些、确定/不确定区域”的确定方法，不扩展示例细节。
- need_review: true

## item_002：等价推出细节部分来自笔记图像，局部文字不清

- source_file: `花生判断笔记总结.pdf`
- source_page: 16
- uncertainty_type: 图像页文字不清/层级不确定
- observed_content: 页面包含“推出类”“等价推出”“正推/逆推”“两难推理”等内容。
- why_uncertain: OCR 可读，但图片中的例题细节和部分手写标注无法完全确认。
- affected_card_id: `lj_conclusion_equivalent_inference_001`
- handling: 只保留与 `【判断推理】逻辑基本知识.pdf` 中一致的逆否等价、命题方向等内容。
- need_review: true

## item_003：评价论证不是独立页标题，属于工程化路由需求

- source_file:
  - `【判断推理】支持、前提假设、比例、解释说明.pdf`
  - `【判断推理】质疑类.pdf`
  - `花生判断笔记总结.pdf`
- source_page:
  - `【判断推理】支持、前提假设、比例、解释说明.pdf`: 1
  - `【判断推理】质疑类.pdf`: 1
  - `花生判断笔记总结.pdf`: 8, 11
- uncertainty_type: 方法命名工程化/原文无独立题型标题
- observed_content: 原资料明确强调论证题需主体一致、话题一致、贴合题干，并区分论据、结论、断点和选项力度；但未单独以“评价论证”作为完整章节。
- why_uncertain: 用户要求 router_rules.yaml 区分“评价论证”，因此用论点-论据-断点评价框架生成路由卡，但标记需复核。
- affected_card_id: `lj_argument_evaluation_001`
- handling: 不新增具体评价题型技巧，只做“检验论证断点”的通用路由框架。
- need_review: true

## item_004：构成对比实验页面部分选项特征文字不完全清晰

- source_file:
  - `花生判断笔记总结.pdf`
  - `【判断推理】质疑类.pdf`
- source_page:
  - `花生判断笔记总结.pdf`: 6
  - `【判断推理】质疑类.pdf`: 1
- uncertainty_type: 扫描图像局部文字不清
- observed_content: 页面展示“构成对比实验例题”，包含支持与质疑两类路径。
- why_uncertain: 图像例题与手写批注较密集，无法确认所有例题选项文本。
- affected_card_id: `lj_compare_experiment_construct_001`
- handling: 仅保留变量控制、组间差异、支持/质疑方向等确定方法，不复刻例题细节。
- need_review: true

## item_005：量词关系的完整矛盾表未逐项展开

- source_file:
  - `【判断推理】逻辑基本知识.pdf`
  - `花生判断笔记总结.pdf`
- source_page:
  - `【判断推理】逻辑基本知识.pdf`: 1
  - `花生判断笔记总结.pdf`: 15, 18
- uncertainty_type: OCR/内容边界不确定
- observed_content: 原资料列出“所有、有些；可能、必然”等范畴关系和矛盾关系。
- why_uncertain: 源文件没有完整展开所有量词否定规则，若后续需要完整形式逻辑表，应另行人工复核。
- affected_card_id: `lj_relation_quantifier_001`
- handling: 卡片只保留常见保守规则和防错提示。
- need_review: true

## item_006：花生判断笔记第20页以后内容未纳入本轮

- source_file: `花生判断笔记总结.pdf`
- source_page: 20-32
- uncertainty_type: 范围外内容
- observed_content: 第20页以后为定义判断、类比推理、图形推理、秒杀及补充等内容。
- why_uncertain: 用户本轮限定为“判断推理-逻辑判断”，这些内容不属于本轮模块。
- affected_card_id: 无
- handling: 未抽取到逻辑判断卡片，后续处理对应模块时再转换。
- need_review: false
