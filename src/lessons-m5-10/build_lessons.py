import re
# -*- coding: utf-8 -*-
"""生成 lessons/L5-1.html … L10-3.html（M5–M10 交互课件）。
用法：python3 src/lessons-m5-10/build_lessons.py
会自动检测 R/L<id>.R 脚本与 R/output/ 中以 L<id> 开头的图表/文本输出并嵌入。"""
import html, importlib.util, json, os, re, glob
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 内容源目录：src/（英文版镜像为 src/en/）
LANG = "en" if os.path.basename(SRC) == "en" else "zh"
REPO = os.path.dirname(os.path.dirname(SRC)) if LANG == "en" else os.path.dirname(SRC)
ROOT = REPO + "/en" if LANG == "en" else REPO       # 站点根：中文版是仓库根，英文版是 en/
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

# ---------- 供内容文件使用的辅助函数 ----------
def T(zh, en): return f'<span class="term">{zh}<span class="en">（{en}）</span></span>'
def W(name, title=None, **kw):
    a = f' data-title="{E(title)}"' if title else ""
    for k, v in kw.items(): a += f' data-{k}="{E(str(v))}"'
    return f'<div class="widget w2" data-widget="{name}"{a}><noscript>此处为交互组件，需要启用 JavaScript。</noscript></div>'
def WJ(name, title, key, data):
    return f'<div class="widget w2" data-widget="{name}" data-title="{E(title)}" data-key="{key}"><script type="application/json">{json.dumps(data, ensure_ascii=False)}</script></div>'
def CODE(code, head=None):
    hd = f'<div class="ctitle">{head}</div>' if head else ""
    return f'<div class="codeblk">{hd}<pre><code class="language-r">{E(code.strip(chr(10)))}</code></pre></div>'
def OUT(text, head="示意输出（数值仅为说明格式）"):
    return f'<div class="codeblk"><div class="ctitle">{head}</div><pre class="out"><code>{E(text.strip(chr(10)))}</code></pre></div>'
def box(kind, title, body):
    if not body.lstrip().startswith("<"): body = f"<p>{body}</p>"
    return f'<div class="box {kind}"><b class="bt">{title}</b>{body}</div>'
# 与 M0–M4 统一的提示框配色：说明=蓝、技巧=绿、警告=橙、关键=紫、社工视角=粉
def NOTE(t, b): return box("sw" if "社工" in t else "analogy", t, b)
def TIP(t, b): return box("key", t, b)
def WARN(t, b): return box("warnbox", t, b)
def KEY(t, b): return box("story", t, b)
def SYM(rows):
    return '<table class="sym"><tr><th>符号</th><th>读法 / 含义</th></tr>' + "".join(f"<tr><td>{s}</td><td>{m}</td></tr>" for s, m in rows) + "</table>"
def MATH(tex): return f'<div class="mathbox">\\[{tex}\\]</div>'
def TABLE(head, rows):
    return '<div class="tablewrap"><table><tr>' + "".join(f"<th>{x}</th>" for x in head) + "</tr>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table></div>"
def LINK(i, txt=None):
    m, l = LMAP[i]
    return f'<a href="{fid(i)}.html">{txt or (i + " " + l["title"])}</a>'

def RLOG(fn, start, n=None, end=None):
    """从 R/output/<fn> 截取一段原样文字：从第一个包含 start 的行开始，取 n 行，或取到包含 end 的行之前。
    课文里的“实际输出”框用它直接读日志，数字永远是当前运行的结果；找不到 start / end 时构建报错。"""
    ls = open(f"{ROOT}/R/output/{fn}", encoding="utf-8").read().splitlines()
    i = next(k for k, x in enumerate(ls) if start in x)
    j = i + n if n else next(k for k in range(i + 1, len(ls)) if end in ls[k])
    return "\n".join(ls[i:j]).rstrip()

RVG = {"ROOT": REPO}
exec(open(SRC + "common/rvals.py", encoding="utf-8").read(), RVG)   # 当前 R 输出中的 bootstrap 等结果
CTX = dict(T=T, W=W, WJ=WJ, CODE=CODE, OUT=OUT, RLOG=RLOG, NOTE=NOTE, TIP=TIP, WARN=WARN, KEY=KEY, SYM=SYM, MATH=MATH, TABLE=TABLE, LINK=LINK,
           RV=RVG["RV"], boot_table_rows=RVG["boot_table_rows"], ss_table_rows=RVG["ss_table_rows"], truth_table_rows=RVG["truth_table_rows"])
L = {}
CTX["L"] = L
for f in sorted(glob.glob(HERE + "c*.py")):
    exec(open(f, encoding="utf-8").read(), CTX)

# ---------- 参考文献（只用大纲中已核验条目） ----------
REFLIST = [r for _, items in REFS for r in items]
def ref(key):
    hits = [r for r in REFLIST if key in r["c"]]
    assert len(hits) == 1, (key, len(hits))
    r = hits[0]
    link = f' <a href="{r["url"]}" target="_blank" rel="noopener">{E(r["url"].replace("https://", ""))}</a>' if r["url"] else ""
    return f'<li>{r["c"]}{link}<div class="muted" style="font-size:.84rem">{E(r["note"])}</div></li>'

# ---------- R 脚本与输出 ----------
def r_assets(i):
    lid = fid(i)
    out = []
    sp = f"{ROOT}/R/{lid}.R"
    if os.path.exists(sp):
        code = open(sp, encoding="utf-8", errors="replace").read()
        out.append(f'<details class="more rsrc"><summary>本课配套完整脚本 <code>R/{lid}.R</code>（{len(code.splitlines())} 行，点击展开）</summary>{CODE(code)}</details>')
    else:
        out.append(f'<div class="pending">本课以阅读与写作为主，没有单独的 R 脚本。</div>')
    for sp2 in sorted(glob.glob(f"{ROOT}/R/{lid}[a-z].R")):          # 同一课的补充脚本，如 R/L7-5b.R
        code2 = open(sp2, encoding="utf-8", errors="replace").read()
        out.append(f'<details class="more rsrc"><summary>本课补充脚本 <code>R/{os.path.basename(sp2)}</code>（{len(code2.splitlines())} 行，点击展开）</summary>{CODE(code2)}</details>')
    files = sorted(set(glob.glob(f"{ROOT}/R/output/{lid}[_.-]*") + glob.glob(f"{ROOT}/R/output/{lid}[a-z][_.-]*") + glob.glob(f"{ROOT}/R/output/{lid}/*")))
    imgs = [f for f in files if f.lower().endswith((".png", ".svg", ".jpg", ".jpeg"))]
    mds = [f for f in files if f.lower().endswith(".md")]
    txts = [f for f in files if f.lower().endswith((".txt", ".csv", ".log"))]
    for f in imgs:
        rel = os.path.relpath(f, ROOT + "/lessons")
        out.append(f'<figure><img src="{E(rel)}" alt="{E(os.path.basename(f))}" loading="lazy"><figcaption>图：<code>{E(os.path.relpath(f, ROOT))}</code>（由配套脚本在模拟数据上实际运行生成）</figcaption></figure>')
    for f in mds:
        raw = open(f, encoding="utf-8", errors="replace").read()
        _title, body = _md.render_md(raw)
        rel = E(os.path.relpath(f, ROOT))
        out.append(f'<div class="md-doc"><p class="muted">来源：<code>{rel}</code></p>{body}</div>')
    txts.sort(key=lambda f: (f.lower().endswith(".csv"), f))
    for f in txts[:8]:
        t = open(f, encoding="utf-8", errors="replace").read()
        t = re.sub(r"[ \t]*\|[ =]*\|[ \t]*\d+%[^\n]*", "", t)
        t = re.sub(r"\n{3,}", "\n\n", t)
        cap = f"实际输出：<code>{E(os.path.relpath(f, ROOT))}</code>"
        if f.lower().endswith(".csv"):
            ls = t.splitlines()
            if len(ls) > 12:
                t = "\n".join(ls[:12]) + f"\n…（共 {len(ls)-1} 行数据，此处只显示前 11 行）"
            cap = f"表格文件（前几行）：<code>{E(os.path.relpath(f, ROOT))}</code>"
        elif len(t) > 12000: t = t[:12000] + "\n…（已截断，完整内容见文件）"
        out.append(OUT(t, cap))
    if os.path.exists(sp) and not files:
        out.append('<div class="pending">该脚本的输出（R/output/ 下以本课编号开头的文件）尚未生成。</div>')
    return "\n".join(out), bool(os.path.exists(sp)), len(imgs), len(txts)

# ---------- 页面 ----------
def ft(mn):
    h_, m_ = divmod(mn, 60)
    return ((f"{h_} 小时" if h_ else "") + (f" {m_} 分钟" if m_ else "")).strip()

# 测验渲染器在 src/common/quiz.py（与 M0–M4、materials/ 测评页共用）
_qspec = importlib.util.spec_from_file_location("quiz", SRC + "common/quiz.py")
_quiz = importlib.util.module_from_spec(_qspec); _qspec.loader.exec_module(_quiz)
quiz_html = _quiz.quiz_tuples

def ex_html(exs):
    out = []
    for n, (title, lvl, prompt, ans) in enumerate(exs, 1):
        out.append(f'<div class="exitem"><h4>练习 {n}：{title}<span class="lvl">{lvl}</span></h4>{prompt}<details class="answer"><summary>查看参考答案 / 思路</summary>{ans}</details></div>')
    return "\n".join(out)

SECS = [("intuition", "直觉", "s-intu", "①"), ("math", "最少数学", "s-math", "②"), ("code", "R 代码", "s-code", "③"), ("quiz", "理解检查", "s-check", "④"), ("ex", "练习", "s-ex", "⑤")]
exec(open(SRC + "common/shell.py", encoding="utf-8").read(), g)
exec(open(SRC + "common/readmd.py", encoding="utf-8").read(), g)
GIVES = {}
HDEF = {"intuition": "先建立画面", "math": "把直觉写成式子", "code": "在 R 中实现", "quiz": "即时测验", "ex": "动手练习"}
report = []
order = [l["id"] for m, l in ALL]
for i in TARGET:
    m, l = LMAP[i]
    c = L.get(i)
    if c is None:
        print("缺少内容：", i); continue
    ridx = order.index(i)
    prev_ = order[ridx - 1] if ridx > 0 else None
    next_ = order[ridx + 1] if ridx + 1 < len(order) else None
    rhtml, has_r, nimg, ntxt = r_assets(i)
    pre = "、".join(f'<a href="{fid(p)}.html">{p} {E(LMAP[p][1]["title"])}</a>' for p in l["pre"]) or "无"
    secs = []
    for key, name, cls, num in SECS:
        if key == "quiz":
            body = '<p class="quizscore"></p>' + quiz_html(c["quiz"])
        elif key == "ex":
            body = ex_html(c["ex"])
            body += '<h3>本课综合练习</h3><div class="box sw"><p>' + E(l["ex"]) + "</p></div>"
            body += "<h3>自测问题</h3><ol>" + "".join(f"<li>{E(x)}</li>" for x in l["chk"]) + "</ol><p class='muted' style='font-size:.88rem'>提示：开始下一课前，请先不看正文，用自己的一两句话回答上面的问题。</p>"
        elif key == "code":
            body = c["code"] + '<h3>配套脚本与运行输出</h3>' + rhtml
        else:
            body = c[key]
        secs.append(f'<section class="sec {cls}" id="{key}"><h2><span class="stag">{num} {name}</span>{c.get("h_" + key, HDEF[key])}</h2>{body}</section>')
    summ = "<ul>" + "".join(f"<li>{x}</li>" for x in c.get("summary", [])) + "</ul>"
    refs = "".join(ref(k) for k in c.get("refs", []))
    secs.append(f'<section class="sec s-sum" id="wrap"><h2><span class="stag">小结</span>本课小结与延伸阅读</h2>{summ}' + (f'<h3>延伸阅读</h3><ul class="refs">{refs}</ul>' if refs else "") + "</section>")
    rnote = f'<a href="../R/{fid(i)}.R">R/{fid(i)}.R</a>' if has_r else "本课无独立脚本"
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
    cjk = len(re.findall(r"[\u4e00-\u9fff]", txt))
    report.append((fid(i), cjk, has_r, nimg, ntxt))
for r in report: print("%-7s 汉字 %5d  R脚本 %-5s 图 %d 文本 %d" % r)
