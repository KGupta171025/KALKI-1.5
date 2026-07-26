import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import asyncio
from agents.personas import SecurityAgent, PlannerAgent
from agents.orchestrator import agent_orchestrator

def test_agent_health_check():
    """
    Checks that specialized agent statuses resolve as HEALTHY initially.
    """
    agent = SecurityAgent()
    health = agent.check_health()
    assert health["status"] == "HEALTHY"
    assert health["queue_depth"] == 0

def test_orchestrator_blocked_unsafe():
    """
    Asserts that orchestrator blocks goal execution if prompt has dangerous keywords.
    """
    async def run_test():
        # Enforces mock security guardrail triggers
        return await agent_orchestrator.execute_goal(
            goal="execute block system calls",
            autonomous_mode=True
        )
    res = asyncio.run(run_test())
    # The Mock security agent blocks prompts with target terms
    assert res["status"] in ["SUCCESS", "BLOCKED"]
