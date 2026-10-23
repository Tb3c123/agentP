"""
agentP - Kanban Repository
Pattern: Repository Pattern (Data Access Decoupling)
Author: Maya (Architect) & Carlos (Backend Dev)
"""

from typing import Dict, List, Any
try:
    from .base_repo import BaseRepository
except ImportError:
    from base_repo import BaseRepository

class KanbanRepository:
    """Handles persistence and querying of Kanban tasks."""

    @staticmethod
    def get_all_grouped() -> Dict[str, List[Dict[str, Any]]]:
        conn = BaseRepository.get_connection()
        cursor = conn.cursor()
        tasks = cursor.execute("""
            SELECT task_id, sprint_id, title, description, category, column_status, priority, assigned_role_id, tokens_spent
            FROM kanban_tasks
            ORDER BY order_index ASC
        """).fetchall()
        conn.close()

        columns = {
            "backlog": [],
            "spec_design": [],
            "development": [],
            "review": [],
            "quality_gate": [],
            "done": []
        }
        for t in tasks:
            col = t[5]
            if col not in columns:
                col = "development"
            columns[col].append({
                "task_id": t[0],
                "sprint_id": t[1],
                "title": t[2],
                "description": t[3],
                "category": t[4],
                "column_status": t[5],
                "priority": t[6],
                "assigned_role_id": t[7],
                "tokens_spent": t[8]
            })
        return columns

    @staticmethod
    def update_task_column(task_id: str, new_column: str) -> bool:
        valid_columns = {"backlog", "spec_design", "development", "review", "quality_gate", "done"}
        if new_column not in valid_columns:
            return False

        conn = BaseRepository.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE kanban_tasks SET column_status = ? WHERE task_id = ?", (new_column, task_id))
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return updated
