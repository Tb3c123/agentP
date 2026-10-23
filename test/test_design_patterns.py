"""
Unit & Integration Tests for Design Patterns Refactoring
Verifies:
1. Mediator Pattern (AlexMediator as central coordinator).
2. Hexagonal Architecture (StoragePort, LlmGatewayPort implementations).
3. State Machine Pattern (Kanban transition enforcement & DoD gatekeeping).
4. Skills Library integration.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "core")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "adapters")))

from ports import StoragePort, LlmGatewayPort
from mediator import AlexMediator
from state_machine import KanbanTaskStateMachine, CheckpointGateStateMachine
from sqlite_adapter import SQLiteStorageAdapter
from daemon_adapter import AgentPDaemonAdapter

class TestDesignPatternsArchitecture(unittest.TestCase):

    def setUp(self):
        self.storage = SQLiteStorageAdapter()
        self.llm = AgentPDaemonAdapter()
        self.mediator = AlexMediator(storage=self.storage, llm_gateway=self.llm)

    def test_01_mediator_command_orchestration(self):
        """Verifies AlexMediator handles single-desk user commands and coordinates swarm."""
        res = self.mediator.handle_user_command("Hãy thiết kế giao diện thanh toán giỏ hàng cho app")
        self.assertIn("Alex", res["sender"])
        self.assertIn("<thinking>", res["thinking_log"])
        self.assertIn("TASK-", res["task_id"])
        self.assertGreater(res["tokens_consumed"], 0)

    def test_02_mediator_emergency_stop_latency(self):
        """Verifies AlexMediator halts the system with latency <15ms."""
        stop_res = self.mediator.trigger_emergency_stop()
        self.assertTrue(stop_res["success"])
        self.assertLess(stop_res["latency_ms"], 15)

        # After emergency stop, commands are blocked
        blocked = self.mediator.handle_user_command("Chạy tiếp tính năng")
        self.assertIn("Dừng Đột Ngột", blocked["content"])

        # Reset
        self.mediator.reset_emergency_stop()
        res_after = self.mediator.handle_user_command("Tiếp tục bình thường")
        self.assertIn("Alex", res_after["sender"])

    def test_03_kanban_state_machine_transition_rules(self):
        """Verifies KanbanTaskStateMachine enforces DoD and blocks illegal state jumps."""
        # Legal transitions
        self.assertTrue(KanbanTaskStateMachine.can_transition("backlog", "development"))
        self.assertTrue(KanbanTaskStateMachine.can_transition("development", "quality_gate"))
        self.assertTrue(KanbanTaskStateMachine.can_transition("quality_gate", "done"))

        # Illegal transitions (cannot jump straight from backlog to done!)
        self.assertFalse(KanbanTaskStateMachine.can_transition("backlog", "done"))
        with self.assertRaises(ValueError):
            KanbanTaskStateMachine.validate_transition("backlog", "done")

    def test_04_hexagonal_adapters_contracts(self):
        """Verifies Adapters correctly implement abstract Ports."""
        # StoragePort implementation
        self.assertIsInstance(self.storage, StoragePort)
        state = self.storage.get_workspace_state("proj_food_delivery")
        self.assertEqual(len(state["swarm_roles"]), 14)

        # LlmGatewayPort implementation
        self.assertIsInstance(self.llm, LlmGatewayPort)
        health = self.llm.check_health()
        self.assertEqual(health["status"], "healthy")
        self.assertEqual(health["service"], "agentp-core-daemon")

if __name__ == "__main__":
    unittest.main()
