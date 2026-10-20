# -*- coding: utf-8 -*-
"""全课程统一的课件“外壳”（页头、顶栏、目录侧栏、标题区、翻页、页脚）。
被 src/build_lessons.py（M0–M4）和 src/lessons-m5-10/build_lessons.py（M5–M10）共同调用，
保证全部课程页面的外观与导航完全一致。所有资源都在 lessons/assets/ 下，离线可用。"""
import html, json
E = html.escape
anchor = lambda i: "L" + i.replace(".", "-")
COPY_NOTE = (
    '© 2026 ZHANG. Content '
    '<a href="https://creativecommons.org/licenses/by/4.0/" rel="license noopener" target="_blank">CC BY 4.0</a>; '
    'code '
    '<a href="https://opensource.org/license/mit" rel="license noopener" target="_blank">MIT</a>. '
    '<a href="https://github.com/bit-admin/clpn-course" rel="noopener" target="_blank">GitHub</a>'
)

def ft(m):
    h, mm = divmod(m, 60)
    return ((f"{h} 小时" if h else "") + (f" {mm} 分钟" if mm else "")).strip()

def modules_json(MODULES, GIVES):
    return json.dumps([dict(id=m["id"], title=m["title"], short=m["title"].split("：")[0].split("（")[0], intro=m["intro"], color=m["color"],
                            n=len(m["lessons"]), hours=round(sum(l["time"] for l in m["lessons"]) / 60, 1), gives=GIVES.get(m["id"], ""))
                       for m in MODULES], ensure_ascii=False)

def course_nav(MODULES, cur, base="", mat="..", docs=True):
    """侧栏下半部分：全部课程（当前模块默认展开、当前课高亮；进阶选学课标“（选学）”）。
    mat 是从当前页回到站点根的相对路径，资料链接据此拼出。
    资料页自己已有一份学习资料目录时，传 docs=False，避免再列一遍。"""
    out = ['<div class="allnav"><b>全部课程</b>']
    for m in MODULES:
        here = any(l["id"] == cur for l in m["lessons"])
        lis = "".join(f'<li><a href="{base}{anchor(l["id"])}.html"' + (' class="cur" aria-current="page"' if l["id"] == cur else "") +
                      f'><span>{l["id"]}</span>{E(l["title"])}{"（选学）" if l.get("opt") else ""}</a></li>' for l in m["lessons"])
        out.append(f'<details{" open" if here else ""} style="--mc:{m["color"]}"><summary>{m["id"]} {E(m["title"].split("：")[0].split("（")[0])}</summary><ul>{lis}</ul></details>')
    if docs:
        items = [("START_HERE.html", "学习指南"), ("materials/glossary.html", "术语表"), ("materials/cheatsheets.html", "速查卡"),
                 ("materials/formulas.html", "公式表"), ("materials/faq.html", "常见问题 FAQ"), ("materials/study_log.html", "学习日志"),
                 ("materials/writing.html", "写作工作坊"), ("materials/reading.html", "论文阅读包"),
                 ("materials/case_elsoc.html", "真实数据案例"),
                 ("materials/assessment.html", "测评"), ("downloads/index.html", "下载")]
        out.append('<div class="matlinks"><b>学习资料</b>' + "".join(f'<a href="{mat}/{href}">{label}</a>' for href, label in items) + "</div>")
    out.append("</div>")
    return "".join(out)

def page(*, lid, m, l, MODULES, GIVES, prev, nxt, body, engine, lead="", rnote="", pre_html=""):
    """engine: 'viz'（M0–M4 组件库 viz.js）或 'viz2'（M5–M10 组件库 viz-m5-10.js）"""
    s = l.get("sessions", 1)
    eng = ('<script>window.COURSE_MODULES=' + modules_json(MODULES, GIVES) + ';</script>\n<script defer src="assets/viz.js"></script>') if engine == "viz" \
        else '<script defer src="assets/viz-m5-10.js"></script>'
    def pg(i, cls, lab):
        if not i: return f'<a href="../index.html" class="{cls}"><small>{lab}</small>返回课程大纲</a>'
        ll = next(x for mm in MODULES for x in mm["lessons"] if x["id"] == i)
        return f'<a href="{anchor(i)}.html" class="{cls}"><small>{lab}</small>{i} {E(ll["title"])}</a>'
    # 模块最后一节核心课（以及模块末尾的选学课）在翻页前提示本模块的阶段测验；10.3 另提示期末考试
    core = [x for x in m["lessons"] if not x.get("opt")]
    slug, aq = m["id"].lower(), ""
    if l is core[-1]:
        extra = "7.6、7.7 是进阶选学课，学过以后再做测验页最后的进阶题。" if any(x.get("opt") for x in m["lessons"]) else ""
        aq = f'<p>本模块的核心课到这里学完了。去做 <a href="../materials/assess_{slug}.html">{m["id"]} 阶段测验</a>，一次答对 70% 及以上再进入下一个模块。{extra}</p>'
        if lid == "10.3": aq += '<p>学完本课后做<a href="../materials/assess_final.html">期末考试</a>（约 90 分钟）。</p>'
    elif l.get("opt") and l is m["lessons"][-1]:
        aq = f'<p>学过本模块的进阶选学课以后，可以做 <a href="../materials/assess_{slug}.html#adv">{m["id"]} 阶段测验最后的进阶题</a>（不计入本模块的正确率）。</p>'
    if aq: body += f'<div class="box key"><b class="bt">阶段测验</b>{aq}</div>'
    # 9.3（报告规范）和 10.3（撰写结果）提示写作工作坊与论文阅读包
    if lid in ("9.3", "10.3"):
        body += ('<div class="box key"><b class="bt">写作练习</b><p>到<a href="../materials/writing.html">写作工作坊</a>看四个“改写前 → 改写后”的范例（数据与测量、统计分析、结果、局限），'
                 '并完成改写任务；想看真实论文怎样写，见<a href="../materials/reading.html">论文阅读包</a>。</p></div>')
    if lid == "10.3":
        body += ('<div class="box key"><b class="bt">真实数据</b><p>课文用的是模拟数据。学完 7.4 和 8.2 之后，可以看<a href="../materials/case_elsoc.html">ELSOC 真实数据案例</a>：'
                 '用公开的抑郁症状追踪数据走完同一套“仅 LASSO”CLPN。分析文件 <code>data/elsoc_phq8_wide.csv</code> 随课程提供，运行 <code>R/case_elsoc.R</code> 即可复现页面上的数字。</p></div>')
    con = "".join(f'<li><b>{E(z)}</b><span class="en">{E(e)}</span></li>' for z, e in l["con"])
    objs = "".join(f"<li>{E(o)}</li>" for o in l["obj"])
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{lid} {E(l["title"])} · CLPN 从零开始</title>
<link rel="stylesheet" href="assets/vendor/fonts/fonts.css">
<link rel="stylesheet" href="assets/vendor/katex/katex.min.css">
<script defer src="assets/vendor/katex/katex.min.js"></script>
<script defer src="assets/vendor/katex/contrib/auto-render.min.js"></script>
<link rel="stylesheet" href="assets/course.css">
<link rel="alternate" type="text/markdown" href="{anchor(lid)}.md" title="阅读文本">
{eng}
<script defer src="assets/lesson.js"></script>
</head>
<body data-lid="{lid}" style="--c:{m["color"]}">
<div class="progressline"></div>
<div class="topbar"><button id="tocBtn" type="button" aria-label="打开目录">目录</button><a class="home" href="../index.html#{anchor(lid)}">CLPN 课程大纲</a><span class="crumb">{m["id"]} {E(m["title"])} / {lid}</span><span class="sp"></span>
<button id="doneBtn" type="button">标记本课为已完成</button><a class="act" id="readView" href="{anchor(lid)}.md" target="_blank" rel="noopener">纯文本查看</a><button id="readBtn" type="button">复制给 LLM</button><a class="act langSwitch" href="../en/lessons/{anchor(lid)}.html">English</a><button id="themeBtn" type="button" aria-label="切换深浅色">深色</button></div>
<div class="wrap">
<nav class="toc" aria-label="本课目录"><div class="toc-local"></div>{course_nav(MODULES, lid)}</nav>
<main>
<header class="lhero"><div class="mnum">模块 {m["id"][1:]} · {E(m["en"])} · 第 {lid} 课</div>
<h1>{E(l["title"])}</h1>
<div class="facts">{"<span>进阶选学（不在标准节奏里）</span>" if l.get("opt") else ""}<span>课文学习 {ft(l["time"])}{f"（分 {s} 次）" if s > 1 else ""}</span><span>先修：{pre_html}</span><span>配套脚本：{rnote}</span></div></header>
<section class="card goals"><h2>本课学习目标</h2><div class="obj"><ol>{objs}</ol></div>
<h3>核心概念</h3><ul class="concepts">{con}</ul>
{lead}
<p class="muted structnote">本课结构：直觉 → 最少数学 → R 代码 → 理解检查 → 练习 → 小结。文中的交互图示可拖动或点击；测验答错会先给提示，答错两次可查看解析。</p></section>
{body}
<nav class="pager">{pg(prev, "pv", "上一课")}{pg(nxt, "nx", "下一课")}</nav>
<p class="foot">CLPN 从零开始 · 第 {lid} 课 · <a href="../index.html#{anchor(lid)}">返回大纲</a></p>
<p class="copy">{COPY_NOTE}</p>
</main></div>
</body></html>
'''
