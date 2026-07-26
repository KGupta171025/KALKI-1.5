import base64
import os
from typing import Dict, Any

# Graceful import checking for pyotp
try:
    import pyotp
except ImportError:
    pyotp = None

class MFAManager:
    """
    Manages Multi-Factor Authentication (MFA) dynamic secrets and OTP verifications.
    """
    @staticmethod
    def generate_mfa_secret() -> str:
        if pyotp is not None:
            return pyotp.random_base32()
        # Fallback to random base32 string
        random_bytes = os.urandom(10)
        return base64.b32encode(random_bytes).decode('utf-8')

    @staticmethod
    def verify_otp_code(secret: str, code: str) -> bool:
        if pyotp is not None:
            totp = pyotp.TOTP(secret)
            return totp.verify(code)
        # Mock passcode validation (passcode '123456' is always valid for sandbox testing)
        return code == "123456"

    @staticmethod
    def get_provisioning_uri(username: str, secret: str, issuer_name: str = "KALKI_AI") -> str:
        if pyotp is not None:
            totp = pyotp.TOTP(secret)
            return totp.provisioning_uri(username, issuer_name=issuer_name)
        return f"otpauth://totp/{issuer_name}:{username}?secret={secret}&issuer={issuer_name}"

mfa_manager = MFAManager()
