from typing import List, Dict, Any

class ToolMeta:
    def __init__(self, name: str, description: str, inputSchema: Dict[str, Any]):
        self.name = name
        self.description = description
        self.inputSchema = inputSchema

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolMeta] = {}

    def register(self, tool: ToolMeta):
        self.tools[tool.name] = tool

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": t.inputSchema
            }
            for t in self.tools.values()
        ]
