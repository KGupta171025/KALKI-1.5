from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List
from app.agents.mcp import mcp_registry
from app.agents.a2a import a2a_bus

router = APIRouter()

@router.get("/mcp/tools")
async def list_mcp_tools():
    return {
        "mcp_version": "1.0",
        "registered_tools": mcp_registry.get_tool_definitions()
    }

@router.get("/traces/{trace_id}")
async def get_execution_trace(trace_id: str):
    trace_events = a2a_bus.get_trace_history(trace_id)
    return {
        "trace_id": trace_id,
        "event_count": len(trace_events),
        "events": trace_events
    }
