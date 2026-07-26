import hashlib
import time
import json
from typing import Dict, Any, Optional

class AuditLogger:
    """
    Production-grade structured Audit Logger.
    Logs system actions, payload hashes, and risk indicators.
    """
    @staticmethod
    def compute_payload_hash(payload: dict) -> str:
        """
        Computes SHA256 signature hash of event parameters for auditing verification.
        """
        payload_str = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(payload_str.encode('utf-8')).hexdigest()

    @staticmethod
    def write_audit_entry(
        user_id: str,
        action: str,
        target: str,
        status_code: int,
        ip_address: str,
        payload: dict
    ) -> Dict[str, Any]:
        payload_hash = AuditLogger.compute_payload_hash(payload)
        
        # Risk assessment heuristics based on status codes
        risk_score = 0.0
        if status_code >= 400:
            risk_score = 0.45
        if status_code == 403:
            risk_score = 0.88

        entry = {
            "timestamp": time.time(),
            "user_id": user_id,
            "action": action,
            "target": target,
            "status_code": status_code,
            "ip_address": ip_address,
            "payload_hash": payload_hash,
            "risk_score": risk_score
        }
        
        # In a real environment, this maps directly to PostgreSQL audit_logs table
        print(f"[AUDIT] {action} by {user_id} on {target} completed (Code: {status_code}). Hash: {payload_hash[:8]}")
        return entry

audit_logger = AuditLogger()
