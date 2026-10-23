"""
agentP - Base Controller
Pattern: Front Controller / Action Dispatcher
Author: Carlos (Backend Dev)
"""

import json
from typing import Tuple, Dict, Any, Optional

class BaseController:
    """Base class for HTTP endpoint controllers."""

    @staticmethod
    def json_response(data: Any, status: int = 200, extra_headers: Optional[Dict[str, str]] = None) -> Tuple[int, Dict[str, str], bytes]:
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Role-Id'
        }
        if extra_headers:
            headers.update(extra_headers)
        body = json.dumps(data).encode('utf-8')
        return status, headers, body

    @staticmethod
    def error_response(message: str, status: int = 400) -> Tuple[int, Dict[str, str], bytes]:
        return BaseController.json_response({"error": message, "success": False}, status=status)
