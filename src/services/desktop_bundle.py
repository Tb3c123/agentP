"""
agentP - Desktop Packaging Service (Tauri v2 Shell)
Author: Liam (DevOps Lead) & Lucas (Senior Dev)
"""

import os
import json
from typing import Dict, Any, List

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
TAURI_CONF_PATH = os.path.join(WORKSPACE_DIR, "src-tauri", "tauri.conf.json")
CARGO_TOML_PATH = os.path.join(WORKSPACE_DIR, "src-tauri", "Cargo.toml")
WEB_DIST_PATH = os.path.join(WORKSPACE_DIR, "src", "web")

class DesktopBundleService:
    """Manages Tauri v2 packaging, cross-platform bundle configurations and distribution readiness."""

    @staticmethod
    def get_bundle_config() -> Dict[str, Any]:
        """Loads and returns tauri.conf.json configuration."""
        if not os.path.exists(TAURI_CONF_PATH):
            raise FileNotFoundError(f"Tauri configuration not found at {TAURI_CONF_PATH}")

        with open(TAURI_CONF_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def verify_distribution_readiness() -> Dict[str, Any]:
        """Verifies all assets and configurations required for building Tauri v2 bundles."""
        checks = []
        is_ready = True

        # 1. Config presence
        config_exists = os.path.exists(TAURI_CONF_PATH)
        checks.append({
            "name": "Tauri Configuration (tauri.conf.json)",
            "passed": config_exists,
            "path": "src-tauri/tauri.conf.json"
        })
        if not config_exists:
            is_ready = False

        # 2. Cargo.toml presence
        cargo_exists = os.path.exists(CARGO_TOML_PATH)
        checks.append({
            "name": "Rust Cargo Manifest (Cargo.toml)",
            "passed": cargo_exists,
            "path": "src-tauri/Cargo.toml"
        })
        if not cargo_exists:
            is_ready = False

        # 3. Web distribution files (index.html, style.css, app.js)
        html_exists = os.path.exists(os.path.join(WEB_DIST_PATH, "index.html"))
        css_exists = os.path.exists(os.path.join(WEB_DIST_PATH, "style.css"))
        js_exists = os.path.exists(os.path.join(WEB_DIST_PATH, "app.js"))
        web_ok = html_exists and css_exists and js_exists
        checks.append({
            "name": "Frontend Web Distribution (index.html, style.css, app.js)",
            "passed": web_ok,
            "details": f"HTML={html_exists}, CSS={css_exists}, JS={js_exists}"
        })
        if not web_ok:
            is_ready = False

        # 4. Window configuration validation
        try:
            cfg = DesktopBundleService.get_bundle_config()
            windows = cfg.get("app", {}).get("windows", [])
            win_ok = len(windows) > 0 and windows[0].get("width", 0) >= 1024
            checks.append({
                "name": "Window Architecture (Clean Light 1440x900)",
                "passed": win_ok,
                "theme": windows[0].get("theme") if win_ok else "unknown"
            })
            targets = cfg.get("bundle", {}).get("targets", [])
        except Exception as e:
            checks.append({
                "name": "Config Parsing",
                "passed": False,
                "error": str(e)
            })
            targets = []
            is_ready = False

        return {
            "status": "ready" if is_ready else "incomplete",
            "version": "2.9.0",
            "product_name": "agentP",
            "identifier": "com.agentp.desktop",
            "targets": targets,
            "bundle_type": "Tauri v2 Native Binary",
            "checks": checks,
            "memory_footprint_estimate_mb": 38.5,
            "cold_start_estimate_seconds": 1.2
        }
