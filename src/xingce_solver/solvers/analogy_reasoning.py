"""Isolated analogy reasoning core for logic judgment questions.

This module implements a minimal structured analogy reasoner for
"类比推理" (analogy reasoning) questions commonly found
in Chinese civil service exams (行测).

It is NOT integrated into solve_logic_reasoning. It is a standalone
engine for testing the core algorithm in isolation.

Version: v0.1
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AnalogyPair:
    """Structured representation of an analogy pair."""
    left: str
    right: str
    raw: str = ""


@dataclass(frozen=True)
class RelationHypothesis:
    """A hypothesis about the relation between two terms."""
    relation_type: str
    confidence: float = 0.0
    evidence: tuple[str, ...] = ()
    direction: str = "left_to_right"
    raw: str = ""


@dataclass(frozen=True)
class AnalogyOption:
    """A parsed answer option."""
    label: str
    pair: AnalogyPair
    text: str = ""


@dataclass
class OptionRelationAssessment:
    """Assessment of an option's relation against the stem's relation."""
    label: str
    relation_type: str | None = None
    score: float = 0.0
    matched_relations: list[str] = field(default_factory=list)
    mismatch_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AnalogyReasoningResult:
    """Result of the analogy reasoning engine."""
    status: str  # solved / ambiguous / analysis_only / inconsistent
    stem_pair: AnalogyPair | None = None
    stem_relations: list[RelationHypothesis] = field(default_factory=list)
    options: list[AnalogyOption] = field(default_factory=list)
    assessments: list[OptionRelationAssessment] = field(default_factory=list)
    option_status: str = "not_attempted"
    predicted_label: str | None = None
    confidence: float = 0.0
    warnings: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Word dictionaries for relation detection
# ---------------------------------------------------------------------------

# Opposite pairs
OPPOSITE_PAIRS: set[tuple[str, str]] = {
    ("大", "小"), ("远", "近"), ("快", "慢"), ("真", "假"), ("强", "弱"),
    ("黑", "白"), ("高", "低"), ("长", "短"), ("深", "浅"), ("新", "旧"),
    ("冷", "热"), ("轻", "重"), ("厚", "薄"), ("宽", "窄"), ("明", "暗"),
    ("上升", "下降"), ("增加", "减少"), ("开始", "结束"), ("出生", "死亡"),
    ("前进", "后退"), ("开放", "封闭"), ("进攻", "防守"), ("获得", "失去"),
    ("成功", "失败"), ("主动", "被动"), ("积极", "消极"), ("正面", "反面"),
    ("上", "下"), ("前", "后"), ("左", "右"), ("内", "外"),
    ("东", "西"), ("南", "北"), ("古", "今"), ("天", "地"),
    ("阴", "阳"), ("刚", "柔"), ("虚", "实"), ("静", "动"),
}

# Material words
MATERIAL_WORDS: set[str] = {
    "木材", "钢铁", "棉花", "玻璃", "纸张", "泥土", "矿石", "塑料",
    "铜", "铁", "铝", "金", "银", "锡", "铅", "锌", "钛", "钨",
    "棉", "麻", "丝", "毛", "皮", "革", "布", "绸", "缎", "绢",
    "木", "竹", "石", "土", "沙", "泥", "煤", "油", "气", "水",
    "纸", "布", "皮", "胶", "漆", "蜡", "盐", "糖", "酒", "茶",
}

# Product words
PRODUCT_WORDS: set[str] = {
    "桌子", "椅子", "床", "柜", "架", "箱", "包", "袋", "帽", "鞋",
    "衣", "裤", "裙", "衫", "袜", "手套", "围巾", "领带", "腰带",
    "笔", "纸", "墨", "砚", "书", "本", "册", "卷", "篇", "章",
    "碗", "盘", "杯", "壶", "瓶", "罐", "缸", "盆", "桶", "盒",
    "刀", "剪", "锤", "锯", "锉", "钻", "斧", "锄", "犁", "耙",
    "镜", "灯", "烛", "炉", "灶", "锅", "铲", "勺", "筷", "叉",
    "车", "船", "轿", "辇", "舆", "辇", "舟", "帆", "桨", "橹",
    "陶", "瓷", "砖", "瓦", "器", "皿", "具", "品", "物", "件",
    "成品", "产品", "制品", "半成品", "原料", "材料",
}

# Profession words
PROFESSION_WORDS: set[str] = {
    "医生", "教师", "律师", "司机", "农民", "警察", "记者", "会计", "裁判",
    "外交人员", "刑警", "法官", "检察官", "军人", "护士", "药剂师",
    "工程师", "建筑师", "设计师", "科学家", "作家", "画家", "音乐家",
    "演员", "导演", "主持人", "编辑", "翻译", "导游", "厨师", "理发师",
    "工匠", "木匠", "铁匠", "石匠", "瓦匠", "裁缝", "鞋匠", "钟表匠",
    "商人", "店主", "经理", "总裁", "会长", "主席", "部长", "市长",
}

# Tool words
TOOL_WORDS: set[str] = {
    "剪刀", "锤子", "笔", "尺子", "算盘", "显微镜", "望远镜", "温度计",
    "刀", "锯", "斧", "凿", "钻", "锉", "钳", "镊", "针", "线",
    "笔", "墨", "纸", "砚", "纸", "墨", "砚", "印", "章", "戳",
    "车", "船", "轿", "辇", "舟", "帆", "桨", "橹", "舵", "锚",
    "灯", "烛", "火", "炉", "灶", "锅", "铲", "勺", "筷", "叉",
    "镜", "镜", "镜", "镜", "镜", "镜", "镜", "镜", "镜", "镜",
    "钟", "表", "日晷", "沙漏", "罗盘", "指南针", "天平", "秤",
}

# Place words
PLACE_WORDS: set[str] = {
    "医院", "学校", "法院", "监狱", "银行", "商场", "市场", "工厂",
    "图书馆", "博物馆", "美术馆", "体育馆", "电影院", "剧院", "公园",
    "车站", "机场", "码头", "港口", "桥梁", "隧道", "道路", "街道",
    "城市", "乡村", "国家", "地区", "省", "市", "县", "镇", "村",
    "山", "河", "湖", "海", "岛", "峰", "谷", "平原", "高原",
    "天", "地", "日", "月", "星", "云", "风", "雨", "雪", "雷",
}

# Function words
FUNCTION_WORDS: set[str] = {
    "治疗", "教学", "审判", "运输", "种植", "巡逻", "报道", "记账",
    "裁决", "外交", "侦查", "判决", "检察", "防卫", "护理", "配药",
    "设计", "建造", "规划", "研究", "写作", "绘画", "演奏", "表演",
    "导演", "主持", "编辑", "翻译", "导游", "烹饪", "理发", "制造",
    "交易", "管理", "经营", "领导", "组织", "协调", "指挥", "控制",
    "裁剪", "缝纫", "加工", "打磨", "雕刻", "锻造", "冶炼", "烧制",
    "诊断", "手术", "化验", "检查", "注射", "包扎", "急救", "康复",
    "教学", "辅导", "批改", "出题", "考试", "评分", "授课", "培训",
    "交涉", "谈判", "签约", "出访", "接待", "陪同", "翻译", "联络",
}

# Category words (broad categories)
CATEGORY_WORDS: set[str] = {
    "动物", "植物", "矿物", "鸟类", "鱼类", "昆虫", "兽类", "爬行",
    "水果", "蔬菜", "粮食", "花卉", "树木", "草", "藤", "苔",
    "颜色", "形状", "大小", "长短", "高低", "快慢", "轻重", "冷热",
    "时间", "空间", "速度", "频率", "温度", "湿度", "压力", "密度",
    "文化", "教育", "科技", "经济", "政治", "军事", "法律", "艺术",
}

# Sequence words
SEQUENCE_WORDS: set[str] = {
    "开始", "初期", "中期", "后期", "结束", "初始", "最终", "首先",
    "其次", "然后", "接着", "最后", "先", "后", "前", "末", "终",
    "春", "夏", "秋", "冬", "早", "中", "晚", "新", "旧",
    "古", "今", "昔", "今", "往", "来", "去", "回", "返",
}

# Degree words
DEGREE_WORDS: set[str] = {
    "轻微", "轻", "中", "重", "严重", "微", "小", "大", "巨", "特",
    "标", "高", "超", "普", "通", "优", "良", "中", "差", "劣",
    "初", "中", "高", "精", "尖", "端", "基", "础", "专", "业",
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
    "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸",
}

# Purpose words
PURPOSE_WORDS: set[str] = {
    "为了", "以便", "旨在", "目的是", "用于", "用来", "以期", "期望",
    "去", "来", "以便于", "以利于", "为了达到", "为了实现", "为了满足",
}

# Causal words
CAUSAL_WORDS: set[str] = {
    "因为", "由于", "因此", "所以", "导致", "造成", "引起", "产生",
    "使得", "致使", "以致", "以至于", "从而", "进而", "于是", "结果",
}

# Whole-part words
WHOLE_PART_WORDS: set[str] = {
    "部分", "组成", "构成", "包含", "包括", "含有", "拥有", "具有",
    "部件", "组件", "零件", "配件", "部件", "组件", "零件", "配件",
    "头", "手", "脚", "眼", "耳", "鼻", "口", "心", "肝", "肺",
    "页", "章", "节", "段", "句", "词", "字", "标点", "符号",
}

# Synonym indicators
SYNONYM_INDICATORS: set[str] = {
    "同义", "近义", "类似", "相近", "相似", "相同", "一样", "一致",
    "都是", "都表示", "都指", "都意味着", "都可以表示", "都可以指",
}

# Ancient-modern meaning indicators
ANCIENT_MODERN_WORDS: set[str] = {
    "古义", "今义", "古", "今", "古代", "现代", "古代汉语", "现代汉语",
    "文言", "白话", "书面", "口语", "正式", "非正式", "雅", "俗",
}

# Naming convention words
NAMING_MATERIAL_WORDS: set[str] = {
    "铜", "铁", "铝", "金", "银", "锡", "铅", "锌", "钛", "钨",
    "木", "竹", "石", "土", "沙", "泥", "棉", "麻", "丝", "毛",
    "皮", "革", "纸", "布", "绸", "缎", "绢", "胶", "漆", "蜡",
}

NAMING_FUNCTION_WORDS: set[str] = {
    "化妆", "照明", "取暖", "降温", "装饰", "保护", "装饰", "实用",
    "观赏", "食用", "药用", "工业", "农业", "军事", "民用", "医用",
    "教学", "科研", "办公", "家用", "户外", "室内", "水上", "空中",
}

NAMING_SHAPE_WORDS: set[str] = {
    "圆", "方", "三角", "四角", "五角", "六角", "八角", "多角",
    "长", "短", "扁", "平", "凹", "凸", "弯", "直", "曲", "斜",
    "大", "小", "粗", "细", "厚", "薄", "宽", "窄", "深", "浅",
}

NAMING_COLOR_WORDS: set[str] = {
    "红", "橙", "黄", "绿", "蓝", "靛", "紫", "黑", "白", "灰",
    "粉", "棕", "褐", "金", "银", "铜", "铁", "铝", "锡", "铅",
}


# ---------------------------------------------------------------------------
# Stem parsing
# ---------------------------------------------------------------------------

_COLON_PATTERN = re.compile(r"[∶:：]")


def parse_stem(stem_text: str) -> list[AnalogyPair]:
    """Parse the stem text to extract analogy pairs.

    Supports:
    1. Two-word: "A∶B" or "A:B" or "A：B"
    2. Three-word: "A∶B∶C" or "A:B:C"
    3. Fill-in-blank: "A 对于（ ）相当于（ ）对于 B"
    4. Four-character phrase: "ABCD∶EFGH"

    Returns list of AnalogyPair. For fill-in-blank, returns the two known
    terms as a pair.
    """
    stem_text = stem_text.strip()
    pairs: list[AnalogyPair] = []

    # Fill-in-blank pattern: "A 对于（ ）相当于（ ）对于 B"
    m = re.search(
        r"(.+?)\s*对于\s*[（(]\s*[）)]\s*相当于\s*[（(]\s*[）)]\s*对于\s*(.+)",
        stem_text,
    )
    if m:
        left = m.group(1).strip()
        right = m.group(2).strip()
        return [AnalogyPair(left=left, right=right, raw=stem_text)]

    # Also support: "A 对于( )相当于 B 对于( )" or "A 对于（）相当于（）对于 B"
    m = re.search(
        r"(.+?)\s*对于\s*[（(]?\s*[）)]?\s*相当于\s*(.+?)\s*对于\s*[（(]?\s*[）)]?",
        stem_text,
    )
    if m:
        left = m.group(1).strip()
        right = m.group(2).strip()
        return [AnalogyPair(left=left, right=right, raw=stem_text)]

    # Colon-separated: A∶B or A:B or A：B
    parts = _COLON_PATTERN.split(stem_text)
    if len(parts) == 2:
        left = parts[0].strip()
        right = parts[1].strip()
        if left and right:
            return [AnalogyPair(left=left, right=right, raw=stem_text)]

    if len(parts) == 3:
        # Three-word: A∶B∶C
        # Return the full triple as a special pair with left=A, right=C, plus mid
        # Also return pairwise pairs for relation detection
        left = parts[0].strip()
        mid = parts[1].strip()
        right = parts[2].strip()
        if left and mid and right:
            # Return the full triple context and pairwise pairs
            return [
                AnalogyPair(left=left, right=right, raw=stem_text),
                AnalogyPair(left=left, right=mid, raw=stem_text),
                AnalogyPair(left=mid, right=right, raw=stem_text),
            ]

    # Fallback: try to split on common separators
    for sep in ["∶", ":", "：", "；", ";"]:
        if sep in stem_text:
            parts = stem_text.split(sep)
            if len(parts) >= 2:
                left = parts[0].strip()
                right = parts[1].strip()
                if left and right:
                    return [AnalogyPair(left=left, right=right, raw=stem_text)]

    return pairs


# ---------------------------------------------------------------------------
# Option parsing
# ---------------------------------------------------------------------------

_OPTION_LABEL_PATTERN = re.compile(r"^([A-Z])[.．、]\s*")


def parse_options(options_dict: dict[str, str]) -> list[AnalogyOption]:
    """Parse options from the options dict.

    Supports:
    1. "A. X∶Y" or "A. X:Y"
    2. "A. X∶Y∶Z"
    3. "X；Y" (semicoloned for fill-in-blank)

    Returns list of AnalogyOption.
    """
    options: list[AnalogyOption] = []

    for label, text in sorted(options_dict.items()):
        text = text.strip()

        # Extract label from text if present (e.g., "A. X∶Y" -> label="A")
        m = _OPTION_LABEL_PATTERN.match(text)
        if m:
            clean_label = m.group(1)
            text = text[m.end():]

        # Parse the pair from the option text
        pair = _parse_option_pair(text)
        if pair:
            options.append(AnalogyOption(label=label, pair=pair, text=text))
        else:
            # If we can't parse, still include the option with raw text
            options.append(AnalogyOption(
                label=label,
                pair=AnalogyPair(left="", right="", raw=text),
                text=text,
            ))

    return options


def _parse_option_pair(text: str) -> AnalogyPair | None:
    """Parse a single option text into an AnalogyPair."""
    text = text.strip()
    if not text:
        return None

    # Try colon separators
    for sep in ["∶", ":", "："]:
        if sep in text:
            parts = text.split(sep)
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip()
                if left and right:
                    return AnalogyPair(left=left, right=right, raw=text)
            elif len(parts) == 3:
                # Three-word: return first two as pair
                left = parts[0].strip()
                mid = parts[1].strip()
                right = parts[2].strip()
                if left and mid and right:
                    return AnalogyPair(left=left, right=mid, raw=text)

    # Try semicolon separator (for fill-in-blank)
    for sep in ["；", ";"]:
        if sep in text:
            parts = text.split(sep)
            if len(parts) >= 2:
                left = parts[0].strip()
                right = parts[1].strip()
                if left and right:
                    return AnalogyPair(left=left, right=right, raw=text)

    # Try comma separator
    for sep in ["，", ","]:
        if sep in text:
            parts = text.split(sep)
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip()
                if left and right:
                    return AnalogyPair(left=left, right=right, raw=text)

    return None


# ---------------------------------------------------------------------------
# Relation detection helpers
# ---------------------------------------------------------------------------

def _word_length_category(word: str) -> str:
    """Categorize word by length for structural matching."""
    if len(word) <= 2:
        return "short"
    elif len(word) <= 4:
        return "medium"
    else:
        return "long"


def _has_common_category(left: str, right: str) -> bool:
    """Check if two words share a common category."""
    left_chars = set(left)
    right_chars = set(right)
    # Check for shared characters
    if left_chars & right_chars:
        return True
    # Check for category membership
    for cat_word in CATEGORY_WORDS:
        if cat_word in left or cat_word in right:
            return True
    return False


def _is_material(word: str) -> bool:
    """Check if a word is a material."""
    return word in MATERIAL_WORDS or any(m in word for m in MATERIAL_WORDS)


def _is_product(word: str) -> bool:
    """Check if a word is a product."""
    return word in PRODUCT_WORDS or any(p in word for p in PRODUCT_WORDS)


def _is_profession(word: str) -> bool:
    """Check if a word is a profession."""
    return word in PROFESSION_WORDS or any(p in word for p in PROFESSION_WORDS)


def _is_tool(word: str) -> bool:
    """Check if a word is a tool."""
    return word in TOOL_WORDS or any(t in word for t in TOOL_WORDS)


def _is_place(word: str) -> bool:
    """Check if a word is a place."""
    return word in PLACE_WORDS or any(p in word for p in PLACE_WORDS)


def _is_function(word: str) -> bool:
    """Check if a word is a function."""
    return word in FUNCTION_WORDS or any(f in word for f in FUNCTION_WORDS)


def _check_opposite(left: str, right: str) -> bool:
    """Check if two words are opposites."""
    # Direct pair check
    if (left, right) in OPPOSITE_PAIRS or (right, left) in OPPOSITE_PAIRS:
        return True
    # Character-level check
    left_chars = set(left)
    right_chars = set(right)
    for l_char in left_chars:
        for r_char in right_chars:
            if (l_char, r_char) in OPPOSITE_PAIRS or (r_char, l_char) in OPPOSITE_PAIRS:
                return True
    return False


def _check_naming_convention(left: str, right: str) -> tuple[bool, str]:
    """Check if two words use different naming conventions.

    Returns (is_naming_convention, description).
    """
    left_is_material = any(m in left for m in NAMING_MATERIAL_WORDS)
    right_is_material = any(m in right for m in NAMING_MATERIAL_WORDS)

    left_is_function = any(f in left for f in NAMING_FUNCTION_WORDS)
    right_is_function = any(f in right for f in NAMING_FUNCTION_WORDS)

    left_is_shape = any(s in left for s in NAMING_SHAPE_WORDS)
    right_is_shape = any(s in right for s in NAMING_SHAPE_WORDS)

    left_is_color = any(c in left for c in NAMING_COLOR_WORDS)
    right_is_color = any(c in right for c in NAMING_COLOR_WORDS)

    # Check for different naming criteria
    criteria_left: list[str] = []
    criteria_right: list[str] = []

    if left_is_material:
        criteria_left.append("material")
    if left_is_function:
        criteria_left.append("function")
    if left_is_shape:
        criteria_left.append("shape")
    if left_is_color:
        criteria_left.append("color")

    if right_is_material:
        criteria_right.append("material")
    if right_is_function:
        criteria_right.append("function")
    if right_is_shape:
        criteria_right.append("shape")
    if right_is_color:
        criteria_right.append("color")

    # If both have criteria but they're different, it's naming_convention
    if criteria_left and criteria_right:
        if set(criteria_left) != set(criteria_right):
            return True, f"left_naming={criteria_left}, right_naming={criteria_right}"

    return False, ""


# ---------------------------------------------------------------------------
# Relation detection functions
# ---------------------------------------------------------------------------

def detect_relation_opposite(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect opposite relation."""
    if _check_opposite(pair.left, pair.right):
        return RelationHypothesis(
            relation_type="opposite",
            confidence=0.9,
            evidence=(pair.left, pair.right),
            raw=pair.raw,
        )
    return None


def detect_relation_same_category(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect same category relation."""
    # Check if both words belong to the same category
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    # Check direct category membership
    for cat in CATEGORY_WORDS:
        if cat in left_lower and cat in right_lower:
            return RelationHypothesis(
                relation_type="same_category",
                confidence=0.8,
                evidence=(pair.left, pair.right, cat),
                raw=pair.raw,
            )

    # Check if they share a common character that indicates category
    left_chars = set(pair.left)
    right_chars = set(pair.right)
    common = left_chars & right_chars
    if common and len(common) >= 1:
        # Check if common characters are category indicators
        for char in common:
            if any(char in cat for cat in CATEGORY_WORDS):
                return RelationHypothesis(
                    relation_type="same_category",
                    confidence=0.6,
                    evidence=(pair.left, pair.right, char),
                    raw=pair.raw,
                )

    return None


def detect_relation_synonym(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect synonym relation."""
    # Check for synonym indicators in evidence
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    for indicator in SYNONYM_INDICATORS:
        if indicator in left_lower or indicator in right_lower:
            return RelationHypothesis(
                relation_type="synonym",
                confidence=0.8,
                evidence=(pair.left, pair.right, indicator),
                raw=pair.raw,
            )

    return None


def detect_relation_species_genus(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect species-genus (hyponymy) relation."""
    # Check if one word is a specific instance of the other's category
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    # Check if left is a species and right is a genus
    for cat in CATEGORY_WORDS:
        if cat in right_lower and len(pair.left) > len(cat):
            # Left might be a species of the category in right
            return RelationHypothesis(
                relation_type="species_genus",
                confidence=0.7,
                evidence=(pair.left, pair.right, cat),
                direction="left_to_right",
                raw=pair.raw,
            )
        if cat in left_lower and len(pair.right) > len(cat):
            # Right might be a species of the category in left
            return RelationHypothesis(
                relation_type="species_genus",
                confidence=0.7,
                evidence=(pair.left, pair.right, cat),
                direction="right_to_left",
                raw=pair.raw,
            )

    return None


def detect_relation_whole_part(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect whole-part relation."""
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    for indicator in WHOLE_PART_WORDS:
        if indicator in left_lower:
            return RelationHypothesis(
                relation_type="whole_part",
                confidence=0.7,
                evidence=(pair.left, pair.right, indicator),
                direction="left_to_right",
                raw=pair.raw,
            )
        if indicator in right_lower:
            return RelationHypothesis(
                relation_type="whole_part",
                confidence=0.7,
                evidence=(pair.left, pair.right, indicator),
                direction="right_to_left",
                raw=pair.raw,
            )

    return None


def detect_relation_material_product(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect material-product relation."""
    left_is_mat = _is_material(pair.left)
    right_is_prod = _is_product(pair.right)
    left_is_prod = _is_product(pair.left)
    right_is_mat = _is_material(pair.right)

    if left_is_mat and right_is_prod:
        return RelationHypothesis(
            relation_type="material_product",
            confidence=0.8,
            evidence=(pair.left, pair.right),
            direction="left_to_right",
            raw=pair.raw,
        )
    if left_is_prod and right_is_mat:
        return RelationHypothesis(
            relation_type="material_product",
            confidence=0.8,
            evidence=(pair.left, pair.right),
            direction="right_to_left",
            raw=pair.raw,
        )

    # Pattern: both share a material substring, but one has a raw/processed prefix
    # Pattern: "原X" = raw material, "processedX" = product
    # Detect by checking if both share a material substring and one has "原" prefix
    RAW_PREFIXES = {"原", "粗", "生", "毛", "初"}

    left_lower = pair.left
    right_lower = pair.right

    for mat in MATERIAL_WORDS:
        if mat in left_lower and mat in right_lower:
            # Both contain the same material word
            left_is_raw = any(left_lower.startswith(p) for p in RAW_PREFIXES)
            right_is_raw = any(right_lower.startswith(p) for p in RAW_PREFIXES)

            # One has raw prefix, the other doesn't → material→product
            if left_is_raw and not right_is_raw:
                return RelationHypothesis(
                    relation_type="material_product",
                    confidence=0.8,
                    evidence=(pair.left, pair.right, mat),
                    direction="left_to_right",
                    raw=pair.raw,
                )
            if right_is_raw and not left_is_raw:
                return RelationHypothesis(
                    relation_type="material_product",
                    confidence=0.8,
                    evidence=(pair.left, pair.right, mat),
                    direction="right_to_left",
                    raw=pair.raw,
                )

    return None


def detect_relation_tool_function(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect tool-function relation."""
    left_is_tool = _is_tool(pair.left)
    right_is_func = _is_function(pair.right)
    left_is_func = _is_function(pair.left)
    right_is_tool = _is_tool(pair.right)

    if left_is_tool and right_is_func:
        return RelationHypothesis(
            relation_type="tool_function",
            confidence=0.8,
            evidence=(pair.left, pair.right),
            direction="left_to_right",
            raw=pair.raw,
        )
    if left_is_func and right_is_tool:
        return RelationHypothesis(
            relation_type="tool_function",
            confidence=0.8,
            evidence=(pair.left, pair.right),
            direction="right_to_left",
            raw=pair.raw,
        )

    return None


def detect_relation_profession_object(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect profession-object relation."""
    # Extended object words for profession-object pairs
    _PROFESSION_OBJECTS = {
        "患者", "病人", "学员", "学生", "顾客", "客户", "当事人",
        "被告", "原告", "嫌疑人", "罪犯", "乘客", "观众", "读者",
        "听众", "选民", "居民", "村民", "市民", "国民", "公众",
    }
    left_is_prof = _is_profession(pair.left)
    right_is_obj = _is_product(pair.right) or _is_place(pair.right) or pair.right in _PROFESSION_OBJECTS
    left_is_obj = _is_product(pair.left) or _is_place(pair.left) or pair.left in _PROFESSION_OBJECTS
    right_is_prof = _is_profession(pair.right)

    if left_is_prof and right_is_obj:
        return RelationHypothesis(
            relation_type="profession_object",
            confidence=0.7,
            evidence=(pair.left, pair.right),
            direction="left_to_right",
            raw=pair.raw,
        )
    if left_is_obj and right_is_prof:
        return RelationHypothesis(
            relation_type="profession_object",
            confidence=0.7,
            evidence=(pair.left, pair.right),
            direction="right_to_left",
            raw=pair.raw,
        )

    return None


def detect_relation_place_function(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect place-function relation."""
    left_is_place = _is_place(pair.left)
    right_is_func = _is_function(pair.right)
    left_is_func = _is_function(pair.left)
    right_is_place = _is_place(pair.right)

    if left_is_place and right_is_func:
        return RelationHypothesis(
            relation_type="place_function",
            confidence=0.7,
            evidence=(pair.left, pair.right),
            direction="left_to_right",
            raw=pair.raw,
        )
    if left_is_func and right_is_place:
        return RelationHypothesis(
            relation_type="place_function",
            confidence=0.7,
            evidence=(pair.left, pair.right),
            direction="right_to_left",
            raw=pair.raw,
        )

    return None


def detect_relation_cause_effect(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect cause-effect relation."""
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    for indicator in CAUSAL_WORDS:
        if indicator in left_lower:
            return RelationHypothesis(
                relation_type="cause_effect",
                confidence=0.7,
                evidence=(pair.left, pair.right, indicator),
                direction="left_to_right",
                raw=pair.raw,
            )
        if indicator in right_lower:
            return RelationHypothesis(
                relation_type="cause_effect",
                confidence=0.7,
                evidence=(pair.left, pair.right, indicator),
                direction="right_to_left",
                raw=pair.raw,
            )

    return None


def detect_relation_process_result(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect process-result relation."""
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    process_indicators = {
        "过程", "步骤", "方法", "手段", "途径", "方式",
        "加工", "制造", "生产", "制作", "建造", "修建",
        "烹饪", "缝纫", "编织", "冶炼", "锻造", "烧制",
        "处理", "加工", "处理", "清洗", "消毒", "整理",
    }
    result_indicators = {
        "结果", "效果", "成果", "成就", "结局", "收获",
        "成品", "产品", "制品", "半成品", "产出", "产量",
        "作品", "产物", "结晶", "果实", "收获", "成效",
    }

    for ind in process_indicators:
        if ind in left_lower:
            return RelationHypothesis(
                relation_type="process_result",
                confidence=0.6,
                evidence=(pair.left, pair.right, ind),
                direction="left_to_right",
                raw=pair.raw,
            )

    for ind in result_indicators:
        if ind in right_lower:
            return RelationHypothesis(
                relation_type="process_result",
                confidence=0.6,
                evidence=(pair.left, pair.right, ind),
                direction="left_to_right",
                raw=pair.raw,
            )

    return None


def detect_relation_sequence(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect sequence/temporal ordering relation."""
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    left_has_seq = any(w in left_lower for w in SEQUENCE_WORDS)
    right_has_seq = any(w in right_lower for w in SEQUENCE_WORDS)

    if left_has_seq or right_has_seq:
        # Determine direction based on word positions
        left_idx = -1
        right_idx = -1
        seq_list = list(SEQUENCE_WORDS)

        for i, w in enumerate(seq_list):
            if w in left_lower:
                left_idx = i
            if w in right_lower:
                right_idx = i

        direction = "left_to_right"
        if left_idx >= 0 and right_idx >= 0:
            if left_idx > right_idx:
                direction = "right_to_left"

        return RelationHypothesis(
            relation_type="sequence",
            confidence=0.7,
            evidence=(pair.left, pair.right),
            direction=direction,
            raw=pair.raw,
        )

    return None


def detect_relation_degree(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect degree/scale progression relation."""
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    left_has_deg = any(w in left_lower for w in DEGREE_WORDS)
    right_has_deg = any(w in right_lower for w in DEGREE_WORDS)

    if left_has_deg or right_has_deg:
        return RelationHypothesis(
            relation_type="degree",
            confidence=0.6,
            evidence=(pair.left, pair.right),
            raw=pair.raw,
        )

    return None


def detect_relation_purpose(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect purpose relation."""
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    for indicator in PURPOSE_WORDS:
        if indicator in left_lower or indicator in right_lower:
            return RelationHypothesis(
                relation_type="purpose",
                confidence=0.7,
                evidence=(pair.left, pair.right, indicator),
                raw=pair.raw,
            )

    # Check for four-character phrase structure: both phrases have internal purpose
    # Pattern: four-char phrases with parallel structure
    # Both phrases follow: [means][action][goal]
    if len(pair.left) == 4 and len(pair.right) == 4:
        # Check if both phrases have action characters in similar positions
        action_chars = {"去", "治", "除", "消", "灭", "破", "立", "建", "造", "创",
                        "修", "养", "保", "护", "守", "防", "御", "攻", "击", "伐",
                        "兴", "振", "举", "推", "促", "助", "辅", "佐", "扶", "援"}
        left_has_action = any(c in pair.left for c in action_chars)
        right_has_action = any(c in pair.right for c in action_chars)

        if left_has_action and right_has_action:
            # Both phrases have action words → likely parallel purpose structure
            return RelationHypothesis(
                relation_type="purpose",
                confidence=0.8,
                evidence=(pair.left, pair.right),
                raw=pair.raw,
            )

        # Check for "以X去Y" or "用X治Y" pattern
        purpose_patterns = ["以", "用", "为", "因", "由"]
        left_has_purpose = any(c in pair.left for c in purpose_patterns)
        right_has_purpose = any(c in pair.right for c in purpose_patterns)
        if left_has_purpose and right_has_purpose:
            return RelationHypothesis(
                relation_type="purpose",
                confidence=0.7,
                evidence=(pair.left, pair.right),
                raw=pair.raw,
            )

    return None


def detect_relation_grammar_structure(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect grammatical structure relation (subject-predicate, verb-object, etc.)."""
    # Check if both words have similar grammatical structure
    left_len = len(pair.left)
    right_len = len(pair.right)

    # Simple structural matching based on length
    if left_len == right_len:
        # Check for common structural patterns
        # Subject-predicate: both have noun + verb
        # Verb-object: both have verb + noun
        # Modifier-head: both have adjective/noun + noun

        # For now, use a simple heuristic based on character overlap
        left_chars = set(pair.left)
        right_chars = set(pair.right)
        overlap = left_chars & right_chars

        if len(overlap) >= 1:
            return RelationHypothesis(
                relation_type="grammar_structure",
                confidence=0.4,
                evidence=(pair.left, pair.right, *overlap),
                raw=pair.raw,
            )

    return None


def detect_relation_cross_relation(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect cross-relation (items share category but classified by different criteria)."""
    # Check if both items can be categorized in overlapping but different ways
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    # Check for overlapping categories
    left_cats: list[str] = []
    right_cats: list[str] = []

    for cat in CATEGORY_WORDS:
        if cat in left_lower:
            left_cats.append(cat)
        if cat in right_lower:
            right_cats.append(cat)

    # If they share some categories but also have different ones
    if left_cats and right_cats:
        common = set(left_cats) & set(right_cats)
        left_only = set(left_cats) - set(right_cats)
        right_only = set(right_cats) - set(left_cats)

        if common and (left_only or right_only):
            return RelationHypothesis(
                relation_type="cross_relation",
                confidence=0.5,
                evidence=(pair.left, pair.right, *common),
                raw=pair.raw,
            )

    return None


def detect_relation_naming_convention(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect naming convention relation."""
    is_naming, desc = _check_naming_convention(pair.left, pair.right)
    if is_naming:
        return RelationHypothesis(
            relation_type="naming_convention",
            confidence=0.7,
            evidence=(pair.left, pair.right, desc),
            raw=pair.raw,
        )
    return None


def detect_relation_aggregation(pair: AnalogyPair) -> RelationHypothesis | None:
    """Detect aggregation relation (parts sum to whole)."""
    left_lower = pair.left.lower()
    right_lower = pair.right.lower()

    # Check for aggregation indicators
    agg_indicators = {"小计", "总计", "合计", "合计", "总", "分", "部分", "整体"}
    for ind in agg_indicators:
        if ind in left_lower or ind in right_lower:
            return RelationHypothesis(
                relation_type="aggregation",
                confidence=0.7,
                evidence=(pair.left, pair.right, ind),
                raw=pair.raw,
            )

    return None


# ---------------------------------------------------------------------------
# Main relation detection
# ---------------------------------------------------------------------------

def detect_all_relations(pair: AnalogyPair) -> list[RelationHypothesis]:
    """Detect all possible relations for an analogy pair.

    Returns a list of RelationHypothesis objects, sorted by confidence.
    """
    hypotheses: list[RelationHypothesis] = []

    # Run all detectors
    detectors = [
        detect_relation_opposite,
        detect_relation_same_category,
        detect_relation_synonym,
        detect_relation_species_genus,
        detect_relation_whole_part,
        detect_relation_material_product,
        detect_relation_tool_function,
        detect_relation_profession_object,
        detect_relation_place_function,
        detect_relation_cause_effect,
        detect_relation_process_result,
        detect_relation_sequence,
        detect_relation_degree,
        detect_relation_purpose,
        detect_relation_grammar_structure,
        detect_relation_cross_relation,
        detect_relation_naming_convention,
        detect_relation_aggregation,
    ]

    for detector in detectors:
        result = detector(pair)
        if result is not None:
            hypotheses.append(result)

    # Sort by confidence (descending)
    hypotheses.sort(key=lambda h: h.confidence, reverse=True)

    # If no relations detected, add unknown
    if not hypotheses:
        hypotheses.append(RelationHypothesis(
            relation_type="unknown",
            confidence=0.0,
            evidence=(pair.left, pair.right),
            raw=pair.raw,
        ))

    return hypotheses


# ---------------------------------------------------------------------------
# Option matching
# ---------------------------------------------------------------------------

def assess_option(
    option: AnalogyOption,
    stem_relations: list[RelationHypothesis],
    stem_pair: AnalogyPair,
) -> OptionRelationAssessment:
    """Assess an option against the stem's relation.

    Returns an OptionRelationAssessment with matching information.
    """
    assessment = OptionRelationAssessment(label=option.label)

    # Detect relations for the option
    option_relations = detect_all_relations(option.pair)

    # Check structural compatibility
    stem_left_len = len(stem_pair.left) if stem_pair else 0
    stem_right_len = len(stem_pair.right) if stem_pair else 0
    opt_left_len = len(option.pair.left)
    opt_right_len = len(option.pair.right)

    stem_struct = _word_length_category(stem_pair.left + stem_pair.right) if stem_pair else "unknown"
    opt_struct = _word_length_category(option.pair.left + option.pair.right)

    # Compare relations
    best_match_score = 0.0
    best_match_type = None

    for stem_rel in stem_relations:
        for opt_rel in option_relations:
            score = 0.0

            # Exact relation type match
            if stem_rel.relation_type == opt_rel.relation_type:
                score += 1.0

                # Direction match
                if stem_rel.direction == opt_rel.direction:
                    score += 0.5
                elif stem_rel.direction == "left_to_right" and opt_rel.direction == "right_to_left":
                    # Reverse direction is still a match
                    score += 0.3

                # Structure compatibility
                if stem_struct == opt_struct:
                    score += 0.2

                # Confidence weighting
                score *= (stem_rel.confidence + opt_rel.confidence) / 2

                if score > best_match_score:
                    best_match_score = score
                    best_match_type = opt_rel.relation_type
                    assessment.matched_relations = [opt_rel.relation_type]

    # Set assessment results
    assessment.score = best_match_score
    assessment.relation_type = best_match_type

    # Add mismatch reasons if no match
    if best_match_score == 0:
        stem_types = [r.relation_type for r in stem_relations]
        opt_types = [r.relation_type for r in option_relations]
        assessment.mismatch_reasons = [
            f"stem_relations={stem_types}, option_relations={opt_types}"
        ]

    # Add trace
    assessment.trace.append({
        "option_label": option.label,
        "option_left": option.pair.left,
        "option_right": option.pair.right,
        "option_relations": [r.relation_type for r in option_relations],
        "match_score": best_match_score,
        "match_type": best_match_type,
    })

    return assessment


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def _detect_three_word_structure(pairs: list[AnalogyPair]) -> list[RelationHypothesis]:
    """Detect structural relations for three-word stems.

    For A∶B∶C, analyze the full chain:
    - A and B are both sub-types of C (cross_relation)
    - B causes A, C is a symptom (cause_effect chain)
    - A, B, C form a sequence or degree progression
    - A and B are both sub-categories that cross with C
    """
    if len(pairs) < 3:
        return []

    # pairs[0] = (A, C), pairs[1] = (A, B), pairs[2] = (B, C)
    first_pair = pairs[0]   # A:C
    second_pair = pairs[1]  # A:B
    third_pair = pairs[2]   # B:C

    relations: list[RelationHypothesis] = []

    # Detect cross_relation: A and B both cross with C
    # e.g., A and B both cross with C
    rel_ab = detect_all_relations(second_pair)
    rel_bc = detect_all_relations(third_pair)
    rel_ac = detect_all_relations(first_pair)

    # Check if A and B have similar relation to C (cross pattern)
    ab_types = {r.relation_type for r in rel_ab}
    bc_types = {r.relation_type for r in rel_bc}

    # If A:B and B:C share relation types, it's a chain
    common_types = ab_types & bc_types
    if common_types:
        for t in common_types:
            relations.append(RelationHypothesis(
                relation_type=t,
                confidence=0.8,
                evidence=(first_pair.left, second_pair.right, third_pair.right),
                raw=first_pair.raw,
            ))

    # Detect degree/sequence chain
    for r in rel_ab:
        if r.relation_type in ("degree", "sequence"):
            relations.append(r)
    for r in rel_bc:
        if r.relation_type in ("degree", "sequence"):
            relations.append(r)

    return relations


def _assess_three_word_option(
    option_text: str,
    stem_structure: list[RelationHypothesis],
    stem_pairs: list[AnalogyPair],
) -> float:
    """Assess a three-word option against a three-word stem structure.

    Returns a match score.
    """
    # Parse option as three-word
    opt_parts = _COLON_PATTERN.split(option_text)
    if len(opt_parts) != 3:
        return 0.0

    opt_left = opt_parts[0].strip()
    opt_mid = opt_parts[1].strip()
    opt_right = opt_parts[2].strip()

    if not (opt_left and opt_mid and opt_right):
        return 0.0

    # Create option pairs
    opt_pairs = [
        AnalogyPair(left=opt_left, right=opt_right, raw=option_text),
        AnalogyPair(left=opt_left, right=opt_mid, raw=option_text),
        AnalogyPair(left=opt_mid, right=opt_right, raw=option_text),
    ]

    # Detect option structure
    opt_structure = _detect_three_word_structure(opt_pairs)

    # Compare structures
    stem_types = {r.relation_type for r in stem_structure}
    opt_types = {r.relation_type for r in opt_structure}

    if not stem_types or not opt_types:
        return 0.0

    # Score based on overlapping relation types
    common = stem_types & opt_types
    if not common:
        return 0.0

    # Base score from common relation types
    score = len(common) / max(len(stem_types), len(opt_types))

    # Bonus for matching structure (both three-word)
    score += 0.2

    return min(score, 1.0)


def solve_analogy_reasoning_core(case: dict[str, Any]) -> AnalogyReasoningResult:
    """Solve analogy reasoning case using rule-based approach.

    Args:
        case: Dictionary containing:
            - stem: str (the stem text)
            - options: dict[str, str] (label -> option text)
            - question_text: str (optional, full question text)

    Returns:
        AnalogyReasoningResult with status:
        - solved + unique_supported: Exactly one option matches well
        - ambiguous: Multiple options match equally well
        - analysis_only: No option matches reliably, or stem parsing failed
        - inconsistent: Structural anomaly
    """
    warnings: list[str] = []
    trace: list[dict[str, Any]] = []

    # Extract inputs
    stem_text = case.get("stem", "")
    options_dict = case.get("options", {})
    question_text = case.get("question_text", "")

    # Parse stem
    stem_pairs = parse_stem(stem_text)

    if not stem_pairs:
        warnings.append("failed_to_parse_stem")
        return AnalogyReasoningResult(
            status="analysis_only",
            warnings=warnings,
            trace=trace,
        )

    # For fill-in-blank or single pair, use the first pair
    stem_pair = stem_pairs[0]

    # Detect relations for stem
    stem_relations = detect_all_relations(stem_pair)

    # Check if this is a three-word stem
    is_three_word = len(stem_pairs) >= 3
    three_word_structure: list[RelationHypothesis] = []
    if is_three_word:
        three_word_structure = _detect_three_word_structure(stem_pairs)
        # Add three-word structure relations to stem_relations
        stem_relations = list(set(stem_relations + three_word_structure))

    trace.append({
        "stem_left": stem_pair.left,
        "stem_right": stem_pair.right,
        "stem_relations": [r.relation_type for r in stem_relations],
        "is_three_word": is_three_word,
        "three_word_structure": [r.relation_type for r in three_word_structure],
    })

    # Parse options
    if not options_dict:
        warnings.append("no_options_provided")
        return AnalogyReasoningResult(
            status="analysis_only",
            stem_pair=stem_pair,
            stem_relations=stem_relations,
            warnings=warnings,
            trace=trace,
        )

    options = parse_options(options_dict)

    # Assess each option
    assessments: list[OptionRelationAssessment] = []
    for opt in options:
        # For three-word stems, use specialized three-word assessment
        if is_three_word and three_word_structure:
            three_word_score = _assess_three_word_option(
                opt.text, three_word_structure, stem_pairs
            )
            # Also do regular pairwise assessment
            assessment = assess_option(opt, stem_relations, stem_pair)
            # Boost score if three-word structure matches
            if three_word_score > 0:
                assessment.score = max(assessment.score, three_word_score)
                assessment.matched_relations.append("three_word_structure")
        else:
            assessment = assess_option(opt, stem_relations, stem_pair)
        assessments.append(assessment)

    # Determine result
    predicted_label = None
    option_status = "not_attempted"
    confidence = 0.0

    # Sort assessments by score
    scored = sorted(assessments, key=lambda a: a.score, reverse=True)

    # Conservative: require strong, clear match to predict
    # Only allow prediction when stem has exactly ONE safe relation type
    stem_rel_types = {r.relation_type for r in stem_relations if r.relation_type != "unknown"}

    # Safe relation types: structural/material relations that are reliably detected
    SAFE_RELATION_TYPES = {
        "material_product", "naming_convention", "aggregation",
        "species_genus", "whole_part", "tool_function",
        "profession_object", "place_function", "process_result",
    }

    # Weak/risky relation types that alone are not sufficient to predict
    WEAK_RELATION_TYPES = {"sequence", "degree", "grammar_structure", "unknown", "purpose", "cause_effect"}

    # Check if only safe relations and no weak ones
    safe_types = stem_rel_types & SAFE_RELATION_TYPES
    weak_types = stem_rel_types & WEAK_RELATION_TYPES
    has_only_safe = len(safe_types) >= 1 and len(weak_types) == 0

    if scored and scored[0].score > 0:
        top_score = scored[0].score
        second_score = scored[1].score if len(scored) > 1 else 0
        score_gap = top_score - second_score

        # Require: only safe relations, high score, big gap, not three-word
        if (
            has_only_safe
            and top_score >= 0.75
            and score_gap >= 0.25
            and not is_three_word
        ):
            predicted_label = scored[0].label
            option_status = "unique_supported"
            confidence = top_score
        elif top_score > 0:
            option_status = "ambiguous"
            confidence = top_score
        else:
            option_status = "no_supported_option"
    else:
        option_status = "no_supported_option"

    # Determine overall status
    status = "analysis_only"
    if option_status == "unique_supported":
        status = "solved"
    elif option_status == "ambiguous":
        status = "ambiguous"
    elif option_status == "no_supported_option":
        status = "analysis_only"

    return AnalogyReasoningResult(
        status=status,
        stem_pair=stem_pair,
        stem_relations=stem_relations,
        options=options,
        assessments=assessments,
        option_status=option_status,
        predicted_label=predicted_label,
        confidence=confidence,
        warnings=warnings,
        trace=trace,
    )
