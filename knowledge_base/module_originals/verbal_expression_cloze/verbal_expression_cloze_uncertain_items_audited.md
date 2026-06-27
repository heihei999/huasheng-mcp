# verbal_expression_cloze_uncertain_items_audited.md

## 审计说明

本轮已将前面上传过的 `花生言语理解笔记.pdf` 纳入 source audit，并与本轮两个 PDF 合并审计。当前不确定项主要来自扫描页、图片批注、页码/OCR 映射和例题细节压缩。

---

## uncertain_001

- source_file: `花生言语理解笔记.pdf`
- source_page: 29-40 附近；OCR 结果中还出现了 41/42 等超出“40页”显示的页码
- uncertainty_type: 页码映射不确定
- observed_content: 常考实词、近义词习惯搭配、易错成语等词表内容在 OCR 中出现页码错位。
- why_uncertain: 文件解析显示 `contains 40 pages`，但抽取文本中出现 `PAGE: 41 / 40`、`PAGE: 42 / 40` 等异常。
- handling: 相关词表卡片保留为备查型卡片；涉及易错成语的 `vecl_cloze_idiom_misread_018` 标记 `need_review=true`。
- suggested_review: 后续人工翻页确认词语积累部分真实页码。

## uncertain_002

- source_file: `花生言语理解笔记.pdf`
- source_page: 13、15、17、19
- uncertainty_type: 手写批注识别不完整
- observed_content: 标题拟定、下文推断、语句填入、语句排序页面含蓝色/红色手写批注。
- why_uncertain: 部分批注为图片文字，OCR 未完整转写。
- handling: 只抽取能稳定识别的方法原则，不复刻不清晰批注。
- suggested_review: 如需训练“例题逐步解析器”，建议人工复核这些页的手写批注。

## uncertain_003

- source_file: `【言语理解与表达】标题、下文、语句填入、排序.pdf`
- source_page: 1
- uncertainty_type: 超长思维导图局部例题未完全展开
- observed_content: 一个页面包含标题、下文、填入、排序多类题型和大量例题。
- why_uncertain: 页面信息密度过高，本轮以方法卡片为主，未逐条拆分全部例题。
- handling: 所有卡片只保留例题中体现的方法，不新增 PDF 外方法。
- suggested_review: 若后续需要例题库，可单独进行“例题 step-by-step 解析”抽取。

## uncertain_004

- source_file: `【言语理解与表达】逻辑填空.pdf`
- source_page: 1
- uncertainty_type: 例题压缩
- observed_content: 逻辑填空 PDF 在单页中包含词义辨析、逻辑对应、对象特征、关联词、固定搭配、程度、色彩、语法、语体、比喻等多个方法。
- why_uncertain: 本轮按方法合并卡片，未把每个例题独立成卡。
- handling: 例题只保留方法触发和选项排除方式。
- suggested_review: 若后续要做题器示范，可单独生成 `examples.jsonl`。

## uncertain_005

- source_file: `花生言语理解笔记.pdf`
- source_page: 22、24、26
- uncertainty_type: 章节页具体内容部分不可见
- observed_content: OCR 显示“词语辨析”“逻辑对应”“宏观把握”等章节标题，但正文主要依赖当前 `逻辑填空.pdf`。
- why_uncertain: 上传笔记对应页部分以图片展示，OCR 未完整给出正文。
- handling: 对逻辑填空方法优先以 `【言语理解与表达】逻辑填空.pdf` 第 1 页为主要来源，笔记只作章节交叉来源。
- suggested_review: 后续如需更高精度，可对花生笔记逻辑填空页进行人工视觉复核。
