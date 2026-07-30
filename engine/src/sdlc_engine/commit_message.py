"""Collect git change sets for commit-message drafting (generate only).

Computes staged / unstaged / ahead-of-base diffs so assistant commands can draft
a commit message from a stable engine report instead of ad-hoc git calls.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass, field
from typing import Literal

from .pointer import PointerStore
from .project import Project

DiffSource = Literal["staged", "unstaged", "ahead-of-base"]


class CommitMessageError(RuntimeError):
    """Raised when git fails or there is nothing to message."""


@dataclass
class DiffSnapshot:
    source: DiffSource
    files: list[str] = field(default_factory=list)
    diff_text: str = ""
    status_porcelain: str = ""
    base_ref: str | None = None
    base_sha: str | None = None
    ahead_commits: list[str] = field(default_factory=list)
    work_id: str = ""
    hint: str = ""

    def as_dict(self) -> dict:
        return asdict(self)


class CommitMessageService:
    def __init__(self, project: Project) -> None:
        self.project = project
        self.root = project.root

    def _git(self, *args: str, check: bool = True) -> str:
        try:
            proc = subprocess.run(
                ["git", "-C", str(self.root), *args],
                check=False,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise CommitMessageError("git is not available on PATH") from exc
        if check and proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
            raise CommitMessageError(f"git {' '.join(args)} failed: {err}")
        return proc.stdout

    def resolve_base(self, preferred: str | None = None) -> tuple[str, str]:
        """Return (ref, merge-base-sha) for the default upstream branch."""
        candidates: list[str] = []
        if preferred:
            candidates.append(preferred)
        candidates.extend(["origin/main", "main", "origin/master", "master"])
        ordered: list[str] = []
        seen: set[str] = set()
        for c in candidates:
            if c not in seen:
                seen.add(c)
                ordered.append(c)

        for ref in ordered:
            show = self._git("rev-parse", "--verify", ref, check=False).strip()
            if not show:
                continue
            mb = self._git("merge-base", "HEAD", ref, check=False).strip()
            if mb:
                return ref, mb
        raise CommitMessageError(
            "could not resolve a merge base (tried origin/main, main, origin/master, master)"
        )

    def _name_only(self, *diff_args: str) -> list[str]:
        out = self._git("diff", "--name-only", *diff_args, check=False)
        return [line for line in out.splitlines() if line.strip()]

    def _untracked_files(self) -> list[str]:
        out = self._git("ls-files", "--others", "--exclude-standard", check=False)
        return [line for line in out.splitlines() if line.strip()]

    def collect(
        self,
        *,
        base: str | None = None,
        work_id: str = "",
        hint: str = "",
        max_diff_chars: int = 80_000,
    ) -> DiffSnapshot:
        status = self._git("status", "--porcelain", check=False)
        staged_files = self._name_only("--cached")
        unstaged_files = self._name_only()
        untracked = self._untracked_files()

        if not work_id:
            work_id = PointerStore(self.project).get() or ""

        if staged_files:
            diff = self._git("diff", "--cached", check=False)
            snap = DiffSnapshot(
                source="staged",
                files=staged_files,
                diff_text=_truncate(diff, max_diff_chars),
                status_porcelain=status,
                work_id=work_id,
                hint=hint,
            )
            return snap

        if unstaged_files or untracked:
            diff = self._git("diff", check=False)
            files = list(dict.fromkeys([*unstaged_files, *untracked]))
            # include brief untracked listing when no tracked unstaged hunks
            if untracked and not diff.strip():
                listed = "\n".join(f"??? {p}" for p in untracked)
                diff = f"# Untracked files (contents not inlined)\n{listed}\n"
            snap = DiffSnapshot(
                source="unstaged",
                files=files,
                diff_text=_truncate(diff, max_diff_chars),
                status_porcelain=status,
                work_id=work_id,
                hint=hint,
            )
            return snap

        base_ref, base_sha = self.resolve_base(base)
        ahead_files = self._name_only(f"{base_sha}...HEAD")
        log = self._git(
            "log",
            "--oneline",
            f"{base_sha}..HEAD",
            check=False,
        )
        commits = [line for line in log.splitlines() if line.strip()]
        if not ahead_files and not commits:
            raise CommitMessageError(
                "nothing to commit: working tree clean and branch is not ahead of base "
                f"({base_ref})"
            )
        diff = self._git("diff", f"{base_sha}...HEAD", check=False)
        return DiffSnapshot(
            source="ahead-of-base",
            files=ahead_files,
            diff_text=_truncate(diff, max_diff_chars),
            status_porcelain=status,
            base_ref=base_ref,
            base_sha=base_sha,
            ahead_commits=commits,
            work_id=work_id,
            hint=hint,
        )

    def report_text(
        self,
        *,
        base: str | None = None,
        work_id: str = "",
        hint: str = "",
        max_diff_chars: int = 80_000,
    ) -> str:
        snap = self.collect(
            base=base, work_id=work_id, hint=hint, max_diff_chars=max_diff_chars
        )
        return format_snapshot_text(snap)

    def report_json(
        self,
        *,
        base: str | None = None,
        work_id: str = "",
        hint: str = "",
        max_diff_chars: int = 80_000,
    ) -> str:
        snap = self.collect(
            base=base, work_id=work_id, hint=hint, max_diff_chars=max_diff_chars
        )
        return json.dumps(snap.as_dict(), indent=2) + "\n"


def format_snapshot_text(snap: DiffSnapshot) -> str:
    lines = [
        "SDLC commit-message diff report (generate only — does not commit)",
        f"source: {snap.source}",
        f"work_id: {snap.work_id or '(none)'}",
        f"hint: {snap.hint or '(none)'}",
    ]
    if snap.base_ref:
        lines.append(f"base_ref: {snap.base_ref}")
    if snap.base_sha:
        lines.append(f"base_sha: {snap.base_sha}")
    if snap.ahead_commits:
        lines.append(f"ahead_commits: {len(snap.ahead_commits)}")
        for c in snap.ahead_commits[:30]:
            lines.append(f"  - {c}")
        if len(snap.ahead_commits) > 30:
            lines.append(f"  … {len(snap.ahead_commits) - 30} more")
    lines.append(f"files ({len(snap.files)}):")
    for path in snap.files[:100]:
        lines.append(f"  - {path}")
    if len(snap.files) > 100:
        lines.append(f"  … {len(snap.files) - 100} more")
    if snap.status_porcelain.strip():
        lines.append("status_porcelain:")
        lines.append(snap.status_porcelain.rstrip())
    lines.append("diff:")
    lines.append(snap.diff_text.rstrip() or "(empty)")
    lines.append("")
    lines.append(
        "Next: draft a paste-ready commit subject (+ optional body) from this report. "
        "Do not run git commit unless the user explicitly asks after reviewing the draft."
    )
    return "\n".join(lines) + "\n"


def _truncate(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    omitted = len(text) - max_chars
    return text[:max_chars] + f"\n\n… [truncated {omitted} chars]\n"
