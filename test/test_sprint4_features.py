"""
Unit & Integration Test Suite for Sprint 4
Covers:
1. File Explorer tree building and Agent Role ownership mapping.
2. Safe Trash deletion to .agents/trash/ and file restoration.
3. Monaco Side-by-Side Split Diff calculation.
4. Antigravity Danger Zone strict 2-factor project name confirmation lock.
5. Project Hub configuration and environment variables retrieval.
"""

import unittest
import os
import shutil
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "services")))
import project_manager as pm

class TestSprint4Features(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sample_file = os.path.join(self.test_dir, "sample_component.tsx")
        with open(self.sample_file, "w") as f:
            f.write("export const Test = () => <div>Hello Sprint 4</div>;")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_agent_role_file_mapping(self):
        """Verifies each file type is correctly mapped to its designated specialist agent."""
        fe_agent = pm.get_agent_for_file("lib/cart_button.tsx")
        self.assertEqual(fe_agent["role_id"], "david_fe")
        self.assertEqual(fe_agent["name"], "David")

        ui_agent = pm.get_agent_for_file("styles/theme.css")
        self.assertEqual(ui_agent["role_id"], "elena_uiux")

        be_agent = pm.get_agent_for_file("src/api/auth.py")
        self.assertEqual(be_agent["role_id"], "carlos_be")

        mobile_agent = pm.get_agent_for_file("lib/main.dart")
        self.assertEqual(mobile_agent["role_id"], "lucas_senior")

        qa_agent = pm.get_agent_for_file("test/test_security.py")
        self.assertEqual(qa_agent["role_id"], "viktor_qa")

        doc_agent = pm.get_agent_for_file("docs/SPEC.md")
        self.assertEqual(doc_agent["role_id"], "marcus_ba")

    def test_02_file_tree_generation(self):
        """Verifies hierarchical file tree generation with sizes and agent tags."""
        tree = pm.build_file_tree(max_depth=2)
        self.assertIn("name", tree)
        self.assertTrue(tree["is_dir"])
        self.assertGreater(len(tree["children"]), 0)

    def test_03_monaco_split_diff_computation(self):
        """Verifies side-by-side split diff engine creates accurate diff metrics."""
        diff = pm.compute_monaco_split_diff("lib/features/cart/cart_button.tsx")
        self.assertIn("old_content", diff)
        self.assertIn("new_content", diff)
        self.assertGreater(diff["lines_added"], 0)
        self.assertGreaterEqual(diff["lines_deleted"], 1)

    def test_04_antigravity_danger_zone_security_lock(self):
        """
        Antigravity Security Test (Viktor & Nora):
        Ensures deletion is 100% locked if confirmation is incorrect by even 1 character.
        """
        # 1. Wrong name -> Strictly blocked
        res_wrong = pm.verify_antigravity_danger_zone("proj_food_delivery", "FoodDelivery-Loyalty")
        self.assertFalse(res_wrong["allowed"])
        self.assertIn("mismatch", res_wrong["error"].lower())

        # 2. Case mismatch -> Strictly blocked
        res_case = pm.verify_antigravity_danger_zone("proj_food_delivery", "fooddelivery-loyalty-app")
        self.assertFalse(res_case["allowed"])

        # 3. Extra character -> Strictly blocked
        res_extra = pm.verify_antigravity_danger_zone("proj_food_delivery", "FoodDelivery-Loyalty-App!")
        self.assertFalse(res_extra["allowed"])

        # 4. Exact match -> Unlocked!
        res_exact = pm.verify_antigravity_danger_zone("proj_food_delivery", "FoodDelivery-Loyalty-App")
        self.assertTrue(res_exact["allowed"])
        self.assertIn("unlocked", res_exact["message"].lower())

    def test_05_safe_trash_workflow(self):
        """Tests moving a file to .agents/trash/ and un-deleting it safely."""
        test_file_rel = "test_trash_sample.txt"
        test_file_abs = os.path.join(pm.WORKSPACE_DIR, test_file_rel)
        with open(test_file_abs, "w") as f:
            f.write("Important business data that must never be lost directly.")

        # Delete safely
        del_res = pm.safe_delete_file(test_file_rel)
        self.assertTrue(del_res["success"])
        self.assertFalse(os.path.exists(test_file_abs))
        trash_id = del_res["trash_id"]

        # Check in trash list
        trash_list = pm.list_trash_files()
        found = any(t.get("trash_id") == trash_id for t in trash_list)
        self.assertTrue(found)

        # Restore from trash
        restore_res = pm.restore_trash_file(trash_id)
        self.assertTrue(restore_res["success"])
        self.assertTrue(os.path.exists(test_file_abs))

        # Cleanup
        if os.path.exists(test_file_abs):
            os.remove(test_file_abs)

if __name__ == "__main__":
    unittest.main()
