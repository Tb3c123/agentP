"""
agentP - Swarm & Real-Time Event Controller (Sprint 7)
Handles multi-turn swarm execution, peer summoning, token budget, and pub-sub events.
Author: Carlos (Backend Dev) & Alex (PM)
"""

import sys
import os
import json
from typing import Dict, Any, Tuple
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))

from pubsub_bus import EventPubSubBus
from summoning_service import DynamicSummoningService
from token_guard import TokenConsumptionGuard
from swarm_runner import SwarmExecutionRunner

class SwarmController(BaseController):
    """Endpoints controller for Sprint 7 Swarm orchestration and event streams."""

    @staticmethod
    def get_events(query_params: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        bus = EventPubSubBus()
        channel = query_params.get('channel', [None])[0]
        since_seq = int(query_params.get('since', [0])[0])
        history = bus.get_history(channel=channel, since_seq=since_seq)
        return BaseController.json_response({
            "events": history,
            "count": len(history),
            "latest_seq": history[-1]["seq"] if history else since_seq
        }, 200)

    @staticmethod
    def run_swarm_cycle(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        prompt = data.get('prompt', 'Triển khai tính năng mới')
        project_id = data.get('project_id', 'proj_food_delivery_01')
        result = SwarmExecutionRunner.execute_task_cycle(prompt=prompt, project_id=project_id)
        return BaseController.json_response(result, 200)

    @staticmethod
    def summon_agent(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        caller = data.get('caller_role', 'david_fe')
        target = data.get('target_role', 'marcus_ba')
        reason = data.get('reason', 'Tham vấn chuyên môn kỹ thuật')
        task_id = data.get('task_id', 'TASK-701')

        res = DynamicSummoningService.create_summon_request(
            caller_role=caller,
            target_role=target,
            reason=reason,
            task_id=task_id
        )
        return BaseController.json_response(res, 200)

    @staticmethod
    def get_token_budget() -> Tuple[int, Dict[str, str], bytes]:
        status = TokenConsumptionGuard.get_budget_status()
        return BaseController.json_response(status, 200)
