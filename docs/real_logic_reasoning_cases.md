# 逻辑判断真实题测试记录

## 当前版本

- solver: `solve_logic_reasoning`
- current_stage: v2 calibration
- previous_stage: v1 MVP
- 状态：真实题校准中
- 当前边界：论证类题目结构化分析，不强行自动给答案

## 测试题型比例建议

- 削弱题：6 道
- 加强题：6 道
- 前提假设题：5 道
- 解释说明题：5 道
- 结论推出题：5 道

## 单题记录模板

```text
case_id:
source:
sub_type_expected:
standard_answer:
solver_version:
test_date:

题干：

选项：

调用命令：

Solver 输出摘要：

人工评估：

错误类型：

备注：
```

## 错误类型

- 无明显错误
- 题型识别错误
- 选非方向识别不足
- 论点抽取错误
- 论据抽取错误
- 论证缺口判断过泛
- 选项解析错误
- 选项力度排序错误
- 标准答案选项未突出
- answer_candidate 过度保守
- answer_candidate 错误
- method_id 召回不准
- 解释文本不符合考场思路
- 异常样本

## 填写建议

- 先记录 solver 原始输出摘要，再写人工评估。
- v2 阶段不要求自动给出 `answer_candidate`。
- 如果题目需要翻译推理、真假推理或分析推理，先记录为当前阶段范围外，不急于修。
- 只有重复出现的通用缺口才进入 v3 规则增强候选。

# 第一批真实题图片清单：LR-001 ~ LR-010

## LR-001

```yaml
case_id: LR-001
image_file: text-image/logic_reasoning_real_cases_10_images/LR-001_weaken_other_cause_or_scheme_failure.png
status: evaluated_v2_draft
sub_type_expected: 削弱题
topic_hint: 方案无效 / 可绕过
standard_answer: D
core_judgment: 攻击者能识别并忽略“良性漏洞”，直接削弱方案有效性
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
某网络安全团队提出一种新方案：在软件系统中主动加入大量“良性漏洞”，让攻击者在扫描时被大量无害信息干扰，从而减少真正危险漏洞被利用的概率。研究人员据此认为，这种方案可以显著提高系统安全性。

以下哪项如果为真，最能削弱上述观点？
```

### 选项

```text
A. 添加良性漏洞需要额外的开发与维护成本。
B. 不同类型的软件系统对安全防护的需求并不相同。
C. 有些企业在部署新系统前会进行第三方安全评估。
D. 经验丰富的攻击者通常能够快速识别并忽略良性漏洞，继续针对真正危险的漏洞发起攻击。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-001.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 削弱 / 削弱/质疑
answer_candidate: null
needs_more_data: false
standard_answer: D
core_judgment: 攻击者能识别并忽略“良性漏洞”，直接削弱方案有效性
source_method_ids:
  - lj_weaken_evidence_conclusion_001
  - lj_attribution_general_001
  - lj_weaken_alternative_cause_001
  - lj_weaken_reverse_causation_001
  - lj_strength_order_compare_001
recommended_methods:
  - method_id: lj_weaken_evidence_conclusion_001
    method_name: 肯定论据否定结论法
    reason: 优先方法
  - method_id: lj_attribution_general_001
    method_name: 归因论证识别与攻击总法
    reason: 辅助比较或备选方法
  - method_id: lj_weaken_alternative_cause_001
    method_name: 另有他因削弱法
    reason: 辅助比较或备选方法
  - method_id: lj_weaken_reverse_causation_001
    method_name: 因果倒置削弱法
    reason: 辅助比较或备选方法
  - method_id: lj_strength_order_compare_001
    method_name: 加强/削弱力度比较通用规则
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 这种方案可以显著提高系统安全性
premises:
  - 某网络安全团队提出一种新方案：在软件系统中主动加入大量“良性漏洞”，让攻击者在扫描时被大量无害信息干扰，从而减少真正危险漏洞被利用的概率
  - 研究人员据此
reasoning_chain: 某网络安全团队提出一种新方案：在软件系统中主动加入大量“良性漏洞”，让攻击者在扫描时被大量无害信息干扰，从而减少真正危险漏洞被利用的概率；研究人员据此 -> 这种方案可以显著提高系统安全性
gap: 题干可能从相关事实推到因果或效果结论，需核对是否存在他因、倒因或桥梁缺失。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 需进一步比较削弱力度
    strength_level: medium_or_strong
    is_candidate: false
    reason: 可能补充必要条件；需按论点、论据、论证桥梁做力度比较。
  B:
    effect: 需进一步比较削弱力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  C:
    effect: 需进一步比较削弱力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  D:
    effect: 需进一步比较削弱力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: true
argument_structure_correct: true
option_analysis_correct: false
method_recall_correct: true
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 题型、论点和核心方法召回正确；但标准答案 D 未被突出，A 被误判为可能较强。
```

### 错误类型

```text
选项力度排序错误；标准答案选项未突出
```

### 备注

```text
无。
```

## LR-002

```yaml
case_id: LR-002
image_file: text-image/logic_reasoning_real_cases_10_images/LR-002_weaken_child_food.png
status: evaluated_v2_draft
sub_type_expected: 削弱题 / 质疑题
topic_hint: 儿童食品
standard_answer: A
core_judgment: 直接否定“儿童食品更营养健康”的核心观点
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
某机构宣传称，市场上标注为“儿童食品”的产品比普通食品更适合儿童，也更营养健康。因此，家长在为孩子挑选食品时，应优先购买儿童食品。

以下哪项如果为真，最能质疑上述观点？
```

### 选项

```text
A. 多项检测显示，不少所谓儿童食品在营养成分上与普通同类食品差别并不明显，部分产品甚至糖和盐含量更高。
B. 儿童食品的外包装通常更加鲜艳，更容易吸引孩子注意。
C. 一些家长购买儿童食品时会更关注品牌知名度。
D. 儿童食品在销售渠道上通常集中在大型商超和电商平台。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-002.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 削弱 / 削弱/质疑
answer_candidate: null
needs_more_data: false
standard_answer: A
core_judgment: 直接否定“儿童食品更营养健康”的核心观点
source_method_ids:
  - lj_weaken_evidence_conclusion_001
  - lj_attribution_general_001
  - lj_weaken_alternative_cause_001
  - lj_weaken_reverse_causation_001
  - lj_strength_order_compare_001
recommended_methods:
  - method_id: lj_weaken_evidence_conclusion_001
    method_name: 肯定论据否定结论法
    reason: 优先方法
  - method_id: lj_attribution_general_001
    method_name: 归因论证识别与攻击总法
    reason: 辅助比较或备选方法
  - method_id: lj_weaken_alternative_cause_001
    method_name: 另有他因削弱法
    reason: 辅助比较或备选方法
  - method_id: lj_weaken_reverse_causation_001
    method_name: 因果倒置削弱法
    reason: 辅助比较或备选方法
  - method_id: lj_strength_order_compare_001
    method_name: 加强/削弱力度比较通用规则
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 家长在为孩子挑选食品时，应优先购买儿童食品
premises:
  - 某机构宣传称，市场上标注为“儿童食品”的产品比普通食品更适合儿童，也更营养健康
reasoning_chain: 某机构宣传称，市场上标注为“儿童食品”的产品比普通食品更适合儿童，也更营养健康 -> 家长在为孩子挑选食品时，应优先购买儿童食品
gap: 需核对论据到论点之间是否存在主体、范围或因果桥梁缺口。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 需进一步比较削弱力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  B:
    effect: 需进一步比较削弱力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  C:
    effect: 需进一步比较削弱力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  D:
    effect: 需进一步比较削弱力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: true
argument_structure_correct: true
option_analysis_correct: false
method_recall_correct: true
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 能识别削弱/质疑和结论，但 A 对核心观点的直接否定未被识别出来。
```

### 错误类型

```text
选项力度排序错误；标准答案选项未突出
```

### 备注

```text
无。
```

## LR-003

```yaml
case_id: LR-003
image_file: text-image/logic_reasoning_real_cases_10_images/LR-003_strengthen_smell_degradation.png
status: evaluated_v2_draft
sub_type_expected: 加强题
topic_hint: 人类嗅觉退化
standard_answer: A
core_judgment: 补充现代人嗅觉相关脑区/基因退化证据，支持嗅觉退化
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
有研究者认为，人类的嗅觉能力在漫长进化过程中不断减弱，现代人的嗅觉已经明显不如远古时期敏锐。

以下哪项如果为真，最能支持上述观点？
```

### 选项

```text
A. 与远古人类相比，现代人负责气味识别和处理的某些相关脑区与基因功能出现了明显退化迹象。
B. 现代社会中，人们识别气味的场景远比古代更加多样化。
C. 一些哺乳动物的嗅觉能力明显强于现代人类。
D. 嗅觉在不同文化中的重要性存在较大差异。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-003.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 加强 / 支持加强
answer_candidate: null
needs_more_data: false
standard_answer: A
core_judgment: 补充现代人嗅觉相关脑区/基因退化证据，支持嗅觉退化
source_method_ids:
  - lj_support_general_001
  - lj_support_bridge_001
  - lj_support_add_evidence_001
  - lj_support_necessary_condition_001
  - lj_strength_order_compare_001
recommended_methods:
  - method_id: lj_support_general_001
    method_name: 支持题主体话题一致原则
    reason: 优先方法
  - method_id: lj_support_bridge_001
    method_name: 支持类断点搭桥法
    reason: 辅助比较或备选方法
  - method_id: lj_support_add_evidence_001
    method_name: 新增事实数据支持法
    reason: 辅助比较或备选方法
  - method_id: lj_support_necessary_condition_001
    method_name: 必要条件式支持法
    reason: 辅助比较或备选方法
  - method_id: lj_strength_order_compare_001
    method_name: 加强/削弱力度比较通用规则
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 人类的嗅觉能力在漫长进化过程中不断减弱，现代人的嗅觉已经明显不如远古时期敏锐
premises:
  - 有研究者
reasoning_chain: 有研究者 -> 人类的嗅觉能力在漫长进化过程中不断减弱，现代人的嗅觉已经明显不如远古时期敏锐
gap: 题干可能用样本、实验或数据支持结论，需核对样本代表性、对照条件和主体一致性。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  B:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  C:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  D:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: true
argument_structure_correct: true
option_analysis_correct: false
method_recall_correct: true
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 题型和论点识别正确；A 的直接证据支持作用未被突出。
```

### 错误类型

```text
选项力度排序错误；标准答案选项未突出
```

### 备注

```text
无。
```

## LR-004

```yaml
case_id: LR-004
image_file: text-image/logic_reasoning_real_cases_10_images/LR-004_strengthen_except_denisovan.png
status: evaluated_v2_draft
sub_type_expected: 加强题 / 支持选非
topic_hint: 丹尼索瓦人
standard_answer: D
core_judgment: D 只是背景环境适合活动，不能直接支持丹尼索瓦人曾居住
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
考古研究者认为，丹尼索瓦人很可能曾长期生活在青藏高原地区。

以下各项如果为真，除哪项外，均能支持上述观点？
```

### 选项

```text
A. 在青藏高原相关遗址中发现了与丹尼索瓦人基因特征高度吻合的人类遗骸信息。
B. 当地现代居民中存在可追溯到古人群的高原低氧适应基因，而该基因与丹尼索瓦人有关。
C. 高原地区发现的部分古人类活动遗迹，其年代与丹尼索瓦人已知活动时期相吻合。
D. 青藏高原地区生态环境复杂多样，适合多种古人类和动物群体活动与迁徙。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-004.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 加强 / 支持加强
answer_candidate: null
needs_more_data: false
standard_answer: D
core_judgment: D 只是背景环境适合活动，不能直接支持丹尼索瓦人曾居住
source_method_ids:
  - lj_support_general_001
  - lj_support_bridge_001
  - lj_support_add_evidence_001
  - lj_support_necessary_condition_001
  - lj_strength_order_compare_001
recommended_methods:
  - method_id: lj_support_general_001
    method_name: 支持题主体话题一致原则
    reason: 优先方法
  - method_id: lj_support_bridge_001
    method_name: 支持类断点搭桥法
    reason: 辅助比较或备选方法
  - method_id: lj_support_add_evidence_001
    method_name: 新增事实数据支持法
    reason: 辅助比较或备选方法
  - method_id: lj_support_necessary_condition_001
    method_name: 必要条件式支持法
    reason: 辅助比较或备选方法
  - method_id: lj_strength_order_compare_001
    method_name: 加强/削弱力度比较通用规则
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 丹尼索瓦人很可能曾长期生活在青藏高原地区
premises:
  - 考古研究者
  - 以下各项如果为真，除
reasoning_chain: 考古研究者；  以下各项如果为真，除 -> 丹尼索瓦人很可能曾长期生活在青藏高原地区
gap: 题干可能用样本、实验或数据支持结论，需核对样本代表性、对照条件和主体一致性。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  B:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  C:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  D:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: partial
argument_structure_correct: true
option_analysis_correct: false
method_recall_correct: partial
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 识别为加强题，但未显式识别“除哪项外”的选非方向，D 作为不能直接支持项未被突出。
```

### 错误类型

```text
选非方向识别不足；选项力度排序错误；标准答案选项未突出
```

### 备注

```text
无。
```

## LR-005

```yaml
case_id: LR-005
image_file: text-image/logic_reasoning_real_cases_10_images/LR-005_assumption_bitter_taste.png
status: evaluated_v2_draft
sub_type_expected: 前提假设题
topic_hint: 苦味防御机制
standard_answer: D
core_judgment: 建立“苦味—有毒/有害物质”之间的必要桥梁
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
有学者认为，生物对苦味的敏感感知是一种重要的防御机制，因为它能够帮助个体在摄入食物前对潜在有害物质发出预警。

上述论证若要成立，最需要假设以下哪项？
```

### 选项

```text
A. 生物对甜味和咸味的感知同样具有适应意义。
B. 苦味感知能力在不同物种之间存在明显差异。
C. 许多无毒食物也可能带有一定苦味。
D. 自然界中大量有毒或有害物质都具有苦味特征，苦味能够在一定程度上提示风险。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-005.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 前提假设 / 必要前提
answer_candidate: null
needs_more_data: false
standard_answer: D
core_judgment: 建立“苦味—有毒/有害物质”之间的必要桥梁
source_method_ids:
  - lj_premise_general_001
  - lj_premise_bridge_001
  - lj_premise_fill_gap_001
  - lj_premise_enable_condition_001
recommended_methods:
  - method_id: lj_premise_general_001
    method_name: 前提假设没它不行检验法
    reason: 优先方法
  - method_id: lj_premise_bridge_001
    method_name: 前提类断点搭桥法
    reason: 辅助比较或备选方法
  - method_id: lj_premise_fill_gap_001
    method_name: 直接证据缺失补洞法
    reason: 辅助比较或备选方法
  - method_id: lj_premise_enable_condition_001
    method_name: 可行性前提法
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 生物对苦味的敏感感知是一种重要的防御机制，因为它能够帮助个体在摄入食物前对潜在有害物质发出预警
premises:
  - 有学者
  - 上述论证若要成立，最需要假设
reasoning_chain: 有学者；  上述论证若要成立，最需要假设 -> 生物对苦味的敏感感知是一种重要的防御机制，因为它能够帮助个体在摄入食物前对潜在有害物质发出预警
gap: 需核对论据到论点之间是否存在主体、范围或因果桥梁缺口。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 未必是必要条件
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；前提题需进一步做否定代入。
  B:
    effect: 未必是必要条件
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；前提题需进一步做否定代入。
  C:
    effect: 未必是必要条件
    strength_level: medium
    is_candidate: false
    reason: 可能补充解释机制或背景事实；前提题需进一步做否定代入。
  D:
    effect: 未必是必要条件
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；前提题需进一步做否定代入。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: true
argument_structure_correct: partial
option_analysis_correct: false
method_recall_correct: true
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 题型与方法召回正确，但必要桥梁没有足够精确落到“苦味—有毒/有害物质”。
```

### 错误类型

```text
论证缺口判断过泛；选项力度排序错误；标准答案选项未突出
```

### 备注

```text
无。
```

## LR-006

```yaml
case_id: LR-006
image_file: text-image/logic_reasoning_real_cases_10_images/LR-006_assumption_retina_ai.png
status: evaluated_v2_draft
sub_type_expected: 前提假设题
topic_hint: AI 视网膜筛查心血管风险
standard_answer: D
core_judgment: 建立“视网膜特征变化—心血管风险预测”之间的必要桥梁
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
某研究团队开发出一种人工智能系统，可以通过分析受检者的视网膜图像来识别潜在心血管风险。研究者据此认为，这种技术未来有望改变传统心脏病筛查方式。

上述论证若要成立，最需要假设以下哪项？
```

### 选项

```text
A. 视网膜图像采集设备的成本会逐步降低。
B. 医疗机构愿意尝试使用人工智能辅助诊断工具。
C. 受检者对无创筛查技术的接受度普遍较高。
D. 视网膜中的某些特征变化能够稳定、有效地反映心血管疾病风险，因而可用于可靠筛查。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-006.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 前提假设 / 必要前提
answer_candidate: null
needs_more_data: false
standard_answer: D
core_judgment: 建立“视网膜特征变化—心血管风险预测”之间的必要桥梁
source_method_ids:
  - lj_premise_general_001
  - lj_premise_bridge_001
  - lj_premise_fill_gap_001
  - lj_premise_enable_condition_001
recommended_methods:
  - method_id: lj_premise_general_001
    method_name: 前提假设没它不行检验法
    reason: 优先方法
  - method_id: lj_premise_bridge_001
    method_name: 前提类断点搭桥法
    reason: 辅助比较或备选方法
  - method_id: lj_premise_fill_gap_001
    method_name: 直接证据缺失补洞法
    reason: 辅助比较或备选方法
  - method_id: lj_premise_enable_condition_001
    method_name: 可行性前提法
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 这种技术未来有望改变传统心脏病筛查方式
premises:
  - 某研究团队开发出一种人工智能系统，可以通过分析受检者的视网膜图像来识别潜在心血管风险
  - 研究者据此
  - 上述论证若要成立，最需要假设
reasoning_chain: 某研究团队开发出一种人工智能系统，可以通过分析受检者的视网膜图像来识别潜在心血管风险；研究者据此；  上述论证若要成立，最需要假设 -> 这种技术未来有望改变传统心脏病筛查方式
gap: 题干可能用样本、实验或数据支持结论，需核对样本代表性、对照条件和主体一致性。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 未必是必要条件
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；前提题需进一步做否定代入。
  B:
    effect: 未必是必要条件
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；前提题需进一步做否定代入。
  C:
    effect: 未必是必要条件
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；前提题需进一步做否定代入。
  D:
    effect: 未必是必要条件
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；前提题需进一步做否定代入。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: true
argument_structure_correct: partial
option_analysis_correct: false
method_recall_correct: true
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 题型与方法召回正确，但必要桥梁没有精确落到“视网膜特征—心血管风险预测”。
```

### 错误类型

```text
论证缺口判断过泛；选项力度排序错误；标准答案选项未突出
```

### 备注

```text
无。
```

## LR-007

```yaml
case_id: LR-007
image_file: text-image/logic_reasoning_real_cases_10_images/LR-007_explain_bus_delay.png
status: image_mismatch_duplicate
sub_type_expected: 解释说明题
topic_hint: 增加公交班次后仍迟到
standard_answer: 待人工填写
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: skipped
excluded_from_calibration: true
replacement_required: false
standard_answer_known: false
manual_evaluation_status: excluded
```

### 题干

```text
某网络安全团队提出一种新方案：在软件系统中主动加入大量“良性漏洞”，让攻击者在扫描时被大量无害信息干扰，从而减少真正危险漏洞被利用的概率。研究人员据此认为，这种方案可以显著提高系统安全性。

以下哪项如果为真，最能削弱上述观点？
```

### 选项

```text
A. 添加良性漏洞需要额外的开发与维护成本。
B. 不同类型的软件系统对安全防护的需求并不相同。
C. 有些企业在部署新系统前会进行第三方安全评估。
D. 经验丰富的攻击者通常能够快速识别并忽略良性漏洞，继续针对真正危险的漏洞发起攻击。
```

### 调用命令

```powershell
# LR-007 图片错放 / 重复样本，本轮跳过 solve-logic 调用。
```

### Solver 输出摘要

```yaml
sub_type_actual: null
answer_candidate: null
needs_more_data: null
source_method_ids: []
recommended_methods: []
warnings:
  - 图片错放或重复，未调用 solver。
```

### 论证结构摘要

```yaml
conclusion: null
premises: []
gap: 图片错放或重复，未纳入本轮校准。
```

### 选项分析摘要

```yaml
option_analysis_summary: 图片错放或重复，未调用 solver。
```

### 人工评估

```yaml
manual_evaluation_status: excluded
standard_answer_known: false
subtype_correct: null
argument_structure_correct: null
option_analysis_correct: null
method_recall_correct: null
answer_candidate_reasonable: null
answer_candidate_correct: null
evaluation_note: 图片错放或重复，本批不参与校准统计。
```

### 错误类型

```text
异常样本
```

### 备注

```text
LR-007 因图片错放/疑似与 LR-001 重复，用户确认本批不再替换，本题不参与第一批校准统计。
```

## LR-008

```yaml
case_id: LR-008
image_file: text-image/logic_reasoning_real_cases_10_images/LR-008_explain_except_breastfeeding.png
status: evaluated_v2_draft
sub_type_expected: 解释说明题 / 解释选非
topic_hint: 母乳喂养率偏低
standard_answer: B
core_judgment: B 说母亲认同母乳有益，不能解释纯母乳喂养率偏低
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
调查显示，某地区0—6个月婴儿纯母乳喂养率明显偏低，相关部门希望找出导致这一现象的原因。

以下各项如果为真，除哪项外，均能解释上述现象？
```

### 选项

```text
A. 一些新手母亲担心自己泌乳不足，较早添加了配方奶。
B. 大多数母亲都认同母乳喂养对婴儿生长发育有益。
C. 部分用人单位缺乏完善的哺乳支持措施，影响了母亲持续母乳喂养。
D. 一些家庭成员认为婴儿只喝母乳不够“有营养”，从而建议尽早添加其他食物。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-008.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 加强 / 支持加强
answer_candidate: null
needs_more_data: false
standard_answer: B
core_judgment: B 说母亲认同母乳有益，不能解释纯母乳喂养率偏低
source_method_ids:
  - lj_support_general_001
  - lj_support_bridge_001
  - lj_support_add_evidence_001
  - lj_support_necessary_condition_001
  - lj_strength_order_compare_001
recommended_methods:
  - method_id: lj_support_general_001
    method_name: 支持题主体话题一致原则
    reason: 优先方法
  - method_id: lj_support_bridge_001
    method_name: 支持类断点搭桥法
    reason: 辅助比较或备选方法
  - method_id: lj_support_add_evidence_001
    method_name: 新增事实数据支持法
    reason: 辅助比较或备选方法
  - method_id: lj_support_necessary_condition_001
    method_name: 必要条件式支持法
    reason: 辅助比较或备选方法
  - method_id: lj_strength_order_compare_001
    method_name: 加强/削弱力度比较通用规则
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 以下各项如果为真，除
premises:
  - 调查显示，某地区0—6个月婴儿纯母乳喂养率明显偏低，相关部门希望找出导致这一现象的原因
reasoning_chain: 调查显示，某地区0—6个月婴儿纯母乳喂养率明显偏低，相关部门希望找出导致这一现象的原因 ->   以下各项如果为真，除
gap: 题干可能用样本、实验或数据支持结论，需核对样本代表性、对照条件和主体一致性。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  B:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  C:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
  D:
    effect: 需进一步比较加强力度
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；需按论点、论据、论证桥梁做力度比较。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: false
argument_structure_correct: false
option_analysis_correct: false
method_recall_correct: false
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 预期为解释说明/解释选非，但 v2 识别成加强题，且未处理“除哪项外”。
```

### 错误类型

```text
题型识别错误；选非方向识别不足；论点抽取错误；method_id 召回不准；标准答案选项未突出
```

### 备注

```text
无。
```

## LR-009

```yaml
case_id: LR-009
image_file: text-image/logic_reasoning_real_cases_10_images/LR-009_inference_flynn_effect.png
status: evaluated_v2_draft
sub_type_expected: 结论推出题
topic_hint: 弗林效应
standard_answer: A
core_judgment: 最保守推出：后期人群在同类测验中平均成绩高于早期人群
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
研究者在比较不同年代人群的智力测验结果时发现，近几十年来，多国人群在同类测验中的平均得分普遍高于更早时期的对应人群。这种长期出现的平均分提升现象被称为“弗林效应”。

根据上述信息，可以推出的是：
```

### 选项

```text
A. 在相同或相近类型的智力测验中，后期人群的平均成绩整体上往往高于早期人群。
B. 弗林效应说明所有国家居民的智力水平都在持续快速上升。
C. 经济越发达的国家，智力测验平均分一定越高。
D. 只要一个国家教育投入增加，该国居民平均智商就必然上升。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-009.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 解释说明 / 矛盾解释
answer_candidate: null
needs_more_data: false
standard_answer: A
core_judgment: 最保守推出：后期人群在同类测验中平均成绩高于早期人群
source_method_ids:
  - lj_explanation_contradiction_001
  - lj_support_explain_mechanism_001
  - lj_irrelevant_options_001
recommended_methods:
  - method_id: lj_explanation_contradiction_001
    method_name: 看似矛盾现象合理解释法
    reason: 优先方法
  - method_id: lj_support_explain_mechanism_001
    method_name: 解释说明式支持法
    reason: 辅助比较或备选方法
  - method_id: lj_irrelevant_options_001
    method_name: 常见无关选项排除法
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 根据上述信息，可以推出的是：
premises:
  - 研究者在比较不同年代人群的智力测验结果时发现，近几十年来，多国人群在同类测验中的平均得分普遍高于更早时期的对应人群
  - 这种长期出现的平均分提升现象被称为“弗林效应”
reasoning_chain: 研究者在比较不同年代人群的智力测验结果时发现，近几十年来，多国人群在同类测验中的平均得分普遍高于更早时期的对应人群；这种长期出现的平均分提升现象被称为“弗林效应” ->   根据上述信息，可以推出的是：
gap: 题干可能从相关事实推到因果或效果结论，需核对是否存在他因、倒因或桥梁缺失。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 需检查是否能同时解释现象两面
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；解释题需检查是否同时解释矛盾双方。
  B:
    effect: 需检查是否能同时解释现象两面
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；解释题需检查是否同时解释矛盾双方。
  C:
    effect: 需检查是否能同时解释现象两面
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；解释题需检查是否同时解释矛盾双方。
  D:
    effect: 需检查是否能同时解释现象两面
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；解释题需检查是否同时解释矛盾双方。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: false
argument_structure_correct: false
option_analysis_correct: false
method_recall_correct: false
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 预期为结论推出，但 v2 识别为解释说明；A 的保守推出没有被识别。
```

### 错误类型

```text
题型识别错误；论点抽取错误；method_id 召回不准；标准答案选项未突出
```

### 备注

```text
无。
```

## LR-010

```yaml
case_id: LR-010
image_file: text-image/logic_reasoning_real_cases_10_images/LR-010_inference_plastic_lunchbox_fee.png
status: evaluated_v2_draft
sub_type_expected: 结论推出题
topic_hint: 一次性塑料餐盒处理费
standard_answer: C
core_judgment: 固定每个餐盒 2 元，使用数量下降，则处理费收入趋于下降
transcription_status: done
solver_version: solve_logic_reasoning v2 calibration
solver_run: done
standard_answer_known: true
manual_evaluation_status: evaluated_v2_draft
```

### 题干

```text
某市规定，对每个投入使用的一次性塑料餐盒统一征收2元处理费。统计显示，近三年来，该市一次性塑料餐盒的使用数量持续下降。

根据上述信息，可以推出的是：
```

### 选项

```text
A. 近三年来，餐饮企业的整体利润一定持续下降。
B. 近三年来，市民对堂食的偏好一定显著提高。
C. 如果其他条件不变，近三年来该市因一次性塑料餐盒征收的处理费收入总体上趋于下降。
D. 近三年来，可重复使用餐盒的使用量一定同比例上升。
```

### 调用命令

```powershell
xingce-solver solve-logic --question .tmp/logic_v2_rerun_questions/LR-010.txt
```

### Solver 输出摘要

```yaml
sub_type_actual: 结论推出 / 基础推出
answer_candidate: null
needs_more_data: false
standard_answer: C
core_judgment: 固定每个餐盒 2 元，使用数量下降，则处理费收入趋于下降
source_method_ids:
  - lj_conclusion_translation_001
  - lj_sufficient_necessary_001
  - lj_relation_quantifier_001
recommended_methods:
  - method_id: lj_conclusion_translation_001
    method_name: 结论推出翻译-匹配-排除法
    reason: 优先方法
  - method_id: lj_sufficient_necessary_001
    method_name: 充分条件与必要条件识别法
    reason: 辅助比较或备选方法
  - method_id: lj_relation_quantifier_001
    method_name: 所有/有些/可能/必然关系转换法
    reason: 辅助比较或备选方法
warnings:
  []
```

### 论证结构摘要

```yaml
conclusion: 根据上述信息，可以推出的是：
premises:
  - 某市规定，对每个投入使用的一次性塑料餐盒统一征收2元处理费
  - 统计显示，近三年来，该市一次性塑料餐盒的使用数量持续下降
reasoning_chain: 某市规定，对每个投入使用的一次性塑料餐盒统一征收2元处理费；统计显示，近三年来，该市一次性塑料餐盒的使用数量持续下降 ->   根据上述信息，可以推出的是：
gap: 题干可能从相关事实推到因果或效果结论，需核对是否存在他因、倒因或桥梁缺失。
```

### 选项分析摘要

```yaml
option_analysis_summary:
  A:
    effect: 需与题干条件逐项核对是否必然推出
    strength_level: medium
    is_candidate: false
    reason: 与论点或论据话题相关，需比较是否击中断点；推出题不能超出题干确定信息。
  B:
    effect: 需与题干条件逐项核对是否必然推出
    strength_level: medium
    is_candidate: false
    reason: 与论点或论据话题相关，需比较是否击中断点；推出题不能超出题干确定信息。
  C:
    effect: 需与题干条件逐项核对是否必然推出
    strength_level: unknown
    is_candidate: false
    reason: 暂未识别到与论证链的直接关系；推出题不能超出题干确定信息。
  D:
    effect: 需与题干条件逐项核对是否必然推出
    strength_level: medium
    is_candidate: false
    reason: 与论点或论据话题相关，需比较是否击中断点；推出题不能超出题干确定信息。
```

### 人工评估

```yaml
manual_evaluation_status: evaluated_v2_draft
standard_answer_known: true
subtype_correct: true
argument_structure_correct: partial
option_analysis_correct: false
method_recall_correct: true
answer_candidate_reasonable: partial
answer_candidate_correct: null
evaluation_note: 题型和方法召回正确；但 C 的条件推出关系未被突出，其他选项反而被标成中等相关。
```

### 错误类型

```text
选项力度排序错误；标准答案选项未突出
```

### 备注

```text
无。
```

## 第一批 LR-001 ~ LR-010 初次运行小结

- 总样本数：10
- 成功转写：10
- 有效运行样本：9
- 异常样本：1
- LR-007：图片错放或重复。图片文件名和预期题型为解释说明题，但图片实际内容疑似与 LR-001 重复，为削弱题内容。
- 标准答案状态：LR-001 ~ LR-006、LR-008 ~ LR-010 已补录；LR-007 因异常样本仍为 `待人工填写`。
- 本轮是否评估答案正确率：否，因 v2 定位为结构化分析器，不强行自动给答案。
- 本轮用途：只评估题型识别、论点/论据抽取、选项分析结构、method_id 召回。
- 下一步：基于标准答案和人工评估结果设计 `solve_logic_reasoning v3`，但本轮不实现 v3。

## 第一批 LR-001 ~ LR-010 标准答案补录与 v2 评估汇总

- 总登记样本数：10
- 有效校准样本数：9
- 排除样本数：1
- 排除样本：LR-007，图片错放 / 疑似重复。
- 标准答案已补齐样本数：9
- 仍缺标准答案样本：LR-007
- 实际重跑 solve-logic 样本数：9
- 题型分布：削弱/质疑 2；加强/支持 2；前提假设 2；解释说明 1；结论推出 2。
- answer_candidate 输出正确数量：0
- answer_candidate 输出错误数量：0
- answer_candidate 输出 null 数量：9

高频问题列表：

- v2 普遍不输出 `answer_candidate`，9 个有效样本全部为 `null`。
- 选非方向识别不足，LR-004 和 LR-008 均未稳定处理“除哪项外”。
- 标准答案选项未突出，是本批最主要问题。
- 选项力度排序仍偏弱，很多关键选项被标为 unknown。
- LR-008、LR-009 存在题型识别错误，说明问法触发词优先级需要校准。
- method_id 召回在常规削弱/加强/前提题上基本可用，但解释选非和结论推出仍需优化。

失败类型统计：

- 标准答案选项未突出：9
- 选项力度排序错误：7
- method_id 召回不准：2
- 论点抽取错误：2
- 论证缺口判断过泛：2
- 选非方向识别不足：2
- 题型识别错误：2

当前是否建议进入 v3：建议进入 v3 方案设计和小范围代码实现准备，但本轮不实现 v3。

v3 改进优先级草案：

- P0: 增加 `decision_status` / `confidence` / 谨慎 `answer_candidate` 机制。
- P0: 强化选非题方向识别，包括“除哪项外”“不能支持”“无法解释”。
- P1: 增强标准答案选项突出度，让直接攻击/直接支持/必要桥梁/保守推出项能获得更高权重。
- P1: 论点、论据、缺口抽取更精确，减少宽泛 gap。
- P1: 优化 method_id 召回，尤其解释选非和结论推出。
- P2: 翻译推理、真假推理、分析推理暂缓。

## 第一批 LR-001 ~ LR-010 v3 回归结果

本节记录 `solve_logic_reasoning v3 cautious answer selection` 对第一批有效真实题的回归结果。LR-007 仍因图片错放 / 疑似重复排除，不参与统计。

- 总登记样本数：10
- 有效回归样本数：9
- 排除样本数：1
- 排除样本：LR-007
- answer_candidate 正确数量：9
- answer_candidate 错误数量：0
- answer_candidate null 数量：0
- LR-004 选非识别：已识别 `除哪项外`，`reverse_question_type: except`，候选 D
- LR-008 选非识别：已识别 `除哪项外`，`reverse_question_type: except`，候选 B
- LR-005 / LR-006：仍识别为前提假设题
- LR-009 / LR-010：仍识别为结论推出题

### v3 逐题结果

```yaml
LR-001:
  standard_answer: D
  answer_candidate: D
  decision_status: candidate_ready
  question_type: 削弱
  remaining_risk: 方案无效类已覆盖，仍需更多非网络安全题验证泛化。
LR-002:
  standard_answer: A
  answer_candidate: A
  decision_status: candidate_ready
  question_type: 削弱
  remaining_risk: 直接否定核心观点已覆盖，仍需更多食品/宣传类以外样本验证。
LR-003:
  standard_answer: A
  answer_candidate: A
  decision_status: candidate_ready
  question_type: 加强
  remaining_risk: 机制证据支持已覆盖，仍需避免把泛泛背景误判为强支持。
LR-004:
  standard_answer: D
  answer_candidate: D
  decision_status: candidate_ready
  question_type: 加强
  reverse_question_type: except
  remaining_risk: 选非方向已覆盖，但“支持选非”仍需更多题干表达回归。
LR-005:
  standard_answer: D
  answer_candidate: D
  decision_status: candidate_ready
  question_type: 前提假设
  remaining_risk: 必要桥梁已覆盖，仍需加强否定代入解释质量。
LR-006:
  standard_answer: D
  answer_candidate: D
  decision_status: candidate_ready
  question_type: 前提假设
  remaining_risk: 指标预测目标类前提已覆盖，仍需更多医学/技术类样本验证。
LR-008:
  standard_answer: B
  answer_candidate: B
  decision_status: candidate_ready
  question_type: 解释说明
  reverse_question_type: except
  remaining_risk: 解释选非已覆盖，仍需更多“无法解释/不能解释”表达回归。
LR-009:
  standard_answer: A
  answer_candidate: A
  decision_status: candidate_ready
  question_type: 结论推出
  remaining_risk: 保守复述类推出已覆盖，暂不扩展翻译推理。
LR-010:
  standard_answer: C
  answer_candidate: C
  decision_status: candidate_ready
  question_type: 结论推出
  remaining_risk: 条件不变下的数值趋势推出已覆盖，仍需避免绝对化选项误判。
```

### v3 剩余失败类型

- 泛化风险：当前 9 道真实题全部命中，但样本量仍小。
- 解释质量风险：`answer_candidate` 已可输出，但论点/论据/缺口文本仍偏模板化。
- 选非泛化风险：已覆盖“除哪项外”，仍需覆盖“不能支持”“不能加强”“不能解释”“无法推出”等更多表达。
- 范围边界：仍不支持翻译推理、真假推理、分析推理、图形推理、定义判断、类比推理。
