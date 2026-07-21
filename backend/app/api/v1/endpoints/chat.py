from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.agents.orchestrator import agent_orchestrator

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    use_rag: bool = True
    enable_agents: bool = True

@router.post("/completions")
async def chat_completions(payload: ChatCompletionRequest):
    if not payload.messages:
        raise HTTPException(status_code=400, detail="Messages array cannot be empty.")
    
    last_user_message = payload.messages[-1].content
    result = await agent_orchestrator.execute_task(last_user_message)
    return result
