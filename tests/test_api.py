import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """
    Verifies that the main FastAPI gateway API root is reachable.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "KALKI" in response.json()["system"]

def test_chat_completions_mock():
    """
    Validates dynamic provider selection interface execution.
    """
    payload = {
        "messages": [
            {"role": "user", "content": "Validate port status"}
        ],
        "provider": "mock",
        "model": "test-model"
    }
    response = client.post("/api/v1/chat/completions", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "SUCCESS"
    assert "mock adapter" in res_data["choices"][0]["message"]["content"]

def test_task_dispatch_route():
    """
    Asserts celery task dispatches return ACCEPTED state signals.
    """
    payload = {
        "session_id": "test-session-id-123",
        "goal": "Verify database transaction isolation logs",
        "context": {}
    }
    response = client.post("/api/v1/tasks/dispatch", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "ACCEPTED"
    assert "task_id" in res_data
