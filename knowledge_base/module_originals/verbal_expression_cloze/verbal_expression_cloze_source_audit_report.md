# verbal_expression_cloze_source_audit_report.md

生成时间：2026-06-08 06:55:06

## 1. 审计范围

本轮模块：**言语理解-语句表达与逻辑填空**

纳入 source audit 的来源文件：

1. `【言语理解与表达】标题、下文、语句填入、排序.pdf`
2. `【言语理解与表达】逻辑填空.pdf`
3. `花生言语理解笔记.pdf`

其中第三个文件是本对话前面已上传的言语笔记，本轮已按用户补充要求纳入合并审计。

## 2. 输出文件

- `verbal_expression_cloze_cards_audited.jsonl`
- `verbal_expression_cloze_methods_audited.md`
- `verbal_expression_cloze_router_rules_audited.yaml`
- `verbal_expression_cloze_uncertain_items_audited.md`
- `verbal_expression_cloze_source_audit_report.md`

## 3. 卡片统计

- 方法卡片总数：45
- 标题填入：4
- 下文推断：6
- 语句填入：6
- 语句排序：8
- 逻辑填空：20
- 综合流程：1

## 4. 工程字段审计

每张卡片均包含统一工程字段：

- `required_inputs`
- `calculation_policy`
- `solver_priority`
- `output_constraints`

并按题型补充专项字段：

- 排序类卡片：`ordering_clues`
- 语句填入卡片：`coherence_checks`
- 逻辑填空卡片：`semantic_clues`
- 逻辑填空卡片：`collocation_rules`

为保证 JSONL schema 稳定，非对应题型也保留这些字段，值为空数组。

## 5. 来源页码审计

### `【言语理解与表达】标题、下文、语句填入、排序.pdf`
- 文件为单页思维导图。
- 所有标题、下文、语句填入、语句排序的核心方法均标注为第 1 页。
- 与 `花生言语理解笔记.pdf` 中对应章节交叉校验。

### `【言语理解与表达】逻辑填空.pdf`
- 文件为单页思维导图。
- 所有逻辑填空核心方法均标注为第 1 页。
- 与 `花生言语理解笔记.pdf` 中“词语辨析、逻辑对应、宏观把握、词语积累”章节交叉校验。

### `花生言语理解笔记.pdf`
- 标题拟定：主要对应第 12-13 页。
- 下文推断：主要对应第 14-15 页。
- 语句填入：主要对应第 16-17 页。
- 语句排序：主要对应第 18-19 页。
- 逻辑填空章节：主要对应第 22、24、26 页。
- 常考实词/搭配积累：主要对应第 29-40 页。
- OCR 出现超出 40 页的异常页码，相关内容已记录在 uncertain_items 中。

## 6. 合并与清洗规则

- 同一方法在思维导图和笔记中均出现时，合并为一张方法卡。
- 当前 PDF 没有依据的方法未新增。
- 对题型边界相近的方法进行拆分：例如“标题主旨变形”和“标题可读性”分成不同卡片。
- 对逻辑填空中“语境提示”和“词语搭配”进行工程化拆分，便于后续 AI 调用。
- 不清晰手写批注未纳入确定性卡片。

## 7. need_review 项

当前明确 `need_review=true` 的卡片：

- `vecl_cloze_idiom_misread_018`

原因：易错成语来源页码在 `花生言语理解笔记.pdf` OCR 中出现页码异常，需要人工确认真实页码。
