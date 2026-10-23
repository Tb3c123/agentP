"""
agentP - Sprint 5 Unit Tests: DevOps, AVD Manager, Remote Controller & Excel Reports
Author: Viktor (QA Lead) & Oliver (Perf)
"""

import unittest
import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'controllers'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'services'))

from dispatcher import RequestDispatcher
from avd_controller import AvdControllerService
from remote_controller import MobileRemoteService
from excel_reporter import ExcelCorporateReporter

class TestSprint5DevOpsReports(unittest.TestCase):

    def test_01_avd_status(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/devops/avd/status')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["device_name"], "Pixel_8_Pro_API_34")
        self.assertEqual(data["adb_port"], 5554)
        self.assertEqual(data["status"], "connected")
        self.assertIn("render_latency_ms", data)

    def test_02_avd_launch(self):
        status, headers, body = RequestDispatcher.dispatch_post('/api/devops/avd/launch', {"mode": "gui"})
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertTrue(data["success"])
        self.assertEqual(data["action"], "launch")

    def test_03_avd_hot_reload(self):
        status, headers, body = RequestDispatcher.dispatch_post('/api/devops/avd/reload', {})
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertTrue(data["success"])
        self.assertIn("latency_ms", data)

    def test_04_avd_screenshot(self):
        status, headers, body = RequestDispatcher.dispatch_post('/api/devops/avd/screenshot', {})
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertTrue(data["success"])
        self.assertIn("avd_screenshot_", data["screenshot_filename"])

    def test_05_remote_pairing_info(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/remote/pairing-info')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["status"], "online")
        self.assertEqual(data["websocket_port"], 8080)
        self.assertIn("pairing_code", data)
        self.assertIn("qr_data_url", data)

    def test_06_excel_acceptance_report(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/reports/excel/export')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["project_name"], "FoodDelivery-Loyalty-App")
        self.assertEqual(data["tokens_saved"], 42500)
        self.assertEqual(data["test_pass_rate"], "100%")
        self.assertIn("report_path", data)
        self.assertTrue(os.path.exists(os.path.join(BASE_DIR, data["report_path"])))

    def test_07_preflight_diagnostics(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/preflight/status')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["total_count"], 7)
        self.assertEqual(data["passed_count"], 7)
        self.assertEqual(data["percentage"], 100)
        self.assertEqual(len(data["checks"]), 7)

    def test_08_protocol_test_connections(self):
        status, headers, body = RequestDispatcher.dispatch_post('/api/protocol/test-connection', {})
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["sessions"]), 14)
        for s in data["sessions"]:
            self.assertGreater(s["latency_ms"], 0)
            self.assertEqual(s["status"], "connected")


if __name__ == '__main__':
    unittest.main()
