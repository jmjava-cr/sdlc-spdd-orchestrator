"""Create/update Jira or GitHub issues from requirements/milestones drafts."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .links import (
    collect_links,
    parse_milestone_requirement,
    set_milestone_bullet,
)
from .project import Project
from .sync_local import LocalSyncService


@dataclass
class IssueDraft:
    system: str  # jira | github
    work_id: str
    title: str
    body: str
    labels: list[str]
    extra: dict


class IssueSyncService:
    def __init__(self, project: Project | None = None) -> None:
        self.project = project or Project.resolve()
        self.local = LocalSyncService(self.project)

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
            body_parts = [
                parsed.get("jira_description") or parsed.get("summary") or "",
                "",
                "### Acceptance criteria",
                parsed.get("jira_acceptance") or "",
                "",
                f"Work ID: `{work_id}`",
                f"Requirement: `requirements/milestones/{work_id}.md`",
            ]
            labels = [x.strip() for x in (parsed.get("jira_labels") or "").split(",") if x.strip()]
            drafts.append(
                IssueDraft(
                    system="jira",
                    work_id=work_id,
                    title=summary[:255] or work_id,
                    body="\n".join(body_parts).strip(),
                    labels=labels,
                    extra={
                        "issuetype": parsed.get("jira_type") or "Story",
                        "key": parsed.get("jira_key") or "",
                        "project": os.environ.get("JIRA_PROJECT", ""),
                    },
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
            from .links import _JIRA_KEY_RE

            if key and _JIRA_KEY_RE.match(key):
                msg = f"Jira issue already linked as {key}; skip create."
                return f"[dry-run] {msg}" if not apply else msg
        if not apply:
            return self._format_dry_run(draft)
        if system == "github":
            return self._push_github(draft)
        return self._push_jira(draft)

    def _format_dry_run(self, draft: IssueDraft) -> str:
        return "\n".join(
            [
                f"[dry-run] would create {draft.system} issue for {draft.work_id}",
                f"title: {draft.title}",
                f"labels: {', '.join(draft.labels) or '-'}",
                f"extra: {json.dumps(draft.extra)}",
                "body:",
                draft.body,
                "",
                "Re-run with --apply to create (requires gh auth or JIRA_* env).",
            ]
        )

    def _push_github(self, draft: IssueDraft) -> str:
        if draft.extra.get("number"):
            return f"GitHub issue already linked as #{draft.extra['number']}; skip create."
        if not shutil.which("gh"):
            raise RuntimeError("gh CLI not found; install GitHub CLI or use --dry-run")
        cmd = [
            "gh",
            "issue",
            "create",
            "--title",
            draft.title,
            "--body",
            draft.body,
        ]
        for label in draft.labels:
            cmd.extend(["--label", label])
        proc = subprocess.run(
            cmd,
            cwd=self.project.root,
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "gh issue create failed")
        url = proc.stdout.strip()
        # extract number
        num = ""
        if "/issues/" in url:
            num = url.rstrip("/").split("/issues/")[-1]
        req = self.project.milestone_path(draft.work_id)
        if num:
            set_milestone_bullet(req, "GitHub", "Number", num)
            set_milestone_bullet(req, "GitHub", "URL", url)
            set_milestone_bullet(req, "GitHub", "Title", draft.title)
        # repair local links
        self.local.repair_links(draft.work_id)
        return f"Created GitHub issue {url}"

    def _push_jira(self, draft: IssueDraft) -> str:
        if draft.extra.get("key"):
            # already has a real key?
            key = draft.extra["key"]
            from .links import _JIRA_KEY_RE

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
        payload = {
            "fields": {
                "project": {"key": project},
                "summary": draft.title,
                "description": draft.body,
                "issuetype": {"name": draft.extra.get("issuetype") or "Story"},
            }
        }
        # Jira Cloud often wants ADF for description; send plain string first — many sites still accept it
        # via legacy. If it fails, user can paste from draft.
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{base}/rest/api/2/issue",
            data=data,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        import base64

        auth = base64.b64encode(f"{email}:{token}".encode()).decode()
        req.add_header("Authorization", f"Basic {auth}")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise RuntimeError(f"Jira create failed ({exc.code}): {detail}") from exc
        key = body.get("key", "")
        if key:
            set_milestone_bullet(self.project.milestone_path(draft.work_id), "Jira", "Key", key)
            set_milestone_bullet(self.project.milestone_path(draft.work_id), "Jira", "Summary", draft.title)
            self.local.repair_links(draft.work_id)
        return f"Created Jira issue {key} ({base}/browse/{key})"

    def pull(self, work_id: str, system: str, *, apply: bool = False) -> str:
        links = collect_links(self.project, work_id)
        if system == "github":
            num = links.github_number
            if not num:
                raise ValueError("no GitHub Number on milestone requirement")
            if not shutil.which("gh"):
                raise RuntimeError("gh CLI not found")
            proc = subprocess.run(
                ["gh", "issue", "view", num, "--json", "title,state,url,labels,body"],
                cwd=self.project.root,
                check=False,
                capture_output=True,
                text=True,
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
            import base64

            req = urllib.request.Request(
                f"{base}/rest/api/2/issue/{key}?fields=summary,status,labels",
                method="GET",
            )
            auth = base64.b64encode(f"{email}:{token}".encode()).decode()
            req.add_header("Authorization", f"Basic {auth}")
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
            fields = data.get("fields", {})
            summary = fields.get("summary", "")
            status = (fields.get("status") or {}).get("name", "")
            report = f"Jira {key}: {summary} [{status}]\nURL: {base}/browse/{key}\n"
            if apply:
                path = self.project.milestone_path(work_id)
                set_milestone_bullet(path, "Jira", "Summary", summary)
                set_milestone_bullet(path, "Jira", "Key", key)
                self.local.repair_links(work_id)
                report += "Applied into requirements/milestones + local links.\n"
            else:
                report += "Dry-run only; pass --apply to write milestone fields.\n"
            return report
        raise ValueError("system must be jira or github")
