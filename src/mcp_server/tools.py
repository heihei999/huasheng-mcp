from typing import List
from .registry import ToolMeta
from .schemas import (
    get_route_schema,
    get_compose_analysis_schema,
    get_compose_answer_schema,
    get_empty_schema,
    get_method_card_schema,
    get_search_methods_schema,
    get_classify_question_schema,
    get_solve_schema,
    get_source_reference_schema
)

def get_all_tools() -> List[ToolMeta]:
    return [
        # Original 3 tools with strict schemas
        ToolMeta(
            name="route_xingce_question",
            description="Route a question to the recommended module or scaffold without solving.",
            inputSchema=get_route_schema()
        ),
        ToolMeta(
            name="compose_analysis_prompt",
            description="Compose a structured analysis prompt without solving.",
            inputSchema=get_compose_analysis_schema()
        ),
        ToolMeta(
            name="compose_answer_prompt",
            description="Compose a conservative answer prompt for LLM-in-the-loop answering.",
            inputSchema=get_compose_answer_schema()
        ),
        
        # New 12 tools explicitly mapped
        ToolMeta(
            name="get_analogy_reasoning_scaffold",
            description="Return the read-only method scaffold for analogy reasoning.",
            inputSchema=get_empty_schema()
        ),
        ToolMeta(
            name="get_definition_judgement_scaffold",
            description="Return the read-only method scaffold for definition judgement.",
            inputSchema=get_empty_schema()
        ),
        ToolMeta(
            name="get_graphic_reasoning_scaffold",
            description="Return the read-only method scaffold for graphic reasoning.",
            inputSchema=get_empty_schema()
        ),
        ToolMeta(
            name="get_logic_analysis_scaffold",
            description="Return the read-only method scaffold for logic analysis reasoning.",
            inputSchema=get_empty_schema()
        ),
        ToolMeta(
            name="get_quantity_relation_scaffold",
            description="Return the read-only method scaffold for quantity relation reasoning.",
            inputSchema=get_empty_schema()
        ),
        ToolMeta(
            name="get_verbal_reasoning_scaffold",
            description="Return the read-only method scaffold for verbal reasoning.",
            inputSchema=get_empty_schema()
        ),
        ToolMeta(
            name="get_method_card",
            description="Get the detailed card for a specific reasoning method.",
            inputSchema=get_method_card_schema()
        ),
        ToolMeta(
            name="get_source_reference",
            description="Get the source reference for a specific reasoning method.",
            inputSchema=get_source_reference_schema()
        ),
        ToolMeta(
            name="search_methods",
            description="Search for reasoning methods based on a query.",
            inputSchema=get_search_methods_schema()
        ),
        ToolMeta(
            name="classify_question",
            description="Classify a question to predict its module and priority method.",
            inputSchema=get_classify_question_schema()
        ),
        ToolMeta(
            name="solve_data_analysis",
            description="Solve a data analysis question.",
            inputSchema=get_solve_schema()
        ),
        ToolMeta(
            name="solve_logic_reasoning",
            description="Solve a logic reasoning question.",
            inputSchema=get_solve_schema()
        )
    ]
