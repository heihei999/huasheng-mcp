"""
Verbal reasoning method scaffold (guidance only, NOT a solver).

Provides structured thinking order, question-type routing, discourse structure
checklists, cloze context checklists, sentence expression checklists, method
checklists, option verification templates, and uncertainty constraints for
future LLM-based reasoning.

This module does NOT output answers. It does NOT integrate with CLI/MCP.
"""
from __future__ import annotations

from typing import Any


def build_verbal_reasoning_scaffold() -> dict[str, Any]:
    """Build the complete verbal reasoning method scaffold."""
    return {
        "module": "verbal_reasoning",
        "version": "v0.1",
        "mode": "method_scaffold_only",
        "positioning": (
            "本模块不是 solver。"
            "本模块不直接判断答案。"
            "本模块不直接选择选项。"
            "本模块用于约束大模型按言语理解方法识别题型、分析文段结构、定位重点句、识别逻辑关系、逐项验证选项，并在无法唯一时 analysis_only。"
        ),
        "stage_order": [
            "题型识别",
            "问法识别",
            "文段结构划分",
            "主题句/重点句定位",
            "逻辑关系识别",
            "语境与词义检查",
            "选项逐项验证",
            "干扰项识别",
            "衔接连贯检查",
            "唯一性判断",
            "不确定性约束",
        ],
        "question_type_router": {
            "主旨意图": {
                "signals": ["主旨", "意图", "概括", "中心", "主要", "核心", "关键词"],
                "focus_points": ["主题句定位", "文段结构", "主体词一致"],
                "preferred_method": "主题句定位 + 结构分析",
                "risk": "机械看转折词、把局部细节当主旨",
                "analysis_only_when": ["多个选项均可解释主旨", "文段结构不明确", "问法目标模糊"],
                "feasibility": "C_scaffold_only",
            },
            "中心理解": {
                "signals": ["中心", "主要意思", "核心观点", "作者想说"],
                "focus_points": ["整体文意", "主题句", "主体词"],
                "preferred_method": "整体概括 + 主题句定位",
                "risk": "以偏概全、过度引申",
                "analysis_only_when": ["文段多层结构复杂", "多个选项均可解释"],
                "feasibility": "C_scaffold_only",
            },
            "标题填入": {
                "signals": ["标题", "最适合做标题", "标题最恰当"],
                "focus_points": ["关键词覆盖", "可读性", "概括性"],
                "preferred_method": "关键词覆盖 + 主旨概括",
                "risk": "标题过宽或过窄",
                "analysis_only_when": ["多个标题均合理", "文段主题不明确"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "下文推断": {
                "signals": ["接下来", "下文", "最可能", "续写"],
                "focus_points": ["尾句新信息", "话题结束", "已谈排除"],
                "preferred_method": "尾句分析 + 话题延续",
                "risk": "重复已谈内容",
                "analysis_only_when": ["尾句指向不明确", "多个选项均可能延续"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "语句填入": {
                "signals": ["填入", "横线", "最恰当", "衔接"],
                "focus_points": ["横线位置功能", "上下文话题", "指代一致"],
                "preferred_method": "位置功能 + 上下文衔接",
                "risk": "指代不明",
                "analysis_only_when": ["上下文指代不明", "多个选项均衔接合理"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "语句排序": {
                "signals": ["排序", "排列", "最连贯", "语序"],
                "focus_points": ["首句判断", "尾句判断", "捆绑关系", "时间逻辑"],
                "preferred_method": "首尾判断 + 捆绑验证",
                "risk": "多个连贯顺序",
                "analysis_only_when": ["存在多个连贯顺序", "捆绑线索不足"],
                "feasibility": "B_scaffold_first_solver_later",
            },
            "逻辑填空": {
                "signals": ["填入", "最恰当", "词语", "成语", "空格"],
                "focus_points": ["语境搭配", "逻辑对应", "词义辨析"],
                "preferred_method": "语境优先 + 词义辨析",
                "risk": "语境误判、词义混淆",
                "analysis_only_when": ["语境不足", "多个词语均合理", "词义无法可靠区分"],
                "feasibility": "C_scaffold_only",
            },
            "成语辨析": {
                "signals": ["成语", "恰当", "使用正确", "望文生义"],
                "focus_points": ["词义", "适用语境", "感情色彩"],
                "preferred_method": "语境还原 + 词义辨析",
                "risk": "望文生义、褒贬误用",
                "analysis_only_when": ["多个成语均合理", "词义无法可靠区分"],
                "feasibility": "C_scaffold_only",
            },
            "实词辨析": {
                "signals": ["实词", "最恰当", "填入", "区别"],
                "focus_points": ["词义侧重", "搭配习惯", "语境色彩"],
                "preferred_method": "字组词法 + 语境搭配",
                "risk": "词义混淆",
                "analysis_only_when": ["多个实词均合理", "词义无法可靠区分"],
                "feasibility": "C_scaffold_only",
            },
            "关联词填空": {
                "signals": ["关联词", "但是", "因此", "不仅", "只有"],
                "focus_points": ["逻辑关系", "语义约束"],
                "preferred_method": "逻辑关系识别 + 语义约束",
                "risk": "逻辑关系判断错误",
                "analysis_only_when": ["逻辑关系不明确", "多个关联词均合理"],
                "feasibility": "C_scaffold_only",
            },
            "细节理解": {
                "signals": ["以下说法正确", "以下说法不正确", "符合原文", "不符合"],
                "focus_points": ["逐项比对", "偷换概念", "范围扩大缩小"],
                "preferred_method": "逐项比对 + 干扰项排除",
                "risk": "遗漏细节、过度推断",
                "analysis_only_when": ["文段信息不足", "多个选项均合理"],
                "feasibility": "D_defer",
            },
            "态度观点": {
                "signals": ["作者态度", "作者观点", "认为", "态度"],
                "focus_points": ["态度词", "转折后观点", "整体倾向"],
                "preferred_method": "态度词定位 + 整体倾向",
                "risk": "误判态度倾向",
                "analysis_only_when": ["态度不明确", "多个选项均可解释"],
                "feasibility": "D_defer",
            },
            "语义衔接": {
                "signals": ["衔接", "连贯", "话题一致", "前后照应"],
                "focus_points": ["话题一致性", "指代一致", "逻辑连贯"],
                "preferred_method": "话题分析 + 指代验证",
                "risk": "话题跳跃判断错误",
                "analysis_only_when": ["话题不明确", "多个选项均衔接合理"],
                "feasibility": "C_scaffold_only",
            },
            "文段结构": {
                "signals": ["结构", "总分", "分总", "转折", "递进"],
                "focus_points": ["结构类型", "主题句位置", "逻辑关系"],
                "preferred_method": "结构分析 + 主题句定位",
                "risk": "结构判断错误",
                "analysis_only_when": ["结构不明确", "多层结构复杂"],
                "feasibility": "C_scaffold_only",
            },
            "其他": {
                "signals": [],
                "focus_points": ["按具体题型分析"],
                "preferred_method": "按具体题型选择",
                "risk": "题型不确定",
                "analysis_only_when": ["题型无法识别"],
                "feasibility": "C_scaffold_only",
            },
        },
        "question_type_checklists": {
            "主旨意图": {
                "signals": ["主旨", "意图", "概括", "中心", "主要"],
                "focus_points": ["主题句定位", "文段结构", "主体词一致"],
                "analysis_steps": [
                    "识别文段结构（总分/分总/转折/递进等）",
                    "定位主题句或重点句",
                    "锁定主体词",
                    "逐选项比对是否覆盖核心话题",
                ],
                "option_verification": [
                    "检查是否回应问法",
                    "检查是否覆盖文段核心话题",
                    "检查是否偷换主体",
                    "检查是否以偏概全",
                ],
                "analysis_only_when": ["多个选项均可解释主旨", "文段结构不明确"],
            },
            "中心理解": {
                "signals": ["中心", "主要意思", "核心观点"],
                "focus_points": ["整体文意", "主题句", "主体词"],
                "analysis_steps": [
                    "通读全文把握整体文意",
                    "定位主题句",
                    "概括核心观点",
                    "逐选项比对",
                ],
                "option_verification": [
                    "检查是否覆盖全文核心",
                    "检查是否过度引申",
                    "检查是否以偏概全",
                ],
                "analysis_only_when": ["文段多层结构复杂", "多个选项均可解释"],
            },
            "标题填入": {
                "signals": ["标题", "最适合做标题"],
                "focus_points": ["关键词覆盖", "可读性", "概括性"],
                "analysis_steps": [
                    "定位主题句和关键词",
                    "概括文段核心内容",
                    "比较选项的概括性和可读性",
                ],
                "option_verification": [
                    "检查关键词是否覆盖",
                    "检查是否过宽或过窄",
                    "检查可读性",
                ],
                "analysis_only_when": ["多个标题均合理", "文段主题不明确"],
            },
            "下文推断": {
                "signals": ["接下来", "下文", "最可能续写"],
                "focus_points": ["尾句新信息", "话题结束", "已谈排除"],
                "analysis_steps": [
                    "分析尾句的新信息指向",
                    "判断话题是否已结束",
                    "排除已谈内容",
                    "选择最可能的延续",
                ],
                "option_verification": [
                    "检查是否延续尾句新信息",
                    "检查是否重复已谈内容",
                    "检查话题连贯性",
                ],
                "analysis_only_when": ["尾句指向不明确", "多个选项均可能延续"],
            },
            "语句填入": {
                "signals": ["填入", "横线", "最恰当衔接"],
                "focus_points": ["横线位置功能", "上下文话题", "指代一致"],
                "analysis_steps": [
                    "判断横线位置功能（首句/中间/尾句）",
                    "分析上下文话题和逻辑",
                    "检查指代是否一致",
                    "选择最恰当的衔接",
                ],
                "option_verification": [
                    "检查是否与上下文话题一致",
                    "检查指代是否明确",
                    "检查逻辑是否连贯",
                ],
                "analysis_only_when": ["上下文指代不明", "多个选项均衔接合理"],
            },
            "语句排序": {
                "signals": ["排序", "排列", "最连贯语序"],
                "focus_points": ["首句判断", "尾句判断", "捆绑关系", "时间逻辑"],
                "analysis_steps": [
                    "判断首句和尾句",
                    "寻找捆绑关系（转折/代词/并列）",
                    "验证时间或逻辑顺序",
                    "逐选项验证连贯性",
                ],
                "option_verification": [
                    "检查首句是否合理",
                    "检查尾句是否合理",
                    "检查捆绑关系是否成立",
                    "检查整体连贯性",
                ],
                "analysis_only_when": ["存在多个连贯顺序", "捆绑线索不足"],
            },
            "逻辑填空": {
                "signals": ["填入", "最恰当词语", "成语"],
                "focus_points": ["语境搭配", "逻辑对应", "词义辨析"],
                "analysis_steps": [
                    "分析上下文语境",
                    "寻找逻辑对应关系",
                    "辨析选项词义",
                    "验证搭配和色彩",
                ],
                "option_verification": [
                    "检查语境是否匹配",
                    "检查搭配是否正确",
                    "检查感情色彩是否一致",
                    "检查语义轻重是否合适",
                ],
                "analysis_only_when": ["语境不足", "多个词语均合理", "词义无法可靠区分"],
            },
            "成语辨析": {
                "signals": ["成语", "使用正确", "望文生义"],
                "focus_points": ["词义", "适用语境", "感情色彩"],
                "analysis_steps": [
                    "还原语境",
                    "辨析成语本义和引申义",
                    "检查适用语境和色彩",
                ],
                "option_verification": [
                    "检查词义是否准确",
                    "检查语境是否匹配",
                    "检查是否望文生义",
                ],
                "analysis_only_when": ["多个成语均合理", "词义无法可靠区分"],
            },
            "实词辨析": {
                "signals": ["实词", "最恰当", "填入区别"],
                "focus_points": ["词义侧重", "搭配习惯", "语境色彩"],
                "analysis_steps": [
                    "分析语境需求",
                    "辨析选项词义侧重",
                    "检查搭配和色彩",
                ],
                "option_verification": [
                    "检查词义侧重是否匹配",
                    "检查搭配是否正确",
                    "检查色彩是否一致",
                ],
                "analysis_only_when": ["多个实词均合理", "词义无法可靠区分"],
            },
            "关联词填空": {
                "signals": ["关联词", "但是", "因此", "不仅"],
                "focus_points": ["逻辑关系", "语义约束"],
                "analysis_steps": [
                    "识别前后句逻辑关系",
                    "匹配关联词语义",
                    "验证逻辑连贯性",
                ],
                "option_verification": [
                    "检查逻辑关系是否正确",
                    "检查语义是否约束",
                ],
                "analysis_only_when": ["逻辑关系不明确", "多个关联词均合理"],
            },
            "细节理解": {
                "signals": ["以下说法正确/不正确", "符合/不符合原文"],
                "focus_points": ["逐项比对", "偷换概念", "范围扩大缩小"],
                "analysis_steps": [
                    "逐选项与原文比对",
                    "检查是否偷换概念",
                    "检查是否范围扩大或缩小",
                    "检查是否无中生有",
                ],
                "option_verification": [
                    "逐项与原文核对",
                    "检查概念是否一致",
                    "检查范围是否准确",
                ],
                "analysis_only_when": ["文段信息不足", "多个选项均合理"],
            },
            "态度观点": {
                "signals": ["作者态度", "作者观点", "认为"],
                "focus_points": ["态度词", "转折后观点", "整体倾向"],
                "analysis_steps": [
                    "定位态度词或观点句",
                    "判断整体倾向",
                    "排除干扰项",
                ],
                "option_verification": [
                    "检查态度是否一致",
                    "检查是否过度推断",
                ],
                "analysis_only_when": ["态度不明确", "多个选项均可解释"],
            },
            "语义衔接": {
                "signals": ["衔接", "连贯", "话题一致"],
                "focus_points": ["话题一致性", "指代一致", "逻辑连贯"],
                "analysis_steps": [
                    "分析话题是否一致",
                    "检查指代是否明确",
                    "验证逻辑是否连贯",
                ],
                "option_verification": [
                    "检查话题是否延续",
                    "检查指代是否一致",
                ],
                "analysis_only_when": ["话题不明确", "多个选项均衔接合理"],
            },
            "干扰项识别": {
                "signals": ["排除", "不正确", "错误"],
                "focus_points": ["偷换概念", "范围扩大缩小", "无中生有", "绝对化"],
                "analysis_steps": [
                    "识别干扰项类型",
                    "逐项验证是否符合文段",
                    "排除干扰项",
                ],
                "option_verification": [
                    "检查是否偷换概念",
                    "检查是否以偏概全",
                    "检查是否无中生有",
                ],
                "analysis_only_when": ["多个选项均可解释", "文段信息不足"],
            },
        },
        "discourse_structure_checklists": {
            "转折关系": {
                "identification_signs": ["但是", "然而", "不过", "却", "其实", "事实上"],
                "analysis_steps": ["定位转折词", "确认转折后为重点"],
                "option_verification": ["检查选项是否对应转折后内容"],
                "risk": ["转折后不一定总是重点，需结合整体文意"],
                "analysis_only_when": ["转折后内容复杂", "多个选项均可对应"],
            },
            "递进关系": {
                "identification_signs": ["不仅", "而且", "更", "甚至", "何况"],
                "analysis_steps": ["定位递进词", "确认递进后为更深层重点"],
                "option_verification": ["检查选项是否对应递进后内容"],
                "risk": ["递进后可能只是补充，不一定是核心"],
                "analysis_only_when": ["递进层次不明确"],
            },
            "因果关系": {
                "identification_signs": ["因此", "所以", "因而", "由此可见", "这说明"],
                "analysis_steps": ["定位因果词", "区分原因和结果", "判断重点在因还是果"],
                "option_verification": ["检查选项是否对应因果重点"],
                "risk": ["因果重点需结合问法判断"],
                "analysis_only_when": ["因果关系复杂", "重点不明确"],
            },
            "并列关系": {
                "identification_signs": ["同时", "此外", "另外", "一方面", "另一方面"],
                "analysis_steps": ["识别并列成分", "整体概括并列内容"],
                "option_verification": ["检查选项是否覆盖全部并列内容"],
                "risk": ["只覆盖部分并列内容导致片面"],
                "analysis_only_when": ["并列内容复杂", "无法完整概括"],
            },
            "对策句": {
                "identification_signs": ["应该", "需要", "必须", "建议", "应当"],
                "analysis_steps": ["定位对策句", "确认对策针对的问题"],
                "option_verification": ["检查选项是否对应对策"],
                "risk": ["对策可能只是部分解决方案"],
                "analysis_only_when": ["对策不明确", "多个对策均可"],
            },
            "问题-对策结构": {
                "identification_signs": ["问题", "对策", "解决", "措施"],
                "analysis_steps": ["识别问题部分", "识别对策部分", "确认重点在对策"],
                "option_verification": ["检查选项是否对应对策"],
                "risk": ["可能只概括问题而忽略对策"],
                "analysis_only_when": ["问题和对策均复杂"],
            },
            "观点-解释结构": {
                "identification_signs": ["认为", "观点", "解释", "比如", "例如"],
                "analysis_steps": ["定位观点句", "确认解释部分为支撑"],
                "option_verification": ["检查选项是否对应观点"],
                "risk": ["可能把解释当重点"],
                "analysis_only_when": ["观点不明确"],
            },
            "背景-观点结构": {
                "identification_signs": ["背景", "近年来", "随着", "发现", "新研究"],
                "analysis_steps": ["识别背景部分", "定位新发现或观点"],
                "option_verification": ["检查选项是否对应新发现"],
                "risk": ["可能把背景当重点"],
                "analysis_only_when": ["背景和观点界限不清"],
            },
            "总分结构": {
                "identification_signs": ["总之", "综上", "因此", "由此可见"],
                "analysis_steps": ["定位总句", "确认分句为支撑"],
                "option_verification": ["检查选项是否对应总句"],
                "risk": ["可能把分句当重点"],
                "analysis_only_when": ["总句不明确"],
            },
            "分总结构": {
                "identification_signs": ["尾句总结", "由此可见", "总之"],
                "analysis_steps": ["定位尾句总结", "确认前文为铺垫"],
                "option_verification": ["检查选项是否对应尾句总结"],
                "risk": ["尾句可能只是补充"],
                "analysis_only_when": ["尾句总结不明确"],
            },
            "主题句定位": {
                "identification_signs": ["首句引入", "尾句总结", "转折后", "递进后"],
                "analysis_steps": ["通过结构判断主题句位置", "锁定主题句"],
                "option_verification": ["检查选项是否对应主题句"],
                "risk": ["主题句可能不明显"],
                "analysis_only_when": ["主题句无法确认"],
            },
            "主体词一致": {
                "identification_signs": ["主体词", "主题词", "核心概念"],
                "analysis_steps": ["锁定主体词", "检查选项是否包含主体词"],
                "option_verification": ["检查选项主体词是否一致"],
                "risk": ["偷换主体词"],
                "analysis_only_when": ["主体词不明确"],
            },
            "干扰项排除": {
                "identification_signs": ["偷换概念", "范围扩大缩小", "无中生有", "绝对化", "以偏概全"],
                "analysis_steps": ["识别干扰项类型", "逐项排除"],
                "option_verification": ["检查选项是否存在干扰特征"],
                "risk": ["干扰项可能很隐蔽"],
                "analysis_only_when": ["多个选项均无明显干扰特征"],
            },
        },
        "cloze_context_checklists": {
            "语境搭配": {
                "scenarios": ["逻辑填空", "实词填空", "成语填空"],
                "check_steps": ["分析上下文语境", "寻找语境线索", "匹配选项"],
                "exclusion_basis": ["语境不匹配则排除"],
                "risk": ["语境判断主观"],
                "analysis_only_when": ["语境线索不足"],
            },
            "感情色彩": {
                "scenarios": ["褒贬判断", "语境色彩匹配"],
                "check_steps": ["判断文段感情色彩", "匹配选项色彩"],
                "exclusion_basis": ["色彩不一致则排除"],
                "risk": ["色彩判断可能主观"],
                "analysis_only_when": ["色彩不明确"],
            },
            "语义轻重": {
                "scenarios": ["程度匹配", "轻重对应"],
                "check_steps": ["判断文段语义轻重", "匹配选项程度"],
                "exclusion_basis": ["轻重不匹配则排除"],
                "risk": ["轻重判断需语感"],
                "analysis_only_when": ["轻重无法区分"],
            },
            "词义侧重": {
                "scenarios": ["近义词辨析", "实词辨析"],
                "check_steps": ["辨析选项词义侧重", "匹配语境需求"],
                "exclusion_basis": ["侧重不匹配则排除"],
                "risk": ["词义差异细微"],
                "analysis_only_when": ["词义无法可靠区分"],
            },
            "固定搭配": {
                "scenarios": ["习惯搭配", "固定用法"],
                "check_steps": ["检查搭配是否固定", "验证习惯用法"],
                "exclusion_basis": ["搭配不固定则排除"],
                "risk": ["搭配可能有地域差异"],
                "analysis_only_when": ["搭配不确定"],
            },
            "成语适配": {
                "scenarios": ["成语填空", "成语使用"],
                "check_steps": ["还原成语本义", "检查适用语境", "验证色彩"],
                "exclusion_basis": ["本义不匹配则排除"],
                "risk": ["望文生义"],
                "analysis_only_when": ["成语词义无法确认"],
            },
            "关联词逻辑": {
                "scenarios": ["关联词填空", "逻辑关系判断"],
                "check_steps": ["识别前后句逻辑", "匹配关联词语义"],
                "exclusion_basis": ["逻辑不匹配则排除"],
                "risk": ["逻辑关系判断错误"],
                "analysis_only_when": ["逻辑关系不明确"],
            },
            "前后照应": {
                "scenarios": ["逻辑填空", "语句填入"],
                "check_steps": ["寻找前后照应点", "验证一致性"],
                "exclusion_basis": ["不照应则排除"],
                "risk": ["照应点可能不明显"],
                "analysis_only_when": ["照应点不明确"],
            },
            "并列对应": {
                "scenarios": ["并列结构填空"],
                "check_steps": ["识别并列成分", "匹配对应词语"],
                "exclusion_basis": ["不对应则排除"],
                "risk": ["并列对应可能不严格"],
                "analysis_only_when": ["并列关系不明确"],
            },
            "转折对应": {
                "scenarios": ["转折结构填空"],
                "check_steps": ["定位转折词", "匹配反向对应"],
                "exclusion_basis": ["不反向对应则排除"],
                "risk": ["转折对应可能不严格"],
                "analysis_only_when": ["转折关系不明确"],
            },
            "递进对应": {
                "scenarios": ["递进结构填空"],
                "check_steps": ["定位递进词", "匹配程度加重"],
                "exclusion_basis": ["不加重则排除"],
                "risk": ["递进程度判断需语感"],
                "analysis_only_when": ["递进关系不明确"],
            },
        },
        "sentence_expression_checklists": {
            "语句填入": {
                "scenarios": ["横线在首句", "横线在中间", "横线在尾句"],
                "check_steps": ["判断横线位置功能", "分析上下文", "选择衔接"],
                "verification": ["检查话题一致", "检查指代明确", "检查逻辑连贯"],
                "risk": ["指代不明"],
                "analysis_only_when": ["上下文指代不明"],
            },
            "语句排序": {
                "scenarios": ["多句排序", "首尾判断"],
                "check_steps": ["判断首句和尾句", "寻找捆绑关系", "验证顺序"],
                "verification": ["检查首句合理", "检查尾句合理", "检查整体连贯"],
                "risk": ["多个连贯顺序"],
                "analysis_only_when": ["存在多个连贯顺序"],
            },
            "下文推断": {
                "scenarios": ["续写推断", "下文最可能"],
                "check_steps": ["分析尾句", "判断话题延续", "排除已谈"],
                "verification": ["检查延续尾句", "检查不重复已谈"],
                "risk": ["重复已谈内容"],
                "analysis_only_when": ["尾句指向不明确"],
            },
            "标题填入": {
                "scenarios": ["标题选择", "最恰当标题"],
                "check_steps": ["定位主题句", "概括核心", "比较选项"],
                "verification": ["检查关键词覆盖", "检查概括性"],
                "risk": ["标题过宽或过窄"],
                "analysis_only_when": ["多个标题均合理"],
            },
            "代词指代": {
                "scenarios": ["语句填入", "语句排序"],
                "check_steps": ["定位代词", "寻找指代对象", "验证一致"],
                "verification": ["检查指代明确", "检查语法一致"],
                "risk": ["指代对象不明确"],
                "analysis_only_when": ["指代对象不明确"],
            },
            "话题一致": {
                "scenarios": ["语句填入", "语义衔接"],
                "check_steps": ["识别话题", "验证话题延续"],
                "verification": ["检查话题一致"],
                "risk": ["话题跳跃判断错误"],
                "analysis_only_when": ["话题不明确"],
            },
            "逻辑顺序": {
                "scenarios": ["语句排序"],
                "check_steps": ["识别时间顺序", "识别空间顺序", "识别逻辑顺序"],
                "verification": ["检查顺序合理"],
                "risk": ["顺序判断错误"],
                "analysis_only_when": ["顺序不明确"],
            },
            "首句判断": {
                "scenarios": ["语句排序"],
                "check_steps": ["判断首句特征", "排除不适合做首句的句子"],
                "verification": ["检查首句合理"],
                "risk": ["首句判断错误"],
                "analysis_only_when": ["首句不明确"],
            },
            "尾句判断": {
                "scenarios": ["语句排序"],
                "check_steps": ["判断尾句特征", "确认总结或对策"],
                "verification": ["检查尾句合理"],
                "risk": ["尾句判断错误"],
                "analysis_only_when": ["尾句不明确"],
            },
        },
        "method_checklists": {
            "主题句定位": {
                "scenarios": ["主旨意图", "中心理解", "标题填入"],
                "steps": ["通过结构判断主题句位置", "锁定主题句", "概括核心"],
                "verification": ["检查选项是否对应主题句"],
                "risk": ["主题句可能不明显"],
                "analysis_only_when": ["主题句无法确认"],
            },
            "关联词分析": {
                "scenarios": ["逻辑填空", "主旨意图", "语句排序"],
                "steps": ["识别关联词", "判断逻辑关系", "匹配语义"],
                "verification": ["检查逻辑关系正确"],
                "risk": ["逻辑关系判断错误"],
                "analysis_only_when": ["逻辑关系不明确"],
            },
            "转折关系": {
                "scenarios": ["主旨意图", "逻辑填空", "语句排序"],
                "steps": ["定位转折词", "确认转折后为重点"],
                "verification": ["检查选项对应转折后"],
                "risk": ["转折后不一定总是重点"],
                "analysis_only_when": ["转折后内容复杂"],
            },
            "递进关系": {
                "scenarios": ["主旨意图", "逻辑填空"],
                "steps": ["定位递进词", "确认递进后为更深层重点"],
                "verification": ["检查选项对应递进后"],
                "risk": ["递进后可能只是补充"],
                "analysis_only_when": ["递进层次不明确"],
            },
            "因果关系": {
                "scenarios": ["主旨意图"],
                "steps": ["定位因果词", "判断重点在因还是果"],
                "verification": ["检查选项对应因果重点"],
                "risk": ["因果重点需结合问法判断"],
                "analysis_only_when": ["因果关系复杂"],
            },
            "对策句": {
                "scenarios": ["主旨意图", "下文推断"],
                "steps": ["定位对策句", "确认对策针对的问题"],
                "verification": ["检查选项对应对策"],
                "risk": ["对策可能只是部分解决方案"],
                "analysis_only_when": ["对策不明确"],
            },
            "总分结构": {
                "scenarios": ["主旨意图", "文段结构"],
                "steps": ["定位总句", "确认分句为支撑"],
                "verification": ["检查选项对应总句"],
                "risk": ["可能把分句当重点"],
                "analysis_only_when": ["总句不明确"],
            },
            "干扰项排除": {
                "scenarios": ["所有言语理解题型"],
                "steps": ["识别干扰项类型", "逐项排除"],
                "verification": ["检查选项是否存在干扰特征"],
                "risk": ["干扰项可能很隐蔽"],
                "analysis_only_when": ["多个选项均无明显干扰特征"],
            },
            "语境搭配": {
                "scenarios": ["逻辑填空", "成语辨析", "实词辨析"],
                "steps": ["分析上下文语境", "寻找语境线索", "匹配选项"],
                "verification": ["检查语境匹配"],
                "risk": ["语境判断主观"],
                "analysis_only_when": ["语境线索不足"],
            },
            "感情色彩": {
                "scenarios": ["逻辑填空", "成语辨析"],
                "steps": ["判断文段感情色彩", "匹配选项色彩"],
                "verification": ["检查色彩一致"],
                "risk": ["色彩判断可能主观"],
                "analysis_only_when": ["色彩不明确"],
            },
            "语义轻重": {
                "scenarios": ["逻辑填空", "实词辨析"],
                "steps": ["判断文段语义轻重", "匹配选项程度"],
                "verification": ["检查轻重匹配"],
                "risk": ["轻重判断需语感"],
                "analysis_only_when": ["轻重无法区分"],
            },
            "衔接连贯": {
                "scenarios": ["语句填入", "语句排序", "语义衔接"],
                "steps": ["分析上下文衔接", "验证逻辑连贯"],
                "verification": ["检查衔接一致"],
                "risk": ["衔接判断可能主观"],
                "analysis_only_when": ["衔接不明确"],
            },
            "排序线索": {
                "scenarios": ["语句排序"],
                "steps": ["寻找首尾线索", "寻找捆绑关系", "验证顺序"],
                "verification": ["检查排序合理"],
                "risk": ["多个连贯顺序"],
                "analysis_only_when": ["存在多个连贯顺序"],
            },
            "代词指代": {
                "scenarios": ["语句填入", "语句排序"],
                "steps": ["定位代词", "寻找指代对象", "验证一致"],
                "verification": ["检查指代明确"],
                "risk": ["指代对象不明确"],
                "analysis_only_when": ["指代对象不明确"],
            },
            "主体词覆盖": {
                "scenarios": ["主旨意图", "标题填入"],
                "steps": ["锁定主体词", "检查选项覆盖"],
                "verification": ["检查主体词一致"],
                "risk": ["偷换主体词"],
                "analysis_only_when": ["主体词不明确"],
            },
        },
        "option_verification": {
            "steps": [
                "逐项核验 A/B/C/D",
                "检查是否回应问法",
                "检查是否覆盖文段核心话题",
                "检查是否偷换主体",
                "检查是否过度引申",
                "检查是否以偏概全",
                "检查是否无中生有",
                "检查是否与文段逻辑关系一致",
                "检查是否与上下文衔接一致",
                "多个选项都能解释则 analysis_only",
                "无选项稳定成立且语义不确定则 analysis_only",
            ],
        },
        "response_template": (
            "【题型识别】\n"
            "判断本题属于哪种言语理解题型（主旨意图、中心理解、标题填入、下文推断、语句填入、语句排序、逻辑填空、成语辨析、实词辨析等）。\n\n"
            "【问法目标】\n"
            "明确题目要求（选主旨、选标题、续写、填入、排序等）。\n\n"
            "【文段结构】\n"
            "分析文段结构类型（总分/分总/转折/递进/因果/并列等）。\n\n"
            "【主题句/重点句】\n"
            "定位主题句或重点句，锁定核心话题。\n\n"
            "【逻辑关系】\n"
            "识别文段中的逻辑关系（转折、递进、因果、并列、对策等）。\n\n"
            "【语境/词义检查】\n"
            "如有词语填空，分析语境搭配、感情色彩、语义轻重、词义侧重。\n\n"
            "【选项核验】\n"
            "逐选项检查是否回应问法、覆盖核心话题、逻辑一致。\n\n"
            "【干扰项排除】\n"
            "识别干扰项类型（偷换概念、范围扩大缩小、无中生有、绝对化等）并排除。\n\n"
            "【衔接连贯检查】\n"
            "如涉及语句填入/排序，检查衔接连贯性。\n\n"
            "【唯一性判断】\n"
            "确认只有一个选项满足所有条件。若不唯一，标注 analysis_only。\n\n"
            "【不确定性说明】\n"
            "列出任何导致不确定的因素，标注 analysis_only。"
        ),
        "uncertainty_policy": {
            "triggers": [
                "题型无法稳定识别 → analysis_only",
                "问法目标不明确 → analysis_only",
                "文段结构无法稳定划分 → analysis_only",
                "主题句/重点句无法确认 → analysis_only",
                "多个选项均可解释 → analysis_only",
                "选项差异依赖强语感且无法确认 → analysis_only",
                "逻辑填空语境不足 → analysis_only",
                "成语/实词词义无法可靠区分 → analysis_only",
                "语句排序存在多个连贯顺序 → analysis_only",
                "语句填入上下文指代不明 → analysis_only",
            ],
        },
        "must_not_do": [
            "不得只按关键词匹配。",
            "不得只看转折词机械选择。",
            "不得把局部细节当主旨。",
            "不得忽略问法。",
            "不得忽略选项范围。",
            "不得默认选择第一个选项。",
            "不得在多个选项都能解释时强行选。",
            "不得把 scaffold 当 solver。",
            "不得用题号、case_id 或标准答案写规则。",
            "不得生成或引用自造真题。",
        ],
    }


def get_verbal_reasoning_stage_order() -> list[str]:
    """Return the ordered thinking stages."""
    return build_verbal_reasoning_scaffold()["stage_order"]


def get_verbal_reasoning_question_type_checklists() -> dict[str, Any]:
    """Return question type checklists."""
    scaffold = build_verbal_reasoning_scaffold()
    return {
        "router": scaffold["question_type_router"],
        "checklists": scaffold["question_type_checklists"],
    }


def get_verbal_reasoning_method_checklists() -> dict[str, Any]:
    """Return method checklists and structure checklists."""
    scaffold = build_verbal_reasoning_scaffold()
    return {
        "methods": scaffold["method_checklists"],
        "discourse_structures": scaffold["discourse_structure_checklists"],
        "cloze_contexts": scaffold["cloze_context_checklists"],
        "sentence_expressions": scaffold["sentence_expression_checklists"],
    }


def render_verbal_reasoning_prompt_template() -> str:
    """Return the prompt template for verbal reasoning."""
    return build_verbal_reasoning_scaffold()["response_template"]
