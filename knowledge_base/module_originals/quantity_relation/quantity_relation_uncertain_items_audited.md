# 数量关系不确定项记录

## item_001
- source_file: 花生数量关系笔记.pdf
- source_page: 全文扫描页
- uncertainty_type: OCR不可用
- observed_content: 文件搜索未能解析出文本，仅能基于渲染页图像进行人工视觉抽取。
- why_uncertain: 扫描笔记页存在较小字号、红色手写/标注和公式，部分细节无法完全机器校验。
- suggested_review: 后续若要极高精度，应对重点页 4、5、7、9、11、13、15、17、19、21-24、26、27、29、31、32、34 做人工复核。
- related_card_id: 多张笔记来源卡片

## item_002
- source_file: 花生数量关系笔记.pdf
- source_page: 4
- uncertainty_type: 公式排版/扫描识别不确定
- observed_content: 计算公式区中立方差/幂运算部分字号较小，部分上标和括号容易误读。
- why_uncertain: 卡片 qr_calculation_formula_001 已按常用标准公式整理，但原扫描的部分符号不够清晰。
- suggested_review: 使用前核对原图第4页基础公式区。
- related_card_id: qr_calculation_formula_001

## item_003
- source_file: 花生数量关系笔记.pdf
- source_page: 27
- uncertainty_type: 口诀边界不确定
- observed_content: “天平称重无脑选最小选项”属于考场经验提示，不是普适数学公式。
- why_uncertain: 该提示适用范围依赖题目是否为标准单异常球称重模型。
- suggested_review: 卡片 qr_balance_weighing_001 已标记 need_review=true，调用时必须确认异常球轻重条件。
- related_card_id: qr_balance_weighing_001

## item_004
- source_file: 花生数量关系笔记.pdf
- source_page: 35
- uncertainty_type: 空白页/无可抽取内容
- observed_content: 渲染后第35页基本为空白。
- why_uncertain: 不作为知识来源，不生成卡片。
- suggested_review: 无需处理，除非原PDF后续存在被截断内容。
- related_card_id: null

## item_005
- source_file: 花生数量关系笔记.pdf
- source_page: 21-24
- uncertainty_type: 例题公式上标细节不确定
- observed_content: 排列组合例题中部分 A/C 上下标较小。
- why_uncertain: 已按题意抽取方法逻辑，例题具体组合式未逐字复刻。
- suggested_review: 若要用于自动公式生成，可对这些页的例题公式单独建立公式卡。
- related_card_id: qr_perm_comb_basic_001, qr_average_grouping_001, qr_circular_permutation_001
