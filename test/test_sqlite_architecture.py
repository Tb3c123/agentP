import unittest
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '.agents', 'db.sqlite')

class TestSQLiteArchitecture(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_01_wal_mode_enabled(self):
        """Kiểm tra chế độ Write-Ahead Logging (WAL) đang bật"""
        mode = self.cursor.execute("PRAGMA journal_mode;").fetchone()[0]
        self.assertEqual(mode.lower(), "wal", "SQLite phải chạy ở chế độ WAL")

    def test_02_all_12_tables_exist(self):
        """Kiểm tra sự tồn tại của đầy đủ 12 bảng chính và bảng migration"""
        expected_tables = {
            'schema_migrations', 'projects', 'project_env_vars', 'agent_roles',
            'provider_sessions', 'chat_sessions', 'chat_messages', 'sprints',
            'kanban_tasks', 'task_subtasks', 'checkpoint_gates', 'audit_git_commits',
            'ui_design_snapshots'
        }
        rows = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        actual_tables = {r[0] for r in rows}
        missing = expected_tables - actual_tables
        self.assertEqual(len(missing), 0, f"Thiếu các bảng: {missing}")

    def test_03_fourteen_roles_seeded(self):
        """Kiểm tra 14 vai trò kỹ thuật đã được nạp đầy đủ"""
        count = self.cursor.execute("SELECT COUNT(*) FROM agent_roles;").fetchone()[0]
        self.assertEqual(count, 14, "Phải có đúng 14 agent roles trong database")

    def test_04_fourteen_provider_sessions_isolated(self):
        """Kiểm tra 14 phiên kết nối 1:1 độc lập cho 14 roles"""
        count = self.cursor.execute("SELECT COUNT(*) FROM provider_sessions;").fetchone()[0]
        self.assertEqual(count, 14, "Phải có đúng 14 provider sessions độc lập")

    def test_05_foreign_key_enforcement(self):
        """Kiểm tra ràng buộc khóa ngoại (Foreign Key) ngăn chặn dữ liệu rác"""
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("""
            INSERT INTO kanban_tasks (
                task_id, project_id, title, category, column_status, priority, assigned_role_id
            ) VALUES ('TASK-ERR', 'non_existent_project', 'Invalid Task', 'frontend', 'backlog', 'low', 'lead_pm');
            """)

    def test_06_checkpoint_approval_trigger(self):
        """Kiểm tra trigger trg_checkpoint_approved_to_done tự động cập nhật Kanban task sang 'done'"""
        # Tạo 1 task thử nghiệm ở cột quality_gate
        test_task_id = "TASK-TEST-TRIGGER"
        self.cursor.execute("""
        INSERT OR REPLACE INTO kanban_tasks (
            task_id, project_id, title, category, column_status, priority, assigned_role_id
        ) VALUES (?, 'proj_food_delivery_01', 'Test Trigger Task', 'qa', 'quality_gate', 'high', 'qa_lead');
        """, (test_task_id,))

        # Tạo checkpoint liên kết với task
        chk_id = "CHK-TEST-01"
        self.cursor.execute("""
        INSERT OR REPLACE INTO checkpoint_gates (
            checkpoint_id, project_id, task_id, title, summary, automated_test_passed, status
        ) VALUES (?, 'proj_food_delivery_01', ?, 'Test Checkpoint', 'Summary', 1, 'pending');
        """, (chk_id, test_task_id))
        self.conn.commit()

        # Xác minh ban đầu task ở cột quality_gate
        status_before = self.cursor.execute("SELECT column_status FROM kanban_tasks WHERE task_id = ?", (test_task_id,)).fetchone()[0]
        self.assertEqual(status_before, "quality_gate")

        # Cập nhật checkpoint sang 'approved'
        self.cursor.execute("UPDATE checkpoint_gates SET status = 'approved' WHERE checkpoint_id = ?", (chk_id,))
        self.conn.commit()

        # Kiểm tra task đã được trigger tự động nhảy sang 'done'
        status_after = self.cursor.execute("SELECT column_status FROM kanban_tasks WHERE task_id = ?", (test_task_id,)).fetchone()[0]
        self.assertEqual(status_after, "done", "Trigger phải tự động chuyển task sang cột 'done' khi checkpoint được duyệt")

        # Dọn dẹp dữ liệu test
        self.cursor.execute("DELETE FROM checkpoint_gates WHERE checkpoint_id = ?", (chk_id,))
        self.cursor.execute("DELETE FROM kanban_tasks WHERE task_id = ?", (test_task_id,))
        self.conn.commit()

if __name__ == '__main__':
    unittest.main()
