"""
agentP - Sprint 6 Unit Tests: 9router In-House Core Engine & Multi-Provider Dynamic Proxy
Tests CLI Bridge, dynamic proxy routing (/v1/messages, /v1/chat/completions), failover & SQLite config.
Author: Viktor (QA Lead) & Lucas (Senior Dev)
"""

import unittest
import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'controllers'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'services'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src', 'repositories'))

from dispatcher import RequestDispatcher
from providers_repo import ProvidersRepository
from cli_bridge import CliBridgeService
from provider_proxy import ProviderProxyService

class TestSprint6ProxyBridge(unittest.TestCase):

    def setUp(self):
        ProvidersRepository.ensure_table()

    def test_01_providers_hub_get(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/providers/hub')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("categories", data)
        self.assertIn("oauth", data["categories"])
        self.assertIn("free", data["categories"])
        self.assertIn("api", data["categories"])
        self.assertIn("compat", data["categories"])
        self.assertGreaterEqual(data["total_providers"], 12)
        self.assertIn("In-House 9router Core", data["architecture"])

    def test_02_update_provider_config(self):
        payload = {
            "provider_id": "deepseek",
            "api_key": "sk-deepseek-test-key-12345",
            "base_url": "https://api.deepseek.com/v1",
            "is_enabled": 1
        }
        status, headers, body = RequestDispatcher.dispatch_post('/api/providers/config', payload)
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertTrue(data["success"])

        # Verify persistence in SQLite WAL
        prov = ProvidersRepository.get_by_id("deepseek")
        self.assertIsNotNone(prov)
        self.assertEqual(prov["api_key"], "sk-deepseek-test-key-12345")
        self.assertEqual(prov["status"], "connected")

    def test_03_test_single_and_all_providers(self):
        # Single test
        status, headers, body = RequestDispatcher.dispatch_post('/api/providers/test', {"provider_id": "openrouter"})
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["provider_id"], "openrouter")
        self.assertGreater(data["latency_ms"], 0)

        # Category test
        status, headers, body = RequestDispatcher.dispatch_post('/api/providers/test', {"category": "oauth"})
        self.assertEqual(status, 200)
        cat_data = json.loads(body.decode('utf-8'))
        self.assertEqual(cat_data["tested_category"], "oauth")

    def test_04_cli_bridge_detection(self):
        status, headers, body = RequestDispatcher.dispatch_get('/api/cli-bridge/status')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("tools", data)
        self.assertIn("claude_code", data["tools"])
        self.assertIn("cursor", data["tools"])
        self.assertEqual(data["proxy_endpoint"], "http://127.0.0.1:9090")

    def test_05_cli_bridge_generate_scripts(self):
        status, headers, body = RequestDispatcher.dispatch_post('/api/cli-bridge/generate-config', {})
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["status"], "generated")
        self.assertIn("files", data)
        self.assertTrue(os.path.exists(data["files"]["shell_script"]))
        self.assertTrue(os.path.exists(data["files"]["cursor_config"]))

        # Verify shell script contents
        with open(data["files"]["shell_script"], "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("ANTHROPIC_BASE_URL", content)
            self.assertIn("OPENAI_BASE_URL", content)
            self.assertIn("9090", content)

    def test_06_openai_chat_completions_proxy(self):
        payload = {
            "model": "deepseek-r1",
            "messages": [
                {"role": "user", "content": "Tạo module tích điểm đổi quà"}
            ],
            "temperature": 0.5
        }
        status, headers, body = RequestDispatcher.dispatch_post('/v1/chat/completions', payload)
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["object"], "chat.completion")
        self.assertEqual(data["model"], "deepseek-r1")
        self.assertIn("choices", data)
        self.assertEqual(len(data["choices"]), 1)
        self.assertIn("reasoning_content", data["choices"][0]["message"])
        self.assertTrue(data["agentp_proxy"]["zero_external_dependency"])

    def test_07_anthropic_messages_proxy(self):
        payload = {
            "model": "claude-3-7-sonnet",
            "messages": [
                {"role": "user", "content": "Viết hàm test coverage cho SQLite WAL"}
            ]
        }
        status, headers, body = RequestDispatcher.dispatch_post('/v1/messages', payload)
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["type"], "message")
        self.assertEqual(data["model"], "claude-3-7-sonnet")
        self.assertIn("content", data)
        self.assertEqual(data["content"][0]["type"], "text")
        self.assertTrue(data["agentp_proxy"]["zero_external_dependency"])

    def test_08_dynamic_failover_mechanism(self):
        # Targeting disconnected model / disabled provider triggers failover
        payload = {
            "model": "cerebras-unsupported-model-99",
            "messages": [
                {"role": "user", "content": "Kiểm tra chế độ dự phòng fallback"}
            ]
        }
        status, headers, body = RequestDispatcher.dispatch_post('/v1/chat/completions', payload)
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertTrue(data["agentp_proxy"]["failover_applied"])
        self.assertIn("Failover", data["agentp_proxy"]["routed_provider"])

if __name__ == '__main__':
    unittest.main()
