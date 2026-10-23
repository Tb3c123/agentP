"""
agentP Architecture - State Machine Pattern
Controls valid transitions across the 6 Kanban columns and Checkpoint Gate states.
Enforces the DoD (Definition of Done) rule: No skipping quality gates!
"""

from typing import Dict, List, Set

class KanbanTaskStateMachine:
    """Enforces strict transitions between Kanban lifecycle states."""

    # 6 Standard Columns
    COLUMNS = [
        "backlog",          # 1. Chờ Làm
        "spec_design",      # 2. Đặc Tả & Thiết Kế
        "development",      # 3. Đang Lập Trình
        "review",           # 4. Code Review
        "quality_gate",     # 5. Kiểm Thử QA
        "done"              # 6. Hoàn Tất Nghiệm Thu
    ]

    # Valid transitions map
    VALID_TRANSITIONS: Dict[str, Set[str]] = {
        "backlog": {"spec_design", "development"},
        "spec_design": {"development", "backlog"},
        "development": {"review", "quality_gate", "spec_design"},
        "review": {"quality_gate", "development"},
        "quality_gate": {"done", "development"},  # Fails QA goes back to dev
        "done": set()                             # Terminal approved state
    }

    @classmethod
    def can_transition(cls, current_status: str, target_status: str) -> bool:
        if current_status not in cls.VALID_TRANSITIONS:
            return False
        return target_status in cls.VALID_TRANSITIONS[current_status]

    @classmethod
    def validate_transition(cls, current_status: str, target_status: str):
        if not cls.can_transition(current_status, target_status):
            valid = list(cls.VALID_TRANSITIONS.get(current_status, []))
            raise ValueError(
                f"Invalid Kanban transition from '{current_status}' to '{target_status}'. "
                f"Valid next states are: {valid}"
            )
        return True


class CheckpointGateStateMachine:
    """Manages User Checkpoint Gate approval lifecycle."""

    STATES = ["pending", "approved", "rejected"]

    @classmethod
    def resolve(cls, current_state: str, action: str) -> str:
        if current_state != "pending":
            raise ValueError(f"Checkpoint already resolved with state '{current_state}'.")
            
        if action not in ["approved", "rejected"]:
            raise ValueError("Action must be 'approved' or 'rejected'.")
            
        return action
