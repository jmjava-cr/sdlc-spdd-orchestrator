"""Run install / upgrade / verify scripts against a target project."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any


def orchestrator_root() -> Path:
    """Locate the SDLC-SPDD orchestrator repo (engine → repo root)."""
    # engine/src/sdlc_engine/installer/runner.py → repo root is parents[4]
    here = Path(__file__).resolve()
    candidate = here.parents[4]
    if (candidate / "scripts" / "setup-agent-prompts.sh").is_file():
        return candidate
    env = os.environ.get("SDLC_ORCHESTRATOR_ROOT", "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        if (p / "scripts" / "setup-agent-prompts.sh").is_file():
            return p
    raise FileNotFoundError(
        "Could not locate orchestrator scripts/. Set SDLC_ORCHESTRATOR_ROOT "
        "or run from an editable install of this repo."
    )


def _assistant_flags(assistants: list[str]) -> list[str]:
    flags: list[str] = []
    normalized = {a.strip().lower() for a in assistants if a and str(a).strip()}
    if "all" in normalized:
        return ["--all"]
    for name in ("cursor", "copilot", "claude"):
        if name in normalized:
            flags.append(f"--{name}")
    return flags


def run_action(
    *,
    action: str,
    target: Path | str,
    assistants: list[str] | None = None,
    dry_run: bool = False,
    force: bool = False,
    no_backup: bool = False,
    with_python_engine: bool = False,
    timeout_sec: int = 300,
) -> dict[str, Any]:
    """Execute install, upgrade, or verify. Returns log + exit code."""
    root = orchestrator_root()
    target_path = Path(target).expanduser().resolve()
    assistants = assistants or ["cursor", "copilot"]
    flags = _assistant_flags(assistants)

    if action == "install":
        script = root / "scripts" / "setup-agent-prompts.sh"
        cmd = [str(script), "--target", str(target_path), *flags]
        if force:
            cmd.append("--force")
        if dry_run:
            cmd.append("--dry-run")
    elif action == "upgrade":
        script = root / "scripts" / "upgrade-project.sh"
        cmd = [str(script), "--target", str(target_path), *flags]
        if dry_run:
            cmd.append("--dry-run")
        if no_backup:
            cmd.append("--no-backup")
    elif action == "verify":
        script = root / "scripts" / "verify-project-install.sh"
        cmd = [str(script), "--target", str(target_path)]
        selected = {a.strip().lower() for a in assistants if a and str(a).strip()}
        want_all = "all" in selected
        for name in ("cursor", "copilot", "claude"):
            if want_all or name in selected:
                cmd.append(f"--require-{name}")
    else:
        return {
            "ok": False,
            "exit_code": 2,
            "command": [],
            "log": f"Unknown action: {action}",
        }

    if not script.is_file():
        return {
            "ok": False,
            "exit_code": 2,
            "command": cmd,
            "log": f"Script not found: {script}",
        }

    proc = subprocess.run(
        cmd,
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=timeout_sec,
        check=False,
    )
    log = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    engine_log = ""
    if with_python_engine and action in {"install", "upgrade"} and proc.returncode == 0 and not dry_run:
        engine_log = _install_python_engine(root, target_path, timeout_sec=timeout_sec)
        log = (log + "\n" + engine_log).strip()

    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "command": cmd,
        "log": log.strip(),
        "engine_log": engine_log.strip() if engine_log else "",
    }


def _install_python_engine(root: Path, target: Path, *, timeout_sec: int) -> str:
    """Best-effort editable install of the engine into the active Python env."""
    engine_dir = root / "engine"
    if not (engine_dir / "pyproject.toml").is_file():
        return "Python engine: skipped (engine/pyproject.toml missing)"
    cmd = [
        "python3",
        "-m",
        "pip",
        "install",
        "-e",
        str(engine_dir),
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(target),
        capture_output=True,
        text=True,
        timeout=timeout_sec,
        check=False,
    )
    out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    status = "ok" if proc.returncode == 0 else f"failed (exit {proc.returncode})"
    return f"Python engine install ({status}):\n{out.strip()}"
