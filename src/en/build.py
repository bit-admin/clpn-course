# -*- coding: utf-8 -*-
"""Build en/index.html (English syllabus) and en/llm.md (English site map for LLMs)."""
import html, json, os, re
SRC = os.path.dirname(os.path.abspath(__file__))
LANG = "en" if os.path.basename(SRC) == "en" else "zh"
REPO = os.path.dirname(os.path.dirname(SRC)) if LANG == "en" else os.path.dirname(SRC)
ROOT = REPO + "/en" if LANG == "en" else REPO
D = SRC + "/"
g = {}
for f in ["data1", "data2", "data3", "data4"]:
    exec(open(D + f + ".py", encoding="utf-8").read(), g)
MODULES, PACING, REFS = g["MODULES"], g["PACING"], g["REFS"]
sg = {}
exec(open(D + "common/shell.py", encoding="utf-8").read(), sg)
COPY_NOTE = sg["COPY_NOTE"]
_con_pair = sg["_con_pair"]
_short_title = sg["_short_title"]
E = html.escape
lessons_all = [(m, l) for m in MODULES for l in m["lessons"]]
ids = {l["id"] for _, l in lessons_all}
for _, l in lessons_all:
    for p in l["pre"]: assert p in ids, (l["id"], p)
n_lessons = len(lessons_all)
core = [(m, l) for m, l in lessons_all if not l.get("opt")]
total_min = sum(l["time"] for _, l in core)
sessions = sum(l.get("sessions", 1) for _, l in core)
fillC, COURSE_SIZE, N_WEEKS = g["fillC"], g["COURSE_SIZE"], g["N_WEEKS"]
def anchor(i): return "L" + i.replace(".", "-")
def ft(m):
    h, mm = divmod(m, 60)
    return ((f"{h} hr" if h else "") + (f" {mm} min" if mm else "")).strip()
def pre_html(pre):
    return '<span class="muted">None (entry lesson)</span>' if not pre else " ".join(f'<a class="chip" href="#{anchor(p)}">{p}</a>' for p in pre)

mods = []
for m in MODULES:
    mins = sum(l["time"] for l in m["lessons"] if not l.get("opt")); opt_mins = sum(l["time"] for l in m["lessons"] if l.get("opt")); out = []
    for l in m["lessons"]:
        s = l.get("sessions", 1)
        con_items = []
        for a, b in l["con"]:
            main_t, sub_t = _con_pair(a, b)
            con_items.append(f'<li><b>{E(main_t)}</b>' + (f'<span class="en">{E(sub_t)}</span>' if sub_t else '') + '</li>')
        con = "".join(con_items)
        math = f'<div class="math"><span class="tag">Essential Math</span>{E(l["math"])}</div>' if l.get("math") else ""
        code = f'<details class="code"><summary>R Code Preview (illustrative)</summary><pre><code>{E(l["code"])}</code></pre></details>' if l.get("code") else ""
        out.append(f'''<details class="lesson" id="{anchor(l["id"])}">
 <summary><label class="done"><input type="checkbox" data-lid="{l["id"]}" aria-label="Mark Lesson {l["id"]} complete"><span></span></label>
  <span class="lid">{l["id"]}</span><span class="ltitle">{E(l["title"])}</span>
  <span class="meta">{"Optional · " if l.get("opt") else ""}{ft(l["time"])}{f" · {s} sessions" if s>1 else ""}</span></summary>
 <div class="lbody">
  <div class="lmeta"><div class="row"><div class="kv"><span class="k">Estimated Time</span>Reading {ft(l["time"])}{f" ({s} sessions)" if s>1 else ""} + exercises ~{ft(max(45, l["time"]//2+30))}</div>
   <div class="kv"><span class="k">Prerequisites</span>{pre_html(l["pre"])}</div></div>
   {('<a class="enter" href="lessons/'+anchor(l["id"])+'.html">Open '+l["id"]+'</a>') if os.path.exists(os.path.join(ROOT,'lessons',anchor(l["id"])+'.html')) else '<span class="muted">Coming soon</span>'}</div>
  <h4>Learning Objectives</h4><ol>{"".join(f"<li>{E(o)}</li>" for o in l["obj"])}</ol>
  <h4>Core Concepts</h4><ul class="concepts">{con}</ul>
  {math}
  <h4>Hands-On Exercise</h4><p class="ex">{E(l["ex"])}</p>
  {code}
  <h4>Self-Check Questions</h4><ol>{"".join(f"<li>{E(c)}</li>" for c in l["chk"])}</ol>
 </div></details>''')
    mods.append(f'''<section class="module" id="{m["id"]}" style="--c:{m["color"]}">
 <header class="mhead"><div class="mnum">Module {m["id"][1:]}</div>
  <h2>{E(m["title"])}</h2><p>{E(m["intro"])}</p>
  <div class="mstats"><span>{len(m["lessons"])} lessons{" (incl. " + str(sum(1 for l in m["lessons"] if l.get("opt"))) + " optional)" if any(l.get("opt") for l in m["lessons"]) else ""}</span><span>~{round(mins/60,1)} hrs{f" (+ ~{round(opt_mins/60,1)} hrs optional)" if opt_mins else ""}</span><span class="mprog" data-mod="{m["id"]}"><i></i><b>0%</b></span></div>
 </header>
 {"".join(out)}
</section>''')

nav = "".join(f'<li class="navmod" style="--c:{m["color"]}"><a href="#{m["id"]}" class="navm">{m["id"][1:]}&nbsp; {E(m["title"])}</a><ul>' +
              "".join(f'<li><a href="#{anchor(l["id"])}" data-nav="{l["id"]}"><span>{l["id"]}</span>{E(l["title"])}{" (optional)" if l.get("opt") else ""}</a></li>' for l in m["lessons"]) + "</ul></li>" for m in MODULES)
flow = ' <em>→</em> '.join(f'<a href="#{m["id"]}" style="--c:{m["color"]}">{m["id"]} {E(_short_title(m["title"]))}</a>' for m in MODULES)
def mod_counts(m):
    core_l = [l for l in m["lessons"] if not l.get("opt")]
    n_opt = len(m["lessons"]) - len(core_l)
    return f'{len(core_l)}{f" + {n_opt} optional" if n_opt else ""}', round(sum(l["time"] for l in core_l) / 60, 1)
modsum = "".join(f'<tr><td><a href="#{m["id"]}">{m["id"]}</a></td><td>{E(m["title"])}</td><td>{mod_counts(m)[0]}</td><td>{mod_counts(m)[1]}</td></tr>' for m in MODULES)
pace = "".join(f'<tr><td>Week {w}</td><td>{E(a)}</td><td>{E(b)}</td></tr>' for w, a, b in PACING)
refs = ""
for sec, items in REFS:
    lis = ""
    for r in items:
        link = f' <a href="{r["url"]}" target="_blank" rel="noopener">{E(r["url"].replace("https://",""))}</a>' if r["url"] else ""
        lis += f'<li><div class="cite">{r["c"]}{link}</div><div class="rnote">{E(r["note"])}</div></li>'
    refs += f'<h3>{E(sec)}</h3><ul class="refs">{lis}</ul>'
seen = {}
for _, l in lessons_all:
    for z, e in l["con"]:
        main_t, sub_t = _con_pair(z, e)
        seen.setdefault(z, (main_t, e, l["id"]))
gloss = "".join(f'<tr><td>{E(main_t)}</td><td><a href="#{anchor(i)}">{i}</a></td></tr>' for z, (main_t, e, i) in seen.items())
modmap = {m["id"]: [l["id"] for l in m["lessons"]] for m in MODULES}

tpl = open(D + "template.html", encoding="utf-8").read()
rep = {"__CSS__": open(REPO + "/src/style.css", encoding="utf-8").read(),
       "__JS__": open(D + "app.js", encoding="utf-8").read().replace("__MODS__", json.dumps(modmap)).replace("__TOTAL__", str(n_lessons)),
       "__NAV__": nav, "__MODULES__": "".join(mods), "__NMOD__": str(len(MODULES)), "__NLES__": str(n_lessons),
       "__HOURS__": str(round(total_min/60)), "__SESS__": str(sessions), "__MODSUM__": modsum, "__FLOW__": flow,
       "__PACE__": pace, "__REFS__": refs, "__GLOSS__": gloss, "__COPYRIGHT__": COPY_NOTE}
for k, v in rep.items(): tpl = tpl.replace(k, v)
tpl = fillC(tpl)
open(ROOT + "/index.html", "w", encoding="utf-8").write(tpl)

def md_cell(s):
    return s.replace("|", "\\|").replace("\n", " ")

lines = ["# CLPN From Scratch · Course Map", "",
         f"Self-paced English course on Cross-Lagged Panel Network (CLPN) analysis: {len(MODULES)} modules, {COURSE_SIZE}, ~{round(total_min/60)} hours of core lesson reading (plus hands-on exercises), scheduled over {N_WEEKS} weeks. Assumed background: introductory calculus, no prior R experience required. The primary panel dataset is simulated and contains no personal data.",
         "",
         "© 2026 ZHANG. Course content (text, lessons, materials, figures, data and data documentation) licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); "
         "code (R scripts, data/simulate_data.R, website JavaScript/CSS, build and test scripts) under the MIT License (https://opensource.org/license/mit). See LICENSE. Source: https://github.com/bit-admin/clpn-course",
         "",
         "This file is a machine-readable directory for agents/LLMs. Each lesson's full text lives in its own Markdown file. Use the map below to decide which lesson to read, then fetch only the relevant file rather than loading all lessons at once.",
         "",
         "Lesson IDs map to filenames by replacing `.` with `-`: Lesson 1.1 is `lessons/L1-1.md`. All relative links below resolve from this folder (`en/`).",
         "",
         "## Site Map",
         "",
         "| Path | Contents |",
         "| --- | --- |",
         "| [index.html](index.html) | Human-readable course syllabus |",
         f"| [START_HERE.html](START_HERE.html) | Study Guide: how to navigate the course, {N_WEEKS}-week schedule, how to study each lesson |",
         "| [START_HERE.md](START_HERE.md) | Markdown version of the Study Guide (generated from the same source as START_HERE.html) |",
         "| [materials/glossary.html](materials/glossary.html) | Glossary of core terms |",
         "| [materials/cheatsheets.html](materials/cheatsheets.html) | Cheat sheets: R basics, regression, CLPN pipeline, reporting checklist |",
         "| [materials/formulas.html](materials/formulas.html) | Formula reference |",
         "| [materials/faq.html](materials/faq.html) | Frequently asked questions (FAQ) |",
         "| [materials/study_log.html](materials/study_log.html) | Study log (fill in directly in your browser) |",
         "| [materials/writing.html](materials/writing.html) | Writing workshop: before/after examples and rewrite tasks for Methods, Results, and Limitations |",
         "| [materials/reading.html](materials/reading.html) | Paper reading pack: curated papers with DOI links and guided reading questions |",
         "| [materials/case_elsoc.html](materials/case_elsoc.html) | Real-data case: CLPN of depressive symptoms in ELSOC (`data/elsoc_phq8_wide.csv`, CC0) |",
         "| [materials/assessment.html](materials/assessment.html) | Assessments hub: pre-test, module quizzes, and final exam (instructions & rubrics) |",
         "| [downloads/index.html](downloads/index.html) | Download the complete course package (offline site, data, R scripts, exercise solutions) |",
         "| [data/data_dictionary.md](data/data_dictionary.md) | Data dictionary for the simulated panel and public datasets |",
         "| [R/README.md](R/README.md) | Installing R/RStudio, running scripts, and execution order |",
         "| `lessons/L*.md` | Plain-text reading version of each lesson |",
         "| `R/L*.R` | Companion R scripts for each lesson |",
         "",
         "In the `.md` reading files, interactive widgets are noted by title and quiz questions mark the correct option.",
         "",
         "## Download",
         "",
         "The complete English course is packaged as [../downloads/clpn-course-en.zip](../downloads/clpn-course-en.zip) (see the [Download page](downloads/index.html)), which extracts to `clpn-course-en/` containing:",
         "",
         "| Path | Contents |",
         "| --- | --- |",
         "| `README.md` | Learner guide for the unpacked folder: where to start and how to run R |",
         "| `index.html`, `START_HERE.html`, `lessons/*.html`, `materials/` | Complete offline edition of the website—double-click `index.html` to browse without internet |",
         "| `data/` | Simulated panel data, data dictionary, `simulate_data.R`, true coefficient matrices; `coaches_mhc_raw.csv` (CC0) for Lesson 7.6; ELSOC original `.RData` and preprocessed `elsoc_phq8_wide.csv` (CC0) |",
         "| `R/` | Lesson R scripts, `_setup.R`, `run_all.R`, `assess_answers.R`, `data_elsoc.R`, `case_elsoc.R`, `R/README.md`, `R/solutions/` exercise solutions, and `R/output/` reference outputs |",
         "| `clpn-course.Rproj`, `LICENSE`, `THIRD_PARTY_NOTICES.md` | RStudio project file and license notices (content CC BY 4.0, code MIT) |",
         "",
         "Double-click `clpn-course.Rproj` to open the project in RStudio. For script dependencies (e.g., 4.3 → 10.1 → 10.2 → 10.3), see [R/README.md](R/README.md).",
         "",
         "## Suggested Pacing",
         "",
         "| Week | Lessons | Focus |",
         "| --- | --- | --- |"]
lines += [f"| Week {w} | {md_cell(a)} | {md_cell(b)} |" for w, a, b in PACING]
lines += ["", "## Modules & Lessons", ""]
for m in MODULES:
    lines.append(f"### {m['id']} {m['title']}")
    lines.append("")
    lines.append(m["intro"])
    lines.append("")
    for l in m["lessons"]:
        pre = ", ".join(l["pre"]) if l["pre"] else "None"
        objs = "; ".join(l["obj"])
        lines.append(f"- [{l['id']} {l['title']}](lessons/{anchor(l['id'])}.md){' (optional advanced)' if l.get('opt') else ''}. Prerequisites: {pre}. Objectives: {objs}")
    lines.append("")
open(ROOT + "/llm.md", "w", encoding="utf-8").write(fillC("\n".join(lines)).rstrip() + "\n")
print("EN build.py:", len(MODULES), n_lessons, sessions, total_min/60, len(seen), len(tpl))
