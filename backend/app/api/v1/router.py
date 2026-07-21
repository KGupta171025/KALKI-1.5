from fastapi import APIRouter
from app.api.v1.endpoints import chat, rag, agents

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["Chat & Agents"])
api_router.include_router(rag.router, prefix="/rag", tags=["Knowledge & RAG"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agent Orchestration"])
