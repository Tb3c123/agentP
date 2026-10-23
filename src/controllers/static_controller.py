"""
agentP - Static Assets Controller
Handles static web serving from src/web and docs/
Author: Carlos (Backend Dev)
"""

import os
import mimetypes
from typing import Dict, Tuple

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
WEB_DIR = os.path.join(os.path.dirname(__file__), '..', 'web')

class StaticController:
    """Serves static files including HTML, CSS, JavaScript, and SVG assets."""

    @staticmethod
    def serve_file(path: str) -> Tuple[int, Dict[str, str], bytes]:
        if path in ('/', ''):
            file_path = os.path.join(WEB_DIR, 'index.html')
        elif path.startswith('/docs/'):
            file_path = os.path.join(BASE_DIR, path.lstrip('/'))
        else:
            rel_path = path.lstrip('/')
            file_path = os.path.join(WEB_DIR, rel_path)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime, _ = mimetypes.guess_type(file_path)
            mime = mime or 'text/plain'
            headers = {
                'Content-Type': mime,
                'Access-Control-Allow-Origin': '*'
            }
            with open(file_path, 'rb') as f:
                content = f.read()
            return 200, headers, content

        headers = {'Content-Type': 'text/plain'}
        return 404, headers, b"404 Not Found"
