# 数量关系 source audit 与工程化清洗报告

## 输入文件
- 【花生十三】数量思维导图.pdf: 8页，文本可解析，作为全量题型体系和公式的主来源。
- 花生数量关系笔记.pdf: 渲染为35页，扫描页无法解析文本，采用页面图像进行视觉抽取；第35页为空白，不作为来源。

## 输出文件
- quantity_relation_cards_audited.jsonl
- quantity_relation_methods_audited.md
- quantity_relation_router_rules_audited.yaml
- quantity_relation_uncertain_items_audited.md
- quantity_relation_source_audit_report.md

## source audit 结论
- 共生成 65 张方法卡片。
- 每张卡片均包含 source_file 与 source_page；同一方法在思维导图和笔记中均出现时已合并并保留双来源。
- 不新增 PDF 中没有依据的方法；笔记中未展开或仅为目录页的内容不单独生成卡片。
- 扫描笔记的工程化字段来自题型方法本身，不引入外部资料。

## 页面来源索引
### 思维导图 PDF
- p1: 排列组合和概率问题
- p2: 几何问题
- p3: 行程问题
- p4: 最值问题
- p5: 工程、经济利润、统筹规划
- p6: 容斥、浓度、周期循环、日期星期、年龄
- p7: 数列、约数倍数、平均数、余数、计算
- p8: 不定方程、鸡兔、盈亏、牛吃草、比赛、植树、钟表、方阵
### 笔记 PDF
- p4-p5: 数论、公式、整除、余数特性
- p7: 和差倍比、不定方程、方程法
- p9: 浓度与十字相乘
- p11: 牛吃草与容斥
- p13: 周期循环、日期星期
- p15: 工程问题
- p17: 利润问题
- p19: 最值问题
- p21-p24: 排列组合与概率
- p26-p27: 鸡兔、盈亏、年龄、方阵、植树、钟表、比赛、天平
- p29: 几何问题
- p31-p32: 行程问题
- p34: 数字推理

## 工程化清洗说明
- 已为所有卡片补充 required_inputs、calculation_policy、solver_priority、output_constraints。
- solver_priority 数值越小越优先；公式直接型和高频模型优先，了解型或边界复杂模型靠后。
- router_rules 中所有 priority_method_id 与 backup_method_id 均在 cards 中存在。
- qr_calculation_formula_001 和 qr_balance_weighing_001 因扫描公式/口诀边界不确定，need_review=true。
