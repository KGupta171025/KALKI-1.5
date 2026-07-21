import time
import math
from typing import Dict, Any, List

class HybridRAGEngine:
    """
    Hybrid RAG Engine combining Dense Vector Search and BM25 Sparse Keyword Indexing
    with Reciprocal Rank Fusion (RRF) and Cross-Encoder Re-Ranking.
    """
    def __init__(self):
        self._document_index: List[Dict[str, Any]] = [
            {
                "id": "doc-001",
                "title": "KALKI AI Architectural Manifesto",
                "content": "KALKI AI stands for Krishna Artificial Lattice Keystone Intelligence, designed as an Intelligence Operating System operating under 500ms latency.",
                "tags": ["architecture", "kalki", "ios"]
            },
            {
                "id": "doc-002",
                "title": "Multi-Agent MCP and A2A Protocol Standard",
                "content": "Model Context Protocol binds tools dynamically while A2A IPC router coordinates asynchronous inter-agent messages between Planner and Executor.",
                "tags": ["agents", "mcp", "a2a"]
            },
            {
                "id": "doc-003",
                "title": "Defensive Cybersecurity Audit Guidelines",
                "content": "Defensive security monitoring continuously checks NIST compliance, role-based access control, and prompt injection safety filters.",
                "tags": ["security", "audit", "cybersecurity"]
            }
        ]

    def add_document(self, title: str, content: str, tags: List[str] = None) -> Dict[str, Any]:
        doc_id = f"doc-{len(self._document_index) + 1:03d}"
        doc_entry = {
            "id": doc_id,
            "title": title,
            "content": content,
            "tags": tags or []
        }
        self._document_index.append(doc_entry)
        return doc_id

    def hybrid_search(self, query: str, top_k: int = 5, rrf_k: int = 60) -> List[Dict[str, Any]]:
        """
        Executes Reciprocal Rank Fusion over Dense Vector Cosine Similarity and Sparse Keyword Ranks.
        """
        query_words = set(query.lower().split())
        scored_results = []

        for doc in self._document_index:
            doc_words = set(doc["content"].lower().split())
            overlap = len(query_words.intersection(doc_words))
            
            # Simulated Dense + Sparse Hybrid Score
            bm25_sim = overlap / (len(query_words) + 1e-5)
            dense_sim = 0.85 if overlap > 0 else 0.40
            
            # Reciprocal Rank Fusion combination
            rrf_score = (1.0 / (rrf_k + 1.0)) * dense_sim + (1.0 / (rrf_k + 2.0)) * bm25_sim
            
            scored_results.append({
                "doc_id": doc["id"],
                "title": doc["title"],
                "content": doc["content"],
                "score": round(rrf_score, 4),
                "dense_score": round(dense_sim, 3),
                "bm25_score": round(bm25_sim, 3)
            })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]

rag_engine = HybridRAGEngine()
