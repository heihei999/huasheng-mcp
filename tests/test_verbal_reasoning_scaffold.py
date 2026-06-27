"""Tests for verbal reasoning scaffold."""
from __future__ import annotations

import importlib
import inspect

import pytest

from xingce_solver.scaffolds.verbal_reasoning_scaffold import (
    build_verbal_reasoning_scaffold,
    get_verbal_reasoning_stage_order,
    get_verbal_reasoning_question_type_checklists,
    get_verbal_reasoning_method_checklists,
    render_verbal_reasoning_prompt_template,
)


# ── 4.1 basic structure ──────────────────────────────────────────────

class TestBasicStructure:
    def test_returns_dict(self):
        result = build_verbal_reasoning_scaffold()
        assert isinstance(result, dict)

    def test_module(self):
        result = build_verbal_reasoning_scaffold()
        assert result["module"] == "verbal_reasoning"

    def test_version(self):
        result = build_verbal_reasoning_scaffold()
        assert result["version"] == "v0.1"

    def test_mode(self):
        result = build_verbal_reasoning_scaffold()
        assert result["mode"] == "method_scaffold_only"


# ── 4.2 top-level fields completeness ─────────────────────────────────

class TestTopLevelFields:
    def test_required_fields(self):
        result = build_verbal_reasoning_scaffold()
        required = [
            "module", "version", "mode", "positioning", "stage_order",
            "question_type_router", "question_type_checklists",
            "discourse_structure_checklists", "cloze_context_checklists",
            "sentence_expression_checklists", "method_checklists",
            "option_verification", "response_template",
            "uncertainty_policy", "must_not_do",
        ]
        for field in required:
            assert field in result, f"Missing field: {field}"


# ── 4.3 stage_order ──────────────────────────────────────────────────

class TestStageOrder:
    def test_stage_order_is_list(self):
        order = get_verbal_reasoning_stage_order()
        assert isinstance(order, list)
        assert len(order) >= 10

    def test_stage_order_contains_required(self):
        order = get_verbal_reasoning_stage_order()
        required = [
            "题型识别", "问法识别", "文段结构划分", "主题句/重点句定位",
            "逻辑关系识别", "语境与词义检查", "选项逐项验证",
            "干扰项识别", "衔接连贯检查", "唯一性判断", "不确定性约束",
        ]
        for stage in required:
            assert stage in order, f"Missing stage: {stage}"

    def test_stage_order_sequence(self):
        order = get_verbal_reasoning_stage_order()
        assert order.index("题型识别") < order.index("文段结构划分")
        assert order.index("文段结构划分") < order.index("主题句/重点句定位")
        assert order.index("主题句/重点句定位") < order.index("选项逐项验证")
        assert order.index("选项逐项验证") < order.index("唯一性判断")


# ── 4.4 question type coverage ───────────────────────────────────────

class TestQuestionTypeCoverage:
    REQUIRED_TYPES = [
        "主旨意图", "中心理解", "标题填入", "下文推断",
        "语句填入", "语句排序", "逻辑填空", "成语辨析",
        "实词辨析", "关联词填空", "语义衔接", "细节理解", "态度观点",
    ]

    def test_router_contains_required(self):
        scaffold = build_verbal_reasoning_scaffold()
        router = scaffold["question_type_router"]
        for pt in self.REQUIRED_TYPES:
            assert pt in router, f"Missing problem type: {pt}"

    def test_checklists_contains_required(self):
        scaffold = build_verbal_reasoning_scaffold()
        checklists = scaffold["question_type_checklists"]
        for pt in ["主旨意图", "中心理解", "标题填入", "下文推断",
                    "语句填入", "语句排序", "逻辑填空", "成语辨析",
                    "实词辨析", "关联词填空", "语义衔接", "干扰项识别"]:
            assert pt in checklists, f"Missing checklist: {pt}"


# ── 4.5 method coverage ──────────────────────────────────────────────

class TestMethodCoverage:
    REQUIRED_METHODS = [
        "主题句定位", "关联词分析", "转折关系", "递进关系",
        "因果关系", "对策句", "总分结构", "干扰项排除",
        "语境搭配", "感情色彩", "语义轻重", "衔接连贯",
        "排序线索", "代词指代", "主体词覆盖",
    ]

    def test_method_checklists_contains_required(self):
        scaffold = build_verbal_reasoning_scaffold()
        methods = scaffold["method_checklists"]
        for m in self.REQUIRED_METHODS:
            assert m in methods, f"Missing method: {m}"


# ── 4.6 structure checklists ─────────────────────────────────────────

class TestStructureChecklists:
    def test_discourse_structures(self):
        scaffold = build_verbal_reasoning_scaffold()
        ds = scaffold["discourse_structure_checklists"]
        for key in ["转折关系", "递进关系", "因果关系", "并列关系",
                     "问题-对策结构", "观点-解释结构", "总分结构",
                     "主题句定位", "主体词一致"]:
            assert key in ds, f"Missing discourse structure: {key}"

    def test_cloze_contexts(self):
        scaffold = build_verbal_reasoning_scaffold()
        cc = scaffold["cloze_context_checklists"]
        for key in ["语境搭配", "感情色彩", "语义轻重", "固定搭配",
                     "成语适配", "关联词逻辑", "前后照应"]:
            assert key in cc, f"Missing cloze context: {key}"

    def test_sentence_expressions(self):
        scaffold = build_verbal_reasoning_scaffold()
        se = scaffold["sentence_expression_checklists"]
        for key in ["语句填入", "语句排序", "下文推断", "标题填入",
                     "代词指代", "话题一致", "逻辑顺序", "首句判断", "尾句判断"]:
            assert key in se, f"Missing sentence expression: {key}"


# ── 4.7 prompt template ──────────────────────────────────────────────

class TestPromptTemplate:
    def test_returns_str(self):
        template = render_verbal_reasoning_prompt_template()
        assert isinstance(template, str)

    def test_contains_required_sections(self):
        template = render_verbal_reasoning_prompt_template()
        required = [
            "【题型识别】", "【问法目标】", "【文段结构】", "【主题句/重点句】",
            "【逻辑关系】", "【语境/词义检查】", "【选项核验】",
            "【干扰项排除】", "【衔接连贯检查】", "【唯一性判断】",
        ]
        for section in required:
            assert section in template, f"Missing section: {section}"

    def test_contains_analysis_only(self):
        template = render_verbal_reasoning_prompt_template()
        assert "analysis_only" in template


# ── 4.8 uncertainty policy ───────────────────────────────────────────

class TestUncertaintyPolicy:
    def test_contains_analysis_only(self):
        scaffold = build_verbal_reasoning_scaffold()
        text = str(scaffold["uncertainty_policy"])
        assert "analysis_only" in text

    def test_contains_key_triggers(self):
        scaffold = build_verbal_reasoning_scaffold()
        text = str(scaffold["uncertainty_policy"])
        for trigger in ["题型无法稳定识别", "问法目标不明确", "文段结构无法稳定划分",
                        "多个选项", "逻辑填空语境不足", "语句排序存在多个连贯顺序"]:
            assert trigger in text, f"Missing trigger: {trigger}"


# ── 4.9 must_not_do ──────────────────────────────────────────────────

class TestMustNotDo:
    def test_contains_required_items(self):
        scaffold = build_verbal_reasoning_scaffold()
        text = str(scaffold["must_not_do"])
        for item in ["不得只按关键词匹配", "不得只看转折词机械选择",
                     "不得把局部细节当主旨", "不得忽略问法",
                     "不得默认选择第一个选项", "不得把 scaffold 当 solver",
                     "不得用题号、case_id 或标准答案写规则",
                     "不得生成或引用自造真题"]:
            assert item in text, f"Missing item: {item}"


# ── 4.10 no answer fields ────────────────────────────────────────────

class TestNoAnswerFields:
    FORBIDDEN = ["answer", "selected_option", "prediction"]

    def test_no_answer_fields(self):
        result = build_verbal_reasoning_scaffold()
        for f in self.FORBIDDEN:
            assert f not in result, f"Has forbidden field: {f}"


# ── 4.11 forbidden dependencies ──────────────────────────────────────

class TestForbiddenDependencies:
    FORBIDDEN = [
        "cv2", "PIL", "Pillow", "pytesseract", "sklearn", "torch",
        "tensorflow", "statsmodels", "xgboost", "lightgbm", "requests",
        "openai", "anthropic", "numpy",
    ]

    def test_no_forbidden_imports(self):
        mod = importlib.import_module("xingce_solver.scaffolds.verbal_reasoning_scaffold")
        source = inspect.getsource(mod)
        for dep in self.FORBIDDEN:
            assert dep not in source, f"References {dep}"


# ── public function signatures ────────────────────────────────────────

class TestPublicFunctions:
    def test_all_callable(self):
        assert callable(build_verbal_reasoning_scaffold)
        assert callable(get_verbal_reasoning_stage_order)
        assert callable(get_verbal_reasoning_question_type_checklists)
        assert callable(get_verbal_reasoning_method_checklists)
        assert callable(render_verbal_reasoning_prompt_template)
