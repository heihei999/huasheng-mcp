import json
import uuid
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional

from sse_starlette.sse import ServerSentEvent

class SSETransportManager:
    def __init__(self):
        self.sessions: Dict[str, asyncio.Queue] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = asyncio.Queue()
        return session_id

    def remove_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    async def send_event(self, session_id: str, event: str, data: Any):
        if session_id in self.sessions:
            queue = self.sessions[session_id]
            
            # format data as string if it's not
            if not isinstance(data, str):
                data = json.dumps(data)
                
            await queue.put(ServerSentEvent(event=event, data=data))

    async def event_generator(self, session_id: str) -> AsyncGenerator[ServerSentEvent, None]:
        queue = self.sessions.get(session_id)
        if not queue:
            return
            
        try:
            while True:
                try:
                    # Wait for an event with a timeout
                    event = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield event
                except asyncio.TimeoutError:
                    # Send a keep-alive ping (SSE comment) to prevent connection drop
                    yield ServerSentEvent(event="ping", data="")
        except asyncio.CancelledError:
            self.remove_session(session_id)
            raise
