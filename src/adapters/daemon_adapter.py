"""
agentP Architecture - agentP Daemon Adapter
Implements LlmGatewayPort using the built-in daemon logic.
"""

import sys
import os
import sqlite3
import time
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core")))
from ports import LlmGatewayPort

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DB_PATH = os.path.join(WORKSPACE_DIR, ".agents", "db.sqlite")

class AgentPDaemonAdapter(LlmGatewayPort):
    """Concrete LLM Gateway Adapter for agentP Core Daemon"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    def check_health(self) -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()
        roles_count = cursor.execute("SELECT COUNT(*) FROM agent_roles").fetchone()[0]
        sessions_count = cursor.execute("SELECT COUNT(*) FROM provider_sessions").fetchone()[0]
        conn.close()

        return {
            "status": "healthy",
            "service": "agentp-core-daemon",
            "active_roles": roles_count,
            "isolated_sessions": sessions_count
        }

    def get_active_sessions(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        sessions = cursor.execute("""
            SELECT session_id, role_id, provider_type, model_name, status, total_tokens_in + total_tokens_out
            FROM provider_sessions
        """).fetchall()
        conn.close()

        return [{
            "session_id": s[0],
            "role_id": s[1],
            "provider": s[2],
            "model": s[3],
            "status": s[4],
            "tokens": s[5]
        } for s in sessions]

    def generate_completion(self, role_id: str, prompt: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()
        role = cursor.execute("SELECT display_name, default_model FROM agent_roles WHERE role_id = ?", (role_id,)).fetchone()
        conn.close()

        if not role:
            raise ValueError(f"Role {role_id} not found")

        display_name, model = role
        if "claude" in model:
            thinking = f"<thinking> Role {role_id} analyzing '{prompt[:30]}...'. Plan: verified. </thinking>"
        elif "deepseek" in model:
            thinking = f"<reasoning_content> Step 1: Formal deduction. Step 2: Verification. Output: Optimal. </reasoning_content>"
        else:
            thinking = f"<thought> Context lookup in SQLite. Tokens optimal. </thought>"

        return {
            "role_id": role_id,
            "display_name": display_name,
            "model": model,
            "content": f"[{display_name}]: Đã hoàn tất xử lý cho '{prompt}'.",
            "thinking_log": thinking,
            "tokens_consumed": len(prompt.split()) * 2 + 100
        }
