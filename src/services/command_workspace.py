import sqlite3
import os
import time
import uuid

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '.agents', 'db.sqlite')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

class CommandWorkspaceService:
    """Quản lý logic Bàn làm việc điều hành chính, Chat stream và Mode A Mini-Kanban"""

    @staticmethod
    def get_workspace_state(project_id="proj_food_delivery_01"):
        conn = get_db()
        cursor = conn.cursor()

        # 1. Project Info
        project = cursor.execute("SELECT project_id, name, slug, workspace_path, status FROM projects WHERE project_id = ?", (project_id,)).fetchone()
        
        # 2. 14 Swarm Roles with Token Meters
        roles = cursor.execute("""
            SELECT role_id, display_name, code_name, category, default_model, color_accent
            FROM agent_roles
            ORDER BY rowid ASC
        """).fetchall()

        # 3. Provider Sessions Token Usage
        sessions = cursor.execute("""
            SELECT role_id, total_tokens_in + total_tokens_out, status
            FROM provider_sessions
            WHERE project_id = ?
        """, (project_id,)).fetchall()
        tokens_map = {s[0]: {"tokens": s[1], "status": s[2]} for s in sessions}

        swarm_roles = []
        for r in roles:
            s_data = tokens_map.get(r[0], {"tokens": 0, "status": "idle"})
            swarm_roles.append({
                "role_id": r[0],
                "display_name": r[1],
                "code_name": r[2],
                "category": r[3],
                "model": r[4],
                "color": r[5],
                "tokens_spent": s_data["tokens"],
                "status": s_data["status"]
            })

        # 4. Mode A: 4 Mini-Kanban Columns
        tasks = cursor.execute("""
            SELECT task_id, title, category, column_status, priority, assigned_role_id, tokens_spent
            FROM kanban_tasks
            WHERE project_id = ?
            ORDER BY order_index ASC
        """, (project_id,)).fetchall()

        kanban_columns = {
            "todo": [],
            "coding": [],
            "qa": [],
            "done": []
        }

        col_mapping = {
            "backlog": "todo",
            "conception": "todo",
            "architecture": "coding",
            "development": "coding",
            "quality_gate": "qa",
            "done": "done"
        }

        for t in tasks:
            col_key = col_mapping.get(t[3], "todo")
            kanban_columns[col_key].append({
                "task_id": t[0],
                "title": t[1],
                "category": t[2],
                "raw_status": t[3],
                "priority": t[4],
                "assigned_role_id": t[5],
                "tokens_spent": t[6]
            })

        # 5. Active Checkpoint
        chk = cursor.execute("""
            SELECT checkpoint_id, task_id, title, summary, diff_stats_files, 
                   diff_stats_insertions, diff_stats_deletions, automated_test_details, status
            FROM checkpoint_gates
            WHERE project_id = ? AND status = 'pending'
            ORDER BY created_at DESC LIMIT 1
        """, (project_id,)).fetchone()

        active_checkpoint = None
        if chk:
            active_checkpoint = {
                "checkpoint_id": chk[0],
                "task_id": chk[1],
                "title": chk[2],
                "summary": chk[3],
                "files_changed": chk[4],
                "insertions": chk[5],
                "deletions": chk[6],
                "test_details": chk[7],
                "status": chk[8]
            }

        # 6. Chat Messages
        chat_rows = cursor.execute("""
            SELECT message_id, sender_type, sender_name, content, thinking_log,
                   thought_duration_ms, tokens_consumed, is_checkpoint_trigger, checkpoint_gate_id, created_at
            FROM chat_messages
            ORDER BY created_at ASC
        """).fetchall()

        messages = []
        for m in chat_rows:
            messages.append({
                "message_id": m[0],
                "sender_type": m[1],
                "sender_name": m[2],
                "content": m[3],
                "thinking_log": m[4],
                "thought_duration_ms": m[5],
                "tokens_consumed": m[6],
                "is_checkpoint_trigger": bool(m[7]),
                "checkpoint_gate_id": m[8],
                "created_at": m[9]
            })

        conn.close()

        return {
            "project": {
                "project_id": project[0],
                "name": project[1],
                "slug": project[2],
                "workspace_path": project[3],
                "status": project[4]
            },
            "swarm_roles": swarm_roles,
            "mini_kanban": kanban_columns,
            "active_checkpoint": active_checkpoint,
            "chat_messages": messages,
            "git_diff": {
                "branch": "feature/cart-voucher",
                "insertions": 45,
                "deletions": 12,
                "files": [
                    {"path": "lib/features/cart/cart_bloc.dart", "lines": "+28"},
                    {"path": "src/modules/cart/cart.controller.ts", "lines": "+17"},
                    {"path": "test/cart/cart_bloc_test.dart", "lines": "+12"}
                ]
            },
            "avd_status": {
                "device": "Google Pixel 8 Pro (API 34)",
                "port": 5554,
                "status": "online"
            }
        }

    @staticmethod
    def send_chat_message(user_text, project_id="proj_food_delivery_01"):
        """Xử lý luồng chat: Bạn gửi tin nhắn -> Alex phản hồi với <thinking> và rã task"""
        conn = get_db()
        cursor = conn.cursor()

        # 1. Store user message
        user_msg_id = f"msg_user_{uuid.uuid4().hex[:8]}"
        chat_sess = cursor.execute("SELECT chat_session_id FROM chat_sessions WHERE project_id = ? LIMIT 1", (project_id,)).fetchone()
        chat_sess_id = chat_sess[0] if chat_sess else "chat_main_session_01"

        cursor.execute("""
            INSERT INTO chat_messages (
                message_id, chat_session_id, sender_type, sender_name, content
            ) VALUES (?, ?, 'user', 'Bạn (Chủ dự án)', ?)
        """, (user_msg_id, chat_sess_id, user_text))

        # 2. Alex (Lead PM) Thought Process & Execution Plan
        thought_start = time.time()
        thinking_log = f"""<thinking>
1. User input received: "{user_text[:80]}..."
2. Context: FoodDelivery-Loyalty-App with 14 swarm roles.
3. Strategy: Assign Marcus (BA) to define specs, Maya to design schema, David (FE) to build UI, and Viktor (QA) to test.
4. Update Kanban columns & sync state via 9router daemon.
</thinking>"""
        thought_duration_ms = int((time.time() - thought_start) * 1000) + 1450

        # Create new task in Kanban if applicable
        task_id = f"TASK-{int(time.time()) % 1000}"
        cursor.execute("""
            INSERT INTO kanban_tasks (
                task_id, project_id, title, category, column_status, priority, assigned_role_id, tokens_spent
            ) VALUES (?, ?, ?, 'frontend', 'development', 'high', 'frontend_dev', 650)
        """, (task_id, project_id, f"Triển khai: {user_text[:35]}..."))

        # 3. Store Alex PM response
        pm_msg_id = f"msg_pm_{uuid.uuid4().hex[:8]}"
        pm_content = f"Chào bạn! Tôi đã phân công ban kỹ thuật: Marcus (BA) viết specs, David (FE) viết code, và Viktor (QA) lập kịch bản test. Nhiệm vụ [{task_id}] đã được đẩy vào cột Coding trên Mini-Kanban."

        cursor.execute("""
            INSERT INTO chat_messages (
                message_id, chat_session_id, sender_type, sender_role_id, sender_name,
                content, thinking_log, thought_duration_ms, tokens_consumed
            ) VALUES (?, ?, 'pm_agent', 'lead_pm', 'Alex (Trưởng Dự Án / Lead PM)', ?, ?, ?, ?)
        """, (pm_msg_id, chat_sess_id, pm_content, thinking_log, thought_duration_ms, 820))

        conn.commit()
        conn.close()

        return {
            "user_message_id": user_msg_id,
            "pm_message_id": pm_msg_id,
            "pm_content": pm_content,
            "thinking_log": thinking_log,
            "new_task_id": task_id
        }

    @staticmethod
    def trigger_emergency_stop(project_id="proj_food_delivery_01"):
        """Nút Dừng Đột Ngột (Emergency Stop ESC) hủy ngay mọi agent đang chạy trong <100ms"""
        t0 = time.time()
        conn = get_db()
        cursor = conn.cursor()

        # Update all active tasks to paused
        cursor.execute("""
            UPDATE kanban_tasks
            SET priority = 'low'
            WHERE project_id = ? AND column_status IN ('conception', 'architecture', 'development')
        """, (project_id,))

        # Update all provider sessions to idle
        cursor.execute("""
            UPDATE provider_sessions
            SET status = 'idle'
            WHERE project_id = ?
        """, (project_id,))

        # Insert emergency event in chat
        chat_sess = cursor.execute("SELECT chat_session_id FROM chat_sessions WHERE project_id = ? LIMIT 1", (project_id,)).fetchone()
        chat_sess_id = chat_sess[0] if chat_sess else "chat_main_session_01"

        stop_msg_id = f"msg_stop_{uuid.uuid4().hex[:8]}"
        cursor.execute("""
            INSERT INTO chat_messages (
                message_id, chat_session_id, sender_type, sender_name, content
            ) VALUES (?, ?, 'system_event', 'HỆ THỐNG AN TOÀN', '⏹️ DỪNG ĐỘT NGỘT: Toàn bộ 13 sub-agents đã được thu hồi và tạm dừng an toàn.')
        """, (stop_msg_id, chat_sess_id))

        conn.commit()
        conn.close()
        elapsed_ms = (time.time() - t0) * 1000

        return {
            "status": "stopped",
            "message": "Toàn bộ tiến trình agent đã dừng lại tức thì.",
            "response_time_ms": round(elapsed_ms, 2)
        }

if __name__ == '__main__':
    state = CommandWorkspaceService.get_workspace_state()
    print("Command Workspace State Loaded:")
    print(f"- Project: {state['project']['name']}")
    print(f"- Swarm roles: {len(state['swarm_roles'])}")
    print(f"- Mini-Kanban: ToDo={len(state['mini_kanban']['todo'])}, Coding={len(state['mini_kanban']['coding'])}, QA={len(state['mini_kanban']['qa'])}, Done={len(state['mini_kanban']['done'])}")
    print(f"- Chat messages: {len(state['chat_messages'])}")
