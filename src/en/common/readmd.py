# -*- coding: utf-8 -*-
"""Convert lesson HTML <main> into plain reading Markdown for agents/LLMs."""
import re
from html.parser import HTMLParser

_SKIP_TAGS = {"script", "style", "svg", "noscript"}
_SKIP_CLASS = {"pager", "foot", "structnote", "progressline"}
_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def _clean(s):
    s = s.replace("\xa0", " ")
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


class _ToMd(HTMLParser):
    def __init__(self, keep_links=False):
        super().__init__(convert_charrefs=True)
        self.keep_links = keep_links
        self.links = []
        self.parts = []
        self.buf = []
        self.skip = 0
        self.skip_tree = 0
        self.in_main = False
        self.in_pre = False
        self.pre = []
        self.pre_lang = ""
        self.lists = []
        self.table = None
        self.row = None
        self.cell = None
        self.mark_ok = False
        self.quiz_ans = None
        self.quiz_tol = None
        self.quiz_depth = 0
        self.scripts = []

    def _add(self, s):
        if self.in_pre:
            self.pre.append(s)
        elif self.cell is not None:
            self.cell.append(s)
        else:
            self.buf.append(s)

    def _emit(self, block):
        block = block.strip("\n")
        if block:
            self.parts.append(block)

    def _flush(self):
        s = _clean("".join(self.buf))
        self.buf = []
        return s

    def _para(self):
        s = self._flush()
        if not s:
            return
        if self.lists:
            kind, n = self.lists[-1]
            indent = "  " * (len(self.lists) - 1)
            if kind == "ol":
                self.lists[-1][1] = n + 1
                self._emit(f"{indent}{n}. {s}")
            else:
                self._emit(f"{indent}- {s}")
            return
        self._emit(s)

    def _div_break(self):
        if self.lists and self.cell is None:
            if self.buf and "".join(self.buf).strip():
                self._add("\n")
        else:
            self._para()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        if tag == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        if self.skip_tree:
            if tag not in _VOID:
                self.skip_tree += 1
            return
        if self.skip:
            if tag in _SKIP_TAGS:
                self.skip += 1
            return
        if tag in _SKIP_TAGS:
            self.skip += 1
            return
        if cls & _SKIP_CLASS:
            self.skip_tree = 1
            return
        if tag == "div" and "widget" in cls:
            name = a.get("data-title") or a.get("data-widget") or "Interactive widget"
            self._para()
            self._emit(f"(Interactive widget: {name})")
            self.skip_tree = 1
            return
        if tag == "div" and "quiz" in cls and a.get("data-ans") and not self.quiz_depth:
            self.quiz_ans = a.get("data-ans")
            self.quiz_tol = a.get("data-tol")
            self.quiz_depth = 1
        elif self.quiz_depth and tag not in _VOID:
            self.quiz_depth += 1
        if tag == "div" and not self.in_pre:
            self._div_break()
        if tag in ("h1", "h2", "h3", "h4", "p", "li"):
            self._para()
        elif tag == "br":
            self._add("\n")
        elif tag == "pre":
            self._para()
            self.in_pre = True
            self.pre = []
            self.pre_lang = "text" if "out" in cls else ""
        elif tag == "code" and not self.in_pre:
            self._add("`")
        elif tag == "code" and self.in_pre and not self.pre_lang and "language-r" in (a.get("class") or ""):
            self.pre_lang = "r"
        elif tag in ("strong", "b"):
            self._add("**")
        elif tag in ("em", "i"):
            self._add("*")
        elif tag in ("sup", "sub") and not self.in_pre:
            target = self.cell if self.cell is not None else self.buf
            self.scripts.append((target, len(target)))
        elif tag == "img":
            src = a.get("src") or ""
            alt = a.get("alt") or "Figure"
            self._para()
            if src:
                self._emit(f"![{alt}]({src})")
        elif tag in ("ul", "ol"):
            self._para()
            self.lists.append(["ol" if tag == "ol" else "ul", 1])
        elif tag == "table":
            self._para()
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag == "a" and self.keep_links and not self.in_pre and a.get("href"):
            target = self.cell if self.cell is not None else self.buf
            self.links.append((target, len(target), a["href"]))
        elif tag == "button" and a.get("data-ok") == "1":
            self.mark_ok = True
        elif tag == "div" and "facts" in cls:
            self._facts = True
        elif tag == "span" and "en" in cls:
            self._add(" ")
        elif tag == "span" and "stag" in cls:
            self._stag = True
        elif tag == "span":
            self._stag = False

    def handle_endtag(self, tag):
        if tag == "main":
            self._para()
            self.in_main = False
            return
        if not self.in_main:
            return
        if self.skip_tree:
            if tag not in _VOID:
                self.skip_tree -= 1
            return
        if self.skip:
            if tag in _SKIP_TAGS:
                self.skip -= 1
            return
        if tag in ("h1", "h2", "h3", "h4"):
            s = self._flush()
            if s:
                self._emit("#" * int(tag[1]) + " " + re.sub(r"\s+", " ", s))
        elif tag == "p":
            self._para()
        elif tag == "li":
            self._para()
        elif tag == "span" and getattr(self, "_stag", False):
            self._add(" ")
            self._stag = False
        elif tag == "span" and getattr(self, "_facts", False):
            self._add("\n")
        elif tag == "div" and getattr(self, "_facts", False):
            self._facts = False
            self._para()
        elif tag == "a" and self.keep_links and self.links:
            target, start, href = self.links.pop()
            current = self.cell if self.cell is not None else self.buf
            text = "".join(target[start:]).strip()
            if target is current and text:
                target[start:] = [f"[{text}]({href})"]
        elif tag == "button":
            s = self._flush()
            if s:
                if self.mark_ok:
                    s += " (Correct)"
                self.buf.append(s)
                self._para()
            self.mark_ok = False
        elif tag == "pre":
            code = "".join(self.pre).replace("\r\n", "\n").strip("\n")
            lang = self.pre_lang
            self.in_pre = False
            self.pre = []
            runs = [len(r) for r in re.findall(r"`{3,}", code)]
            fence = "`" * max(3, max(runs, default=0) + 1)
            self._emit(f"{fence}{lang}\n{code}\n{fence}")
        elif tag == "code" and not self.in_pre:
            self._add("`")
        elif tag in ("strong", "b"):
            self._add("**")
        elif tag in ("em", "i"):
            self._add("*")
        elif tag in ("sup", "sub") and not self.in_pre and self.scripts:
            target, start = self.scripts.pop()
            text = "".join(target[start:]).strip()
            if text:
                mark = "^" if tag == "sup" else "_"
                simple = re.fullmatch(r"[^\W_]|[+\-−]?\d+(?:\.\d+)?", text)
                target[start:] = [mark + (text if simple else f"({text})")]
        elif tag == "div" and not self.in_pre:
            self._div_break()
        elif tag in ("ul", "ol"):
            self._para()
            if self.lists:
                self.lists.pop()
        elif tag in ("td", "th") and self.cell is not None:
            text = _clean("".join(self.cell))
            self.row.append(text.replace("|", "\\|").replace("\n", " "))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            rows = [r for r in self.table if any(c.strip() for c in r)]
            self.table = None
            if rows:
                width = max(len(r) for r in rows)
                rows = [r + [""] * (width - len(r)) for r in rows]
                lines = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join("---" for _ in rows[0]) + " |"]
                lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
                self._emit("\n".join(lines))
        elif tag == "figcaption":
            self._para()
        if self.quiz_depth and tag not in _VOID:
            self.quiz_depth -= 1
            if self.quiz_depth == 0 and self.quiz_ans:
                tol = self.quiz_tol
                self._emit("Reference answer: " + self.quiz_ans + (f" (tolerance ±{tol})" if tol and tol not in ("0", "0.0") else ""))
                self.quiz_ans = None
                self.quiz_tol = None

    def handle_data(self, data):
        if not self.in_main or self.skip or self.skip_tree:
            return
        self._add(data)


def reading_md(html, keep_links=False):
    """Extract <main> from a full lesson/guide HTML page and convert to Markdown."""
    parser = _ToMd(keep_links=keep_links)
    parser.feed(html)
    parser.close()
    parser._para()
    body = "\n\n".join(parser.parts)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return body
