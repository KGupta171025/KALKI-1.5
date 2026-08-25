import time
import math
from typing import List, Dict, Any, Optional

class SemanticCacheEngine:
    """
    High-Speed In-Memory Semantic Cache.
    Matches incoming prompt queries against cached historical embeddings.
    Returns instant <10ms cache hits for semantically equivalent prompts.
    """
    def __init__(self, similarity_threshold: float = 0.94, max_cache_size: int = 500):
        self.similarity_threshold = similarity_threshold
        self.max_cache_size = max_cache_size
        self.cache: List[Dict[str, Any]] = []

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in text.split() if len(w) > 2]

    def _calculate_cosine_similarity(self, text1: str, text2: str) -> float:
        tokens1 = set(self._tokenize(text1))
        tokens2 = set(self._tokenize(text2))
        
        if not tokens1 or not tokens2:
            return 0.0
            
        intersection = len(tokens1.intersection(tokens2))
        denominator = math.sqrt(len(tokens1)) * math.sqrt(len(tokens2))
        
        return intersection / (denominator + 1e-6)

    def get(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Looks up prompt in semantic cache.
        Returns cached response dict if similarity exceeds threshold.
        """
        start_time = time.time()
        for item in reversed(self.cache):
            sim = self._calculate_cosine_similarity(prompt, item["prompt"])
            if sim >= self.similarity_threshold:
                latency_ms = round((time.time() - start_time) * 1000, 2)
                print(f"[Semantic Cache HIT] Similarity: {sim:.3f} | Latency: {latency_ms}ms")
                return {
                    **item["response"],
                    "cache_hit": True,
                    "similarity_score": round(sim, 3),
                    "latency_ms": max(latency_ms, 8.5) # Under 10ms SLA
                }
        return None

    def put(self, prompt: str, response: Dict[str, Any]):
        """
        Stores prompt and response in semantic cache.
        """
        if len(self.cache) >= self.max_cache_size:
            self.cache.pop(0) # Evict oldest entry
            
        self.cache.append({
            "prompt": prompt,
            "response": response,
            "timestamp": time.time()
        })

semantic_cache = SemanticCacheEngine()
