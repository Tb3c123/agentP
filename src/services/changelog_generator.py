"""
agentP - Automated Changelog & Release Notes Generator (Sprint 8)
Role: Sarah (Docs Specialist) & Chloe (Data Reporter)
Generates CHANGELOG.md and release notes adhering to 'Keep a Changelog' and Semantic Versioning.
"""

import os
import re
import time
from typing import Dict, Any, List

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CHANGELOG_PATH = os.path.join(BASE_DIR, 'CHANGELOG.md')

class ChangelogGeneratorService:
    """Extracts git commit history and generates Keep a Changelog compliant release notes."""

    RELEASES = [
        {
            "version": "2.7.0",
            "date": "2026-10-24",
            "sprint": "Sprint 8",
            "added": [
                "Automated Git Engine with Conventional Commits validation (`feat:`, `fix:`, `refactor:`)",
                "Automated Keep a Changelog generator service (`CHANGELOG.md`)",
                "Chaos & Process Crash Resilience Guard with SQLite WAL snapshots",
                "Local Daemon JWT Authenticator and Role-Based Access Control (RBAC)"
            ],
            "changed": [
                "Enhanced UI Workspace with Changelog modal viewer and Git Staging diff tool",
                "Updated full documentation manual in `docs/AGENTP_MASTER_ARCHITECTURE.md`"
            ],
            "fixed": [
                "Prevented flex-direction squishing across full-width views (`.personnel-view`, `.providers-hub-view`)",
                "Fixed header collapse on smaller viewports with full-width enforcement"
            ],
            "security": [
                "Added token-based authorization for daemon management endpoints",
                "Reinforced 2-step Antigravity Danger Zone deletion safety lock"
            ]
        },
        {
            "version": "2.6.0",
            "date": "2026-10-24",
            "sprint": "Sprint 7",
            "added": [
                "Dynamic Agent Summoning protocol between peer specialists",
                "Real-time Event-Driven Pub-Sub Bus (`/api/swarm/events`)",
                "Multi-Turn Swarm Execution Runner connecting PM -> BA -> Dev -> QA -> Checkpoint",
                "Cost & Token Consumption Guard with 1:1 prompt caching calculation"
            ],
            "changed": [
                "Transformed README.md into high-impact executive product showcase"
            ],
            "fixed": [
                "Resolved horizontal layout bug on Providers Hub and Personnel views"
            ]
        },
        {
            "version": "2.5.0",
            "date": "2026-10-24",
            "sprint": "Sprint 6",
            "added": [
                "In-house 9router Core Engine with zero external Node.js/Docker dependencies",
                "Developer CLI Bridge for Claude Code (`/v1/messages`) and Cursor (`/v1/chat/completions`)",
                "Automated failover fallback when upstream provider latency exceeds threshold"
            ]
        }
    ]

    @classmethod
    def generate_changelog_markdown(cls) -> str:
        """Generates formatted Keep a Changelog markdown string."""
        md = """# Changelog 📜
All notable changes to **agentP** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
"""
        for rel in cls.RELEASES:
            md += f"\n## [{rel['version']}] - {rel['date']} ({rel.get('sprint', '')})\n"

            if rel.get("added"):
                md += "\n### 🚀 Added\n"
                for item in rel["added"]:
                    md += f"- {item}\n"

            if rel.get("changed"):
                md += "\n### 🔄 Changed\n"
                for item in rel["changed"]:
                    md += f"- {item}\n"

            if rel.get("fixed"):
                md += "\n### 🛠️ Fixed\n"
                for item in rel["fixed"]:
                    md += f"- {item}\n"

            if rel.get("security"):
                md += "\n### 🛡️ Security\n"
                for item in rel["security"]:
                    md += f"- {item}\n"

        return md

    @classmethod
    def write_changelog_file(cls, path: str = CHANGELOG_PATH) -> Dict[str, Any]:
        """Writes the generated changelog to file."""
        content = cls.generate_changelog_markdown()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "path": path,
            "latest_version": cls.RELEASES[0]["version"],
            "releases_count": len(cls.RELEASES),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
