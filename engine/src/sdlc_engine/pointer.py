"""Local Work ID pointer (.sdlc/pointer)."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .project import Project


class PointerError(RuntimeError):
    pass


@dataclass
class PointerStore:
    project: Project

    def __post_init__(self) -> None:
        self.project.ensure_runtime_dirs()

    def get(self) -> str:
        path = self.project.pointer_path
        if not path.is_file():
            return ""
        return path.read_text(encoding="utf-8").strip()

    def set(self, work_id: str) -> str:
        if not work_id:
            raise PointerError("missing pointer id")
        path = self.project.pointer_path
        tmp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
        tmp.write_text(work_id, encoding="utf-8")
        tmp.replace(path)
        return work_id

    def reset(self) -> None:
        path = self.project.pointer_path
        if path.exists():
            path.unlink()

    def init_from_env(self) -> str | None:
        override = os.environ.get("SDLC_POINTER_OVERRIDE")
        if override:
            self.set(override)
            return override
        return None

    def run_against(self, expected: str, argv: list[str]) -> int:
        import subprocess

        current = self.get()
        if current != expected:
            raise PointerError(
                f"Pointer mismatch: current='{current}' expected='{expected}' — refusing to run"
            )
        if not argv:
            raise PointerError("run_against requires a command")
        return subprocess.call(argv, cwd=self.project.root)
