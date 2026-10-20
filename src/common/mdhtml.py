# -*- coding: utf-8 -*-
"""把课程里的 Markdown 渲染成 HTML。只覆盖这些文件实际用到的写法：
标题、段落、粗体、行内代码、链接、自动链接、围栏代码、引用、有序/无序列表、表格。
相对链接若指向同名 .md，改到渲染后的 .html。"""
import html, re

_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_AUTO = re.compile(r"<(https?://[^>\s]+)>")
_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITAL = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_HEAD = re.compile(r"^(#{1,4}) +(.+)$")
_LIST = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
_FENCE = re.compile(r"^```")
_TABLE_RULE = re.compile(r"^\|?\s*:?-{3,}")

def _slot(slots, snippet):
    slots.append(snippet)
    return f"{len(slots) - 1}"

def inline(s):
    slots = []
    def code(m):
        return _slot(slots, "<code>" + html.escape(m.group(1)) + "</code>")
    s = _CODE.sub(code, s)
    def link(m):
        text, url = m.group(1), m.group(2)
        if not url.startswith(("http://", "https://", "mailto:")):
            url = re.sub(r"\.md(?=(?:#|$))", ".html", url)
        return _slot(slots, f'<a href="{html.escape(url, quote=True)}">{inline(text)}</a>')
    s = _LINK.sub(link, s)
    def auto(m):
        url = m.group(1)
        return _slot(slots, f'<a href="{html.escape(url, quote=True)}">{html.escape(url)}</a>')
    s = _AUTO.sub(auto, s)
    s = html.escape(s)
    s = _BOLD.sub(r"<strong>\1</strong>", s)
    s = _ITAL.sub(r"<em>\1</em>", s)
    return re.sub(r"(\d+)", lambda m: slots[int(m.group(1))], s)

def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def _table(rows):
    head = _cells(rows[0])
    body = [_cells(r) for r in rows[2:]]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'

def _list(lines):
    items = []
    for ln in lines:
        m = _LIST.match(ln)
        if m:
            kind = "ol" if m.group(2)[:1].isdigit() else "ul"
            items.append([len(m.group(1)), kind, m.group(3)])
        elif items:
            items[-1][2] += " " + ln.strip()
    def build(idx, level):
        parts = []
        while idx < len(items) and items[idx][0] >= level:
            if items[idx][0] > level:
                child, idx = build(idx, items[idx][0])
                if parts:
                    parts[-1] = parts[-1][:-5] + child + "</li>"
                continue
            tag = items[idx][1]
            chunks = []
            while idx < len(items) and items[idx][0] == level and items[idx][1] == tag:
                text = items[idx][2]
                idx += 1
                child = ""
                if idx < len(items) and items[idx][0] > level:
                    child, idx = build(idx, items[idx][0])
                chunks.append("<li>" + inline(text) + child + "</li>")
            parts.append(f"<{tag}>{''.join(chunks)}</{tag}>")
        return "".join(parts), idx
    html_out, _ = build(0, items[0][0] if items else 0)
    return html_out

def _block_start(line):
    return (not line.strip() or _FENCE.match(line) or line.startswith("|") or line.startswith(">")
            or _HEAD.match(line) or _LIST.match(line))

def render_md(text):
    """返回 (title, html)。title 取第一个一级标题，没有则为空。"""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    i, n = 0, len(lines)
    blocks, title = [], ""
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if _FENCE.match(line):
            lang = line[3:].strip().lower()
            i += 1
            buf = []
            while i < n and not _FENCE.match(lines[i]):
                buf.append(lines[i]); i += 1
            if i < n: i += 1
            cls = ' class="language-r"' if lang == "r" else ""
            blocks.append(f'<div class="codeblk"><pre><code{cls}>{html.escape(chr(10).join(buf))}</code></pre></div>')
            continue
        sline = line.lstrip()
        if sline.startswith("|") and i + 1 < n and _TABLE_RULE.match(lines[i + 1].lstrip().strip().strip("|")):
            rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            blocks.append(_table(rows))
            continue
        m = _HEAD.match(line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1 and not title:
                title = text
            else:
                blocks.append(f"<h{min(level, 4)}>{inline(text)}</h{min(level, 4)}>")
            i += 1
            continue
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            blocks.append("<blockquote><p>" + inline(" ".join(buf)) + "</p></blockquote>")
            continue
        if _LIST.match(line):
            buf = []
            while i < n and (_LIST.match(lines[i]) or (lines[i].startswith(" ") and lines[i].strip() and not _block_start(lines[i].lstrip()))):
                buf.append(lines[i]); i += 1
            blocks.append(_list(buf))
            continue
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not _block_start(lines[i]):
            buf.append(lines[i]); i += 1
        blocks.append("<p>" + "<br>\n".join(inline(x) for x in buf) + "</p>")
    return title, "\n".join(blocks)
