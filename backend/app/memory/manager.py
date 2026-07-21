import time
from typing import Dict, Any, List, Optional

class HierarchicalMemoryManager:
    """
    Manages short-term, long-term, semantic, episodic, and procedural memory stores.
    """
    def __init__(self):
        self._short_term: Dict[str, List[Dict[str, Any]]] = {}
        self._long_term: Dict[str, Dict[str, Any]] = {}
        self._semantic_triples: List[Dict[str, Any]] = []
        self._episodic_history: List[Dict[str, Any]] = []
        self._procedural_dags: Dict[str, Dict[str, Any]] = {}

    def add_short_term_message(self, session_id: str, role: str, content: str):
        if session_id not in self._short_term:
            self._short_term[session_id] = []
        self._short_term[session_id].append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })

    def get_short_term_context(self, session_id: str, max_history: int = 10) -> List[Dict[str, Any]]:
        return self._short_term.get(session_id, [])[-max_history:]

    def set_long_term_preference(self, user_id: str, key: str, value: Any):
        if user_id not in self._long_term:
            self._long_term[user_id] = {}
        self._long_term[user_id][key] = value

    def get_long_term_preferences(self, user_id: str) -> Dict[str, Any]:
        return self._long_term.get(user_id, {"response_style": "detailed", "domain": "AI Systems"})

    def record_episodic_event(self, user_id: str, task_goal: str, execution_trace: List[Dict[str, Any]], success: bool):
        self._episodic_history.append({
            "user_id": user_id,
            "goal": task_goal,
            "trace": execution_trace,
            "success": success,
            "timestamp": time.time()
        })

    def get_memory_summary(self, user_id: str) -> Dict[str, Any]:
        return {
            "short_term_active_sessions": len(self._short_term),
            "long_term_user_prefs": self.get_long_term_preferences(user_id),
            "episodic_records_count": len(self._episodic_history),
            "procedural_workflows_count": len(self._procedural_dags)
        }

memory_manager = HierarchicalMemoryManager()
