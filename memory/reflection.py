import time
from typing import Dict, Any, List
from memory.manager import memory_manager

class MemoryReflector:
    """
    Self-Reflection agent engine.
    Analyzes episodic logs to generate optimized task execution procedures.
    """
    @staticmethod
    def reflect_on_failures(failed_episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs critique loops over failed execution sequences, updating procedural rules (Self-Correction).
        """
        reflections = []
        for episode in failed_episodes:
            goal = episode.get("goal", "unknown")
            error_reason = episode.get("error", "execution timeout")
            
            # Formulate corrective lesson learned
            lesson = f"For goal '{goal}' failing due to '{error_reason}', fallback to local Ollama nodes."
            
            # Save lesson learned to procedural memory database
            memory_manager.register_procedural_macro(
                name=f"fallback_rule_for_{goal.replace(' ', '_')[:30]}",
                trigger=f"task_failure: {error_reason}",
                steps=[
                    "switch_llm_provider: ollama",
                    "execute_local_inference",
                    "verify_with_validator"
                ]
            )
            
            reflections.append({
                "target_goal": goal,
                "lesson_learned": lesson,
                "timestamp": time.time()
            })
            
        return reflections

memory_reflector = MemoryReflector()
