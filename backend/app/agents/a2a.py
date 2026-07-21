import asyncio
import time
from typing import Dict, Any, List

class A2AMessageBus:
    """
    Agent-to-Agent (A2A) IPC Router.
    Facilitates asynchronous task delegation, state sync, and multi-agent coordination.
    """
    def __init__(self):
        self._execution_history: List[Dict[str, Any]] = []

    async def send_message(
        self, 
        sender: str, 
        recipient: str, 
        message_type: str, 
        payload: Dict[str, Any],
        trace_id: str
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        event_frame = {
            "trace_id": trace_id,
            "sender": sender,
            "recipient": recipient,
            "message_type": message_type,
            "payload": payload,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        self._execution_history.append(event_frame)
        
        # Simulate asynchronous microsecond A2A bus transmission
        await asyncio.sleep(0.01)
        
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        
        return {
            "status": "DELIVERED",
            "latency_ms": elapsed_ms,
            "frame": event_frame
        }

    def get_trace_history(self, trace_id: str) -> List[Dict[str, Any]]:
        return [item for item in self._execution_history if item["trace_id"] == trace_id]

a2a_bus = A2AMessageBus()
