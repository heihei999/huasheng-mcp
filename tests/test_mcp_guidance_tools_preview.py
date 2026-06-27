"""Tests for MCP guidance tools preview integration."""
from __future__ import annotations

import inspect

import pytest

from xingce_solver.mcp_server import (
    tool_get_graphic_reasoning_scaffold,
    tool_get_definition_judgement_scaffold,
    tool_get_analogy_reasoning_scaffold,
    tool_get_logic_analysis_scaffold,
    tool_get_quantity_relation_scaffold,
    tool_get_verbal_reasoning_scaffold,
    tool_route_xingce_question,
    tool_compose_xingce_analysis_prompt,
    tool_compose_xingce_answer_prompt,
)


# ── 8.1 MCP server module can be imported ─────────────────────────────

class TestMCPServerImport:
    def test_import_mcp_server(self):
        import xingce_solver.mcp_server as mcp_server
        assert mcp_server is not None

    def test_create_mcp_server_callable(self):
        from xingce_solver.mcp_server import create_mcp_server
        assert callable(create_mcp_server)

    def test_mcp_server_has_15_tools(self):
        """Verify MCP server registers 15 tools (v0.4: +compose_xingce_answer_prompt)."""
        import inspect
        from xingce_solver.mcp_server import create_mcp_server
        source = inspect.getsource(create_mcp_server)
        tool_count = source.count("@server.tool()")
        assert tool_count == 15, f"Expected 15 tools, found {tool_count}"


# ── 8.2 tool functions exist ──────────────────────────────────────────

class TestToolFunctionsExist:
    def test_graphic_tool_exists(self):
        assert callable(tool_get_graphic_reasoning_scaffold)

    def test_definition_tool_exists(self):
        assert callable(tool_get_definition_judgement_scaffold)

    def test_analogy_tool_exists(self):
        assert callable(tool_get_analogy_reasoning_scaffold)

    def test_logic_tool_exists(self):
        assert callable(tool_get_logic_analysis_scaffold)

    def test_quantity_relation_tool_exists(self):
        assert callable(tool_get_quantity_relation_scaffold)

    def test_verbal_reasoning_tool_exists(self):
        assert callable(tool_get_verbal_reasoning_scaffold)


# ── 8.3 return dict ──────────────────────────────────────────────────

class TestReturnDict:
    def test_graphic_returns_dict(self):
        result = tool_get_graphic_reasoning_scaffold()
        assert isinstance(result, dict)

    def test_definition_returns_dict(self):
        result = tool_get_definition_judgement_scaffold()
        assert isinstance(result, dict)

    def test_analogy_returns_dict(self):
        result = tool_get_analogy_reasoning_scaffold()
        assert isinstance(result, dict)

    def test_logic_returns_dict(self):
        result = tool_get_logic_analysis_scaffold()
        assert isinstance(result, dict)

    def test_quantity_relation_returns_dict(self):
        result = tool_get_quantity_relation_scaffold()
        assert isinstance(result, dict)

    def test_verbal_reasoning_returns_dict(self):
        result = tool_get_verbal_reasoning_scaffold()
        assert isinstance(result, dict)


# ── 8.4 module field correct ─────────────────────────────────────────

class TestModuleField:
    def test_graphic_module(self):
        result = tool_get_graphic_reasoning_scaffold()
        assert result["module"] == "graphic_reasoning"

    def test_definition_module(self):
        result = tool_get_definition_judgement_scaffold()
        assert result["module"] == "definition_judgement"

    def test_analogy_module(self):
        result = tool_get_analogy_reasoning_scaffold()
        assert result["module"] == "analogy_reasoning"

    def test_logic_module(self):
        result = tool_get_logic_analysis_scaffold()
        assert result["module"] == "logic_analysis"

    def test_quantity_relation_module(self):
        result = tool_get_quantity_relation_scaffold()
        assert result["module"] == "quantity_relation"

    def test_verbal_reasoning_module(self):
        result = tool_get_verbal_reasoning_scaffold()
        assert result["module"] == "verbal_reasoning"


# ── 8.5 mode correct ─────────────────────────────────────────────────

class TestModeField:
    def test_graphic_mode(self):
        result = tool_get_graphic_reasoning_scaffold()
        assert result["mode"] == "method_scaffold_only"

    def test_definition_mode(self):
        result = tool_get_definition_judgement_scaffold()
        assert result["mode"] == "method_scaffold_only"

    def test_analogy_mode(self):
        result = tool_get_analogy_reasoning_scaffold()
        assert result["mode"] == "method_scaffold_only"

    def test_logic_mode(self):
        result = tool_get_logic_analysis_scaffold()
        assert result["mode"] == "method_scaffold_only"

    def test_quantity_relation_mode(self):
        result = tool_get_quantity_relation_scaffold()
        assert result["mode"] == "method_scaffold_only"

    def test_verbal_reasoning_mode(self):
        result = tool_get_verbal_reasoning_scaffold()
        assert result["mode"] == "method_scaffold_only"


# ── 8.6 no answer fields ─────────────────────────────────────────────

class TestNoAnswerFields:
    FORBIDDEN = ["answer", "selected_option", "prediction"]

    def test_graphic_no_answer(self):
        result = tool_get_graphic_reasoning_scaffold()
        for f in self.FORBIDDEN:
            assert f not in result, f"graphic scaffold has {f}"

    def test_definition_no_answer(self):
        result = tool_get_definition_judgement_scaffold()
        for f in self.FORBIDDEN:
            assert f not in result, f"definition scaffold has {f}"

    def test_analogy_no_answer(self):
        result = tool_get_analogy_reasoning_scaffold()
        for f in self.FORBIDDEN:
            assert f not in result, f"analogy scaffold has {f}"

    def test_logic_no_answer(self):
        result = tool_get_logic_analysis_scaffold()
        for f in self.FORBIDDEN:
            assert f not in result, f"logic scaffold has {f}"

    def test_quantity_relation_no_answer(self):
        result = tool_get_quantity_relation_scaffold()
        for f in self.FORBIDDEN:
            assert f not in result, f"quantity_relation scaffold has {f}"

    def test_verbal_reasoning_no_answer(self):
        result = tool_get_verbal_reasoning_scaffold()
        for f in self.FORBIDDEN:
            assert f not in result, f"verbal_reasoning scaffold has {f}"


# ── 8.7 uncertainty_policy and must_not_do ────────────────────────────

class TestUncertaintyPolicy:
    def _check(self, result: dict, name: str):
        assert "uncertainty_policy" in result, f"{name} missing uncertainty_policy"
        assert "must_not_do" in result, f"{name} missing must_not_do"
        text = str(result)
        assert "analysis_only" in text, f"{name} missing analysis_only"

    def test_graphic(self):
        self._check(tool_get_graphic_reasoning_scaffold(), "graphic")

    def test_definition(self):
        self._check(tool_get_definition_judgement_scaffold(), "definition")

    def test_analogy(self):
        self._check(tool_get_analogy_reasoning_scaffold(), "analogy")

    def test_logic(self):
        self._check(tool_get_logic_analysis_scaffold(), "logic")

    def test_quantity_relation(self):
        self._check(tool_get_quantity_relation_scaffold(), "quantity_relation")

    def test_verbal_reasoning(self):
        self._check(tool_get_verbal_reasoning_scaffold(), "verbal_reasoning")


# ── 8.8 forbidden dependency check ───────────────────────────────────

class TestForbiddenDependencies:
    FORBIDDEN = [
        "cv2", "PIL", "Pillow", "pytesseract", "sklearn", "torch",
        "tensorflow", "statsmodels", "xgboost", "lightgbm", "openai",
        "anthropic", "requests", "numpy",
    ]

    def test_mcp_server_no_forbidden_imports(self):
        source = inspect.getsource(
            __import__("xingce_solver.mcp_server", fromlist=["mcp_server"])
        )
        for dep in self.FORBIDDEN:
            assert dep not in source, f"mcp_server references {dep}"


# ── 8.9 no solver call in guidance tools ──────────────────────────────

class TestNoSolverCall:
    SOLVER_NAMES = [
        "solve_logic_reasoning",
        "solve_data_analysis",
        "solve_definition_judgement",
        "solve_analogy_reasoning",
        "solve_logic_analysis",
    ]

    def test_guidance_tool_source_no_solver(self):
        mod = __import__("xingce_solver.mcp_server", fromlist=["mcp_server"])
        # Check only the guidance helper functions, not the full module
        for func_name in [
            "tool_get_graphic_reasoning_scaffold",
            "tool_get_definition_judgement_scaffold",
            "tool_get_analogy_reasoning_scaffold",
            "tool_get_logic_analysis_scaffold",
            "tool_get_quantity_relation_scaffold",
            "tool_get_verbal_reasoning_scaffold",
        ]:
            func = getattr(mod, func_name)
            source = inspect.getsource(func)
            for solver in self.SOLVER_NAMES:
                assert solver not in source, f"{func_name} calls {solver}"


# ── route_xingce_question tests ──────────────────────────────────────

class TestRouteXingceQuestion:
    FORBIDDEN = ["answer", "selected_option", "prediction"]

    def test_exists(self):
        assert callable(tool_route_xingce_question)

    def test_returns_dict(self):
        result = tool_route_xingce_question("test question")
        assert isinstance(result, dict)

    def test_mode(self):
        result = tool_route_xingce_question("test question")
        assert result["mode"] == "route_only"

    def test_answer_policy(self):
        result = tool_route_xingce_question("test question")
        assert result["answer_policy"] == "do_not_answer_inside_router"

    def test_no_answer_fields(self):
        result = tool_route_xingce_question("test question")
        for f in self.FORBIDDEN:
            assert f not in result, f"Has forbidden field: {f}"

    def test_graphic_reasoning_route(self):
        result = tool_route_xingce_question("图形推理题 选择最合适的一项")
        assert result["module_guess"] == "graphic_reasoning"
        assert result["recommended_tool"] == "get_graphic_reasoning_scaffold"

    def test_graphic_by_image(self):
        result = tool_route_xingce_question("选一个", image_present=True)
        assert result["module_guess"] == "graphic_reasoning"

    def test_definition_judgement_route(self):
        result = tool_route_xingce_question("以下属于上述定义的是")
        assert result["module_guess"] == "definition_judgement"
        assert result["recommended_tool"] == "get_definition_judgement_scaffold"

    def test_analogy_route(self):
        result = tool_route_xingce_question(
            "医生：医院",
            options={"A": "教师：学校", "B": "农民：工地",
                     "C": "工人：工厂", "D": "作家：书房"},
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["recommended_tool"] == "get_analogy_reasoning_scaffold"

    def test_logic_reasoning_route(self):
        result = tool_route_xingce_question("以下哪项最能削弱上述论证")
        assert result["module_guess"] == "logic_reasoning"
        assert result["recommended_track"] == "solver_candidate"
        assert result["recommended_tool"] is None

    def test_logic_analysis_route(self):
        result = tool_route_xingce_question("甲乙丙三人排序 甲在乙前面")
        assert result["module_guess"] == "logic_analysis"
        assert result["recommended_tool"] == "get_logic_analysis_scaffold"

    def test_quantity_relation_route(self):
        result = tool_route_xingce_question("工程问题 甲乙合作几天完成")
        assert result["module_guess"] == "quantity_relation"
        assert result["recommended_tool"] == "get_quantity_relation_scaffold"

    def test_verbal_reasoning_route(self):
        result = tool_route_xingce_question("这段文字的主旨是什么")
        assert result["module_guess"] == "verbal_reasoning"
        assert result["recommended_tool"] == "get_verbal_reasoning_scaffold"

    def test_data_analysis_route(self):
        result = tool_route_xingce_question("根据资料 同比增长率是多少")
        assert result["module_guess"] == "data_analysis"
        assert result["recommended_track"] == "solver_candidate"
        assert result["recommended_tool"] is None

    def test_unknown_route(self):
        result = tool_route_xingce_question("abc123 random text")
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"

    def test_hint_confirms(self):
        result = tool_route_xingce_question(
            "主旨是什么", module_hint="verbal_reasoning"
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["confidence"] == "high"

    def test_hint_conflict(self):
        """v0.5.0: module_hint overrides weak keyword routes."""
        result = tool_route_xingce_question(
            "图形推理 选择最合适的一项", module_hint="verbal_reasoning"
        )
        # v0.5.0: module_hint takes priority over keyword routing
        assert result["module_guess"] == "verbal_reasoning"
        assert result["module_hint_applied"] is True
        assert result["module_hint_conflict"] is True
        assert result["heuristic_module_guess"] == "graphic_reasoning"
        assert any("overrides" in w for w in result["warnings"])

    def test_hint_unknown_ignored(self):
        """v0.5.0: unknown hint is silently ignored (normalize returns None)."""
        result = tool_route_xingce_question(
            "test", module_hint="not_a_real_module"
        )
        # v0.5.0: unknown hint → normalize returns None → no override applied
        assert result["module_hint"] is None
        assert result["module_hint_applied"] is False

    def test_no_solver_call(self):
        mod = __import__("xingce_solver.mcp_server", fromlist=["mcp_server"])
        func = getattr(mod, "tool_route_xingce_question")
        source = inspect.getsource(func)
        for solver in ["solve_logic_reasoning", "solve_data_analysis"]:
            assert solver not in source, f"route_xingce_question calls {solver}"


# ── route_uncertain hardening tests ──────────────────────────────────

class TestRouteUncertainHardening:
    """Test that insufficient signals properly route to route_uncertain."""

    FORBIDDEN = ["answer", "selected_option", "prediction"]

    def test_insufficient_condition_routes_to_uncertain(self):
        """条件不足 should route to route_uncertain under strict_mode."""
        result = tool_route_xingce_question("条件不足", options=None, strict_mode=True)
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"
        assert result["recommended_tool"] is None
        assert result["fallback_policy"] == "analysis_only_if_uncertain"

    def test_insufficient_info_routes_to_uncertain(self):
        """信息不足 should route to route_uncertain under strict_mode."""
        result = tool_route_xingce_question("信息不足", options=None, strict_mode=True)
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"
        assert result["recommended_tool"] is None

    def test_cannot_judge_routes_to_uncertain(self):
        """无法判断 should route to route_uncertain under strict_mode."""
        result = tool_route_xingce_question("无法判断", options=None, strict_mode=True)
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"

    def test_uncertain_routes_to_uncertain(self):
        """不确定 should route to route_uncertain under strict_mode."""
        result = tool_route_xingce_question("不确定", options=None, strict_mode=True)
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"

    def test_empty_text_routes_to_uncertain(self):
        """Empty text should route to route_uncertain under strict_mode."""
        result = tool_route_xingce_question("", options=None, strict_mode=True)
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"
        assert result["confidence"] == "unknown"

    def test_blank_text_routes_to_uncertain(self):
        """Whitespace-only text should route to route_uncertain under strict_mode."""
        result = tool_route_xingce_question("   ", options=None, strict_mode=True)
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"

    def test_too_short_no_signal_routes_to_uncertain(self):
        """Very short text without module signal should route to route_uncertain."""
        result = tool_route_xingce_question("ab", options=None, strict_mode=True)
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"

    def test_no_options_short_text_routes_to_uncertain(self):
        """Short text with no options should route to route_uncertain."""
        result = tool_route_xingce_question("测试", options=None, strict_mode=True)
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"

    def test_warnings_contain_insufficient(self):
        """Warnings should contain insufficient/uncertain indicator."""
        result = tool_route_xingce_question("条件不足", options=None, strict_mode=True)
        warning_text = " ".join(result["warnings"])
        assert "insufficient" in warning_text or "uncertain" in warning_text

    def test_no_answer_fields_on_uncertain(self):
        """route_uncertain should not contain answer fields."""
        result = tool_route_xingce_question("条件不足", options=None, strict_mode=True)
        for f in self.FORBIDDEN:
            assert f not in result, f"route_uncertain has forbidden field: {f}"

    def test_reasoning_signals_not_empty(self):
        """reasoning_signals should not be empty."""
        result = tool_route_xingce_question("条件不足", options=None, strict_mode=True)
        assert len(result["reasoning_signals"]) > 0

    def test_weak_condition_not_high_confidence_logic_analysis(self):
        """Single '条件' should not trigger high confidence logic_analysis."""
        result = tool_route_xingce_question("条件", options=None, strict_mode=True)
        # Should be uncertain, not logic_analysis with high confidence
        assert result["module_guess"] != "logic_analysis" or result["confidence"] != "high"

    def test_strong_logic_analysis_still_works(self):
        """Strong logic_analysis signals should still route correctly."""
        result = tool_route_xingce_question(
            "甲乙丙三人排序 甲在乙前面 条件组合",
            options={"A": "甲第一", "B": "乙第一", "C": "丙第一", "D": "无法确定"},
        )
        assert result["module_guess"] == "logic_analysis"
        assert result["recommended_tool"] == "get_logic_analysis_scaffold"
        assert result["confidence"] == "high"

    def test_strict_mode_false_bypasses_insufficient_check(self):
        """strict_mode=False should bypass insufficient signal check."""
        result = tool_route_xingce_question("条件不足", options=None, strict_mode=False)
        # When strict_mode is False, may still route based on keywords
        # but should not crash
        assert "mode" in result
        assert result["mode"] == "route_only"


# ── compose_xingce_analysis_prompt tests ─────────────────────────────

class TestComposeXingceAnalysisPrompt:
    FORBIDDEN = ["answer", "selected_option", "prediction"]

    def test_exists(self):
        assert callable(tool_compose_xingce_analysis_prompt)

    def test_returns_dict(self):
        result = tool_compose_xingce_analysis_prompt("test question")
        assert isinstance(result, dict)

    def test_mode(self):
        result = tool_compose_xingce_analysis_prompt("test question")
        assert result["mode"] == "prompt_composition"

    def test_contains_route(self):
        result = tool_compose_xingce_analysis_prompt("test question")
        assert "route" in result
        assert result["route"]["mode"] == "route_only"

    def test_contains_prompt_text(self):
        result = tool_compose_xingce_analysis_prompt("test question")
        assert "prompt_text" in result
        assert isinstance(result["prompt_text"], str)
        assert len(result["prompt_text"]) > 0

    def test_contains_prompt_contract(self):
        result = tool_compose_xingce_analysis_prompt("test question")
        assert "prompt_contract" in result
        assert result["prompt_contract"]["must_not_force_answer"] is True
        assert result["prompt_contract"]["analysis_only_if_uncertain"] is True

    def test_no_answer_fields(self):
        result = tool_compose_xingce_analysis_prompt("test question")
        for f in self.FORBIDDEN:
            assert f not in result, f"Has forbidden field: {f}"

    def test_graphic_route(self):
        result = tool_compose_xingce_analysis_prompt("图形推理 规律 选择最合适的一项")
        assert result["route"]["module_guess"] == "graphic_reasoning"
        assert result["route"]["recommended_tool"] == "get_graphic_reasoning_scaffold"

    def test_definition_route(self):
        result = tool_compose_xingce_analysis_prompt("以下属于上述定义的是")
        assert result["route"]["module_guess"] == "definition_judgement"
        assert result["route"]["recommended_tool"] == "get_definition_judgement_scaffold"

    def test_analogy_route(self):
        result = tool_compose_xingce_analysis_prompt(
            "医生：医院", options={"A": "教师：学校", "B": "农民：工地"}
        )
        assert result["route"]["module_guess"] == "analogy_reasoning"
        assert result["route"]["recommended_tool"] == "get_analogy_reasoning_scaffold"

    def test_quantity_route(self):
        result = tool_compose_xingce_analysis_prompt("工程问题 甲乙合作几天")
        assert result["route"]["module_guess"] == "quantity_relation"
        assert result["route"]["recommended_tool"] == "get_quantity_relation_scaffold"

    def test_verbal_route(self):
        result = tool_compose_xingce_analysis_prompt("这段文字的主旨是什么")
        assert result["route"]["module_guess"] == "verbal_reasoning"
        assert result["route"]["recommended_tool"] == "get_verbal_reasoning_scaffold"

    def test_logic_reasoning_solver_candidate(self):
        result = tool_compose_xingce_analysis_prompt("以下哪项最能削弱上述论证")
        assert result["route"]["module_guess"] == "logic_reasoning"
        assert result["route"]["recommended_track"] == "solver_candidate"
        assert "不调用 solver" in result["prompt_text"] or "不调用solver" in result["prompt_text"]

    def test_data_analysis_solver_candidate(self):
        result = tool_compose_xingce_analysis_prompt("根据资料 同比增长率是多少")
        assert result["route"]["module_guess"] == "data_analysis"
        assert result["route"]["recommended_track"] == "solver_candidate"
        assert "不调用 solver" in result["prompt_text"] or "不调用solver" in result["prompt_text"]

    def test_unknown_route(self):
        result = tool_compose_xingce_analysis_prompt("abc123 random")
        assert result["route"]["module_guess"] == "unknown"
        assert result["route"]["recommended_track"] == "route_uncertain"
        assert "analysis_only" in result["prompt_text"]

    def test_prompt_text_contains_verification(self):
        result = tool_compose_xingce_analysis_prompt("test question")
        assert "逐项核验" in result["prompt_text"]

    def test_prompt_text_contains_analysis_only(self):
        result = tool_compose_xingce_analysis_prompt("test question")
        assert "analysis_only" in result["prompt_text"]

    def test_no_solver_call(self):
        mod = __import__("xingce_solver.mcp_server", fromlist=["mcp_server"])
        func = getattr(mod, "tool_compose_xingce_analysis_prompt")
        source = inspect.getsource(func)
        for solver in ["solve_logic_reasoning", "solve_data_analysis"]:
            assert solver not in source, f"compose_xingce_analysis_prompt calls {solver}"


# ── compose route_uncertain hardening tests ──────────────────────────

class TestComposeRouteUncertainHardening:
    """Test that compose handles route_uncertain properly."""

    FORBIDDEN = ["answer", "selected_option", "prediction"]

    def test_insufficient_condition_compose_route(self):
        """compose should reflect route_uncertain for '条件不足'."""
        result = tool_compose_xingce_analysis_prompt(
            "条件不足", options=None, strict_mode=True
        )
        assert result["route"]["module_guess"] == "unknown"
        assert result["route"]["recommended_track"] == "route_uncertain"
        assert result["route"]["recommended_tool"] is None

    def test_insufficient_info_compose_route(self):
        """compose should reflect route_uncertain for '信息不足'."""
        result = tool_compose_xingce_analysis_prompt(
            "信息不足", options=None, strict_mode=True
        )
        assert result["route"]["module_guess"] == "unknown"
        assert result["route"]["recommended_track"] == "route_uncertain"

    def test_compose_uncertain_prompt_contains_analysis_only(self):
        """compose prompt_text should contain analysis_only for uncertain route."""
        result = tool_compose_xingce_analysis_prompt(
            "条件不足", options=None, strict_mode=True
        )
        assert "analysis_only" in result["prompt_text"]

    def test_compose_uncertain_no_answer_fields(self):
        """compose with uncertain route should not contain answer fields."""
        result = tool_compose_xingce_analysis_prompt(
            "条件不足", options=None, strict_mode=True
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"compose uncertain has forbidden field: {f}"

    def test_compose_uncertain_prompt_contract(self):
        """compose uncertain should have proper prompt_contract."""
        result = tool_compose_xingce_analysis_prompt(
            "条件不足", options=None, strict_mode=True
        )
        assert result["prompt_contract"]["must_not_force_answer"] is True
        assert result["prompt_contract"]["analysis_only_if_uncertain"] is True

    def test_compose_empty_text_route(self):
        """compose should handle empty text."""
        result = tool_compose_xingce_analysis_prompt(
            "", options=None, strict_mode=True
        )
        assert result["route"]["module_guess"] == "unknown"
        assert result["route"]["recommended_track"] == "route_uncertain"

    def test_compose_weak_condition_not_high_confidence_logic_analysis(self):
        """compose should not give high confidence logic_analysis for weak signal."""
        result = tool_compose_xingce_analysis_prompt(
            "条件", options=None, strict_mode=True
        )
        # Should be uncertain or low confidence, not high confidence logic_analysis
        assert (
            result["route"]["module_guess"] != "logic_analysis"
            or result["route"]["confidence"] != "high"
        )

    def test_compose_strong_logic_analysis_still_works(self):
        """compose should still handle strong logic_analysis signals."""
        result = tool_compose_xingce_analysis_prompt(
            "甲乙丙三人排序 甲在乙前面 条件组合",
            options={"A": "甲第一", "B": "乙第一", "C": "丙第一", "D": "无法确定"},
        )
        assert result["route"]["module_guess"] == "logic_analysis"
        assert result["route"]["recommended_tool"] == "get_logic_analysis_scaffold"


# ── true-question routing hardening v0.2 tests ──────────────────────

class TestTrueQuestionRoutingV02:
    """Test true-question routing hardening v0.2."""

    FORBIDDEN = ["answer", "selected_option", "prediction"]

    # ── analogy reasoning with ∶ symbol ──────────────────────────────

    def test_analogy_ratio_symbol_simple(self):
        """卫冕∶夺冠 should route to analogy_reasoning."""
        result = tool_route_xingce_question(
            "卫冕∶夺冠",
            options={"A": "火器∶枪", "B": "演员∶歌唱", "C": "教师∶教书", "D": "运动员∶比赛"},
            strict_mode=True,
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["confidence"] == "high"
        assert result["recommended_track"] == "scaffold_guidance"
        assert result["recommended_tool"] == "get_analogy_reasoning_scaffold"

    def test_analogy_ratio_symbol_complex(self):
        """酒器∶尊∶爵 should route to analogy_reasoning."""
        result = tool_route_xingce_question(
            "酒器∶尊∶爵",
            options={"A": "兵器∶剑∶矛", "B": "家具∶桌∶椅", "C": "乐器∶琴∶瑟", "D": "文具∶笔∶墨"},
            strict_mode=True,
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["confidence"] == "high"
        assert result["recommended_tool"] == "get_analogy_reasoning_scaffold"

    def test_analogy_ratio_no_answer_fields(self):
        """analogy route should not contain answer fields."""
        result = tool_route_xingce_question(
            "卫冕∶夺冠",
            options={"A": "火器∶枪", "B": "演员∶歌唱"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"analogy route has forbidden field: {f}"

    # ── quantity relation economic/proportion ────────────────────────

    def test_quantity_economic_income_expense(self):
        """economic income/expense question should route to quantity_relation."""
        result = tool_route_xingce_question(
            "某企业去年全年收入1200万元，支出960万元。今年收入增加，支出减少，问今年上半年支出比下半年如何？",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "quantity_relation"
        assert result["recommended_track"] == "scaffold_guidance"
        assert result["recommended_tool"] == "get_quantity_relation_scaffold"

    def test_quantity_economic_no_answer_fields(self):
        """quantity economic route should not contain answer fields."""
        result = tool_route_xingce_question(
            "某企业去年全年收入1200万元，支出960万元。",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"quantity route has forbidden field: {f}"

    # ── logic analysis arrangement ───────────────────────────────────

    def test_logic_analysis_person_month_city(self):
        """person-month-city arrangement should route to logic_analysis."""
        result = tool_route_xingce_question(
            "张、王、李、杨4人到上海、苏州、杭州和南京调研，每个月城市均不同，问以下哪项不可能？",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"
        assert result["confidence"] in ("high", "medium")
        assert result["recommended_track"] == "scaffold_guidance"
        assert result["recommended_tool"] == "get_logic_analysis_scaffold"

    def test_logic_analysis_arrangement_no_answer_fields(self):
        """logic analysis arrangement route should not contain answer fields."""
        result = tool_route_xingce_question(
            "张、王、李、杨4人到上海、苏州、杭州和南京调研",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"logic_analysis route has forbidden field: {f}"

    # ── route_uncertain preservation ─────────────────────────────────

    def test_route_uncertain_condition_insufficient(self):
        """条件不足 should still route to route_uncertain."""
        result = tool_route_xingce_question(
            "条件不足", options=None, strict_mode=True
        )
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"
        assert result["recommended_tool"] is None
        assert any("insufficient" in w or "uncertain" in w for w in result["warnings"])

    def test_route_uncertain_condition_alone(self):
        """条件 alone should route to route_uncertain, not high confidence logic_analysis."""
        result = tool_route_xingce_question(
            "条件", options=None, strict_mode=True
        )
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"
        # Must not be high confidence logic_analysis
        assert not (result["module_guess"] == "logic_analysis" and result["confidence"] == "high")

    # ── strong logic_analysis preserved ──────────────────────────────

    def test_strong_logic_analysis_preserved(self):
        """甲乙丙 排序 位置 条件 should still route to logic_analysis."""
        result = tool_route_xingce_question(
            "甲乙丙 排序 位置 条件",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"
        assert result["confidence"] == "high"
        assert result["recommended_tool"] == "get_logic_analysis_scaffold"

    def test_strong_logic_analysis_no_answer_fields(self):
        """strong logic_analysis route should not contain answer fields."""
        result = tool_route_xingce_question(
            "甲乙丙 排序 位置 条件",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"logic_analysis route has forbidden field: {f}"


# ── model-in-the-loop routing review v0.3 tests ──────────────────────

class TestModelInTheLoopRoutingV03:
    """Test model-in-the-loop routing review v0.3."""

    FORBIDDEN = ["answer", "selected_option", "prediction"]

    # ── new route fields ─────────────────────────────────────────────

    def test_route_has_model_review_required(self):
        """route should have model_review_required field."""
        result = tool_route_xingce_question("测试题目", strict_mode=True)
        assert "model_review_required" in result
        assert isinstance(result["model_review_required"], bool)

    def test_route_has_override_allowed(self):
        """route should have override_allowed field."""
        result = tool_route_xingce_question("测试题目", strict_mode=True)
        assert "override_allowed" in result
        assert result["override_allowed"] is True

    def test_route_has_review_instruction(self):
        """route should have review_instruction field."""
        result = tool_route_xingce_question("测试题目", strict_mode=True)
        assert "review_instruction" in result
        assert "advisory" in result["review_instruction"].lower()

    def test_route_has_possible_modules(self):
        """route should have possible_modules field."""
        result = tool_route_xingce_question("测试题目", strict_mode=True)
        assert "possible_modules" in result
        assert isinstance(result["possible_modules"], list)

    def test_route_has_conflict_signals(self):
        """route should have conflict_signals field."""
        result = tool_route_xingce_question("测试题目", strict_mode=True)
        assert "conflict_signals" in result
        assert isinstance(result["conflict_signals"], list)

    # ── model_review_required scenarios ──────────────────────────────

    def test_model_review_required_for_medium_confidence(self):
        """v0.5.0: module_hint gives high confidence → no model review required."""
        result = tool_route_xingce_question("测试题目", module_hint="verbal_reasoning")
        # v0.5.0: module_hint applied with high confidence → model_review_required=False
        assert result["module_hint_applied"] is True
        assert result["confidence"] == "high"
        assert result["model_review_required"] is False

    def test_model_review_required_for_unknown(self):
        """unknown module should require model review."""
        result = tool_route_xingce_question("abc123 random", strict_mode=True)
        assert result["model_review_required"] is True

    def test_model_review_required_for_route_uncertain(self):
        """route_uncertain should require model review."""
        result = tool_route_xingce_question("条件不足", strict_mode=True)
        assert result["model_review_required"] is True

    def test_model_review_required_for_conflict(self):
        """conflict signals should require model review."""
        result = tool_route_xingce_question(
            "将以上6个句子重新排列，语序正确的一项是",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        assert result["model_review_required"] is True
        assert len(result["conflict_signals"]) > 0

    # ── sentence ordering → verbal_reasoning ─────────────────────────

    def test_sentence_order_to_verbal_reasoning(self):
        """sentence ordering pattern should route to verbal_reasoning."""
        result = tool_route_xingce_question(
            "将以上6个句子重新排列，语序正确的一项是（ ）",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["confidence"] == "high"
        assert "sentence_order_pattern" in result["reasoning_signals"]
        assert "contains_排列_but_sentence_order_pattern" in result["conflict_signals"]

    def test_sentence_order_possible_modules(self):
        """sentence ordering should have verbal_reasoning in possible_modules."""
        result = tool_route_xingce_question(
            "将以上6个句子重新排列，语序正确的一项是",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        modules = [pm["module"] for pm in result["possible_modules"]]
        assert "verbal_reasoning" in modules

    def test_sentence_order_no_answer_fields(self):
        """sentence ordering route should not contain answer fields."""
        result = tool_route_xingce_question(
            "将以上6个句子重新排列，语序正确的一项是",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"sentence order route has forbidden field: {f}"

    # ── sentence insertion → verbal_reasoning ────────────────────────

    def test_sentence_insertion_to_verbal_reasoning(self):
        """sentence insertion pattern should route to verbal_reasoning."""
        result = tool_route_xingce_question(
            "下面这段文字最适合填入文中哪个位置？",
            options={"A": "①处", "B": "②处", "C": "③处", "D": "④处"},
            strict_mode=True,
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["confidence"] == "high"
        assert "sentence_insertion_pattern" in result["reasoning_signals"]
        assert "contains_位置_but_sentence_insertion_pattern" in result["conflict_signals"]

    def test_sentence_insertion_possible_modules(self):
        """sentence insertion should have verbal_reasoning in possible_modules."""
        result = tool_route_xingce_question(
            "下面这段文字最适合填入文中哪个位置？",
            options={"A": "①处", "B": "②处"},
            strict_mode=True,
        )
        modules = [pm["module"] for pm in result["possible_modules"]]
        assert "verbal_reasoning" in modules

    def test_sentence_insertion_no_answer_fields(self):
        """sentence insertion route should not contain answer fields."""
        result = tool_route_xingce_question(
            "下面这段文字最适合填入文中哪个位置？",
            options={"A": "①处", "B": "②处"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"sentence insertion route has forbidden field: {f}"

    # ── main idea pattern → verbal_reasoning ─────────────────────────

    def test_main_idea_introduce(self):
        """主要介绍 should route to verbal_reasoning."""
        result = tool_route_xingce_question(
            "这段文字主要介绍的是：",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["confidence"] == "high"
        assert "main_idea_pattern" in result["reasoning_signals"]

    def test_main_idea_talk(self):
        """主要讲 should route to verbal_reasoning."""
        result = tool_route_xingce_question(
            "这段文字主要讲的是：",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert "main_idea_pattern" in result["reasoning_signals"]

    def test_main_idea_explain(self):
        """主要说明 should route to verbal_reasoning."""
        result = tool_route_xingce_question(
            "这段文字主要说明：",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert "main_idea_pattern" in result["reasoning_signals"]

    def test_main_idea_no_answer_fields(self):
        """main idea route should not contain answer fields."""
        result = tool_route_xingce_question(
            "这段文字主要介绍的是：",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"main idea route has forbidden field: {f}"

    # ── three-part analogy ───────────────────────────────────────────

    def test_three_part_analogy(self):
        """感想∶主观性∶体会 should route to analogy_reasoning."""
        result = tool_route_xingce_question(
            "感想∶主观性∶体会",
            options={
                "A": "观察∶客观性∶记录",
                "B": "计划∶可行性∶执行",
                "C": "预测∶准确性∶验证",
                "D": "创新∶独特性∶突破",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["confidence"] == "high"
        assert "analogy_structure" in result["reasoning_signals"]
        assert "analogy_symbol_detected" in result["conflict_signals"]

    def test_three_part_analogy_no_answer_fields(self):
        """three-part analogy route should not contain answer fields."""
        result = tool_route_xingce_question(
            "感想∶主观性∶体会",
            options={"A": "观察∶客观性∶记录", "B": "计划∶可行性∶执行"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"three-part analogy route has forbidden field: {f}"

    # ── data analysis extended patterns ──────────────────────────────

    def test_data_analysis_extended_zhanquan(self):
        """占全国 should route to data_analysis."""
        result = tool_route_xingce_question(
            "2022年中部六省中型灌区新增节水能力占全国中型灌区的（ ）",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"
        assert "data_analysis_extended_pattern" in result["reasoning_signals"]

    def test_data_analysis_extended_bizhong(self):
        """比重 should route to data_analysis."""
        result = tool_route_xingce_question(
            "2022年某地区GDP占全国的比重是多少？",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"

    def test_data_analysis_extended_tongbi(self):
        """同比增长 should route to data_analysis."""
        result = tool_route_xingce_question(
            "2022年某市GDP同比增长多少？",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"

    def test_data_analysis_extended_shangshuziliao(self):
        """上述资料 should route to data_analysis."""
        result = tool_route_xingce_question(
            "能够从上述资料中推出的是：",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"

    def test_data_analysis_extended_possible_modules(self):
        """data analysis extended should have data_analysis in possible_modules."""
        result = tool_route_xingce_question(
            "2022年某地区GDP占全国的比重是多少？",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        modules = [pm["module"] for pm in result["possible_modules"]]
        assert "data_analysis" in modules

    def test_data_analysis_extended_no_answer_fields(self):
        """data analysis extended route should not contain answer fields."""
        result = tool_route_xingce_question(
            "2022年某地区GDP占全国的比重是多少？",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"data analysis extended route has forbidden field: {f}"

    # ── compose prompt contains model review ─────────────────────────

    def test_compose_prompt_contains_model_review(self):
        """compose prompt should contain model review instructions."""
        result = tool_compose_xingce_analysis_prompt(
            "测试题目", options={"A": "选项A", "B": "选项B"}, strict_mode=True
        )
        assert "题型复核提示" in result["prompt_text"]
        assert "advisory" in result["prompt_text"].lower()

    def test_compose_prompt_contains_override_allowed(self):
        """compose prompt should mention override allowed."""
        result = tool_compose_xingce_analysis_prompt(
            "测试题目", options={"A": "选项A", "B": "选项B"}, strict_mode=True
        )
        assert "override" in result["prompt_text"].lower() or "改判" in result["prompt_text"]

    def test_compose_prompt_contains_possible_modules(self):
        """compose prompt should contain possible_modules."""
        result = tool_compose_xingce_analysis_prompt(
            "将以上6个句子重新排列，语序正确的一项是",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        assert "possible_modules" in result["prompt_text"]

    def test_compose_prompt_contains_conflict_signals(self):
        """compose prompt should contain conflict_signals."""
        result = tool_compose_xingce_analysis_prompt(
            "将以上6个句子重新排列，语序正确的一项是",
            options={"A": "选项A", "B": "选项B"},
            strict_mode=True,
        )
        assert "conflict_signals" in result["prompt_text"]

    def test_compose_route_has_new_fields(self):
        """compose route should have new v0.3 fields."""
        result = tool_compose_xingce_analysis_prompt(
            "测试题目", options={"A": "选项A", "B": "选项B"}, strict_mode=True
        )
        assert "possible_modules" in result["route"]
        assert "model_review_required" in result["route"]
        assert "override_allowed" in result["route"]
        assert "review_instruction" in result["route"]
        assert "conflict_signals" in result["route"]

    # ── safety checks ────────────────────────────────────────────────

    def test_no_answer_fields_in_any_route(self):
        """no route should contain answer fields."""
        test_cases = [
            ("将以上6个句子重新排列，语序正确的一项是", {"A": "选项A", "B": "选项B"}),
            ("下面这段文字最适合填入文中哪个位置？", {"A": "①处", "B": "②处"}),
            ("这段文字主要介绍的是：", {"A": "选项A", "B": "选项B"}),
            ("感想∶主观性∶体会", {"A": "观察∶客观性∶记录", "B": "计划∶可行性∶执行"}),
            ("2022年某地区GDP占全国的比重是多少？", {"A": "选项A", "B": "选项B"}),
        ]
        for text, opts in test_cases:
            result = tool_route_xingce_question(text, options=opts, strict_mode=True)
            for f in self.FORBIDDEN:
                assert f not in result, f"route for '{text[:20]}...' has forbidden field: {f}"

    def test_no_solver_call_in_route(self):
        """route function should not call solver."""
        mod = __import__("xingce_solver.mcp_server", fromlist=["mcp_server"])
        func = getattr(mod, "tool_route_xingce_question")
        source = inspect.getsource(func)
        for solver in ["solve_logic_reasoning", "solve_data_analysis"]:
            assert solver not in source, f"route_xingce_question calls {solver}"

    def test_no_solver_call_in_compose(self):
        """compose function should not call solver."""
        mod = __import__("xingce_solver.mcp_server", fromlist=["mcp_server"])
        func = getattr(mod, "tool_compose_xingce_analysis_prompt")
        source = inspect.getsource(func)
        for solver in ["solve_logic_reasoning", "solve_data_analysis"]:
            assert solver not in source, f"compose_xingce_analysis_prompt calls {solver}"


# ── analogy priority bugfix v0.3.1 tests ────────────────────────────

class TestAnalogyPriorityBugfixV031:
    """Test analogy routing priority before graphic keywords (v0.3.1)."""

    FORBIDDEN = ["answer", "selected_option", "prediction"]

    # ── three-part analogy with graphic keyword in options ───────────

    def test_three_part_analogy_with_gui_lv_in_options(self):
        """感想∶主观性∶体会 with 规律 in options should be analogy_reasoning."""
        result = tool_route_xingce_question(
            "感想∶主观性∶体会",
            options={
                "A": "规律∶客观性∶发现",
                "B": "示范性∶形象∶展示",
                "C": "标准∶统一性∶判断",
                "D": "情绪∶波动性∶表达",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["confidence"] == "high"
        assert result["recommended_tool"] == "get_analogy_reasoning_scaffold"
        assert "analogy_structure" in result["reasoning_signals"]
        assert "analogy_symbol_detected" in result["conflict_signals"]

    def test_three_part_analogy_with_gui_lv_no_answer_fields(self):
        """three-part analogy with 规律 should not have answer fields."""
        result = tool_route_xingce_question(
            "感想∶主观性∶体会",
            options={
                "A": "规律∶客观性∶发现",
                "B": "示范性∶形象∶展示",
                "C": "标准∶统一性∶判断",
                "D": "情绪∶波动性∶表达",
            },
            strict_mode=True,
        )
        for f in self.FORBIDDEN:
            assert f not in result, f"three-part analogy has forbidden field: {f}"

    def test_three_part_analogy_with_gui_lv_has_v03_fields(self):
        """three-part analogy with 规律 should have v0.3 fields."""
        result = tool_route_xingce_question(
            "感想∶主观性∶体会",
            options={
                "A": "规律∶客观性∶发现",
                "B": "示范性∶形象∶展示",
                "C": "标准∶统一性∶判断",
                "D": "情绪∶波动性∶表达",
            },
            strict_mode=True,
        )
        assert "possible_modules" in result
        assert "model_review_required" in result
        assert "override_allowed" in result
        assert result["override_allowed"] is True
        assert "review_instruction" in result
        assert "conflict_signals" in result

    # ── two-part analogy still works ─────────────────────────────────

    def test_two_part_analogy_still_works(self):
        """卫冕∶夺冠 should still route to analogy_reasoning."""
        result = tool_route_xingce_question(
            "卫冕∶夺冠",
            options={
                "A": "冒险∶孤注一掷",
                "B": "竞赛∶调解",
                "C": "触犯∶惩罚",
                "D": "开辟∶创立",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["confidence"] == "high"
        assert result["recommended_tool"] == "get_analogy_reasoning_scaffold"

    # ── three-part analogy "酒器∶尊∶爵" still works ──────────────────

    def test_three_part_analogy_jiuqi_still_works(self):
        """酒器∶尊∶爵 should still route to analogy_reasoning."""
        result = tool_route_xingce_question(
            "酒器∶尊∶爵",
            options={
                "A": "茶具∶壶∶杯",
                "B": "餐具∶碗∶筷",
                "C": "酒器∶尊∶爵",
                "D": "乐器∶琴∶瑟",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["confidence"] == "high"
        assert result["recommended_tool"] == "get_analogy_reasoning_scaffold"

    # ── graphic reasoning not degraded ───────────────────────────────

    def test_graphic_reasoning_not_degraded(self):
        """graphic question should still route to graphic_reasoning."""
        result = tool_route_xingce_question(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "graphic_reasoning"
        assert result["confidence"] == "high"
        assert result["recommended_tool"] == "get_graphic_reasoning_scaffold"

    def test_graphic_reasoning_heibai_not_degraded(self):
        """黑白块图形题 should still route to graphic_reasoning."""
        result = tool_route_xingce_question(
            "下列图形中，黑白块位置变化，选择最合适的一项。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "graphic_reasoning"
        assert result["recommended_tool"] == "get_graphic_reasoning_scaffold"

    def test_graphic_reasoning_tuxingtui_li_not_degraded(self):
        """图形推理题 should still route to graphic_reasoning."""
        result = tool_route_xingce_question(
            "图形推理：下列图形中，哪一项与题干图形规律一致？",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "graphic_reasoning"
        assert result["recommended_tool"] == "get_graphic_reasoning_scaffold"


# ── 8.16 compose_xingce_answer_prompt (v0.4) ─────────────────────────


class TestComposeAnswerPromptExist:
    """Test that compose_xingce_answer_prompt tool exists."""

    def test_tool_exists(self):
        assert callable(tool_compose_xingce_answer_prompt)

    def test_returns_dict(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert isinstance(result, dict)


class TestComposeAnswerPromptFields:
    """Test that compose_xingce_answer_prompt returns required fields."""

    def test_has_required_top_level_fields(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "tool" in result
        assert "version" in result
        assert "route" in result
        assert "answer_prompt" in result
        assert "output_schema" in result
        assert "safety_contract" in result
        assert "answer_allowed" in result
        assert "analysis_only_required_if" in result
        assert "model_review_required" in result
        assert "override_allowed" in result

    def test_tool_name_is_correct(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert result["tool"] == "compose_xingce_answer_prompt"

    def test_version_is_v04(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert result["version"] in ("v0.4", "v0.4.1", "v0.4.2", "v0.5.0")

    def test_route_has_v03_fields(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        route = result["route"]
        assert "possible_modules" in route
        assert "model_review_required" in route
        assert "override_allowed" in route
        assert "review_instruction" in route
        assert "conflict_signals" in route


class TestComposeAnswerPromptSafety:
    """Test that compose_xingce_answer_prompt does not return forbidden fields."""

    def test_no_answer_field(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "answer" not in result

    def test_no_selected_option_field(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "selected_option" not in result

    def test_no_prediction_field(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "prediction" not in result


class TestComposeAnswerPromptContent:
    """Test answer_prompt content constraints."""

    def test_answer_prompt_contains_route_advisory(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "MCP route is advisory, not final" in result["answer_prompt"]

    def test_answer_prompt_contains_unique_answer(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "exactly one option is justified" in result["answer_prompt"]

    def test_answer_prompt_contains_analysis_only(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "analysis_only" in result["answer_prompt"]

    def test_answer_prompt_contains_no_invent(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "Do not invent missing visual/table content" in result["answer_prompt"]

    def test_answer_prompt_contains_no_guessing(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "Do not guess" in result["answer_prompt"]

    def test_answer_prompt_contains_no_default_first(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "Do not default to A or the first option" in result["answer_prompt"]


class TestComposeAnswerPromptModuleConstraints:
    """Test module-specific constraints in answer_prompt."""

    def test_graphic_module_has_visual_constraint(self):
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
        )
        prompt = result["answer_prompt"]
        assert "missing visual" in prompt.lower() or "missing figure" in prompt.lower()
        assert "analysis_only" in prompt

    def test_data_analysis_has_table_constraint(self):
        result = tool_compose_xingce_answer_prompt(
            "2022年某地区GDP占全国的比重是多少？",
            options={"A": "10%", "B": "20%", "C": "30%", "D": "40%"},
            strict_mode=True,
        )
        prompt = result["answer_prompt"]
        assert "table" in prompt.lower() or "material" in prompt.lower()
        assert "analysis_only" in prompt

    def test_analogy_has_relationship_constraint(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        prompt = result["answer_prompt"]
        assert "relationship" in prompt.lower() or "relation" in prompt.lower()


class TestComposeAnswerPromptOutputSchema:
    """Test output_schema structure."""

    def test_output_schema_has_mode(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "mode" in result["output_schema"]

    def test_output_schema_has_safety_checks(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "safety_checks" in result["output_schema"]
        sc = result["output_schema"]["safety_checks"]
        assert "read_full_question" in sc
        assert "unique_option_justified" in sc
        assert "no_guessing" in sc


class TestComposeAnswerPromptSafetyContract:
    """Test safety_contract structure."""

    def test_safety_contract_has_required_fields(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        sc = result["safety_contract"]
        assert sc["no_answer_field_in_tool_return"] is True
        assert sc["no_solver_call"] is True
        assert sc["no_external_llm_api"] is True
        assert sc["answer_only_when_unique"] is True
        assert sc["no_default_to_first_option"] is True
        assert sc["no_invented_visual_or_table"] is True


class TestComposeAnswerPromptAnalysisOnlyRequiredIf:
    """Test analysis_only_required_if list."""

    def test_has_required_conditions(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        conditions = result["analysis_only_required_if"]
        assert "missing_visual_content" in conditions
        assert "missing_table_or_material" in conditions
        assert "multiple_plausible_options" in conditions
        assert "low_confidence" in conditions
        assert "route_uncertain_without_semantic_override" in conditions


class TestComposeAnswerPromptRouting:
    """Test that routing still works correctly in answer prompt."""

    def test_analogy_bug_sample_still_analogy(self):
        """感想∶主观性∶体会 should route to analogy_reasoning."""
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={
                "A": "规律∶客观性∶发现",
                "B": "示范性∶形象∶展示",
                "C": "标准∶统一性∶判断",
                "D": "情绪∶波动性∶表达",
            },
            strict_mode=True,
        )
        assert result["route"]["module_guess"] == "analogy_reasoning"
        assert result["route"]["recommended_tool"] == "get_analogy_reasoning_scaffold"

    def test_graphic_sample_still_graphic(self):
        """图形规律题 should route to graphic_reasoning."""
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
        )
        assert result["route"]["module_guess"] == "graphic_reasoning"
        assert result["route"]["recommended_tool"] == "get_graphic_reasoning_scaffold"

    def test_route_uncertain_still_conservative(self):
        """条件不足 should be route_uncertain."""
        result = tool_compose_xingce_answer_prompt(
            "条件不足",
            strict_mode=True,
        )
        assert result["route"]["module_guess"] == "unknown"
        assert result["route"]["recommended_track"] == "route_uncertain"
        assert result["answer_allowed"] is False

    def test_logic_analysis_strong_signal(self):
        """甲乙丙 排序 位置 条件 should route to logic_analysis."""
        result = tool_compose_xingce_answer_prompt(
            "甲乙丙 排序 位置 条件",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
        )
        assert result["route"]["module_guess"] == "logic_analysis"
        assert result["route"]["recommended_tool"] == "get_logic_analysis_scaffold"


class TestComposeAnswerPromptAllowAnswer:
    """Test allow_answer parameter."""

    def test_allow_answer_false_forces_analysis_only(self):
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
            allow_answer=False,
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "answer_mode_disabled"
        assert "Answer Gate" in result["answer_prompt"]


# ── v0.4.1 Conservative Answer Gate Hardening Tests ──────────────


class TestLogicArrangementRouting:
    """Test that person arrangement questions with 左边/右边 route to logic_analysis."""

    def test_person_arrangement_with_left_right(self):
        """甲乙丙丁排成一排 + 左边 should be logic_analysis, not graphic_reasoning."""
        result = tool_route_xingce_question(
            "甲乙丙丁排成一排，甲不在两端，乙在丙左边，问下列哪项可能正确？",
            options={"A": "甲在最左边", "B": "乙在最右边", "C": "丙在甲左边", "D": "丁在最左边"},
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"

    def test_person_arrangement_with_position(self):
        """Person + position signals should route to logic_analysis."""
        result = tool_route_xingce_question(
            "小王小李小张坐在一排，小王不坐在两端，小李坐在小张右边。",
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"

    def test_graphic_left_right_still_works(self):
        """左边给定展开图 should still route to graphic_reasoning."""
        result = tool_route_xingce_question(
            "左边给定的是纸盒的展开图，右边哪一项可以由它折叠而成？",
            strict_mode=True,
        )
        assert result["module_guess"] == "graphic_reasoning"

    def test_graphic_pattern_still_works(self):
        """图形规律 should still route to graphic_reasoning."""
        result = tool_route_xingce_question(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            strict_mode=True,
        )
        assert result["module_guess"] == "graphic_reasoning"


class TestAnswerGateGraphicReasoning:
    """Test answer gate for graphic reasoning without visual content."""

    def test_graphic_without_image_blocks_answer(self):
        """Graphic reasoning without image should block answer."""
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
            image_present=False,
            visual_description="",
        )
        assert result["route"]["module_guess"] == "graphic_reasoning"
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_visual_content"
        assert "Answer Gate" in result["answer_prompt"]
        assert "analysis_only" in result["answer_prompt"]

    def test_graphic_with_image_allows_answer(self):
        """Graphic reasoning with image_present=true should allow answer."""
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
            image_present=True,
        )
        assert result["route"]["module_guess"] == "graphic_reasoning"
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None

    def test_graphic_with_visual_description_allows_answer(self):
        """Graphic reasoning with detailed visual_description should allow answer."""
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
            visual_description="图形由黑色和白色方块组成，黑色方块在每一行向右移动一格",
        )
        assert result["route"]["module_guess"] == "graphic_reasoning"
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None


class TestAnswerGateDataAnalysis:
    """Test answer gate for data analysis without material."""

    def test_data_analysis_without_material_blocks_answer(self):
        """Data analysis without material should block answer."""
        result = tool_compose_xingce_answer_prompt(
            "2022年中部六省中型灌区新增节水能力占全国中型灌区的比重约为多少？",
            options={"A": "15%", "B": "23%", "C": "31%", "D": "46%"},
            strict_mode=True,
            material_present=False,
            table_present=False,
            material_text="",
        )
        assert result["route"]["module_guess"] == "data_analysis"
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"
        assert "Answer Gate" in result["answer_prompt"]

    def test_data_analysis_with_material_allows_answer(self):
        """Data analysis with material_present=true should allow answer."""
        result = tool_compose_xingce_answer_prompt(
            "2022年中部六省中型灌区新增节水能力占全国中型灌区的比重约为多少？",
            options={"A": "15%", "B": "23%", "C": "31%", "D": "46%"},
            strict_mode=True,
            material_present=True,
        )
        assert result["route"]["module_guess"] == "data_analysis"
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None

    def test_data_analysis_with_table_allows_answer(self):
        """Data analysis with table_present=true should allow answer."""
        result = tool_compose_xingce_answer_prompt(
            "2022年中部六省中型灌区新增节水能力占全国中型灌区的比重约为多少？",
            options={"A": "15%", "B": "23%", "C": "31%", "D": "46%"},
            strict_mode=True,
            table_present=True,
        )
        assert result["route"]["module_guess"] == "data_analysis"
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None

    def test_data_analysis_with_material_text_allows_answer(self):
        """Data analysis with detailed material_text should allow answer."""
        result = tool_compose_xingce_answer_prompt(
            "2022年中部六省中型灌区新增节水能力占全国中型灌区的比重约为多少？",
            options={"A": "15%", "B": "23%", "C": "31%", "D": "46%"},
            strict_mode=True,
            material_text="2022年全国中型灌区新增节水能力为100万立方米，其中中部六省合计23万立方米。",
        )
        assert result["route"]["module_guess"] == "data_analysis"
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None


class TestAnswerGateRouteUncertain:
    """Test answer gate for route_uncertain."""

    def test_route_uncertain_blocks_answer(self):
        """Route uncertain should block answer."""
        result = tool_compose_xingce_answer_prompt(
            "条件不足",
            strict_mode=True,
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "route_uncertain_without_semantic_override"


class TestAnswerGateContextRequirements:
    """Test context_requirements field."""

    def test_context_requirements_graphic(self):
        """Graphic reasoning should have requires_visual=true."""
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
        )
        cr = result["context_requirements"]
        assert cr["requires_visual"] is True
        assert cr["requires_table_or_material"] is False
        assert cr["image_present"] is False

    def test_context_requirements_data_analysis(self):
        """Data analysis should have requires_table_or_material=true."""
        result = tool_compose_xingce_answer_prompt(
            "2022年中部六省中型灌区新增节水能力占全国中型灌区的比重约为多少？",
            options={"A": "15%", "B": "23%", "C": "31%", "D": "46%"},
            strict_mode=True,
        )
        cr = result["context_requirements"]
        assert cr["requires_visual"] is False
        assert cr["requires_table_or_material"] is True
        assert cr["material_present"] is False


class TestAnswerGateSafety:
    """Test that v0.4.1 changes don't introduce forbidden fields."""

    def test_no_answer_field_in_result(self):
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
            image_present=False,
        )
        assert "answer" not in result
        assert "selected_option" not in result
        assert "prediction" not in result

    def test_answer_block_reason_in_result(self):
        """answer_block_reason should be present in result."""
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
            image_present=False,
        )
        assert "answer_block_reason" in result
        assert result["answer_block_reason"] == "missing_visual_content"

    def test_context_requirements_in_result(self):
        """context_requirements should be present in result."""
        result = tool_compose_xingce_answer_prompt(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
        )
        assert "context_requirements" in result
        assert isinstance(result["context_requirements"], dict)


# ── v0.4.2 Data material gate hardening ─────────────────────────────

class TestDataMaterialGateRouting:
    """Test that material/table/chart signals route to data_analysis."""

    def test_table_avg_growth_route_to_data_analysis(self):
        """表中平均每年增长量 should route to data_analysis."""
        result = tool_route_xingce_question(
            "表中2018—2022年工业增加值平均每年增长量约为多少亿元？",
            options={"A": "120", "B": "180", "C": "240", "D": "300"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"

    def test_according_to_table_route_to_data_analysis(self):
        """根据表格 should route to data_analysis."""
        result = tool_route_xingce_question(
            "根据表格，2021年甲地区生产总值同比增长率约为多少？",
            options={"A": "3.2%", "B": "5.6%", "C": "7.1%", "D": "9.8%"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"

    def test_above_data_route_to_data_analysis(self):
        """上述资料 should route to data_analysis."""
        result = tool_route_xingce_question(
            "上述资料显示，2022年A市常住人口比上年增加了多少万人？",
            options={"A": "12", "B": "18", "C": "24", "D": "30"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"

    def test_chart_data_route_to_data_analysis(self):
        """图中数据 should route to data_analysis."""
        result = tool_route_xingce_question(
            "图中数据显示，第三季度销售额占全年销售额的比重约为多少？",
            options={"A": "18%", "B": "24%", "C": "31%", "D": "39%"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"


class TestDataMaterialGateNegativeCases:
    """Test that ordinary quantity relation questions are NOT misrouted."""

    def test_pool_problem_stays_quantity(self):
        """水池问题 should stay quantity_relation."""
        result = tool_route_xingce_question(
            "一个水池甲管注满需8小时，乙管注满需12小时，两管同时开几小时注满？",
            options={"A": "4.8", "B": "5", "C": "6", "D": "10"},
            strict_mode=True,
        )
        assert result["module_guess"] == "quantity_relation"

    def test_meeting_problem_stays_quantity(self):
        """相遇问题 should stay quantity_relation."""
        result = tool_route_xingce_question(
            "甲乙两车相向而行，甲车每小时60公里，乙车每小时80公里，几小时相遇？",
            options={"A": "2", "B": "3", "C": "4", "D": "5"},
            strict_mode=True,
        )
        assert result["module_guess"] == "quantity_relation"


class TestDataMaterialGateAnswerBlocking:
    """Test that material signals trigger answer blocking when material is missing."""

    def test_table_question_without_material_blocks_answer(self):
        """表中题缺表格材料时 answer_allowed=false."""
        result = tool_compose_xingce_answer_prompt(
            "表中2018—2022年工业增加值平均每年增长量约为多少亿元？",
            options={"A": "120", "B": "180", "C": "240", "D": "300"},
            strict_mode=True,
            allow_answer=True,
            material_present=False,
            table_present=False,
            material_text="",
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"
        assert result["context_requirements"]["requires_table_or_material"] is True
        assert "Answer Gate" in result["answer_prompt"]
        assert "analysis_only" in result["answer_prompt"]
        assert "answer = null" in result["answer_prompt"]

    def test_table_question_with_material_allows_answer(self):
        """表中题有表格材料时 answer_allowed=true."""
        result = tool_compose_xingce_answer_prompt(
            "表中2018—2022年工业增加值平均每年增长量约为多少亿元？",
            options={"A": "120", "B": "180", "C": "240", "D": "300"},
            strict_mode=True,
            allow_answer=True,
            table_present=True,
        )
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None
        assert result["context_requirements"]["requires_table_or_material"] is True

    def test_according_to_table_without_material_blocks(self):
        """根据表格题缺材料时 answer_allowed=false."""
        result = tool_compose_xingce_answer_prompt(
            "根据表格，2021年甲地区生产总值同比增长率约为多少？",
            options={"A": "3.2%", "B": "5.6%", "C": "7.1%", "D": "9.8%"},
            strict_mode=True,
            allow_answer=True,
            material_present=False,
            table_present=False,
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"
        assert result["context_requirements"]["requires_table_or_material"] is True

    def test_above_data_without_material_blocks(self):
        """上述资料题缺材料时 answer_allowed=false."""
        result = tool_compose_xingce_answer_prompt(
            "上述资料显示，2022年A市常住人口比上年增加了多少万人？",
            options={"A": "12", "B": "18", "C": "24", "D": "30"},
            strict_mode=True,
            allow_answer=True,
            material_present=False,
            table_present=False,
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"

    def test_chart_data_without_material_blocks(self):
        """图中数据题缺材料时 answer_allowed=false."""
        result = tool_compose_xingce_answer_prompt(
            "图中数据显示，第三季度销售额占全年销售额的比重约为多少？",
            options={"A": "18%", "B": "24%", "C": "31%", "D": "39%"},
            strict_mode=True,
            allow_answer=True,
            material_present=False,
            table_present=False,
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"
        assert result["context_requirements"]["requires_table_or_material"] is True


class TestDataMaterialGateSafety:
    """Test that v0.4.2 changes don't introduce forbidden fields."""

    def test_no_answer_field_in_material_gate_result(self):
        """No answer/selected_option/prediction in result."""
        result = tool_compose_xingce_answer_prompt(
            "表中2018—2022年工业增加值平均每年增长量约为多少亿元？",
            options={"A": "120", "B": "180", "C": "240", "D": "300"},
            strict_mode=True,
            allow_answer=True,
            material_present=False,
            table_present=False,
        )
        assert "answer" not in result
        assert "selected_option" not in result
        assert "prediction" not in result


class TestTextArrangementRouting:
    """v0.4.3: Text-based arrangement/sequencing → logic_analysis."""

    def test_book_arrangement(self):
        """四本书从左到右摆放 → logic_analysis."""
        result = tool_route_xingce_question(
            "四本书从左到右摆放，语文书不在最左边，数学书在英语书左边，以下哪项可能为真？",
            options={
                "A": "语文书在最右边",
                "B": "数学书在英语书右边",
                "C": "英语书在最左边",
                "D": "语文书在数学书左边",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"
        assert "text_arrangement_signals" in result["reasoning_signals"]

    def test_contestant_order(self):
        """选手按顺序出场 → logic_analysis."""
        result = tool_route_xingce_question(
            "A、B、C、D四名选手按顺序出场，A早于C，B不相邻D，问可能的出场顺序是？",
            options={"A": "ABCD", "B": "BACD", "C": "BDAC", "D": "DCBA"},
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"
        assert "text_arrangement_signals" in result["reasoning_signals"]

    def test_program_performance_order(self):
        """节目依次演出 → logic_analysis."""
        result = tool_route_xingce_question(
            "五个节目依次演出，舞蹈在合唱前面，小品不在最后，以下安排可能正确的是？",
            options={
                "A": "舞蹈-合唱-小品",
                "B": "小品-舞蹈-合唱",
                "C": "合唱-舞蹈-小品",
                "D": "合唱-小品-舞蹈",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"
        assert "text_arrangement_signals" in result["reasoning_signals"]

    def test_graphic_left_given_still_graphic(self):
        """左边给定纸盒展开图 → graphic_reasoning (不退化)."""
        result = tool_route_xingce_question(
            "左边给定的是纸盒的展开图，右边哪一项可以由它折叠而成？",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "graphic_reasoning"


class TestDefinitionJudgementRouting:
    """v0.4.3: Clear definition questions → definition_judgement."""

    def test_opportunity_cost(self):
        """所谓机会成本...下列体现 → definition_judgement."""
        result = tool_route_xingce_question(
            "所谓机会成本，是指为了得到某种东西而放弃的其他选择中价值最高者。下列体现机会成本的是？",
            options={
                "A": "某人看电影放弃了加班收入",
                "B": "某人买东西花了100元",
                "C": "某人存钱获得利息",
                "D": "某人获得奖金",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "definition_judgement"
        assert "definition_intro_question_pattern" in result["reasoning_signals"]

    def test_information_cocoon(self):
        """信息茧房是指...下列属于 → definition_judgement."""
        result = tool_route_xingce_question(
            "概念界定：信息茧房是指人们只接触自己感兴趣的信息。下列属于信息茧房的是？",
            options={
                "A": "只看系统推荐的同类信息",
                "B": "广泛阅读不同观点",
                "C": "随机浏览新闻",
                "D": "参加线下讨论",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "definition_judgement"

    def test_administrative_license(self):
        """行政许可是指...下列属于 → definition_judgement."""
        result = tool_route_xingce_question(
            "行政许可是指行政机关根据公民、法人或者其他组织的申请，经依法审查，准予其从事特定活动的行为。下列属于行政许可的是？",
            options={
                "A": "颁发营业执照",
                "B": "行政机关内部开会",
                "C": "发布天气预报",
                "D": "企业自行招聘",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "definition_judgement"


class TestRouteCoverageRegressionSafety:
    """v0.4.3: Verify v0.4.2 behaviors don't regress."""

    def test_data_material_still_data_analysis(self):
        """表中材料题 → data_analysis (不退化)."""
        result = tool_route_xingce_question(
            "表中2018—2022年工业增加值平均每年增长量约为多少亿元？",
            options={"A": "120", "B": "180", "C": "240", "D": "300"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"

    def test_quantity_still_quantity(self):
        """普通水池题 → quantity_relation (不退化)."""
        result = tool_route_xingce_question(
            "一个水池甲管注满需8小时，乙管注满需12小时，两管同时开几小时注满？",
            options={"A": "4.8", "B": "5", "C": "6", "D": "10"},
            strict_mode=True,
        )
        assert result["module_guess"] == "quantity_relation"

    def test_no_answer_field_in_route_coverage_result(self):
        """No answer/selected_option/prediction in compose result."""
        result = tool_compose_xingce_answer_prompt(
            "所谓机会成本，是指为了得到某种东西而放弃的其他选择中价值最高者。下列体现机会成本的是？",
            options={
                "A": "某人看电影放弃了加班收入",
                "B": "某人买东西花了100元",
                "C": "某人存钱获得利息",
                "D": "某人获得奖金",
            },
            strict_mode=True,
            allow_answer=True,
        )
        assert "answer" not in result
        assert "selected_option" not in result
        assert "prediction" not in result


# ── v0.5.0 module context override tests ─────────────────────────────

class TestModuleContextOverrideV050:
    """v0.5.0: module_hint / section_context override tests."""

    # ── 1. module_hint=类比推理 → analogy_reasoning ──────────────────

    def test_analogy_hint_short_word_group(self):
        """module_hint=类比推理 能把短词组类比题 route 到 analogy_reasoning."""
        result = tool_route_xingce_question(
            "石头∶雕刻∶雕塑",
            options={"A": "泥土∶烧制∶陶器", "B": "树木∶砍伐∶森林", "C": "种子∶浇水∶植物", "D": "布料∶裁剪∶衣服"},
            strict_mode=True,
            module_hint="类比推理",
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["module_hint_applied"] is True
        assert result["module_hint_conflict"] is False
        assert result["confidence"] == "high"

    def test_analogy_hint_chinese_name(self):
        """section_context='判断推理-类比推理' 也能归一化。"""
        result = tool_route_xingce_question(
            "卫冕∶夺冠",
            options={"A": "加班∶加薪", "B": "卫冕∶蝉联", "C": "比赛∶训练", "D": "夺冠∶失败"},
            strict_mode=True,
            section_context="判断推理-类比推理",
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["module_hint_applied"] is True

    # ── 2. module_hint=言语理解 + 构图/图像 → verbal_reasoning ────────

    def test_verbal_hint_with_graphic_words(self):
        """module_hint=言语理解 时 '构图/图像' 不应触发 graphic_reasoning。"""
        result = tool_route_xingce_question(
            "这段文字通过分析艺术作品的构图方式，说明审美经验受到文化传统影响。对这段文字概括最准确的是：",
            options={"A": "审美经验受文化传统影响", "B": "构图方式决定艺术价值", "C": "艺术作品没有固定标准", "D": "文化传统阻碍审美"},
            strict_mode=True,
            module_hint="言语理解",
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["module_hint_applied"] is True

    def test_verbal_hint_answer_prompt_no_visual_block(self):
        """module_hint=言语理解 时 answer 不应被 missing_visual_content 阻断。"""
        result = tool_compose_xingce_answer_prompt(
            "这段文字通过分析艺术作品的构图方式，说明审美经验受到文化传统影响。对这段文字概括最准确的是：",
            options={"A": "审美经验受文化传统影响", "B": "构图方式决定艺术价值", "C": "艺术作品没有固定标准", "D": "文化传统阻碍审美"},
            strict_mode=True,
            allow_answer=True,
            module_hint="言语理解",
        )
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None

    # ── 3. module_hint=数量关系 + 占比/比例 → quantity_relation ────────

    def test_quantity_hint_with_data_words(self):
        """module_hint=数量关系 时 '占比/比例' 不应触发 data_analysis。"""
        result = tool_route_xingce_question(
            "某班男生人数占全班人数的40%，后来转入5名男生后男生占比变为50%，问原来全班有多少人？",
            options={"A": "20", "B": "25", "C": "30", "D": "35"},
            strict_mode=True,
            module_hint="数量关系",
        )
        assert result["module_guess"] == "quantity_relation"
        assert result["module_hint_applied"] is True

    def test_quantity_hint_answer_prompt_no_material_block(self):
        """module_hint=数量关系 时 answer 不应被 missing_table_or_material 阻断。"""
        result = tool_compose_xingce_answer_prompt(
            "某班男生人数占全班人数的40%，后来转入5名男生后男生占比变为50%，问原来全班有多少人？",
            options={"A": "20", "B": "25", "C": "30", "D": "35"},
            strict_mode=True,
            allow_answer=True,
            module_hint="数量关系",
        )
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None

    # ── 4. module_hint=资料分析 缺材料 → missing_table_or_material ───

    def test_data_hint_requires_material(self):
        """module_hint=资料分析 缺材料时 answer_allowed=false。"""
        result = tool_compose_xingce_answer_prompt(
            "2022年A市常住人口比上年增加了多少万人？",
            options={"A": "12", "B": "18", "C": "24", "D": "30"},
            strict_mode=True,
            allow_answer=True,
            module_hint="资料分析",
            material_present=False,
            table_present=False,
            material_text="",
        )
        assert result["route"]["module_guess"] == "data_analysis"
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"

    # ── 5. module_hint=图形推理 缺图 → missing_visual_content ────────

    def test_graphic_hint_requires_image(self):
        """module_hint=图形推理 缺图时 answer_allowed=false。"""
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
            allow_answer=True,
            module_hint="图形推理",
            image_present=False,
            visual_description="",
        )
        assert result["route"]["module_guess"] == "graphic_reasoning"
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_visual_content"

    # ── 6. 强材料信号不能被错误 module_hint 放松 ────────────────────

    def test_strong_material_signal_overrides_hint(self):
        """'表中' 强材料信号优先于 module_hint=数量关系。"""
        result = tool_compose_xingce_answer_prompt(
            "表中2018—2022年工业增加值平均每年增长量约为多少亿元？",
            options={"A": "120", "B": "180", "C": "240", "D": "300"},
            strict_mode=True,
            allow_answer=True,
            module_hint="数量关系",
            material_present=False,
            table_present=False,
            material_text="",
        )
        # Strong material signal should force data_analysis
        assert result["route"]["module_guess"] == "data_analysis"
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"

    def test_strong_material_signal_route(self):
        """'根据表格' 强材料信号优先于 module_hint。"""
        result = tool_route_xingce_question(
            "根据表格，2020年GDP同比增长了多少？",
            options={"A": "5%", "B": "6%", "C": "7%", "D": "8%"},
            strict_mode=True,
            module_hint="数量关系",
        )
        assert result["module_guess"] == "data_analysis"
        assert result["module_hint_applied"] is False
        assert result["module_hint_conflict"] is True

    # ── 7. module_hint conflict 字段返回 ────────────────────────────

    def test_hint_conflict_fields(self):
        """module_hint 冲突时返回 heuristic_module_guess / module_hint_conflict / warnings。"""
        result = tool_route_xingce_question(
            "这段文字主要介绍构图方式对艺术的影响。",
            options={"A": "构图很重要", "B": "艺术需要构图", "C": "审美受文化影响", "D": "构图决定价值"},
            strict_mode=True,
            module_hint="言语理解",
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["module_hint_applied"] is True
        assert "heuristic_module_guess" in result
        assert "module_hint_conflict" in result

    def test_hint_no_conflict_when_matching(self):
        """module_hint 与 heuristic 一致时无冲突。"""
        result = tool_route_xingce_question(
            "感想∶主观性∶体会",
            options={"A": "规律∶客观性∶发现", "B": "示范性∶形象∶展示"},
            strict_mode=True,
            module_hint="类比推理",
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["module_hint_applied"] is True
        assert result["module_hint_conflict"] is False

    # ── 8. 无 module_hint 时 v0.4.3 行为不退化 ────────────────────

    def test_no_hint_text_arrangement(self):
        """四本书从左到右摆放 → logic_analysis (不退化)."""
        result = tool_route_xingce_question(
            "四本书从左到右摆放，语文书在数学书左边，英语书在最右边。下列哪项可能为真？",
            options={"A": "语文书在最左边", "B": "数学书在最右边", "C": "英语书在中间", "D": "数学书在最左边"},
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"
        assert result["module_hint_applied"] is False

    def test_no_hint_definition_judgement(self):
        """所谓机会成本...下列体现 → definition_judgement (不退化)."""
        result = tool_route_xingce_question(
            "所谓机会成本，是指为了得到某种东西而放弃的其他选择中价值最高者。下列体现机会成本的是？",
            options={
                "A": "某人看电影放弃了加班收入",
                "B": "某人买东西花了100元",
                "C": "某人存钱获得利息",
                "D": "某人获得奖金",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "definition_judgement"
        assert result["module_hint_applied"] is False

    def test_no_hint_data_material(self):
        """表中...平均每年增长量 → data_analysis (不退化)."""
        result = tool_route_xingce_question(
            "表中2018—2022年工业增加值平均每年增长量约为多少亿元？",
            options={"A": "120", "B": "180", "C": "240", "D": "300"},
            strict_mode=True,
        )
        assert result["module_guess"] == "data_analysis"
        assert result["module_hint_applied"] is False

    def test_no_hint_graphic_reasoning(self):
        """左边给定纸盒展开图 → graphic_reasoning (不退化)."""
        result = tool_route_xingce_question(
            "左边给定的是纸盒的展开图，下列哪一项能由它折叠而成？",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
        )
        assert result["module_guess"] == "graphic_reasoning"
        assert result["module_hint_applied"] is False

    def test_no_hint_quantity_relation(self):
        """水池题 → quantity_relation (不退化)."""
        result = tool_route_xingce_question(
            "一个水池甲管注满需8小时，乙管注满需12小时，两管同时开几小时注满？",
            options={"A": "4.8", "B": "5", "C": "6", "D": "10"},
            strict_mode=True,
        )
        assert result["module_guess"] == "quantity_relation"
        assert result["module_hint_applied"] is False

    def test_no_hint_route_uncertain(self):
        """条件不足 → route_uncertain (不退化)."""
        result = tool_route_xingce_question(
            "条件不足",
            strict_mode=True,
        )
        assert result["recommended_track"] == "route_uncertain"
        assert result["module_hint_applied"] is False

    # ── 9. compose answer prompt 无 answer/selected_option/prediction ──

    def test_no_answer_field_in_compose_result(self):
        """compose_xingce_answer_prompt 顶层仍无 answer / selected_option / prediction。"""
        result = tool_compose_xingce_answer_prompt(
            "石头∶雕刻∶雕塑",
            options={"A": "泥土∶烧制∶陶器", "B": "树木∶砍伐∶森林", "C": "种子∶浇水∶植物", "D": "布料∶裁剪∶衣服"},
            strict_mode=True,
            allow_answer=True,
            module_hint="类比推理",
        )
        assert "answer" not in result
        assert "selected_option" not in result
        assert "prediction" not in result

    # ── section_context variants ────────────────────────────────────

    def test_section_context_chinese_full(self):
        """section_context='言语理解与表达' 归一化到 verbal_reasoning。"""
        result = tool_route_xingce_question(
            "这段文字意在说明什么？",
            options={"A": "观点A", "B": "观点B", "C": "观点C", "D": "观点D"},
            strict_mode=True,
            section_context="言语理解与表达",
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["module_hint_applied"] is True

    def test_section_context_english(self):
        """section_context='data_analysis' 直接归一化。"""
        result = tool_route_xingce_question(
            "某市去年GDP为5000亿元，今年增长了8%。",
            options={"A": "5200", "B": "5400", "C": "5600", "D": "5800"},
            strict_mode=True,
            section_context="data_analysis",
        )
        assert result["module_guess"] == "data_analysis"
        assert result["module_hint_applied"] is True

    def test_section_context_with_prefix(self):
        """section_context='第四部分 资料分析' 能提取尾部归一化。"""
        result = tool_route_xingce_question(
            "2022年某市GDP为多少？",
            options={"A": "1000", "B": "2000", "C": "3000", "D": "4000"},
            strict_mode=True,
            section_context="第四部分 资料分析",
        )
        assert result["module_guess"] == "data_analysis"
        assert result["module_hint_applied"] is True

    # ── v0.5.0 route fields present ────────────────────────────────

    def test_route_has_v050_fields(self):
        """route 结果包含 v0.5.0 字段。"""
        result = tool_route_xingce_question(
            "测试题目",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
            module_hint="言语理解",
        )
        assert "module_hint" in result
        assert "section_context" in result
        assert "module_hint_applied" in result
        assert "module_hint_conflict" in result
        assert "heuristic_module_guess" in result

    def test_compose_route_has_v050_fields(self):
        """compose route 子字典包含 v0.5.0 字段。"""
        result = tool_compose_xingce_analysis_prompt(
            "测试题目",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
            module_hint="言语理解",
        )
        route = result["route"]
        assert "module_hint" in route
        assert "section_context" in route
        assert "module_hint_applied" in route
        assert "module_hint_conflict" in route
        assert "heuristic_module_guess" in route

    def test_answer_route_has_v050_fields(self):
        """answer prompt route 子字典包含 v0.5.0 字段。"""
        result = tool_compose_xingce_answer_prompt(
            "测试题目",
            options={"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
            strict_mode=True,
            allow_answer=True,
            module_hint="言语理解",
        )
        route = result["route"]
        assert "module_hint" in route
        assert "section_context" in route
        assert "module_hint_applied" in route
        assert "module_hint_conflict" in route
        assert "heuristic_module_guess" in route


class TestModuleContextEdgeCasesV051:
    """v0.5.1: module_hint overrides insufficient phrase; plain '图' not data_analysis."""

    # ── Fix 1: module_hint overrides insufficient_phrase_detected ──────

    def test_module_hint_overrides_insufficient_phrase_verbal(self):
        result = tool_route_xingce_question(
            "作者接下来最可能论述的是：",
            options={
                "A": "问题产生的原因",
                "B": "具体解决措施",
                "C": "相关历史背景",
                "D": "不同观点比较",
            },
            strict_mode=True,
            module_hint="言语理解",
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["module_hint_applied"] is True
        assert result["module_guess"] != "unknown"
        assert result["recommended_track"] != "route_uncertain"

    def test_module_hint_overrides_insufficient_phrase_answer_prompt(self):
        result = tool_compose_xingce_answer_prompt(
            "作者接下来最可能论述的是：",
            options={
                "A": "问题产生的原因",
                "B": "具体解决措施",
                "C": "相关历史背景",
                "D": "不同观点比较",
            },
            strict_mode=True,
            allow_answer=True,
            module_hint="言语理解",
        )
        assert result["route"]["module_guess"] == "verbal_reasoning"
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None

    def test_no_hint_still_route_uncertain_on_insufficient_phrase(self):
        result = tool_route_xingce_question(
            "条件不足",
            strict_mode=True,
        )
        assert result["module_guess"] == "unknown"
        assert result["recommended_track"] == "route_uncertain"
        assert "insufficient_phrase_detected" in result["reasoning_signals"]

    # ── Fix 2: plain graph words don't trigger data_analysis gate ──────

    def test_definition_hint_with_relationship_graph_not_data_analysis(self):
        result = tool_route_xingce_question(
            "人际关系图是指用节点和连线表示个体之间关系的一种图示方法。下列属于人际关系图的是：",
            options={
                "A": "用点表示人员、用线表示朋友关系的图",
                "B": "某地区年度GDP统计表",
                "C": "某产品销售额折线图",
                "D": "某班考试成绩柱状图",
            },
            strict_mode=True,
            module_hint="定义判断",
        )
        assert result["module_guess"] == "definition_judgement"
        assert result["module_hint_applied"] is True
        assert result["module_guess"] != "data_analysis"

    def test_definition_hint_with_relationship_graph_allows_answer(self):
        result = tool_compose_xingce_answer_prompt(
            "人际关系图是指用节点和连线表示个体之间关系的一种图示方法。下列属于人际关系图的是：",
            options={
                "A": "用点表示人员、用线表示朋友关系的图",
                "B": "某地区年度GDP统计表",
                "C": "某产品销售额折线图",
                "D": "某班考试成绩柱状图",
            },
            strict_mode=True,
            allow_answer=True,
            module_hint="定义判断",
        )
        assert result["route"]["module_guess"] == "definition_judgement"
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None

    def test_plain_graph_words_do_not_trigger_data_material_gate(self):
        result = tool_compose_xingce_answer_prompt(
            "下图是一种关系图示，用于说明概念之间的包含关系。下列符合上述定义的是：",
            options={
                "A": "用圆圈表示概念范围",
                "B": "用表格统计产量",
                "C": "用折线展示增长率",
                "D": "用柱状图比较销量",
            },
            strict_mode=True,
            allow_answer=True,
            module_hint="定义判断",
        )
        assert result["route"]["module_guess"] == "definition_judgement"
        assert result["answer_allowed"] is True
        assert result["answer_block_reason"] is None
        assert result["context_requirements"]["requires_table_or_material"] is False

    # ── Strong material signals still work ─────────────────────────────

    def test_chart_data_still_triggers_material_gate(self):
        result = tool_compose_xingce_answer_prompt(
            "图中数据显示，第三季度销售额占全年销售额的比重约为多少？",
            options={
                "A": "18%",
                "B": "24%",
                "C": "31%",
                "D": "39%",
            },
            strict_mode=True,
            allow_answer=True,
            module_hint="数量关系",
            material_present=False,
            table_present=False,
            material_text="",
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"
        assert result["context_requirements"]["requires_table_or_material"] is True

    def test_table_signal_still_overrides_wrong_quantity_hint(self):
        result = tool_compose_xingce_answer_prompt(
            "表中2018—2022年工业增加值平均每年增长量约为多少亿元？",
            options={"A": "120", "B": "180", "C": "240", "D": "300"},
            strict_mode=True,
            allow_answer=True,
            module_hint="数量关系",
            material_present=False,
            table_present=False,
            material_text="",
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"

    # ── v0.5.0 regression (no退化) ────────────────────────────────────

    def test_analogy_hint_no_regression(self):
        result = tool_route_xingce_question(
            "石头∶雕刻∶雕塑",
            options={
                "A": "泥土∶烧制∶陶器",
                "B": "树木∶砍伐∶森林",
                "C": "种子∶浇水∶植物",
                "D": "布料∶裁剪∶衣服",
            },
            strict_mode=True,
            module_hint="类比推理",
        )
        assert result["module_guess"] == "analogy_reasoning"
        assert result["module_hint_applied"] is True

    def test_verbal_hint_with_graphic_words_no_regression(self):
        result = tool_route_xingce_question(
            "这段文字通过分析艺术作品的构图方式，说明审美经验受到文化传统影响。对这段文字概括最准确的是：",
            options={
                "A": "审美经验受文化传统影响",
                "B": "构图方式决定艺术价值",
                "C": "艺术作品没有固定标准",
                "D": "文化传统阻碍审美",
            },
            strict_mode=True,
            module_hint="言语理解",
        )
        assert result["module_guess"] == "verbal_reasoning"
        assert result["module_hint_applied"] is True

    def test_quantity_hint_with_data_words_no_regression(self):
        result = tool_route_xingce_question(
            "某班男生人数占全班人数的40%，后来转入5名男生后男生占比变为50%，问原来全班有多少人？",
            options={"A": "20", "B": "25", "C": "30", "D": "35"},
            strict_mode=True,
            module_hint="数量关系",
        )
        assert result["module_guess"] == "quantity_relation"
        assert result["module_hint_applied"] is True

    def test_data_hint_requires_material_no_regression(self):
        result = tool_compose_xingce_answer_prompt(
            "2022年A市常住人口比上年增加了多少万人？",
            options={"A": "12", "B": "18", "C": "24", "D": "30"},
            strict_mode=True,
            allow_answer=True,
            module_hint="资料分析",
            material_present=False,
            table_present=False,
            material_text="",
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_table_or_material"

    def test_graphic_hint_requires_image_no_regression(self):
        result = tool_compose_xingce_answer_prompt(
            "从所给四个选项中，选择最合适的一个，使之呈现一定规律。",
            options={"A": "图形A", "B": "图形B", "C": "图形C", "D": "图形D"},
            strict_mode=True,
            allow_answer=True,
            module_hint="图形推理",
            image_present=False,
            visual_description="",
        )
        assert result["answer_allowed"] is False
        assert result["answer_block_reason"] == "missing_visual_content"

    def test_no_hint_v043_text_arrangement_no_regression(self):
        result = tool_route_xingce_question(
            "四本书从左到右摆放，语文书不在最左边，数学书在英语书左边，以下哪项可能为真？",
            options={
                "A": "语文书在最右边",
                "B": "数学书在最左边",
                "C": "英语书在最右边",
                "D": "数学书在最右边",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "logic_analysis"

    def test_no_hint_v043_definition_judgement_no_regression(self):
        result = tool_route_xingce_question(
            "所谓机会成本，是指为了得到某种东西而放弃的其他选择中价值最高者。下列体现机会成本的是？",
            options={
                "A": "小张花100元买了一张电影票",
                "B": "小李放弃了高薪工作选择创业",
                "C": "小王存钱买了新车",
                "D": "小赵用奖金买了礼物",
            },
            strict_mode=True,
        )
        assert result["module_guess"] == "definition_judgement"

    # ── Security: no answer/selected_option/prediction leak ────────────

    def test_no_answer_field_in_v051_edge_case_results(self):
        for result in [
            tool_route_xingce_question(
                "作者接下来最可能论述的是：",
                options={"A": "原因", "B": "措施", "C": "背景", "D": "比较"},
                strict_mode=True,
                module_hint="言语理解",
            ),
            tool_route_xingce_question(
                "人际关系图是指用节点和连线表示个体之间关系的一种图示方法。下列属于人际关系图的是：",
                options={"A": "关系图", "B": "统计表", "C": "折线图", "D": "柱状图"},
                strict_mode=True,
                module_hint="定义判断",
            ),
        ]:
            assert "answer" not in result, f"answer leaked in {result}"
            assert "selected_option" not in result
            assert "prediction" not in result
