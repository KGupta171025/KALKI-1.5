import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import time
from memory.manager import memory_manager
from memory.consolidation import memory_consolidator
from memory.reflection import memory_reflector

def test_short_term_context():
    """
    Checks adding and retrieving messages from conversation queues.
    """
    session = "sess-test"
    memory_manager.add_conversation_message(session, "user", "Hello World")
    history = memory_manager.get_conversation_history(session)
    assert len(history) >= 1
    assert history[-1]["content"] == "Hello World"

def test_long_term_preferences():
    """
    Verifies user preferences are saved and retrieved cleanly.
    """
    user = "usr-test"
    memory_manager.save_user_preference(user, "test_style", "concise")
    prefs = memory_manager.get_user_preferences(user)
    assert prefs["test_style"] == "concise"

def test_memory_ranking():
    """
    Checks that Recency and Relevance weights list ranking sorts items descending.
    """
    candidates = [
        {"id": "1", "content": "Fact A", "relevance": 0.5, "timestamp": time.time() - 100},
        {"id": "2", "content": "Fact B", "relevance": 0.9, "timestamp": time.time()}
    ]
    ranked = memory_consolidator.rank_retrieved_memories(candidates, "Query")
    assert ranked[0]["id"] == "2" # Fact B has higher relevance and recency

def test_self_reflection():
    """
    Validates that failed execution traces trigger procedural rule synthesis.
    """
    failures = [
        {"goal": "Check Neo4j port", "error": "Bolt connection reset"}
    ]
    reflections = memory_reflector.reflect_on_failures(failures)
    assert len(reflections) == 1
    assert reflections[0]["target_goal"] == "Check Neo4j port"
    
    # Check that procedural memory registered it
    macros = memory_manager.list_procedural_macros()
    assert any(k.startswith("fallback_rule_for_") for k in macros.keys())
