"""
agentP - License & Desktop Distribution Controller
Handles offline licensing, machine fingerprinting, desktop bundle status and quality gate audits.
Author: Sophia (Security Lead) & Liam (DevOps Lead)
"""

import json
from typing import Dict, Any, Tuple
from base_controller import BaseController
from license_guard import LicenseGuardService
from desktop_bundle import DesktopBundleService
from quality_gate_service import QualityGateService

class LicenseController(BaseController):
    """Controller handling software licensing, machine hardware binding, and desktop distribution."""

    @classmethod
    def get_license_status(cls) -> Tuple[int, Dict[str, str], bytes]:
        """Returns the current active license status, machine fingerprint, and tier capabilities."""
        status = LicenseGuardService.get_current_license_status()
        return cls.json_response(status, status=200)

    @classmethod
    def activate_license(cls, body_data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        """Activates a provided offline license key."""
        key = body_data.get("license_key", "").strip()
        if not key:
            return cls.error_response("license_key is required for activation.", status=400)

        res = LicenseGuardService.activate_license(key)
        code = 200 if res.get("status") == "activated" else 400
        return cls.json_response(res, status=code)

    @classmethod
    def generate_license(cls, body_data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        """Admin generator for offline licenses."""
        tier = body_data.get("tier", "ENTERPRISE_SWARM")
        fingerprint = body_data.get("machine_fingerprint")
        duration = int(body_data.get("duration_days", 365))
        licensee = body_data.get("licensee", "Enterprise Owner")

        try:
            lic = LicenseGuardService.generate_license_key(
                tier=tier,
                machine_fingerprint=fingerprint,
                duration_days=duration,
                licensee=licensee
            )
            return cls.json_response(lic, status=201)
        except Exception as e:
            return cls.error_response(str(e), status=400)

    @classmethod
    def get_desktop_bundle_info(cls) -> Tuple[int, Dict[str, str], bytes]:
        """Returns Tauri v2 packaging configuration and distribution readiness."""
        info = DesktopBundleService.verify_distribution_readiness()
        return cls.json_response(info, status=200)

    @classmethod
    def get_quality_gate_status(cls) -> Tuple[int, Dict[str, str], bytes]:
        """Executes and returns the 5-factor production quality gate report."""
        report = QualityGateService.run_full_quality_gate()
        code = 200 if report.get("status") == "APPROVED_FOR_RELEASE" else 422
        return cls.json_response(report, status=code)
