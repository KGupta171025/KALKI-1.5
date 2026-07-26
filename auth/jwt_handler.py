import datetime
from typing import Optional, Dict, Any
from config.settings import settings

# Graceful import check for python-jose, fallback to standard mock tokens
try:
    from jose import jwt
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except ImportError:
    jwt = None
    pwd_context = None

class JWTManager:
    """
    Handles JWT token creation, signature verification, and password hashing.
    """
    @staticmethod
    def get_password_hash(password: str) -> str:
        if pwd_context is not None:
            return pwd_context.hash(password)
        return f"hashed_mock_{password}"

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        if pwd_context is not None:
            return pwd_context.verify(plain_password, hashed_password)
        return hashed_password == f"hashed_mock_{plain_password}"

    @staticmethod
    def create_access_token(subject: str, expires_delta: Optional[datetime.timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "issued_at": datetime.datetime.utcnow().timestamp()
        }
        
        if jwt is not None:
            return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return f"mock_token_for_{subject}_expires_{int(expire.timestamp())}"

    @staticmethod
    def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
        if jwt is not None:
            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                return decoded
            except Exception:
                return None
        # Handle verification of mock tokens in local runtime validations
        if token.startswith("mock_token_for_"):
            parts = token.split("_")
            return {"sub": parts[3]}
        return None

jwt_manager = JWTManager()
