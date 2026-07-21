from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from app.rag.engine import rag_engine

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/search")
async def search_knowledge_base(payload: SearchRequest):
    results = rag_engine.hybrid_search(payload.query, payload.top_k)
    return {
        "query": payload.query,
        "results_count": len(results),
        "results": results
    }

@router.post("/documents/upload")
async def upload_document(
    title: str = Form(...),
    content: str = Form(...)
):
    doc_id = rag_engine.add_document(title, content)
    return {
        "status": "SUCCESS",
        "document_id": doc_id,
        "message": f"Document '{title}' indexed successfully for hybrid RAG search."
    }
