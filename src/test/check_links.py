# -*- coding: utf-8 -*-
"""静态检查全部 HTML / Markdown（*.md，跳过 src/ 和 dist/）中的内部链接与资源：文件是否存在、#锚点是否存在；并报告任何外部 http(s) 资源引用。
用法：python3 src/test/check_links.py"""
import os, re, sys, html, urllib.parse
from html.parser import HTMLParser
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs = []; s.ids = set()
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if tag == "a" and a.get("name"): s.ids.add(a["name"])
        for k in ("href", "src"):
            if k in a and a[k] is not None: s.refs.append((tag, k, a[k]))
SKIP = ("/src", "/.git", "/node_modules", "/.venv", "/.wrangler", "/dist")
pages, mds = {}, []
for dp, dn, fn in os.walk(ROOT):
    rel = dp.replace(ROOT, "")
    if any(rel == p or rel.startswith(p + "/") for p in SKIP): continue   # dist/ 是部署副本，不重复检查
    for f in fn:
        if f.endswith(".md"): mds.append(os.path.relpath(os.path.join(dp, f), ROOT))
        if f.endswith(".html"):
            path = os.path.join(dp, f); p = P(); p.feed(open(path, encoding="utf-8").read()); pages[path] = p
bad, ext, n = [], [], 0
for path, p in pages.items():
    for tag, k, ref in p.refs:
        n += 1
        if ref.startswith(("http://", "https://", "//")):
            if tag != "a": ext.append((path, ref))      # 外部资源（脚本 / 样式 / 图片）= 离线时会失效
            continue
        if ref.startswith(("mailto:", "javascript:", "data:")): continue
        u = urllib.parse.urlsplit(ref); target = urllib.parse.unquote(u.path); frag = urllib.parse.unquote(u.fragment)
        tp = os.path.normpath(os.path.join(os.path.dirname(path), target)) if target else path
        if not os.path.exists(tp): bad.append((path, ref, "missing file")); continue
        if frag and tp.endswith(".html"):
            if tp not in pages: q = P(); q.feed(open(tp, encoding="utf-8").read()); pages[tp] = q
            if frag not in pages[tp].ids: bad.append((path, ref, "missing anchor #" + frag))
# Markdown 文件中的相对链接
for md in ["START_HERE.md", "R/README.md", "materials/study_log.md", "data/data_dictionary.md"]:
    if md not in mds: bad.append((md, "", "missing md"))
for md in sorted(mds):
    mp = os.path.join(ROOT, md)
    text = re.sub(r"(?ms)^(`{3,}).*?^\1`*\s*$", "", open(mp, encoding="utf-8").read())   # 代码块里的 ](…) 不是链接
    text = re.sub(r"`[^`\n]*`", "", text)
    for ref in re.findall(r"\]\(([^)\s]+)\)", text):
        if ref.startswith(("http", "#", "<")): continue
        n += 1
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(mp), urllib.parse.unquote(ref.split("#")[0])))): bad.append((md, ref, "missing file"))
rel = lambda x: os.path.relpath(x, ROOT) if x.startswith("/") else x
print(f"HTML pages: {len([p for p in pages])}, Markdown files: {len(mds)}, references checked: {n}")
for x in bad: print("BROKEN", rel(x[0]), x[1], x[2])
for x in ext: print("EXTERNAL RESOURCE", rel(x[0]), x[1])
print("broken:", len(bad), " external resources:", len(ext))
sys.exit(1 if bad or ext else 0)
