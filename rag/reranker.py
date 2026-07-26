from typing import List, Dict, Any

try:
    from sentence_transformers import CrossEncoder
except ImportError:
    CrossEncoder = None

class CrossEncoderReranker:
    """
    Evaluates semantic match scores of candidate chunks against query text.
    """
    def __init__(self, model_name: str = "BAAI/bge-reranker-large"):
        self.model_name = model_name
        self._model = None
        # Attempt lazy load
        if CrossEncoder is not None:
            try:
                self._model = CrossEncoder(model_name)
            except Exception:
                pass

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        if self._model is not None:
            pairs = [[query, c["content"]] for c in candidates]
            scores = self._model.predict(pairs)
            for idx, score in enumerate(scores):
                candidates[idx]["rerank_score"] = float(score)
        else:
            # Fallback mock scoring
            query_words = set(query.lower().split())
            for c in candidates:
                content_words = set(c["content"].lower().split())
                overlap = len(query_words.intersection(content_words))
                c["rerank_score"] = overlap / (len(query_words) + 1e-5)

        candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        return candidates[:top_n]

reranker = CrossEncoderReranker()
