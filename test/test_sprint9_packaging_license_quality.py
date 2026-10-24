"""
agentP - Sprint 9 Unit Tests: Tauri v2 Packaging, Hardware License Guard & Quality Gate
Author: Viktor (QA Lead) & Sophia (Security Lead) & Liam (DevOps Lead)
"""

import unittest
import os
import sys
import json
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'controllers'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'services'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'repositories'))

from dispatcher import RequestDispatcher
from desktop_bundle import DesktopBundleService
from license_guard import LicenseGuardService, TIER_CAPABILITIES
from quality_gate_service import QualityGateService

class TestSprint9PackagingLicenseQuality(unittest.TestCase):

    def test_01_tauri_bundle_config_and_structure(self):
        cfg = DesktopBundleService.get_bundle_config()
        self.assertEqual(cfg["productName"], "agentP")
        self.assertEqual(cfg["identifier"], "com.agentp.desktop")
        self.assertEqual(cfg["version"], "2.9.0")
        
        windows = cfg["app"]["windows"]
        self.assertGreaterEqual(len(windows), 1)
        self.assertEqual(windows[0]["width"], 1440)
        self.assertEqual(windows[0]["height"], 900)
        self.assertEqual(windows[0]["theme"], "Light")
        self.assertEqual(windows[0]["backgroundColor"], "#F8FAFC")
        self.assertIn("dmg", cfg["bundle"]["targets"])
        self.assertIn("msi", cfg["bundle"]["targets"])

    def test_02_desktop_bundle_service_readiness(self):
        readiness = DesktopBundleService.verify_distribution_readiness()
        self.assertEqual(readiness["status"], "ready")
        self.assertEqual(readiness["version"], "2.9.0")
        self.assertGreater(len(readiness["checks"]), 0)
        for check in readiness["checks"]:
            self.assertTrue(check["passed"], f"Failed check: {check['name']}")

    def test_03_hardware_machine_fingerprinting(self):
        fp1 = LicenseGuardService.get_machine_fingerprint()
        fp2 = LicenseGuardService.get_machine_fingerprint()
        # Must be deterministic on same machine
        self.assertEqual(fp1, fp2)
        self.assertTrue(fp1.startswith("AP-"))
        parts = fp1.split("-")
        self.assertEqual(len(parts), 3)

    def test_04_license_key_generation_and_validation(self):
        fp = LicenseGuardService.get_machine_fingerprint()
        gen = LicenseGuardService.generate_license_key(
            tier="ENTERPRISE_SWARM",
            machine_fingerprint=fp,
            duration_days=180,
            licensee="Enterprise Owner"
        )
        self.assertTrue(gen["license_key"].startswith("AGENTP-ENTERPRISE_SWARM-"))
        
        # Validate against same fingerprint
        val = LicenseGuardService.validate_license_key(gen["license_key"], current_machine_fp=fp)
        self.assertTrue(val["valid"])
        self.assertEqual(val["tier"], "ENTERPRISE_SWARM")
        self.assertEqual(val["licensee"], "Enterprise Owner")
        self.assertTrue(val["features"]["cli_9router_bridge"])
        self.assertTrue(val["features"]["avd_pixel8_controller"])
        self.assertGreater(val["days_remaining"], 170.0)

    def test_05_license_key_machine_lock_protection(self):
        # Generate for machine A
        gen = LicenseGuardService.generate_license_key(
            tier="PRO_INDIE",
            machine_fingerprint="AP-ARM64-AAAA11112222",
            duration_days=30
        )
        # Attempt to validate on machine B
        val = LicenseGuardService.validate_license_key(
            gen["license_key"],
            current_machine_fp="AP-ARM64-BBBB33334444"
        )
        self.assertFalse(val["valid"])
        self.assertTrue(val.get("machine_mismatch"))
        self.assertIn("locked to different machine", val["reason"])

    def test_06_license_key_tamper_and_expiration(self):
        fp = LicenseGuardService.get_machine_fingerprint()
        # Expired license
        gen_exp = LicenseGuardService.generate_license_key(
            tier="COMMUNITY",
            machine_fingerprint=fp,
            duration_days=-5
        )
        val_exp = LicenseGuardService.validate_license_key(gen_exp["license_key"], current_machine_fp=fp)
        self.assertFalse(val_exp["valid"])
        self.assertTrue(val_exp.get("expired"))

        # Tampered signature
        tampered_key = gen_exp["license_key"][:-4] + "DEAD"
        val_tamper = LicenseGuardService.validate_license_key(tampered_key, current_machine_fp=fp)
        self.assertFalse(val_tamper["valid"])

    def test_07_license_activation_and_sqlite_persistence(self):
        fp = LicenseGuardService.get_machine_fingerprint()
        gen = LicenseGuardService.generate_license_key(tier="ENTERPRISE_SWARM", machine_fingerprint=fp)
        act = LicenseGuardService.activate_license(gen["license_key"])
        self.assertEqual(act["status"], "activated")

        status = LicenseGuardService.get_current_license_status()
        self.assertTrue(status["is_licensed"])
        self.assertEqual(status["tier"], "ENTERPRISE_SWARM")
        self.assertEqual(status["badge"], "Enterprise")

    def test_08_wcag_color_contrast_ratios(self):
        contrast = QualityGateService.audit_wcag_color_contrast()
        self.assertTrue(contrast["passed"])
        self.assertEqual(contrast["standard"], "WCAG 2.2 Level AA / AAA")
        
        # Verify specific pairs
        pairs = {p["pair"]: p for p in contrast["audited_pairs"]}
        self.assertIn("Alpine Teal UI Accent (Button/Pill)", pairs)
        self.assertGreaterEqual(pairs["Alpine Teal UI Accent (Button/Pill)"]["contrast_ratio"], 3.0)
        self.assertIn("Fedora Brown on White", pairs)
        self.assertGreaterEqual(pairs["Fedora Brown on White"]["contrast_ratio"], 7.0)

    def test_09_production_quality_gate_audit(self):
        report = QualityGateService.run_full_quality_gate()
        self.assertEqual(report["status"], "APPROVED_FOR_RELEASE")
        self.assertEqual(report["score"], "5/5")
        self.assertEqual(report["quality_score_percent"], 100.0)

    def test_10_license_and_desktop_controller_endpoints(self):
        # 1. GET /api/license/status
        status, headers, body = RequestDispatcher.dispatch_get("/api/license/status")
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertTrue(data["is_licensed"])
        self.assertEqual(data["badge"], "Enterprise")

        # 2. GET /api/desktop/bundle-info
        status, headers, body = RequestDispatcher.dispatch_get("/api/desktop/bundle-info")
        self.assertEqual(status, 200)
        desktop = json.loads(body.decode('utf-8'))
        self.assertEqual(desktop["status"], "ready")

        # 3. GET /api/quality-gate/status
        status, headers, body = RequestDispatcher.dispatch_get("/api/quality-gate/status")
        self.assertEqual(status, 200)
        qg = json.loads(body.decode('utf-8'))
        self.assertEqual(qg["status"], "APPROVED_FOR_RELEASE")

        # 4. POST /api/license/generate
        fp = LicenseGuardService.get_machine_fingerprint()
        status, headers, body = RequestDispatcher.dispatch_post("/api/license/generate", {
            "tier": "PRO_INDIE",
            "machine_fingerprint": fp,
            "duration_days": 90
        })
        self.assertEqual(status, 201)
        gen = json.loads(body.decode('utf-8'))
        self.assertEqual(gen["tier"], "PRO_INDIE")

if __name__ == '__main__':
    unittest.main()
