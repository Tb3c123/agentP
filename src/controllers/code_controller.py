"""
agentP - Code & File Operations Controller
Handles file tree, content reading, safe trash, Monaco split diff, and file deletion.
Author: Carlos (Backend Dev) & Lucas (Senior Dev)
"""

import sys
import os
from typing import Dict, Any, Tuple
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))
import project_manager as pm

class CodeController(BaseController):
    """Manages file explorer, Monaco split diff, and safe file operations."""

    @staticmethod
    def get_file_tree() -> Tuple[int, Dict[str, str], bytes]:
        tree = pm.build_file_tree()
        return BaseController.json_response(tree, 200)

    @staticmethod
    def get_file_content(filepath: str) -> Tuple[int, Dict[str, str], bytes]:
        if not filepath:
            return BaseController.error_response("Missing file path", 400)
        res = pm.read_file_content(filepath)
        status = 200 if res.get('success') else 400
        return BaseController.json_response(res, status)

    @staticmethod
    def get_split_diff(filepath: str) -> Tuple[int, Dict[str, str], bytes]:
        target = filepath or 'lib/features/cart/cart_button.tsx'
        diff_data = pm.compute_monaco_split_diff(target)
        return BaseController.json_response(diff_data, 200)

    @staticmethod
    def get_trash_items() -> Tuple[int, Dict[str, str], bytes]:
        trash_items = pm.list_trash_files()
        return BaseController.json_response({"trash": trash_items}, 200)

    @staticmethod
    def delete_file(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        filepath = data.get('filepath', '')
        if not filepath:
            return BaseController.error_response("Missing filepath parameter", 400)
        res = pm.delete_file_safely(filepath)
        status = 200 if res.get('success') else 400
        return BaseController.json_response(res, status)
