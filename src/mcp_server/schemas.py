from typing import Any, Dict

def get_route_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question text to route."
            }
        },
        "required": ["question"]
    }

def get_compose_analysis_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "route": {
                "type": "string",
                "description": "The route result or module guess."
            },
            "question": {
                "type": "string",
                "description": "The question text."
            }
        },
        "required": ["route", "question"]
    }

def get_compose_answer_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "analysis": {
                "type": "string",
                "description": "The analysis content."
            }
        },
        "required": ["analysis"]
    }

def get_empty_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {},
        "required": []
    }

def get_method_card_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "method_id": {
                "type": "string",
                "description": "The ID of the method card to retrieve."
            },
            "kb_dir": {
                "type": "string",
                "description": "Optional custom knowledge base directory."
            }
        },
        "required": ["method_id"]
    }

def get_search_methods_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query."
            },
            "module": {
                "type": "string",
                "description": "Optional module to filter by."
            },
            "top_k": {
                "type": "integer",
                "description": "Number of top results to return."
            },
            "kb_dir": {
                "type": "string",
                "description": "Optional knowledge base directory."
            }
        },
        "required": ["query"]
    }

def get_classify_question_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "question_text": {
                "type": "string",
                "description": "The question text to classify."
            },
            "top_k": {
                "type": "integer",
                "description": "Number of top results to return."
            },
            "kb_dir": {
                "type": "string",
                "description": "Optional knowledge base directory."
            }
        },
        "required": ["question_text"]
    }

def get_solve_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "question_text": {
                "type": "string",
                "description": "The question text to solve."
            },
            "options": {
                "type": "object",
                "description": "Optional dictionary mapping option letters to their text.",
                "additionalProperties": {"type": "string"}
            },
            "kb_dir": {
                "type": "string",
                "description": "Optional custom knowledge base directory."
            }
        },
        "required": ["question_text"]
    }

def get_source_reference_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "method_id": {
                "type": "string",
                "description": "The method ID."
            },
            "kb_dir": {
                "type": "string",
                "description": "Optional custom knowledge base directory."
            }
        },
        "required": ["method_id"]
    }
