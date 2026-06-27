# 判断推理-图形推理不确定项（audited）

## item_001：黑白运算具体运算表细节
- source_file: 花生图形推理笔记.pdf
- source_page: 6, 17
- uncertainty_type: 图示细节不完全可读
- observed_content: 笔记中有黑+白、白+黑、黑+黑、白+白的示例推导，但局部小图和表格过密。
- handling: 卡片 `gr_black_white_operation_001` 只保留“同位置建立统一运算表”的确定方法，不固化具体运算结果表。
- related_card_id: gr_black_white_operation_001, gr_black_white_block_001
- need_review: true

## item_002：线数量中的复杂线组分类
- source_file: 花生图形推理笔记.pdf
- source_page: 9, 12, 15
- uncertainty_type: 图示层级与局部文字不完全清晰
- observed_content: 曲直性、角、图形间关系页均涉及线段、平行线组、连接线、公共线等，但部分示例图示较密。
- handling: 卡片 `gr_quantity_line_001` 只抽取“先定义线的计数口径并保持一致”的方法，不补造细分口诀。
- related_card_id: gr_quantity_line_001
- need_review: true

## item_003：功能元素具体标记对象清单
- source_file: 花生图形推理笔记.pdf
- source_page: 16
- uncertainty_type: 图示较密，部分小字难以确认
- observed_content: 页面列出标记点、线、面、角以及黑点连接关系等多类对象。
- handling: 卡片 `gr_functional_element_001` 保留“先找标记，再找依附对象和相对位置”的稳定流程；未穷举所有示例对象。
- related_card_id: gr_functional_element_001
- need_review: true

## item_004：字母属性完整字母表分类
- source_file: 花生图形推理笔记.pdf
- source_page: 20
- uncertainty_type: 部分字母列表较小，可能受字体影响
- observed_content: 页面给出轴对称、中心对称、曲直、开闭等字母分类。
- handling: 卡片 `gr_letter_symbol_001` 抽取观察顺序，不把所有字母分类作为硬编码表；如后续要做自动解题，建议人工复核字母分类表。
- related_card_id: gr_letter_symbol_001
- need_review: true

## item_005：六面体展开图结构细节
- source_file: 花生图形推理笔记.pdf
- source_page: 21
- uncertainty_type: 图示结构很多，部分变体未完全枚举
- observed_content: 页面列出1-4-1、2-3-1、2-2-2、0-3-3结构，并标注一共有4类11种。
- handling: 卡片 `gr_cube_net_overall_001` 只保留结构识别和验证流程，不枚举全部11种展开图。
- related_card_id: gr_cube_net_overall_001
- need_review: true

## item_006：思维导图单页过长导致部分小图细节不可审计
- source_file: 【判断推理】图形推理.pdf
- source_page: 1
- uncertainty_type: 思维导图缩放导致局部小图不可精确读取
- observed_content: 思维导图包含全模块结构、口诀和大量示例图，但局部图例无法逐一确认。
- handling: 以其作为结构来源和总流程来源；具体细节优先采用花生图形推理笔记对应页。
- related_card_id: gr_total_flow_001, gr_mnemonic_15_001
- need_review: true
