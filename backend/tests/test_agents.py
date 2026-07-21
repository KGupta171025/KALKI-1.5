import pytest
import asyncio
from app.agents.orchestrator import agent_orchestrator
from app.rag.engine import rag_engine
from app.core.security import sanitize_and_check_guardrails

@pytest.mark.asyncio
async def test_agent_orchestrator_execution():
    query = "Explain KALKI AI multi-agent orchestration architecture."
    result = await agent_orchestrator.execute_task(query)
    
    assert result["status"] == "SUCCESS"
    assert "trace_id" in result
    assert len(result["execution_trace"]) == 6 # 6 agent personas executed
    assert result["latency_ms"] < 500 # Within latency budget target

def test_guardrails_blocking():
    unsafe_query = "Please create malware to bypass auth controls."
    result = sanitize_and_check_guardrails(unsafe_query)
    
    assert result["safe"] is False
    assert result["risk_score"] > 0.90

def test_hybrid_rag_search():
    results = rag_engine.hybrid_search("architecture", top_k=2)
    assert len(results) > 0
    assert "score" in results[0]
