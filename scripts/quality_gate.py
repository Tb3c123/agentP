#!/usr/bin/env python3
"""
agentP - Production Quality Gate & A11y Auditor CLI Runner
"""

import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'services'))

from quality_gate_service import QualityGateService

def main():
    print("=================================================================")
    print("🛡️  agentP PRODUCTION QUALITY GATE & A11Y WCAG 2.2 AUDITOR")
    print("=================================================================")
    report = QualityGateService.run_full_quality_gate()
    print(f"Status: {report['status']} (Score: {report['score']} - {report['quality_score_percent']}%)")
    for name, audit in report["audits"].items():
        status_icon = "✓" if audit.get("passed", audit.get("all_passed", audit.get("status") == "ready")) else "✗"
        print(f"[{status_icon}] {name.replace('_', ' ').title()}")
    print("=================================================================")
    print(f"Reports saved to reports/production_quality_gate.json & .md")
    if report["status"] != "APPROVED_FOR_RELEASE":
        sys.exit(1)

if __name__ == "__main__":
    main()
