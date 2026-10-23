"""
agentP - Monaco Split Diff Strategy Engine
Pattern: Strategy Pattern (Algorithm Encapsulation)
Author: Lucas (Senior Dev)
"""

import os
from typing import Dict, Any, List

class DiffStrategyInterface:
    """Strategy interface for computing file diffs."""
    def compute_diff(self, original_text: str, modified_text: str, filepath: str) -> Dict[str, Any]:
        raise NotImplementedError


class MonacoSideBySideDiffStrategy(DiffStrategyInterface):
    """Side-by-side split diff computation tailored for Monaco Editor rendering."""

    def compute_diff(self, original_text: str, modified_text: str, filepath: str) -> Dict[str, Any]:
        orig_lines = original_text.splitlines()
        mod_lines = modified_text.splitlines()

        diff_lines: List[Dict[str, Any]] = []
        added_count = 0
        deleted_count = 0

        # Simple unified-style line mapping for side-by-side display
        max_len = max(len(orig_lines), len(mod_lines))
        for idx in range(max_len):
            old_line = orig_lines[idx] if idx < len(orig_lines) else None
            new_line = mod_lines[idx] if idx < len(mod_lines) else None

            if old_line == new_line:
                diff_lines.append({
                    "line_no": idx + 1,
                    "type": "unchanged",
                    "old_content": old_line or "",
                    "new_content": new_line or ""
                })
            elif old_line is not None and new_line is not None:
                diff_lines.append({
                    "line_no": idx + 1,
                    "type": "modified",
                    "old_content": old_line,
                    "new_content": new_line
                })
                added_count += 1
                deleted_count += 1
            elif old_line is not None:
                diff_lines.append({
                    "line_no": idx + 1,
                    "type": "deleted",
                    "old_content": old_line,
                    "new_content": ""
                })
                deleted_count += 1
            else:
                diff_lines.append({
                    "line_no": idx + 1,
                    "type": "added",
                    "old_content": "",
                    "new_content": new_line or ""
                })
                added_count += 1

        return {
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "added_lines": added_count,
            "deleted_lines": deleted_count,
            "total_changes": added_count + deleted_count,
            "original_code": original_text,
            "modified_code": modified_text,
            "lines": diff_lines
        }
