"""Tests for the graphic reasoning method scaffold."""

from __future__ import annotations

import inspect

from xingce_solver.scaffolds.graphic_reasoning_scaffold import (
    build_graphic_reasoning_scaffold,
    get_anti_pattern_guards,
    get_black_white_operation_rules,
    get_dot_grid_coordinate_protocol,
    get_falsification_protocol,
    get_graphic_reasoning_stage_order,
    get_graphic_reasoning_visual_checklists,
    get_nine_grid_fallback_protocol,
    get_spatial_verification_protocol,
    get_specialized_templates,
    get_uncertainty_reporting_protocol,
    get_visual_transcription_protocol,
    render_graphic_reasoning_prompt_template,
)


# ---------------------------------------------------------------------------
# Basic structure
# ---------------------------------------------------------------------------


class TestBasicStructure:
    """Test basic scaffold structure."""

    def test_returns_dict(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert isinstance(scaffold, dict)

    def test_module_field(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert scaffold["module"] == "graphic_reasoning"

    def test_version_field(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert scaffold["version"] == "v0.2.2"

    def test_mode_field(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert scaffold["mode"] == "method_scaffold_only"


# ---------------------------------------------------------------------------
# Stage order
# ---------------------------------------------------------------------------


class TestStageOrder:
    """Test ten-layer observation order."""

    def test_stage_order_length(self) -> None:
        order = get_graphic_reasoning_stage_order()
        assert len(order) == 10

    def test_stage_order_content_and_sequence(self) -> None:
        order = get_graphic_reasoning_stage_order()
        expected = [
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
        assert order == expected


# ---------------------------------------------------------------------------
# Composition router
# ---------------------------------------------------------------------------


class TestCompositionRouter:
    """Test composition-based routing."""

    def test_has_four_routes(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        router = scaffold["composition_router"]
        assert "组成相同" in router
        assert "组成相似" in router
        assert "组成不同" in router
        assert "特殊图形" in router

    def test_same_composition_has_position_patterns(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        patterns = scaffold["composition_router"]["组成相同"]["patterns"]
        assert "平移" in patterns
        assert "旋转" in patterns
        assert "翻转" in patterns

    def test_similar_composition_has_style_patterns(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        patterns = scaffold["composition_router"]["组成相似"]["patterns"]
        assert "遍历" in patterns
        assert "加减同异" in patterns
        assert "黑白运算" in patterns

    def test_different_composition_has_quantity_patterns(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        patterns = scaffold["composition_router"]["组成不同"]["patterns"]
        assert "点" in patterns
        assert "线" in patterns
        assert "面" in patterns
        assert "角" in patterns
        assert "素" in patterns

    def test_special_graphics_has_spatial_patterns(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        patterns = scaffold["composition_router"]["特殊图形"]["patterns"]
        assert "六面体展开图" in patterns
        assert "截面图" in patterns
        assert "三视图" in patterns
        assert "立体拼合" in patterns


# ---------------------------------------------------------------------------
# Visual checklists
# ---------------------------------------------------------------------------


class TestVisualChecklists:
    """Test visual checklists."""

    def test_has_required_keys(self) -> None:
        checklists = get_graphic_reasoning_visual_checklists()
        required = [
            "数字类", "字母类", "功能元素", "黑白块",
            "六面体展开图", "截面图", "三视图", "立体拼合",
        ]
        for key in required:
            assert key in checklists, f"Missing checklist key: {key}"

    def test_digit_classifications(self) -> None:
        checklists = get_graphic_reasoning_visual_checklists()
        digits = checklists["数字类"]["classifications"]
        # Axisymmetric digits
        for d in ["0", "3", "6", "8", "9"]:
            assert d in digits["常见轴对称数字"]
        # All-curve digits
        for d in ["0", "3", "6", "8", "9"]:
            assert d in digits["全曲数字"]
        # All-straight digits
        for d in ["1", "4", "7"]:
            assert d in digits["全直数字"]

    def test_letter_classifications(self) -> None:
        checklists = get_graphic_reasoning_visual_checklists()
        letters = checklists["字母类"]["classifications"]
        # Axisymmetric letters
        for c in "ABCDEHIKMOTUVWXY":
            assert c in letters["轴对称字母"], f"{c} missing from axisymmetric"
        # Center-symmetric letters
        for c in "NSZ":
            assert c in letters["中心对称字母"]

    def test_functional_elements(self) -> None:
        checklists = get_graphic_reasoning_visual_checklists()
        fe = checklists["功能元素"]
        assert "交点" in fe["标记点"]
        assert "端点" in fe["标记点"]
        assert "最大面" in fe["标记面"]
        assert "最小角" in fe["标记角"]

    def test_black_white_blocks(self) -> None:
        checklists = get_graphic_reasoning_visual_checklists()
        bw = checklists["黑白块"]
        assert "同位置运算" in bw["checks"]
        assert any("不能预设固定运算规则" in c for c in bw["constraints"])

    def test_cube_net(self) -> None:
        checklists = get_graphic_reasoning_visual_checklists()
        cube = checklists["六面体展开图"]
        assert "1-4-1" in cube["net_types"]
        assert "2-3-1" in cube["net_types"]
        assert "2-2-2" in cube["net_types"]
        assert "0-3-3" in cube["net_types"]
        assert any("时针" in c for c in cube["checks"])


# ---------------------------------------------------------------------------
# Uncertainty policy
# ---------------------------------------------------------------------------


class TestUncertaintyPolicy:
    """Test uncertainty policy."""

    def test_has_analysis_only(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        policy = scaffold["uncertainty_policy"]
        assert any("analysis_only" in v for v in policy.values())

    def test_has_fold_ambiguous(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        policy = scaffold["uncertainty_policy"]
        assert "fold_ambiguous" in policy

    def test_has_bw_table_uncertain(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        policy = scaffold["uncertainty_policy"]
        assert "bw_table_uncertain" in policy


# ---------------------------------------------------------------------------
# Response template
# ---------------------------------------------------------------------------


class TestResponseTemplate:
    """Test response template."""

    def test_has_required_sections(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        required_markers = [
            "【命题形式】",
            "【组成判断】",
            "【视觉转写】",
            "【选项逐项验证】",
            "【唯一性判断】",
        ]
        for marker in required_markers:
            assert marker in template, f"Missing marker: {marker}"
        assert "analysis_only" in template

    def test_v02_new_sections_present(self) -> None:
        """v0.2 template must include MCP route, visual transcription, etc."""
        template = render_graphic_reasoning_prompt_template()
        v02_markers = [
            "【MCP 路由结果】",
            "【是否有图检查】",
            "【视觉转写】",
            "【专项模板选择】",
            "【选项逐项验证】",
        ]
        for marker in v02_markers:
            assert marker in template, f"Missing v0.2 marker: {marker}"

    def test_template_mentions_abcd(self) -> None:
        """Template must mention A/B/C/D for per-option verification."""
        template = render_graphic_reasoning_prompt_template()
        assert "A/B/C/D" in template

    def test_template_mentions_analysis_only(self) -> None:
        """Template must mention analysis_only."""
        template = render_graphic_reasoning_prompt_template()
        assert "analysis_only" in template

    def test_template_mentions_7_specialized_templates(self) -> None:
        """Template must list all 7 specialized template options."""
        template = render_graphic_reasoning_prompt_template()
        assert "grid_black_shape" in template
        assert "complex_black_white_pattern" in template
        assert "line_symbol_pattern" in template
        assert "three_views" in template
        assert "cube_net" in template
        assert "solid_assembly" in template
        assert "grouping_classification" in template


# ---------------------------------------------------------------------------
# Specialized templates (v0.2)
# ---------------------------------------------------------------------------


class TestSpecializedTemplates:
    """Test the 7 specialized forced-verification templates."""

    def test_returns_dict(self) -> None:
        templates = get_specialized_templates()
        assert isinstance(templates, dict)

    def test_has_all_7_templates(self) -> None:
        templates = get_specialized_templates()
        expected_keys = [
            "grid_black_shape",
            "complex_black_white_pattern",
            "line_symbol_pattern",
            "three_views",
            "cube_net",
            "solid_assembly",
            "grouping_classification",
        ]
        for key in expected_keys:
            assert key in templates, f"Missing specialized template: {key}"
        assert len(templates) == 7

    def test_scaffold_contains_specialized_templates(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "specialized_templates" in scaffold
        assert isinstance(scaffold["specialized_templates"], dict)
        assert len(scaffold["specialized_templates"]) == 7

    # -- Template A: grid_black_shape --

    def test_grid_black_shape_has_mandatory_recording(self) -> None:
        templates = get_specialized_templates()
        t = templates["grid_black_shape"]
        assert "mandatory_recording" in t
        rec = t["mandatory_recording"]
        assert any("覆盖行列" in r for r in rec)
        assert any("顶点" in r for r in rec)
        assert any("斜边方向" in r for r in rec)
        assert any("覆盖格数量" in r for r in rec)
        assert any("平移" in r and "旋转" in r for r in rec)
        assert any("A/B/C/D" in r for r in rec)

    def test_grid_black_shape_constraint(self) -> None:
        templates = get_specialized_templates()
        t = templates["grid_black_shape"]
        assert "constraint" in t
        assert "朝向像旋转" in t["constraint"]

    # -- Template B: complex_black_white_pattern --

    def test_complex_bw_has_decomposition(self) -> None:
        templates = get_specialized_templates()
        t = templates["complex_black_white_pattern"]
        assert "mandatory_decomposition" in t
        dec = t["mandatory_decomposition"]
        assert any("固定部件" in d for d in dec)
        assert any("移动部件" in d for d in dec)
        assert any("黑色区域" in d for d in dec)
        assert any("白色缺口" in d for d in dec)

    def test_complex_bw_constraint(self) -> None:
        templates = get_specialized_templates()
        t = templates["complex_black_white_pattern"]
        assert "constraint" in t
        assert "整体旋转" in t["constraint"]

    # -- Template C: line_symbol_pattern --

    def test_line_symbol_has_checks(self) -> None:
        templates = get_specialized_templates()
        t = templates["line_symbol_pattern"]
        assert "mandatory_checks" in t
        checks = t["mandatory_checks"]
        assert "线段数" in checks
        assert "端点数" in checks
        assert "交点数" in checks
        assert "封闭区域数" in checks
        assert "平行线" in checks
        assert "垂直线" in checks
        assert "开闭性" in checks
        assert "曲直性" in checks

    def test_line_symbol_constraint(self) -> None:
        templates = get_specialized_templates()
        t = templates["line_symbol_pattern"]
        assert "constraint" in t
        assert "开放/封闭" in t["constraint"]

    # -- Template D: three_views --

    def test_three_views_has_coordinate_requirement(self) -> None:
        templates = get_specialized_templates()
        t = templates["three_views"]
        assert "mandatory_procedure" in t
        proc = t["mandatory_procedure"]
        assert any("坐标" in p or "格子表" in p for p in proc)
        assert any("俯视图" in p for p in proc)
        assert any("左视图" in p for p in proc)
        assert any("高度" in p for p in proc)

    def test_three_views_has_verification_steps(self) -> None:
        templates = get_specialized_templates()
        t = templates["three_views"]
        assert "verification_steps" in t
        steps_text = " ".join(t["verification_steps"])
        assert "坐标" in steps_text
        assert "高度" in steps_text
        assert "俯视图" in steps_text
        assert "左视图" in steps_text
        assert "正视图" in steps_text

    def test_three_views_constraint(self) -> None:
        templates = get_specialized_templates()
        t = templates["three_views"]
        assert "constraint" in t
        assert "坐标" in t["constraint"] or "格子表" in t["constraint"]

    # -- Template E: cube_net --

    def test_cube_net_has_face_procedures(self) -> None:
        templates = get_specialized_templates()
        t = templates["cube_net"]
        assert "mandatory_procedure" in t
        proc = t["mandatory_procedure"]
        assert any("相邻面" in p for p in proc)
        assert any("相对面" in p for p in proc)
        assert any("公共边" in p for p in proc)
        assert any("公共点" in p for p in proc)
        assert any("图案方向" in p for p in proc)

    def test_cube_net_has_verification_steps(self) -> None:
        templates = get_specialized_templates()
        t = templates["cube_net"]
        assert "verification_steps" in t
        steps_text = " ".join(t["verification_steps"])
        assert "相邻面" in steps_text
        assert "相对面" in steps_text
        assert "公共边" in steps_text
        assert "公共点" in steps_text
        assert "图案方向" in steps_text

    def test_cube_net_constraint(self) -> None:
        templates = get_specialized_templates()
        t = templates["cube_net"]
        assert "constraint" in t
        assert "公共边" in t["constraint"]
        assert "公共点" in t["constraint"]

    # -- Template F: solid_assembly --

    def test_solid_assembly_has_count_procedures(self) -> None:
        templates = get_specialized_templates()
        t = templates["solid_assembly"]
        assert "mandatory_procedure" in t
        proc = t["mandatory_procedure"]
        assert any("方块总数" in p for p in proc)
        assert any("颜色" in p for p in proc)
        assert any("层数" in p for p in proc)
        assert any("重叠" in p for p in proc)

    def test_solid_assembly_has_verification_steps(self) -> None:
        templates = get_specialized_templates()
        t = templates["solid_assembly"]
        assert "verification_steps" in t
        steps_text = " ".join(t["verification_steps"])
        assert "方块总数" in steps_text
        assert "颜色" in steps_text
        assert "重叠" in steps_text

    def test_solid_assembly_constraint(self) -> None:
        templates = get_specialized_templates()
        t = templates["solid_assembly"]
        assert "constraint" in t
        assert "数量矛盾" in t["constraint"]

    def test_solid_assembly_has_residual_check(self) -> None:
        templates = get_specialized_templates()
        t = templates["solid_assembly"]
        assert "residual_check" in t
        rc = t["residual_check"]
        assert "description" in rc
        assert "required_calculations" in rc
        assert "constraints" in rc
        assert "keywords" in rc

    def test_solid_assembly_residual_check_keywords(self) -> None:
        templates = get_specialized_templates()
        rc = templates["solid_assembly"]["residual_check"]
        keywords = rc["keywords"]
        assert "残差" in keywords
        assert "目标总块数" in keywords
        assert "颜色数" in keywords
        assert "已知组件" in keywords
        assert "待选组件" in keywords
        assert "全白" in keywords
        assert "数量守恒" in keywords
        assert "凹凸互补" in keywords
        assert "重叠" in keywords
        assert "颜色错位" in keywords

    def test_solid_assembly_residual_check_calculations(self) -> None:
        templates = get_specialized_templates()
        rc = templates["solid_assembly"]["residual_check"]
        calcs = rc["required_calculations"]
        assert any("目标总块数" in c for c in calcs)
        assert any("目标颜色块" in c for c in calcs)
        assert any("已知组件" in c for c in calcs)
        assert any("remaining_total_blocks" in c for c in calcs)
        assert any("remaining_color_blocks" in c for c in calcs)
        assert any("remaining_white_blocks" in c for c in calcs)

    def test_solid_assembly_residual_check_constraints(self) -> None:
        templates = get_specialized_templates()
        rc = templates["solid_assembly"]["residual_check"]
        constraints = rc["constraints"]
        assert any("全白" in c for c in constraints)
        assert any("不得默认" in c for c in constraints)
        assert any("analysis_only" in c for c in constraints)

    # -- Template G: grouping_classification --

    def test_grouping_has_dimension_requirement(self) -> None:
        templates = get_specialized_templates()
        t = templates["grouping_classification"]
        assert "mandatory_procedure" in t
        proc = t["mandatory_procedure"]
        assert any("3 个候选分类维度" in p or "至少" in p for p in proc)
        assert any("选项反推验证" in p or "A/B/C/D" in p for p in proc)

    def test_grouping_has_candidate_dimensions(self) -> None:
        templates = get_specialized_templates()
        t = templates["grouping_classification"]
        assert "candidate_dimensions" in t
        dims = t["candidate_dimensions"]
        assert len(dims) >= 11  # at least 11 candidate dimensions
        assert "对称性" in dims
        assert "曲直性" in dims
        assert "开闭性" in dims
        assert "封闭区域数" in dims

    def test_grouping_has_verification_steps(self) -> None:
        templates = get_specialized_templates()
        t = templates["grouping_classification"]
        assert "verification_steps" in t
        steps_text = " ".join(t["verification_steps"])
        assert "候选维度" in steps_text or "维度" in steps_text
        assert "选项" in steps_text or "反推" in steps_text

    def test_grouping_constraint(self) -> None:
        templates = get_specialized_templates()
        t = templates["grouping_classification"]
        assert "constraint" in t
        assert "3 个候选维度" in t["constraint"] or "候选维度" in t["constraint"]

    def test_grouping_has_forced_dimensions_by_type(self) -> None:
        templates = get_specialized_templates()
        t = templates["grouping_classification"]
        assert "forced_dimensions_by_type" in t
        fdt = t["forced_dimensions_by_type"]
        assert "line_polygon" in fdt
        assert "black_white_block" in fdt

    def test_grouping_forced_line_polygon_dimensions(self) -> None:
        templates = get_specialized_templates()
        lp = templates["grouping_classification"]["forced_dimensions_by_type"]["line_polygon"]
        assert "description" in lp
        assert "dimensions" in lp
        assert "precision_requirement" in lp
        dims = lp["dimensions"]
        assert any("封闭区域" in d or "面数" in d for d in dims)
        assert any("部分数" in d for d in dims)
        assert any("一笔画" in d or "奇点" in d for d in dims)
        assert any("端点" in d for d in dims)
        assert any("交点" in d for d in dims)
        assert any("平行线" in d for d in dims)
        assert any("直角" in d for d in dims)
        assert any("最大面" in d for d in dims)
        assert any("构件" in d for d in dims)

    def test_grouping_forced_bw_block_dimensions(self) -> None:
        templates = get_specialized_templates()
        bw = templates["grouping_classification"]["forced_dimensions_by_type"]["black_white_block"]
        assert "description" in bw
        assert "dimensions" in bw
        dims = bw["dimensions"]
        assert any("面积占比" in d for d in dims)
        assert any("重心" in d for d in dims)
        assert any("最大黑色区域" in d for d in dims)
        assert any("接边" in d for d in dims)
        assert any("接角" in d for d in dims)
        assert any("对称" in d for d in dims)
        assert any("部分数" in d for d in dims)
        assert any("外框" in d for d in dims)

    def test_grouping_precision_requirement(self) -> None:
        templates = get_specialized_templates()
        lp = templates["grouping_classification"]["forced_dimensions_by_type"]["line_polygon"]
        assert "封闭区域" in lp["precision_requirement"]
        assert "图1=3面" in lp["precision_requirement"]
        assert "禁止" in lp["precision_requirement"]
        assert "较多/较少" in lp["precision_requirement"]


# ---------------------------------------------------------------------------
# Visual transcription protocol (v0.2)
# ---------------------------------------------------------------------------


class TestVisualTranscriptionProtocol:
    """Test the mandatory visual transcription protocol."""

    def test_returns_dict(self) -> None:
        protocol = get_visual_transcription_protocol()
        assert isinstance(protocol, dict)

    def test_scaffold_contains_protocol(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "visual_transcription_protocol" in scaffold
        assert isinstance(scaffold["visual_transcription_protocol"], dict)

    def test_mandatory_flag(self) -> None:
        protocol = get_visual_transcription_protocol()
        assert protocol["mandatory"] is True

    def test_has_required_fields(self) -> None:
        protocol = get_visual_transcription_protocol()
        fields = protocol["required_fields"]
        assert "proposition_form" in fields
        assert "image_present" in fields
        assert "figure_count" in fields
        assert "option_count" in fields
        assert "given_figures_visual_facts" in fields
        assert "options_visual_facts" in fields
        assert "uncertain_visual_details" in fields

    def test_has_field_descriptions(self) -> None:
        protocol = get_visual_transcription_protocol()
        desc = protocol["field_descriptions"]
        assert "proposition_form" in desc
        assert "image_present" in desc
        assert "given_figures_visual_facts" in desc
        assert "options_visual_facts" in desc

    def test_fallback_rule(self) -> None:
        protocol = get_visual_transcription_protocol()
        assert "fallback_rule" in protocol
        assert "analysis_only" in protocol["fallback_rule"]


# ---------------------------------------------------------------------------
# Anti-pattern guards (v0.2)
# ---------------------------------------------------------------------------


class TestAntiPatternGuards:
    """Test anti-pattern guards."""

    def test_returns_list(self) -> None:
        guards = get_anti_pattern_guards()
        assert isinstance(guards, list)

    def test_scaffold_contains_guards(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "anti_pattern_guards" in scaffold
        assert isinstance(scaffold["anti_pattern_guards"], list)

    def test_minimum_8_guards(self) -> None:
        guards = get_anti_pattern_guards()
        assert len(guards) >= 13

    def test_each_guard_has_id_forbidden_required(self) -> None:
        guards = get_anti_pattern_guards()
        for guard in guards:
            assert "id" in guard, f"Guard missing 'id': {guard}"
            assert "forbidden" in guard, f"Guard missing 'forbidden': {guard}"
            assert "required" in guard, f"Guard missing 'required': {guard}"

    def test_guard_no_first_glance(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "no_first_glance" in ids

    def test_guard_no_single_candidate(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "no_single_candidate" in ids

    def test_guard_grouping_needs_dimensions(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "grouping_needs_dimensions" in ids

    def test_guard_spatial_needs_verification(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        # Check for the spatial guard (name may contain Chinese chars)
        spatial_found = any("spatial" in gid for gid in ids)
        assert spatial_found, f"Missing spatial guard, got ids: {ids}"

    def test_guard_bw_needs_component_split(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "bw_needs_component_split" in ids

    def test_guard_grid_needs_position转写(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        grid_found = any("grid" in gid for gid in ids)
        assert grid_found, f"Missing grid guard, got ids: {ids}"

    def test_guard_unified_rule_required(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "unified_rule_required" in ids

    def test_guard_unique_option_required(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "unique_option_required" in ids

    def test_guard_no_intuitive_cross_section_rejection(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "no_intuitive_cross_section_rejection" in ids

    def test_guard_no_color_count_assumption(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "no_color_count_assumption" in ids

    def test_guard_no_fuzzy_face_count(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "no_fuzzy_face_count" in ids

    def test_guard_no_single_dimension_grouping(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "no_single_dimension_grouping" in ids

    def test_guard_no_failed_rule_persistence(self) -> None:
        guards = get_anti_pattern_guards()
        ids = [g["id"] for g in guards]
        assert "no_failed_rule_persistence" in ids


# ---------------------------------------------------------------------------
# Forbidden dependencies
# ---------------------------------------------------------------------------


class TestNoForbiddenDependencies:
    """Test that no forbidden libraries are imported."""

    def test_no_forbidden_imports(self) -> None:
        """Check that no forbidden libraries are imported (not just mentioned in text)."""
        mod = __import__(
            "xingce_solver.scaffolds.graphic_reasoning_scaffold",
            fromlist=["graphic_reasoning_scaffold"],
        )
        # Check actual module-level imports, not string content
        module_dict = vars(mod)
        forbidden_modules = [
            "cv2", "PIL", "Pillow", "pytesseract",
            "sklearn", "torch", "tensorflow", "statsmodels",
            "xgboost", "lightgbm", "requests", "openai", "anthropic",
        ]
        for lib in forbidden_modules:
            assert lib not in module_dict, f"Found forbidden import: {lib}"
            # Also check sys.modules wasn't loaded by this module
        # Check import statements in source (lines starting with import/from)
        source = inspect.getsource(mod)
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                for lib in forbidden_modules:
                    assert lib not in stripped, f"Found forbidden import statement: {stripped}"


# ---------------------------------------------------------------------------
# No solver behavior
# ---------------------------------------------------------------------------


class TestNoSolverBehavior:
    """Test that scaffold does not behave as a solver."""

    def test_no_answer_field(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "answer" not in scaffold
        assert "selected_option" not in scaffold
        assert "prediction" not in scaffold


# ---------------------------------------------------------------------------
# No hardcoded answer sequences
# ---------------------------------------------------------------------------


class TestNoHardcodedAnswers:
    """Test that no hardcoded answer sequences exist in code or templates."""

    def test_no_hardcoded_answer_sequence_in_scaffold(self) -> None:
        """Must not contain hardcoded answer sequences like 'A D D C B B D B B C'."""
        scaffold = build_graphic_reasoning_scaffold()
        scaffold_str = str(scaffold)
        # Check for common hardcoded answer patterns
        forbidden_patterns = [
            "A D D C", "B B D B", "D B B C",
            "ADD C", "BD B", "ADB C",
            "答案是A", "答案是B", "答案是C", "答案是D",
            "D A C B D", "B A C C D", "D A C B D B A C C D",
        ]
        for pattern in forbidden_patterns:
            assert pattern not in scaffold_str, f"Found hardcoded pattern: {pattern}"

    def test_no_hardcoded_answer_sequence_in_template(self) -> None:
        """Template must not contain hardcoded answer sequences."""
        template = render_graphic_reasoning_prompt_template()
        forbidden_patterns = [
            "A D D C", "B B D B", "D B B C",
            "答案是A", "答案是B", "答案是C", "答案是D",
            "D A C B D", "B A C C D", "D A C B D B A C C D",
        ]
        for pattern in forbidden_patterns:
            assert pattern not in template, f"Found hardcoded pattern in template: {pattern}"


# ---------------------------------------------------------------------------
# Black-white operation rules (v0.2.1)
# ---------------------------------------------------------------------------


class TestBlackWhiteOperationRules:
    """Test the black-white overlay operation rules."""

    def test_returns_dict(self) -> None:
        rules = get_black_white_operation_rules()
        assert isinstance(rules, dict)

    def test_scaffold_contains_rules(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "black_white_operation_rules" in scaffold
        assert isinstance(scaffold["black_white_operation_rules"], dict)

    def test_has_all_8_operation_types(self) -> None:
        rules = get_black_white_operation_rules()
        ops = rules["operation_types"]
        expected = [
            "direct_overlay",
            "xor_remove_same_keep_different",
            "keep_same_remove_different",
            "black_intersection",
            "white_intersection",
            "color_inversion",
            "line_overlay",
            "line_xor",
        ]
        for key in expected:
            assert key in ops, f"Missing operation type: {key}"
        assert len(ops) == 8

    def test_each_operation_has_name_rule_description(self) -> None:
        rules = get_black_white_operation_rules()
        for op_id, op in rules["operation_types"].items():
            assert "name" in op, f"{op_id} missing 'name'"
            assert "rule" in op, f"{op_id} missing 'rule'"
            assert "description" in op, f"{op_id} missing 'description'"

    def test_mandatory_process(self) -> None:
        rules = get_black_white_operation_rules()
        assert "mandatory_process" in rules
        proc = rules["mandatory_process"]
        assert any("同一行或同一列" in p for p in proc)
        assert any("逐格代入" in p for p in proc)
        assert any("完整推出" in p for p in proc)
        assert any("不允许只说" in p for p in proc)

    def test_constraint(self) -> None:
        rules = get_black_white_operation_rules()
        assert "constraint" in rules
        assert "逐格代入" in rules["constraint"]

    def test_direct_overlay_rule(self) -> None:
        rules = get_black_white_operation_rules()
        op = rules["operation_types"]["direct_overlay"]
        assert "黑+黑=黑" in op["rule"]

    def test_xor_rule(self) -> None:
        rules = get_black_white_operation_rules()
        op = rules["operation_types"]["xor_remove_same_keep_different"]
        assert "黑+黑=白" in op["rule"]


# ---------------------------------------------------------------------------
# Falsification protocol (v0.2.1)
# ---------------------------------------------------------------------------


class TestFalsificationProtocol:
    """Test the falsification protocol."""

    def test_returns_dict(self) -> None:
        protocol = get_falsification_protocol()
        assert isinstance(protocol, dict)

    def test_scaffold_contains_protocol(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "falsification_protocol" in scaffold
        assert isinstance(scaffold["falsification_protocol"], dict)

    def test_mandatory_flag(self) -> None:
        protocol = get_falsification_protocol()
        assert protocol["mandatory"] is True

    def test_has_5_steps(self) -> None:
        protocol = get_falsification_protocol()
        assert len(protocol["steps"]) == 5

    def test_step_ids(self) -> None:
        protocol = get_falsification_protocol()
        ids = [s["id"] for s in protocol["steps"]]
        assert "unified_check" in ids
        assert "option_elimination" in ids
        assert "competing_rule" in ids
        assert "conflict_check" in ids
        assert "uniqueness_check" in ids

    def test_unified_check_requires_all_figures(self) -> None:
        protocol = get_falsification_protocol()
        step = next(s for s in protocol["steps"] if s["id"] == "unified_check")
        assert "所有已知图" in step["requirement"]

    def test_option_elimination_requires_abcd(self) -> None:
        protocol = get_falsification_protocol()
        step = next(s for s in protocol["steps"] if s["id"] == "option_elimination")
        assert "A/B/C/D" in step["requirement"]

    def test_competing_rule_required(self) -> None:
        protocol = get_falsification_protocol()
        step = next(s for s in protocol["steps"] if s["id"] == "competing_rule")
        assert "竞争规律" in step["requirement"]

    def test_conflict_check(self) -> None:
        protocol = get_falsification_protocol()
        step = next(s for s in protocol["steps"] if s["id"] == "conflict_check")
        assert "竞争规律" in step["requirement"]
        assert "冲突" in step["requirement"]

    def test_uniqueness_check_requires_analysis_only(self) -> None:
        protocol = get_falsification_protocol()
        step = next(s for s in protocol["steps"] if s["id"] == "uniqueness_check")
        assert "analysis_only" in step["requirement"]

    def test_forbidden_field(self) -> None:
        protocol = get_falsification_protocol()
        assert "forbidden" in protocol
        assert "不允许" in protocol["forbidden"]

    def test_output_fields(self) -> None:
        protocol = get_falsification_protocol()
        assert "output_fields" in protocol
        fields = protocol["output_fields"]
        assert "current_rule_explains_all" in fields
        assert "competing_rule_tried" in fields
        assert "competing_rule_prediction" in fields
        assert "conflict_explanation" in fields


# ---------------------------------------------------------------------------
# Spatial verification protocol (v0.2.1)
# ---------------------------------------------------------------------------


class TestSpatialVerificationProtocol:
    """Test the spatial verification protocol."""

    def test_returns_dict(self) -> None:
        protocol = get_spatial_verification_protocol()
        assert isinstance(protocol, dict)

    def test_scaffold_contains_protocol(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "spatial_verification_protocol" in scaffold
        assert isinstance(scaffold["spatial_verification_protocol"], dict)

    def test_mandatory_flag(self) -> None:
        protocol = get_spatial_verification_protocol()
        assert protocol["mandatory"] is True

    def test_has_three_types(self) -> None:
        protocol = get_spatial_verification_protocol()
        assert "three_views" in protocol
        assert "cube_net" in protocol
        assert "solid_assembly" in protocol

    def test_has_four_types_including_cross_section(self) -> None:
        protocol = get_spatial_verification_protocol()
        assert "cross_section" in protocol

    # -- three_views --

    def test_three_views_has_coordinate_requirement(self) -> None:
        protocol = get_spatial_verification_protocol()
        tv = protocol["three_views"]
        assert "required_steps" in tv
        steps = tv["required_steps"]
        assert any("坐标" in s or "格子表" in s for s in steps)
        assert any("俯视图" in s for s in steps)
        assert any("左视图" in s for s in steps)
        assert any("正视图" in s for s in steps)

    def test_three_views_has_height_matrix(self) -> None:
        protocol = get_spatial_verification_protocol()
        tv = protocol["three_views"]
        assert "required_output" in tv
        output = tv["required_output"]
        assert any("高度" in o for o in output)
        assert any("颜色" in o for o in output)
        assert any("遮挡" in o for o in output)

    # -- cube_net --

    def test_cube_net_has_face_requirements(self) -> None:
        protocol = get_spatial_verification_protocol()
        cn = protocol["cube_net"]
        assert "required_steps" in cn
        steps = cn["required_steps"]
        assert any("相邻面" in s for s in steps)
        assert any("相对面" in s for s in steps)
        assert any("公共边" in s for s in steps)
        assert any("公共点" in s for s in steps)
        assert any("图案方向" in s for s in steps)

    def test_cube_net_has_required_output(self) -> None:
        protocol = get_spatial_verification_protocol()
        cn = protocol["cube_net"]
        assert "required_output" in cn
        output = cn["required_output"]
        assert any("相邻面" in o for o in output)
        assert any("相对面" in o for o in output)
        assert any("公共边" in o for o in output)
        assert any("公共点" in o for o in output)
        assert any("图案方向" in o for o in output)

    # -- solid_assembly --

    def test_solid_assembly_has_count_requirements(self) -> None:
        protocol = get_spatial_verification_protocol()
        sa = protocol["solid_assembly"]
        assert "required_steps" in sa
        steps = sa["required_steps"]
        assert any("方块总数" in s for s in steps)
        assert any("颜色" in s for s in steps)
        assert any("层数" in s for s in steps)
        assert any("凹凸" in s for s in steps)
        assert any("重叠" in s for s in steps)

    def test_solid_assembly_has_required_output(self) -> None:
        protocol = get_spatial_verification_protocol()
        sa = protocol["solid_assembly"]
        assert "required_output" in sa
        output = sa["required_output"]
        assert any("方块总数" in o for o in output)
        assert any("颜色数" in o for o in output)
        assert any("层数" in o for o in output)
        assert any("凹凸" in o for o in output)
        assert any("重叠" in o for o in output)
        assert any("数量矛盾" in o for o in output)

    def test_solid_assembly_constraint(self) -> None:
        protocol = get_spatial_verification_protocol()
        sa = protocol["solid_assembly"]
        assert "constraint" in sa
        assert "数量矛盾" in sa["constraint"]
        assert "不得硬解释" in sa["constraint"]

    # -- cross_section --

    def test_cross_section_has_required_steps(self) -> None:
        protocol = get_spatial_verification_protocol()
        cs = protocol["cross_section"]
        assert "required_steps" in cs
        steps = cs["required_steps"]
        assert any("切面" in s for s in steps)
        assert any("平行" in s and "侧面" in s for s in steps)
        assert any("平行" in s and "底面" in s for s in steps)
        assert any("三点" in s for s in steps)

    def test_cross_section_has_required_output(self) -> None:
        protocol = get_spatial_verification_protocol()
        cs = protocol["cross_section"]
        assert "required_output" in cs
        output = cs["required_output"]
        assert any("切面" in o for o in output)
        assert any("平行" in o for o in output)
        assert any("截面" in o for o in output)
        assert any("规则" in o and "图形" in o for o in output)
        assert any("选项" in o and "验证" in o for o in output)

    def test_cross_section_has_geometric_guards(self) -> None:
        protocol = get_spatial_verification_protocol()
        cs = protocol["cross_section"]
        assert "geometric_guards" in cs
        guards = cs["geometric_guards"]
        assert "parallel_to_side" in guards
        assert "parallel_to_base" in guards
        assert "same_height_layer" in guards
        assert "adjacent_face_intersection" in guards
        assert "three_point_plane" in guards
        assert "no_intuitive_rejection" in guards

    def test_cross_section_geometric_guards_content(self) -> None:
        protocol = get_spatial_verification_protocol()
        guards = protocol["cross_section"]["geometric_guards"]
        assert "矩形" in guards["parallel_to_side"]
        assert "底面" in guards["parallel_to_base"]
        assert "直角" in guards["adjacent_face_intersection"]
        assert "三点" in guards["three_point_plane"]
        assert "不得凭视觉直觉" in guards["no_intuitive_rejection"]

    def test_cross_section_constraint(self) -> None:
        protocol = get_spatial_verification_protocol()
        cs = protocol["cross_section"]
        assert "constraint" in cs
        assert "不得凭直觉" in cs["constraint"]
        assert "analysis_only" in cs["constraint"]


# ---------------------------------------------------------------------------
# Uncertainty reporting protocol (v0.2.1)
# ---------------------------------------------------------------------------


class TestUncertaintyReportingProtocol:
    """Test the uncertainty reporting protocol."""

    def test_returns_dict(self) -> None:
        protocol = get_uncertainty_reporting_protocol()
        assert isinstance(protocol, dict)

    def test_scaffold_contains_protocol(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "uncertainty_reporting_protocol" in scaffold
        assert isinstance(scaffold["uncertainty_reporting_protocol"], dict)

    def test_mandatory_flag(self) -> None:
        protocol = get_uncertainty_reporting_protocol()
        assert protocol["mandatory"] is True

    def test_has_required_fields(self) -> None:
        protocol = get_uncertainty_reporting_protocol()
        fields = protocol["required_fields"]
        assert "confidence_level" in fields
        assert "risk_points" in fields
        assert "possible_competing_rule" in fields
        assert "why_other_options_rejected" in fields

    def test_has_field_descriptions(self) -> None:
        protocol = get_uncertainty_reporting_protocol()
        desc = protocol["field_descriptions"]
        assert "confidence_level" in desc
        assert "risk_points" in desc
        assert "possible_competing_rule" in desc
        assert "why_other_options_rejected" in desc

    def test_confidence_levels(self) -> None:
        protocol = get_uncertainty_reporting_protocol()
        desc = protocol["field_descriptions"]["confidence_level"]
        assert "high" in desc
        assert "medium" in desc
        assert "low" in desc

    def test_risk_points_description(self) -> None:
        protocol = get_uncertainty_reporting_protocol()
        desc = protocol["field_descriptions"]["risk_points"]
        assert "不确定" in desc or "风险" in desc

    def test_analysis_only_triggers(self) -> None:
        protocol = get_uncertainty_reporting_protocol()
        assert "analysis_only_triggers" in protocol
        triggers = protocol["analysis_only_triggers"]
        assert any("confidence_level" in t for t in triggers)
        assert any("risk_points" in t for t in triggers)
        assert any("competing_rule" in t for t in triggers)


# ---------------------------------------------------------------------------
# Visual transcription protocol grid requirements (v0.2.1)
# ---------------------------------------------------------------------------


class TestVisualTranscriptionGridRequirements:
    """Test grid-specific requirements in visual transcription protocol."""

    def test_has_grid_specific_requirements(self) -> None:
        protocol = get_visual_transcription_protocol()
        assert "grid_specific_requirements" in protocol

    def test_coordinate_system(self) -> None:
        protocol = get_visual_transcription_protocol()
        grid = protocol["grid_specific_requirements"]
        assert "coordinate_system" in grid
        assert "坐标" in grid["coordinate_system"]

    def test_black_cell_coordinates(self) -> None:
        protocol = get_visual_transcription_protocol()
        grid = protocol["grid_specific_requirements"]
        assert "black_cell_coordinates" in grid
        assert "坐标" in grid["black_cell_coordinates"]

    def test_line_endpoint_coordinates(self) -> None:
        protocol = get_visual_transcription_protocol()
        grid = protocol["grid_specific_requirements"]
        assert "line_endpoint_coordinates" in grid
        assert "端点" in grid["line_endpoint_coordinates"]

    def test_key_vertices(self) -> None:
        protocol = get_visual_transcription_protocol()
        grid = protocol["grid_specific_requirements"]
        assert "key_vertices" in grid
        assert "顶点" in grid["key_vertices"]

    def test_diagonal_direction(self) -> None:
        protocol = get_visual_transcription_protocol()
        grid = protocol["grid_specific_requirements"]
        assert "diagonal_direction" in grid
        assert "斜边" in grid["diagonal_direction"]

    def test_coverage_cells(self) -> None:
        protocol = get_visual_transcription_protocol()
        grid = protocol["grid_specific_requirements"]
        assert "coverage_cells" in grid
        assert "覆盖格" in grid["coverage_cells"]

    def test_options_same_transcription(self) -> None:
        protocol = get_visual_transcription_protocol()
        grid = protocol["grid_specific_requirements"]
        assert "options_same_transcription" in grid
        assert "A/B/C/D" in grid["options_same_transcription"]


# ---------------------------------------------------------------------------
# Prompt template v0.2.1 sections
# ---------------------------------------------------------------------------


class TestResponseTemplateV021:
    """Test v0.2.1 prompt template sections."""

    def test_has_competing_rule_section(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "【候选规律 2 / 竞争规律】" in template

    def test_has_falsification_section(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "【证伪检查】" in template

    def test_has_risk_section(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "【风险点与置信度】" in template

    def test_has_final_answer_section(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "【最终答案或 analysis_only】" in template

    def test_template_mentions_competing_rule(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "竞争规律" in template

    def test_template_mentions_falsification(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "证伪" in template

    def test_template_mentions_analysis_only(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "analysis_only" in template

    def test_template_mentions_confidence_level(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "confidence_level" in template

    def test_template_mentions_risk_points(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "risk_points" in template

    def test_spatial_requires_coordinate核验(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "坐标/面/块的核验过程" in template

    def test_grouping_requires_3_dimensions(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "至少 3 个维度" in template

    def test_overlay_requires_operation代入(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "运算规则代入" in template


# ---------------------------------------------------------------------------
# Dot grid coordinate protocol (v0.2.2)
# ---------------------------------------------------------------------------


class TestDotGridCoordinateProtocol:
    """Test the dot-grid coordinate protocol."""

    def test_returns_dict(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert isinstance(protocol, dict)

    def test_scaffold_contains_protocol(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "dot_grid_coordinate_protocol" in scaffold
        assert isinstance(scaffold["dot_grid_coordinate_protocol"], dict)

    def test_mandatory_flag(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert protocol["mandatory"] is True

    def test_has_applicability(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert "applicability" in protocol
        assert "蜂窝" in protocol["applicability"]
        assert "网格圆圈" in protocol["applicability"]
        assert "九宫格" in protocol["applicability"]

    def test_coordinate_system_required(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert "coordinate_system_required" in protocol
        assert "虚拟坐标系" in protocol["coordinate_system_required"]
        assert "不允许" in protocol["coordinate_system_required"]

    def test_black_point_set_required(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert "black_point_set_required" in protocol
        assert "坐标集合" in protocol["black_point_set_required"]
        assert "集合形式" in protocol["black_point_set_required"]

    def test_option_black_point_set_required(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert "option_black_point_set_required" in protocol
        assert "A/B/C/D" in protocol["option_black_point_set_required"]
        assert "坐标集合" in protocol["option_black_point_set_required"]

    def test_coordinate_set_operations(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert "coordinate_set_operations" in protocol
        ops = protocol["coordinate_set_operations"]
        assert "direct_overlay" in ops
        assert "xor_remove_same_keep_different" in ops
        assert "intersection" in ops
        assert "complement_or_inversion" in ops
        assert "row_or_column_translation" in ops
        assert "rotation_or_reflection" in ops

    def test_movement_trace_check(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert "movement_trace_check" in protocol
        assert "移动轨迹" in protocol["movement_trace_check"]
        assert "统一规律" in protocol["movement_trace_check"]

    def test_symmetry_check(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert "symmetry_check" in protocol
        assert "对称轴" in protocol["symmetry_check"]
        assert "对称中心" in protocol["symmetry_check"]
        assert "坐标集合" in protocol["symmetry_check"]

    def test_fallback_to_analysis_only(self) -> None:
        protocol = get_dot_grid_coordinate_protocol()
        assert "fallback_to_analysis_only" in protocol
        assert "analysis_only" in protocol["fallback_to_analysis_only"]


# ---------------------------------------------------------------------------
# Nine-grid fallback protocol (v0.2.2)
# ---------------------------------------------------------------------------


class TestNineGridFallbackProtocol:
    """Test the nine-grid fallback protocol."""

    def test_returns_dict(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert isinstance(protocol, dict)

    def test_scaffold_contains_protocol(self) -> None:
        scaffold = build_graphic_reasoning_scaffold()
        assert "nine_grid_fallback_protocol" in scaffold
        assert isinstance(scaffold["nine_grid_fallback_protocol"], dict)

    def test_mandatory_flag(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert protocol["mandatory"] is True

    def test_has_applicability(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert "applicability" in protocol
        assert "九宫格" in protocol["applicability"]

    def test_horizontal_first(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert "horizontal_first" in protocol
        assert "横向" in protocol["horizontal_first"]

    def test_vertical_second(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert "vertical_second" in protocol
        assert "纵向" in protocol["vertical_second"]

    def test_failure_detection(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert "failure_detection" in protocol
        assert "任一行" in protocol["failure_detection"] or "一列" in protocol["failure_detection"]
        assert "失效" in protocol["failure_detection"]
        assert "硬套" in protocol["failure_detection"]

    def test_mandatory_switch_targets(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert "mandatory_switch_targets" in protocol
        targets = protocol["mandatory_switch_targets"]
        assert any("轴对称" in t for t in targets)
        assert any("中心对称" in t for t in targets)
        assert any("移动轨迹" in t for t in targets)
        assert any("重心" in t for t in targets)
        assert any("坐标集合映射" in t for t in targets)

    def test_no_failed_rule_persistence(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert "no_failed_rule_persistence" in protocol
        assert "不得" in protocol["no_failed_rule_persistence"]
        assert "硬套" in protocol["no_failed_rule_persistence"]
        assert "对称性" in protocol["no_failed_rule_persistence"]
        assert "移动轨迹" in protocol["no_failed_rule_persistence"]

    def test_competing_rule_output(self) -> None:
        protocol = get_nine_grid_fallback_protocol()
        assert "competing_rule_output" in protocol
        assert "analysis_only" in protocol["competing_rule_output"]


# ---------------------------------------------------------------------------
# Prompt template v0.2.2 sections
# ---------------------------------------------------------------------------


class TestResponseTemplateV022:
    """Test v0.2.2 prompt template sections."""

    def test_dot_grid_coordinate_in_visual_transcription(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "黑点坐标集合" in template

    def test_nine_grid_fallback_in_candidate_rule(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "九宫格" in template
        assert "切换" in template or "对称性" in template

    def test_cross_section_in_verification(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "截面图" in template
        assert "切面" in template or "平行" in template

    def test_residual_check_in_verification(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "残差" in template
        assert "目标块数" in template or "已知组件" in template

    def test_grouping_forced_dimensions_in_verification(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "面数" in template or "部分数" in template
        assert "面积占比" in template or "重心" in template

    def test_analysis_only_for_unclear_visual_facts(self) -> None:
        template = render_graphic_reasoning_prompt_template()
        assert "关键视觉事实不清楚" in template or "分析_only" in template or "analysis_only" in template


# ---------------------------------------------------------------------------
# Cross-section checklist (v0.2.2)
# ---------------------------------------------------------------------------


class TestCrossSectionChecklist:
    """Test the updated cross-section checklist."""

    def test_has_geometric_section_guards(self) -> None:
        checklists = get_graphic_reasoning_visual_checklists()
        cs = checklists["截面图"]
        assert "geometric_section_guards" in cs
        guards = cs["geometric_section_guards"]
        assert len(guards) >= 6
        assert any("平行" in g and "侧面" in g for g in guards)
        assert any("平行" in g and "底面" in g for g in guards)
        assert any("高度层" in g for g in guards)
        assert any("相邻面" in g and "直角" in g for g in guards)
        assert any("三点" in g for g in guards)
        assert any("不得凭" in g and "直觉" in g for g in guards)

    def test_constraint_updated(self) -> None:
        checklists = get_graphic_reasoning_visual_checklists()
        cs = checklists["截面图"]
        assert "constraint" in cs
        assert "不得凭直觉" in cs["constraint"]
        assert "逐一验证" in cs["constraint"]


# ---------------------------------------------------------------------------
# Hardcoded answer sequence check (v0.2.2)
# ---------------------------------------------------------------------------


class TestNoHardcodedAnswersV022:
    """Test that no hardcoded answer sequences exist in new content."""

    def test_no_hardcoded_answers_in_new_protocols(self) -> None:
        """Must not contain the test answer sequence D A C B D B A C C D."""
        scaffold = build_graphic_reasoning_scaffold()
        scaffold_str = str(scaffold)
        forbidden_patterns = [
            "D A C B D", "B A C C D", "D A C B D B A C C D",
            "DACBD", "BACCD", "DACBDBACCD",
        ]
        for pattern in forbidden_patterns:
            assert pattern not in scaffold_str, f"Found hardcoded pattern: {pattern}"

    def test_no_hardcoded_answers_in_template(self) -> None:
        """Template must not contain the test answer sequence."""
        template = render_graphic_reasoning_prompt_template()
        forbidden_patterns = [
            "D A C B D", "B A C C D", "D A C B D B A C C D",
            "DACBD", "BACCD",
        ]
        for pattern in forbidden_patterns:
            assert pattern not in template, f"Found hardcoded pattern in template: {pattern}"
