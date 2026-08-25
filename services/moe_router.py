import math
from typing import List, Dict, Any

class MoERouter:
    """
    Mixture-of-Experts (MoE) Softmax Routing Engine.
    Dynamically routes user prompts across specialized domain experts:
      1. CodeExpert: Programming, algorithms, syntax, debugging.
      2. MathExpert: Logic, data science, statistics, equations.
      3. SecurityExpert: NIST compliance, prompt injection, cryptography.
      4. GeneralExpert: Conversational synthesis & reasoning.
    """
    EXPERTS = {
        "CodeExpert": ["code", "function", "bug", "python", "javascript", "class", "api", "git", "refactor"],
        "MathExpert": ["math", "equation", "matrix", "calculate", "probability", "statistics", "vector"],
        "SecurityExpert": ["security", "audit", "nist", "encryption", "injection", "auth", "token", "rbac"],
        "GeneralExpert": ["hello", "explain", "summarize", "overview", "kalki", "system", "architecture"]
    }

    @classmethod
    def route_prompt(cls, prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        words = set(prompt_lower.split())
        
        raw_scores = {}
        for expert, keywords in cls.EXPERTS.items():
            overlap = len(words.intersection(set(keywords)))
            raw_scores[expert] = float(overlap * 2.0 + 1.0) # Base prior score of 1.0

        # Apply Softmax activation: P(E_i | prompt) = exp(S_i) / sum(exp(S_j))
        max_score = max(raw_scores.values())
        exp_scores = {k: math.exp(v - max_score) for k, v in raw_scores.items()}
        sum_exp = sum(exp_scores.values())
        softmax_weights = {k: round(v / sum_exp, 4) for k, v in exp_scores.items()}

        # Select Top-1 Primary Expert
        primary_expert = max(softmax_weights, key=softmax_weights.get)

        return {
            "prompt": prompt,
            "primary_expert": primary_expert,
            "routing_weights": softmax_weights,
            "top_confidence": softmax_weights[primary_expert]
        }

moe_router = MoERouter()
