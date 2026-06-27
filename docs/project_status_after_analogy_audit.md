# Project Status After Analogy Audit

## 当前 HEAD

- commit: `73e5595`
- message: audit analogy strong relation package
- 日期: 2026-06-15

## 当前项目目标

花生十三方法论 MCP/CLI 解题系统。基于规则的知识库 + 可解释 solver，不走机器学习路线。

## 总体原则

- method_id + 可解释规则 solver
- 不走机器学习
- 不唯一则 analysis_only
- wrong 优先级高于 correct（宁可 correct=0 也不能 wrong>0）
- 不根据答案写规则
- 不默认选第一个 option

## 冻结文件

- `src/xingce_solver/solvers/data_analysis.py` — 资料分析 v5 stable，已冻结
- `knowledge_base/all_cards.jsonl` — 知识库，不允许修改

## 已集成模块

### 1. 资料分析 (solve_data_analysis v5)

- 状态: 已冻结
- 不允许修改

### 2. 论证类逻辑推理 (v5-v6)

- 状态: 已集成 solve_logic_reasoning
- 第二批 20 题: **18 correct / 0 wrong / 2 null**

### 3. 翻译推理 (v6.1)

- 状态: 已集成 solve_logic_reasoning
- 16 题: **16 correct / 0 wrong / 0 null**（满分）

### 4. 真假推理 (v7.1)

- 状态: 已保守接入 solve_logic_reasoning
- 12 题: **4 correct / 0 wrong / 8 null**

### 5. 分析推理 / 朴素逻辑 (v9.0)

- 状态: 已保守接入 solve_logic_reasoning
- 12 题: **2 correct / 0 wrong / 10 null**
- 当前不建议继续在原 12 题包上堆规则

## 未集成/暂停模块

### 6. 定义判断 (v1.4)

- 状态: isolated core 已完成，未接入主 solver
- 12 题: **0 correct / 0 wrong / 12 null**
- **暂停原因**: 需要语义理解，纯规则框架无法突破；当前收益为零

### 7. 类比推理 (v1.4)

- 状态: isolated core 已完成，未接入主 solver
- 第一批 12 题: **2 correct / 0 wrong / 10 null**
- 第二批 strong package 12 题: **0 correct / 0 wrong / 12 null**
- **暂停原因**: 纯规则框架对类比推理覆盖率有限；第一批仅 material_product/naming_convention 可安全解决；第二批三词型/语义关系过多，core 无法覆盖

## 为什么不建议图形推理直接开发

图形推理需要视觉模式识别能力，纯规则/文本框架无法处理图像内容。在没有 OCR/视觉模型接入方案之前，不建议直接开发 solver。

## 下一阶段候选方向

A. **回到真假推理 v7.2** — 做小范围 assignment refinement，争取更多 solved，但必须 wrong=0
B. **扩充论证类/翻译推理真题回归** — 巩固高价值模块，验证泛化能力
C. **图形推理只做前置调研** — 不直接写 solver，先研究题型结构和可能的文本化方案
D. **暂不建议继续定义判断/类比推理硬堆规则** — 投入产出比低
