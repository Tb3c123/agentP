"""
agentP - JWT & Role-Based Access Guard (Sprint 8)
Role: Sophia (Security & Compliance Lead)
Provides HMAC-SHA256 session token generation, verification, and RBAC permission enforcement.
"""

import hmac
import hashlib
import base64
import json
import time
from typing import Dict, Any, Optional

SECRET_KEY = b"agentp-secure-internal-hmac-key-2026"

ROLE_PERMISSIONS = {
    "ADMIN": ["all", "delete_project", "approve_checkpoint", "modify_code", "chat"],
    "LEAD_PM": ["approve_checkpoint", "assign_tasks", "modify_code", "chat", "summon"],
    "DEVELOPER": ["modify_code", "run_tests", "chat", "summon"],
    "VIEWER": ["read_only", "view_kanban", "view_logs"]
}

class JwtRbacGuard:
    """Manages secure JWT token generation and role-based access control."""

    @classmethod
    def generate_token(cls, user_id: str, role: str = "LEAD_PM", expiry_hours: int = 24) -> str:
        """Generates a base64 encoded HMAC-SHA256 signed token."""
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": user_id,
            "role": role,
            "iat": int(time.time()),
            "exp": int(time.time()) + (expiry_hours * 3600),
            "permissions": ROLE_PERMISSIONS.get(role, ["read_only"])
        }

        h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signing_input = f"{h_b64}.{p_b64}".encode()

        signature = hmac.new(SECRET_KEY, signing_input, hashlib.sha256).digest()
        sig_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

        return f"{h_b64}.{p_b64}.{sig_b64}"

    @classmethod
    def verify_token(cls, token: str) -> Dict[str, Any]:
        """Verifies token integrity and expiration."""
        parts = token.split(".")
        if len(parts) != 3:
            return {"valid": False, "error": "Invalid token format"}

        h_b64, p_b64, sig_b64 = parts
        signing_input = f"{h_b64}.{p_b64}".encode()
        expected_sig = hmac.new(SECRET_KEY, signing_input, hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(sig_b64 + "=="[:len(sig_b64) % 4])

        if not hmac.compare_digest(expected_sig, actual_sig):
            return {"valid": False, "error": "Invalid signature"}

        try:
            payload = json.loads(base64.urlsafe_b64decode(p_b64 + "=="[:len(p_b64) % 4]).decode())
            if payload.get("exp", 0) < time.time():
                return {"valid": False, "error": "Token expired"}
            return {"valid": True, "payload": payload}
        except Exception as e:
            return {"valid": False, "error": str(e)}

    @classmethod
    def check_permission(cls, token: str, action: str) -> bool:
        """Verifies if the token bearer has permission for the specified action."""
        res = cls.verify_token(token)
        if not res["valid"]:
            return False
        perms = res["payload"].get("permissions", [])
        return "all" in perms or action in perms
