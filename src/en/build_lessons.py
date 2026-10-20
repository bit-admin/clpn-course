# -*- coding: utf-8 -*-
"""Build en/lessons/L0-1.html … L4-3.html (English M0–M4 interactive lessons)."""
import html, importlib.util, json, os, re, sys
SRC = os.path.dirname(os.path.abspath(__file__))
LANG = "en" if os.path.basename(SRC) == "en" else "zh"
REPO = os.path.dirname(os.path.dirname(SRC)) if LANG == "en" else os.path.dirname(SRC)
ROOT = REPO + "/en" if LANG == "en" else REPO
D = ROOT + "/"
g = {"ROOT": REPO}
for f in ["data1", "data2", "data3", "data4"]:
    exec(open(SRC + "/" + f + ".py", encoding="utf-8").read(), g)
MODULES = g["MODULES"]
E = html.escape
anchor = lambda i: "L" + i.replace(".", "-")
ALL = [(m, l) for m in MODULES for l in m["lessons"]]
IDX = {l["id"]: (m, l) for m, l in ALL}
TARGET = sys.argv[1:] or [l["id"] for m, l in ALL if m["id"] in ("M0", "M1", "M2", "M3", "M4")]
GIVES = {
    "M0": "Motivation and big-picture roadmap: know where you are going and why it matters.",
    "M1": "Statistical language: mean, variance, correlation, standard error, p-value—the prerequisites for reading every number in CLPN output.",
    "M2": "R skills: from zero to writing CLPN estimation code independently.",
    "M3": "Regression & LASSO: the engine of CLPN—each T2 node is a regularized regression.",
    "M4": "Longitudinal data: how T1/T2 panel data are collected, reshaped, and checked for missingness.",
    "M5": "CLPM & RI-CLPM: what cross-lagged paths mean and the between-person vs. within-person pitfall.",
    "M6": "Network psychometrics: nodes, edges, partial correlations, regularization, centrality.",
    "M7": "CLPN itself: estimation, visualization, out- and in-expected influence.",
    "M8": "Stability checks: bootstrap intervals and CS-coefficients to judge whether results are trustworthy.",
    "M9": "Reading papers, methodological critique, and reporting standards.",
    "M10": "Capstone project: execute and write up a complete CLPN analysis end to end.",
}
def exists(i): return os.path.exists(D + "lessons/" + anchor(i) + ".html") or i in TARGET
def lesson_link(i, text=None):
    m, l = IDX[i]; t = text or f"{i} {l['title']}"
    if exists(i): return f'<a href="{anchor(i)}.html">{E(t)}</a>'
    return f'<a href="../index.html#{anchor(i)}">{E(t)}</a>'

def code_block(lang, title, body):
    t = f'<div class="ctitle">{E(title)}</div>' if title else ""
    cls = ' class="out"' if lang == "out" else ""
    c = ' class="language-r"' if lang == "r" else ""
    return f'<div class="codeblk">{t}<pre{cls}><code{c}>{E(body)}</code></pre></div>'

_qspec = importlib.util.spec_from_file_location("quiz", SRC + "/common/quiz.py")
_quiz = importlib.util.module_from_spec(_qspec); _qspec.loader.exec_module(_quiz)
quiz = _quiz.quiz

FENCE = re.compile(r"^```(\w+)[ \t]*(.*?)\n(.*?)^```[ \t]*$", re.S | re.M)
exec(open(SRC + "/common/rvals.py", encoding="utf-8").read(), g)
def _term_html(a, b):
    a, b = a.strip(), b.strip()
    if re.search(r"[一-鿿]", a) and not re.search(r"[一-鿿]", b):
        return f'<span class="term">{b}</span>'
    if re.search(r"[一-鿿]", b) or not b or a.lower() == b.lower():
        return f'<span class="term">{a}</span>'
    return f'<span class="term">{a}<span class="en"> ({b})</span></span>'

def render(src):
    src = g["fillV"](src)
    def rep(m):
        lang, title, body = m.group(1), m.group(2).strip(), m.group(3).rstrip("\n")
        if lang == "quiz": return quiz(body)
        return code_block(lang, title, body)
    src = FENCE.sub(rep, src)
    src = re.sub(r"\{\{L:([0-9.]+)(?:\|([^}]*))?\}\}", lambda m: lesson_link(m.group(1), m.group(2)), src)
    src = re.sub(r"\{\{T:([^|}]+)\|([^}]*)\}\}", lambda m: _term_html(m.group(1), m.group(2)), src)
    return src

exec(open(SRC + "/common/shell.py", encoding="utf-8").read(), g)
exec(open(SRC + "/common/readmd.py", encoding="utf-8").read(), g)
order = [l["id"] for m, l in ALL]
stats = []
for lid in TARGET:
    m, l = IDX[lid]
    fn = SRC + "/lessons/" + anchor(lid) + ".html"
    if not os.path.exists(fn): print("Missing lesson source:", fn); continue
    body = render(open(fn, encoding="utf-8").read())
    k = order.index(lid)
    prv = order[k - 1] if k > 0 else None; nxt = order[k + 1] if k + 1 < len(order) else None
    pre = ", ".join(lesson_link(p) for p in l["pre"]) or "None (entry lesson)"
    rfile = f"R/{anchor(lid)}.R"
    rnote = (f'<a href="../{rfile}">{rfile}</a>' if os.path.exists(D + rfile) else ('No R script for this lesson' if m["id"] == "M0" else 'No standalone R script'))
    page = g["page"](lid=lid, m=m, l=l, MODULES=MODULES, GIVES=GIVES, prev=prv, nxt=nxt, body=body, engine="viz", rnote=rnote, pre_html=pre)
    page = g["fillC"](page)
    out = D + "lessons/" + anchor(lid) + ".html"
    open(out, "w", encoding="utf-8").write(page)
    open(out[:-5] + ".md", "w", encoding="utf-8").write(g["reading_md"](page, keep_links=True))
    txt = re.sub(r"<[^>]+>", "", body); words = len(re.findall(r"[A-Za-z]+", txt))
    stats.append((lid, words, body.count('class="quiz"'), body.count('data-widget')))
for s in stats: print("%-5s words %5d  quizzes %2d  widgets %d" % s)
