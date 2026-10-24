"""
agentP - Sprint 7 Unit Tests: Dynamic Agent Summoning, Real-Time Event Bus & Swarm Runner
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
from pubsub_bus import EventPubSubBus
from summoning_service import DynamicSummoningService
from token_guard import TokenConsumptionGuard
from swarm_runner import SwarmExecutionRunner

class TestSprint7SwarmSummoning(unittest.TestCase):

    def setUp(self):
        EventPubSubBus.reset()

    def test_01_event_pubsub_bus(self):
        bus = EventPubSubBus()
        received = []

        def on_event(ev):
            received.append(ev)

        bus.subscribe("chat_channel", on_event)
        env = bus.publish("chat_channel", "MSG_SENT", {"text": "Xin chào Alex"})

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["channel"], "chat_channel")
        self.assertEqual(received[0]["type"], "MSG_SENT")
        self.assertEqual(received[0]["data"]["text"], "Xin chào Alex")
        self.assertEqual(env["seq"], 1)

    def test_02_event_history_since(self):
        bus = EventPubSubBus()
        bus.publish("ch1", "EV1", {"i": 1})
        bus.publish("ch2", "EV2", {"i": 2})
        bus.publish("ch1", "EV3", {"i": 3})

        all_hist = bus.get_history()
        self.assertEqual(len(all_hist), 3)

        since_hist = bus.get_history(channel="ch1", since_seq=1)
        self.assertEqual(len(since_hist), 1)
        self.assertEqual(since_hist[0]["type"], "EV3")

    def test_03_dynamic_agent_summoning(self):
        res = DynamicSummoningService.create_summon_request(
            caller_role="david_fe",
            target_role="marcus_ba",
            reason="Làm rõ logic voucher giảm giá 20%",
            task_id="TASK-701"
        )
        self.assertIn("summon_id", res)
        self.assertEqual(res["caller_role"], "david_fe")
        self.assertEqual(res["target_role"], "marcus_ba")
        self.assertIn("David", res["caller_name"])
        self.assertIn("Marcus", res["target_name"])
        self.assertIn("<david_fe_thinking>", res["caller_thought"])
        self.assertIn("<marcus_ba_thinking>", res["target_thought"])
        self.assertIn("Marcus (Lead Business Analyst)", res["resolution"])

    def test_04_token_guard_usage_and_budget(self):
        rec = TokenConsumptionGuard.record_usage(
            session_id="sess_alex_01",
            tokens_in=500,
            tokens_out=250,
            cached_tokens=100
        )
        self.assertEqual(rec["session_id"], "sess_alex_01")
        self.assertGreater(rec["cost_usd"], 0)
        self.assertGreater(rec["savings_usd"], 0)

        budget = TokenConsumptionGuard.get_budget_status()
        self.assertIn("total_tokens_spent", budget)
        self.assertIn("total_tokens_saved", budget)
        self.assertEqual(budget["total_tokens_saved"], 42500)
        self.assertEqual(budget["burn_rate_status"], "optimal")

    def test_05_swarm_runner_cycle(self):
        res = SwarmExecutionRunner.execute_task_cycle(
            prompt="Thiết kế module tích điểm đổi quà và voucher giảm giá"
        )
        self.assertIn("task_id", res)
        self.assertIn("checkpoint", res)
        self.assertEqual(res["checkpoint"]["status"], "pending_approval")
        self.assertTrue(res["summoning_invoked"])
        self.assertIn("Alex", res["alex_response"])
        self.assertIn("<alex_thinking>", res["alex_thinking"])
        self.assertEqual(len(res["stages_completed"]), 4)

    def test_06_dispatcher_swarm_endpoints(self):
        # 1. Run cycle endpoint
        status, headers, body = RequestDispatcher.dispatch_post(
            '/api/swarm/run-cycle',
            {"prompt": "Tối ưu hóa bảng CSDL SQLite WAL"}
        )
        self.assertEqual(status, 200)
        cycle_data = json.loads(body.decode('utf-8'))
        self.assertIn("task_id", cycle_data)

        # 2. Summon endpoint
        status, headers, body = RequestDispatcher.dispatch_post(
            '/api/swarm/summon',
            {"caller_role": "carlos_be", "target_role": "maya_syst", "reason": "Tư vấn cấu trúc index"}
        )
        self.assertEqual(status, 200)
        summon_data = json.loads(body.decode('utf-8'))
        self.assertEqual(summon_data["caller_role"], "carlos_be")

        # 3. Events endpoint
        status, headers, body = RequestDispatcher.dispatch_get('/api/swarm/events?since=0')
        self.assertEqual(status, 200)
        events_data = json.loads(body.decode('utf-8'))
        self.assertIn("events", events_data)
        self.assertGreater(len(events_data["events"]), 0)

        # 4. Token budget endpoint
        status, headers, body = RequestDispatcher.dispatch_get('/api/swarm/token-budget')
        self.assertEqual(status, 200)
        budget_data = json.loads(body.decode('utf-8'))
        self.assertEqual(budget_data["burn_rate_status"], "optimal")

if __name__ == '__main__':
    unittest.main()
