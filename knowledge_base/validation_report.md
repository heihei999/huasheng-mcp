# validation_report.md

## 总览
- 总卡片数：292
- 模块数：9
- need_review=true 卡片数：8
- 原始模块 ZIP 数：7

## 每模块卡片数
- 资料分析: 33
- 数量关系: 65
- 判断推理-图形推理: 39
- 判断推理-逻辑判断: 42
- 判断推理-定义判断: 13
- 判断推理-类比推理: 23
- 言语理解-主旨意图: 32
- 言语理解-语句表达: 25
- 言语理解-逻辑填空: 20

## need_review=true 卡片列表
- lj_relation_quantifier_001 | 判断推理-逻辑判断 | 结论推出 | 所有/有些/可能/必然关系转换法
- lj_compare_experiment_construct_001 | 判断推理-逻辑判断 | 加强削弱 | 构成对比实验变量控制法
- lj_conclusion_equivalent_inference_001 | 判断推理-逻辑判断 | 结论推出 | 等价命题与选项替换法
- lj_category_analysis_001 | 判断推理-逻辑判断 | 分析推理 | 文氏图范畴分析法
- lj_argument_evaluation_001 | 判断推理-逻辑判断 | 评价论证 | 评价论证结构定位法
- qr_calculation_formula_001 | 数量关系 | 数论与计算 | 常用代数公式与乘方尾数法
- qr_balance_weighing_001 | 数量关系 | 统筹规划问题 | 接近3^n判断称重次数
- vecl_cloze_idiom_misread_018 | 言语理解-逻辑填空 | 逻辑填空 | 望文生义防错卡

### 特别关注模块
- 数量关系: ['qr_calculation_formula_001', 'qr_balance_weighing_001']
- 言语理解-逻辑填空: ['vecl_cloze_idiom_misread_018']
- 判断推理-逻辑判断: ['lj_relation_quantifier_001', 'lj_compare_experiment_construct_001', 'lj_conclusion_equivalent_inference_001', 'lj_category_analysis_001', 'lj_argument_evaluation_001']

## JSONL 解析结果
- 输入模块 JSONL 错误数：0
- all_cards.jsonl 解析：通过

## YAML 解析结果
- 输入/输出 YAML 错误数：0
- global_router_rules.yaml：通过
- module_map.yaml：通过
- synonyms.yaml：通过

## id 唯一性检查
- 未发现冲突；所有原 method_id 均保持不变。

## 必需字段完整性检查
- 缺失字段记录数：0
- 通过：所有卡片均包含统一 schema 必需字段。

## router method_id 引用检查
- 路由规则总数：135
- 无效 method_id 引用数：0
- 通过：所有 priority_method_id 和 backup_method_ids 均可在 all_cards.jsonl 中找到。

## router method_id 修正记录
```json
[
  {
    "route_id": "dj_ar_analogy_reasoning",
    "notes": [
      "semantic: ar_semantic_synonym_001 -> ar_semantic_synonym_001",
      "semantic: ar_semantic_antonym_001 -> ar_semantic_antonym_001",
      "semantic: ar_semantic_extended_001 -> ar_semantic_extended_001",
      "semantic: ar_semantic_secondary_001 -> ar_semantic_secondary_001",
      "grammar: ar_grammar_pos_001 -> ar_grammar_pos_001",
      "grammar: ar_grammar_structure_001 -> ar_grammar_structure_001",
      "logic: ar_logic_cross_001 -> ar_logic_cross_001",
      "logic: ar_logic_species_genus_001 -> ar_logic_species_genus_001",
      "logic: ar_logic_composition_001 -> ar_logic_composition_001",
      "logic: ar_logic_opposition_contradiction_001 -> ar_logic_opposition_contradiction_001",
      "logic: ar_logic_equivalence_001 -> ar_logic_equivalence_001",
      "correspondence: ar_correspond_cause_effect_001 -> ar_correspond_cause_effect_001",
      "correspondence: ar_correspond_time_sequence_001 -> ar_correspond_time_sequence_001",
      "correspondence: ar_sentence_tool_object_place_001 -> ar_sentence_tool_object_place_001",
      "correspondence: ar_correspond_subject_quantity_001 -> ar_correspond_subject_quantity_001",
      "other: ar_split_word_001 -> ar_split_word_001",
      "other: ar_common_traps_001 -> ar_common_traps_001",
      "patch_v1_1: restored existing correspondence cards to backup_method_ids: ar_correspond_necessary_001, ar_correspond_material_001, ar_correspond_function_001, ar_correspond_purpose_001"
    ]
  }
]
```

## v1.1 路由补丁记录
- 已复核 `dj_ar_analogy_reasoning` 类比推理总路由。
- `ar_correspond_necessary_001`、`ar_correspond_material_001`、`ar_correspond_function_001`、`ar_correspond_purpose_001` 均存在于 `all_cards.jsonl`。
- 已将上述 4 张“对应关系类”卡片恢复进该路由的 `backup_method_ids`。
- 已删除该路由中将上述卡片误标为 fallback 到 `ar_total_flow_001` 的修正说明。
- 复验结果：所有 router `priority_method_id` 与 `backup_method_ids` 均存在，未新增卡片，未改动原卡片内容。

## solver_priority 标准化结果
- 已将整数 solver_priority 统一转换为 `{tier, rank, fallback_method_ids}` 对象。
- 已保留资料分析原有对象型 solver_priority，并补齐缺失键。

## aliases 补全结果
- 原卡片无 aliases 时已统一补 `aliases: []`。
- 未凭空新增别名。

## reasoning_policy 补全结果
- 原卡片只有 calculation_policy 时，已复制为 reasoning_policy。
- 两者均存在时保留原值。

## source_file/source_page 标准化结果
- source_file 已统一为数组。
- source_page 已统一为数组。
- 未新增 PDF 页码，未删除已有来源。

## 模块命名标准化
- `判断推理-定义判断与类比推理` 已按 question_type 拆分为 `判断推理-定义判断` 与 `判断推理-类比推理`。
- `言语理解-语句表达与逻辑填空` 已按 question_type 拆分为 `言语理解-语句表达` 与 `言语理解-逻辑填空`。
- 为保留溯源，发生拆分的卡片保留 `original_module` 字段。

## 发现的问题
- 未发现阻断性问题。
- need_review=true 卡片仍保留在全库中，但不建议在 Codex/MCP 中作为高优先级自动调用方法。
- v1.2 表达澄清：`source_audit_summary.md` 中“没有 need_review”的表述应理解为“没有卡片级 `need_review=true`”，不代表模块 `uncertain_items_audited.md` 中没有页面级、例题级或局部图示复核建议。

## 建议处理方式
- Codex/MCP 检索时优先过滤或降权 `need_review=true` 卡片。
- 若用户明确请求复核来源，再打开对应 source_file/source_page 做人工核验。
- 后续新增模块时，先生成 audited 版 zip，再重新运行本合并流程。

## v1.2 source_audit_summary 表达澄清
- 已将 `source_audit_summary.md` 中每模块的 `need_review` 表述改为 `card_level_need_review`。
- 已新增“页面/例题级 uncertain_items 说明”表格，汇总各模块原始 uncertain_items 的复核建议。
- 本次只修改说明文档，不修改 `all_cards.jsonl`、`global_router_rules.yaml`、`method_manifest.json` 或任何模块原始卡片。


## v1.3 最终 PDF 对照复核
- 已对 v1.2 最终包与 16 个原始 PDF 做逐项来源对照。
- 16 个 PDF 均存在；所有 source_file 均来自这 16 个 PDF。
- 所有 source_page 均在对应 PDF 物理页码范围内。
- 未发现 method_id 冲突、router 引用失效、必需字段缺失或模块来源误串。
- 未修改 all_cards.jsonl、global_router_rules.yaml 或任何方法卡片正文。
- 详细结果见 `final_pdf_crosscheck_report.md`。
