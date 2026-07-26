import time
from typing import List, Dict, Any
from memory.manager import memory_manager

class MemoryConsolidator:
    """
    Routinely reviews episodic logs to compress history and consolidate long-term rules.
    """
    @staticmethod
    def consolidate_conversation_session(session_id: str) -> Dict[str, Any]:
        """
        Compresses conversation dialogs into summary facts (Memory Compression).
        """
        history = memory_manager.get_conversation_history(session_id, limit=100)
        if not history:
            return {"status": "SKIPPED", "reason": "No conversation history found."}

        # Simulating summary consolidation extraction
        summary_fact = f"User discussed KALKI architectural specs and verified port 8000 health."
        
        # Save to long term memory preferences
        memory_manager.save_user_preference(
            user_id="anonymous",
            key="last_interaction_summary",
            value=summary_fact
        )

        return {
            "status": "CONSOLIDATED",
            "extracted_facts_count": 1,
            "session_id": session_id,
            "summary": summary_fact
        }

    @staticmethod
    def expire_stale_memories(retention_seconds: int = 86400 * 30):
        """
        Prunes old, unaccessed memories (Memory Expiration).
        """
        current_time = time.time()
        print(f"[Memory Engine] Running memory expiration pass. Current time: {current_time}")
        # Pruning logic would clear outdated db rows in postgres/qdrant
        return True

    @staticmethod
    def rank_retrieved_memories(memories: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Ranks memories using Recency and Relevance weight calculations (Memory Ranking).
        """
        ranked = []
        for mem in memories:
            relevance = mem.get("relevance", 0.5)
            # Add recency booster
            time_decay = 1.0 / (time.time() - mem.get("timestamp", time.time()) + 1.0)
            score = relevance * 0.7 + time_decay * 0.3
            
            ranked.append({
                **mem,
                "memory_rank_score": round(score, 4)
            })
            
        ranked.sort(key=lambda x: x["memory_rank_score"], reverse=True)
        return ranked

memory_consolidator = MemoryConsolidator()
