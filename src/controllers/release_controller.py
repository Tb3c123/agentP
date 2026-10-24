"""
agentP - Release, Git & Resilience Controller (Sprint 8)
Handles changelog generation, Git conventional commits, WAL snapshots, and RBAC authentication.
Author: Carlos (Backend Dev) & Sophia (Security Lead)
"""

import sys
import os
from typing import Dict, Any, Tuple
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))

from git_engine import GitEngineService
from changelog_generator import ChangelogGeneratorService
from resilience_guard import ChaosResilienceGuard
from jwt_auth import JwtRbacGuard

class ReleaseController(BaseController):
    """Endpoints controller for Sprint 8 features."""

    @staticmethod
    def get_changelog() -> Tuple[int, Dict[str, str], bytes]:
        releases = ChangelogGeneratorService.RELEASES
        raw_md = ChangelogGeneratorService.generate_changelog_markdown()
        return BaseController.json_response({
            "latest_version": releases[0]["version"],
            "releases": releases,
            "markdown": raw_md
        }, 200)

    @staticmethod
    def export_changelog() -> Tuple[int, Dict[str, str], bytes]:
        res = ChangelogGeneratorService.write_changelog_file()
        return BaseController.json_response({
            "status": "success",
            "message": "✓ Đã xuất file CHANGELOG.md thành công theo chuẩn Keep a Changelog.",
            "details": res
        }, 200)

    @staticmethod
    def get_git_status() -> Tuple[int, Dict[str, str], bytes]:
        res = GitEngineService.get_staging_status()
        return BaseController.json_response(res, 200)

    @staticmethod
    def validate_commit(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        msg = data.get("message", "")
        res = GitEngineService.validate_commit_message(msg)
        return BaseController.json_response(res, 200)

    @staticmethod
    def create_branch(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        task_id = data.get("task_id", "TASK-801")
        title = data.get("title", "git feature branch")
        res = GitEngineService.create_task_branch(task_id, title)
        return BaseController.json_response(res, 200)

    @staticmethod
    def get_resilience_status() -> Tuple[int, Dict[str, str], bytes]:
        res = ChaosResilienceGuard.verify_wal_health()
        return BaseController.json_response(res, 200)

    @staticmethod
    def create_snapshot() -> Tuple[int, Dict[str, str], bytes]:
        res = ChaosResilienceGuard.create_atomic_snapshot()
        return BaseController.json_response(res, 200)

    @staticmethod
    def generate_auth_token(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        user_id = data.get("user_id", "alex_pm")
        role = data.get("role", "LEAD_PM")
        token = JwtRbacGuard.generate_token(user_id=user_id, role=role)
        return BaseController.json_response({
            "token": token,
            "user_id": user_id,
            "role": role,
            "status": "active"
        }, 200)
