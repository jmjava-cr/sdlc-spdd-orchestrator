"""Local regenerable SQLite index — lightweight store before GUIDE/Neo4j.

The binary DB lives under gitignored `.sdlc/index.sqlite`. Multi-user sync stays
git (markdown + work-registry.tsv). Rebuild anytime from on-disk artifacts.
Optional JSON/SQL export is for inspection or hand-off — not a shared live DB.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import canvas as canvas_mod
from .links import collect_links, note_token, parse_canvas_metadata, parse_milestone_requirement
from .project import Project
from .registry import TeamRegistry

SCHEMA_VERSION = "1"
DEFAULT_DB_NAME = "index.sqlite"

# Safe read-only query surface for `db query` convenience filters.
_SELECT_RE = re.compile(r"^\s*select\b", re.IGNORECASE | re.DOTALL)
_FORBIDDEN_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|attach|detach|pragma|create|replace)\b",
    re.IGNORECASE,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class RebuildStats:
    work_items: int = 0
    artifacts: int = 0
    local_sessions: int = 0
    path: str = ""
    rebuilt_at: str = ""
    source_commit: str = ""

    def as_text(self) -> str:
        return (
            f"Rebuilt SQLite index: {self.path}\n"
            f"  work_items: {self.work_items}\n"
            f"  artifacts: {self.artifacts}\n"
            f"  local_sessions: {self.local_sessions}\n"
            f"  source_commit: {self.source_commit or '(unknown)'}\n"
            f"  rebuilt_at: {self.rebuilt_at}\n"
        )


class LocalIndex:
    """Regenerable SQLite index of Work IDs, registry, and artifact paths."""

    def __init__(self, project: Project | None = None, db_path: Path | None = None) -> None:
        self.project = project or Project.resolve()
        self.project.ensure_runtime_dirs()
        self.db_path = db_path or (self.project.sdlc_dir / DEFAULT_DB_NAME)

    def connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _git_head(self) -> str:
        try:
            return subprocess.check_output(
                ["git", "-C", str(self.project.root), "rev-parse", "--short", "HEAD"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def _init_schema(self, conn: sqlite3.Connection) -> None:
        conn.executescript(
            """
            DROP TABLE IF EXISTS work_search;
            DROP TABLE IF EXISTS artifacts;
            DROP TABLE IF EXISTS local_sessions;
            DROP TABLE IF EXISTS work_items;
            DROP TABLE IF EXISTS meta;

            CREATE TABLE meta (
              key TEXT PRIMARY KEY,
              value TEXT NOT NULL
            );

            CREATE TABLE work_items (
              work_id TEXT PRIMARY KEY,
              title TEXT,
              work_type TEXT,
              canvas_status TEXT,
              final_status TEXT,
              milestone TEXT,
              source_system TEXT,
              source_issue TEXT,
              source_url TEXT,
              canvas_path TEXT,
              requirement_path TEXT,
              feature_path TEXT,
              registry_status TEXT,
              registry_owner TEXT,
              registry_phase TEXT,
              registry_note TEXT,
              jira_key TEXT,
              github_number TEXT,
              has_canvas INTEGER NOT NULL DEFAULT 0,
              has_requirement INTEGER NOT NULL DEFAULT 0,
              has_feature INTEGER NOT NULL DEFAULT 0,
              updated TEXT
            );

            CREATE TABLE artifacts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              work_id TEXT,
              kind TEXT NOT NULL,
              path TEXT NOT NULL,
              title TEXT,
              mtime TEXT,
              UNIQUE(kind, path)
            );

            CREATE TABLE local_sessions (
              session_id TEXT PRIMARY KEY,
              title TEXT,
              status TEXT,
              intent TEXT,
              owner TEXT,
              promoted_to TEXT,
              updated TEXT,
              path TEXT
            );
            """
        )
        # FTS5 when available; otherwise search falls back to LIKE.
        try:
            conn.execute(
                "CREATE VIRTUAL TABLE work_search USING fts5("
                "work_id, title, work_type, canvas_status, jira_key, github_number, "
                "registry_note, body, tokenize='porter')"
            )
            conn.execute(
                "INSERT INTO meta(key, value) VALUES ('fts', 'fts5')"
            )
        except sqlite3.OperationalError:
            conn.execute(
                "INSERT INTO meta(key, value) VALUES ('fts', 'like')"
            )
        conn.execute(
            "INSERT INTO meta(key, value) VALUES ('schema_version', ?)",
            (SCHEMA_VERSION,),
        )

    def rebuild(self) -> RebuildStats:
        stats = RebuildStats(path=str(self.db_path), rebuilt_at=_utc_now(), source_commit=self._git_head())
        with self.connect() as conn:
            self._init_schema(conn)
            registry = TeamRegistry(self.project)
            rows = {r.work_id: r for r in registry.rows()}
            work_ids = registry.discover_work_ids()
            fts = self._meta(conn, "fts") == "fts5"

            for wid in work_ids:
                reg = rows.get(wid)
                links = collect_links(self.project, wid, reg)
                meta: dict[str, str] = {}
                if links.canvas and links.canvas.is_file():
                    meta = parse_canvas_metadata(links.canvas)
                req_parsed: dict[str, str] = {}
                if links.milestone_req and links.milestone_req.is_file():
                    req_parsed = parse_milestone_requirement(links.milestone_req)
                final = ""
                if links.canvas and links.canvas.is_file():
                    kind = canvas_mod.final_kind(links.canvas)
                    final = kind or ""
                    # Prefer explicit Final Status text when present
                    text = links.canvas.read_text(encoding="utf-8")
                    m = re.search(
                        r"## Final Status.*?^\s*-\s*Status:\s*(.+)$",
                        text,
                        re.IGNORECASE | re.MULTILINE | re.DOTALL,
                    )
                    if m:
                        final = m.group(1).strip()

                title = meta.get("title") or req_parsed.get("jira_summary") or wid
                jira = links.jira_key or (note_token(reg.note, "jira") if reg else "")
                gh = links.github_number or ""
                if reg and not gh:
                    tok = note_token(reg.note, "github")
                    gh = tok.lstrip("#") if tok else ""

                canvas_rel = self._rel(links.canvas) if links.canvas and links.canvas.is_file() else ""
                req_rel = (
                    self._rel(links.milestone_req)
                    if links.milestone_req and links.milestone_req.is_file()
                    else ""
                )
                feat = self.project.feature_dir(wid)
                feat_rel = self._rel(feat) if feat.is_dir() else ""

                conn.execute(
                    """
                    INSERT INTO work_items(
                      work_id, title, work_type, canvas_status, final_status, milestone,
                      source_system, source_issue, source_url,
                      canvas_path, requirement_path, feature_path,
                      registry_status, registry_owner, registry_phase, registry_note,
                      jira_key, github_number,
                      has_canvas, has_requirement, has_feature, updated
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        wid,
                        title,
                        meta.get("work_type") or "",
                        meta.get("status") or "",
                        final,
                        meta.get("milestone") or "",
                        meta.get("source_system") or links.canvas_source_system or "",
                        meta.get("source_issue") or links.canvas_source_issue or "",
                        meta.get("source_url") or links.canvas_source_url or "",
                        canvas_rel,
                        req_rel,
                        feat_rel,
                        reg.status if reg else "available",
                        reg.owner if reg else "",
                        reg.phase if reg else "",
                        reg.note if reg else "",
                        jira,
                        gh,
                        1 if canvas_rel else 0,
                        1 if req_rel else 0,
                        1 if feat_rel else 0,
                        reg.updated if reg else stats.rebuilt_at,
                    ),
                )
                stats.work_items += 1

                body_bits = [title, meta.get("status") or "", jira, gh, reg.note if reg else ""]
                if links.milestone_req and links.milestone_req.is_file():
                    body_bits.append(req_parsed.get("summary") or "")
                    body_bits.append(req_parsed.get("jira_description") or "")

                for kind, path in self._artifact_paths(wid, links, feat):
                    if not path.is_file() and not (kind == "feature" and path.is_dir()):
                        continue
                    mtime = ""
                    try:
                        mtime = datetime.fromtimestamp(
                            path.stat().st_mtime, tz=timezone.utc
                        ).strftime("%Y-%m-%dT%H:%M:%SZ")
                    except OSError:
                        pass
                    conn.execute(
                        "INSERT OR REPLACE INTO artifacts(work_id, kind, path, title, mtime) "
                        "VALUES (?,?,?,?,?)",
                        (wid, kind, self._rel(path), title if kind == "canvas" else "", mtime),
                    )
                    stats.artifacts += 1

                if fts:
                    conn.execute(
                        "INSERT INTO work_search(work_id, title, work_type, canvas_status, "
                        "jira_key, github_number, registry_note, body) VALUES (?,?,?,?,?,?,?,?)",
                        (
                            wid,
                            title,
                            meta.get("work_type") or "",
                            meta.get("status") or "",
                            jira,
                            gh,
                            reg.note if reg else "",
                            "\n".join(x for x in body_bits if x),
                        ),
                    )

            # Local sessions (machine-private)
            local_root = self.project.sdlc_dir / "local-sessions"
            if local_root.is_dir():
                for meta_path in sorted(local_root.glob("*/session.json")):
                    try:
                        data = json.loads(meta_path.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        continue
                    sid = data.get("id") or meta_path.parent.name
                    conn.execute(
                        "INSERT OR REPLACE INTO local_sessions("
                        "session_id, title, status, intent, owner, promoted_to, updated, path) "
                        "VALUES (?,?,?,?,?,?,?,?)",
                        (
                            sid,
                            data.get("title") or "",
                            data.get("status") or "",
                            data.get("intent") or "",
                            data.get("owner") or "",
                            data.get("promoted_to") or "",
                            data.get("updated") or "",
                            self._rel(meta_path.parent),
                        ),
                    )
                    stats.local_sessions += 1

            conn.execute(
                "INSERT OR REPLACE INTO meta(key, value) VALUES ('rebuilt_at', ?)",
                (stats.rebuilt_at,),
            )
            conn.execute(
                "INSERT OR REPLACE INTO meta(key, value) VALUES ('source_commit', ?)",
                (stats.source_commit,),
            )
            conn.commit()
        return stats

    def _rel(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.project.root.resolve()))
        except ValueError:
            return str(path)

    def _artifact_paths(self, wid: str, links, feat: Path) -> list[tuple[str, Path]]:
        out: list[tuple[str, Path]] = []
        if links.canvas:
            out.append(("canvas", links.canvas))
        if links.milestone_req:
            out.append(("requirement", links.milestone_req))
        if feat.is_dir():
            out.append(("feature", feat))
        analysis = self.project.analysis_path(wid)
        if analysis.is_file():
            out.append(("analysis", analysis))
        review = self.project.review_path(wid)
        if review.is_file():
            out.append(("review", review))
        sync = self.project.sync_path(wid)
        if sync.is_file():
            out.append(("sync", sync))
        return out

    def _meta(self, conn: sqlite3.Connection, key: str) -> str:
        row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else ""

    def status_text(self) -> str:
        if not self.db_path.is_file():
            return (
                f"SQLite index missing: {self.db_path}\n"
                "Rebuild: ./scripts/sdlc.sh db rebuild\n"
            )
        with self.connect() as conn:
            try:
                n_work = conn.execute("SELECT COUNT(*) AS n FROM work_items").fetchone()["n"]
                n_art = conn.execute("SELECT COUNT(*) AS n FROM artifacts").fetchone()["n"]
                n_local = conn.execute("SELECT COUNT(*) AS n FROM local_sessions").fetchone()["n"]
            except sqlite3.Error as exc:
                return f"SQLite index unreadable ({exc}). Run: ./scripts/sdlc.sh db rebuild\n"
            return (
                f"SQLite index: {self.db_path}\n"
                f"  schema: {self._meta(conn, 'schema_version') or '?'}\n"
                f"  fts: {self._meta(conn, 'fts') or '?'}\n"
                f"  rebuilt_at: {self._meta(conn, 'rebuilt_at') or '?'}\n"
                f"  source_commit: {self._meta(conn, 'source_commit') or '?'}\n"
                f"  work_items: {n_work}\n"
                f"  artifacts: {n_art}\n"
                f"  local_sessions: {n_local}\n"
                "\n"
                "Multi-user sync: git (markdown + work-registry.tsv), not this file.\n"
                "Before GUIDE/Neo4j this is a local query cache only.\n"
            )

    def ensure(self) -> None:
        if not self.db_path.is_file():
            self.rebuild()

    def query_sql(self, sql: str, params: Iterable[Any] = ()) -> list[dict[str, Any]]:
        sql = sql.strip().rstrip(";")
        if not _SELECT_RE.match(sql) or _FORBIDDEN_SQL.search(sql):
            raise ValueError("db query only allows a single read-only SELECT statement")
        self.ensure()
        with self.connect() as conn:
            cur = conn.execute(sql, tuple(params))
            cols = [d[0] for d in cur.description or []]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def find(
        self,
        *,
        work_id: str = "",
        status: str = "",
        search: str = "",
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        self.ensure()
        limit = max(1, min(limit, 500))
        with self.connect() as conn:
            if search:
                fts = self._meta(conn, "fts")
                if fts == "fts5":
                    rows = conn.execute(
                        "SELECT w.* FROM work_items w "
                        "WHERE w.work_id IN ("
                        "  SELECT work_id FROM work_search WHERE work_search MATCH ?"
                        ") ORDER BY w.work_id LIMIT ?",
                        (search, limit),
                    ).fetchall()
                else:
                    like = f"%{search}%"
                    rows = conn.execute(
                        "SELECT * FROM work_items WHERE "
                        "work_id LIKE ? OR title LIKE ? OR jira_key LIKE ? "
                        "OR github_number LIKE ? OR registry_note LIKE ? "
                        "LIMIT ?",
                        (like, like, like, like, like, limit),
                    ).fetchall()
                return [dict(r) for r in rows]
            clauses: list[str] = []
            params: list[Any] = []
            if work_id:
                clauses.append("work_id = ?")
                params.append(work_id)
            if status:
                clauses.append("(registry_status = ? OR canvas_status = ? OR final_status = ?)")
                params.extend([status, status, status])
            where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
            params.append(limit)
            rows = conn.execute(
                f"SELECT * FROM work_items{where} ORDER BY work_id LIMIT ?",
                params,
            ).fetchall()
            return [dict(r) for r in rows]

    def export_json(self, path: Path | None = None) -> str:
        self.ensure()
        with self.connect() as conn:
            payload = {
                "schema_version": self._meta(conn, "schema_version"),
                "rebuilt_at": self._meta(conn, "rebuilt_at"),
                "source_commit": self._meta(conn, "source_commit"),
                "work_items": [
                    dict(r) for r in conn.execute("SELECT * FROM work_items ORDER BY work_id")
                ],
                "artifacts": [
                    dict(r) for r in conn.execute("SELECT * FROM artifacts ORDER BY work_id, kind")
                ],
                "local_sessions": [
                    dict(r) for r in conn.execute("SELECT * FROM local_sessions ORDER BY session_id")
                ],
            }
        text = json.dumps(payload, indent=2) + "\n"
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return text

    def export_sql(self, path: Path | None = None) -> str:
        self.ensure()
        lines = [
            f"-- SDLC local index dump ({_utc_now()})",
            f"-- source: {self.db_path}",
            "BEGIN;",
        ]
        with self.connect() as conn:
            for line in conn.iterdump():
                lines.append(line)
        lines.append("COMMIT;")
        text = "\n".join(lines) + "\n"
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return text


def format_rows(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "(no rows)\n"
    cols = columns or list(rows[0].keys())
    widths = {c: len(c) for c in cols}
    for row in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(row.get(c, "") or "")))
    header = "  ".join(c.ljust(widths[c]) for c in cols)
    sep = "  ".join("-" * widths[c] for c in cols)
    lines = [header, sep]
    for row in rows:
        lines.append("  ".join(str(row.get(c, "") or "").ljust(widths[c]) for c in cols))
    return "\n".join(lines) + "\n"
