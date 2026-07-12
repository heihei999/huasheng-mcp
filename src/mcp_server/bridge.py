from typing import Any, Dict

class XingceBridge:
    def __init__(self, mcp_runtime: Any):
        self.mcp = mcp_runtime

    def call(self, tool_name: str, args: Dict[str, Any]) -> Any:
        # Alias mapping for backwards compatibility with REST endpoints
        alias_map = {
            "compose_xingce_analysis_prompt": "compose_analysis_prompt",
            "compose_xingce_answer_prompt": "compose_answer_prompt"
        }
        actual_tool_name = alias_map.get(tool_name, tool_name)
        
        method = getattr(self.mcp, actual_tool_name, None)
        if not method:
            # Maybe it does not have tool_ prefix
            method = getattr(self.mcp, f"tool_{actual_tool_name}", None)
            
        if not method:
            raise ValueError(f"Unknown tool: {tool_name} (mapped to {actual_tool_name})")
        
        return method(**args)
