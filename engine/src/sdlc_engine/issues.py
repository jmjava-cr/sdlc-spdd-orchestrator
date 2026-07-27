"""Create/update Jira or GitHub issues from requirements/milestones drafts."""

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .jira_format import (
    adf_to_markdown,
    build_jira_markdown,
    markdown_to_adf,
    markdown_to_wiki,
)
from .links import (
    _JIRA_KEY_RE,
    collect_links,
    parse_milestone_requirement,
    set_milestone_bullet,
    set_milestone_subsection,
)
from .project import Project
from .sync_local import LocalSyncService

# Optional hooks for tests (inject fake gh / HTTP).
GhRunner = Callable[[list[str], Path], subprocess.CompletedProcess]
UrlOpener = Callable[..., object]


@dataclass
class IssueDraft:
    system: str  # jira | github
    work_id: str
    title: str
    body: str
    labels: list[str]
    extra: dict


def _default_gh_runner(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=False, capture_output=True, text=True)


class IssueSyncService:
    def __init__(
        self,
        project: Project | None = None,
        *,
        gh_runner: GhRunner | None = None,
        urlopen: UrlOpener | None = None,
    ) -> None:
        self.project = project or Project.resolve()
        self.local = LocalSyncService(self.project)
        self._gh_runner = gh_runner or _default_gh_runner
        self._urlopen = urlopen or urllib.request.urlopen

    def _github_repo(self) -> str:
        return (
            os.environ.get("SDLC_GITHUB_REPO")
            or os.environ.get("GH_REPO")
            or ""
        ).strip()

    def _gh_cmd(self, *parts: str) -> list[str]:
        cmd = ["gh", *parts]
        repo = self._github_repo()
        if repo:
            # Insert --repo after the gh subcommand group (issue create/view/close).
            # gh accepts: gh issue create --repo OWNER/NAME ...
            if len(cmd) >= 3 and cmd[1] == "issue":
                cmd[3:3] = ["--repo", repo]
            else:
                cmd.extend(["--repo", repo])
        return cmd

    def draft(self, work_id: str, system: str = "both") -> list[IssueDraft]:
        req = self.project.milestone_path(work_id)
        if not req.is_file():
            raise FileNotFoundError(f"missing requirements/milestones/{work_id}.md")
        parsed = parse_milestone_requirement(req)
        summary = parsed.get("jira_summary") or parsed.get("summary") or work_id
        summary = " ".join(summary.split())
        drafts: list[IssueDraft] = []
        systems = ["jira", "github"] if system == "both" else [system]
        if "jira" in systems:
            req_rel = f"requirements/milestones/{work_id}.md"
            body_md = build_jira_markdown(
                work_id=work_id,
                summary=summary,
                description=parsed.get("jira_description") or parsed.get("summary") or "",
                acceptance=parsed.get("jira_acceptance") or "",
                business_value=parsed.get("jira_business_value") or "",
                scope_in=parsed.get("jira_scope_in") or "",
                scope_out=parsed.get("jira_scope_out") or "",
                requirement_rel=req_rel,
            )
            labels = [x.strip() for x in (parsed.get("jira_labels") or "").split(",") if x.strip()]
            fmt = self._jira_description_format(os.environ.get("JIRA_BASE_URL", ""))
            extra = {
                "issuetype": parsed.get("jira_type") or "Story",
                "key": parsed.get("jira_key") or "",
                "project": os.environ.get("JIRA_PROJECT", ""),
                "components": parsed.get("jira_components") or "",
                "description_format": fmt,
                "description_wiki": markdown_to_wiki(body_md),
                "description_adf": markdown_to_adf(body_md),
            }
            drafts.append(
                IssueDraft(
                    system="jira",
                    work_id=work_id,
                    title=summary[:255] or work_id,
                    body=body_md,
                    labels=labels,
                    extra=extra,
                )
            )
        if "github" in systems:
            title = parsed.get("github_title") or summary or work_id
            body = parsed.get("github_body") or parsed.get("summary") or ""
            body = (
                body.strip()
                + f"\n\n---\nWork ID: `{work_id}`\nRequirement: `requirements/milestones/{work_id}.md`\n"
            )
            labels = [x.strip() for x in (parsed.get("github_labels") or "").split(",") if x.strip()]
            drafts.append(
                IssueDraft(
                    system="github",
                    work_id=work_id,
                    title=title[:256],
                    body=body.strip(),
                    labels=labels,
                    extra={"number": parsed.get("github_number") or ""},
                )
            )
        return drafts

    def push(self, work_id: str, system: str, *, apply: bool = False) -> str:
        if system not in {"jira", "github"}:
            raise ValueError("system must be jira or github")
        drafts = self.draft(work_id, system=system)
        draft = drafts[0]
        if system == "github" and draft.extra.get("number"):
            msg = (
                f"GitHub issue already linked as #{draft.extra['number']}; skip create."
            )
            return f"[dry-run] {msg}" if not apply else msg
        if system == "jira":
            key = draft.extra.get("key") or ""
            if key and _JIRA_KEY_RE.match(key):
                msg = f"Jira issue already linked as {key}; skip create."
                return f"[dry-run] {msg}" if not apply else msg
        if not apply:
            return self._format_dry_run(draft)
        if system == "github":
            return self._push_github(draft)
        return self._push_jira(draft)

    def _format_dry_run(self, draft: IssueDraft) -> str:
        lines = [
            f"[dry-run] would create {draft.system} issue for {draft.work_id}",
            f"title: {draft.title}",
            f"labels: {', '.join(draft.labels) or '-'}",
        ]
        if draft.system == "jira":
            fmt = draft.extra.get("description_format") or "adf"
            lines.append(f"description_format: {fmt} (Jira Cloud v3 uses ADF)")
            lines.append("body (markdown source):")
            lines.append(draft.body)
            if fmt == "adf":
                lines.append("body (ADF JSON):")
                lines.append(json.dumps(draft.extra.get("description_adf"), indent=2))
            else:
                lines.append("body (wiki markup):")
                lines.append(str(draft.extra.get("description_wiki") or ""))
        else:
            lines.append(f"extra: {json.dumps({k: v for k, v in draft.extra.items() if k != 'description_adf'})}")
            lines.append("body:")
            lines.append(draft.body)
        lines.extend(
            [
                "",
                "Re-run with --apply to create (requires gh auth or JIRA_* env).",
            ]
        )
        return "\n".join(lines)

    def _jira_api_version(self, base: str) -> str:
        explicit = os.environ.get("JIRA_API_VERSION", "").strip()
        if explicit in {"2", "3"}:
            return explicit
        # Cloud hosts need v3 + ADF; Server/DC often still on v2 wiki.
        if "atlassian.net" in base.lower():
            return "3"
        return os.environ.get("JIRA_API_VERSION_DEFAULT", "3")

    def _jira_description_format(self, base: str) -> str:
        explicit = os.environ.get("JIRA_DESCRIPTION_FORMAT", "").strip().lower()
        if explicit in {"adf", "wiki", "plain"}:
            return explicit
        return "adf" if self._jira_api_version(base) == "3" else "wiki"

    def _jira_description_payload(self, draft: IssueDraft, fmt: str):
        if fmt == "adf":
            return draft.extra.get("description_adf") or markdown_to_adf(draft.body)
        if fmt == "wiki":
            return draft.extra.get("description_wiki") or markdown_to_wiki(draft.body)
        return draft.body

    def _push_github(self, draft: IssueDraft) -> str:
        if draft.extra.get("number"):
            return f"GitHub issue already linked as #{draft.extra['number']}; skip create."
        if self._gh_runner is _default_gh_runner and not shutil.which("gh"):
            raise RuntimeError("gh CLI not found; install GitHub CLI or use --dry-run")
        cmd = self._gh_cmd("issue", "create", "--title", draft.title, "--body", draft.body)
        for label in draft.labels:
            cmd.extend(["--label", label])
        proc = self._gh_runner(cmd, self.project.root)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "gh issue create failed")
        url = proc.stdout.strip().splitlines()[-1].strip()
        num = ""
        if "/issues/" in url:
            num = url.rstrip("/").split("/issues/")[-1]
        req = self.project.milestone_path(draft.work_id)
        if num:
            set_milestone_bullet(req, "GitHub", "Number", num)
            set_milestone_bullet(req, "GitHub", "URL", url)
            set_milestone_bullet(req, "GitHub", "Title", draft.title)
        self.local.repair_links(draft.work_id)
        return f"Created GitHub issue {url}"

    def _jira_auth_header(self) -> str:
        email = os.environ.get("JIRA_EMAIL", "")
        token = os.environ.get("JIRA_API_TOKEN", "")
        return "Basic " + base64.b64encode(f"{email}:{token}".encode()).decode()

    def _push_jira(self, draft: IssueDraft) -> str:
        if draft.extra.get("key"):
            key = draft.extra["key"]
            if _JIRA_KEY_RE.match(key):
                return f"Jira issue already linked as {key}; skip create."
        base = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
        email = os.environ.get("JIRA_EMAIL", "")
        token = os.environ.get("JIRA_API_TOKEN", "")
        project = draft.extra.get("project") or os.environ.get("JIRA_PROJECT", "")
        if not (base and email and token and project):
            raise RuntimeError(
                "Jira push requires JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT"
            )
        api_ver = self._jira_api_version(base)
        fmt = self._jira_description_format(base)
        fields: dict = {
            "project": {"key": project},
            "summary": draft.title,
            "description": self._jira_description_payload(draft, fmt),
            "issuetype": {"name": draft.extra.get("issuetype") or "Story"},
        }
        if draft.labels:
            fields["labels"] = draft.labels
        # Components: comma-separated names → [{"name": ...}]
        comps = draft.extra.get("components") or ""
        comp_names = [c.strip() for c in comps.split(",") if c.strip()]
        if comp_names:
            fields["components"] = [{"name": c} for c in comp_names]

        def _post(version: str, description) -> dict:
            payload = {"fields": {**fields, "description": description}}
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{base}/rest/api/{version}/issue",
                data=data,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self._jira_auth_header(),
                    "Accept": "application/json",
                },
            )
            with self._urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())

        try:
            body = _post(api_ver, fields["description"])
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            # Auto-fallback: Cloud sometimes rejects wrong shape; try the other format once.
            if exc.code in {400, 415} and os.environ.get("JIRA_DESCRIPTION_FALLBACK", "1") != "0":
                alt_fmt = "wiki" if fmt == "adf" else "adf"
                alt_ver = "2" if alt_fmt == "wiki" else "3"
                try:
                    body = _post(alt_ver, self._jira_description_payload(draft, alt_fmt))
                    fmt, api_ver = alt_fmt, alt_ver
                except urllib.error.HTTPError as exc2:
                    detail2 = exc2.read().decode(errors="replace")
                    raise RuntimeError(
                        f"Jira create failed ({exc.code} via v{api_ver}/{fmt}): {detail}\n"
                        f"Fallback ({exc2.code} via v{alt_ver}/{alt_fmt}): {detail2}"
                    ) from exc2
            else:
                raise RuntimeError(f"Jira create failed ({exc.code}): {detail}") from exc
        key = body.get("key", "")
        if key:
            set_milestone_bullet(self.project.milestone_path(draft.work_id), "Jira", "Key", key)
            set_milestone_bullet(
                self.project.milestone_path(draft.work_id), "Jira", "Summary", draft.title
            )
            self.local.repair_links(draft.work_id)
        return (
            f"Created Jira issue {key} ({base}/browse/{key}) "
            f"[api=v{api_ver} description={fmt}]"
        )

    def pull(self, work_id: str, system: str, *, apply: bool = False) -> str:
        links = collect_links(self.project, work_id)
        if system == "github":
            num = links.github_number
            if not num:
                raise ValueError("no GitHub Number on milestone requirement")
            if self._gh_runner is _default_gh_runner and not shutil.which("gh"):
                raise RuntimeError("gh CLI not found")
            proc = self._gh_runner(
                self._gh_cmd(
                    "issue",
                    "view",
                    num,
                    "--json",
                    "title,state,url,labels,body",
                ),
                self.project.root,
            )
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr.strip() or "gh issue view failed")
            data = json.loads(proc.stdout)
            report = (
                f"GitHub #{num}: {data.get('title')} [{data.get('state')}]\n"
                f"URL: {data.get('url')}\n"
            )
            if apply:
                req = self.project.milestone_path(work_id)
                set_milestone_bullet(req, "GitHub", "Title", data.get("title") or "")
                set_milestone_bullet(req, "GitHub", "URL", data.get("url") or "")
                set_milestone_bullet(req, "GitHub", "Number", str(num))
                labels = data.get("labels") or []
                if isinstance(labels, list) and labels:
                    names = []
                    for lab in labels:
                        if isinstance(lab, dict) and lab.get("name"):
                            names.append(str(lab["name"]))
                        elif isinstance(lab, str):
                            names.append(lab)
                    if names:
                        set_milestone_bullet(req, "GitHub", "Labels", ", ".join(names))
                self.local.repair_links(work_id)
                report += "Applied into requirements/milestones + local links.\n"
            else:
                report += "Dry-run only; pass --apply to write milestone fields.\n"
            return report
        if system == "jira":
            key = links.jira_key
            if not key:
                raise ValueError("no Jira Key on milestone requirement")
            base = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
            email = os.environ.get("JIRA_EMAIL", "")
            token = os.environ.get("JIRA_API_TOKEN", "")
            if not (base and email and token):
                raise RuntimeError("Jira pull requires JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN")
            api_ver = self._jira_api_version(base)
            req = urllib.request.Request(
                f"{base}/rest/api/{api_ver}/issue/{key}?fields=summary,status,labels,description",
                method="GET",
                headers={
                    "Authorization": self._jira_auth_header(),
                    "Accept": "application/json",
                },
            )
            with self._urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
            fields = data.get("fields", {})
            summary = fields.get("summary", "")
            status = (fields.get("status") or {}).get("name", "")
            desc_raw = fields.get("description")
            desc_md = adf_to_markdown(desc_raw) if isinstance(desc_raw, dict) else (desc_raw or "")
            report = (
                f"Jira {key}: {summary} [{status}]\n"
                f"URL: {base}/browse/{key}\n"
                f"description_format: {'adf' if isinstance(desc_raw, dict) else 'text'}\n"
            )
            if desc_md:
                report += "description (markdown):\n" + desc_md.rstrip() + "\n"
            if apply:
                path = self.project.milestone_path(work_id)
                set_milestone_bullet(path, "Jira", "Summary", summary)
                set_milestone_bullet(path, "Jira", "Key", key)
                if desc_md.strip():
                    set_milestone_subsection(path, "Jira", "Description", desc_md.strip())
                self.local.repair_links(work_id)
                report += "Applied into requirements/milestones + local links.\n"
            else:
                report += "Dry-run only; pass --apply to write milestone fields.\n"
            return report
        raise ValueError("system must be jira or github")

    def close_github(self, number: str) -> str:
        """Best-effort close for integration-test cleanup."""
        proc = self._gh_runner(
            self._gh_cmd("issue", "close", str(number)),
            self.project.root,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "gh issue close failed")
        return f"Closed GitHub issue #{number}"
