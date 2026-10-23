"""
agentP - Protocol Controller
Handles built-in agentP Core Daemon protocol, health checks, sessions, and chat completions.
Author: Carlos (Backend Dev)
"""

import sys
import os
import time
from typing import Dict, Any, Tuple
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'repositories')))
from sessions_repo import SessionsRepository

class ProtocolController(BaseController):
    """Manages protocol health, 1:1 isolated sessions, token savings, and mock LLM streams."""

    @staticmethod
    def get_health(port: int = 9090) -> Tuple[int, Dict[str, str], bytes]:
        health = SessionsRepository.get_health(port=port)
        return BaseController.json_response(health, 200)

    @staticmethod
    def get_sessions() -> Tuple[int, Dict[str, str], bytes]:
        sessions = SessionsRepository.get_sessions()
        return BaseController.json_response({"sessions": sessions, "total": len(sessions)}, 200)

    @staticmethod
    def get_tokens() -> Tuple[int, Dict[str, str], bytes]:
        tokens = SessionsRepository.get_token_metrics()
        return BaseController.json_response(tokens, 200)

    @staticmethod
    def chat_completions(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        role_id = data.get('role_id', 'lead_pm')
        prompt = data.get('prompt', '')
        task_id = data.get('task_id', 'TASK-101')

        # Thinking tag mapping based on specialist role
        if role_id == 'qa_lead':
            thinking_log = f"<reasoning_content>\n1. Phân tích ca kiểm thử cho {task_id}.\n2. Chạy Jest test suite: 100% PASS.\n</reasoning_content>"
            model = "deepseek-r1"
        elif role_id == 'frontend_dev':
            thinking_log = f"<thought>\n1. Khởi tạo State & Event cho {task_id}.\n2. Đồng bộ widget qua Onlook AST engine.\n</thought>"
            model = "gemini-2.5-flash"
        else:
            thinking_log = f"<thinking>\n1. Tiếp nhận prompt: {prompt[:40]}...\n2. Phân rã story points và ủy quyền Swarm 1:1.\n</thinking>"
            model = "claude-3.5-sonnet"

        res = {
            "id": f"chatcmpl-{int(time.time())}",
            "role_id": role_id,
            "model": model,
            "task_id": task_id,
            "thinking_log": thinking_log,
            "response": f"Chuyên viên [{role_id}] đã tiếp nhận nhiệm vụ {task_id} thành công.",
            "tokens_consumed": 1240,
            "latency_ms": 145
        }
        return BaseController.json_response(res, 200)
