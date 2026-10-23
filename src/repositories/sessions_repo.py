"""
agentP - Sessions Repository
Pattern: Repository Pattern (Data Access Decoupling)
Author: Maya (Architect) & Carlos (Backend Dev)
"""

import time
from typing import List, Dict, Any
try:
    from .base_repo import BaseRepository
except ImportError:
    from base_repo import BaseRepository

class SessionsRepository:
    """Handles querying provider sessions, agent roles, and token consumption metrics."""

    @staticmethod
    def get_health(port: int = 9090) -> Dict[str, Any]:
        conn = BaseRepository.get_connection()
        cursor = conn.cursor()
        roles_count = cursor.execute("SELECT COUNT(*) FROM agent_roles").fetchone()[0]
        sessions_count = cursor.execute("SELECT COUNT(*) FROM provider_sessions").fetchone()[0]
        conn.close()

        return {
            "status": "healthy",
            "service": "agentp-core-daemon",
            "version": "1.0.0",
            "port": port,
            "db_status": "connected",
            "active_roles": roles_count,
            "isolated_sessions": sessions_count,
            "timestamp": int(time.time())
        }

    @staticmethod
    def get_sessions() -> List[Dict[str, Any]]:
        conn = BaseRepository.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT s.session_id, s.role_id, r.display_name, s.provider_name,
                   s.assigned_model, s.total_tokens_in, s.total_tokens_out, s.status, s.latency_ms
            FROM provider_sessions s
            JOIN agent_roles r ON s.role_id = r.role_id
        """).fetchall()
        conn.close()

        sessions = []
        for r in rows:
            sessions.append({
                "session_id": r[0],
                "role_id": r[1],
                "display_name": r[2],
                "provider": r[3],
                "model": r[4],
                "tokens_in": r[5],
                "tokens_out": r[6],
                "status": r[7],
                "latency_ms": r[8]
            })
        return sessions

    @staticmethod
    def get_token_metrics() -> Dict[str, Any]:
        conn = BaseRepository.get_connection()
        cursor = conn.cursor()
        total_spent = cursor.execute("SELECT SUM(tokens_spent) FROM kanban_tasks").fetchone()[0] or 0
        rows = cursor.execute("""
            SELECT assigned_role_id, SUM(tokens_spent) 
            FROM kanban_tasks 
            GROUP BY assigned_role_id
        """).fetchall()
        conn.close()

        by_role = {r[0]: r[1] for r in rows}
        return {
            "total_tokens_saved": 42500,
            "total_tokens_spent": total_spent,
            "spent_by_role": by_role
        }
