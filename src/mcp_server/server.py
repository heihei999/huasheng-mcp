import json
import logging
import asyncio
from typing import Any, Dict
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

from .config import Config
from .registry import ToolRegistry
from .tools import get_all_tools
from .bridge import XingceBridge
from .transport import SSETransportManager
from .runtime_adapter import XingceRuntimeAdapter

# Import the existing runtime module without modifying it
from xingce_solver import mcp_server as xingce_runtime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Xingce MCP SSE Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
registry = ToolRegistry()
for tool in get_all_tools():
    registry.register(tool)

adapter = XingceRuntimeAdapter(xingce_runtime)
bridge = XingceBridge(mcp_runtime=adapter)
transport = SSETransportManager()

@app.get("/.well-known/mcp.json")
async def mcp_manifest():
    """
    MCP capability manifest endpoint.
    """
    return {
        "server": {
            "name": "xingce-mcp",
            "version": "1.0.0"
        },
        "capabilities": {
            "tools": True
        },
        "transport": "SSE",
        "tools": registry.list_tools()
    }

@app.get(Config.SSE_ENDPOINT)
async def sse_endpoint(request: Request):
    """
    Standard MCP SSE connection endpoint.
    """
    session_id = transport.create_session()
    
    # Standard MCP requires sending an 'endpoint' event with the URI to POST messages
    # We will use /message as the standard POST endpoint
    base_url = str(request.base_url).rstrip("/")
    endpoint_uri = f"{base_url}/message?session_id={session_id}"
    
    # We must send this asynchronously to the queue
    async def send_initial():
        # First send the tools/list manifest event as required
        await transport.send_event(session_id, "tools/list", registry.list_tools())
        # Then send the endpoint event
        await transport.send_event(session_id, "endpoint", endpoint_uri)
    
    asyncio.create_task(send_initial())
    
    return EventSourceResponse(transport.event_generator(session_id))

@app.post("/message")
async def mcp_message_handler(request: Request, session_id: str):
    """
    Standard MCP JSON-RPC message handler.
    """
    try:
        msg = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # We process JSON-RPC and send the response back via SSE
    if "method" not in msg:
        return JSONResponse(status_code=400, content={"error": "Missing method"})

    method = msg["method"]
    msg_id = msg.get("id")

    async def process_and_respond():
        response: Dict[str, Any] = {"jsonrpc": "2.0", "id": msg_id}
        
        try:
            if method == "initialize":
                response["result"] = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "xingce-mcp-sse", "version": "1.0.0"}
                }
            elif method == "notifications/initialized":
                return # No response needed
            elif method == "tools/list":
                response["result"] = {
                    "tools": registry.list_tools()
                }
            elif method == "tools/call":
                params = msg.get("params", {})
                tool_name = params.get("name")
                args = params.get("arguments", {})
                
                # Use bridge to dispatch
                result = bridge.call(tool_name, args)
                
                # Format standard MCP tool call result
                # Typically MCP tools return a list of content objects
                result_text = json.dumps(result, ensure_ascii=False) if not isinstance(result, str) else result
                response["result"] = {
                    "content": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ],
                    "isError": False
                }
            else:
                response["error"] = {"code": -32601, "message": f"Method not found: {method}"}
                
        except Exception as e:
            logger.error(f"Error processing {method}: {e}", exc_info=True)
            response["error"] = {"code": -32000, "message": str(e)}

        if msg_id is not None:
            await transport.send_event(session_id, "message", response)

    # Process in background or await directly? Standard MCP clients expect HTTP 202
    asyncio.create_task(process_and_respond())
    return JSONResponse(status_code=202, content="Accepted")


# --- Standard REST API Endpoints for OpenWebUI ---
@app.post("/api/route_xingce_question")
async def api_route(request: Request):
    data = await request.json()
    return bridge.call("route_xingce_question", data)

@app.post("/api/compose_xingce_analysis_prompt")
async def api_compose_analysis(request: Request):
    data = await request.json()
    return bridge.call("compose_xingce_analysis_prompt", data)

@app.post("/api/compose_xingce_answer_prompt")
async def api_compose_answer(request: Request):
    data = await request.json()
    return bridge.call("compose_xingce_answer_prompt", data)

# --- Universal REST API Endpoint for all Tools ---
@app.post("/api/execute_tool")
async def api_execute_tool(request: Request):
    data = await request.json()
    tool_name = data.get("name")
    args = data.get("args", {})
    from xingce_solver import mcp_server as xingce_mcp
    func = getattr(xingce_mcp, tool_name, None)
    if func:
        return func(**args)
    return {"error": "tool not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
