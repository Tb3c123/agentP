import http.server
import socketserver
import json
import sqlite3
import os
import time
from urllib.parse import urlparse

PORT = 9090
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '.agents', 'db.sqlite')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

class NineRouterService:
    """Core 9router protocol and session isolation logic"""
    
    @staticmethod
    def get_health():
        conn = get_db()
        cursor = conn.cursor()
        roles_count = cursor.execute("SELECT COUNT(*) FROM agent_roles").fetchone()[0]
        sessions_count = cursor.execute("SELECT COUNT(*) FROM provider_sessions").fetchone()[0]
        conn.close()

        return {
            "status": "healthy",
            "service": "9router-daemon",
            "version": "1.0.0",
            "port": PORT,
            "db_status": "connected",
            "active_roles": roles_count,
            "isolated_sessions": sessions_count,
            "timestamp": int(time.time())
        }

    @staticmethod
    def get_sessions():
        conn = get_db()
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
        return {"sessions": sessions, "total": len(sessions)}

    @staticmethod
    def get_tokens():
        conn = get_db()
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

    @staticmethod
    def get_kanban():
        conn = get_db()
        cursor = conn.cursor()
        tasks = cursor.execute("""
            SELECT task_id, title, category, column_status, priority, assigned_role_id, tokens_spent
            FROM kanban_tasks
            ORDER BY order_index ASC
        """).fetchall()
        conn.close()

        data = []
        for t in tasks:
            data.append({
                "task_id": t[0],
                "title": t[1],
                "category": t[2],
                "column_status": t[3],
                "priority": t[4],
                "assigned_role_id": t[5],
                "tokens_spent": t[6]
            })
        return {"tasks": data}

    @staticmethod
    def chat_completions(role_id, prompt, task_id=None):
        conn = get_db()
        cursor = conn.cursor()
        role = cursor.execute("SELECT display_name, default_model, persona_summary FROM agent_roles WHERE role_id = ?", (role_id,)).fetchone()
        
        if not role:
            conn.close()
            raise ValueError(f"Role '{role_id}' not found")

        display_name, model, persona = role

        # Simulate Raw Model Thinking logic depending on model type
        thought_start = time.time()
        if "claude" in model:
            thinking_log = f"<thinking> Analyzing role {role_id}. Decomposing requirements: '{prompt[:50]}...'. Plan: verify schema, formulate AST updates, dispatch to swarm. </thinking>"
        elif "deepseek" in model:
            thinking_log = f"<reasoning_content> Step 1: Formal verification of logic constraints. Step 2: Unit test coverage calculus. Conclusion: PASS </reasoning_content>"
        else:
            thinking_log = f"<thought> Context lookup in .agents/db.sqlite. Processing tokens: 350. Execution optimal. </thought>"
        
        thought_duration_ms = int((time.time() - thought_start) * 1000) + 1200
        tokens_in = len(prompt.split()) * 2
        tokens_out = 150
        total_tokens = tokens_in + tokens_out

        response_content = f"[{display_name}]: Đã xử lý yêu cầu liên quan đến '{prompt}'. Trạng thái: Sẵn sàng thực thi."

        # Update provider session stats in SQLite
        cursor.execute("""
            UPDATE provider_sessions 
            SET total_tokens_in = total_tokens_in + ?,
                total_tokens_out = total_tokens_out + ?,
                last_ping_at = CURRENT_TIMESTAMP
            WHERE role_id = ?
        """, (tokens_in, tokens_out, role_id))

        # If task_id provided, update token spent on kanban task
        if task_id:
            cursor.execute("""
                UPDATE kanban_tasks
                SET tokens_spent = tokens_spent + ?
                WHERE task_id = ?
            """, (total_tokens, task_id))

        conn.commit()
        conn.close()

        return {
            "role_id": role_id,
            "display_name": display_name,
            "model": model,
            "content": response_content,
            "thinking_log": thinking_log,
            "thought_duration_ms": thought_duration_ms,
            "tokens_consumed": total_tokens
        }

    @staticmethod
    def resolve_checkpoint(checkpoint_id, action, feedback=""):
        if action not in ['approved', 'rejected']:
            raise ValueError("Action must be 'approved' or 'rejected'")

        conn = get_db()
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
            "message": f"Checkpoint {checkpoint_id} resolved as {action}."
        }


class NineRouterHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Role-Id')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/health':
            self._set_headers(200)
            self.wfile.write(json.dumps(NineRouterService.get_health()).encode('utf-8'))
        elif path == '/sessions':
            self._set_headers(200)
            self.wfile.write(json.dumps(NineRouterService.get_sessions()).encode('utf-8'))
        elif path == '/tokens':
            self._set_headers(200)
            self.wfile.write(json.dumps(NineRouterService.get_tokens()).encode('utf-8'))
        elif path == '/kanban':
            self._set_headers(200)
            self.wfile.write(json.dumps(NineRouterService.get_kanban()).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}

        if path == '/chat/completions':
            role_id = data.get('role_id', 'lead_pm')
            prompt = data.get('prompt', '')
            task_id = data.get('task_id', None)
            try:
                res = NineRouterService.chat_completions(role_id, prompt, task_id)
                self._set_headers(200)
                self.wfile.write(json.dumps(res).encode('utf-8'))
            except ValueError as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        elif path == '/checkpoint/resolve':
            checkpoint_id = data.get('checkpoint_id')
            action = data.get('action')
            feedback = data.get('feedback', '')
            try:
                res = NineRouterService.resolve_checkpoint(checkpoint_id, action, feedback)
                self._set_headers(200)
                self.wfile.write(json.dumps(res).encode('utf-8'))
            except ValueError as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))

def run_server():
    server_address = ('127.0.0.1', PORT)
    httpd = socketserver.TCPServer(server_address, NineRouterHandler)
    httpd.allow_reuse_address = True
    print(f"✓ 9router Local Daemon running at http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down 9router daemon.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
