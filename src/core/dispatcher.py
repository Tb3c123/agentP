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
from studio_controller import StudioController
from devops_controller import DevOpsController
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

        # 7. UI Studio AST Snapshots & Concept Board
        if path in ('/api/studio/snapshots', '/api/studio/snapshots/'):
            return StudioController.get_snapshots()
        if path == '/api/studio/concept-board':
            return StudioController.get_concept_board()

        # 8. Sprint 5: DevOps, AVD & Mobile Remote Controller & Preflight
        if path in ('/api/preflight/status', '/api/preflight/run', '/api/devops/preflight'):
            return DevOpsController.get_preflight()
        if path == '/api/devops/avd/status':
            return DevOpsController.get_avd_status()
        if path == '/api/remote/pairing-info':
            return DevOpsController.get_remote_pairing()
        if path in ('/api/reports/excel/export', '/api/reports/excel'):
            return DevOpsController.export_excel_report()

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
        if path == '/api/studio/sync-onlook':
            return StudioController.sync_onlook(body_data)
        if path == '/api/studio/save-tldraw':
            return StudioController.save_tldraw(body_data)
        if path == '/api/devops/avd/launch':
            return DevOpsController.launch_avd(body_data)
        if path == '/api/devops/avd/reload':
            return DevOpsController.reload_avd()
        if path == '/api/devops/avd/screenshot':
            return DevOpsController.screenshot_avd()
        if path in ('/api/preflight/run', '/api/devops/preflight/run'):
            return DevOpsController.get_preflight()
        if path in ('/api/protocol/test-connection', '/api/protocol/test'):
            return ProtocolController.test_connections()
        if path == '/api/protocol/update-model':
            return ProtocolController.update_model(body_data)
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
