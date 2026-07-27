"""Jira description formatting: markdown ↔ ADF / wiki markup.

Jira Cloud REST v3 requires Atlassian Document Format (ADF) for `description`.
Plain markdown strings either fail create or render as unformatted blobs — the
main pain point when syncing from `requirements/milestones/ ## Jira`.
"""

from __future__ import annotations

import re
from typing import Any

# ---------------------------------------------------------------------------
# Structured body from milestone fields
# ---------------------------------------------------------------------------


def build_jira_markdown(
    *,
    work_id: str,
    summary: str = "",
    description: str = "",
    acceptance: str = "",
    business_value: str = "",
    scope_in: str = "",
    scope_out: str = "",
    requirement_rel: str = "",
) -> str:
    """Compose a consistently structured markdown description for Jira."""
    parts: list[str] = []

    def _add(heading: str, body: str) -> None:
        body = (body or "").strip()
        if not body:
            return
        parts.append(f"## {heading}")
        parts.append("")
        parts.append(body)
        parts.append("")

    _add("Summary", summary)
    _add("Description", description)
    _add("Business value", business_value)
    _add("Scope in", scope_in)
    _add("Scope out", scope_out)
    _add("Acceptance criteria", acceptance)

    parts.append("## Traceability")
    parts.append("")
    parts.append(f"- Work ID: `{work_id}`")
    if requirement_rel:
        parts.append(f"- Requirement: `{requirement_rel}`")
    parts.append("")
    return "\n".join(parts).strip() + "\n"


# ---------------------------------------------------------------------------
# Markdown → ADF
# ---------------------------------------------------------------------------


def _text_nodes(text: str) -> list[dict[str, Any]]:
    """Parse a single line of markdown into ADF inline text nodes."""
    if not text:
        return []
    nodes: list[dict[str, Any]] = []
    # Links, bold, italic, code — left-to-right scan
    token = re.compile(
        r"(`([^`]+)`)"
        r"|(\*\*([^*]+)\*\*)"
        r"|(\*([^*]+)\*)"
        r"|(\[([^\]]+)\]\(([^)]+)\))"
        r"|(_([^_]+)_)"
    )
    pos = 0
    for m in token.finditer(text):
        if m.start() > pos:
            nodes.append({"type": "text", "text": text[pos : m.start()]})
        if m.group(2) is not None:  # code
            nodes.append({"type": "text", "text": m.group(2), "marks": [{"type": "code"}]})
        elif m.group(4) is not None:  # **bold**
            nodes.append({"type": "text", "text": m.group(4), "marks": [{"type": "strong"}]})
        elif m.group(6) is not None:  # *italic*
            nodes.append({"type": "text", "text": m.group(6), "marks": [{"type": "em"}]})
        elif m.group(8) is not None:  # [label](url)
            nodes.append(
                {
                    "type": "text",
                    "text": m.group(8),
                    "marks": [{"type": "link", "attrs": {"href": m.group(9)}}],
                }
            )
        elif m.group(11) is not None:  # _italic_
            nodes.append({"type": "text", "text": m.group(11), "marks": [{"type": "em"}]})
        pos = m.end()
    if pos < len(text):
        nodes.append({"type": "text", "text": text[pos:]})
    # ADF disallows empty text nodes
    return [n for n in nodes if n.get("text") != ""]


def _paragraph(text: str) -> dict[str, Any]:
    content = _text_nodes(text.strip())
    if not content:
        # Empty paragraph still valid as hardBreak container — use a space.
        content = [{"type": "text", "text": " "}]
    return {"type": "paragraph", "content": content}


def _heading(level: int, text: str) -> dict[str, Any]:
    level = max(1, min(level, 6))
    content = _text_nodes(text.strip()) or [{"type": "text", "text": text.strip() or " "}]
    return {"type": "heading", "attrs": {"level": level}, "content": content}


def _code_block(text: str, language: str = "") -> dict[str, Any]:
    node: dict[str, Any] = {
        "type": "codeBlock",
        "content": [{"type": "text", "text": text.rstrip("\n") or " "}],
    }
    if language:
        node["attrs"] = {"language": language}
    return node


def _rule() -> dict[str, Any]:
    return {"type": "rule"}


def _list(items: list[tuple[str, str]], ordered: bool = False) -> dict[str, Any]:
    """items: list of (marker, text) where marker is '', 'todo', or 'done'."""
    list_items = []
    for marker, text in items:
        para = _paragraph(text)
        if marker == "todo":
            # Task items use taskList in newer ADF; keep bullet + [ ] prefix for compatibility.
            para = _paragraph(f"[ ] {text}")
        elif marker == "done":
            para = _paragraph(f"[x] {text}")
        list_items.append({"type": "listItem", "content": [para]})
    return {"type": "orderedList" if ordered else "bulletList", "content": list_items}


def markdown_to_adf(markdown: str) -> dict[str, Any]:
    """Convert a constrained markdown subset to Atlassian Document Format."""
    lines = (markdown or "").replace("\r\n", "\n").split("\n")
    content: list[dict[str, Any]] = []
    i = 0
    bullet_re = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
    check_re = re.compile(r"^\[([ xX])\]\s+(.*)$")

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            buf: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            content.append(_code_block("\n".join(buf), lang))
            continue

        # Horizontal rule
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            content.append(_rule())
            i += 1
            continue

        # Headings
        hm = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if hm:
            content.append(_heading(len(hm.group(1)), hm.group(2)))
            i += 1
            continue

        # Lists (bullet / ordered / checkbox)
        bm = bullet_re.match(line)
        if bm:
            ordered = bm.group(2)[-1] == "."
            items: list[tuple[str, str]] = []
            while i < len(lines):
                bm2 = bullet_re.match(lines[i])
                if not bm2:
                    break
                is_ord = bm2.group(2)[-1] == "."
                if is_ord != ordered:
                    break
                body = bm2.group(3)
                cm = check_re.match(body)
                if cm:
                    marker = "done" if cm.group(1).lower() == "x" else "todo"
                    items.append((marker, cm.group(2)))
                else:
                    items.append(("", body))
                i += 1
            content.append(_list(items, ordered=ordered))
            continue

        # Paragraph — gather consecutive non-empty, non-special lines
        buf = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            ns = nxt.strip()
            if not ns:
                break
            if (
                ns.startswith("#")
                or ns.startswith("```")
                or bullet_re.match(nxt)
                or re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", ns)
            ):
                break
            buf.append(ns)
            i += 1
        content.append(_paragraph(" ".join(buf)))

    if not content:
        content = [_paragraph(" ")]

    return {"type": "doc", "version": 1, "content": content}


# ---------------------------------------------------------------------------
# Markdown → Jira wiki markup (API v2)
# ---------------------------------------------------------------------------


def markdown_to_wiki(markdown: str) -> str:
    """Convert constrained markdown to Jira wiki markup for REST API v2."""
    lines = (markdown or "").replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    bullet_re = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
    in_code = False
    code_buf: list[str] = []

    def _inline_wiki(text: str) -> str:
        text = re.sub(r"`([^`]+)`", r"{{\1}}", text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"*\1*", text)
        text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"_\1_", text)
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"[\1|\2]", text)
        return text

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                lang = ""  # ignored for wiki
                out.append("{code" + (f":{lang}" if lang else "") + "}")
                out.extend(code_buf)
                out.append("{code}")
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        if not stripped:
            out.append("")
            i += 1
            continue
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            out.append("----")
            i += 1
            continue
        hm = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if hm:
            level = min(len(hm.group(1)), 6)
            out.append(f"h{level}. {_inline_wiki(hm.group(2))}")
            i += 1
            continue
        bm = bullet_re.match(line)
        if bm:
            ordered = bm.group(2)[-1] == "."
            while i < len(lines) and bullet_re.match(lines[i]):
                bm2 = bullet_re.match(lines[i])
                assert bm2
                body = bm2.group(3)
                prefix = "#" if ordered else "*"
                cm = re.match(r"^\[([ xX])\]\s+(.*)$", body)
                if cm:
                    mark = "(x)" if cm.group(1).lower() == "x" else "( )"
                    out.append(f"{prefix} {mark} {_inline_wiki(cm.group(2))}")
                else:
                    out.append(f"{prefix} {_inline_wiki(body)}")
                i += 1
            continue
        out.append(_inline_wiki(stripped))
        i += 1
    return "\n".join(out).strip() + "\n"


# ---------------------------------------------------------------------------
# ADF → markdown (for pull)
# ---------------------------------------------------------------------------


def adf_to_markdown(doc: Any) -> str:
    """Best-effort ADF → markdown for writing back into milestone requirements."""
    if doc is None:
        return ""
    if isinstance(doc, str):
        return doc
    if not isinstance(doc, dict):
        return str(doc)
    content = doc.get("content") or []
    parts: list[str] = []

    def inline(nodes: list[dict] | None) -> str:
        if not nodes:
            return ""
        chunks: list[str] = []
        for n in nodes:
            t = n.get("type")
            if t == "text":
                text = n.get("text", "")
                marks = {m.get("type") for m in (n.get("marks") or [])}
                href = None
                for m in n.get("marks") or []:
                    if m.get("type") == "link":
                        href = (m.get("attrs") or {}).get("href")
                if "code" in marks:
                    text = f"`{text}`"
                if "strong" in marks:
                    text = f"**{text}**"
                if "em" in marks:
                    text = f"*{text}*"
                if href:
                    text = f"[{text}]({href})"
                chunks.append(text)
            elif t == "hardBreak":
                chunks.append("\n")
            elif t == "emoji":
                chunks.append((n.get("attrs") or {}).get("shortName", ""))
            elif "content" in n:
                chunks.append(inline(n.get("content")))
        return "".join(chunks)

    def walk(nodes: list[dict]) -> None:
        for n in nodes:
            t = n.get("type")
            if t == "paragraph":
                parts.append(inline(n.get("content")))
                parts.append("")
            elif t == "heading":
                level = int((n.get("attrs") or {}).get("level") or 1)
                parts.append("#" * level + " " + inline(n.get("content")))
                parts.append("")
            elif t == "bulletList":
                for item in n.get("content") or []:
                    text = inline((item.get("content") or [{}])[0].get("content"))
                    # flatten nested paragraphs lightly
                    if not text and item.get("content"):
                        text = " ".join(
                            inline(p.get("content"))
                            for p in item["content"]
                            if p.get("type") == "paragraph"
                        )
                    parts.append(f"- {text}".rstrip())
                parts.append("")
            elif t == "orderedList":
                for idx, item in enumerate(n.get("content") or [], 1):
                    text = ""
                    if item.get("content"):
                        text = " ".join(
                            inline(p.get("content"))
                            for p in item["content"]
                            if p.get("type") == "paragraph"
                        )
                    parts.append(f"{idx}. {text}".rstrip())
                parts.append("")
            elif t == "codeBlock":
                lang = (n.get("attrs") or {}).get("language") or ""
                parts.append(f"```{lang}".rstrip())
                parts.append(inline(n.get("content")))
                parts.append("```")
                parts.append("")
            elif t == "rule":
                parts.append("---")
                parts.append("")
            elif t == "blockquote":
                walk(n.get("content") or [])
            elif "content" in n:
                walk(n["content"])

    walk(content)
    # collapse excess blanks
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(parts)).strip()
    return text + ("\n" if text else "")
