"""ADF document → HTML for the WYSIWYG viewer."""

from __future__ import annotations

import html
import re
from typing import Any

_GWT = re.compile(r"^\s*(Given|When|Then|And|But)\b", re.I)


def _esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def _apply_marks(text: str, marks: list[dict[str, Any]] | None) -> str:
    out = _esc(text)
    for mark in marks or []:
        mtype = mark.get("type")
        if mtype == "strong":
            out = f"<strong>{out}</strong>"
        elif mtype == "em":
            out = f"<em>{out}</em>"
        elif mtype == "code":
            out = f"<code>{out}</code>"
        elif mtype == "strike":
            out = f"<s>{out}</s>"
        elif mtype == "underline":
            out = f"<u>{out}</u>"
        elif mtype == "link":
            href = (mark.get("attrs") or {}).get("href") or "#"
            out = f'<a href="{_esc(str(href))}" target="_blank" rel="noopener">{out}</a>'
    return out


def _inline(nodes: list[dict[str, Any]] | None) -> str:
    if not nodes:
        return ""
    parts: list[str] = []
    for node in nodes:
        ntype = node.get("type")
        if ntype == "text":
            parts.append(_apply_marks(node.get("text") or "", node.get("marks")))
        elif ntype == "hardBreak":
            parts.append("<br>")
        elif ntype == "mention":
            attrs = node.get("attrs") or {}
            parts.append(
                f'<span class="mention" data-id="{_esc(str(attrs.get("id", "")))}">'
                f"@{_esc(str(attrs.get('text') or attrs.get('id') or 'user'))}</span>"
            )
        elif ntype == "emoji":
            attrs = node.get("attrs") or {}
            parts.append(_esc(str(attrs.get("shortName") or attrs.get("text") or "")))
        elif ntype == "inlineCard":
            url = (node.get("attrs") or {}).get("url") or ""
            parts.append(f'<a class="inline-card" href="{_esc(str(url))}">{_esc(str(url))}</a>')
        else:
            # Unknown inline: try children or skip
            if node.get("content"):
                parts.append(_inline(node["content"]))
    return "".join(parts)


def _is_gwt_list_item(item: dict[str, Any]) -> bool:
    for child in item.get("content") or []:
        if child.get("type") != "paragraph":
            continue
        text = "".join(
            (n.get("text") or "") if n.get("type") == "text" else ("\n" if n.get("type") == "hardBreak" else "")
            for n in (child.get("content") or [])
        )
        if any(_GWT.match(line) for line in text.split("\n") if line.strip()):
            return True
    return False


def _gwt_item_html(item: dict[str, Any]) -> str:
    segments: list[str] = []
    for child in item.get("content") or []:
        if child.get("type") != "paragraph":
            continue
        buf: list[str] = []
        for n in child.get("content") or []:
            if n.get("type") == "hardBreak":
                if buf:
                    segments.append("".join(buf))
                    buf = []
            elif n.get("type") == "text":
                buf.append(_apply_marks(n.get("text") or "", n.get("marks")))
            else:
                buf.append(_inline([n]))
        if buf:
            segments.append("".join(buf))
    body = "".join(f'<div class="gwt-line">{seg}</div>' for seg in segments if seg)
    return f'<div class="gwt-scenario" contenteditable="true">{body}</div>'


def _block(node: dict[str, Any], warnings: list[str]) -> str:
    ntype = node.get("type")
    attrs = node.get("attrs") or {}
    content = node.get("content") or []

    if ntype == "paragraph":
        inner = _inline(content)
        return f"<p>{inner}</p>" if inner else "<p><br></p>"

    if ntype == "heading":
        level = int(attrs.get("level") or 2)
        level = min(max(level, 1), 6)
        return f"<h{level}>{_inline(content)}</h{level}>"

    if ntype == "bulletList":
        if content and all(_is_gwt_list_item(it) for it in content):
            return '<div class="gwt-block">' + "".join(_gwt_item_html(it) for it in content) + "</div>"
        items = []
        for it in content:
            if it.get("type") != "listItem":
                continue
            items.append(f"<li>{_blocks(it.get('content') or [], warnings)}</li>")
        return f"<ul>{''.join(items)}</ul>"

    if ntype == "orderedList":
        items = []
        for it in content:
            if it.get("type") != "listItem":
                continue
            items.append(f"<li>{_blocks(it.get('content') or [], warnings)}</li>")
        return f"<ol>{''.join(items)}</ol>"

    if ntype == "listItem":
        return _blocks(content, warnings)

    if ntype == "codeBlock":
        lang = attrs.get("language") or ""
        code = "".join(
            (n.get("text") or "") if n.get("type") == "text" else ""
            for n in content
        )
        return (
            f'<pre class="code-block" data-language="{_esc(str(lang))}">'
            f"<code>{_esc(code)}</code></pre>"
        )

    if ntype == "blockquote":
        return f"<blockquote>{_blocks(content, warnings)}</blockquote>"

    if ntype == "rule":
        return "<hr>"

    if ntype == "panel":
        ptype = attrs.get("panelType") or "info"
        return (
            f'<div class="panel panel-{_esc(str(ptype))}" data-panel-type="{_esc(str(ptype))}">'
            f"{_blocks(content, warnings)}</div>"
        )

    if ntype == "table":
        rows = []
        for row in content:
            if row.get("type") != "tableRow":
                continue
            cells = []
            for cell in row.get("content") or []:
                tag = "th" if cell.get("type") == "tableHeader" else "td"
                cells.append(f"<{tag}>{_blocks(cell.get('content') or [], warnings)}</{tag}>")
            rows.append(f"<tr>{''.join(cells)}</tr>")
        return f'<table class="adf-table"><tbody>{"".join(rows)}</tbody></table>'

    if ntype in {"tableRow", "tableCell", "tableHeader"}:
        return _blocks(content, warnings)

    if ntype == "mediaSingle":
        for child in content:
            if child.get("type") == "media":
                mattrs = child.get("attrs") or {}
                url = mattrs.get("url") or mattrs.get("src") or ""
                alt = mattrs.get("alt") or ""
                if url:
                    return (
                        f'<figure class="media-single" data-layout="{_esc(str(attrs.get("layout") or "center"))}">'
                        f'<img src="{_esc(str(url))}" alt="{_esc(str(alt))}" />'
                        f"</figure>"
                    )
        warnings.append("mediaSingle without external url skipped")
        return ""

    if ntype == "mediaGroup":
        return "".join(_block(c, warnings) for c in content)

    if ntype == "expand":
        title = attrs.get("title") or "Details"
        return (
            f"<details class='expand'><summary>{_esc(str(title))}</summary>"
            f"{_blocks(content, warnings)}</details>"
        )

    warnings.append(f"unknown ADF node type skipped: {ntype}")
    if content:
        return _blocks(content, warnings)
    return ""


def _blocks(nodes: list[dict[str, Any]], warnings: list[str]) -> str:
    return "".join(_block(n, warnings) for n in nodes)


def _inject_attr(html: str, attr: str) -> str:
    """Inject an attribute into the first opening tag of an HTML fragment."""
    if not html.startswith("<"):
        return html
    # <tag ...> or <tag>
    gt = html.find(">")
    if gt <= 0:
        return html
    open_tag = html[:gt]
    if " " in open_tag or open_tag.endswith("/"):
        return f"{open_tag} {attr}{html[gt:]}"
    return f"{open_tag} {attr}{html[gt:]}"


def adf_to_html(doc: dict[str, Any], *, collect_warnings: list[str] | None = None) -> str:
    """Convert an ADF ``doc`` node to HTML fragment.

    Top-level blocks receive ``data-block-index`` for split-pane click sync.
    """
    warnings = collect_warnings if collect_warnings is not None else []
    if not isinstance(doc, dict) or doc.get("type") != "doc":
        raise ValueError("ADF root must be type=doc")
    parts: list[str] = []
    for i, node in enumerate(doc.get("content") or []):
        frag = _block(node, warnings)
        if frag:
            parts.append(_inject_attr(frag, f'data-block-index="{i}"'))
    return "".join(parts) or "<p data-block-index=\"0\"><br></p>"
