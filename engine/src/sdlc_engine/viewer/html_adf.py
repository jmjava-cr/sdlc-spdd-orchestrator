"""HTML fragment → ADF document (round-trip for save path)."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import unquote

_GWT = re.compile(r"^\s*(Given|When|Then|And|But)\b", re.I)


def _text_node(text: str, marks: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    if text == "":
        return None
    node: dict[str, Any] = {"type": "text", "text": text}
    if marks:
        node["marks"] = list(marks)
    return node


def _push_text(out: list[dict[str, Any]], text: str, marks: list[dict[str, Any]]) -> None:
    node = _text_node(text, marks or None)
    if node:
        out.append(node)


class _HtmlToAdf(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doc_content: list[dict[str, Any]] = []
        self._stack: list[dict[str, Any]] = []
        self._marks: list[dict[str, Any]] = []
        self._div_kinds: list[str] = []
        self._in_pre = False
        self._pre_lang = ""
        self._pre_text: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._skip_depth:
            self._skip_depth += 1
            return
        ad = {k: (v or "") for k, v in attrs}
        cls = ad.get("class", "")
        classes = set(cls.split())
        # Editor chrome (drag handle / delete) must not enter ADF
        if "gwt-chrome" in classes or "gwt-handle" in classes or "gwt-delete" in classes:
            self._skip_depth = 1
            return

        if tag in {"strong", "b"}:
            self._marks.append({"type": "strong"})
            return
        if tag in {"em", "i"}:
            self._marks.append({"type": "em"})
            return
        if tag == "code" and not self._in_pre:
            self._marks.append({"type": "code"})
            return
        if tag in {"s", "strike", "del"}:
            self._marks.append({"type": "strike"})
            return
        if tag == "u":
            self._marks.append({"type": "underline"})
            return
        if tag == "a":
            href = ad.get("href") or "#"
            self._marks.append({"type": "link", "attrs": {"href": href}})
            return
        if tag == "br":
            self._append_inline({"type": "hardBreak"})
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            node = {"type": "heading", "attrs": {"level": int(tag[1])}, "content": []}
            self._push_block(node)
            return
        if tag == "p":
            self._push_block({"type": "paragraph", "content": []})
            return
        if tag == "ul":
            self._push_block({"type": "bulletList", "content": []})
            return
        if tag == "ol":
            self._push_block({"type": "orderedList", "content": []})
            return
        if tag == "li":
            self._push_block({"type": "listItem", "content": [{"type": "paragraph", "content": []}]})
            # Point stack at the paragraph inside listItem for inline text
            li = self._stack[-1]
            self._stack.append(li["content"][0])
            return
        if tag == "blockquote":
            self._push_block({"type": "blockquote", "content": []})
            return
        if tag == "hr":
            self.doc_content.append({"type": "rule"})
            return
        if tag == "pre":
            self._in_pre = True
            self._pre_lang = ad.get("data-language") or ""
            self._pre_text = []
            return
        if tag == "code" and self._in_pre:
            return
        if tag == "div" and "panel" in classes:
            ptype = ad.get("data-panel-type") or "info"
            for part in classes:
                if part.startswith("panel-") and part != "panel":
                    ptype = part[len("panel-") :]
            self._div_kinds.append("panel")
            self._push_block({"type": "panel", "attrs": {"panelType": ptype}, "content": []})
            return
        if tag == "div" and "gwt-block" in classes:
            self._div_kinds.append("gwt-block")
            self._push_block({"type": "bulletList", "content": [], "_gwt": True})
            return
        if tag == "div" and "gwt-scenario" in classes:
            owned = False
            if not self._stack or not self._stack[-1].get("_gwt"):
                self._push_block({"type": "bulletList", "content": [], "_gwt": True})
                owned = True
            self._div_kinds.append("gwt-scenario-owned" if owned else "gwt-scenario")
            item = {"type": "listItem", "content": [{"type": "paragraph", "content": []}]}
            self._stack[-1]["content"].append(item)
            self._stack.append(item["content"][0])
            return
        if tag == "div" and "gwt-line" in classes:
            self._div_kinds.append("gwt-line")
            para = self._current_inline_parent()
            if para is not None:
                content = para.setdefault("content", [])
                while (
                    content
                    and content[-1].get("type") == "text"
                    and not (content[-1].get("text") or "").strip()
                ):
                    content.pop()
                if content:
                    content.append({"type": "hardBreak"})
            return
        if tag == "div":
            self._div_kinds.append("other")
            return
        if tag == "table":
            self._push_block({"type": "table", "attrs": {}, "content": []})
            return
        if tag == "tbody":
            return
        if tag == "tr":
            self._push_block({"type": "tableRow", "content": []})
            return
        if tag == "th":
            self._push_block({"type": "tableHeader", "content": [{"type": "paragraph", "content": []}]})
            self._stack.append(self._stack[-1]["content"][0])
            return
        if tag == "td":
            self._push_block({"type": "tableCell", "content": [{"type": "paragraph", "content": []}]})
            self._stack.append(self._stack[-1]["content"][0])
            return
        if tag == "figure" and "media-single" in cls.split():
            self._push_block(
                {
                    "type": "mediaSingle",
                    "attrs": {"layout": ad.get("data-layout") or "center"},
                    "content": [],
                }
            )
            return
        if tag == "img":
            url = ad.get("src") or ""
            alt = ad.get("alt") or ""
            media = {
                "type": "media",
                "attrs": {"type": "external", "url": unquote(url), "alt": alt},
            }
            if self._stack and self._stack[-1].get("type") == "mediaSingle":
                self._stack[-1]["content"].append(media)
            else:
                self.doc_content.append(
                    {
                        "type": "mediaSingle",
                        "attrs": {"layout": "center"},
                        "content": [media],
                    }
                )
            return
        if tag == "details":
            self._push_block({"type": "expand", "attrs": {"title": "Details"}, "content": []})
            return
        if tag == "summary":
            # Collect summary text into expand title via marks stack trick
            self._push_block({"type": "paragraph", "content": [], "_summary": True})
            return

    def handle_endtag(self, tag: str) -> None:
        if self._skip_depth:
            self._skip_depth -= 1
            return

        if tag in {"strong", "b", "em", "i", "code", "s", "strike", "del", "u", "a"}:
            if tag == "code" and self._in_pre:
                return
            if self._marks:
                # pop matching mark type
                want = {
                    "strong": "strong",
                    "b": "strong",
                    "em": "em",
                    "i": "em",
                    "code": "code",
                    "s": "strike",
                    "strike": "strike",
                    "del": "strike",
                    "u": "underline",
                    "a": "link",
                }[tag]
                for i in range(len(self._marks) - 1, -1, -1):
                    if self._marks[i]["type"] == want:
                        self._marks.pop(i)
                        break
            return

        if tag == "pre":
            code = "".join(self._pre_text)
            node: dict[str, Any] = {
                "type": "codeBlock",
                "attrs": {"language": self._pre_lang or None},
                "content": [],
            }
            if node["attrs"]["language"] is None:
                node["attrs"] = {}
            if code:
                node["content"] = [{"type": "text", "text": code}]
            if self._stack:
                self._stack[-1].setdefault("content", []).append(node)
            else:
                self.doc_content.append(node)
            self._in_pre = False
            self._pre_text = []
            self._pre_lang = ""
            return

        if tag == "div":
            kind = self._div_kinds.pop() if self._div_kinds else "other"
            if kind == "gwt-line":
                return
            if kind in {"gwt-scenario", "gwt-scenario-owned"}:
                if self._stack and self._stack[-1].get("type") == "paragraph":
                    self._stack.pop()
                if kind == "gwt-scenario-owned" and self._stack and self._stack[-1].get("type") == "bulletList":
                    node = self._stack.pop()
                    if "_gwt" in node:
                        del node["_gwt"]
                return
            if kind in {"gwt-block", "panel"}:
                if self._stack and self._stack[-1].get("type") in {"panel", "bulletList"}:
                    node = self._stack.pop()
                    if "_gwt" in node:
                        del node["_gwt"]
            return

        if tag in {
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "ul",
            "ol",
            "blockquote",
            "table",
            "tr",
            "figure",
            "details",
        }:
            self._pop_until(
                {
                    "h1": "heading",
                    "h2": "heading",
                    "h3": "heading",
                    "h4": "heading",
                    "h5": "heading",
                    "h6": "heading",
                    "p": "paragraph",
                    "ul": "bulletList",
                    "ol": "orderedList",
                    "blockquote": "blockquote",
                    "table": "table",
                    "tr": "tableRow",
                    "figure": "mediaSingle",
                    "details": "expand",
                }[tag]
            )
            return

        if tag == "li":
            # pop paragraph then listItem
            if self._stack and self._stack[-1].get("type") == "paragraph":
                self._stack.pop()
            if self._stack and self._stack[-1].get("type") == "listItem":
                self._stack.pop()
            return

        if tag in {"th", "td"}:
            if self._stack and self._stack[-1].get("type") == "paragraph":
                self._stack.pop()
            if self._stack and self._stack[-1].get("type") in {"tableHeader", "tableCell"}:
                self._stack.pop()
            return

        if tag == "summary":
            if self._stack and self._stack[-1].get("_summary"):
                para = self._stack.pop()
                title = "".join(
                    n.get("text", "") for n in para.get("content") or [] if n.get("type") == "text"
                )
                for frame in reversed(self._stack):
                    if frame.get("type") == "expand":
                        frame["attrs"]["title"] = title or "Details"
                        break
            return

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_pre:
            self._pre_text.append(data)
            return
        if not data:
            return
        # Collapse pure whitespace between blocks but keep spaces in paragraphs
        parent = self._current_inline_parent()
        if parent is None:
            # Top-level text → wrap in paragraph
            if data.strip():
                para: dict[str, Any] = {"type": "paragraph", "content": []}
                _push_text(para["content"], data, self._marks)
                self.doc_content.append(para)
            return
        _push_text(parent.setdefault("content", []), data, self._marks)

    def _push_block(self, node: dict[str, Any]) -> None:
        if self._stack:
            self._stack[-1].setdefault("content", []).append(node)
        else:
            self.doc_content.append(node)
        # Nodes that accept nested blocks stay on stack
        if node.get("type") in {
            "heading",
            "paragraph",
            "bulletList",
            "orderedList",
            "listItem",
            "blockquote",
            "panel",
            "table",
            "tableRow",
            "tableCell",
            "tableHeader",
            "mediaSingle",
            "expand",
        }:
            self._stack.append(node)

    def _pop_until(self, ntype: str) -> None:
        while self._stack:
            node = self._stack.pop()
            if "_gwt" in node:
                del node["_gwt"]
            if node.get("type") == ntype:
                break

    def _current_inline_parent(self) -> dict[str, Any] | None:
        for frame in reversed(self._stack):
            if frame.get("type") in {"paragraph", "heading"}:
                return frame
        return None

    def _append_inline(self, node: dict[str, Any]) -> None:
        parent = self._current_inline_parent()
        if parent is None:
            para: dict[str, Any] = {"type": "paragraph", "content": [node]}
            self.doc_content.append(para)
            return
        parent.setdefault("content", []).append(node)


def _strip_empty_text(nodes: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    if not nodes:
        return []
    out: list[dict[str, Any]] = []
    for n in nodes:
        if n.get("type") == "text" and n.get("text") == "":
            continue
        if "content" in n and isinstance(n["content"], list):
            n = {**n, "content": _strip_empty_text(n["content"])}
        # Drop private keys
        n = {k: v for k, v in n.items() if not str(k).startswith("_")}
        out.append(n)
    return out


def _normalize_gwt_lists(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ensure GWT-looking list items keep hardBreak structure."""
    out = []
    for n in nodes:
        if n.get("type") == "bulletList":
            items = []
            for it in n.get("content") or []:
                if it.get("type") != "listItem":
                    items.append(it)
                    continue
                # Flatten multiple paragraphs into one with hardBreaks when GWT-like
                paras = [c for c in (it.get("content") or []) if c.get("type") == "paragraph"]
                if len(paras) > 1:
                    merged: list[dict[str, Any]] = []
                    for i, p in enumerate(paras):
                        if i and merged:
                            merged.append({"type": "hardBreak"})
                        merged.extend(p.get("content") or [])
                    text = "".join(
                        x.get("text", "") if x.get("type") == "text" else "\n"
                        for x in merged
                    )
                    if any(_GWT.match(line) for line in text.split("\n") if line.strip()):
                        it = {"type": "listItem", "content": [{"type": "paragraph", "content": merged}]}
                items.append(it)
            out.append({"type": "bulletList", "content": items})
        elif "content" in n:
            out.append({**n, "content": _normalize_gwt_lists(n["content"])})
        else:
            out.append(n)
    return out


def html_to_adf(html_fragment: str) -> dict[str, Any]:
    """Parse an HTML fragment into an ADF ``doc``."""
    parser = _HtmlToAdf()
    parser.feed(html_fragment or "")
    parser.close()
    content = _strip_empty_text(parser.doc_content)
    content = _normalize_gwt_lists(content)
    if not content:
        content = [{"type": "paragraph", "content": []}]
    return {"type": "doc", "version": 1, "content": content}
