"""
agentP - UI Visual & Layout Auditor Unit Test
Validates that Zoe's automated UI inspector successfully checks CSS flex directions,
header widths, and grid containers, and detects simulated regressions.
Author: Viktor (QA Lead) & Zoe (UI Tester)
"""

import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts'))

from ui_tester_auditor import UiTesterAuditor

class TestUiVisualAuditor(unittest.TestCase):

    def setUp(self):
        self.auditor = UiTesterAuditor()

    def test_01_run_full_audit(self):
        report = self.auditor.audit_all()
        self.assertEqual(report["status"], "PASSED")
        self.assertEqual(report["defects_count"], 0)
        self.assertGreaterEqual(report["total_inspections"], 5)

    def test_02_detect_missing_flex_column_regression(self):
        # Simulate bad CSS missing flex-direction: column
        bad_css = ".personnel-view { display: flex; }"
        self.auditor.defects = []
        self.auditor.inspections = []
        self.auditor._audit_view_panels_flex_direction(bad_css, "<html></html>")
        self.assertTrue(any(d["target"] == ".personnel-view" for d in self.auditor.defects))
        self.assertEqual(self.auditor.defects[0]["severity"], "CRITICAL")

    def test_03_detect_missing_columns_layout(self):
        # Simulate HTML missing providers-hub-columns-layout
        bad_html = "<section id='viewProvidersHub'><div>Bad</div></section>"
        self.auditor.defects = []
        self.auditor.inspections = []
        self.auditor._audit_providers_hub_layout(bad_html, ".providers-hub-columns-layout {}")
        self.assertTrue(any(d["target"] == "#viewProvidersHub" for d in self.auditor.defects))

if __name__ == '__main__':
    unittest.main()
