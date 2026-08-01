"""Local ADF file store — browse any directory on the machine."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from sdlc_engine.jira_format import load_adf_document

_ADF_SUFFIXES = (".adf.json", ".json", ".txt")
# Block only NUL / empty; local tool — full filesystem is intentional.
_BAD = re.compile(r"[\x00]")


class AdfStoreError(ValueError):
    """Invalid path or ADF document."""


class AdfStore:
    def __init__(self, root: Path) -> None:
        """``root`` is the default start directory (usually cwd), not a jail."""
        self.root = Path(root).expanduser().resolve()
        self.adf_dir = (self.root / "adf").resolve()

    def ensure_dir(self) -> Path:
        self.adf_dir.mkdir(parents=True, exist_ok=True)
        return self.adf_dir

    def resolve_path(self, path_str: str) -> Path:
        """Resolve a user path. Absolute paths are used as-is; relative → under root.

        Bare filenames (no separator) map to ``adf/<name>`` for convenience.
        """
        raw = (path_str or "").strip()
        if not raw or _BAD.search(raw):
            raise AdfStoreError("invalid path")
        p = Path(raw).expanduser()
        if not p.is_absolute():
            text = raw.replace("\\", "/")
            if "/" not in text and not text.startswith("."):
                p = self.adf_dir / text
            else:
                p = (self.root / p).resolve()
        else:
            p = p.resolve()
        return p

    def resolve(self, name: str) -> Path:
        """Legacy: bare name or path → resolved Path."""
        return self.resolve_path(name)

    def resolve_dir(self, path_str: str | None) -> Path:
        if not (path_str or "").strip():
            return self.root
        path = self.resolve_path(path_str)
        if not path.exists():
            raise AdfStoreError(f"not found: {path}")
        if not path.is_dir():
            raise AdfStoreError(f"not a directory: {path}")
        return path

    def _candidate_name(self, name: str) -> bool:
        return name.endswith(".adf.json") or name.endswith(".json") or name.endswith(".txt")

    def list_files(self) -> list[str]:
        """Basenames of valid ADF docs in default ``adf/`` (index shortcut)."""
        if not self.adf_dir.is_dir():
            return []
        names: list[str] = []
        for p in sorted(self.adf_dir.iterdir()):
            if not p.is_file() or p.name.startswith("."):
                continue
            if not self._candidate_name(p.name):
                continue
            try:
                self.load_path(str(p))
            except (AdfStoreError, OSError, json.JSONDecodeError, ValueError):
                continue
            names.append(p.name)
        return names

    def browse(self, path_str: str | None = "") -> dict[str, Any]:
        """List directories + ADF candidates in any local directory."""
        dir_path = self.resolve_dir(path_str)
        dirs: list[dict[str, str]] = []
        files: list[dict[str, Any]] = []
        try:
            entries = list(dir_path.iterdir())
        except OSError as exc:
            raise AdfStoreError(f"cannot read directory: {exc}") from exc
        for p in sorted(entries, key=lambda x: (not x.is_dir(), x.name.lower())):
            if p.name.startswith("."):
                continue
            abs_s = str(p.resolve()) if p.exists() else str(p)
            if p.is_dir():
                dirs.append({"name": p.name, "path": abs_s, "kind": "dir"})
            elif p.is_file() and self._candidate_name(p.name):
                valid = False
                try:
                    self.load_path(abs_s)
                    valid = True
                except (AdfStoreError, OSError, json.JSONDecodeError, ValueError):
                    valid = False
                files.append(
                    {
                        "name": p.name,
                        "path": abs_s,
                        "kind": "file",
                        "valid": valid,
                    }
                )
        parent = str(dir_path.parent.resolve()) if dir_path.parent != dir_path else None
        return {
            "path": str(dir_path.resolve()),
            "parent": parent,
            "dirs": dirs,
            "files": files,
            "home": str(Path.home().resolve()),
            "root_start": str(self.root),
            "adf_dir": str(self.adf_dir),
        }

    def load_path(self, path_str: str) -> dict[str, Any]:
        path = self.resolve_path(path_str)
        if not path.is_file():
            raise AdfStoreError(f"not found: {path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise AdfStoreError(f"invalid JSON in {path}: {exc}") from exc
        try:
            return load_adf_document(data)
        except ValueError as exc:
            raise AdfStoreError(str(exc)) from exc

    def save_path(self, path_str: str, doc: dict[str, Any]) -> Path:
        path = self.resolve_path(path_str)
        try:
            validated = load_adf_document(doc)
        except ValueError as exc:
            raise AdfStoreError(str(exc)) from exc
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(validated, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return path

    def create_path(self, path_str: str, *, title: str | None = None) -> Path:
        path = self.resolve_path(path_str)
        if path.exists():
            raise AdfStoreError(f"already exists: {path}")
        heading = title or path.stem.replace(".adf", "")
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [{"type": "text", "text": heading}],
                },
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Description goes here."}],
                },
            ],
        }
        return self.save_path(str(path), doc)

    def load(self, name: str) -> dict[str, Any]:
        return self.load_path(name)

    def save(self, name: str, doc: dict[str, Any]) -> Path:
        return self.save_path(name, doc)

    def issue_key_from_name(self, name: str) -> str:
        base = Path(name).name
        stem = base
        for suf in _ADF_SUFFIXES:
            if stem.endswith(suf):
                stem = stem[: -len(suf)]
                break
        else:
            stem = Path(stem).stem
        return stem.upper() if re.fullmatch(r"[A-Za-z]+-\d+", stem) else stem

    def display_path(self, path_str: str) -> str:
        return str(self.resolve_path(path_str))
