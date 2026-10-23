"""
agentP - Project & Settings Controller
Handles smart auto-naming, project settings, and Antigravity Danger Zone deletion.
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
from auto_namer import generate_project_names
import project_manager as pm

class ProjectController(BaseController):
    """Manages project naming, settings configuration, and safe project deletion."""

    @staticmethod
    def auto_name(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        description = data.get('description', '')
        suggestions = generate_project_names(description)
        return BaseController.json_response(suggestions, 200)

    @staticmethod
    def get_settings() -> Tuple[int, Dict[str, str], bytes]:
        settings = pm.get_project_settings()
        return BaseController.json_response(settings, 200)

    @staticmethod
    def verify_delete(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        project_id = data.get('project_id', '')
        confirmation = data.get('confirmation', '')
        res = pm.verify_project_deletion(project_id, confirmation)
        status = 200 if res.get('allowed') else 403
        return BaseController.json_response(res, status)
