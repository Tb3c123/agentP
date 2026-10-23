"""
agentP - Studio Controller (Sprint 3: Dual-Mode UI/UX Studio)
Handles Tldraw whiteboard persistence and Onlook DOM-to-Code AST 2-way synchronization.
Author: Elena (UI/UX) & Lucas (Senior Dev)
"""

import sys
import os
import json
from typing import Dict, Any, Tuple
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))
from ast_sync import AstSyncEngine

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DESIGNS_DIR = os.path.join(BASE_DIR, '.agents', 'designs')

class StudioController(BaseController):
    """Manages Dual-Mode Studio operations: Tldraw Whiteboard & Onlook AST Sync."""

    @staticmethod
    def sync_onlook(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        file_path = data.get('file_path', 'lib/features/cart/cart_button.tsx')
        component_tag = data.get('component_tag', 'CartCheckoutButton')
        new_classes = data.get('new_classes', 'bg-teal-600 text-white font-bold py-3 px-6 rounded-lg')
        project_id = data.get('project_id', 'proj_food_delivery_01')

        res = AstSyncEngine.sync_dom_to_code(
            file_path=file_path,
            component_tag=component_tag,
            new_classes=new_classes,
            project_id=project_id
        )
        return BaseController.json_response(res, 200)

    @staticmethod
    def save_tldraw(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        title = data.get('title', 'Cart Screen Wireframe')
        canvas_data = data.get('canvas_data', {})
        project_id = data.get('project_id', 'proj_food_delivery_01')
        task_id = data.get('task_id', 'TASK-301')

        res = AstSyncEngine.save_tldraw_snapshot(
            project_id=project_id,
            title=title,
            canvas_data=canvas_data,
            task_id=task_id
        )
        return BaseController.json_response(res, 200)

    @staticmethod
    def get_snapshots(project_id: str = "proj_food_delivery_01") -> Tuple[int, Dict[str, str], bytes]:
        snaps = AstSyncEngine.get_snapshots(project_id=project_id)
        return BaseController.json_response({"snapshots": snaps}, 200)

    @staticmethod
    def get_concept_board() -> Tuple[int, Dict[str, str], bytes]:
        tldr_path = os.path.join(DESIGNS_DIR, 'concept_board.tldr')
        if os.path.exists(tldr_path):
            with open(tldr_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            return BaseController.json_response(content, 200)
        return BaseController.json_response({"version": 1, "elements": []}, 200)
