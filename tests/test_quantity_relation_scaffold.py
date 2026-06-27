"""Tests for quantity relation scaffold."""
from __future__ import annotations

import importlib
import inspect

import pytest

from xingce_solver.scaffolds.quantity_relation_scaffold import (
    build_quantity_relation_scaffold,
    get_quantity_relation_stage_order,
    get_quantity_relation_problem_type_checklists,
    get_quantity_relation_method_checklists,
    render_quantity_relation_prompt_template,
)


# ── 4.1 basic structure ──────────────────────────────────────────────

class TestBasicStructure:
    def test_returns_dict(self):
        result = build_quantity_relation_scaffold()
        assert isinstance(result, dict)

    def test_module(self):
        result = build_quantity_relation_scaffold()
        assert result["module"] == "quantity_relation"

    def test_version(self):
        result = build_quantity_relation_scaffold()
        assert result["version"] == "v0.1"

    def test_mode(self):
        result = build_quantity_relation_scaffold()
        assert result["mode"] == "method_scaffold_only"


# ── 4.2 top-level fields completeness ─────────────────────────────────

class TestTopLevelFields:
    def test_required_fields(self):
        result = build_quantity_relation_scaffold()
        required = [
            "module", "version", "mode", "positioning", "stage_order",
            "problem_type_router", "problem_type_checklists",
            "method_checklists", "option_verification", "response_template",
            "uncertainty_policy", "must_not_do",
        ]
        for field in required:
            assert field in result, f"Missing field: {field}"


# ── 4.3 stage_order ──────────────────────────────────────────────────

class TestStageOrder:
    def test_stage_order_is_list(self):
        order = get_quantity_relation_stage_order()
        assert isinstance(order, list)
        assert len(order) >= 10

    def test_stage_order_contains_required(self):
        order = get_quantity_relation_stage_order()
        required = [
            "题型识别", "问法识别", "已知量抽取", "未知量设定",
            "单位统一", "方法选择", "模型建立", "计算/代入验证",
            "量级检查", "唯一性判断", "不确定性约束",
        ]
        for stage in required:
            assert stage in order, f"Missing stage: {stage}"

    def test_stage_order_sequence(self):
        order = get_quantity_relation_stage_order()
        assert order.index("题型识别") < order.index("已知量抽取")
        assert order.index("已知量抽取") < order.index("单位统一")
        assert order.index("单位统一") < order.index("方法选择")
        assert order.index("方法选择") < order.index("模型建立")
        assert order.index("模型建立") < order.index("计算/代入验证")
        assert order.index("计算/代入验证") < order.index("唯一性判断")


# ── 4.4 problem type coverage ────────────────────────────────────────

class TestProblemTypeCoverage:
    REQUIRED_TYPES = [
        "工程问题", "行程问题", "经济利润问题", "浓度/溶液混合问题",
        "容斥/集合问题", "排列组合", "概率问题", "几何问题",
        "鸡兔同笼", "日期星期问题", "特征余数", "牛吃草", "抽屉原理",
    ]

    def test_problem_type_router_contains_required(self):
        scaffold = build_quantity_relation_scaffold()
        router = scaffold["problem_type_router"]
        for pt in self.REQUIRED_TYPES:
            assert pt in router, f"Missing problem type: {pt}"

    def test_problem_type_checklists_contains_required(self):
        scaffold = build_quantity_relation_scaffold()
        checklists = scaffold["problem_type_checklists"]
        for pt in ["工程问题", "行程问题", "经济利润问题", "浓度/溶液混合问题",
                    "容斥/集合问题", "排列组合", "概率问题", "鸡兔同笼",
                    "日期星期问题", "特征余数", "牛吃草"]:
            assert pt in checklists, f"Missing checklist: {pt}"

    def test_router_has_feasibility(self):
        scaffold = build_quantity_relation_scaffold()
        router = scaffold["problem_type_router"]
        for pt, info in router.items():
            assert "feasibility" in info, f"{pt} missing feasibility"


# ── 4.5 method coverage ──────────────────────────────────────────────

class TestMethodCoverage:
    REQUIRED_METHODS = [
        "代入排除", "特值法", "方程法", "赋值法", "枚举法",
        "十字交叉法", "比例法", "图表辅助", "公式法", "估算量级",
    ]

    def test_method_checklists_contains_required(self):
        scaffold = build_quantity_relation_scaffold()
        methods = scaffold["method_checklists"]
        for m in self.REQUIRED_METHODS:
            assert m in methods, f"Missing method: {m}"

    def test_methods_have_required_fields(self):
        scaffold = build_quantity_relation_scaffold()
        methods = scaffold["method_checklists"]
        for m, info in methods.items():
            assert "scenarios" in info, f"{m} missing scenarios"
            assert "steps" in info, f"{m} missing steps"
            assert "verification" in info, f"{m} missing verification"
            assert "risk" in info, f"{m} missing risk"
            assert "analysis_only_when" in info, f"{m} missing analysis_only_when"


# ── 4.6 prompt template ──────────────────────────────────────────────

class TestPromptTemplate:
    def test_returns_str(self):
        template = render_quantity_relation_prompt_template()
        assert isinstance(template, str)

    def test_contains_required_sections(self):
        template = render_quantity_relation_prompt_template()
        required = [
            "【题型识别】", "【问法目标】", "【已知量】", "【未知量】",
            "【单位统一】", "【方法选择】", "【模型建立】", "【计算/代入验证】",
            "【量级检查】", "【唯一性判断】",
        ]
        for section in required:
            assert section in template, f"Missing section: {section}"

    def test_contains_analysis_only(self):
        template = render_quantity_relation_prompt_template()
        assert "analysis_only" in template


# ── 4.7 uncertainty policy ───────────────────────────────────────────

class TestUncertaintyPolicy:
    def test_contains_analysis_only(self):
        scaffold = build_quantity_relation_scaffold()
        text = str(scaffold["uncertainty_policy"])
        assert "analysis_only" in text

    def test_contains_key_triggers(self):
        scaffold = build_quantity_relation_scaffold()
        text = str(scaffold["uncertainty_policy"])
        for trigger in ["题型无法稳定识别", "问法目标不明确", "单位无法完整抽取",
                        "多个建模方式", "多个选项", "题干存在歧义"]:
            assert trigger in text, f"Missing trigger: {trigger}"


# ── 4.8 must_not_do ──────────────────────────────────────────────────

class TestMustNotDo:
    def test_contains_required_items(self):
        scaffold = build_quantity_relation_scaffold()
        text = str(scaffold["must_not_do"])
        for item in ["不得看见数字就硬套公式", "不得忽略单位", "不得忽略问法",
                     "不得默认选择第一个选项", "不得把 scaffold 当 solver",
                     "不得用题号、case_id 或标准答案写规则",
                     "不得生成或引用自造真题"]:
            assert item in text, f"Missing item: {item}"


# ── 4.9 no answer fields ─────────────────────────────────────────────

class TestNoAnswerFields:
    FORBIDDEN = ["answer", "selected_option", "prediction"]

    def test_no_answer_fields(self):
        result = build_quantity_relation_scaffold()
        for f in self.FORBIDDEN:
            assert f not in result, f"Has forbidden field: {f}"


# ── 4.10 forbidden dependencies ──────────────────────────────────────

class TestForbiddenDependencies:
    FORBIDDEN = [
        "cv2", "PIL", "Pillow", "pytesseract", "sklearn", "torch",
        "tensorflow", "statsmodels", "xgboost", "lightgbm", "requests",
        "openai", "anthropic", "numpy",
    ]

    def test_no_forbidden_imports(self):
        mod = importlib.import_module("xingce_solver.scaffolds.quantity_relation_scaffold")
        source = inspect.getsource(mod)
        for dep in self.FORBIDDEN:
            assert dep not in source, f"References {dep}"


# ── public function signatures ────────────────────────────────────────

class TestPublicFunctions:
    def test_all_callable(self):
        assert callable(build_quantity_relation_scaffold)
        assert callable(get_quantity_relation_stage_order)
        assert callable(get_quantity_relation_problem_type_checklists)
        assert callable(get_quantity_relation_method_checklists)
        assert callable(render_quantity_relation_prompt_template)
