# 类比推理 v1 设计文档

## 1. 目标

实现行测"判断推理 → 类比推理"题型的独立规则 solver，遵循项目核心原则：
- 纯规则 + 可解释推理
- 不引入机器学习
- 不唯一则 analysis_only
- 不根据答案写规则

## 2. 与其它题型的边界

| 题型 | 入口 | 核心 |
|------|------|------|
| 逻辑判断 | solve_logic_reasoning | 论证类/翻译推理/真假推理/分析推理 |
| 定义判断 | definition_judgement.py (isolated) | 定义匹配 |
| 分析推理 | logic_analysis_reasoning.py (isolated) | 朴素逻辑/排序/分组 |
| **类比推理** | **analogy_reasoning.py (isolated)** | **词组关系类比** |

类比推理与逻辑判断无交集。类比推理关注词语间的结构/语义关系，不涉及命题逻辑。

## 3. v1.0-v1.1 范围

- 仅做 isolated core，不接入 solve_logic_reasoning
- 不改 CLI/MCP
- 不新增 MCP tool
- 不新增 CLI 命令

## 4. 词组解析设计

支持的题干格式：
- 二词型：`A∶B` / `A:B` / `A：B`
- 三词型：`A∶B∶C`
- 填空型：`A 对于（ ）相当于（ ）对于 B`
- 四字成语型：`ABCD∶EFGH`

支持的选项格式：
- `A. X∶Y`
- `A. X∶Y∶Z`
- `X；Y`（填空型）

## 5. 关系类型设计

支持 18 种通用关系类型：

| 关系类型 | 说明 | 检测方式 |
|---------|------|---------|
| opposite | 反义 | 通用反义词对集合 |
| same_category | 并列/同类 | 类别词匹配 |
| synonym | 近义 | 近义指示词 |
| species_genus | 种属 | 类别词+实例 |
| whole_part | 整体-部分 | 部分指示词 |
| material_product | 材料-成品 | 材料词素+制品词素 |
| tool_function | 工具-用途 | 工具词+功能词 |
| profession_object | 职业-对象 | 职业词+对象词 |
| place_function | 地点-功能 | 地点词+功能词 |
| cause_effect | 因果 | 因果指示词 |
| process_result | 过程-结果 | 过程词+结果词 |
| sequence | 顺承 | 时间顺序词 |
| degree | 程度递进 | 程度词 |
| purpose | 目的 | 目的指示词+四字结构 |
| grammar_structure | 语法结构 | 字符重叠 |
| cross_relation | 交叉关系 | 类别交叉 |
| naming_convention | 命名方式 | 材料/功能/形状命名 |
| aggregation | 汇总关系 | 汇总指示词 |

所有词典均为通用类别词，不含具体真题答案词。

## 6. Option Matching 设计

1. 对题干检测所有关系 hypotheses
2. 对每个选项检测所有关系 hypotheses
3. 比较关系类型、方向、结构兼容性
4. 打分排序

决策规则（保守策略）：
- 仅当 top score > 阈值 且 明显优于第二 且 无混合关系 且 无弱关系 → solved
- 三词型额外加 +0.2 阈值惩罚
- 仅含 sequence/degree/grammar_structure → 不预测
- 其它情况 → ambiguous 或 analysis_only

## 7. 12 道真题审计结果

### v1.0

| 指标 | 值 |
|------|-----|
| Total | 12 |
| Solved | 4 |
| Ambiguous | 3 |
| Analysis_only | 5 |
| Correct | 2 |
| Wrong | 2 |

### v1.1

| 指标 | 值 |
|------|-----|
| Total | 12 |
| Solved | 0 |
| Ambiguous | 6 |
| Analysis_only | 6 |
| Correct | 0 |
| Wrong | 0 |

### v1.0 → v1.1 变化原因

- v1.0 有 2 wrong，违反 wrong=0 硬约束
- v1.1 收紧决策规则：提高三词型阈值、过滤弱关系预测、移除具体真题词
- correct 从 2 降至 0 是为了保证 wrong=0

### v1.3 (Conservative Recovery)

| 指标 | 值 |
|------|-----|
| Total | 12 |
| Solved | 2 |
| Ambiguous | 5 |
| Analysis_only | 5 |
| Correct | 2 |
| Wrong | 0 |

v1.2-v1.3 conservative recovery 策略：

1. **只恢复安全关系**：`material_product` 和 `naming_convention` 是仅允许的安全关系
2. **严格阈值**：top_score >= 0.75, score_gap >= 0.25
3. **排除三词型**：三词型和填空型保持保守
4. **改进材料检测**：增加"原X"→"加工X"通用模式（原前缀 vs 无前缀），不使用具体真题词
5. **移除弱关系预测**：sequence/degree/grammar_structure/purpose/cause_effect 单独出现时不预测

v1.0 的 2 wrong 处理：
- analog_006 (sequence only, three-word): 保持 ambiguous
- analog_011 (mixed relations, four-char): 保持 ambiguous

## 8. 当前 correct/wrong/null

- correct = 2
- wrong = 0
- null = 10

## 9. 是否建议进入 v1.5 integration

**暂不建议。** 当前 correct=2，尚未达到 correct >= 3 的 integration gate。

## 10. 后续计划

1. 扩充/清洗类比推理题包：更多 material_product / naming_convention 类题可能直接提升 correct
2. 改进三词型结构分析（analog_005-008）
3. 改进填空型解析（analog_009-010）
4. 改进四字成语关系检测（analog_011）
5. 达到 correct >= 3 + wrong = 0 后再考虑保守接入

## 11. v1.4 (Aggregation Recovery Attempt)

v1.4 尝试恢复 analog_002（小计∶总计，答案 D）。

诊断结果：**无法安全恢复。**

原因：所有 4 个选项都检测到完全相同的 aggregation 关系（confidence=0.70, score=1.050）。正确答案 D 与错误选项 A/B/C 的区别在于 "可加总" vs "不可加总"，这需要领域知识，无法用通用 aggregation 规则表达。

v1.4 与 v1.3 结果完全相同：correct=2, wrong=0。

## 12. v1.5 (Strong-Relation Package Audit)

v1.5 用当前 v1.4 core 直接审计第二批强关系题包（12 题），不修改 solver。

### 第二批题包路径

```
text-image/analogy_reasoning_strong_relations_open_verified_v2/questions_manifest.json
```

### 第二批 audit 结果

| 指标 | 值 |
|------|-----|
| Total | 12 |
| Solved | 0 |
| Ambiguous | 4 |
| Analysis_only | 8 |
| Correct | 0 |
| Wrong | 0 |

### 第一批 vs 第二批对比

| 指标 | 第一批 (v1.4) | 第二批 (v1.5) |
|------|---------------|---------------|
| Correct | 2 | 0 |
| Wrong | 0 | 0 |
| Solved | 2 | 0 |

### 为什么第二批 correct=0

第二批以三词型（8/12）和语义关系为主，当前 core 缺少：
- tool_function / profession_object 不在 SAFE_RELATION_TYPES
- species_genus 检测器不够精确
- 缺少 action_compound、necessary_attribute、state_progression 等检测器

### 是否达到 integration gate

**否。** 未达到 correct >= 4, wrong = 0。

### 下一步建议

1. 将 tool_function, profession_object 加入 SAFE_RELATION_TYPES（需验证不引入 wrong）
2. 改进 species_genus 检测器
3. 考虑暂停类比推理，转入其他题型
