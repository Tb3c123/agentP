#!/usr/bin/env python3
"""
agentP - Desktop Packaging & Tauri v2 Validation Runner
Author: Liam (DevOps Lead) & Lucas (Senior Dev)
"""

import sys
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'services'))

from desktop_bundle import DesktopBundleService

def main():
    print("=================================================================")
    print("📦 agentP TAURI v2 DESKTOP BUNDLE & PACKAGING VALIDATOR")
    print("=================================================================")
    status = DesktopBundleService.verify_distribution_readiness()
    print(f"Product: {status['product_name']} (v{status['version']})")
    print(f"Identifier: {status['identifier']}")
    print(f"Bundle Type: {status['bundle_type']}")
    print(f"Distribution Targets: {', '.join(status['targets'])}")
    print(f"RAM Footprint Estimate: {status['memory_footprint_estimate_mb']} MB")
    print(f"Cold Boot Estimate: {status['cold_start_estimate_seconds']} s")
    print("-----------------------------------------------------------------")
    for check in status["checks"]:
        mark = "✓" if check["passed"] else "✗"
        print(f"[{mark}] {check['name']}")
    print("=================================================================")
    print(f"Packaging Readiness: {status['status'].upper()}")

    if status["status"] != "ready":
        sys.exit(1)

if __name__ == "__main__":
    main()
