"""
agentP Architecture - SQLite Storage Adapter
Implements StoragePort using SQLite in WAL mode.
"""

import sqlite3
import os
import sys
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core")))
from ports import StoragePort

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DB_PATH = os.path.join(WORKSPACE_DIR, ".agents", "db.sqlite")

class SQLiteStorageAdapter(StoragePort):
    """Concrete Storage Adapter for SQLite"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    def get_workspace_state(self, project_id: str = "proj_food_delivery") -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()

        # Swarm roles
        cursor.execute("SELECT role_id, display_name, persona_summary, default_model, is_active FROM agent_roles")
        roles = []
        for r in cursor.fetchall():
            roles.append({
                "role_id": r[0],
                "display_name": r[1],
                "persona": r[2],
                "model": r[3],
                "status": "connected" if r[4] else "offline",
                "tokens_spent": "1.2k"
            })

        # Mini kanban
        cursor.execute("SELECT task_id, title, column_status, priority, assigned_role_id FROM kanban_tasks ORDER BY order_index ASC")
        tasks = cursor.fetchall()

        cols = {"todo": [], "coding": [], "qa": [], "done": []}
        for t in tasks:
            col = t[2]
            target = "todo"
            if col in ["development", "coding"]: target = "coding"
            elif col in ["review", "quality_gate", "qa"]: target = "qa"
            elif col == "done": target = "done"

            cols[target].append({
                "task_id": t[0],
                "title": t[1],
                "priority": t[3],
                "role": t[4]
            })

        conn.close()
        return {
            "project_id": project_id,
            "swarm_roles": roles,
            "mini_kanban": cols
        }

    def save_task(self, task_data: Dict[str, Any]) -> str:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO kanban_tasks 
        (task_id, project_id, title, category, column_status, priority, assigned_role_id, tokens_spent, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (
            task_data.get("task_id"),
            task_data.get("project_id", "proj_food_delivery_01"),
            task_data.get("title"),
            task_data.get("category", "frontend"),
            task_data.get("column_status", "development"),
            task_data.get("priority", "medium"),
            task_data.get("assigned_role_id", "frontend_dev"),
            task_data.get("tokens_spent", 0)
        ))
        conn.commit()
        conn.close()
        return task_data.get("task_id")

    def update_task_status(self, task_id: str, new_status: str) -> bool:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE kanban_tasks SET column_status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?", (new_status, task_id))
        conn.commit()
        conn.close()
        return True

    def resolve_checkpoint(self, checkpoint_id: str, action: str, feedback: str = "") -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE checkpoint_gates 
        SET status = ?, user_feedback = ?, resolved_at = CURRENT_TIMESTAMP 
        WHERE checkpoint_id = ?
        """, (action, feedback, checkpoint_id))
        conn.commit()
        conn.close()
        return {
            "checkpoint_id": checkpoint_id,
            "status": action,
            "feedback": feedback
        }

    def record_token_usage(self, role_id: str, tokens_in: int, tokens_out: int, task_id: Optional[str] = None):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE provider_sessions 
        SET total_tokens_in = total_tokens_in + ?,
            total_tokens_out = total_tokens_out + ?,
            last_ping_at = CURRENT_TIMESTAMP
        WHERE role_id = ?
        """, (tokens_in, tokens_out, role_id))
        conn.commit()
        conn.close()
