from datetime import datetime, timedelta
from typing import Any, Union, Dict, List

try:
    from jose import jwt
except ImportError:
    jwt = None

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except ImportError:
    pwd_context = None

from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if pwd_context:
        return pwd_context.verify(plain_password, hashed_password)
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    if pwd_context:
        return pwd_context.hash(password)
    return f"hashed_{password}"

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    if jwt:
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return f"token_mock_{subject}_{int(expire.timestamp())}"


# Defensive Safety Guardrails
PROHIBITED_PATTERNS: List[str] = [
    "create malware", "bypass auth", "exploit vulnerability", 
    "unauthorized access", "ddos attack", "surveillance without consent"
]

def sanitize_and_check_guardrails(prompt: str) -> Dict[str, Any]:
    """
    Scans incoming prompt against AI Guardrail defense policies.
    """
    prompt_lower = prompt.lower()
    for pattern in PROHIBITED_PATTERNS:
        if pattern in prompt_lower:
            return {
                "safe": False,
                "risk_score": 0.98,
                "reason": f"Violates KALKI Defensive Safety Constraint: Contains prohibited pattern '{pattern}'"
            }
    return {
        "safe": True,
        "risk_score": 0.02,
        "reason": "Passed Security Guardrail inspection"
    }
