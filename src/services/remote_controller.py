"""
agentP - Mobile Remote Controller & QR Pairing Service
Role: Liam (DevOps) & David (Frontend)
Sprint 5: Mobile Remote Pairing & Local Network Host
"""

import time
import socket
from typing import Dict, Any

class MobileRemoteService:
    """Provides local network host status and pairing credentials for mobile phones."""

    DEFAULT_HOST_IP = "192.168.1.15"
    WS_PORT = 8080
    HTTP_PORT = 9090
    PAIRING_KEY = "AGENTP-PAIR-7749"

    @classmethod
    def get_pairing_info(cls) -> Dict[str, Any]:
        return {
            "host_name": "agentp-macbook-pro.local",
            "ip_address": cls.DEFAULT_HOST_IP,
            "http_port": cls.HTTP_PORT,
            "websocket_port": cls.WS_PORT,
            "pairing_code": cls.PAIRING_KEY,
            "qr_data_url": f"agentp://connect?host={cls.DEFAULT_HOST_IP}&port={cls.WS_PORT}&key={cls.PAIRING_KEY}",
            "status": "online",
            "connected_devices": 1,
            "device_model": "Pixel 8 Pro (Remote Client)",
            "allowed_actions": ["approve_checkpoint", "view_kanban", "emergency_stop", "trigger_hot_reload"]
        }
