"""
agentP - Sprint 8 Unit Tests: Git Engine, Conventional Commits, Changelog, Chaos Resilience & RBAC
Author: Viktor (QA Lead) & Sophia (Security Lead)
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
from git_engine import GitEngineService
from changelog_generator import ChangelogGeneratorService
from resilience_guard import ChaosResilienceGuard
from jwt_auth import JwtRbacGuard

class TestSprint8GitResilienceChangelog(unittest.TestCase):

    def test_01_git_conventional_commits_validation(self):
        # Valid conventional commits
        v1 = GitEngineService.validate_commit_message("feat(auth): implement JWT RBAC authenticator")
        self.assertTrue(v1["valid"])
        self.assertEqual(v1["type"], "feat")
        self.assertEqual(v1["scope"], "auth")

        v2 = GitEngineService.validate_commit_message("fix: resolve flex layout squish on providers hub")
        self.assertTrue(v2["valid"])
        self.assertEqual(v2["type"], "fix")
        self.assertIsNone(v2["scope"])

        # Invalid commit message
        v3 = GitEngineService.validate_commit_message("fixed some bugs and updated ui")
        self.assertFalse(v3["valid"])
        self.assertIn("Conventional Commits", v3["reason"])

    def test_02_git_task_branch_creation(self):
        branch = GitEngineService.create_task_branch("TASK-801", "Automated Git Engine and Branching Strategy")
        self.assertEqual(branch["task_id"], "TASK-801")
        self.assertTrue(branch["branch_name"].startswith("feature/task-801-"))
        self.assertEqual(branch["base_branch"], "main")

    def test_03_git_commit_audit_persistence(self):
        audit = GitEngineService.record_commit_audit(
            commit_hash="c0ffee1",
            message="feat(git): add commit audit logging",
            author="git_specialist"
        )
        self.assertEqual(audit["commit_hash"], "c0ffee1")
        self.assertTrue(audit["conventional"])
        self.assertEqual(audit["status"], "audited")

    def test_04_changelog_generation(self):
        md = ChangelogGeneratorService.generate_changelog_markdown()
        self.assertIn("# Changelog 📜", md)
        self.assertIn("## [2.7.0]", md)
        self.assertIn("### 🚀 Added", md)
        self.assertIn("Keep a Changelog", md)

        write_res = ChangelogGeneratorService.write_changelog_file()
        self.assertEqual(write_res["latest_version"], "2.7.0")
        self.assertTrue(os.path.exists(write_res["path"]))

    def test_05_chaos_resilience_wal_health(self):
        health = ChaosResilienceGuard.verify_wal_health()
        self.assertEqual(health["journal_mode"].lower(), "wal")
        self.assertEqual(health["integrity_check"].lower(), "ok")
        self.assertTrue(health["foreign_keys_enabled"])
        self.assertTrue(health["is_healthy"])

        recovery = ChaosResilienceGuard.simulate_crash_recovery()
        self.assertEqual(recovery["recovery_status"], "RECOVERED_CLEAN")
        self.assertEqual(recovery["data_loss_bytes"], 0)

    def test_06_atomic_snapshot_backup(self):
        snap = ChaosResilienceGuard.create_atomic_snapshot()
        self.assertEqual(snap["status"], "success")
        self.assertGreater(snap["size_bytes"], 0)
        self.assertTrue(os.path.exists(os.path.join(BASE_DIR, snap["snapshot_file"])))

    def test_07_jwt_rbac_generation_and_verification(self):
        token = JwtRbacGuard.generate_token(user_id="lead_pm_alex", role="LEAD_PM")
        self.assertIsInstance(token, str)
        self.assertEqual(len(token.split(".")), 3)

        # Verification
        res = JwtRbacGuard.verify_token(token)
        self.assertTrue(res["valid"])
        self.assertEqual(res["payload"]["sub"], "lead_pm_alex")
        self.assertEqual(res["payload"]["role"], "LEAD_PM")

        # Permission check
        self.assertTrue(JwtRbacGuard.check_permission(token, "approve_checkpoint"))
        self.assertTrue(JwtRbacGuard.check_permission(token, "summon"))
        self.assertFalse(JwtRbacGuard.check_permission(token, "delete_project"))

    def test_08_dispatcher_sprint8_endpoints(self):
        # 1. Changelog GET
        status, headers, body = RequestDispatcher.dispatch_get('/api/release/changelog')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertEqual(data["latest_version"], "2.7.0")

        # 2. Git staging GET
        status, headers, body = RequestDispatcher.dispatch_get('/api/git/staging')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("branch", data)

        # 3. Resilience GET
        status, headers, body = RequestDispatcher.dispatch_get('/api/resilience/status')
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertTrue(data["is_healthy"])

        # 4. Validate commit POST
        status, headers, body = RequestDispatcher.dispatch_post(
            '/api/git/validate-commit',
            {"message": "feat(core): enhance event bus"}
        )
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertTrue(data["valid"])

        # 5. Auth token POST
        status, headers, body = RequestDispatcher.dispatch_post(
            '/api/auth/token',
            {"user_id": "test_dev", "role": "DEVELOPER"}
        )
        self.assertEqual(status, 200)
        data = json.loads(body.decode('utf-8'))
        self.assertIn("token", data)

if __name__ == '__main__':
    unittest.main()
