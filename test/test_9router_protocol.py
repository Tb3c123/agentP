import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'daemon'))
from router import NineRouterService

class TestNineRouterProtocol(unittest.TestCase):
    def test_01_health_endpoint(self):
        """Kiểm tra logic /health trả về trạng thái lành mạnh và 14 roles/sessions"""
        data = NineRouterService.get_health()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["active_roles"], 14)
        self.assertEqual(data["isolated_sessions"], 14)
        self.assertEqual(data["db_status"], "connected")
        self.assertEqual(data["service"], "9router-daemon")

    def test_02_sessions_endpoint(self):
        """Kiểm tra logic /sessions trả về danh sách 14 phiên cô lập 1:1"""
        data = NineRouterService.get_sessions()
        self.assertEqual(data["total"], 14)
        role_ids = {s["role_id"] for s in data["sessions"]}
        self.assertIn("lead_pm", role_ids)
        self.assertIn("qa_lead", role_ids)
        self.assertIn("frontend_dev", role_ids)
        self.assertIn("system_architect", role_ids)

    def test_03_chat_completions_with_thinking_stream(self):
        """Kiểm tra xử lý prompt và trích xuất raw thinking log cho Claude và DeepSeek"""
        # Test 1: Lead PM (Claude 3.5 Sonnet) -> should have <thinking>
        res_pm = NineRouterService.chat_completions(
            role_id="lead_pm",
            prompt="Khởi tạo Sprint 1 và cấu hình 9router daemon",
            task_id="TASK-102"
        )
        self.assertEqual(res_pm["role_id"], "lead_pm")
        self.assertIn("<thinking>", res_pm["thinking_log"])
        self.assertGreater(res_pm["tokens_consumed"], 0)

        # Test 2: QA Lead (DeepSeek R1) -> should have <reasoning_content>
        res_qa = NineRouterService.chat_completions(
            role_id="qa_lead",
            prompt="Kiểm tra toàn bộ test suites của Sprint 1",
            task_id="TASK-103"
        )
        self.assertEqual(res_qa["role_id"], "qa_lead")
        self.assertIn("<reasoning_content>", res_qa["thinking_log"])

        # Test 3: Frontend Dev (Gemini 2.5 Flash) -> should have <thought>
        res_fe = NineRouterService.chat_completions(
            role_id="frontend_dev",
            prompt="Dựng khung Onboarding Launchpad",
            task_id="TASK-104"
        )
        self.assertEqual(res_fe["role_id"], "frontend_dev")
        self.assertIn("<thought>", res_fe["thinking_log"])

    def test_04_token_metrics_endpoint(self):
        """Kiểm tra logic /tokens ghi nhận thống kê token chính xác"""
        data = NineRouterService.get_tokens()
        self.assertIn("total_tokens_spent", data)
        self.assertIn("total_tokens_saved", data)
        self.assertGreaterEqual(data["total_tokens_spent"], 0)

    def test_05_kanban_endpoint(self):
        """Kiểm tra logic /kanban trả về danh sách task Kanban"""
        data = NineRouterService.get_kanban()
        self.assertIn("tasks", data)
        self.assertGreaterEqual(len(data["tasks"]), 4)

if __name__ == '__main__':
    unittest.main()
