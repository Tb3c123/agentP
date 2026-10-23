"""
agentP - Kanban Controller
Handles 6-column Kanban task status retrievals and task movements.
Author: Carlos (Backend Dev)
"""

import sys
import os
from typing import Dict, Any, Tuple
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'repositories')))
from kanban_repo import KanbanRepository

class KanbanController(BaseController):
    """Manages 6-column Kanban state and task transitions."""

    @staticmethod
    def get_all_tasks() -> Tuple[int, Dict[str, str], bytes]:
        columns = KanbanRepository.get_all_grouped()
        return BaseController.json_response({"columns": columns}, 200)

    @staticmethod
    def move_task(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        task_id = data.get('task_id', '')
        new_column = data.get('new_column', '')

        if not task_id or not new_column:
            return BaseController.error_response("Missing task_id or new_column", 400)

        success = KanbanRepository.update_task_column(task_id, new_column)
        if success:
            return BaseController.json_response({"success": True, "task_id": task_id, "column": new_column}, 200)
        return BaseController.error_response("Invalid column or task not found", 400)
