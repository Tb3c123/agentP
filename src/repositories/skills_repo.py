"""
agentP - Skills Repository
Pattern: Repository Pattern (Data Access Decoupling)
Author: Maya (Architect) & Carlos (Backend Dev)
"""

from typing import List, Dict, Any, Optional
try:
    from .base_repo import BaseRepository
except ImportError:
    from base_repo import BaseRepository

class SkillsRepository:
    """Handles querying and filtering of Universal Agent Skills."""

    @staticmethod
    def get_all_skills(category: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = BaseRepository.get_connection()
        cursor = conn.cursor()

        if category:
            rows = cursor.execute("""
                SELECT skill_id, name, category, description, tools_required, file_path 
                FROM agent_skills 
                WHERE category = ?
                ORDER BY name
            """, (category,)).fetchall()
        else:
            rows = cursor.execute("""
                SELECT skill_id, name, category, description, tools_required, file_path 
                FROM agent_skills 
                ORDER BY category, name
            """).fetchall()

        conn.close()
        return [
            {
                "id": r[0],
                "name": r[1],
                "category": r[2],
                "description": r[3],
                "tools": r[4],
                "file_path": r[5]
            }
            for r in rows
        ]

    @staticmethod
    def count() -> int:
        conn = BaseRepository.get_connection()
        cursor = conn.cursor()
        total = cursor.execute("SELECT COUNT(*) FROM agent_skills").fetchone()[0]
        conn.close()
        return total
