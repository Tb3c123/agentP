import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'daemon'))
from router import AgentPCoreDaemonService

class TestAgentPProtocol(unittest.TestCase):
    def test_01_health_endpoint(self):
        """Kiểm tra logic /health trả về trạng thái lành mạnh và 14 roles/sessions"""
        data = AgentPCoreDaemonService.get_health()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["active_roles"], 14)
        self.assertEqual(data["isolated_sessions"], 14)
        self.assertEqual(data["db_status"], "connected")
        self.assertEqual(data["service"], "agentp-core-daemon")

    def test_02_sessions_endpoint(self):
        """Kiểm tra logic /sessions trả về danh sách 14 phiên cô lập 1:1"""
        data = AgentPCoreDaemonService.get_sessions()
        self.assertEqual(data["total"], 14)
        role_ids = {s["role_id"] for s in data["sessions"]}
        self.assertIn("lead_pm", role_ids)
        self.assertIn("qa_lead", role_ids)
        self.assertIn("frontend_dev", role_ids)
        self.assertIn("system_architect", role_ids)

    def test_03_chat_completions_with_thinking_stream(self):
        """Kiểm tra xử lý prompt và trích xuất raw thinking log cho Claude và DeepSeek"""
        # Test 1: Lead PM (Claude 3.5 Sonnet) -> should have <thinking>
        res_pm = AgentPCoreDaemonService.chat_completions(
            role_id="lead_pm",
            prompt="Khởi tạo Sprint 1 và cấu hình agentP core daemon",
            task_id="TASK-102"
        )
        self.assertEqual(res_pm["role_id"], "lead_pm")
        self.assertIn("<thinking>", res_pm["thinking_log"])
        self.assertGreater(res_pm["tokens_consumed"], 0)

        # Test 2: QA Lead (DeepSeek R1) -> should have <reasoning_content>
        res_qa = AgentPCoreDaemonService.chat_completions(
            role_id="qa_lead",
            prompt="Kiểm tra toàn bộ test suites của Sprint 1",
            task_id="TASK-103"
        )
        self.assertEqual(res_qa["role_id"], "qa_lead")
        self.assertIn("<reasoning_content>", res_qa["thinking_log"])

        # Test 3: Frontend Dev (Gemini 2.5 Flash) -> should have <thought>
        res_fe = AgentPCoreDaemonService.chat_completions(
            role_id="frontend_dev",
            prompt="Thiết kế UI Clean Light Mode cho AgentP",
            task_id="TASK-101"
        )
        self.assertEqual(res_fe["role_id"], "frontend_dev")
        self.assertIn("<thought>", res_fe["thinking_log"])

    def test_04_token_accounting(self):
        """Kiểm tra việc tích lũy tokens và tính toán số token tiết kiệm"""
        tokens_data = AgentPCoreDaemonService.get_tokens()
        self.assertIn("total_tokens_spent", tokens_data)
        self.assertIn("total_tokens_saved", tokens_data)
        self.assertGreaterEqual(tokens_data["total_tokens_saved"], 0)

    def test_05_kanban_sync_trigger(self):
        """Kiểm tra truy vấn danh sách task kanban từ CSDL SQLite"""
        kanban_data = AgentPCoreDaemonService.get_kanban()
        self.assertIn("tasks", kanban_data)
        self.assertGreater(len(kanban_data["tasks"]), 0)

    def test_06_checkpoint_approval(self):
        """Kiểm tra giải quyết Checkpoint Gate và tự động cập nhật task Kanban"""
        res = AgentPCoreDaemonService.resolve_checkpoint(
            checkpoint_id="CHK-01",
            action="approved",
            feedback="Phê duyệt kiến trúc Lõi agentP Core Daemon."
        )
        self.assertEqual(res["status"], "approved")
        self.assertEqual(res["checkpoint_id"], "CHK-01")

if __name__ == '__main__':
    unittest.main()
