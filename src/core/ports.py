"""
agentP Architecture - Abstract Ports (Hexagonal Architecture)
Defines clear contracts between the Domain Core and external technologies (DB, LLM, UI).
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class StoragePort(ABC):
    """Outbound Port: Persistence contract for SQLite / Database"""

    @abstractmethod
    def get_workspace_state(self, project_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def save_task(self, task_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def update_task_status(self, task_id: str, new_status: str) -> bool:
        pass

    @abstractmethod
    def resolve_checkpoint(self, checkpoint_id: str, action: str, feedback: str = "") -> Dict[str, Any]:
        pass

    @abstractmethod
    def record_token_usage(self, role_id: str, tokens_in: int, tokens_out: int, task_id: Optional[str] = None):
        pass


class LlmGatewayPort(ABC):
    """Outbound Port: AI Model Gateway contract for 1:1 sessions"""

    @abstractmethod
    def generate_completion(self, role_id: str, prompt: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def check_health(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        pass


class EventBusPort(ABC):
    """Outbound/Inbound Port: Event publication & subscription contract"""

    @abstractmethod
    def publish(self, event_type: str, payload: Dict[str, Any]):
        pass

    @abstractmethod
    def subscribe(self, event_type: str, handler):
        pass
