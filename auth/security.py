import time
import re
from typing import Dict, Any, Tuple
from fastapi import Request, HTTPException

class RateLimiter:
    """
    Token Bucket Rate Limiter.
    Limits client API requests to prevent abuse/DoS attacks.
    """
    def __init__(self, requests_per_minute: int = 60):
        self.rate = requests_per_minute
        self.capacity = requests_per_minute
        self.tokens: Dict[str, float] = {}
        self.last_update: Dict[str, float] = {}

    def is_rate_limited(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self.tokens:
            self.tokens[client_id] = self.capacity
            self.last_update[client_id] = now
            return False

        elapsed = now - self.last_update[client_id]
        self.last_update[client_id] = now
        # Replenish tokens based on elapsed time
        self.tokens[client_id] = min(self.capacity, self.tokens[client_id] + elapsed * (self.rate / 60.0))

        if self.tokens[client_id] >= 1.0:
            self.tokens[client_id] -= 1.0
            return False
        return True

class InputSanitizer:
    """
    Perimeter Defense Sanitizer blocking XSS, SQLi, and OS command injection vectors.
    """
    DANGEROUS_PATTERNS = [
        re.compile(r"<script.*?>.*?</script>", re.IGNORECASE),
        re.compile(r"UNION\s+SELECT", re.IGNORECASE),
        re.compile(r";\s*DROP\s+TABLE", re.IGNORECASE),
        re.compile(r"exec\s*\(\s*['\"]", re.IGNORECASE),
        re.compile(r"system\s*\(\s*['\"]", re.IGNORECASE)
    ]

    @classmethod
    def sanitize_text(cls, text: str) -> Tuple[bool, str]:
        for pattern in cls.DANGEROUS_PATTERNS:
            if pattern.search(text):
                return False, f"Security Violation: Input matched prohibited security pattern: '{pattern.pattern}'"
        return True, text

rate_limiter = RateLimiter(requests_per_minute=120)
input_sanitizer = InputSanitizer()
