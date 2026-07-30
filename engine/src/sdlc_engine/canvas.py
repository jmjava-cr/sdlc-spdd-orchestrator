"""REASONS Canvas helpers: Final Status and next operation inference."""

from __future__ import annotations

import re
from pathlib import Path


def final_status_text(canvas_path: Path) -> str:
    if not canvas_path.is_file():
        return ""
    text = canvas_path.read_text(encoding="utf-8")
    in_final = False
    for line in text.splitlines():
        if line.startswith("## Final Status"):
            in_final = True
            continue
        if in_final and line.startswith("## "):
            break
        if in_final and line.startswith("- Status:"):
            return line.split(":", 1)[1].strip()
    return ""


def final_kind(canvas_path: Path) -> str:
    """Return complete | cancelled | other."""
    line = final_status_text(canvas_path).lower()
    if not line:
        return "other"
    if "cancel" in line:
        return "cancelled"
    if "complete" in line and "in progress" not in line:
        return "complete"
    return "other"


def is_archivable(canvas_path: Path) -> bool:
    return final_kind(canvas_path) in {"complete", "cancelled"}


_OP_HEADER = re.compile(r"^###\s+(T\d+)\s*[-–—:]\s*(.+)$")
_OP_STATUS = re.compile(r"^- Status:\s*(.+)$", re.IGNORECASE)


def next_operation(canvas_path: Path) -> tuple[str, str]:
    """Return (operation_id, title) for the first incomplete Operation, else ('', '')."""
    if not canvas_path.is_file():
        return "", ""
    current_op = ""
    current_title = ""
    in_ops = False
    for line in canvas_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## O") or line.startswith("## Operations"):
            in_ops = True
            continue
        if in_ops and line.startswith("## ") and not line.startswith("## O"):
            break
        if not in_ops:
            continue
        m = _OP_HEADER.match(line.strip())
        if m:
            current_op, current_title = m.group(1), m.group(2).strip()
            continue
        if current_op:
            sm = _OP_STATUS.match(line.strip())
            if sm:
                status = sm.group(1).strip().lower()
                if "complete" not in status and "done" not in status:
                    return current_op, current_title
                current_op, current_title = "", ""
    return "", ""
