"""
agentP - Request Dispatcher
Pattern: Front Controller & Action Dispatcher Pattern
Author: Carlos (Backend Dev) & Alex (PM)
"""

import sys
import os
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'controllers')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))

from protocol_controller import ProtocolController
from workspace_controller import WorkspaceController
from kanban_controller import KanbanController
from code_controller import CodeController
from project_controller import ProjectController
from skills_controller import SkillsController
from static_controller import StaticController
from ast_sync import AstSyncEngine

class RequestDispatcher:
    """Dispatches incoming HTTP requests to dedicated domain controllers."""

    @staticmethod
    def dispatch_get(url_path: str, port: int = 9090) -> Tuple[int, Dict[str, str], bytes]:
        parsed = urlparse(url_path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # 1. Protocol endpoints
        if path in ('/health', '/api/health'):
            return ProtocolController.get_health(port)
        if path in ('/sessions', '/api/sessions'):
            return ProtocolController.get_sessions()
        if path in ('/tokens', '/api/tokens'):
            return ProtocolController.get_tokens()

        # 2. Workspace & Chat
        if path == '/api/workspace':
            return WorkspaceController.get_state()

        # 3. Kanban Board
        if path in ('/kanban', '/api/kanban', '/api/kanban/all'):
            return KanbanController.get_all_tasks()

        # 4. Universal Skills Library
        if path == '/api/skills':
            cat = query.get('category', [None])[0]
            return SkillsController.get_skills(category=cat)

        # 5. Code & File Operations
        if path == '/api/files/tree':
            return CodeController.get_file_tree()
        if path == '/api/files/content':
            filepath = query.get('path', [''])[0]
            return CodeController.get_file_content(filepath)
        if path == '/api/files/trash':
            return CodeController.get_trash_items()
        if path == '/api/code/diff':
            filepath = query.get('path', ['lib/features/cart/cart_button.tsx'])[0]
            return CodeController.get_split_diff(filepath)

        # 6. Project & Settings
        if path == '/api/project/settings':
            return ProjectController.get_settings()

        # 7. UI Studio AST Snapshots
        if path == '/api/studio/snapshots':
            snaps = AstSyncEngine.get_snapshots()
            headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            import json
            return 200, headers, json.dumps({"snapshots": snaps}).encode('utf-8')

        # Fallback: Static web files
        return StaticController.serve_file(path)

    @staticmethod
    def dispatch_post(url_path: str, body_data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        parsed = urlparse(url_path)
        path = parsed.path

        if path == '/api/chat/send':
            return WorkspaceController.send_chat(body_data)
        if path == '/api/checkpoint/respond':
            return WorkspaceController.respond_checkpoint(body_data)
        if path == '/api/kanban/move-task':
            return KanbanController.move_task(body_data)
        if path == '/api/files/delete':
            return CodeController.delete_file(body_data)
        if path == '/api/auto-name':
            return ProjectController.auto_name(body_data)
        if path == '/api/project/verify-delete':
            return ProjectController.verify_delete(body_data)
        if path == '/v1/chat/completions':
            return ProtocolController.chat_completions(body_data)

        headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        import json
        return 404, headers, json.dumps({"error": f"Endpoint not found: {path}"}).encode('utf-8')
