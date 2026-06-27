# Quantity Relation v0.1 Scope Audit

## 1. Baseline

- HEAD: `3ba360e`
- tag: `stable-mcp-guidance-tools-3ba360e`
- git status: 4 untracked text-image directories + 1 new output file
- test baseline: 314 passed (full suite)

## 2. Audit scope

本次只做数量关系知识卡审计和路线规划：

- no solver added
- no scaffold added
- no MCP/CLI integration
- no real-case package created
- no web search
- no OCR
- no fabricated questions

## 3. Knowledge card inventory summary

- quantity_relation card count: 65
- source files checked: knowledge_base/all_cards.jsonl, knowledge_base/module_originals/quantity_relation/
- field availability: 全部 65 张卡片字段完整（id, module, question_type, sub_type, method_name, tags, trigger_conditions, anti_conditions, required_inputs, reasoning_policy, calculation_policy, solver_priority, steps, formulas, examples, pitfalls, forbidden, output_constraints, source_file, source_page, confidence, need_review, source_zip）
- parsing limitations: 无，JSONL 格式完整解析

## 4. Category coverage

| Category | Found | Related card titles/method_ids | Notes |
|----------|-------|-------------------------------|-------|
| 工程问题 | ✅ 2 | qr_work_basic_001, qr_work_rest_001 | 高 confidence，适合 solver-first |
| 行程问题 | ✅ 8 | qr_travel_basic_001, qr_meeting_chasing_001, qr_multiple_meeting_001, qr_circular_motion_001, qr_stream_boat_001, qr_escalator_001, qr_train_bridge_001, qr_team_marching_001 | 题型丰富，基础行程可 solver，变形需 scaffold |
| 经济利润问题 | ✅ 3 | qr_profit_basic_001, qr_profit_batch_001, qr_profit_fund_flow_001 | 高 confidence，适合 solver-first |
| 浓度/溶液混合问题 | ✅ 2 | qr_concentration_basic_001, qr_alligation_001 | 公式明确，可 solver-first |
| 比例/倍数问题 | ✅ 2 | qr_number_property_001, qr_average_number_001 | 基础方法，适合 scaffold |
| 年龄问题 | ✅ 1 | qr_age_problem_001 | 单卡，需 scaffold 补充 |
| 容斥/集合问题 | ✅ 2 | qr_inclusion_exclusion_001, qr_inclusion_exclusion_extreme_001 | 基础容斥可 solver，最值需 scaffold |
| 排列组合 | ✅ 9 | qr_perm_comb_basic_001, qr_adjacent_bundle_001, qr_nonadjacent_insert_001, qr_fixed_order_001, qr_same_elements_distribution_001, qr_average_grouping_001, qr_derangement_001, qr_circular_permutation_001, qr_repeated_permutation_001 | 卡片最多，但自然语言建模复杂，scaffold-first |
| 概率问题 | ✅ 5 | qr_probability_basic_001, qr_geometric_probability_001, qr_two_person_same_group_001, qr_lottery_probability_001, qr_match_probability_order_001 | 依赖排列组合，scaffold-first |
| 几何问题 | ✅ 5 | qr_geometry_formula_001, qr_geometry_scaling_001, qr_geometry_extreme_001, qr_shortest_distance_001, qr_one_stroke_001 | 公式可 solver，最值/构造需 scaffold |
| 数列问题 | ✅ 1 | qr_sequence_formula_001 | 基础数列公式可 solver |
| 方程/不定方程 | ✅ 2 | qr_equation_method_001, qr_indeterminate_equation_001 | 方程法可 solver，不定方程需 scaffold |
| 最值问题 | ✅ 5 | qr_extreme_sum_fixed_001, qr_extreme_unfavorable_001, qr_extreme_function_001, qr_extreme_product_001, qr_extreme_three_end_001 | 构造性强，scaffold-first |
| 牛吃草 | ✅ 1 | qr_cow_grazing_001 | 公式明确，可 solver-first |
| 鸡兔同笼 | ✅ 1 | qr_chicken_rabbit_001 | 公式明确，可 solver-first |
| 日期星期问题 | ✅ 1 | qr_date_week_001 | 单卡，可 solver-first |
| 抽屉原理 | Not found in current cards. | | |
| 统筹优化 | ✅ 4 | qr_planning_optimal_001, qr_time_planning_001, qr_balance_weighing_001, qr_bottle_exchange_001 | 统筹性强，scaffold-first |
| 数论与计算 | ✅ 2 | qr_calculation_formula_001, qr_number_property_001 | 基础方法，适合 scaffold |
| 余数问题 | ✅ 2 | qr_remainder_formula_001, qr_remainder_enum_001 | 公式明确，可 solver-first |
| 特殊情景应用 | ✅ 6 | qr_chicken_rabbit_001, qr_surplus_deficit_001, qr_square_array_001, qr_tree_planting_001, qr_tree_overlap_001, qr_clock_problem_001 | 多数有明确公式，可 solver-first |
| 比赛问题 | ✅ 1 | qr_competition_schedule_001 | 单卡，可 solver-first |

## 5. Method coverage

| Method | Found | Related cards | Solver relevance | Scaffold relevance |
|--------|-------|---------------|-----------------|-------------------|
| 代入排除 | ✅ | qr_number_property_001, qr_indeterminate_equation_001 | 高 | 中 |
| 特值法 | ✅ | qr_work_basic_001, qr_profit_basic_001 | 高 | 中 |
| 方程法 | ✅ | qr_equation_method_001, qr_profit_batch_001 | 高 | 低 |
| 赋值法 | ✅ | qr_work_basic_001 | 高 | 低 |
| 枚举法 | ✅ | qr_remainder_enum_001, qr_indeterminate_equation_001 | 中 | 高 |
| 十字交叉法 | ✅ | qr_alligation_001, qr_extreme_product_001 | 高 | 中 |
| 比例法 | ✅ | qr_travel_basic_001, qr_meeting_chasing_001, qr_average_number_001 | 高 | 中 |
| 图表辅助 | ✅ | qr_inclusion_exclusion_001, qr_geometry_formula_001 | 中 | 高 |
| 公式/口诀 | ✅ | 12 cards | 高 | 低 |
| 模型/套路 | ✅ | 13 cards | 中 | 高 |
| 构造/极端 | ✅ | 7 cards | 低 | 高 |
| 统筹 | ✅ | 2 cards | 低 | 高 |

## 6. Feasibility grading

| Category | Grade | Reason | Suggested route |
|----------|-------|--------|----------------|
| 工程问题 | A_solver_first | 公式明确（W=E*T），赋值法成熟，2 张高 confidence 卡 | solver |
| 经济利润问题 | A_solver_first | 基础公式清晰，3 张卡覆盖单件/分批/资金 | solver |
| 鸡兔同笼 | A_solver_first | 理论最大值与实际值差值公式明确 | solver |
| 盈亏问题 | A_solver_first | 盈数亏数除以分配标准差公式明确 | solver |
| 日期星期问题 | A_solver_first | 粗算修正日期差法，单卡但公式明确 | solver |
| 余数问题（特征） | A_solver_first | 余同取余/和同加和/差同减差口诀明确 | solver |
| 植树问题 | A_solver_first | 两端/一端/环形/两端不植树公式明确 | solver |
| 浓度/溶液混合问题 | A_solver_first | 溶质守恒 + 十字相乘，公式明确 | solver |
| 比赛问题 | A_solver_first | 循环赛/淘汰赛/轮空规则明确 | solver |
| 方阵问题 | A_solver_first | 最外层边长平方与层人数公式明确 | solver |
| 数列问题 | A_solver_first | 等差/等比/递推公式明确 | solver |
| 牛吃草 | A_solver_first | 白吃牛与干活牛三步法明确 | solver |
| 行程问题（基础） | B_scaffold_first_solver_later | 基础行程公式明确，但变形题多（8 子类型） | scaffold → solver |
| 容斥问题 | B_scaffold_first_solver_later | 一般容斥可 solver，最值容斥需 scaffold | scaffold → solver |
| 数论与计算 | B_scaffold_first_solver_later | 代数公式可 solver，尾数法需 scaffold 补充判断 | scaffold → solver |
| 不定方程 | B_scaffold_first_solver_later | 奇偶/整除/代入策略需 scaffold 引导 | scaffold → solver |
| 排列组合 | C_scaffold_only | 9 张卡覆盖广，但自然语言建模复杂，公式虽明确但组合爆炸风险高 | scaffold only |
| 概率问题 | C_scaffold_only | 依赖排列组合，几何概型需图形理解 | scaffold only |
| 最值问题 | C_scaffold_only | 构造性强，需 scaffold 引导极端思维 | scaffold only |
| 统筹优化 | C_scaffold_only | 策略性强，需 scaffold 引导统筹思维 | scaffold only |
| 几何问题（最值/构造） | C_scaffold_only | 几何最值和一笔画需 scaffold 引导 | scaffold only |
| 年龄问题 | C_scaffold_only | 单卡，需 scaffold 补充题型覆盖 | scaffold only |
| 抽屉原理 | D_defer | 当前无卡片覆盖 | defer |

## 7. Recommended first solver targets

### 1. 工程问题（qr_work_basic_001, qr_work_rest_001）

- why suitable: 公式 W=E*T 明确，赋值法成熟，2 张高 confidence 卡（0.96, 0.92）
- expected input_features: question_text 中出现"工作总量"、"效率"、"时间"、"合作"、"交替"
- safe solving strategy: 赋值法（设总量为效率公倍数）→ 列方程 → 求解
- analysis_only conditions: 效率变化规则不明确、多人交替工作模式复杂、约束不足

### 2. 经济利润问题（qr_profit_basic_001, qr_profit_batch_001, qr_profit_fund_flow_001）

- why suitable: 基础公式清晰（利润率=（售价-成本）/成本），3 张卡覆盖主要场景
- expected input_features: question_text 中出现"成本"、"售价"、"利润"、"折扣"、"利润率"
- safe solving strategy: 列成本/售价/利润方程 → 求解
- analysis_only conditions: 多批销售条件复杂、资金往来路径不明确

### 3. 鸡兔同笼（qr_chicken_rabbit_001）

- why suitable: 理论最大值与实际值差值公式明确，单卡但公式简单
- expected input_features: question_text 中出现"鸡兔同笼"或隐含头脚关系
- safe solving strategy: 假设全为一种 → 计算差值 → 求解
- analysis_only conditions: 多于两种动物、约束不足

### 4. 余数问题-特征余数（qr_remainder_formula_001）

- why suitable: 余同取余/和同加和/差同减差口诀明确，confidence=0.94
- expected input_features: question_text 中出现"除以A余B"多个条件
- safe solving_strategy: 判断口诀特征 → 求 LCM → 写表达式 → 代入选项
- analysis_only conditions: 不满足口诀特征（需转枚举）、范围条件不足

### 5. 浓度/溶液混合问题（qr_concentration_basic_001, qr_alligation_001）

- why suitable: 溶质守恒 + 十字相乘公式明确，2 张高 confidence 卡（0.94, 0.95）
- expected input_features: question_text 中出现"浓度"、"溶质"、"溶液"、"混合"
- safe solving_strategy: 溶质守恒列方程 或 十字相乘求比例
- analysis_only conditions: 多次混合条件复杂、浓度变化规则不明确

## 8. Recommended scaffold scope

数量关系 scaffold 应包含：

- 题型识别（22 种题型路由）
- 已知量/未知量抽取
- 单位统一
- 变量设定
- 方程/比例/枚举/代入策略选择
- 选项代入验证
- 估算与量级检查
- 唯一性判断
- analysis_only 触发条件
- must_not_do 禁止事项

## 9. Future user-provided real-case audit principle

**本阶段不制作真题包。**

未来如果需要数量关系真题测试包，必须满足：

- 真题来源由用户提供
- 题干、选项、标准答案必须来自已核验资料
- 不能由 Claude / Codex 杜撰
- 不能联网搜索题目
- 不能把标准答案写进 solver 规则
- 不能根据 case_id、题号、文件名、答案位置写规则
- 测试包建议放在 `text-image/quantity_relation_real_cases_verified_v1/` 这类本地目录
- 测试包默认保持 untracked，不直接提交 git
- 审计脚本只用于计算 correct / wrong / null / analysis_only
- wrong = 0 优先于 correct 数量
- 不唯一必须 analysis_only

## 10. Risks

- 数量关系自然语言抽取风险：题干中的数学关系可能用多种自然语言表达，抽取不完整会导致建模错误
- 单位换算风险：题目可能涉及不同单位（小时/分钟、米/千米），遗漏换算会导致计算错误
- 公式误套风险：相似题型可能适用不同公式（如行程问题的多种变形），误套会导致 wrong
- 选项代入误判风险：代入验证时可能因计算错误误判选项正误
- 缺少用户提供真题回归包风险：无法在真实题目上验证 solver 的 wrong=0 约束

## 11. Boundary

确认：

- no solver added
- no scaffold added
- no MCP/CLI integration
- no knowledge base modification
- no real-case package created
- no external LLM/API
- no OCR/OpenCV/PIL/ML dependency

## 12. Recommendation

**优先做 quantity_relation_scaffold v0.1 isolated。**

理由：

1. 65 张卡片覆盖 22 种题型，但大部分题型需要自然语言理解和数学建模能力，纯规则 solver 难以覆盖。
2. scaffold 可以为所有题型提供统一的思考框架（题型识别 → 量抽取 → 策略选择 → 选项验证），降低后续 solver 开发风险。
3. 即使是 A_solver_first 的题型（工程、利润、鸡兔同笼等），也需要 scaffold 提供 analysis_only 约束，避免强行输出错误答案。
4. 排列组合（9 卡）和概率（5 卡）占比最大但最适合 scaffold-first，先做 scaffold 可以覆盖这些高频题型的方法论。
5. scaffold 完成后，可以针对 A_solver_first 的 12 种题型做 isolated small solver，逐步扩大覆盖。
