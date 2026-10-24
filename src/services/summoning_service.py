"""
agentP - Dynamic Agent Summoning Protocol (Sprint 7)
Pattern: Mediator & Dynamic Delegation Pattern
Author: Marcus (Lead BA) & Alex (PM)
Enables autonomous cross-role summoning when agents encounter blockers or require specialist consultation.
"""

import time
import os
import sys
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from pubsub_bus import EventPubSubBus

class DynamicSummoningService:
    """Manages dynamic peer-to-peer agent summoning under Alex PM's oversight."""

    ROLE_NAMES = {
        "lead_pm": "Alex (Trưởng Dự Án / Lead PM)",
        "marcus_ba": "Marcus (Lead Business Analyst)",
        "maya_syst": "Maya (Kiến Trúc Sư Hệ Thống)",
        "elena_ui": "Elena (Chuyên Gia UI/UX)",
        "david_fe": "David (Kỹ Sư Frontend React/Flutter)",
        "carlos_be": "Carlos (Kỹ Sư Backend NestJS/Python)",
        "lucas_fe": "Lucas (Kỹ Sư Trưởng Senior Engine)",
        "viktor_qa": "Viktor (Trưởng Nhóm Kiểm Thử QA)",
        "liam_devops": "Liam (Kỹ Sư DevOps & AVD)",
        "frank_sre": "Frank (Chuyên Gia Độ Tin Cậy SRE)",
        "sophia_sec": "Sophia (Chuyên Gia Bảo Mật & Compliance)",
        "chloe_data": "Chloe (Chuyên Viên Báo Cáo & Token)",
        "sarah_docs": "Sarah (Chuyên Viên Tài Liệu)",
        "oliver_perf": "Oliver (Kỹ Sư Tối Ưu Hiệu Năng)"
    }

    @classmethod
    def create_summon_request(cls, caller_role: str, target_role: str, reason: str, task_id: str = "TASK-701") -> Dict[str, Any]:
        """Creates a dynamic summoning invocation between two agents."""
        bus = EventPubSubBus()
        caller_name = cls.ROLE_NAMES.get(caller_role, caller_role)
        target_name = cls.ROLE_NAMES.get(target_role, target_role)

        summon_id = f"SUMMON-{int(time.time())}-{caller_role[:4]}"

        # Simulated prompt and response exchange
        caller_thought = f"<{caller_role}_thinking>\n1. Đang triển khai {task_id}.\n2. Phát hiện khúc mắc: '{reason}'.\n3. Cần triệu hồi {target_name} để hội ý chéo.\n</{caller_role}_thinking>"
        target_thought = f"<{target_role}_thinking>\n1. Tiếp nhận yêu cầu triệu hồi từ {caller_name}.\n2. Phân tích tài liệu & tiêu chí kỹ thuật.\n3. Đã đưa ra hướng giải quyết cụ thể cho {task_id}.\n</{target_role}_thinking>"

        target_resolution = f"[{target_name} Phản Hồi]: Đã làm rõ vấn đề '{reason}' cho {task_id}. Toàn bộ tiêu chuẩn đã được cập nhật vào CSDL SQLite và sẵn sàng cho {caller_name} tiếp tục lập trình."

        event_data = {
            "summon_id": summon_id,
            "caller_role": caller_role,
            "caller_name": caller_name,
            "target_role": target_role,
            "target_name": target_name,
            "task_id": task_id,
            "reason": reason,
            "caller_thought": caller_thought,
            "target_thought": target_thought,
            "resolution": target_resolution,
            "status": "resolved",
            "tokens_consumed": 480,
            "timestamp": time.time()
        }

        # Broadcast via EventBus
        bus.publish("summoning", "AGENT_SUMMONED", event_data)
        bus.publish("workspace", "NEW_ACTIVITY", {
            "icon": "⚡",
            "title": f"{caller_name} đã triệu hồi {target_name}",
            "description": reason,
            "time": "Vừa xong"
        })

        return event_data
