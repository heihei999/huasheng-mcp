"""Phase-1 retrieval utilities for the Xingce solver."""

from .kb import (
    KnowledgeBase,
    get_method_card,
    get_source_reference,
    load_cards,
    search_method_matches,
    search_methods,
)
from .router import classify_question
from .solvers import solve_data_analysis, solve_logic_reasoning

__all__ = [
    "KnowledgeBase",
    "classify_question",
    "get_method_card",
    "get_source_reference",
    "load_cards",
    "search_method_matches",
    "search_methods",
    "solve_data_analysis",
    "solve_logic_reasoning",
]

__version__ = "0.1.0"
