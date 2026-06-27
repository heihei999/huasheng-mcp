# source_audit_summary.md

## 全库来源审计范围
本文件汇总七个已经完成 source audit 的模块 zip。当前合并流程没有重新解析 PDF，也没有新增方法。

## 每个模块使用的源文件
### 资料分析
- 来源 zip：['data_analysis_knowledge_base_audited.zip']
- 【花生十三】资料分析思维导图.pdf
- 花生资料分析笔记.pdf
- card_level_need_review：0 张

### 数量关系
- 来源 zip：['quantity_relation_knowledge_base_audited.zip']
- 【花生十三】数量思维导图.pdf
- 花生数量关系笔记.pdf
- card_level_need_review：2 张，['qr_calculation_formula_001', 'qr_balance_weighing_001']

### 判断推理-图形推理
- 来源 zip：['graphic_reasoning_knowledge_base_audited.zip']
- 【判断推理】图形推理.pdf
- 花生图形推理笔记.pdf
- card_level_need_review：0 张

### 判断推理-逻辑判断
- 来源 zip：['logical_judgment_knowledge_base_audited.zip']
- 【判断推理】支持、前提假设、比例、解释说明.pdf
- 【判断推理】质疑类.pdf
- 【判断推理】逻辑基本知识.pdf
- 花生判断笔记总结.pdf
- card_level_need_review：5 张，['lj_relation_quantifier_001', 'lj_compare_experiment_construct_001', 'lj_conclusion_equivalent_inference_001', 'lj_category_analysis_001', 'lj_argument_evaluation_001']

### 判断推理-定义判断
- 来源 zip：['definition_analogy_knowledge_base_reaudited.zip']
- 【判断推理】定义判断.pdf
- 花生判断笔记总结.pdf
- card_level_need_review：0 张

### 判断推理-类比推理
- 来源 zip：['definition_analogy_knowledge_base_reaudited.zip']
- 【判断推理】类比推理.pdf
- 花生判断笔记总结.pdf
- card_level_need_review：0 张

### 言语理解-主旨意图
- 来源 zip：['verbal_main_idea_knowledge_base_audited.zip']
- 【言语理解与表达】主旨意图.pdf
- 花生言语理解笔记.pdf
- card_level_need_review：0 张

### 言语理解-语句表达
- 来源 zip：['verbal_expression_cloze_knowledge_base_audited.zip']
- 【言语理解与表达】标题、下文、语句填入、排序.pdf
- 【言语理解与表达】逻辑填空.pdf
- 花生言语理解笔记.pdf
- card_level_need_review：0 张

### 言语理解-逻辑填空
- 来源 zip：['verbal_expression_cloze_knowledge_base_audited.zip']
- 【言语理解与表达】逻辑填空.pdf
- 花生言语理解笔记.pdf
- card_level_need_review：1 张，['vecl_cloze_idiom_misread_018']

## 各模块 source audit 结论
- graphic_reasoning_knowledge_base_audited.zip: 已读取 `graphic_reasoning_cards_audited.jsonl`，卡片数 39。
- logical_judgment_knowledge_base_audited.zip: 已读取 `logical_judgment_cards_audited.jsonl`，卡片数 42。
- quantity_relation_knowledge_base_audited.zip: 已读取 `quantity_relation_cards_audited.jsonl`，卡片数 65。
- verbal_expression_cloze_knowledge_base_audited.zip: 已读取 `verbal_expression_cloze_cards_audited.jsonl`，卡片数 45。
- verbal_main_idea_knowledge_base_audited.zip: 已读取 `verbal_main_idea_cards_audited.jsonl`，卡片数 32。
- data_analysis_knowledge_base_audited.zip: 已读取 `data_analysis_cards_audited.jsonl`，卡片数 33。
- definition_analogy_knowledge_base_reaudited.zip: 已读取 `definition_analogy_cards_audited.jsonl`，卡片数 36。

## 哪些模块没有卡片级 need_review=true
- 资料分析
- 判断推理-图形推理
- 判断推理-定义判断
- 判断推理-类比推理
- 言语理解-主旨意图
- 言语理解-语句表达

## 哪些模块仍有卡片级 need_review=true
- 数量关系: ['qr_calculation_formula_001', 'qr_balance_weighing_001']
- 判断推理-逻辑判断: ['lj_relation_quantifier_001', 'lj_compare_experiment_construct_001', 'lj_conclusion_equivalent_inference_001', 'lj_category_analysis_001', 'lj_argument_evaluation_001']
- 言语理解-逻辑填空: ['vecl_cloze_idiom_misread_018']


## 页面/例题级 uncertain_items 说明（v1.2 表达澄清）

本节用于澄清：上文“没有卡片级 need_review=true”只表示 `all_cards.jsonl` 中该模块没有自动降权的卡片，并不等于原模块 `uncertain_items_audited.md` 中没有页面级、例题级或图示局部复核建议。

这些页面/例题级不确定项已经保留在 `module_originals/<module>/*_uncertain_items_audited.md` 中，供人工复核和后续例题库建设使用；合并流程未删除这些信息，也未把它们强行提升为卡片级 `need_review=true`。

| 模块 | 卡片级 need_review=true | uncertain_items 复核项概况 | 处理建议 |
|---|---:|---|---|
| 资料分析 | 0 | 5 个页面/例题级不确定项，另有 1 个已解决命名项 | 方法卡片可正常调用；若要复刻例题完整计算过程，优先复核假设分配、比例经验、例题数字细节 |
| 数量关系 | 2 | 5 个扫描/OCR/公式边界类记录，其中 `qr_calculation_formula_001`、`qr_balance_weighing_001` 已作为卡片级 need_review | 这两张卡片在 Codex/MCP 中降权；公式页和称重模型优先人工复核 |
| 判断推理-图形推理 | 0 | 6 个局部图示不确定项，包括黑白运算表、线数量、功能元素、字母分类、六面体展开图、思维导图小图细节 | 图推总流程和主方法可调用；涉及局部图示表格或自动视觉分类时需人工复核 |
| 判断推理-逻辑判断 | 5 | 5 个卡片级 need_review 项，另有 1 个范围外说明项 | 逻辑判断 need_review 卡片不作为高优先级自动调用方法 |
| 判断推理-定义判断/类比推理 | 0 | 2 个局部复核项，主要是类比推理小字例子、拆词法局部例词；另有 1 个已解决项 | 定义/类比主流程可调用；若要扩展示例库，复核小字例子 |
| 言语理解-主旨意图 | 0 | 3 个页面/方法边界复核项，包括手写批注、单页高密度思维导图、递进关系例题较少 | 主旨意图结构卡可调用；递进关系卡和手写批注不用于硬规则扩展 |
| 言语理解-语句表达/逻辑填空 | 1 | 5 个页码/OCR/批注/例题压缩类复核项，其中 `vecl_cloze_idiom_misread_018` 为卡片级 need_review | 逻辑填空易错成语卡降权；如做词表级训练，复核页码异常和扫描批注 |

因此，v1.2 以后请将“没有 need_review”统一理解为“没有卡片级 `need_review=true`”，而不是“没有任何复核建议”。

## source_page 说明
- 全库保留原模块 audited 版中的 source_page。
- source_page 表示 PDF 物理页码。
- 本轮合并未新增页码，未删除已有来源。

## 后续优先复核建议
- 优先复核 `need_review=true` 卡片。
- 优先复核数量关系、逻辑填空、逻辑判断中被标记 need_review 的卡片，因为这些模块涉及公式、语义边界或论证力度。
- 若发现路由触发过宽，优先调整 `global_router_rules.yaml` 中对应 route，而不要直接改卡片正文。
## v1.1 路由复核补充
- 本补丁仅修正全局路由 `dj_ar_analogy_reasoning` 的 `backup_method_ids`，恢复已存在的类比推理对应关系卡片。
- 未重新解析 PDF，未新增方法卡片，未改动 source_file/source_page。


## v1.2 表达澄清补充
- 本补丁仅澄清 `source_audit_summary.md` 中“need_review”的含义：它默认指 `all_cards.jsonl` 的卡片级 `need_review=true`。
- 模块原始 `uncertain_items_audited.md` 中的页面级、例题级、图示局部复核建议仍然保留，并已在上表汇总。
- 未修改 `all_cards.jsonl`，未修改任何方法卡片内容，未重新解析 PDF。


## v1.3 最终 PDF 对照复核补充
- 已将全库 `source_file/source_page` 与 16 个原始 PDF 逐项核对。
- 结论：source_file 覆盖且仅覆盖这 16 个 PDF；source_page 均为对应 PDF 的有效物理页码；未发现跨模块误引用 PDF。
- 本补充不改变卡片内容、不新增方法、不重新解析 PDF。
