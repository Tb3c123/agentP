"""
agentP - Workspace Controller
Handles chat streams, executive Alex desk commands, and user checkpoint gate responses.
Author: Carlos (Backend Dev)
"""

import sys
import os
from typing import Dict, Any, Tuple
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))
from command_workspace import CommandWorkspaceService

class WorkspaceController(BaseController):
    """Manages Workspace state and conversational interactions with Alex."""

    @staticmethod
    def get_state() -> Tuple[int, Dict[str, str], bytes]:
        state = CommandWorkspaceService.get_workspace_state()
        return BaseController.json_response(state, 200)

    @staticmethod
    def send_chat(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        message = data.get('message', '')
        if not message.strip():
            return BaseController.error_response("Message cannot be empty", 400)
        res = CommandWorkspaceService.handle_chat_message(message)
        return BaseController.json_response(res, 200)

    @staticmethod
    def respond_checkpoint(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        checkpoint_id = data.get('checkpoint_id', '')
        action = data.get('action', '')
        feedback = data.get('feedback', '')
        res = CommandWorkspaceService.respond_to_checkpoint(checkpoint_id, action, feedback)
        return BaseController.json_response(res, 200)
