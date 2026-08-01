"""Detect whether a target path needs a fresh install or an upgrade."""

from __future__ import annotations

from pathlib import Path
from typing import Any


MARKERS = (
    "scripts/sdlc-spdd/sdlc.sh",
    "agent-context/sdlc-workflow.sh",
    "agent-context/work-registry.tsv",
    ".cursor/commands/sdlc-spdd-init.md",
    ".github/prompts/sdlc-spdd-init.prompt.md",
    ".claude/commands/sdlc-spdd-init.md",
)


def detect_target(target: Path | str) -> dict[str, Any]:
    """Return install-mode diagnosis for ``target``."""
    root = Path(target).expanduser().resolve()
    exists = root.is_dir()
    markers_found: list[str] = []
    if exists:
        for rel in MARKERS:
            if (root / rel).exists():
                markers_found.append(rel)

    has_cursor = (root / ".cursor/commands/sdlc-spdd-init.md").is_file() if exists else False
    has_copilot = (root / ".github/prompts/sdlc-spdd-init.prompt.md").is_file() if exists else False
    has_claude = (root / ".claude/commands/sdlc-spdd-init.md").is_file() if exists else False

    if not exists:
        mode = "missing"
        recommendation = "create"
    elif markers_found:
        mode = "upgrade"
        recommendation = "upgrade"
    else:
        mode = "fresh"
        recommendation = "install"

    return {
        "path": str(root),
        "exists": exists,
        "mode": mode,
        "recommendation": recommendation,
        "markers": markers_found,
        "assistants": {
            "cursor": has_cursor,
            "copilot": has_copilot,
            "claude": has_claude,
        },
    }
