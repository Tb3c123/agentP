import unittest
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'services'))
from ast_sync import AstSyncEngine

class TestSprint3Features(unittest.TestCase):
    def test_01_ast_sync_dom_to_code(self):
        """Kiểm tra đồng bộ Onlook DOM sang code thật đạt độ trễ <50ms"""
        test_file = "lib/features/cart/test_sync_button.tsx"
        new_classes = "bg-teal-600 hover:bg-teal-700 text-white font-bold py-3 px-6 rounded-lg shadow-sm"
        
        res = AstSyncEngine.sync_dom_to_code(
            file_path=test_file,
            component_tag="TestCheckoutButton",
            new_classes=new_classes
        )

        self.assertEqual(res["status"], "synced")
        self.assertEqual(res["new_classes"], new_classes)
        self.assertLess(res["latency_ms"], 50.0, "Độ trễ ghi AST vào file phải dưới 50ms")

        # Verify file content
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', test_file))
        self.assertTrue(os.path.exists(abs_path))
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn(new_classes, content)

        # Cleanup test file
        if os.path.exists(abs_path):
            os.remove(abs_path)

    def test_02_save_tldraw_snapshot(self):
        """Kiểm tra xuất và lưu snapshot bản vẽ Tldraw (.tldr)"""
        canvas_data = {
            "version": 1,
            "title": "Test Wireframe Board",
            "elements": [
                {"id": "box_1", "type": "wireframe", "title": "Cart View"},
                {"id": "note_1", "type": "note", "text": "Elena UI note"}
            ]
        }
        res = AstSyncEngine.save_tldraw_snapshot(
            project_id="proj_food_delivery_01",
            title="Cart Wireframe Concept",
            canvas_data=canvas_data
        )

        self.assertIn("snapshot_id", res)
        self.assertTrue(os.path.exists(res["file_path"]))
        self.assertEqual(res["elements_count"], 2)

        # Verify JSON
        with open(res["file_path"], 'r') as f:
            saved_json = json.load(f)
        self.assertEqual(saved_json["title"], "Test Wireframe Board")

    def test_03_get_snapshots_from_sqlite(self):
        """Kiểm tra truy vấn lịch sử snapshot thiết kế từ CSDL SQLite"""
        snapshots = AstSyncEngine.get_snapshots("proj_food_delivery_01")
        self.assertGreater(len(snapshots), 0)
        first = snapshots[0]
        self.assertIn("snapshot_id", first)
        self.assertIn("studio_mode", first)
        self.assertTrue(first["synced_to_code"])

if __name__ == '__main__':
    unittest.main()
