import unittest
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'services'))
from auto_namer import generate_project_names
from command_workspace import CommandWorkspaceService

class TestSprint2Features(unittest.TestCase):
    def test_01_auto_namer_food_delivery(self):
        """Kiểm tra thuật toán sinh tên tự động từ mô tả đồ ăn & voucher"""
        desc = "Ứng dụng đặt đồ ăn trên Android và Web bằng Flutter & NestJS, có giỏ hàng, tích điểm voucher và thanh toán QR."
        res = generate_project_names(desc)
        self.assertEqual(res["primary"], "FoodDelivery-Loyalty-App")
        self.assertIn("FoodDelivery", res["detected_domains"])
        self.assertIn("Loyalty", res["detected_domains"])
        self.assertIn("Flutter", res["detected_tech"])
        self.assertEqual(res["suggested_path"], "~/Projects/FoodDelivery-Loyalty-App")

    def test_02_auto_namer_ecommerce(self):
        """Kiểm tra sinh tên dự án sàn thương mại điện tử"""
        desc = "Xây dựng shop thương mại điện tử bán hàng trực tuyến tích hợp thanh toán ví điện tử"
        res = generate_project_names(desc)
        self.assertEqual(res["primary"], "ECommerce-Payment-App")

    def test_03_workspace_state_structure(self):
        """Kiểm tra cấu trúc dữ liệu trả về cho Bàn làm việc điều hành"""
        state = CommandWorkspaceService.get_workspace_state()
        self.assertIn("project", state)
        self.assertIn("swarm_roles", state)
        self.assertEqual(len(state["swarm_roles"]), 14)
        self.assertIn("mini_kanban", state)
        self.assertIn("todo", state["mini_kanban"])
        self.assertIn("coding", state["mini_kanban"])
        self.assertIn("qa", state["mini_kanban"])
        self.assertIn("done", state["mini_kanban"])
        self.assertIn("git_diff", state)
        self.assertIn("avd_status", state)

    def test_04_chat_message_flow_with_thinking(self):
        """Kiểm tra luồng chat: Bạn gửi chỉ thị -> Alex phản hồi với <thinking> và tạo task"""
        user_prompt = "Hãy thiết kế module tích điểm đổi quà thành viên"
        res = CommandWorkspaceService.send_chat_message(user_prompt)
        self.assertIn("user_message_id", res)
        self.assertIn("pm_message_id", res)
        self.assertIn("<thinking>", res["thinking_log"])
        self.assertIn("TASK-", res["new_task_id"])

    def test_05_emergency_stop_performance(self):
        """Kiểm tra nút Dừng Đột Ngột (Emergency Stop) phản hồi dưới 100ms"""
        res = CommandWorkspaceService.trigger_emergency_stop()
        self.assertEqual(res["status"], "stopped")
        self.assertLess(res["response_time_ms"], 100.0, "Thời gian phản hồi dừng khẩn cấp phải dưới 100ms")

if __name__ == '__main__':
    unittest.main()
