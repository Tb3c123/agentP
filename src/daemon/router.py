"""
agentP Core Daemon (Built-in Local Protocol Router)
Refactored using Front Controller & Action Dispatcher Pattern
Author: Carlos (Backend Dev) & Maya (Architect)
"""

import http.server
import socketserver
import json
import os
import sys

# Add source paths to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'controllers'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'repositories'))

from dispatcher import RequestDispatcher
from base_repo import BaseRepository
from sessions_repo import SessionsRepository
from kanban_repo import KanbanRepository
from protocol_controller import ProtocolController

PORT = 9090

class AgentPCoreDaemonService:
    """Facade for agentP protocol and session isolation logic (Maintains backward-compatibility)."""

    @staticmethod
    def get_health():
        return SessionsRepository.get_health(PORT)

    @staticmethod
    def get_sessions():
        sessions = SessionsRepository.get_sessions()
        return {"sessions": sessions, "total": len(sessions)}

    @staticmethod
    def get_tokens():
        return SessionsRepository.get_token_metrics()

    @staticmethod
    def get_kanban():
        conn = BaseRepository.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT task_id, sprint_id, title, description, category, column_status, priority, assigned_role_id, tokens_spent
            FROM kanban_tasks
            ORDER BY order_index ASC
        """).fetchall()
        conn.close()
        tasks = []
        for t in rows:
            tasks.append({
                "task_id": t[0], "sprint_id": t[1], "title": t[2], "description": t[3],
                "category": t[4], "column_status": t[5], "priority": t[6],
                "assigned_role_id": t[7], "tokens_spent": t[8]
            })
        return {"tasks": tasks, "total": len(tasks)}

    @staticmethod
    def resolve_checkpoint(checkpoint_id="CHK-01", action="approved", feedback=""):
        return {
            "status": action,
            "checkpoint_id": checkpoint_id,
            "feedback": feedback,
            "updated": True
        }

    @staticmethod
    def chat_completions(role_id="lead_pm", prompt="", task_id="TASK-101"):
        _, _, body = ProtocolController.chat_completions({"role_id": role_id, "prompt": prompt, "task_id": task_id})
        return json.loads(body.decode('utf-8'))


class RouterHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Dispatches HTTP requests to domain controllers via RequestDispatcher."""

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Role-Id')
        self.end_headers()

    def do_GET(self):
        status, headers, body = RequestDispatcher.dispatch_get(self.path, PORT)
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            body_data = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
        except Exception:
            body_data = {}

        status, headers, body = RequestDispatcher.dispatch_post(self.path, body_data)
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), RouterHTTPHandler) as httpd:
        print(f"✓ agentP Core Daemon running at http://127.0.0.1:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
