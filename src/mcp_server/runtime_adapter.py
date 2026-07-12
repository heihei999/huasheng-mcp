from typing import Any

class XingceRuntimeAdapter:
    """
    Adapts the internal xingce_solver.mcp_server functions to the specific
    tool interfaces expected by the SSE server.
    """
    def __init__(self, raw_module: Any):
        self.raw = raw_module

    # --- Original 3 Tools (Strict mapping) ---
    def route_xingce_question(self, question: str):
        return self.raw.tool_route_xingce_question(question_text=question)

    def compose_analysis_prompt(self, route: str, question: str):
        return self.raw.tool_compose_xingce_analysis_prompt(
            module_hint=route,
            question_text=question
        )

    def compose_answer_prompt(self, analysis: str):
        return self.raw.tool_compose_xingce_answer_prompt(
            question_text=analysis
        )
        
    # --- New 12 Tools (Direct mapping) ---
    def get_analogy_reasoning_scaffold(self):
        return self.raw.tool_get_analogy_reasoning_scaffold()

    def get_definition_judgement_scaffold(self):
        return self.raw.tool_get_definition_judgement_scaffold()

    def get_graphic_reasoning_scaffold(self):
        return self.raw.tool_get_graphic_reasoning_scaffold()

    def get_logic_analysis_scaffold(self):
        return self.raw.tool_get_logic_analysis_scaffold()

    def get_quantity_relation_scaffold(self):
        return self.raw.tool_get_quantity_relation_scaffold()

    def get_verbal_reasoning_scaffold(self):
        return self.raw.tool_get_verbal_reasoning_scaffold()

    def get_method_card(self, method_id: str, kb_dir: str = None):
        return self.raw.tool_get_method_card(method_id=method_id, kb_dir=kb_dir)

    def get_source_reference(self, method_id: str, kb_dir: str = None):
        return self.raw.tool_get_source_reference(method_id=method_id, kb_dir=kb_dir)

    def search_methods(self, query: str, module: str = None, top_k: int = 5, kb_dir: str = None):
        return self.raw.tool_search_methods(query=query, module=module, top_k=top_k, kb_dir=kb_dir)

    def classify_question(self, question_text: str, top_k: int = 5, kb_dir: str = None):
        return self.raw.tool_classify_question(question_text=question_text, top_k=top_k, kb_dir=kb_dir)

    def solve_data_analysis(self, question_text: str, options: dict = None, kb_dir: str = None):
        return self.raw.tool_solve_data_analysis(question_text=question_text, options=options, kb_dir=kb_dir)

    def solve_logic_reasoning(self, question_text: str, options: dict = None, kb_dir: str = None):
        return self.raw.tool_solve_logic_reasoning(question_text=question_text, options=options, kb_dir=kb_dir)
