# -*- coding: utf-8 -*-
"""Build en/lessons/L5-1.html … L10-3.html (English M5–M10 interactive lessons)."""
import html, importlib.util, json, os, re, glob
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG = "en" if os.path.basename(SRC) == "en" else "zh"
REPO = os.path.dirname(os.path.dirname(SRC)) if LANG == "en" else os.path.dirname(SRC)
ROOT = REPO + "/en" if LANG == "en" else REPO
_mdspec = importlib.util.spec_from_file_location("mdhtml", SRC + "/common/mdhtml.py")
_md = importlib.util.module_from_spec(_mdspec); _mdspec.loader.exec_module(_md)
SRC = SRC + "/"
HERE = SRC + "lessons-m5-10/"
E = html.escape
g = {}
for f in ["data1", "data2", "data3", "data4"]:
    exec(open(SRC + f + ".py", encoding="utf-8").read(), g)
MODULES, REFS = g["MODULES"], g["REFS"]
ALL = [(m, l) for m in MODULES for l in m["lessons"]]
LMAP = {l["id"]: (m, l) for m, l in ALL}
TARGET = [l["id"] for m, l in ALL if m["id"] in ("M5", "M6", "M7", "M8", "M9", "M10")]
fid = lambda i: "L" + i.replace(".", "-")

def T(a, b=""):
    a, b = (a or "").strip(), (b or "").strip()
    if re.search(r"[一-鿿]", a) and not re.search(r"[一-鿿]", b):
        return f'<span class="term">{b}</span>'
    if re.search(r"[一-鿿]", b) or not b or a.lower() == b.lower():
        return f'<span class="term">{a}</span>'
    return f'<span class="term">{a}<span class="en"> ({b})</span></span>'

def W(name, title=None, **kw):
    a = f' data-title="{E(title)}"' if title else ""
    for k, v in kw.items(): a += f' data-{k}="{E(str(v))}"'
    return f'<div class="widget w2" data-widget="{name}"{a}><noscript>Interactive widget (requires JavaScript).</noscript></div>'
def WJ(name, title, key, data):
    return f'<div class="widget w2" data-widget="{name}" data-title="{E(title)}" data-key="{key}"><script type="application/json">{json.dumps(data, ensure_ascii=False)}</script></div>'
def CODE(code, head=None):
    hd = f'<div class="ctitle">{head}</div>' if head else ""
    return f'<div class="codeblk">{hd}<pre><code class="language-r">{E(code.strip(chr(10)))}</code></pre></div>'
def OUT(text, head="Illustrative output (numbers shown for format)"):
    return f'<div class="codeblk"><div class="ctitle">{head}</div><pre class="out"><code>{E(text.strip(chr(10)))}</code></pre></div>'
def box(kind, title, body):
    if not body.lstrip().startswith("<"): body = f"<p>{body}</p>"
    return f'<div class="box {kind}"><b class="bt">{title}</b>{body}</div>'
def NOTE(t, b): return box("sw" if ("social work" in t.lower() or "practice" in t.lower() or "社工" in t) else "analogy", t, b)
def TIP(t, b): return box("key", t, b)
def WARN(t, b): return box("warnbox", t, b)
def KEY(t, b): return box("story", t, b)
def SYM(rows):
    return '<table class="sym"><tr><th>Symbol</th><th>Reading / Meaning</th></tr>' + "".join(f"<tr><td>{s}</td><td>{m}</td></tr>" for s, m in rows) + "</table>"
def MATH(tex): return f'<div class="mathbox">\\[{tex}\\]</div>'
def TABLE(head, rows):
    return '<div class="tablewrap"><table><tr>' + "".join(f"<th>{x}</th>" for x in head) + "</tr>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table></div>"
def LINK(i, txt=None):
    m, l = LMAP[i]
    return f'<a href="{fid(i)}.html">{txt or (i + " " + l["title"])}</a>'

def RLOG(fn, start, n=None, end=None):
    """Verbatim slice of en/R/output/<fn>: from the first line containing `start`, n lines or up to the line containing `end`."""
    ls = open(f"{ROOT}/R/output/{fn}", encoding="utf-8").read().splitlines()
    i = next((k for k, x in enumerate(ls) if start in x), None)
    if i is None: raise SystemExit(f"RLOG: {start!r} not found in en/R/output/{fn}")
    j = i + n if n else next((k for k in range(i + 1, len(ls)) if end in ls[k]), None)
    if j is None: raise SystemExit(f"RLOG: end {end!r} not found after {start!r} in en/R/output/{fn}")
    return "\n".join(ls[i:j]).rstrip()

RVG = {"ROOT": REPO}
exec(open(SRC + "common/rvals.py", encoding="utf-8").read(), RVG)
L = {}
NODES = ["lone1", "lone2", "lone3", "lone4", "dep1", "dep2", "dep3", "dep4", "dep5"]
ZH = dict(lone1="Lack of companionship", lone2="Feeling left out", lone3="Feeling isolated", lone4="No one understands me",
          dep1="Depressed mood", dep2="Loss of interest", dep3="Sleep problems", dep4="Fatigue", dep5="Worthlessness")
def TRUTH_MAT(prefix, caption, zero_dot=False):
    def cell(k, j):
        v = RVG["RV"][f"{prefix}_{k}>{j}"]
        if zero_dot and v in ("0.000", "−0.000"): v = "·"
        return f'<span class="muted">{v}</span>' if k == j else v
    return (f'<div style="flex:1 1 30rem;min-width:0"><p style="margin:.2rem 0;font-size:.9rem"><b>{caption}</b></p>'
            + TABLE(["T1 ↓ / T2 →"] + NODES, [[k] + [cell(k, j) for j in NODES] for k in NODES]) + "</div>")
def TWO_TRUTHS():
    return ('<div style="display:flex;flex-wrap:wrap;gap:1rem;font-size:.82rem">'
            + TRUTH_MAT("pop", "Population target (true_B_population.csv)")
            + TRUTH_MAT("win", "Within-person truth (true_B_within.csv; · = 0)", zero_dot=True) + "</div>")
def ADD(lid, key, html):
    L[lid][key] = L[lid].get(key, "") + html
CTX = dict(T=T, W=W, WJ=WJ, CODE=CODE, OUT=OUT, RLOG=RLOG, NOTE=NOTE, TIP=TIP, WARN=WARN, KEY=KEY, SYM=SYM, MATH=MATH, TABLE=TABLE, LINK=LINK,
           RV=RVG["RV"], boot_table_rows=RVG["boot_table_rows"], ss_table_rows=RVG["ss_table_rows"], truth_table_rows=RVG["truth_table_rows"],
           NODES=NODES, ZH=ZH, TRUTH_MAT=TRUTH_MAT, TWO_TRUTHS=TWO_TRUTHS, ADD=ADD, L=L)
for f in sorted(glob.glob(HERE + "c*.py")):
    exec(open(f, encoding="utf-8").read(), CTX)

REFLIST = [r for _, items in REFS for r in items]
def ref(key):
    hits = [r for r in REFLIST if key in r["c"]]
    assert len(hits) == 1, (key, len(hits))
    r = hits[0]
    link = f' <a href="{r["url"]}" target="_blank" rel="noopener">{E(r["url"].replace("https://", ""))}</a>' if r["url"] else ""
    return f'<li>{r["c"]}{link}<div class="muted" style="font-size:.84rem">{E(r["note"])}</div></li>'

def r_assets(i):
    lid = fid(i)
    out = []
    sp = f"{ROOT}/R/{lid}.R"
    if os.path.exists(sp):
        code = open(sp, encoding="utf-8", errors="replace").read()
        out.append(f'<details class="more rsrc"><summary>Complete companion script <code>R/{lid}.R</code> ({len(code.splitlines())} lines, click to expand)</summary>{CODE(code)}</details>')
    else:
        out.append(f'<div class="pending">This lesson focuses on reading and writing and does not have a standalone R script.</div>')
    for sp2 in sorted(glob.glob(f"{ROOT}/R/{lid}[a-z].R")):
        code2 = open(sp2, encoding="utf-8", errors="replace").read()
        out.append(f'<details class="more rsrc"><summary>Supplementary script <code>R/{os.path.basename(sp2)}</code> ({len(code2.splitlines())} lines, click to expand)</summary>{CODE(code2)}</details>')
    files = sorted(set(glob.glob(f"{ROOT}/R/output/{lid}[_.-]*") + glob.glob(f"{ROOT}/R/output/{lid}[a-z][_.-]*") + glob.glob(f"{ROOT}/R/output/{lid}/*")))
    imgs = [f for f in files if f.lower().endswith((".png", ".svg", ".jpg", ".jpeg"))]
    mds = [f for f in files if f.lower().endswith(".md")]
    txts = [f for f in files if f.lower().endswith((".txt", ".csv", ".log"))]
    for f in imgs:
        rel = os.path.relpath(f, ROOT + "/lessons")
        out.append(f'<figure><img src="{E(rel)}" alt="{E(os.path.basename(f))}" loading="lazy"><figcaption>Figure: <code>{E(os.path.relpath(f, ROOT))}</code> (generated by running the companion script on the simulated dataset)</figcaption></figure>')
    for f in mds:
        raw = open(f, encoding="utf-8", errors="replace").read()
        _title, body = _md.render_md(raw)
        rel = E(os.path.relpath(f, ROOT))
        out.append(f'<div class="md-doc"><p class="muted">Source: <code>{rel}</code></p>{body}</div>')
    txts.sort(key=lambda f: (f.lower().endswith(".csv"), f))
    for f in txts[:8]:
        t = open(f, encoding="utf-8", errors="replace").read()
        t = re.sub(r"[ \t]*\|[ =]*\|[ \t]*\d+%[^\n]*", "", t)
        t = re.sub(r"\n{3,}", "\n\n", t)
        cap = f"Actual output: <code>{E(os.path.relpath(f, ROOT))}</code>"
        if f.lower().endswith(".csv"):
            ls = t.splitlines()
            if len(ls) > 12:
                t = "\n".join(ls[:12]) + f"\n… ({len(ls)-1} rows total; showing first 11 rows)"
            cap = f"Table file (first rows): <code>{E(os.path.relpath(f, ROOT))}</code>"
        elif len(t) > 12000: t = t[:12000] + "\n… (truncated; see file for full output)"
        out.append(OUT(t, cap))
    if os.path.exists(sp) and not files:
        out.append('<div class="pending">Output files for this script in R/output/ have not been generated yet.</div>')
    return "\n".join(out), bool(os.path.exists(sp)), len(imgs), len(txts)

_qspec = importlib.util.spec_from_file_location("quiz", SRC + "common/quiz.py")
_quiz = importlib.util.module_from_spec(_qspec); _qspec.loader.exec_module(_quiz)
quiz_html = _quiz.quiz_tuples

def ex_html(exs):
    out = []
    for n, (title, lvl, prompt, ans) in enumerate(exs, 1):
        out.append(f'<div class="exitem"><h4>Exercise {n}: {title}<span class="lvl">{lvl}</span></h4>{prompt}<details class="answer"><summary>Show Reference Solution / Walkthrough</summary>{ans}</details></div>')
    return "\n".join(out)

SECS = [("intuition", "Intuition", "s-intu", "①"), ("math", "Essential Math", "s-math", "②"), ("code", "R Code", "s-code", "③"), ("quiz", "Concept Check", "s-check", "④"), ("ex", "Exercises", "s-ex", "⑤")]
exec(open(SRC + "common/shell.py", encoding="utf-8").read(), g)
exec(open(SRC + "common/readmd.py", encoding="utf-8").read(), g)
GIVES = {}
HDEF = {"intuition": "Build the Mental Picture", "math": "Write the Intuition as Equations", "code": "Implement in R", "quiz": "Instant Check", "ex": "Hands-On Practice"}
report = []
order = [l["id"] for m, l in ALL]
for i in TARGET:
    m, l = LMAP[i]
    c = L.get(i)
    if c is None:
        print("Missing lesson content:", i); continue
    ridx = order.index(i)
    prev_ = order[ridx - 1] if ridx > 0 else None
    next_ = order[ridx + 1] if ridx + 1 < len(order) else None
    rhtml, has_r, nimg, ntxt = r_assets(i)
    pre = ", ".join(f'<a href="{fid(p)}.html">{p} {E(LMAP[p][1]["title"])}</a>' for p in l["pre"]) or "None"
    secs = []
    for key, name, cls, num in SECS:
        if key == "quiz":
            body = '<p class="quizscore"></p>' + quiz_html(c["quiz"])
        elif key == "ex":
            body = ex_html(c["ex"])
            body += '<h3>Integrative Exercise</h3><div class="box sw"><p>' + E(l["ex"]) + "</p></div>"
            body += "<h3>Self-Check Questions</h3><ol>" + "".join(f"<li>{E(x)}</li>" for x in l["chk"]) + "</ol><p class='muted' style='font-size:.88rem'>Tip: Before starting the next lesson, answer each question above in one or two sentences without looking at the text.</p>"
        elif key == "code":
            body = c["code"] + '<h3>Companion Script &amp; Output</h3>' + rhtml
        else:
            body = c[key]
        secs.append(f'<section class="sec {cls}" id="{key}"><h2><span class="stag">{num} {name}</span>{c.get("h_" + key, HDEF[key])}</h2>{body}</section>')
    summ = "<ul>" + "".join(f"<li>{x}</li>" for x in c.get("summary", [])) + "</ul>"
    refs = "".join(ref(k) for k in c.get("refs", []))
    secs.append(f'<section class="sec s-sum" id="wrap"><h2><span class="stag">Summary</span>Key Takeaways &amp; Further Reading</h2>{summ}' + (f'<h3>Further Reading</h3><ul class="refs">{refs}</ul>' if refs else "") + "</section>")
    rnote = f'<a href="../R/{fid(i)}.R">R/{fid(i)}.R</a>' if has_r else "No standalone R script"
    page = g["page"](lid=i, m=m, l=l, MODULES=MODULES, GIVES=GIVES, prev=prev_, nxt=next_, body="".join(secs), engine="viz2",
                     lead=c.get("lead", ""), rnote=rnote, pre_html=pre)
    page = g["fillC"](RVG["fillV"](page))
    path = f"{ROOT}/lessons/{fid(i)}.html"
    open(path, "w", encoding="utf-8").write(page)
    open(path[:-5] + ".md", "w", encoding="utf-8").write(g["reading_md"](page, keep_links=True))
    txt = re.sub(r"<nav.*?</nav>", "", page, flags=re.S)
    txt = re.sub(r"<pre.*?</pre>", "", txt, flags=re.S)
    txt = re.sub(r"<script.*?</script>", "", txt, flags=re.S)
    txt = re.sub(r"<[^>]+>", "", txt)
    words = len(re.findall(r"[A-Za-z]+", txt))
    report.append((fid(i), words, has_r, nimg, ntxt))
for r in report: print("%-7s words %5d  R %-5s figs %d txts %d" % r)
