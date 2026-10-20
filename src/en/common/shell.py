# -*- coding: utf-8 -*-
"""Shared HTML shell for all English course pages (header, topbar, TOC sidebar, hero, pager, footer).
Used by src/en/build_lessons.py (M0–M4) and src/en/lessons-m5-10/build_lessons.py (M5–M10)."""
import html, json, re
E = html.escape
anchor = lambda i: "L" + i.replace(".", "-")
COPY_NOTE = (
    '© 2026 ZHANG. Content '
    '<a href="https://creativecommons.org/licenses/by/4.0/" rel="license noopener" target="_blank">CC BY 4.0</a>; '
    'code '
    '<a href="https://opensource.org/license/mit" rel="license noopener" target="_blank">MIT</a>. '
    '<a href="https://github.com/bit-admin/clpn-course" rel="noopener" target="_blank">GitHub</a>'
)

def _has_cjk(s):
    return bool(re.search(r"[一-鿿]", s or ""))

def _short_title(t):
    return re.split(r"[:：\(（]", t)[0].strip()

def _con_pair(a, b):
    if _has_cjk(a) and not _has_cjk(b):
        return b, ""
    if _has_cjk(b):
        return a, ""
    if a.strip().lower() == (b or "").strip().lower():
        return a, ""
    return a, b

def ft(m):
    h, mm = divmod(m, 60)
    return ((f"{h} hr" if h else "") + (f" {mm} min" if mm else "")).strip()

def modules_json(MODULES, GIVES):
    return json.dumps([dict(id=m["id"], title=m["title"], short=_short_title(m["title"]), intro=m["intro"], color=m["color"],
                            n=len(m["lessons"]), hours=round(sum(l["time"] for l in m["lessons"]) / 60, 1), gives=GIVES.get(m["id"], ""))
                       for m in MODULES], ensure_ascii=False)

def course_nav(MODULES, cur, base="", mat="..", docs=True):
    """Lower half of the sidebar: all lessons + study materials."""
    out = ['<div class="allnav"><b>All Lessons</b>']
    for m in MODULES:
        here = any(l["id"] == cur for l in m["lessons"])
        lis = "".join(f'<li><a href="{base}{anchor(l["id"])}.html"' + (' class="cur" aria-current="page"' if l["id"] == cur else "") +
                      f'><span>{l["id"]}</span>{E(l["title"])}{" (optional)" if l.get("opt") else ""}</a></li>' for l in m["lessons"])
        out.append(f'<details{" open" if here else ""} style="--mc:{m["color"]}"><summary>{m["id"]} {E(_short_title(m["title"]))}</summary><ul>{lis}</ul></details>')
    if docs:
        items = [("START_HERE.html", "Study Guide"), ("materials/glossary.html", "Glossary"), ("materials/cheatsheets.html", "Cheat Sheets"),
                 ("materials/formulas.html", "Formula Reference"), ("materials/faq.html", "FAQ"), ("materials/study_log.html", "Study Log"),
                 ("materials/writing.html", "Writing Workshop"), ("materials/reading.html", "Paper Reading Pack"),
                 ("materials/case_elsoc.html", "Real-Data Case (ELSOC)"),
                 ("materials/assessment.html", "Assessments"), ("downloads/index.html", "Download")]
        out.append('<div class="matlinks"><b>Study Materials</b>' + "".join(f'<a href="{mat}/{href}">{label}</a>' for href, label in items) + "</div>")
    out.append("</div>")
    return "".join(out)

def page(*, lid, m, l, MODULES, GIVES, prev, nxt, body, engine, lead="", rnote="", pre_html=""):
    """engine: 'viz' (M0–M4 widget library viz.js) or 'viz2' (M5–M10 widget library viz-m5-10.js)"""
    s = l.get("sessions", 1)
    eng = ('<script>window.COURSE_MODULES=' + modules_json(MODULES, GIVES) + ';</script>\n<script defer src="assets/viz.js"></script>') if engine == "viz" \
        else '<script defer src="assets/viz-m5-10.js"></script>'
    def pg(i, cls, lab):
        if not i: return f'<a href="../index.html" class="{cls}"><small>{lab}</small>Back to Syllabus</a>'
        ll = next(x for mm in MODULES for x in mm["lessons"] if x["id"] == i)
        return f'<a href="{anchor(i)}.html" class="{cls}"><small>{lab}</small>{i} {E(ll["title"])}</a>'
    core = [x for x in m["lessons"] if not x.get("opt")]
    slug, aq = m["id"].lower(), ""
    if l is core[-1]:
        extra = " Lessons 7.6 and 7.7 are optional advanced lessons; after studying them, do the advanced questions at the end of the quiz page." if any(x.get("opt") for x in m["lessons"]) else ""
        aq = f'<p>You have finished the core lessons of this module. Take the <a href="../materials/assess_{slug}.html">{m["id"]} module quiz</a>, and move on to the next module once you get at least 70% right on the first try.{extra}</p>'
        if lid == "10.3": aq += '<p>After this lesson, take the <a href="../materials/assess_final.html">final exam</a> (about 90 minutes).</p>'
    elif l.get("opt") and l is m["lessons"][-1]:
        aq = f'<p>Once you have studied this module\'s optional advanced lessons, you can do the <a href="../materials/assess_{slug}.html#adv">advanced questions at the end of the {m["id"]} module quiz</a> (they do not count toward the module score).</p>'
    if aq: body += f'<div class="box key"><b class="bt">Module quiz</b>{aq}</div>'
    if lid in ("9.3", "10.3"):
        body += ('<div class="box key"><b class="bt">Writing practice</b><p>In the <a href="../materials/writing.html">Writing Workshop</a>, read the four "before → after" examples (Data and Measures, Statistical Analysis, Results, Limitations) '
                 'and do the rewriting tasks; to see how real papers are written, use the <a href="../materials/reading.html">Paper Reading Pack</a>.</p></div>')
    if lid == "10.3":
        body += ('<div class="box key"><b class="bt">Real data</b><p>The lessons use simulated data. After Lessons 7.4 and 8.2, look at the <a href="../materials/case_elsoc.html">ELSOC real-data case</a>: '
                 'it runs the same LASSO-only CLPN on public panel data on depressive symptoms. The analysis file <code>data/elsoc_phq8_wide.csv</code> comes with the course; run <code>R/case_elsoc.R</code> to reproduce the numbers on that page.</p></div>')
    con_items = []
    for a, b in l["con"]:
        main_t, sub_t = _con_pair(a, b)
        con_items.append(f'<li><b>{E(main_t)}</b>' + (f'<span class="en">{E(sub_t)}</span>' if sub_t else '') + '</li>')
    con = "".join(con_items)
    objs = "".join(f"<li>{E(o)}</li>" for o in l["obj"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{lid} {E(l["title"])} · CLPN From Scratch</title>
<link rel="stylesheet" href="assets/vendor/fonts/fonts.css">
<link rel="stylesheet" href="assets/vendor/katex/katex.min.css">
<script defer src="assets/vendor/katex/katex.min.js"></script>
<script defer src="assets/vendor/katex/contrib/auto-render.min.js"></script>
<link rel="stylesheet" href="assets/course.css">
<link rel="alternate" type="text/markdown" href="{anchor(lid)}.md" title="Plain text">
{eng}
<script defer src="assets/lesson.js"></script>
</head>
<body data-lid="{lid}" style="--c:{m["color"]}">
<div class="progressline"></div>
<div class="topbar"><button id="tocBtn" type="button" aria-label="Open table of contents">Contents</button><a class="home" href="../index.html#{anchor(lid)}">CLPN Syllabus</a><span class="crumb">{m["id"]} {E(m["title"])} / {lid}</span><span class="sp"></span>
<button id="doneBtn" type="button">Mark lesson complete</button><a class="act" id="readView" href="{anchor(lid)}.md" target="_blank" rel="noopener">Plain text</a><button id="readBtn" type="button">Copy for LLM</button><a class="act langSwitch" href="../../lessons/{anchor(lid)}.html">中文</a><button id="themeBtn" type="button" aria-label="Switch to dark mode">Dark</button></div>
<div class="wrap">
<nav class="toc" aria-label="Lesson table of contents"><div class="toc-local"></div>{course_nav(MODULES, lid)}</nav>
<main>
<header class="lhero"><div class="mnum">Module {m["id"][1:]} · {E(m["en"])} · Lesson {lid}</div>
<h1>{E(l["title"])}</h1>
<div class="facts">{"<span>Optional advanced lesson (not part of the standard pace)</span>" if l.get("opt") else ""}<span>Study time {ft(l["time"])}{f" (in {s} sessions)" if s > 1 else ""}</span><span>Prerequisites: {pre_html}</span><span>R script: {rnote}</span></div></header>
<section class="card goals"><h2>Learning Objectives</h2><div class="obj"><ol>{objs}</ol></div>
<h3>Core Concepts</h3><ul class="concepts">{con}</ul>
{lead}
<p class="muted structnote">Lesson structure: Intuition → Essential Math → R Code → Concept Check → Exercises → Summary. You can drag or click the interactive figures; a wrong quiz answer first gets a hint, and after two wrong answers you can see the explanation.</p></section>
{body}
<nav class="pager">{pg(prev, "pv", "Previous")}{pg(nxt, "nx", "Next")}</nav>
<p class="foot">CLPN From Scratch · Lesson {lid} · <a href="../index.html#{anchor(lid)}">Back to Syllabus</a></p>
<p class="copy">{COPY_NOTE}</p>
</main></div>
</body></html>
'''
