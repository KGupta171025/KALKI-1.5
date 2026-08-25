import json
from typing import Optional, Any
from config.settings import settings

try:
    import redis
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception:
    redis_client = None

class RedisCacheManager:
    """
    High-Throughput Redis Read-Aside and Write-Through Caching Engine.
    Exposes TTL expiration and fast key retrieval for completions and embeddings.
    """
    @staticmethod
    def get(key: str) -> Optional[Any]:
        if redis_client is not None:
            try:
                val = redis_client.get(key)
                if val:
                    return json.loads(val)
            except Exception:
                pass
        return None

    @staticmethod
    def set(key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        if redis_client is not None:
            try:
                serialized = json.dumps(value)
                redis_client.setex(key, ttl_seconds, serialized)
                return True
            except Exception:
                pass
        return False

cache_manager = RedisCacheManager()
