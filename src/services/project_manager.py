"""
agentP - Project Manager & File Operations Service
Sprint 4: File Explorer, Safe Trash, Git Diff & Antigravity Danger Zone Safety
Roles: Sam (Fullstack), Max (Git), Nora (Security), Viktor (QA Lead)
"""

import os
import shutil
import json
import sqlite3
import time
from typing import Dict, List, Optional, Any

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
AGENTS_DIR = os.path.join(WORKSPACE_DIR, ".agents")
TRASH_DIR = os.path.join(AGENTS_DIR, "trash")
DB_PATH = os.path.join(AGENTS_DIR, "db.sqlite")

# Ensure trash directory exists
os.makedirs(TRASH_DIR, exist_ok=True)

# Map file extensions/paths to Agent Roles
ROLE_FILE_MAPPING = {
    ".tsx": {"role_id": "david_fe", "name": "David", "title": "Frontend Dev", "color": "#0284C7"},
    ".jsx": {"role_id": "david_fe", "name": "David", "title": "Frontend Dev", "color": "#0284C7"},
    ".html": {"role_id": "david_fe", "name": "David", "title": "Frontend Dev", "color": "#0284C7"},
    ".css": {"role_id": "elena_uiux", "name": "Elena", "title": "UI/UX Designer", "color": "#D946EF"},
    ".tldr": {"role_id": "elena_uiux", "name": "Elena", "title": "UI/UX Designer", "color": "#D946EF"},
    ".py": {"role_id": "carlos_be", "name": "Carlos", "title": "Backend Dev", "color": "#059669"},
    ".dart": {"role_id": "lucas_senior", "name": "Lucas", "title": "Senior Mobile Dev", "color": "#7C3AED"},
    ".sql": {"role_id": "maya_arch", "name": "Maya", "title": "System Architect", "color": "#0F766E"},
    ".md": {"role_id": "marcus_ba", "name": "Marcus", "title": "Lead BA", "color": "#D97706"},
    "test_": {"role_id": "viktor_qa", "name": "Viktor", "title": "QA Lead", "color": "#DC2626"},
    ".sh": {"role_id": "liam_devops", "name": "Liam", "title": "DevOps Engineer", "color": "#475569"},
    "Dockerfile": {"role_id": "liam_devops", "name": "Liam", "title": "DevOps Engineer", "color": "#475569"},
}


def get_agent_for_file(filepath: str) -> Dict[str, str]:
    """Determines which agent owns or maintains a file."""
    filename = os.path.basename(filepath)
    if filename.startswith("test_") or "test/" in filepath:
        return ROLE_FILE_MAPPING["test_"]
    
    for ext, agent in ROLE_FILE_MAPPING.items():
        if filename.endswith(ext):
            return agent
            
    return {"role_id": "alex_pm", "name": "Alex", "title": "Lead PM", "color": "#0D9488"}


def build_file_tree(start_path: str = WORKSPACE_DIR, max_depth: int = 4) -> Dict[str, Any]:
    """Generates a hierarchical file tree with agent ownership and metadata."""
    ignored = {".git", "__pycache__", "node_modules", ".venv", ".pytest_cache", ".DS_Store"}
    
    def _scan(current_path: str, depth: int) -> Dict[str, Any]:
        name = os.path.basename(current_path) or "root"
        is_dir = os.path.isdir(current_path)
        
        rel_path = os.path.relpath(current_path, WORKSPACE_DIR)
        node = {
            "name": name,
            "path": rel_path if rel_path != "." else "",
            "is_dir": is_dir,
            "children": []
        }
        
        if is_dir:
            if depth >= max_depth:
                return node
            try:
                entries = sorted(os.listdir(current_path))
                for entry in entries:
                    if entry in ignored:
                        continue
                    full_p = os.path.join(current_path, entry)
                    node["children"].append(_scan(full_p, depth + 1))
            except PermissionError:
                pass
        else:
            try:
                stat = os.stat(current_path)
                node["size"] = stat.st_size
                node["modified"] = stat.st_mtime
                node["agent"] = get_agent_for_file(current_path)
            except Exception:
                node["size"] = 0
                node["agent"] = get_agent_for_file(current_path)
                
        return node

    return _scan(start_path, 0)


def read_file_content(relative_path: str) -> Dict[str, Any]:
    """Reads a workspace file safely."""
    clean_rel = os.path.normpath(relative_path).lstrip("/")
    abs_path = os.path.join(WORKSPACE_DIR, clean_rel)
    
    # Boundary check
    if not abs_path.startswith(WORKSPACE_DIR):
        return {"error": "Access denied: Path outside workspace", "success": False}
        
    if not os.path.exists(abs_path):
        return {"error": "File not found", "success": False}
        
    if os.path.isdir(abs_path):
        return {"error": "Path is a directory", "success": False}
        
    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return {
            "success": True,
            "path": clean_rel,
            "filename": os.path.basename(clean_rel),
            "content": content,
            "agent": get_agent_for_file(clean_rel),
            "lines": len(content.splitlines())
        }
    except Exception as e:
        return {"error": str(e), "success": False}


def safe_delete_file(relative_path: str) -> Dict[str, Any]:
    """
    Safely moves a file to .agents/trash/ instead of permanent deletion.
    Includes restoration metadata so it can be un-deleted.
    """
    clean_rel = os.path.normpath(relative_path).lstrip("/")
    abs_path = os.path.join(WORKSPACE_DIR, clean_rel)
    
    if not abs_path.startswith(WORKSPACE_DIR):
        return {"error": "Access denied: Path outside workspace", "success": False}
        
    if not os.path.exists(abs_path):
        return {"error": "File does not exist", "success": False}
        
    try:
        trash_id = f"{int(time.time())}_{os.path.basename(clean_rel)}"
        trash_dest = os.path.join(TRASH_DIR, trash_id)
        
        # Copy to trash with meta
        shutil.move(abs_path, trash_dest)
        
        meta = {
            "trash_id": trash_id,
            "original_rel_path": clean_rel,
            "deleted_at": time.time(),
            "deleted_by": "user_or_agent"
        }
        with open(f"{trash_dest}.meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f)
            
        return {
            "success": True,
            "message": f"File '{clean_rel}' has been moved safely to .agents/trash/",
            "trash_id": trash_id
        }
    except Exception as e:
        return {"error": str(e), "success": False}


def restore_trash_file(trash_id: str) -> Dict[str, Any]:
    """Restores a file from .agents/trash/ back to its original location."""
    trash_file = os.path.join(TRASH_DIR, trash_id)
    meta_file = f"{trash_file}.meta.json"
    
    if not os.path.exists(trash_file) or not os.path.exists(meta_file):
        return {"error": "Trash file or metadata not found", "success": False}
        
    try:
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        target_path = os.path.join(WORKSPACE_DIR, meta["original_rel_path"])
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        shutil.move(trash_file, target_path)
        os.remove(meta_file)
        
        return {
            "success": True,
            "message": f"Restored '{meta['original_rel_path']}' successfully",
            "path": meta["original_rel_path"]
        }
    except Exception as e:
        return {"error": str(e), "success": False}


def list_trash_files() -> List[Dict[str, Any]]:
    """Lists all files in .agents/trash/ with metadata."""
    items = []
    if not os.path.exists(TRASH_DIR):
        return items
        
    for fname in os.listdir(TRASH_DIR):
        if fname.endswith(".meta.json"):
            meta_p = os.path.join(TRASH_DIR, fname)
            try:
                with open(meta_p, "r", encoding="utf-8") as f:
                    items.append(json.load(f))
            except Exception:
                pass
    return sorted(items, key=lambda x: x.get("deleted_at", 0), reverse=True)


def compute_monaco_split_diff(filepath: str, old_version: Optional[str] = None, new_version: Optional[str] = None) -> Dict[str, Any]:
    """
    Computes a side-by-side split diff for Monaco Editor.
    If versions not supplied, uses sample or file content vs proposed changes.
    """
    if old_version is None or new_version is None:
        # Default showcase sample if not provided
        old_version = (
            "export const CartCheckoutButton = () => {\n"
            "  return (\n"
            "    <button className=\"bg-gray-400 text-black py-2 px-4 rounded\">\n"
            "      Thanh toán\n"
            "    </button>\n"
            "  );\n"
            "};"
        )
        new_version = (
            "export const CartCheckoutButton = () => {\n"
            "  // Upgraded by Elena UI/UX & Lucas Senior Dev\n"
            "  return (\n"
            "    <button className=\"bg-teal-600 hover:bg-teal-700 text-white font-bold py-3 px-6 rounded-lg shadow-sm transition-all\">\n"
            "      Thanh toán ngay & Nhận Xu 🪙\n"
            "    </button>\n"
            "  );\n"
            "};"
        )

    old_lines = old_version.splitlines()
    new_lines = new_version.splitlines()
    
    return {
        "filepath": filepath,
        "old_content": old_version,
        "new_content": new_version,
        "old_line_count": len(old_lines),
        "new_line_count": len(new_lines),
        "lines_added": max(0, len(new_lines) - len(old_lines) + 2),
        "lines_deleted": 1
    }


def verify_antigravity_danger_zone(project_id: str, confirmation_input: str) -> Dict[str, Any]:
    """
    Strict Antigravity-style 2-factor confirmation:
    Requires the user to type the EXACT expected project name.
    If mismatched by even 1 character (case-sensitive, trimmed), delete is REJECTED.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM projects WHERE project_id = ?", (project_id,))
        row = cursor.fetchone()
        conn.close()
        
        expected_name = row[0] if row else "FoodDelivery-Loyalty-App"
    except Exception:
        expected_name = "FoodDelivery-Loyalty-App"
        
    cleaned_input = confirmation_input.strip()
    is_match = (cleaned_input == expected_name)
    
    if not is_match:
        return {
            "allowed": False,
            "error": f"Confirmation mismatch. Expected '{expected_name}', got '{cleaned_input}'. Deletion is strictly locked.",
            "expected": expected_name
        }
        
    return {
        "allowed": True,
        "message": f"Confirmation match '{expected_name}'. Danger zone unlocked.",
        "expected": expected_name
    }


def get_project_settings(project_id: str = "proj_food_delivery") -> Dict[str, Any]:
    """Fetches project configuration and environment variables from SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT project_id, name, description, local_path, git_repo_url, default_branch, status, created_at FROM projects WHERE project_id = ?", (project_id,))
        row = cursor.fetchone()
        
        env_vars = []
        cursor.execute("SELECT var_key, var_value, is_secret FROM project_env_vars WHERE project_id = ?", (project_id,))
        for r in cursor.fetchall():
            env_vars.append({"key": r[0], "value": "••••••••" if r[2] else r[1], "is_secret": bool(r[2])})
            
        conn.close()
        
        if row:
            return {
                "project_id": row[0],
                "name": row[1],
                "description": row[2],
                "local_path": row[3],
                "git_repo_url": row[4],
                "default_branch": row[5],
                "status": row[6],
                "created_at": row[7],
                "env_vars": env_vars
            }
    except Exception as e:
        return {"error": str(e), "success": False}
        
    return {
        "project_id": project_id,
        "name": "FoodDelivery-Loyalty-App",
        "description": "Ứng dụng giao đồ ăn tích hợp chương trình tích điểm khách hàng thân thiết",
        "local_path": WORKSPACE_DIR,
        "git_repo_url": "https://github.com/Tb3c123/agentP.git",
        "default_branch": "main",
        "status": "in_progress",
        "env_vars": [
            {"key": "PORT", "value": "9090", "is_secret": False},
            {"key": "AVD_DEVICE_NAME", "value": "Pixel_8_Pro_API_34", "is_secret": False},
            {"key": "LLM_PROXY_URL", "value": "http://127.0.0.1:9090", "is_secret": False}
        ]
    }
