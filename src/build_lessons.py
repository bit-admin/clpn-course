# -*- coding: utf-8 -*-
"""生成 lessons/L*.html 交互课件。
内容源：src/lessons/L<id>.html（HTML 片段 + 少量宏），元数据（标题、目标、概念、先修）来自 data*.py。
宏：
  ```r [标题]   ...```      → 可复制的 R 代码块
  ```out [标题] ...```      → R 输出（浅色，不可复制按钮）
  ```quiz ...```            → 测验。行首标记：Q: 题干  - 错误选项 || 反馈  + 正确选项 || 反馈
                              N: 答案 | 容差（数值题）  T: 答案1 || 答案2（文本题）  H: 提示  E: 解释
运行：python3 src/build_lessons.py
"""
import html, importlib.util, json, os, re, sys
SRC = os.path.dirname(os.path.abspath(__file__))   # 内容源目录：src/（英文版镜像为 src/en/）
LANG = "en" if os.path.basename(SRC) == "en" else "zh"
REPO = os.path.dirname(os.path.dirname(SRC)) if LANG == "en" else os.path.dirname(SRC)
ROOT = REPO + "/en" if LANG == "en" else REPO       # 站点根：中文版是仓库根，英文版是 en/
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
GIVES = {"M0": "动机与整体地图：知道终点在哪里、为什么值得走。",
 "M1": "统计语言：均值、方差、相关、标准误、p 值——读懂 CLPN 输出里每一个数字的前提。",
 "M2": "R 技能：从零到能独立写 CLPN 估计代码。",
 "M3": "回归与 LASSO：CLPN 的“发动机”，每个 T2 节点就是一次正则化回归。",
 "M4": "纵向数据：知道 T1/T2 数据怎么来、怎么整理、缺失怎么办。",
 "M5": "CLPM / RI-CLPM：理解交叉滞后的含义与被试间/被试内的陷阱。",
 "M6": "网络心理测量：节点、边、偏相关、正则化、中心性。",
 "M7": "CLPN 本身：估计、作图、出/入期望影响。",
 "M8": "稳定性检验：bootstrap 与 CS 系数，判断结果能否被信任。",
 "M9": "读论文、批判与报告规范。",
 "M10": "毕业项目：独立完成一次完整的 CLPN。"}
def ft(m):
    h, mm = divmod(m, 60)
    return ((f"{h} 小时" if h else "") + (f" {mm} 分钟" if mm else "")).strip()
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

# 测验渲染器在 src/common/quiz.py（M0–M4、M5–M10、materials/ 测评页共用）
_qspec = importlib.util.spec_from_file_location("quiz", SRC + "/common/quiz.py")
_quiz = importlib.util.module_from_spec(_qspec); _qspec.loader.exec_module(_quiz)
quiz = _quiz.quiz

FENCE = re.compile(r"^```(\w+)[ \t]*(.*?)\n(.*?)^```[ \t]*$", re.S | re.M)
exec(open(SRC + "/common/rvals.py", encoding="utf-8").read(), g)
def render(src):
    src = g["fillV"](src)
    def rep(m):
        lang, title, body = m.group(1), m.group(2).strip(), m.group(3).rstrip("\n")
        if lang == "quiz": return quiz(body)
        return code_block(lang, title, body)
    src = FENCE.sub(rep, src)
    # {{L:1.4}} → 课程链接
    src = re.sub(r"\{\{L:([0-9.]+)(?:\|([^}]*))?\}\}", lambda m: lesson_link(m.group(1), m.group(2)), src)
    # {{T:中文|English}} → 双语术语
    src = re.sub(r"\{\{T:([^|}]+)\|([^}]+)\}\}", lambda m: f'<span class="term">{m.group(1)}<span class="en">（{m.group(2)}）</span></span>', src)
    return src

exec(open(SRC + "/common/shell.py", encoding="utf-8").read(), g)
exec(open(SRC + "/common/readmd.py", encoding="utf-8").read(), g)
order = [l["id"] for m, l in ALL]
stats = []
for lid in TARGET:
    m, l = IDX[lid]
    fn = SRC + "/lessons/" + anchor(lid) + ".html"
    if not os.path.exists(fn): print("缺少内容源", fn); continue
    body = render(open(fn, encoding="utf-8").read())
    k = order.index(lid)
    prv = order[k - 1] if k > 0 else None; nxt = order[k + 1] if k + 1 < len(order) else None
    pre = "、".join(lesson_link(p) for p in l["pre"]) or "无（起点课）"
    rfile = f"R/{anchor(lid)}.R"
    rnote = (f'<a href="../{rfile}">{rfile}</a>' if os.path.exists(D + rfile) else ('本课无 R 脚本' if m["id"] == "M0" else '本课无独立脚本'))
    page = g["page"](lid=lid, m=m, l=l, MODULES=MODULES, GIVES=GIVES, prev=prv, nxt=nxt, body=body, engine="viz", rnote=rnote, pre_html=pre)
    page = g["fillC"](page)   # 课程规模宏 {{C:…}}（src/data4.py；模块导言里也有）
    out = D + "lessons/" + anchor(lid) + ".html"
    open(out, "w", encoding="utf-8").write(page)
    open(out[:-5] + ".md", "w", encoding="utf-8").write(g["reading_md"](page, keep_links=True))
    txt = re.sub(r"<[^>]+>", "", body); zh = len(re.findall(r"[\u4e00-\u9fff]", txt))
    stats.append((lid, zh, body.count('class="quiz"'), body.count('data-widget')))
for s in stats: print("%-5s 汉字 %5d  测验 %2d  组件 %d" % s)
