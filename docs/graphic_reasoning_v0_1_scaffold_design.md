# 图形推理 v0.1 Method Scaffold 设计文档

## 1. 背景

图形推理（graphic reasoning）需要视觉模式识别能力。纯规则/文本框架无法处理图像内容，因此不适合做本地图像识别 solver。

## 2. 本阶段定位

**method scaffold，不是 solver。**

本模块只负责：
- 构造图推观察顺序
- 提供视觉检查清单
- 生成给多模态大模型的作答模板
- 约束不确定性策略（analysis_only）

本模块不负责：
- 识别图像
- 数点线面
- 输出答案

## 3. 知识来源

- `knowledge_base/all_cards.jsonl` — 已有 39 张图推主方法卡
- `knowledge_base/module_originals/graphic_reasoning/graphic_reasoning_visual_checklists_audited.md` — 已补充视觉检查清单

## 4. 模块边界

不 OCR、不 OpenCV、不 PIL、不自动解析图片、不直接出答案、不接入 solve_logic_reasoning、不接入正式 CLI / MCP。

## 5. 输出结构

| 字段 | 说明 |
|------|------|
| `stage_order` | 十层观察顺序 |
| `composition_router` | 组成关系路由（相同/相似/不同/特殊） |
| `visual_checklists` | 15 个视觉检查清单 |
| `response_template` | 多模态大模型作答模板 |
| `uncertainty_policy` | 6 种 analysis_only 触发条件 |
| `must_not_do` | 7 条禁止事项 |

## 6. 未来使用方式

MCP 接入多模态大模型后，由多模态大模型负责看图，本 scaffold 负责约束观察顺序、证据说明、选项验证和 analysis_only 策略。

## 7. 验收

- pytest 通过
- smoke 通过
- 保护文件无 diff
- 无 OCR/OpenCV/PIL/ML 依赖
