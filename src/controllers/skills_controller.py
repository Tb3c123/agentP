"""
agentP - Skills Controller
Handles queries for the 30 Universal Skills & Rules library.
Author: Carlos (Backend Dev)
"""

import sys
import os
from typing import Dict, Any, Tuple, Optional
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'repositories')))
from skills_repo import SkillsRepository

class SkillsController(BaseController):
    """Manages 30 Universal Skills querying and category filtering."""

    @staticmethod
    def get_skills(category: Optional[str] = None) -> Tuple[int, Dict[str, str], bytes]:
        skills = SkillsRepository.get_all_skills(category=category)
        return BaseController.json_response({
            "total": len(skills),
            "skills": skills
        }, 200)
