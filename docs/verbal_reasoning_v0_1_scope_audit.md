# Verbal Reasoning v0.1 Scope Audit

## 1. Baseline

- HEAD: `78a7ee6`
- tag: `stable-quantity-relation-mcp-guidance-78a7ee6`
- git status: 4 untracked text-image directories only
- test baseline: 342 passed

## 2. Audit scope

本次只审计言语理解知识卡和后续实现路线：

- no solver added
- no scaffold added
- no MCP/CLI integration
- no real-case package created
- no web search
- no OCR
- no fabricated questions

## 3. Knowledge card inventory summary

- verbal reasoning total card count: 77
- module counts: 言语理解-主旨意图 (32), 言语理解-语句表达 (25), 言语理解-逻辑填空 (20)
- source files checked: knowledge_base/all_cards.jsonl, knowledge_base/module_originals/verbal_expression_cloze/, knowledge_base/module_originals/verbal_main_idea/
- field availability: 全部 77 张卡片字段完整（id, module, question_type, sub_type, method_name, tags, trigger_conditions, anti_conditions, required_inputs, reasoning_policy, calculation_policy, solver_priority, steps, formulas, examples, pitfalls, forbidden, output_constraints, source_file, source_page, confidence, need_review, source_zip）
- parsing limitations: 无，JSONL 格式完整解析

## 4. Category coverage

| Category | Found | Related card titles/method_ids | Notes |
|----------|-------|-------------------------------|-------|
| 主旨意图 | ✅ 32 | vr_mi_* 系列 | 覆盖完整：总流程、问法识别、主体词、主题句、结构类型、干扰项排除 |
| 中心理解 | ✅ | vr_mi_center_understanding_001 | 归入主旨意图大类 |
| 标题填入 | ✅ | vecl_title_mainidea_001, vecl_title_keyword_002, vecl_title_readability_003, vecl_title_option_elimination_022, vr_mi_title_total_001, vr_mi_title_keyword_001 | 6 张卡 |
| 下文推断 | ✅ | vecl_next_* 系列 | 5 张卡：尾句新信息、话题结束、问题对策、文末对策、已谈不再谈 + 干扰项 |
| 语句填入 | ✅ | vecl_insert_* 系列 | 5 张卡：整体首句、关键词覆盖、话题一致、总结句、主语语法指代 + 横线位置 |
| 语句排序 | ✅ | vecl_order_* 系列 | 7 张卡：整体结构、首句判断、尾句判断、转折捆绑、代词指代、尾首相连、时间逻辑 + 并列捆绑 |
| 逻辑填空 | ✅ 20 | vecl_cloze_* 系列 | 覆盖完整：总流程、成语辨析、实词辨析、逻辑对应、语境还原、转折/递进/并列提示、固定搭配、程度轻重、感情色彩、语法、语体、政治语境、关联词、多空题策略 |
| 词语辨析 | ✅ | vecl_cloze_idiom_context_002, vecl_cloze_realword_morpheme_003 | 成语辨析 + 实词辨析 |
| 成语辨析 | ✅ | vecl_cloze_idiom_context_002, vecl_cloze_idiom_misread_018 | 含望文生义防错 |
| 实词辨析 | ✅ | vecl_cloze_realword_morpheme_003, vecl_cloze_common_words_016 | 含实词积累 |
| 关联词填空 | ✅ | vecl_cloze_relation_word_021 | 关联词语义约束法 |
| 细节理解 | Not found in current cards. | | |
| 态度观点 | Not found in current cards. | | |
| 语义衔接 | ✅ | vecl_insert_topic_consistency_003, vecl_insert_summary_004 | 话题一致、概括得当 |
| 文段结构 | ✅ | vr_mi_* 结构类卡片 | 转折、递进、因果、必要条件、总分/分总、并列、二层、背景-新发现 |
| 转折关系 | ✅ | vr_mi_turning_point_001, vecl_cloze_transition_007, vecl_order_binding_transition_004 | 主旨+填空+排序 |
| 递进关系 | ✅ | vr_mi_progression_001, vecl_cloze_progressive_008 | 主旨+填空 |
| 因果关系 | ✅ | vr_mi_causality_001 | 主旨 |
| 并列关系 | ✅ | vr_mi_parallel_001, vecl_cloze_parallel_009, vecl_order_pair_binding_020 | 主旨+填空+排序 |
| 对策句 | ✅ | vr_mi_problem_solution_001, vecl_next_problem_solution_003, vecl_next_specific_solution_004 | 主旨+下文推断 |
| 问题-对策结构 | ✅ | vr_mi_problem_solution_001 | 主旨 |
| 观点-解释结构 | ✅ | vr_mi_view_explain_001 | 主旨 |
| 背景-观点结构 | ✅ | vr_mi_background_new_discovery_001 | 背景-新发现 |
| 总分/分总/总分总结构 | ✅ | vr_mi_total_part_001 | 总分/分总 |
| 干扰项识别 | ✅ | vr_mi_eliminate_* 系列 (9 张) + vecl_title_option_elimination_022 + vecl_next_option_elimination_023 | 覆盖完整 |
| 语境搭配 | ✅ | vecl_cloze_as_writer_006, vecl_cloze_fixed_collocation_010, vecl_cloze_collocation_bank_017 | 语境还原+固定搭配+搭配积累 |
| 感情色彩 | ✅ | vecl_cloze_sentiment_012 | 褒贬色彩匹配 |
| 语义轻重 | ✅ | vecl_cloze_degree_011 | 程度轻重匹配 |
| 其他 | ✅ | vecl_cloze_style_metaphor_014, vecl_cloze_political_context_015, vecl_cloze_grammar_013 | 语体与比喻、政治语境、语法正确 |

## 5. Method coverage

| Method | Found | Related cards | Solver relevance | Scaffold relevance |
|--------|-------|---------------|-----------------|-------------------|
| 主题句定位 | ✅ | vr_mi_topic_sentence_001 | 低 | 高 |
| 关联词分析 | ✅ | vecl_cloze_relation_word_021, vecl_cloze_transition_007, vecl_cloze_progressive_008, vecl_cloze_parallel_009 | 低 | 高 |
| 转折关系 | ✅ | vr_mi_turning_point_001, vecl_cloze_transition_007, vecl_order_binding_transition_004 | 低 | 高 |
| 递进关系 | ✅ | vr_mi_progression_001, vecl_cloze_progressive_008 | 低 | 高 |
| 因果关系 | ✅ | vr_mi_causality_001 | 低 | 高 |
| 对策句 | ✅ | vr_mi_problem_solution_001, vecl_next_problem_solution_003 | 低 | 高 |
| 总分结构 | ✅ | vr_mi_total_part_001 | 低 | 高 |
| 干扰项排除 | ✅ | vr_mi_eliminate_* 系列 (9 张) + vecl_title_option_elimination_022 + vecl_next_option_elimination_023 | 低 | 高 |
| 语境搭配 | ✅ | vecl_cloze_as_writer_006, vecl_cloze_fixed_collocation_010 | 低 | 高 |
| 感情色彩 | ✅ | vecl_cloze_sentiment_012 | 低 | 高 |
| 语义轻重 | ✅ | vecl_cloze_degree_011 | 低 | 高 |
| 衔接连贯 | ✅ | vecl_insert_topic_consistency_003, vecl_insert_summary_004 | 低 | 高 |
| 排序线索 | ✅ | vecl_order_* 系列 (7 张) | 中 | 高 |
| 代词指代 | ✅ | vecl_order_pronoun_005, vecl_insert_pronoun_grammar_005 | 中 | 高 |
| 时间逻辑顺序 | ✅ | vecl_order_time_logic_007 | 中 | 高 |
| 主体词覆盖 | ✅ | vr_mi_subject_word_001, vecl_title_keyword_002 | 低 | 高 |
| 语体与比喻 | ✅ | vecl_cloze_style_metaphor_014 | 低 | 高 |
| 政治语境 | ✅ | vecl_cloze_political_context_015 | 低 | 高 |

## 6. Feasibility grading

| Category | Grade | Reason | Suggested route |
|----------|-------|--------|----------------|
| 语句排序 | B_scaffold_first_solver_later | 有明确线索（首句判断、转折捆绑、代词指代、尾首相连、时间逻辑），但需语义理解辅助 | scaffold → 局部辅助规则 |
| 语句填入 | B_scaffold_first_solver_later | 横线位置功能明确，但需整体文意判断 | scaffold → 局部辅助规则 |
| 标题填入 | B_scaffold_first_solver_later | 有关键词覆盖和可读性方法，但需语义判断 | scaffold → 局部辅助规则 |
| 下文推断 | B_scaffold_first_solver_later | 尾句新信息、话题结束等方法明确，但需语义判断 | scaffold → 局部辅助规则 |
| 主旨意图 | C_scaffold_only | 依赖强语义理解，转折/递进/因果等虽有规则但机械选易误伤 | scaffold only |
| 中心理解 | C_scaffold_only | 需整体文意判断 | scaffold only |
| 逻辑填空 | C_scaffold_only | 语境搭配、感情色彩、成语辨析高度依赖语义和语感 | scaffold only |
| 成语辨析 | C_scaffold_only | 需要语义积累和语感 | scaffold only |
| 实词辨析 | C_scaffold_only | 需要语义积累和语感 | scaffold only |
| 干扰项识别 | C_scaffold_only | 9 种干扰项类型需语义判断 | scaffold only |
| 态度观点 | D_defer | 当前无卡片覆盖 | defer |
| 细节理解 | D_defer | 当前无卡片覆盖 | defer |

## 7. Recommended scaffold scope

verbal_reasoning_scaffold 应包含：

- stage_order
- question_type_router
- discourse_structure_checklists
- cloze_context_checklists
- sentence_expression_checklists
- option_verification
- response_template
- uncertainty_policy
- must_not_do

## 8. Future user-provided real-case audit principle

**本阶段不制作真题包。**

未来如果需要言语理解真题测试包，必须满足：

- 真题来源由用户提供
- 题干、选项、标准答案必须来自已核验资料
- 不能由 Claude / Codex 杜撰
- 不能联网搜索题目
- 不能把标准答案写进 solver/scaffold 规则
- 不能根据 case_id、题号、文件名、答案位置写规则
- 测试包建议放在 `text-image/verbal_reasoning_real_cases_verified_v1/` 这类本地目录
- 测试包默认保持 untracked，不直接提交 git
- 审计脚本只用于计算 correct / wrong / null / analysis_only
- wrong = 0 优先于 correct 数量
- 不唯一必须 analysis_only

## 9. Risks

- 语义理解风险：言语理解高度依赖自然语言理解，纯规则难以覆盖
- 关键词机械匹配风险：只看关键词可能误判主旨
- 只看转折词误判风险：转折后不一定总是重点
- 逻辑填空语境误判风险：语境搭配需要语感和积累
- 成语/实词辨析需要语义和语感：无法纯规则覆盖
- 缺少用户提供真题回归包风险：无法验证 wrong=0

## 10. Boundary

确认：

- no solver added
- no scaffold added
- no MCP/CLI integration
- no knowledge base modification
- no real-case package created
- no external LLM/API
- no OCR/OpenCV/PIL/ML dependency

## 11. Recommendation

**优先做 verbal_reasoning_scaffold v0.1 isolated。**

不建议直接做强规则 solver。言语理解 77 张卡片覆盖 3 个子模块，但所有题型都依赖深层语义理解，A_solver_first 可以为空。即使是 B 类的语句排序/填入/标题/下文推断，也需要 scaffold 先约束大模型，后续只能做局部辅助规则（如首句判断、转折捆绑），不能直接自动选答案。
