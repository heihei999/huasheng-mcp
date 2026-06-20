"""Graphic reasoning method scaffold for multi-modal LLM guidance.

This module constructs observation scaffolds for 图形推理 (graphic reasoning)
questions. It is NOT a solver. It does NOT recognize images. It does NOT
output answers. It only generates structured guidance for future multi-modal
LLM integration.

Version: v0.1
"""

from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_graphic_reasoning_scaffold() -> dict[str, Any]:
    """Build the complete graphic reasoning method scaffold.

    Returns a stable, testable dict containing stage order, composition
    router, visual checklists, response template, uncertainty policy,
    and must-not-do constraints.
    """
    return {
        "module": "graphic_reasoning",
        "version": "v0.1",
        "mode": "method_scaffold_only",
        "positioning": _build_positioning(),
        "stage_order": get_graphic_reasoning_stage_order(),
        "composition_router": _build_composition_router(),
        "visual_checklists": get_graphic_reasoning_visual_checklists(),
        "response_template": render_graphic_reasoning_prompt_template(),
        "uncertainty_policy": _build_uncertainty_policy(),
        "must_not_do": _build_must_not_do(),
    }


def get_graphic_reasoning_stage_order() -> list[str]:
    """Return the ten-layer observation order for graphic reasoning."""
    return [
        "命题形式",
        "组成关系",
        "属性规律",
        "数量规律",
        "位置规律",
        "样式规律",
        "特殊题型",
        "空间类题型",
        "选项验证",
        "不确定性约束",
    ]


def get_graphic_reasoning_visual_checklists() -> dict[str, Any]:
    """Return all visual checklists for graphic reasoning."""
    return {
        "命题形式": _checklist_proposition_form(),
        "属性规律": _checklist_attribute_rules(),
        "数量规律": _checklist_quantity_rules(),
        "位置规律": _checklist_position_rules(),
        "样式规律": _checklist_style_rules(),
        "图形间关系": _checklist_inter_figure_relations(),
        "功能元素": _checklist_functional_elements(),
        "黑白块": _checklist_black_white_blocks(),
        "汉字类": _checklist_chinese_characters(),
        "数字类": _checklist_digits(),
        "字母类": _checklist_letters(),
        "六面体展开图": _checklist_cube_net(),
        "截面图": _checklist_cross_section(),
        "三视图": _checklist_three_views(),
        "立体拼合": _checklist_solid_assembly(),
    }


def render_graphic_reasoning_prompt_template() -> str:
    """Render a prompt template for multi-modal LLM graphic reasoning."""
    return (
        "你是图形推理多模态观察助手。\n"
        "\n"
        "【命题形式】\n"
        "说明是一组图、两组图、九宫格、分组分类、空间重构还是其他形式。\n"
        "\n"
        "【组成判断】\n"
        "说明图形组成是相同、相似、不同，还是特殊图形。\n"
        "\n"
        "【优先规律】\n"
        "根据组成判断，选择位置、样式、属性、数量、特殊或空间类路径。\n"
        "\n"
        "【视觉证据】\n"
        "逐条列出从图中看到的证据，例如数量、位置、方向、对称、曲直、开闭、黑白块、公共边等。\n"
        "必须列出视觉证据，不得跳过。\n"
        "\n"
        "【候选规律】\n"
        "提出最多 1-2 个候选规律，并说明为什么成立。\n"
        "\n"
        "【选项验证】\n"
        "逐一验证 A/B/C/D 是否符合候选规律。\n"
        "\n"
        "【唯一性判断】\n"
        "如果唯一，输出答案；如果不唯一，输出 analysis_only。\n"
        "只有唯一选项满足规律时才能输出答案。\n"
        "不唯一时输出 analysis_only，不得强行猜答案。\n"
        "\n"
        "【不确定性说明】\n"
        "说明哪些图形细节看不清，哪些规律不能唯一确定。\n"
        "不得默认选择第一个选项。\n"
        "不得只说'看起来像'，必须指出视觉依据。\n"
    )


# ---------------------------------------------------------------------------
# Internal builders
# ---------------------------------------------------------------------------


def _build_positioning() -> dict[str, str]:
    """Build the positioning description."""
    return {
        "is_solver": False,
        "is_image_recognizer": False,
        "outputs_answer": False,
        "description": (
            "本模块不是 solver，不识别图像，不直接输出答案。"
            "本模块用于约束多模态大模型按图推方法论观察、说明视觉证据、"
            "验证选项，并在无法唯一时 analysis_only。"
        ),
    }


def _build_composition_router() -> dict[str, dict[str, Any]]:
    """Build the composition-based routing rules."""
    return {
        "组成相同": {
            "priority": "位置规律",
            "patterns": ["平移", "旋转", "翻转", "移动路径", "方向变化", "内外位置变化"],
            "constraint": "组成相同时，不要一上来数点线面；优先检查位置变化。",
        },
        "组成相似": {
            "priority": "样式规律",
            "patterns": ["遍历", "加减同异", "去同存异", "去异存同", "黑白运算", "局部替换"],
            "constraint": "组成相似时，不要一上来数数量；优先检查样式变化。",
        },
        "组成不同": {
            "priority": "属性和数量",
            "patterns": ["点", "线", "面", "角", "素", "一笔画", "封闭开放", "对称", "曲直"],
            "constraint": "组成不同时，再系统检查属性和数量。",
        },
        "特殊图形": {
            "priority": "专项检查",
            "patterns": [
                "黑白块", "汉字", "数字", "字母", "功能元素",
                "六面体展开图", "截面图", "三视图", "立体拼合",
            ],
            "constraint": "特殊图形优先触发专项检查。",
        },
    }


def _build_uncertainty_policy() -> dict[str, str]:
    """Build the uncertainty policy."""
    return {
        "rule_not_unified": "规律无法统一解释题干图形 → analysis_only",
        "multiple_options_match": "两个及以上选项都符合候选规律 → analysis_only",
        "unreliable_detail": "必须依赖无法确认的小图细节 → analysis_only",
        "unreliable_recognition": "图形识别结果不可靠 → analysis_only",
        "fold_ambiguous": "空间折叠无法唯一排除 → analysis_only",
        "bw_table_uncertain": "黑白运算表无法唯一确定 → analysis_only",
    }


def _build_must_not_do() -> list[str]:
    """Build the must-not-do constraints."""
    return [
        "不得默认选择第一个选项",
        "不得在无法唯一排除时强行给答案",
        "不得用题号、case_id 或标准答案写规则",
        "不得跳过视觉证据说明",
        "不得只说'看起来像'，必须指出视觉依据",
        "不得把图推 scaffold 当成本地图像 solver",
        "不得引入 OCR、OpenCV、PIL 或机器学习依赖",
    ]


# ---------------------------------------------------------------------------
# Visual checklists
# ---------------------------------------------------------------------------


def _checklist_proposition_form() -> dict[str, Any]:
    """Proposition form checklist."""
    return {
        "forms": ["一组图", "两组图", "九宫格", "分组分类", "类比式图推", "空间重构"],
        "guidance": {
            "一组图": "按从左到右寻找递推、周期、数量或位置变化。",
            "两组图": "先看第一组内部规律，再迁移到第二组。",
            "九宫格": "优先横向看，再纵向看，必要时看 S 型、米字型或中心对称关系。",
            "分组分类": "先找每组内部共同点，再找两组之间差异点。",
            "空间重构": "优先看相对面、公共边、公共点和选项可排除点。",
        },
    }


def _checklist_attribute_rules() -> dict[str, Any]:
    """Attribute rules checklist."""
    return {
        "对称性": {
            "types": ["轴对称", "中心对称", "轴对称 + 中心对称"],
            "checks": ["对称轴数量", "对称轴方向", "对称轴与图形中线条/点/面的关系"],
            "hint_shapes": ["Z", "S", "风车", "太极", "平行四边形", "正三角形", "田字格", "五角星", "正六边形"],
        },
        "开闭性": {
            "types": ["开放图形", "封闭图形", "半开半闭图形"],
            "checks": ["封闭区域是否存在缺口", "图形是否完全围成封闭空间"],
        },
        "曲直性": {
            "types": ["全曲线", "全直线", "曲线 + 直线"],
            "checks": ["内部曲直", "外部曲直", "曲直交替", "曲线数量", "直线数量"],
        },
    }


def _checklist_quantity_rules() -> dict[str, Any]:
    """Quantity rules checklist."""
    return {
        "点": {
            "types": ["交点", "端点", "切点", "出头点", "曲直交点", "内部交点", "外框交点", "公共点", "功能点"],
            "notes": [
                "出头点不一定都算交点，需要看题组是否统一。",
                "端点是否计数要结合题组规律。",
                "点数量题常与一笔画、线段、功能元素结合。",
            ],
        },
        "线": {
            "types": [
                "直线数量", "曲线数量", "线段数量", "横线", "竖线", "斜线",
                "平行线", "平行线组", "垂直线", "公共边", "公共线",
                "连接线", "延伸线", "组成封闭面的线", "图形间相交于线",
            ],
        },
        "面": {
            "types": [
                "封闭面总数", "最大面形状", "最大面面积", "最大面属性",
                "最大面与外框是否相似", "部分面数量", "三角形面数量",
                "四边形面数量", "特殊形状面数量",
            ],
        },
        "角": {
            "types": ["角总数", "直角数", "锐角数", "钝角数", "最大角", "最小角", "角方向"],
            "hint": "电话卡、垂线、三角形、折线图形常提示直角数。",
        },
        "素": {
            "types": [
                "元素种类", "元素个数", "相同元素数量", "不同元素数量",
                "元素间数量换算", "内部元素", "外部元素", "元素位置",
                "元素方向", "元素大小",
            ],
        },
        "一笔画": {"checks": ["奇点数量", "是否连通", "是否一笔画"]},
        "部分数": {"checks": ["连通区域数量"]},
    }


def _checklist_position_rules() -> dict[str, Any]:
    """Position rules checklist."""
    return {
        "平移": {
            "checks": ["移动主体", "移动方向", "移动路径", "移动步数", "是否循环", "是否反弹"],
            "directions": ["上下", "左右", "斜向", "顺时针", "逆时针", "内外移动", "绕圈移动"],
            "step_patterns": ["固定步数", "递增步数", "递减步数", "交替步数"],
            "paths": ["直线路径", "环形路径", "宫格路径", "外圈路径", "内圈路径", "蛇形路径", "反弹路径"],
        },
        "旋转": {
            "checks": ["旋转中心", "旋转方向", "旋转角度", "每步旋转角度是否固定"],
            "common_angles": ["45°", "90°", "135°", "180°"],
        },
        "翻转": {
            "checks": ["左右翻转", "上下翻转", "沿斜轴翻转", "翻转后是否再旋转", "局部翻转", "整体翻转"],
        },
    }


def _checklist_style_rules() -> dict[str, Any]:
    """Style rules checklist."""
    return {
        "遍历": {
            "types": ["颜色遍历", "形状遍历", "数量遍历", "位置遍历", "方向遍历", "元素种类遍历"],
        },
        "加减同异": {
            "types": ["相加", "相减", "去同存异", "去异存同", "叠加后变色", "叠加后抵消", "同位置运算"],
            "constraints": [
                "必须逐位置比较。",
                "必须先从已知图推出统一规则。",
                "不能凭单个位置猜运算结果。",
                "若运算表不能统一解释已知图，应 analysis_only。",
            ],
        },
        "黑白运算": {
            "process": [
                "1. 判断是否为同位置黑白叠加。",
                "2. 建立黑+黑、黑+白、白+黑、白+白的运算表。",
                "3. 用至少一组已知图验证运算表。",
                "4. 运算表一致后再代入问号图。",
                "5. 若题干无法推出唯一运算表，不强行选择。",
            ],
            "constraint": "不同题的黑白运算表可能不同，不能预设固定运算规则。",
        },
    }


def _checklist_inter_figure_relations() -> dict[str, Any]:
    """Inter-figure relations checklist."""
    return {
        "relations": [
            "相离", "相交于点", "相交于线", "相交于面",
            "包含", "内外关系", "公共边", "公共点",
            "公共区域", "重叠面积", "连接方式",
        ],
    }


def _checklist_functional_elements() -> dict[str, Any]:
    """Functional elements checklist."""
    return {
        "标记点": ["交点", "端点", "切点", "中心点", "外框点", "内部点", "曲直交点"],
        "标记线": ["直线", "曲线", "最长线", "最短线", "平行线", "垂直线", "公共边", "连接线"],
        "标记面": ["最大面", "最小面", "相交面", "阴影面", "直线面", "曲线面", "内部面", "外部面"],
        "标记角": ["最大角", "最小角", "直角", "锐角", "钝角", "内角", "外角"],
        "相对位置": ["上", "下", "左", "右", "内", "外", "中心", "边上", "角上", "交点上", "端点上"],
        "特殊关系": [
            "黑点连线与原图线条是否平行、垂直或重合。",
            "标记点是否落在最大面、最小面或特殊面内。",
            "箭头是否指向特殊点、特殊线、特殊面或特殊角。",
            "阴影是否标记最大区域、最小区域或相交区域。",
        ],
    }


def _checklist_black_white_blocks() -> dict[str, Any]:
    """Black-white blocks checklist."""
    return {
        "checks": [
            "整体对称", "黑白面积", "黑块数量", "白块数量",
            "黑块位置", "白块位置", "黑块连通", "白块连通",
            "黑块相邻关系", "黑白相邻关系", "同位置运算",
            "局部平移", "局部旋转",
        ],
        "recommended_order": [
            "1. 先看整体对称性。",
            "2. 再看黑白面积比例。",
            "3. 再看黑块数量是否递增、递减或恒定。",
            "4. 再看黑块是否连通，连通块数量是否变化。",
            "5. 再看黑块是否相邻，边相邻还是角相邻。",
            "6. 再看同位置黑白运算。",
            "7. 最后看局部位置移动。",
        ],
        "constraints": [
            "黑白块题不能只看黑块数量；若数量无规律，应继续检查连通、相邻、对称、运算和位置。",
            "不同题的黑白运算表可能不同，不能预设固定运算规则。",
            "必须从已知图推出统一运算表。",
        ],
    }


def _checklist_chinese_characters() -> dict[str, Any]:
    """Chinese character checklist."""
    return {
        "checks": [
            "结构", "上下结构", "左右结构", "包围结构",
            "封闭面", "曲直性", "开闭性", "笔画数",
            "部分数", "交点数", "元素数量", "部首位置",
            "相同部件", "汉字读音", "声母韵母", "偏旁遍历",
        ],
        "emphasis": "汉字图推优先当作图形看，不优先当作语文题。",
    }


def _checklist_digits() -> dict[str, Any]:
    """Digit visual classification checklist."""
    return {
        "checks": [
            "对称性", "曲直性", "开闭性", "封闭面数量",
            "数字大小", "奇偶性", "递增递减", "数字运算", "排列顺序",
        ],
        "classifications": {
            "常见轴对称数字": ["0", "3", "6", "8", "9"],
            "全曲数字": ["0", "3", "6", "8", "9"],
            "全直数字": ["1", "4", "7"],
            "曲直混合数字": ["2", "5"],
            "开放图形": ["1", "2", "3", "5", "7"],
            "全封闭图形": ["0", "8"],
            "半封闭图形": ["4", "6", "9"],
            "0个面": ["1", "2", "3", "5", "7"],
            "1个面": ["0", "4", "6", "9"],
            "2个面": ["8"],
        },
        "note": "数字题可以同时考图形属性和数字本身运算，必须先判断题目是在考'图形化数字'还是'数字运算'。",
    }


def _checklist_letters() -> dict[str, Any]:
    """Letter visual classification checklist."""
    return {
        "checks": [
            "字母表顺序", "对称性", "中心对称", "曲直性",
            "开闭性", "封闭面数量", "大小写形式", "字母本身算法",
        ],
        "classifications": {
            "轴对称字母": list("ABCDEHIKMOTUVWXY"),
            "中心对称字母": list("NSZ"),
            "全曲": list("COSU"),
            "全直": list("AEFHIKLMNTVWXYZ"),
            "曲直混合": list("BDGJPQR"),
            "开放图形": list("CEFGHIJKLMNSTUVWXYZ"),
            "全封闭图形": list("BDO"),
            "半封闭图形": list("APQR"),
            "0个面": list("CEFGHIJKLMNSTUVWXYZ"),
            "1个面": list("ADOPR"),
            "2个面": list("B"),
        },
        "notes": [
            "字母分类默认基于常见大写印刷体。",
            "若题干字体特殊，以题干视觉形态为准。",
            "若出现小写字母，不能直接套用大写表。",
        ],
    }


def _checklist_cube_net() -> dict[str, Any]:
    """Cube net (六面体展开图) checklist."""
    return {
        "net_types": ["1-4-1", "2-3-1", "2-2-2", "0-3-3"],
        "note": "六面体展开图常见 4 类 11 种结构。",
        "checks": [
            "相对面排除",
            "公共边验证",
            "公共点验证",
            "时针方向",
            "面内图案方向",
            "特殊面",
            "选项排除",
        ],
        "constraints": [
            "若仅靠相对面无法排除，应继续使用公共边、公共点、时针法，不能直接猜。",
        ],
    }


def _checklist_cross_section() -> dict[str, Any]:
    """Cross section (截面图) checklist."""
    return {
        "checks": [
            "立体类型", "切入位置", "切割方向",
            "截面边数", "截面形状", "能否截出选项形状", "是否存在不可能截面",
        ],
        "rules": [
            "六面体一般最多可截出六边形。",
            "六面体不能截出正五边形。",
            "圆柱常见截面包括圆、椭圆、矩形等。",
            "圆锥常见截面包括圆、椭圆、三角形等。",
            "圆锥通常不能截出四边形。",
        ],
        "constraint": "如果选项形状需要曲面参与，必须确认原立体是否有曲面。",
    }


def _checklist_three_views() -> dict[str, Any]:
    """Three views (三视图) checklist."""
    return {
        "views": ["主视图", "俯视图", "左视图"],
        "rules": ["长对正", "高平齐", "宽相等"],
        "checks": ["可见线", "不可见线", "遮挡关系", "曲面交接"],
        "core_rules": [
            "有线就有线，没线就没线。",
            "被遮挡部分不可见。",
            "曲面平滑交接处一般无线。",
        ],
    }


def _checklist_solid_assembly() -> dict[str, Any]:
    """Solid assembly (立体拼合) checklist."""
    return {
        "checks": [
            "块数", "体积", "占地面积", "最大块", "特殊块",
            "凹凸关系", "长短关系", "高低关系", "分层结构", "严丝合缝",
        ],
        "process": [
            "1. 先数小方块总数。",
            "2. 再找占地面积大的特殊块。",
            "3. 按层画图或按层想象。",
            "4. 检查凸凹是否互补。",
            "5. 检查长短、高低是否一致。",
            "6. 检查拼合后是否多块、少块或重叠。",
        ],
        "constraint": "若某个选项不能严丝合缝，或需要重叠/穿插才能成立，应排除。",
    }
