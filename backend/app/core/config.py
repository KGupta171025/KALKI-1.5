import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "KALKI AI — Intelligence Operating System"
    VERSION: str = "1.5.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "kalki_super_secret_jwt_key_2026_change_in_production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 day
    ALGORITHM: str = "HS256"
    
    # Databases
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "kalki_db")
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    
    # AI Engine Defaults
    DEFAULT_LLM_MODEL: str = "llama-3-70b-instruct"
    SLM_EDGE_MODEL: str = "phi-3-mini-4k-instruct-int4"
    EMBEDDING_DIM: int = 1536
    
    # Latency Targets
    LATENCY_BUDGET_MS: int = 500
    RAG_LATENCY_BUDGET_MS: int = 200

    model_config = SettingsConfigDict(case_sensitive=True, extra="ignore")

settings = Settings()
