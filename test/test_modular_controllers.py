"""
agentP - Modular Controllers & Repositories Unit Tests
Verifies the Front Controller & Action Dispatcher refactoring.
Author: Viktor (Lead QA)
"""

import unittest
import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'controllers'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'repositories'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'services'))

from dispatcher import RequestDispatcher
from kanban_repo import KanbanRepository
from skills_repo import SkillsRepository
from sessions_repo import SessionsRepository
from diff_strategy import MonacoSideBySideDiffStrategy

class TestModularControllers(unittest.TestCase):

    def test_01_dispatcher_health(self):
        status, headers, body = RequestDispatcher.dispatch_get('/health')
        self.assertEqual(status, 200)
        self.assertEqual(headers.get('Content-Type'), 'application/json')
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["active_roles"], 14)

    def test_02_dispatcher_workspace_state(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/workspace')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("swarm_roles", data)
        self.assertIn("mini_kanban", data)
        self.assertIn("chat_messages", data)

    def test_03_dispatcher_kanban_all(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/kanban/all')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("columns", data)
        self.assertIn("development", data["columns"])
        self.assertIn("done", data["columns"])

    def test_04_dispatcher_skills(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/skills')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["total"], 30)
        self.assertEqual(len(data["skills"]), 30)

    def test_05_dispatcher_file_tree(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/files/tree')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("name", data)
        self.assertIn("children", data)

    def test_06_dispatcher_auto_name(self):
        status, headers, body = RequestDispatcher.dispatch_post(
            '/api/auto-name',
            {"description": "Xây dựng ứng dụng đặt đồ ăn trực tuyến bằng Flutter"}
        )
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("primary", data)
        self.assertIn("suggested_path", data)

    def test_07_diff_strategy(self):
        strategy = MonacoSideBySideDiffStrategy()
        orig = "line 1\nline 2\nline 3"
        mod = "line 1\nline 2 modified\nline 3\nline 4 added"
        diff = strategy.compute_diff(orig, mod, "test.tsx")
        self.assertEqual(diff["filepath"], "test.tsx")
        self.assertGreater(diff["added_lines"], 0)
        self.assertGreater(diff["total_changes"], 0)
        self.assertIn("lines", diff)

    def test_08_repositories_data_isolation(self):
        columns = KanbanRepository.get_all_grouped()
        self.assertIsInstance(columns, dict)
        self.assertIn("backlog", columns)
        
        skills = SkillsRepository.get_all_skills()
        self.assertEqual(len(skills), 30)
        
        sessions = SessionsRepository.get_sessions()
        self.assertEqual(len(sessions), 14)

    def test_09_dispatcher_studio_sync_onlook(self):
        payload = {
            "file_path": "lib/features/cart/cart_button.tsx",
            "component_tag": "CartCheckoutButton",
            "new_classes": "bg-teal-600 text-white font-bold py-3 px-6 rounded-lg shadow-md"
        }
        status, headers, body = RequestDispatcher.dispatch_post('/api/studio/sync-onlook', payload)
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["status"], "synced")
        self.assertEqual(data["component_tag"], "CartCheckoutButton")
        self.assertLess(data["latency_ms"], 100) # DoD latency requirement

    def test_10_dispatcher_studio_save_tldraw(self):
        payload = {
            "title": "Cart Screen Wireframe & User Flow",
            "canvas_data": {
                "version": 1,
                "elements": [{"id": "wireframe_1", "type": "box", "x": 100, "y": 100}]
            }
        }
        status, headers, body = RequestDispatcher.dispatch_post('/api/studio/save-tldraw', payload)
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("snapshot_id", data)
        self.assertIn("concept_board.tldr", data["file_path"])

    def test_11_dispatcher_studio_snapshots(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/studio/snapshots')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("snapshots", data)
        self.assertGreaterEqual(len(data["snapshots"]), 1)


if __name__ == '__main__':
    unittest.main()
