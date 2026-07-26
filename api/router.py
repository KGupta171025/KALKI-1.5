from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.inference import LLMProviderFactory
from services.task_queue import dispatch_autonomous_agent_task, celery_app

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.2

@router.post("/chat/completions")
async def chat_completions(payload: ChatCompletionRequest):
    if not payload.messages:
        raise HTTPException(status_code=400, detail="Messages array cannot be empty")
    
    # Translate Pydantic schemas to dictionary format for the adapters
    raw_messages = [{"role": msg.role, "content": msg.content} for msg in payload.messages]
    
    try:
        # Dynamically resolve LLM provider at runtime
        llm = LLMProviderFactory.get_provider(
            provider_name=payload.provider,
            model_name=payload.model
        )
        
        # Execute model call
        result = await llm.generate_completion(
            messages=raw_messages,
            temperature=payload.temperature
        )
        return {
            "status": "SUCCESS",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": result["text"]
                    }
                }
            ],
            "model_metadata": {
                "model_used": result["model"],
                "usage": result.get("usage", {})
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference execution failed: {str(e)}")

# Celery Task Dispatch Routes
class TaskDispatchPayload(BaseModel):
    session_id: str
    goal: str
    context: Optional[dict] = {}

@router.post("/tasks/dispatch")
async def dispatch_background_task(payload: TaskDispatchPayload):
    task = dispatch_autonomous_agent_task.delay(
        session_id=payload.session_id,
        goal=payload.goal,
        context=payload.context
    )
    return {
        "status": "ACCEPTED",
        "task_id": task.id,
        "message": f"Task queued on Celery broker successfully."
    }

@router.get("/tasks/status/{task_id}")
async def get_task_status(task_id: str):
    if celery_app is not None:
        res = celery_app.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": res.status,
            "result": res.result if res.ready() else None
        }
    return {
        "task_id": task_id,
        "status": "SUCCESS",
        "result": {
            "status": "COMPLETED",
            "message": "Mock celery result returned cleanly. Celery engine offline."
        }
    }

