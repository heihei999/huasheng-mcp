"""Tests for judgement reasoning scaffolds (definition, analogy, logic analysis)."""
from __future__ import annotations

import importlib
import inspect

import pytest

from xingce_solver.scaffolds.definition_judgement_scaffold import (
    build_definition_judgement_scaffold,
    get_definition_judgement_stage_order,
    get_definition_judgement_element_checklists,
    render_definition_judgement_prompt_template,
)
from xingce_solver.scaffolds.analogy_reasoning_scaffold import (
    build_analogy_reasoning_scaffold,
    get_analogy_reasoning_stage_order,
    get_analogy_reasoning_relation_checklists,
    render_analogy_reasoning_prompt_template,
)
from xingce_solver.scaffolds.logic_analysis_scaffold import (
    build_logic_analysis_scaffold,
    get_logic_analysis_stage_order,
    get_logic_analysis_structure_checklists,
    render_logic_analysis_prompt_template,
)


# ── 8.1 basic structure ──────────────────────────────────────────────

class TestBasicStructure:
    def test_definition_returns_dict(self):
        result = build_definition_judgement_scaffold()
        assert isinstance(result, dict)

    def test_definition_module(self):
        result = build_definition_judgement_scaffold()
        assert result["module"] == "definition_judgement"

    def test_definition_version(self):
        result = build_definition_judgement_scaffold()
        assert result["version"] == "v0.1"

    def test_definition_mode(self):
        result = build_definition_judgement_scaffold()
        assert result["mode"] == "method_scaffold_only"

    def test_analogy_returns_dict(self):
        result = build_analogy_reasoning_scaffold()
        assert isinstance(result, dict)

    def test_analogy_module(self):
        result = build_analogy_reasoning_scaffold()
        assert result["module"] == "analogy_reasoning"

    def test_analogy_version(self):
        result = build_analogy_reasoning_scaffold()
        assert result["version"] == "v0.1"

    def test_analogy_mode(self):
        result = build_analogy_reasoning_scaffold()
        assert result["mode"] == "method_scaffold_only"

    def test_logic_returns_dict(self):
        result = build_logic_analysis_scaffold()
        assert isinstance(result, dict)

    def test_logic_module(self):
        result = build_logic_analysis_scaffold()
        assert result["module"] == "logic_analysis"

    def test_logic_version(self):
        result = build_logic_analysis_scaffold()
        assert result["version"] == "v0.1"

    def test_logic_mode(self):
        result = build_logic_analysis_scaffold()
        assert result["mode"] == "method_scaffold_only"


# ── 8.2 top-level fields completeness ─────────────────────────────────

class TestTopLevelFields:
    def test_definition_fields(self):
        result = build_definition_judgement_scaffold()
        required = [
            "module", "version", "mode", "positioning", "stage_order",
            "question_polarity", "definition_elements", "option_verification",
            "response_template", "uncertainty_policy", "must_not_do",
        ]
        for field in required:
            assert field in result, f"Missing field: {field}"

    def test_analogy_fields(self):
        result = build_analogy_reasoning_scaffold()
        required = [
            "module", "version", "mode", "positioning", "stage_order",
            "question_forms", "relation_types", "relation_verification",
            "option_comparison", "response_template", "uncertainty_policy",
            "must_not_do",
        ]
        for field in required:
            assert field in result, f"Missing field: {field}"

    def test_logic_fields(self):
        result = build_logic_analysis_scaffold()
        required = [
            "module", "version", "mode", "positioning", "stage_order",
            "problem_type_router", "structure_templates",
            "constraint_extraction", "option_verification",
            "response_template", "uncertainty_policy", "must_not_do",
        ]
        for field in required:
            assert field in result, f"Missing field: {field}"


# ── 8.3 stage_order ──────────────────────────────────────────────────

class TestStageOrder:
    def test_definition_stage_order(self):
        order = get_definition_judgement_stage_order()
        assert "问法识别" in order
        assert "定义要素抽取" in order
        assert "选项逐项匹配" in order
        assert "唯一性判断" in order
        assert "不确定性约束" in order

    def test_definition_stage_order_is_list(self):
        order = get_definition_judgement_stage_order()
        assert isinstance(order, list)
        assert len(order) >= 5

    def test_analogy_stage_order(self):
        order = get_analogy_reasoning_stage_order()
        assert "题干关系造句" in order
        assert "关系类型识别" in order
        assert "选项关系套入" in order
        assert "横纵比较" in order
        assert "不确定性约束" in order

    def test_analogy_stage_order_is_list(self):
        order = get_analogy_reasoning_stage_order()
        assert isinstance(order, list)
        assert len(order) >= 5

    def test_logic_stage_order(self):
        order = get_logic_analysis_stage_order()
        assert "对象集合抽取" in order
        assert "约束条件抽取" in order
        assert "结构框架建立" in order
        assert "选项代入验证" in order
        assert "唯一性判断" in order

    def test_logic_stage_order_is_list(self):
        order = get_logic_analysis_stage_order()
        assert isinstance(order, list)
        assert len(order) >= 5


# ── 8.4 key content ──────────────────────────────────────────────────

class TestKeyContent:
    def test_definition_elements(self):
        scaffold = build_definition_judgement_scaffold()
        elements_text = str(scaffold["definition_elements"])
        assert "主体" in elements_text
        assert "客体" in elements_text
        assert "条件" in elements_text
        assert "方式" in elements_text
        assert "目的" in elements_text
        assert "结果" in elements_text
        assert "排除项" in elements_text
        assert "必要条件" in elements_text
        assert "附加描述" in elements_text

    def test_definition_polarity(self):
        scaffold = build_definition_judgement_scaffold()
        polarity_text = str(scaffold["question_polarity"])
        assert "选非" in polarity_text

    def test_definition_analysis_only(self):
        scaffold = build_definition_judgement_scaffold()
        uncertainty_text = str(scaffold["uncertainty_policy"])
        assert "analysis_only" in uncertainty_text

    def test_analogy_relation_types(self):
        scaffold = build_analogy_reasoning_scaffold()
        types_text = str(scaffold["relation_types"])
        assert "近义关系" in types_text
        assert "反义关系" in types_text
        assert "种属关系" in types_text
        assert "组成关系" in types_text
        assert "功能关系" in types_text
        assert "因果关系" in types_text
        assert "工具-用途" in types_text
        assert "职业-工具" in types_text

    def test_analogy_relation_verification(self):
        scaffold = build_analogy_reasoning_scaffold()
        verification_text = str(scaffold["relation_verification"])
        assert "关系方向" in verification_text
        assert "关系强弱" in verification_text

    def test_analogy_analysis_only(self):
        scaffold = build_analogy_reasoning_scaffold()
        uncertainty_text = str(scaffold["uncertainty_policy"])
        assert "analysis_only" in uncertainty_text

    def test_logic_problem_types(self):
        scaffold = build_logic_analysis_scaffold()
        router_text = str(scaffold["problem_type_router"])
        assert "排序题" in router_text
        assert "分组题" in router_text
        assert "匹配题" in router_text
        assert "真假话题" in router_text
        assert "半真半假题" in router_text

    def test_logic_structure_templates(self):
        scaffold = build_logic_analysis_scaffold()
        templates_text = str(scaffold["structure_templates"])
        assert "对象-属性表" in templates_text
        assert "排序轴" in templates_text
        assert "分组框" in templates_text
        assert "选项代入表" in templates_text

    def test_logic_analysis_only(self):
        scaffold = build_logic_analysis_scaffold()
        uncertainty_text = str(scaffold["uncertainty_policy"])
        assert "analysis_only" in uncertainty_text


# ── 8.5 prompt template ──────────────────────────────────────────────

class TestPromptTemplate:
    def test_definition_template_is_str(self):
        template = render_definition_judgement_prompt_template()
        assert isinstance(template, str)

    def test_definition_template_sections(self):
        template = render_definition_judgement_prompt_template()
        assert "【问法极性】" in template
        assert "【定义要素】" in template
        assert "【选项核验】" in template
        assert "【唯一性判断】" in template
        assert "analysis_only" in template

    def test_analogy_template_is_str(self):
        template = render_analogy_reasoning_prompt_template()
        assert isinstance(template, str)

    def test_analogy_template_sections(self):
        template = render_analogy_reasoning_prompt_template()
        assert "【题干形式】" in template
        assert "【题干造句】" in template
        assert "【关系类型】" in template
        assert "【选项套入】" in template
        assert "【唯一性判断】" in template
        assert "analysis_only" in template

    def test_logic_template_is_str(self):
        template = render_logic_analysis_prompt_template()
        assert isinstance(template, str)

    def test_logic_template_sections(self):
        template = render_logic_analysis_prompt_template()
        assert "【题型识别】" in template
        assert "【对象集合】" in template
        assert "【约束条件】" in template
        assert "【选项代入】" in template
        assert "【唯一性判断】" in template
        assert "analysis_only" in template


# ── 8.6 forbidden dependencies ───────────────────────────────────────

class TestForbiddenDependencies:
    FORBIDDEN = [
        "cv2", "PIL", "Pillow", "pytesseract", "sklearn", "torch",
        "tensorflow", "statsmodels", "xgboost", "lightgbm", "requests",
        "openai", "anthropic", "numpy",
    ]

    def _read_source(self, module_name: str) -> str:
        mod = importlib.import_module(f"xingce_solver.scaffolds.{module_name}")
        return inspect.getsource(mod)

    def test_definition_no_forbidden_imports(self):
        source = self._read_source("definition_judgement_scaffold")
        for dep in self.FORBIDDEN:
            assert dep not in source, f"definition_judgement_scaffold references {dep}"

    def test_analogy_no_forbidden_imports(self):
        source = self._read_source("analogy_reasoning_scaffold")
        for dep in self.FORBIDDEN:
            assert dep not in source, f"analogy_reasoning_scaffold references {dep}"

    def test_logic_no_forbidden_imports(self):
        source = self._read_source("logic_analysis_scaffold")
        for dep in self.FORBIDDEN:
            assert dep not in source, f"logic_analysis_scaffold references {dep}"


# ── 8.7 no solver answer fields ──────────────────────────────────────

class TestNoSolverFields:
    FORBIDDEN_FIELDS = ["answer", "selected_option", "prediction"]

    def test_definition_no_answer_fields(self):
        result = build_definition_judgement_scaffold()
        for field in self.FORBIDDEN_FIELDS:
            assert field not in result, f"definition scaffold has forbidden field: {field}"

    def test_analogy_no_answer_fields(self):
        result = build_analogy_reasoning_scaffold()
        for field in self.FORBIDDEN_FIELDS:
            assert field not in result, f"analogy scaffold has forbidden field: {field}"

    def test_logic_no_answer_fields(self):
        result = build_logic_analysis_scaffold()
        for field in self.FORBIDDEN_FIELDS:
            assert field not in result, f"logic scaffold has forbidden field: {field}"


# ── 8.8 uncertainty policy ───────────────────────────────────────────

class TestUncertaintyPolicy:
    COMMON_ITEMS = [
        "analysis_only",
        "不唯一",
        "不得默认选择第一个选项",
        "不得用题号、case_id 或标准答案写规则",
    ]

    def _get_all_text(self, scaffold: dict) -> str:
        return str(scaffold)

    def test_definition_uncertainty(self):
        scaffold = build_definition_judgement_scaffold()
        text = self._get_all_text(scaffold)
        for item in self.COMMON_ITEMS:
            assert item in text, f"definition scaffold missing: {item}"

    def test_analogy_uncertainty(self):
        scaffold = build_analogy_reasoning_scaffold()
        text = self._get_all_text(scaffold)
        for item in self.COMMON_ITEMS:
            assert item in text, f"analogy scaffold missing: {item}"

    def test_logic_uncertainty(self):
        scaffold = build_logic_analysis_scaffold()
        text = self._get_all_text(scaffold)
        for item in self.COMMON_ITEMS:
            assert item in text, f"logic scaffold missing: {item}"


# ── public function signatures ────────────────────────────────────────

class TestPublicFunctionSignatures:
    def test_definition_public_functions_exist(self):
        assert callable(build_definition_judgement_scaffold)
        assert callable(get_definition_judgement_stage_order)
        assert callable(get_definition_judgement_element_checklists)
        assert callable(render_definition_judgement_prompt_template)

    def test_analogy_public_functions_exist(self):
        assert callable(build_analogy_reasoning_scaffold)
        assert callable(get_analogy_reasoning_stage_order)
        assert callable(get_analogy_reasoning_relation_checklists)
        assert callable(render_analogy_reasoning_prompt_template)

    def test_logic_public_functions_exist(self):
        assert callable(build_logic_analysis_scaffold)
        assert callable(get_logic_analysis_stage_order)
        assert callable(get_logic_analysis_structure_checklists)
        assert callable(render_logic_analysis_prompt_template)
