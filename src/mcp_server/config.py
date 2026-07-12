import os

class Config:
    HOST: str = os.getenv("MCP_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("MCP_PORT", "8000"))
    SSE_ENDPOINT: str = "/sse"
    TOOL_CALL_ENDPOINT: str = "/tool/call"
