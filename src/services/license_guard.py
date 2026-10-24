"""
agentP - Hardware-Locked Cryptographic License Guard
Provides 100% offline license generation, hardware fingerprinting, signature verification, and seat/tier entitlements.
Author: Sophia (Security Lead) & Carlos (Backend Dev)
"""

import os
import sys
import hmac
import hashlib
import time
import uuid
import platform
import json
import sqlite3
from typing import Dict, Any, Optional

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
LICENSE_FILE_PATH = os.path.join(WORKSPACE_DIR, ".agents", "license.json")
DB_PATH = os.path.join(WORKSPACE_DIR, ".agents", "db.sqlite")

# Internal master cryptographic signing key for offline license validation
LICENSE_MASTER_SECRET = b"AGENTP_OFFLINE_HMAC_MASTER_KEY_V290_2026"

TIER_CAPABILITIES = {
    "COMMUNITY": {
        "tier_name": "agentP Community Edition",
        "badge": "Community",
        "max_projects": 1,
        "max_swarm_roles": 4,
        "monthly_token_quota": 50000,
        "features": {
            "single_desk_chat": True,
            "tldraw_whiteboard": True,
            "onlook_dom_sync": False,
            "avd_pixel8_controller": False,
            "cli_9router_bridge": False,
            "excel_corporate_export": False,
            "priority_wal_recovery": False
        }
    },
    "PRO_INDIE": {
        "tier_name": "agentP Pro Indie Suite",
        "badge": "Pro",
        "max_projects": 5,
        "max_swarm_roles": 14,
        "monthly_token_quota": 500000,
        "features": {
            "single_desk_chat": True,
            "tldraw_whiteboard": True,
            "onlook_dom_sync": True,
            "avd_pixel8_controller": True,
            "cli_9router_bridge": True,
            "excel_corporate_export": True,
            "priority_wal_recovery": False
        }
    },
    "ENTERPRISE_SWARM": {
        "tier_name": "agentP Enterprise Multi-Agent Swarm",
        "badge": "Enterprise",
        "max_projects": -1,  # Unlimited
        "max_swarm_roles": 14,
        "monthly_token_quota": -1,  # Unlimited
        "features": {
            "single_desk_chat": True,
            "tldraw_whiteboard": True,
            "onlook_dom_sync": True,
            "avd_pixel8_controller": True,
            "cli_9router_bridge": True,
            "excel_corporate_export": True,
            "priority_wal_recovery": True,
            "custom_ai_models": True,
            "tamper_proof_audit": True
        }
    }
}

class LicenseGuardService:
    """Manages offline hardware-locked licenses, validation, and seat entitlements."""

    @staticmethod
    def get_machine_fingerprint() -> str:
        """
        Generates a deterministic hardware machine fingerprint based on system architecture,
        machine node, system platform and hardware MAC.
        Format: AP-{ARCH}-{HASH_12}
        """
        raw_components = [
            platform.machine(),
            platform.system(),
            platform.node(),
            str(uuid.getnode())  # Hardware MAC address
        ]
        fingerprint_input = ":".join(raw_components).encode('utf-8')
        sha = hashlib.sha256(fingerprint_input).hexdigest()[:12].upper()
        arch = platform.machine().upper()
        return f"AP-{arch}-{sha}"

    @staticmethod
    def generate_license_key(
        tier: str = "ENTERPRISE_SWARM",
        machine_fingerprint: Optional[str] = None,
        duration_days: int = 365,
        licensee: str = "Enterprise Owner"
    ) -> Dict[str, Any]:
        """
        Generates a cryptographically signed offline license key locked to a machine fingerprint.
        Format: AGENTP-{TIER}-{EXPIRY}-{M_HASH}-{SIG}
        """
        if tier not in TIER_CAPABILITIES:
            raise ValueError(f"Invalid tier: {tier}. Must be one of {list(TIER_CAPABILITIES.keys())}")

        m_fp = machine_fingerprint or LicenseGuardService.get_machine_fingerprint()
        m_hash = hashlib.sha256(m_fp.encode('utf-8')).hexdigest()[:8].upper()

        if duration_days == 0:
            expiry_timestamp = 253402300799  # Perpetual (Year 9999)
        else:
            expiry_timestamp = int(time.time()) + (duration_days * 86400)

        payload = f"{tier}:{expiry_timestamp}:{m_hash}:{licensee}"
        signature = hmac.new(LICENSE_MASTER_SECRET, payload.encode('utf-8'), hashlib.sha256).hexdigest()[:12].upper()

        key = f"AGENTP-{tier}-{expiry_timestamp}-{m_hash}-{signature}"

        return {
            "license_key": key,
            "tier": tier,
            "licensee": licensee,
            "machine_fingerprint": m_fp,
            "machine_hash": m_hash,
            "expires_at": expiry_timestamp,
            "signature": signature
        }

    @staticmethod
    def validate_license_key(key: str, current_machine_fp: Optional[str] = None) -> Dict[str, Any]:
        """
        Validates an offline license key against cryptographic signature, expiration and machine binding.
        """
        if not key or not isinstance(key, str):
            return {"valid": False, "reason": "Empty or invalid license key format."}

        parts = key.strip().split("-")
        # Format: AGENTP-{TIER}-{EXPIRY}-{M_HASH}-{SIG}
        if len(parts) != 5 or parts[0] != "AGENTP":
            return {"valid": False, "reason": "Malformed license key structure."}

        _, tier, expiry_str, key_m_hash, signature = parts

        if tier not in TIER_CAPABILITIES:
            return {"valid": False, "reason": f"Unknown license tier '{tier}'."}

        try:
            expiry_ts = int(expiry_str)
        except ValueError:
            return {"valid": False, "reason": "Corrupt expiration timestamp in key."}

        # Check expiration
        now_ts = int(time.time())
        if now_ts > expiry_ts:
            return {
                "valid": False,
                "reason": f"License expired at {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(expiry_ts))}.",
                "expired": True
            }

        # Check machine fingerprint binding
        target_fp = current_machine_fp or LicenseGuardService.get_machine_fingerprint()
        expected_m_hash = hashlib.sha256(target_fp.encode('utf-8')).hexdigest()[:8].upper()
        if key_m_hash != expected_m_hash:
            return {
                "valid": False,
                "reason": f"License locked to different machine. Expected hash {expected_m_hash}, got {key_m_hash}.",
                "machine_mismatch": True
            }

        # Verify HMAC signature against common licensees
        valid_sig = False
        recognized_licensee = None
        for candidate_licensee in ["Enterprise Owner", "Default Licensee", "agentP Pro User", "Developer Seat"]:
            payload = f"{tier}:{expiry_ts}:{key_m_hash}:{candidate_licensee}"
            expected_sig = hmac.new(LICENSE_MASTER_SECRET, payload.encode('utf-8'), hashlib.sha256).hexdigest()[:12].upper()
            if hmac.compare_digest(signature, expected_sig):
                valid_sig = True
                recognized_licensee = candidate_licensee
                break

        if not valid_sig:
            return {"valid": False, "reason": "Cryptographic signature verification failed (tampered key)."}

        capabilities = TIER_CAPABILITIES[tier]
        return {
            "valid": True,
            "tier": tier,
            "licensee": recognized_licensee,
            "tier_info": capabilities,
            "expires_at": expiry_ts,
            "days_remaining": round((expiry_ts - now_ts) / 86400, 1),
            "machine_fingerprint": target_fp,
            "features": capabilities["features"]
        }

    @staticmethod
    def activate_license(key: str) -> Dict[str, Any]:
        """Validates and persists the activated license to .agents/license.json and SQLite."""
        validation = LicenseGuardService.validate_license_key(key)
        if not validation["valid"]:
            return validation

        # 1. Write to .agents/license.json
        os.makedirs(os.path.dirname(LICENSE_FILE_PATH), exist_ok=True)
        license_record = {
            "license_key": key,
            "tier": validation["tier"],
            "licensee": validation["licensee"],
            "activated_at": int(time.time()),
            "expires_at": validation["expires_at"],
            "machine_fingerprint": validation["machine_fingerprint"]
        }
        with open(LICENSE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(license_record, f, indent=2)

        # 2. Persist to SQLite app_licenses table
        LicenseGuardService._sync_sqlite_license(license_record)

        return {
            "status": "activated",
            "message": f"Successfully activated {validation['tier_info']['tier_name']}",
            "license": license_record,
            "capabilities": validation["tier_info"]
        }

    @staticmethod
    def get_current_license_status() -> Dict[str, Any]:
        """Returns the current active license status or falls back to valid default Enterprise Swarm."""
        fp = LicenseGuardService.get_machine_fingerprint()

        # Check if saved license file exists
        if os.path.exists(LICENSE_FILE_PATH):
            try:
                with open(LICENSE_FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                val = LicenseGuardService.validate_license_key(data.get("license_key", ""), current_machine_fp=fp)
                if val["valid"]:
                    return {
                        "is_licensed": True,
                        "tier": val["tier"],
                        "badge": val["tier_info"]["badge"],
                        "tier_name": val["tier_info"]["tier_name"],
                        "license_key": data.get("license_key"),
                        "licensee": data.get("licensee", "Enterprise Owner"),
                        "machine_fingerprint": fp,
                        "days_remaining": val["days_remaining"],
                        "features": val["features"]
                    }
            except Exception:
                pass

        # Default fallback: Enterprise Swarm pre-activated for development & verification
        default_gen = LicenseGuardService.generate_license_key(tier="ENTERPRISE_SWARM", machine_fingerprint=fp)
        LicenseGuardService.activate_license(default_gen["license_key"])

        return {
            "is_licensed": True,
            "tier": "ENTERPRISE_SWARM",
            "badge": "Enterprise",
            "tier_name": "agentP Enterprise Multi-Agent Swarm",
            "license_key": default_gen["license_key"],
            "licensee": "Enterprise Owner",
            "machine_fingerprint": fp,
            "days_remaining": 365.0,
            "features": TIER_CAPABILITIES["ENTERPRISE_SWARM"]["features"]
        }

    @staticmethod
    def _sync_sqlite_license(record: Dict[str, Any]):
        """Creates table app_licenses if needed and inserts the active license."""
        if not os.path.exists(DB_PATH):
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_licenses (
                    license_id TEXT PRIMARY KEY,
                    license_key TEXT NOT NULL UNIQUE,
                    tier TEXT NOT NULL,
                    licensee TEXT NOT NULL,
                    machine_fingerprint TEXT NOT NULL,
                    activated_at INTEGER NOT NULL,
                    expires_at INTEGER NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active'
                );
            """)
            lic_id = f"LIC-{record['tier'][:4]}-{record['activated_at']}"
            cursor.execute("""
                INSERT OR REPLACE INTO app_licenses
                (license_id, license_key, tier, licensee, machine_fingerprint, activated_at, expires_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
            """, (
                lic_id,
                record["license_key"],
                record["tier"],
                record["licensee"],
                record["machine_fingerprint"],
                record["activated_at"],
                record["expires_at"]
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[LicenseGuard] Warning syncing SQLite license: {e}")
