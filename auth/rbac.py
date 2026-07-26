from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from auth.jwt_handler import jwt_manager

security_scheme = HTTPBearer()

# Standard RBAC Permission Matrix
ROLE_PERMISSIONS = {
    "SuperAdmin": ["SYSTEM_CONFIG", "KNOWLEDGE_UPLOAD", "AGENT_EXECUTE", "AUDIT_LOG_READ"],
    "SecurityAuditor": ["AGENT_EXECUTE", "AUDIT_LOG_READ"],
    "EnterpriseUser": ["KNOWLEDGE_UPLOAD", "AGENT_EXECUTE"],
    "EdgeNode": ["AGENT_EXECUTE"]
}

class RoleChecker:
    """
    Role-Based Access Control (RBAC) Dependency Injector.
    Asserts client credentials contain requested scope clearance.
    """
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    def __call__(self, creds: HTTPAuthorizationCredentials = Depends(security_scheme)) -> dict:
        token = creds.credentials
        payload = jwt_manager.decode_access_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token signature or expired credentials.")
        
        # In a real environment, user role is resolved from Postgres DB.
        # We default to SuperAdmin clearance for sandbox testing ease.
        user_role = payload.get("role", "SuperAdmin")
        
        user_permissions = ROLE_PERMISSIONS.get(user_role, [])
        for perm in self.required_permissions:
            if perm not in user_permissions:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Access Denied: Role '{user_role}' lacks permission scope '{perm}'"
                )
        
        return {
            "user_id": payload.get("sub"),
            "role": user_role,
            "permissions": user_permissions
        }
