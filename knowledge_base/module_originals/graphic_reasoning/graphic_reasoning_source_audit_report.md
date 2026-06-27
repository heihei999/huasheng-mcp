# 判断推理-图形推理 source audit report

## 输入文件

- `花生图形推理笔记.pdf`：共25页。第1页封面，第2页目录，第3-24页为可用知识页，第25页空白页。本轮使用第3-24页。
- `【判断推理】图形推理.pdf`：共1页长图式思维导图。本轮用于总流程、口诀、模块结构和部分提示来源。

## 输出文件

- `graphic_reasoning_cards_audited.jsonl`
- `graphic_reasoning_methods_audited.md`
- `graphic_reasoning_router_rules_audited.yaml`
- `graphic_reasoning_uncertain_items_audited.md`
- `graphic_reasoning_source_audit_report.md`

## Source audit 结果

1. 每张卡片均保留 `source_file` 和 `source_page`，并使用页码数组记录多个来源。
2. 每张卡片均补充工程字段：`required_inputs`、`calculation_policy`、`solver_priority`、`output_constraints`。
3. 按用户要求，每张卡片均包含 `check_order` 或 `verification_steps`，用于约束后续解题器不得跳步猜测。
4. 本轮未新增 PDF 外方法；对于无法精确读取的图示细节，已进入 `graphic_reasoning_uncertain_items_audited.md`。
5. 思维导图页过长且局部图例过密，因此只作为总流程和结构来源；细节方法主要以笔记页为准。

## 卡片统计

- 总卡片数：39
- 总流程/路由类：6张
- 位置规律类：3张
- 样式规律类：3张
- 属性规律类：3张
- 数量规律及图形关系类：7张
- 特殊题型类：4张
- 空间重构类：6张
- 选项验证/易错点：2张

## 重点校验项

- `gr_total_flow_001` 为全局优先调用卡。
- `gr_option_verification_001` 为所有题型最终验证卡。
- `gr_common_misjudgment_001` 用于多规律冲突和防止 AI 乱猜。
- 空间重构卡片均明确相对面、公共边、时针法的调用顺序。
- 数量规律卡片均要求先定义计数口径，再验证选项。

## 保留的不确定项

详见 `graphic_reasoning_uncertain_items_audited.md`。主要集中在黑白运算具体表格、功能元素小图细节、字母完整分类、六面体展开图全部变体、思维导图局部小图。
