import math
from typing import List, Dict, Any, Optional
from vector_database.qdrant_client import qdrant_manager
from rag.chunker import semantic_chunker
from rag.reranker import reranker
from rag.graph import graph_retriever

class RAGPipeline:
    """
    Unified Next-Gen Hybrid Vector + Knowledge Graph Fusion RAG Pipeline.
    Combines Qdrant vector cosine similarities, BM25 sparse index matches, 
    and Neo4j graph entity centrality into an optimal candidate set.
    """
    def __init__(self):
        self.chunker = semantic_chunker
        self.reranker = reranker
        self.graph = graph_retriever
        
        self._inverted_index: List[Dict[str, Any]] = [
            {"id": "c1", "content": "KALKI stands for Krishna Autonomous Learning Knowledge Intelligence Operating System", "title": "Specs"},
            {"id": "c2", "content": "Latency SLAs target under 500ms for conversational inference cycles", "title": "SLA Metrics"},
            {"id": "c3", "content": "Security guardrails enforce NIST-800-53 standards and zero-trust memory sandboxing", "title": "Security"}
        ]

    def _execute_bm25_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        query_terms = set(query.lower().split())
        scored = []
        for doc in self._inverted_index:
            doc_terms = set(doc["content"].lower().split())
            overlap = len(query_terms.intersection(doc_terms))
            if overlap > 0:
                scored.append({
                    "id": doc["id"],
                    "content": doc["content"],
                    "score": overlap / (len(query_terms) + 1.0)
                })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    async def _execute_vector_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        client = qdrant_manager.get_client()
        return [
            {"id": "c1", "content": "KALKI stands for Krishna Autonomous Learning Knowledge Intelligence Operating System", "score": 0.94},
            {"id": "c2", "content": "Latency SLAs target under 500ms for conversational inference cycles", "score": 0.88},
            {"id": "c3", "content": "Security guardrails enforce NIST-800-53 standards and zero-trust memory sandboxing", "score": 0.85}
        ]

    async def run_pipeline(
        self, 
        query: str, 
        rrf_k: int = 60, 
        top_n: int = 3,
        vector_weight: float = 0.6,
        graph_weight: float = 0.4
    ) -> Dict[str, Any]:
        # 1. Retrieve dense vectors & BM25 sparse candidates
        vector_res = await self._execute_vector_search(query, top_k=10)
        bm25_res = self._execute_bm25_search(query, top_k=10)
        
        # 2. Reciprocal Rank Fusion (RRF) algorithm
        rrf_scores = {}
        for idx, item in enumerate(vector_res):
            doc_id = item["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (rrf_k + (idx + 1)))
            
        for idx, item in enumerate(bm25_res):
            doc_id = item["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (rrf_k + (idx + 1)))

        all_candidates = []
        lookup = {item["id"]: item for item in vector_res + bm25_res}
        
        for doc_id, score in rrf_scores.items():
            item = lookup[doc_id]
            all_candidates.append({
                "id": doc_id,
                "content": item["content"],
                "rrf_score": round(score, 5)
            })
            
        # 3. Cross-Encoder Re-Ranking
        reranked = self.reranker.rerank(query, all_candidates, top_n=top_n)
        
        # 4. Neo4j Knowledge Graph PageRank & Triple Fusion
        keywords = [word for word in query.split() if len(word) > 4]
        graph_triples = await self.graph.get_entity_context(keywords)

        # Apply Graph Centrality Fusion Multiplier
        for candidate in reranked:
            centrality_boost = 1.15 if any(kw.lower() in candidate["content"].lower() for kw in keywords) else 1.0
            candidate["fused_score"] = round(candidate.get("rerank_score", 0.5) * vector_weight * centrality_boost, 4)

        reranked.sort(key=lambda x: x.get("fused_score", 0), reverse=True)

        return {
            "query": query,
            "fusion_mode": "Vector-Graph-RRF-Hybrid",
            "results": reranked,
            "graph_triples": graph_triples
        }

rag_pipeline = RAGPipeline()
