# -*- coding: utf-8 -*-
"""Generate study material pages materials/*.html, root study guide START_HERE.html (and START_HERE.md generated from it), and materials/study_log.md.
Shares lessons/assets/course.css, lesson.js, and local KaTeX with lesson pages. Works offline and is printable.
Run: python3 src/en/build_materials.py"""
import html, importlib.util, os, re
SRC = os.path.dirname(os.path.abspath(__file__))   # Source directory: src/ (English mirror is src/en/)
LANG = "en" if os.path.basename(SRC) == "en" else "zh"
REPO = os.path.dirname(os.path.dirname(SRC)) if LANG == "en" else os.path.dirname(SRC)
ROOT = REPO + "/en" if LANG == "en" else REPO       # Site root: repo root for zh, en/ for English
D = ROOT + "/"
g = {}
for f in ["data1", "data2", "data3", "data4"]:
    exec(open(SRC + "/" + f + ".py", encoding="utf-8").read(), g)
exec(open(SRC + "/common/shell.py", encoding="utf-8").read(), g)
exec(open(SRC + "/materials/glossary_defs.py", encoding="utf-8").read(), g)
MODULES, PACING, DEFS, course_nav, COPY_NOTE = g["MODULES"], g["PACING"], g["DEFS"], g["course_nav"], g["COPY_NOTE"]
_con_pair = g["_con_pair"]
fillC = g["fillC"]
E = html.escape
anchor = lambda i: "L" + i.replace(".", "-")
LES = {l["id"]: (m, l) for m in MODULES for l in m["lessons"]}
def L(i, txt=None): return f'<a href="../lessons/{anchor(i)}.html">{txt or (i + " " + E(LES[i][1]["title"]))}</a>'
def Ls(*ids): return ", ".join(L(i, i) for i in ids)
os.makedirs(D + "materials", exist_ok=True)
os.makedirs(D + "downloads", exist_ok=True)

PAGES = [("START_HERE.html", "Study Guide"), ("materials/glossary.html", "Glossary"), ("materials/cheatsheets.html", "Cheat Sheets"),
         ("materials/formulas.html", "Formula Reference"), ("materials/faq.html", "FAQ"), ("materials/study_log.html", "Study Log"), ("materials/writing.html", "Writing Workshop"), ("materials/reading.html", "Paper Reading Pack"), ("materials/case_elsoc.html", "Real-Data Case (ELSOC)"), ("materials/assessment.html", "Assessments"),
         ("downloads/index.html", "Download")]

def page(fname, title, lead, body, math=False, rel=None):
    if rel is None:
        rel = fname if "/" in fname else "materials/" + fname
    dest_dir = os.path.dirname(rel)
    def href(target):
        return os.path.relpath(target, dest_dir or ".").replace(os.sep, "/")
    nav = "".join(f'<li><a href="{href(f)}"' + (' class="cur" aria-current="page"' if f == rel else "") + f'>{t}</a></li>' for f, t in PAGES)
    assets = href("lessons/assets")
    kt = (f'<link rel="stylesheet" href="{assets}/vendor/katex/katex.min.css">\n'
          f'<script defer src="{assets}/vendor/katex/katex.min.js"></script>\n'
          f'<script defer src="{assets}/vendor/katex/contrib/auto-render.min.js"></script>\n') if math else ""
    html_ = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} · CLPN From Scratch</title>
<link rel="stylesheet" href="{assets}/vendor/fonts/fonts.css">
{kt}<link rel="stylesheet" href="{assets}/course.css">
<script defer src="{assets}/lesson.js"></script>
<script>addEventListener("beforeprint",function(){{document.querySelectorAll("details.faq").forEach(function(d){{d.open=true}})}});</script>
</head>
<body class="matpage" style="--c:#003262">
<div class="progressline"></div>
<div class="topbar"><button id="tocBtn" type="button" aria-label="Open table of contents">Contents</button><a class="home" href="{href("index.html")}#materials">CLPN Syllabus</a><span class="crumb">Study Materials / {E(title)}</span><span class="sp"></span>
<a class="act langSwitch" href="{href("../" + rel)}">中文</a><button id="printBtn" type="button" onclick="window.print()">Print</button><button id="themeBtn" type="button" aria-label="Toggle dark mode">Dark</button></div>
<div class="wrap">
<nav class="toc" aria-label="Table of contents"><div class="toc-local"></div>{course_nav(MODULES, None, base=href("lessons") + "/", mat=href("."), docs=False)}<div class="allnav"><b>Study Materials</b><ul class="matnav">{nav}</ul></div></nav>
<main>
<header class="lhero"><div class="mnum">Study Materials</div><h1>{E(title)}</h1><div class="lead">{lead}</div></header>
{body}
<p class="foot">CLPN From Scratch · <a href="{href("index.html")}#materials">Back to Syllabus</a></p>
<p class="copy">{COPY_NOTE}</p>
</main></div>
</body></html>
'''
    open(os.path.join(D, rel), "w", encoding="utf-8").write(fillC(html_))

def sec(id_, h, body, cls=""): return f'<section class="sec {cls}" id="{id_}"><h2>{h}</h2>{body}</section>'


# Running R locally: shared description between downloads page and study guide (pre = relative prefix from page to site root)
def local_setup(pre):
    return f"""
<h3>1. Download and Extract</h3>
<p>Get <code>clpn-course-en.zip</code> from the <a href="{pre}downloads/index.html">Download page</a> and extract it (Windows: right-click → "Extract All…"; Mac: double-click). You get a folder <code>clpn-course-en/</code> with everything you need to study and run R:</p>
<div class="codeblk"><pre class="out"><code>clpn-course-en/
├── index.html             ← Offline course website: double-click to open in a browser, no internet needed
├── README.md              ← Folder guide (read this first)
├── START_HERE.html        ← Study guide
├── lessons/, materials/   ← Lesson pages and study materials
├── clpn-course.Rproj      ← Double-click to open the course project in RStudio
├── LICENSE, THIRD_PARTY_NOTICES.md
├── data/                  ← Simulated data, data dictionary, simulate_data.R, true_B_*.csv; real data coaches_mhc_raw.csv for the Lesson 7.6 exercise
└── R/
    ├── README.md / .html  ← R code user guide
    ├── _setup.R, run_all.R
    ├── L0-2.R, L1-1.R … L10-3.R, L2-6_report.Rmd, assess_answers.R
    ├── data_elsoc.R, case_elsoc.R   ← Real-data case (preprocessing, CLPN)
    ├── solutions/         ← Exercise solutions
    └── output/            ← Reference results (the figures and logs shown on the site); running the scripts overwrites them with your results</code></pre></div>
<p>Extract the archive first; do not open files from inside the zip preview window. Keep spaces and non-ASCII characters out of the path (for example, put the folder at <code>D:\\clpn-course-en</code>). If you clone the repository from GitHub, the <code>en/</code> folder has the same layout.</p>
<h3>2. Open the Project</h3>
<ol>
<li>Follow the <a href="{pre}R/README.html">R Code User Guide</a> to install R and RStudio (install R first, then RStudio).</li>
<li>Double-click <code>clpn-course-en/clpn-course.Rproj</code>. RStudio opens it as a project, and the working directory is the <code>clpn-course-en</code> folder. The first line of every script, <code>source("R/_setup.R")</code>, depends on this, so do not open <code>.R</code> files by double-clicking them.</li>
<li>Open <code>R/L2-4.R</code> and click Source to install the packages the course needs (only once).</li>
<li>Open <code>R/L1-1.R</code> and run it line by line (Ctrl/Cmd + Enter) to check that you see output. After that, open the matching <code>R/Lx-y.R</code> for each lesson (Lessons 0.1 and 9.1 have no script).</li>
</ol>
<h3>3. Run Order and Dependencies</h3>
<p>Run the scripts in lesson order. The scripts below read files that earlier scripts write to <code>R/output/</code>. The bundled <code>R/output/</code> already holds reference results, so these scripts also run on their own. If you change and rerun an earlier script, the later scripts use your new results. If a file they need is missing (for example, because you deleted <code>R/output/</code>), the script stops at the start and tells you which script to run first.</p>
<div class="tablewrap"><table><tr><th>Script</th><th>Run first</th></tr>
<tr><td><code>L6-5.R</code>, <code>solutions/L6-4_solution.R</code>, <code>solutions/L6-5_solution.R</code></td><td><code>L6-4.R</code></td></tr>
<tr><td><code>L10-1.R</code> → <code>L10-2.R</code> → <code>L10-3.R</code></td><td>In order: <code>L4-3.R</code> → <code>L10-1.R</code> → <code>L10-2.R</code> → <code>L10-3.R</code> (each step needs the results of the one before)</td></tr>
<tr><td><code>solutions/L8-3_solution.R</code></td><td><code>L8-2.R</code> (reads <code>L8-2_boot.rds</code>) and <code>L8-3.R</code></td></tr>
<tr><td><code>case_elsoc.R</code></td><td>The bundled <code>data/elsoc_phq8_wide.csv</code> (written by <code>data_elsoc.R</code> from the bundled original file)</td></tr>
<tr><td>All other scripts</td><td>None</td></tr>
</table></div>
<p><b>Run everything at once</b>: <code>source("R/run_all.R")</code>. It runs all lesson scripts and the final-exam answer script in lesson order, then all solution scripts (<code>R/solutions/</code>). This takes about 40–95 minutes, depending on your computer; most of the time goes to the bootstraps in L8-2, L8-3, and L10-2. A summary is written to <code>R/output/run_all_status.csv</code>. It also runs <code>data_elsoc.R</code> and <code>case_elsoc.R</code> for the real-data case.</p>
<p>The bootstrap runs on a <b>single core</b> by default (<code>nCores = 1</code>) with a fixed seed. With the same R and package versions, the results are bitwise reproducible and match the numbers on the site. Running in parallel is several times faster, but the results are no longer reproducible: interval endpoints usually change only in the second or third decimal place, but a CS-coefficient can jump a whole grid step (in the course data, in-EI moves between 0.44 and 0.52, right across the 0.5 reference line).</p>"""

# =====================================================================  Study Guide
hours = round(sum(l["time"] for m in MODULES for l in m["lessons"] if not l.get("opt")) / 60)   # Core lessons only, consistent with index.html and llm.md (optional lessons opt=True excluded)
modrows = "".join(f'<tr><td><b>{m["id"]}</b></td><td>{E(m.get("en") or m["title"])}</td><td>{len(m["lessons"])}</td><td>{" ".join(L(l["id"], l["id"]) for l in m["lessons"])}</td></tr>' for m in MODULES)
pace = "".join(f'<tr><td>Week {w}</td><td>{E(a)}</td><td>{E(b)}</td></tr>' for w, a, b in PACING)
guide = sec("site", "1. What Is on This Website", r"""
<p>You study this course in your browser. The table below lists the pages on this site. You can download the whole site, with the data, R scripts, and exercise solutions, as one package: get <code>clpn-course-en.zip</code> from the <a href="downloads/index.html">Download page</a>, extract it to the <code>clpn-course-en/</code> folder, and double-click <code>index.html</code> to study offline. For running R, see Section 5.</p>
<div class="tablewrap"><table><tr><th>Page</th><th>What It Is</th><th>When to Use It</th></tr>
<tr><td><a href="index.html">Course Syllabus</a></td><td>11 modules; objectives, concepts, and exercises for every lesson, with progress checkboxes</td><td>Start every study session here</td></tr>
<tr><td>Lesson Pages</td><td>{{C:size}}, all interactive (Intuition → Essential Math → R Code → Concept Check → Exercises → Summary). Open them from links such as "Start 1.1" on the syllabus</td><td>The main content of each lesson</td></tr>
<tr><td>Study Materials</td><td>This guide, <a href="materials/glossary.html">Glossary</a>, <a href="materials/cheatsheets.html">Cheat Sheets</a>, <a href="materials/formulas.html">Formula Reference</a>, <a href="materials/faq.html">FAQ</a>, <a href="materials/study_log.html">Study Log</a></td><td>Any time you need to look something up</td></tr>
<tr><td><a href="downloads/index.html">Download</a></td><td>The whole course in one zip: offline website, data, R scripts, and exercise solutions</td><td>When you want to study offline or run R on your own computer</td></tr>
<tr><td><a href="materials/writing.html">Writing Workshop</a>, <a href="materials/reading.html">Paper Reading Pack</a></td><td>Before-and-after rewrites of methods, results, and limitations; selected papers with reading questions</td><td>During Lessons 9.3 and 10.3; when you write up your capstone project</td></tr>
<tr><td><a href="materials/case_elsoc.html">Real-Data Case (ELSOC)</a></td><td>A CLPN of depressive symptoms (PHQ-8) in ELSOC. The analysis files come with the course</td><td>After Lessons 7.4 and 8.2; as a model for your capstone project</td></tr>
<tr><td><a href="materials/assessment.html">Assessments</a></td><td>Pre-test, a quiz for each module, and the final exam, with scoring rubrics</td><td>Before you start, after each module, and after Lesson 10.3</td></tr>
<tr><td><a href="R/README.html">R Code User Guide</a></td><td>Installing R and RStudio, opening the project, running scripts</td><td>When you reach the R code</td></tr>
<tr><td><a href="data/data_dictionary.html">Data Dictionary</a></td><td>What each variable means in the simulated N = 800, three-wave loneliness–depression data</td><td>While you do the exercises</td></tr>
</table></div>
<p>Progress ("Mark lesson complete") is saved in your browser. You lose it if you switch browsers or clear the cache, so keep important notes in your Study Log.</p>""")
guide += sec("order", "2. What Order to Follow", r"""
<p>The module numbers follow the logical order of the material: M0 Overview → M1 Statistics Foundations → M2 R Programming → M3 Regression & Regularization → M4 Longitudinal Data → M5 CLPM → M6 Network Psychometrics → M7 CLPN → M8 Stability → M9 Critical Reading & Reporting → M10 Capstone Mini-Project. In practice, <b>study M1 (statistics) and M2 (R) side by side, alternating in Weeks 2–5, and take M3 (regression) after both</b>: as soon as you learn a statistical idea, try it in R. Each lesson page lists its prerequisites at the top as links.</p>
<div class="tablewrap"><table><tr><th>Module</th><th>Topic</th><th>Lessons</th><th>Lesson List</th></tr>""" + modrows + r"""</table></div>""")
guide += sec("lesson", "3. How to Study Each Lesson (~2–3 Hours)", r"""
<ol><li><b>Read the objectives (2 min):</b> Read "Learning Objectives" and "Core Concepts". Look up unfamiliar terms in the <a href="materials/glossary.html">Glossary</a> first.</li>
<li><b>① Intuition (20–30 min):</b> Do not skip it. Form a picture in your head before you look at equations, and drag the interactive widgets yourself.</li>
<li><b>② Essential Math (15–30 min):</b> Work through the worked example with pen and paper. All formulas are collected in the <a href="materials/formulas.html">Formula Reference</a>.</li>
<li><b>③ R Code (30–60 min):</b> Double-click <code>clpn-course.Rproj</code> to open the RStudio project, open the matching <code>R/Lx-y.R</code>, and <b>run it line by line</b> (Ctrl/Cmd + Enter). Compare your output with the output on the page. You can expand the full script at the bottom of the page.</li>
<li><b>④ Concept Check (10 min):</b> A wrong answer first gets a hint; the answer appears only after two wrong tries.</li>
<li><b>⑤ Exercises (1–2 hours):</b> Do them yourself before you look at the solutions. Solutions to coding exercises are in <code>R/solutions/</code>. For writing exercises, check your draft point by point against the rubric in the lesson and revise it once before you save it. Keep each lesson's exercise scripts and output in one folder; you will use them again in the capstone project.</li>
<li><b>Summary and log (10 min):</b> Click "Mark lesson complete" and write three sentences in your <a href="materials/study_log.html">Study Log</a>: what you learned, what is still unclear, and what you want to work out next.</li></ol>
<div class="box key"><b class="bt">Stuck?</b><p>① Read "Common mistakes" and "Common questions and pitfalls" in the lesson. ② Check the <a href="materials/faq.html">FAQ</a>. ③ For an R error, paste the last line of the error message into a search engine. ④ If that does not help, write a minimal reproducible example as shown in """ + L("2.1", "Lesson 2.1") + r""" and ask classmates, colleagues, or an R forum (such as Posit Community or Stack Overflow). If you have been stuck for more than 30 minutes, try a different approach instead of grinding on. Writing the minimal example often shows you the cause.</p></div>""")
guide += sec("plan", "4. {{C:weeks}}-Week Study Plan", r"""
<p><b>Standard pace: {{C:weeks}} weeks, 3 sessions a week</b> (4 in Weeks 14 and 15), 60–150 minutes per session, plus 2–3 hours of exercises a week: about 5–7 hours a week in total. Reading the core lessons takes about """ + str(hours) + r""" hours (not counting optional lessons and exercises). If you study full-time during a break, you can compress this to about 12 weeks (4 sessions a week). If you study alongside other courses, you can stretch it to about 19 weeks (one buffer week after Weeks 5, 8, and 13). The optional advanced lessons {{C:optlist}} are not part of the standard pace: if you have time, study them on your own after Week 13. The relaxed pace puts them in the buffer week after Week 13; the compressed pace leaves them out.</p>
<div class="tablewrap"><table><tr><th>Week</th><th>Lessons</th><th>Focus</th></tr>""" + pace + r"""</table></div>
<p class="muted">At the end of each week, write a weekly summary in your Study Log, file the week's exercise scripts and output, and use the progress bar on the syllabus to check that you are on schedule.</p>""")
guide += sec("r", "5. Running R on Your Computer", local_setup(""))
guide += sec("progress", "6. Progress & Self-Assessment", r"""
<ul><li>Set aside 30 minutes each week for review. Reread the "What still feels unclear" column in your Study Log, cross off what you can now resolve yourself, and for anything left, write down exactly which step you are stuck on and carry it into the next week.</li>
<li>Save exercise results as scripts plus output (or a Quarto report), not just screenshots. You will need them to check your work weeks later or to reuse code in the capstone project.</li>
<li>For writing exercises (interpretation paragraphs, peer reviews, methods and results), write a draft first, then score it point by point against the rubric in the lesson and in the <a href="materials/writing.html">Writing Workshop</a>, and revise it once. If you can, swap drafts with a classmate or colleague and ask them to mark any sentence that reads like a causal conclusion.</li>
<li>Take the module quizzes in Weeks 5 and 8 (M1 + M2, M3 + M4). Weeks 15–16 are for the capstone project (""" + Ls("10.1", "10.2", "10.3") + r"""). Before the project starts, write a one-page analysis plan and save it with a date. If you change anything once the analysis is under way, list each change and the reason for it in the report.</li></ul>""")
guide += sec("assess", "7. Assessments: Pre-Test, Module Quizzes & Final Exam", r"""
<ul><li><b>Before you start</b>: Take the <a href="materials/assess_pre.html">pre-test</a> (about 20 min, not scored). It suggests whether to follow the {{C:weeks}}-week standard pace or the 19-week pace with a buffer week after Weeks 5, 8, and 13.</li>
<li><b>After each module</b>: Take that module's quiz (15–25 min). If you get 70% or more right on the first try, move on; if not, use the links in the explanations of the questions you missed to review.</li>
<li><b>After Lesson 10.3</b>: Take the final exam (about 90 min) and compare it with your pre-test to see how far you have come.</li>
<li>Record the number you got right on the first try in your <a href="materials/study_log.html">Study Log</a>. The scoring rubrics are on the <a href="materials/assessment.html">Assessments page</a>.</li></ul>""")
guide = guide.replace('href="../lessons/', 'href="lessons/')
page("START_HERE.html", "Study Guide: How to Use This Course", "<p>This page explains how to study with this website: what is on it, what order to follow, how to work through each lesson, and how to plan your {{C:weeks}} weeks. Markdown version: <a href=\"START_HERE.md\" download><code>START_HERE.md</code></a> (identical content).</p>", guide, rel="START_HERE.html")

# =====================================================================  Glossary
seen = {}
for m in MODULES:
    for l in m["lessons"]:
        for z, e in l["con"]:
            if z not in seen: seen[z] = (_con_pair(z, e)[0], l["id"], m)
gl = ""
for m in MODULES:
    rows = [(z, en_t, i) for z, (en_t, i, mm) in seen.items() if mm is m]
    if not rows: continue
    gl += sec("g-" + m["id"], f'{m["id"]} {E(m.get("en") or m["title"])}', '<div class="tablewrap"><table class="gloss"><tr><th>Term</th><th>One-Sentence Definition</th><th>Introduced In</th></tr>' +
              "".join(f'<tr><td><b>{E(en_t)}</b></td><td>{E(DEFS.get(z) or DEFS.get(en_t) or "")}</td><td>{L(i, i)}</td></tr>' for z, en_t, i in rows) + "</table></div>")
gsearch = '<div class="card glsearch"><label>Filter terms: <input id="glq" type="search" placeholder="e.g., partial correlation / bootstrap"></label> <span class="muted" id="gln"></span></div>' \
          '<script>document.addEventListener("DOMContentLoaded",function(){var q=document.getElementById("glq"),n=document.getElementById("gln");if(!q)return;q.addEventListener("input",function(){var v=q.value.trim().toLowerCase(),k=0;document.querySelectorAll("table.gloss tr").forEach(function(tr){if(!tr.querySelector("td"))return;var on=!v||tr.textContent.toLowerCase().indexOf(v)>=0;tr.style.display=on?"":"none";if(on)k++;});n.textContent=v?(k+" matches"):"";});});</script>'
page("glossary.html", "Glossary of Core Terms", f"<p>All {len(seen)} core terms across the course, grouped by module, with a one-sentence definition and a link to the lesson where each term is formally introduced. Navigation bars are automatically hidden when printing.</p>", gsearch + gl)

# =====================================================================  Cheat Sheets
def card(id_, title, body): return f'<section class="sec cheat" id="{id_}"><h2>{title}</h2>{body}</section>'
def tbl(head, rows): return '<div class="tablewrap"><table><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table></div>"
C = lambda s: f"<code>{E(s)}</code>"
cs = card("r", "Cheat Sheet 1 · R Fundamentals", tbl(["Goal", "Code", "Notes"], [
["Assignment / Inspection", C("x <- c(3, 5, 4); x"), "R is case-sensitive; quotes for strings"],
["Mean / SD / With missing data", C("mean(x); sd(x); mean(x, na.rm = TRUE)"), "sd() uses n − 1 denominator"],
["Read data / Inspect structure", C('dat <- read.csv("data/clpn_sim_wide.csv"); str(dat)'), "Paths relative to project root"],
["Dimensions / First rows / Summary", C("dim(dat); head(dat); summary(dat)"), "Health-check after import (Lesson 2.4)"],
["Select column / Subset rows", C('dat$age; dat[dat$gender == 1, ]'), "Use == for comparison, not ="],
["Count missing values", C("colSums(is.na(dat))"), "Never write x == NA"],
["Row sums (Total score)", C("rowSums(dat[, paste0(lone_items, \"_t1\")])"), "Do not use sum() inside mutate()"],
["dplyr pipeline", C("dat |> filter(age >= 60) |> group_by(gender) |> summarise(M = mean(age))"), "Remember to assign the result"],
["Wide → Long", C('pivot_longer(dat, cols = matches("^(lone|dep)\\\\d_t\\\\d$"), names_to = c(".value", "wave"), names_sep = "_t")'), "Reshapes only the 9 item columns; other columns like gender and age are retained. Rows = N × waves"],
["Correlation / Matrix", C("cor(x, y); round(cor(d), 2)"), "Missing: use = \"pairwise.complete.obs\""],
["Regression / Output / CIs", C("fit <- lm(y ~ x1 + x2, data = d); summary(fit); confint(fit)"), "Logistic regression: glm(..., family = binomial)"],
["Standardization", C("scale(x)[, 1]"), "scale() returns a matrix"],
["Plotting", C("ggplot(d, aes(x, y)) + geom_point()"), "+ goes at the end of the line"],
["Save plot", C('ggsave("R/output/fig.png", width = 12, height = 9, units = "cm", dpi = 300)'), ""],
["Random seed / Session info", C("set.seed(2026); sessionInfo()"), "Include in your methods section"],
["Help", C("?cor; example(cor)"), "Check Usage and Examples first"]]) +
'<p class="muted">Three most common errors: <b>object not found</b> (not created or misspelled) · <b>could not find function</b> (misspelled or library not loaded) · <b>unexpected symbol / input</b> (punctuation, unmatched brackets/quotes). See ' + L("2.1", "Lesson 2.1") + '.</p>')
cs += card("reg", "Cheat Sheet 2 · Reading Regression Output", tbl(["Output Term", "Meaning", "How to Report"], [
["Estimate (b)", "Holding other predictors constant, for each 1-unit increase in x, y changes by b on average", "b = 0.32"],
["Std.all / β", "Standardized coefficient: for a 1 SD increase in x, y changes by β SD on average", "β = .25 (APA style: omit leading zero for statistics bounded by 1)"],
["Std. Error", "Sampling uncertainty of b", "Typically reported in tables"],
["t value = b / SE", "Distance from 0 in units of standard error", "t(797) = 7.82"],
["Pr(>|t|)", "Probability of observing a result as extreme as or more extreme than observed, assuming null b = 0 is true", "p &lt; .001 (never write p = 0)"],
["confint()", "95% confidence interval; excludes 0 ⇔ p &lt; .05", "95% CI [0.24, 0.40]"],
["R² / Adjusted R²", "Proportion of variance in the outcome explained by the model", "R² = .10"],
["glm Estimate", "Log-odds; exp() yields the odds ratio (OR)", "OR = 1.65, 95% CI [...]"],
["OR", "For a 1-unit increase in x, odds are multiplied by OR (not probability)", "Odds increase by (OR − 1) × 100%"]]) +
'<div class="box key"><b class="bt">One-Sentence Template</b><p>"After controlling for <u>covariates</u>, <u>predictor</u> positively/negatively predicted <u>outcome</u> (b = __, 95% CI [__, __], p = __); the model explained __% of the variance in <u>outcome</u>."</p></div>' +
'<div class="box warnbox"><b class="bt">Five Pitfalls to Avoid</b><ul><li>Describing b in causal terms ("leads to", "drives", "causes").</li><li>Writing p &gt; .05 as "there is no relationship".</li><li>Comparing β across different samples.</li><li>Treating significant correlation but non-significant regression as contradictory—it is the expected result of "controlling" (' + L("2.5", "Lesson 2.5") + ').</li><li>Confusing odds ratios with risk ratios.</li></ul></div>')
cs += card("pipe", "Cheat Sheet 3 · CLPN Analysis Workflow", tbl(["Step", "What to Do", "Key Code / File", "Lesson"], [
["0 Plan", "Document research questions, nodes, λ selection rule, seed, and stability criteria in the analysis plan", C("R/output/L10-1_analysis_plan.md"), Ls("10.1")],
["1 Data", "Import, check ranges and missingness, attrition analysis; align T1 / T2 by ID", C("read.csv(); colSums(is.na())"), Ls("2.4", "4.2", "4.3")],
["2 Descriptives", "Mean, SD, skewness; item correlations", C("psych::describe()"), Ls("2.5")],
["3 Redundancy Check", "Identify items with high conceptual overlap", C("networktools::goldbricker()"), Ls("9.2")],
["4 Estimation", "Run nodewise LASSO regression for each T2 node; standardize items first, 10-fold CV", C("set.seed(2026); B <- clpn_estimate(X, Y, rule = \"lambda.min\")"), Ls("7.2")],
["5 Visualization", "Directed network graph; omit autoregressive edges or display as self-loops; fix maximum edge weight", C("qgraph(cl_only(B), directed = TRUE)"), Ls("7.3")],
["6 Centrality", "Out-EI, in-EI, bridge EI; exclude autoregressions", C("rowSums(cl_only(B)); colSums(cl_only(B))"), Ls("7.4")],
["7 Accuracy", "Non-parametric bootstrap for edge weight confidence intervals (B ≥ 1000)", C("bootnet(..., fun = custom_estimation_function)"), Ls("8.2")],
["8 Stability", "Case-dropping bootstrap; interpret centrality rankings only if CS ≥ 0.25", C("corStability()"), Ls("8.3")],
["9 Sensitivity", "lambda.1se, adjust for covariates, replicate across T2 → T3", C("clpn_estimate(..., covariates = )"), Ls("7.5", "9.2")],
["10 Reporting", "Detail every parameter setting in methods; ensure every number is traceable to output files", C("sessionInfo()"), Ls("9.3", "10.3")]]) +
'<div class="box story"><b class="bt">Three Bottom Lines</b><ul><li>CLPN edges represent <b>temporal prediction</b>, not causality.</li><li>Standard CLPN conflates between-person and within-person effects (' + L("5.3", "5.3") + ', ' + L("7.5", "7.5") + ').</li><li>Centrality rankings without stability evaluation must not be interpreted.</li></ul></div>')
cs += card("report", "Cheat Sheet 4 · Reporting Checklist", '<p class="muted">Based on ' + L("9.3", "Lesson 9.3") + ' (adapted from Burger et al., 2023 reporting standards for network analysis). Check item by item:</p><ul class="checklist">' + "".join(f"<li>[ ] {x}</li>" for x in [
"<b>Sample</b>: N, recruitment strategy, sample size and attrition rate across waves, attrition analysis results",
"<b>Design</b>: Number of waves, measurement lag interval, and rationale for choosing this interval",
"<b>Nodes</b>: Full item wording or abbreviations, source scales, rationale for node selection; redundancy check (goldbricker)",
"<b>Missing Data</b>: Handling method (listwise deletion / imputation / FIML) and justification",
"<b>Preprocessing</b>: Whether items were standardized; handling of ordinal response categories",
"<b>Estimation</b>: Software and versions (R, glmnet, bootnet); nodewise LASSO; λ rule (lambda.min / 1se); number of CV folds; random seed",
"<b>Covariates</b>: Which covariates were included and whether they were penalized (penalty.factor = 0)",
"<b>Centrality</b>: Metric names; whether autoregressions were excluded; community definitions for bridge centrality",
"<b>Accuracy</b>: Bootstrap type and number of resamples (B); edge weight CI plot",
"<b>Stability</b>: Case-dropping bootstrap resamples; CS-coefficient and evaluation criteria (0.7 / 95% / 0.25)",
"<b>Sensitivity Analyses</b>: Which analyses were performed; whether primary conclusions held",
"<b>Network Plots</b>: Figure caption detailing edge colors, thickness scaling (maximum), threshold, layout; how autoregressions are represented",
"<b>Tables</b>: Full B matrix (can be placed in supplementary materials); table of non-zero cross-lagged edges",
"<b>Language & Framing</b>: Use 'predicted' rather than 'caused' or 'drove'; avoid equating single items directly with broad constructs",
"<b>Limitations</b>: Conflation of between- and within-person effects, unmeasured confounding, time lag dependence, sample representativeness",
"<b>Open Science</b>: Code and (simulated or shareable) data availability; preregistration details (if applicable)"]) + "</ul>")
page("cheatsheets.html", "One-Page Cheat Sheets", "<p>Four cheat sheets: <a href=\"#r\">R Fundamentals</a> · <a href=\"#reg\">Reading Regression Output</a> · <a href=\"#pipe\">CLPN Analysis Workflow</a> · <a href=\"#report\">Reporting Checklist</a>. Each card prints on a separate page.</p>", cs)

# =====================================================================  Formula Reference
def F(name, tex, note, les): return f'<tr><td><b>{name}</b></td><td>\\(\\displaystyle {tex}\\)</td><td>{note}</td><td>{Ls(*les)}</td></tr>'
def ftab(rows): return '<div class="tablewrap"><table class="ftab"><tr><th>Name</th><th>Formula</th><th>Notes</th><th>Lesson</th></tr>' + "".join(rows) + "</table></div>"
fm = sec("f1", "Descriptive Statistics & Inference", ftab([
F("Mean", r"\bar x=\frac{1}{n}\sum_{i=1}^{n}x_i", "", ["1.2"]),
F("Sample Variance / SD", r"s^2=\frac{1}{n-1}\sum_{i}(x_i-\bar x)^2,\quad s=\sqrt{s^2}", "var(), sd() in R", ["1.2"]),
F("z-Score", r"z_i=\frac{x_i-\bar x}{s}", "Mean 0, SD 1", ["1.3"]),
F("Covariance", r"\operatorname{cov}(x,y)=\frac{1}{n-1}\sum_i(x_i-\bar x)(y_i-\bar y)", "", ["1.4"]),
F("Pearson Correlation", r"r=\frac{\operatorname{cov}(x,y)}{s_x s_y}", "−1 ≤ r ≤ 1", ["1.4"]),
F("Standard Error of the Mean", r"SE_{\bar x}=\frac{s}{\sqrt n}", "Quadrupling n halves SE", ["1.5"]),
F("95% Confidence Interval", r"\bar x\pm1.96\times SE", "Large-sample normal approximation", ["1.5"]),
F("Independent Samples t", r"t=\frac{\bar x_1-\bar x_2}{s_p\sqrt{1/n_1+1/n_2}}", "", ["1.6"]),
F("Cohen's d", r"d=\frac{\bar x_1-\bar x_2}{s_p}", "0.2 / 0.5 / 0.8 benchmarks", ["1.6"]),
F("Expected False Positives in Multiple Testing", r"E[\text{False Positives}]=m\times\alpha", "190 × 0.05 = 9.5", ["1.6"])]))
fm += sec("f2", "Regression & Regularization", ftab([
F("Simple Linear Regression", r"\hat y=b_0+b_1x,\quad b_1=\frac{\operatorname{cov}(x,y)}{s_x^2},\quad b_0=\bar y-b_1\bar x", "Ordinary least squares (OLS)", ["3.1"]),
F("Coefficient of Determination", r"R^2=1-\frac{\sum(y_i-\hat y_i)^2}{\sum(y_i-\bar y)^2}", "In simple regression, R² = r²", ["3.1"]),
F("Multiple Regression", r"y=b_0+b_1x_1+\dots+b_kx_k+e", "", ["3.2"]),
F("VIF", r"\mathrm{VIF}_j=\frac{1}{1-R_j^2}", "&gt; 5–10 indicates collinearity", ["3.2"]),
F("Standardized Coefficient", r"\beta=b\,\frac{s_x}{s_y}", "", ["3.3"]),
F("Logistic Regression", r"\operatorname{logit}(p)=\ln\frac{p}{1-p}=b_0+b_1x", r"\(p=1/(1+e^{-\text{logit}})\)", ["3.4"]),
F("Odds Ratio", r"\mathrm{OR}=e^{b_1}", "", ["3.4"]),
F("Ridge Regression", r"\min_b\ \frac{1}{2n}\sum_i(y_i-x_i^\top b)^2+\lambda\cdot\frac{1}{2}\sum_j b_j^2", "α = 0 in glmnet; ridge penalty includes 1/2 factor by glmnet convention", ["3.5"]),
F("LASSO", r"\min_b\ \frac{1}{2n}\sum_i(y_i-x_i^\top b)^2+\lambda\sum_j|b_j|", "α = 1 in glmnet", ["3.5", "7.2"]),
F("Soft Thresholding (Orthogonal Case)", r"\hat\beta_j=\operatorname{sign}(\hat\beta_j^{OLS})\max(|\hat\beta_j^{OLS}|-\lambda,0)", "", ["6.3"])]))
fm += sec("f3", "Longitudinal Models", ftab([
F("ICC", r"ICC=\frac{\sigma^2_{\text{between}}}{\sigma^2_{\text{between}}+\sigma^2_{\text{within}}}", "", ["4.1"]),
F("Rubin's Rules (Point Estimate)", r"\bar Q=\frac1m\sum_{l=1}^m\hat Q_l", "Multiple imputation", ["4.3"]),
F("Rubin's Rules (Total Variance)", r"T=\bar U+\left(1+\frac1m\right)B", "Within- + between-imputation variance", ["4.3"]),
F("CLPM", r"L_{t+1}=a_LL_t+c\,D_t+e,\quad D_{t+1}=a_DD_t+d\,L_t+e", "a: autoregressive, c, d: cross-lagged", ["5.1"]),
F("RI-CLPM Decomposition", r"x_{it}=\mu_t+RI_i+w_{it}", "Dynamic model specified on within-person components w", ["5.3"]),
F("Cross-Lagged Effect over Lag Δ", r"A=\begin{pmatrix}a&0\\c&a\end{pmatrix}\ \Rightarrow\ (A^{\Delta})_{21}=\Delta\,a^{\Delta-1}c", "Assuming identical autoregression a per unit time, unidirectional cross-lagged effect c (L → D), x<sub>t+1</sub> = A x<sub>t</sub>; rises then decays", ["5.4"])]))
fm += sec("f4", "Networks & CLPN", ftab([
F("Partial Correlation (3 Variables)", r"r_{xy\cdot z}=\frac{r_{xy}-r_{xz}r_{yz}}{\sqrt{(1-r_{xz}^2)(1-r_{yz}^2)}}", "", ["6.2"]),
F("Partial Correlation from Precision Matrix", r"K=\Sigma^{-1},\quad\rho_{ij}=-\frac{k_{ij}}{\sqrt{k_{ii}k_{jj}}}", "Note the negative sign", ["6.2"]),
F("Graphical LASSO", r"\max_K\ \log\det K-\operatorname{tr}(SK)-\lambda\sum_{i\ne j}|k_{ij}|", "", ["6.3"]),
F("EBIC (Graphical Model)", r"\mathrm{EBIC}=-2\ell+E\ln N+4\gamma E\ln p", "Used in EBICglasso: E = number of edges, p = number of nodes, typically γ = 0.5", ["6.3"]),
F("EBIC (Nodewise Regression)", r"\mathrm{EBIC}_j=N\ln(\mathrm{RSS}_j/N)+k_j\ln N+2\gamma k_j\ln p", "Used in <code>clpn_estimate(rule = \"ebic\")</code>: k<sub>j</sub> = number of non-zero coefficients in j-th regression, p = number of predictors", ["7.2", "9.2"]),
F("Strength / Expected Influence", r"S_i=\sum_{j}|w_{ij}|,\quad EI_i=\sum_j w_{ij}", "", ["6.5"]),
F("CLPN Nodewise Regression", r"z(y_{j,t+1})=\sum_{k=1}^{p}B_{kj}\,z(y_{k,t})+e_j", "B[k, j]: k → j", ["7.1", "7.2"]),
F("Out / In Expected Influence", r"\text{outEI}_k=\sum_{j\ne k}B_{kj},\quad\text{inEI}_j=\sum_{k\ne j}B_{kj}", "Total sums of out-EI and in-EI are equal", ["7.4"]),
F("Bridge Out-EI", r"\text{bridgeOutEI}_k=\sum_{j\notin C(k)}B_{kj}", "C(k): community containing node k", ["7.4"])]))
fm += sec("f5", "Bootstrap & Stability", ftab([
F("Percentile Bootstrap CI", r"[\hat\theta^*_{(0.025)},\ \hat\theta^*_{(0.975)}]", "B ≥ 1000", ["8.1"]),
F("Bootstrap Standard Error", r"SE^*=\operatorname{sd}(\hat\theta^*_1,\dots,\hat\theta^*_B)", "", ["8.1"]),
F("CI Width and Sample Size", r"\text{Width}\propto1/\sqrt N", "", ["8.1"]),
F("CS-Coefficient", r"CS=\max\{q:\ P(\operatorname{cor}(\hat c_{\text{orig}},\hat c_{\text{drop-}q})\ge0.7)\ge0.95\}", "≥ 0.25 interpretable, ≥ 0.5 preferred", ["8.3"])]))
page("formulas.html", "Formula Reference", "<p>All formulas used across the course compiled on a single page. Each formula notes the lesson where it is introduced; click to return to the lesson. Notation: n / N = sample size, p = number of nodes, λ = penalty parameter, B = CLPN coefficient matrix.</p>", fm, math=True)

# =====================================================================  FAQ
FAQ = [
("Study & Usage", [
("I have no prior background in statistics or programming. Can I really learn this?", "Yes. The course starts from the mean and 'what is a variable' (" + L("1.1", "1.1") + "), and R starts from installation (" + L("2.1", "2.1") + "). The key is following the lesson order, running the code yourself in every lesson, and maintaining 5–7 hours per week."),
("Do I have to follow the lessons in order?", "We strongly recommend following the <a href=\"../START_HERE.html#plan\">{{C:weeks}}-Week Plan</a>. Prerequisites are listed at the top of each lesson page; if you have already mastered certain content, you can take just the quiz, and skip the lesson if you answer every item correctly."),
("Why did my progress disappear?", "The 'completed' marks are saved in your browser's local storage. Switching browsers, using incognito mode, or clearing browser cache will erase them. Record important learning records in your <a href=\"study_log.html\">Study Log</a>."),
("Where are the exercise solutions?", "Each lesson has expandable reference solutions for its exercises. For exercises requiring code, full solutions are in <code>R/solutions/</code>, included in the course archive on the <a href=\"../downloads/index.html\">Download page</a>. Execution logs are in <code>R/output/sol_*_log.txt</code>.")]),
("R & Software", [
("What should I do if package installation throws an error?", "First check your internet connection, and configure a reliable CRAN mirror in RStudio (Tools → Global Options → Packages). Non-ASCII characters or spaces in Windows usernames or file paths often cause installation issues; we recommend placing the course in a simple path such as <code>D:\\clpn-course\\</code>. See the <a href=\"../R/README.html\">R Code User Guide</a> for details."),
("Why don't my numbers match the website exactly?", "Most scripts set a random seed, so results should match bit-for-bit. Bootstrap-related scripts (8.2, 8.3, 10.2) run on a single core by default; with a fixed seed, their results are also completely reproducible. If you set nCores greater than 1 (parallel processing), the seed does not govern child processes, and results will differ across runs. Edge weight confidence interval endpoints typically fluctuate only in the second or third decimal place, but the CS-coefficient does not vary continuously: it can only take values on the dropping-proportion grid (spaced by ~0.08), so it can jump by an entire step. In our course data, in-EI fluctuates between 0.44 and 0.52, landing once above and once below 0.5, changing the qualitative conclusion. For reported results, always run single-core with a fixed seed. In addition, minor differences can arise from different R or package versions."),
("Special characters or fonts display as boxes or garbled text?", "For plot labels: <code>_setup.R</code> attempts to set appropriate plot fonts; if issues persist, see common mistakes in " + L("2.6", "2.6") + ". For data encoding issues when reading CSV files, see " + L("2.4", "2.4") + "."),
("Should I use Quarto or R Markdown?", "Either works. Course examples use Quarto (<code>R/solutions/week06.qmd</code>); if Quarto is not installed, the same content can be adapted to an .Rmd file and rendered with rmarkdown."),
("What is in _setup.R?", "It locates the course root directory, configures output paths and plot fonts, defines item names, and loads utility functions (<code>clpn_estimate()</code>, <code>cl_only()</code>, <code>edge_list()</code>, etc.). It is well worth reading, but does not need modification.")]),
("Statistical Concepts", [
("What actually is a p-value?", "The probability of observing data as extreme as or more extreme than the observed data, assuming the null hypothesis is true. It is NOT the 'probability that the null hypothesis is true', nor does it measure effect size. See " + L("1.6", "1.6") + "."),
("The correlation is significant but the regression coefficient is not—is something wrong?", "No. A regression coefficient represents the 'unique' association after controlling for other predictors, which answers a fundamentally different question from bivariate correlation. Social support in the course dataset is a prime example (" + L("2.5", "2.5") + ")."),
("Why use LASSO instead of standard linear regression?", "With many nodes, standard OLS regression produces many small coefficients that are 'non-zero merely by chance' (overfitting, false positives). LASSO shrinks small coefficients exactly to zero, yielding a sparser, more interpretable network, at the cost of shrinkage bias in the retained coefficients. See " + L("3.5", "3.5") + " and " + L("6.3", "6.3") + "."),
("Should I choose lambda.min or lambda.1se?", "lambda.min minimizes cross-validation prediction error and retains more edges; lambda.1se is more conservative and produces a sparser network. Pre-specify one in your analysis plan as the primary analysis (this course uses lambda.min) and use the other as a sensitivity check. See " + L("7.2", "7.2") + "."),
("What is the difference between between-person and within-person effects?", "Between-person: whether individuals who are more lonely than others are also more depressed; within-person: when an individual is more lonely than their own usual level, are they subsequently more depressed. Standard CLPM and CLPN conflate these two levels. See " + L("4.1", "4.1") + " and " + L("5.3", "5.3") + ".")]),
("CLPN Methodology", [
("Do CLPN edges indicate causality?", "Not directly. Edges represent 'temporal prediction after controlling for all T1 nodes', which can be influenced by stable traits, unmeasured confounding, and the choice of measurement lag. In writing, use terms like 'predicted' or 'consistent with', and avoid causal claims like 'caused' or 'drove'. See " + L("5.4", "5.4") + "."),
("How large a sample size is required?", "There is no universally accepted rule of thumb such as 'N must be at least X times the number of nodes'. The ratio N/p (sample size divided by number of nodes) is only a crude heuristic: when it is small, each nodewise regression has little information, leading to sparser and less stable networks. With 9 nodes there are 81 coefficients; in the course data N/p = 800/9 ≈ 89. The actual sample size needed depends on the hypothesized true network (edge density and strength) and the specific research question, and should be evaluated via simulation: Constantin, Schuurman, and Vermunt (2026) provide a general Monte Carlo framework for sample size planning in network models, demonstrated in a simplified version in Lesson " + L("7.6", "7.6") + ". After data collection, evaluate stability using bootstrap and the CS-coefficient; see " + L("8.2", "8.2") + " and " + L("8.3", "8.3") + "."),
("Can I estimate a CLPN with only two waves of data?", "You can estimate a T1 → T2 network, but you cannot test replication across a subsequent lag interval, nor can you use RI-CLPM to separate stable traits (which requires at least 3 waves). State this clearly in your limitations section."),
("Is the node ranked highest in centrality the optimal intervention target?", "No. First confirm that CS ≥ 0.25 (preferably ≥ 0.5) and that the difference between the first and second ranked nodes is statistically significant via bootstrap testing. Even then, high centrality only reflects 'strong predictive associations'. Whether intervening on that node produces change requires experimental intervention studies. See " + L("6.5", "6.5") + " and " + L("7.4", "7.4") + "."),
("Is the course dataset real data?", "The main panel used in the lessons is simulated (N = 800, 3 waves of community adult residents) according to a predefined true structure (<code>data/simulate_data.R</code>), which allows us to verify whether the methods recover the true structure (the population target and within-person truth; see " + L("7.2", "7.2") + "). See the <a href=\"../data/data_dictionary.html\">Data Dictionary</a> for details. In addition, two real public datasets are included: the sports coaches mental health panel for the Lesson 7.6 exercise (CC0, bundled in the course package); and the <a href=\"case_elsoc.html\">ELSOC Case</a> using PHQ-8 from the Chilean Longitudinal Social Survey (CC0, preprocessed analysis file bundled). Sources, licenses, and citation formats for both are provided in the Data Dictionary.")]),
("Writing & Reporting", [
("What details are most frequently omitted in methods sections?", "The λ selection rule, number of CV folds, random seed, whether items were standardized, whether covariates were penalized, whether centrality calculations include autoregressions, number of bootstrap resamples, and the CS criterion. Check against the <a href=\"cheatsheets.html#report\">Reporting Checklist</a> item by item."),
("How do I ensure numbers in the results section are error-free?", "Every number should be traceable to a specific output file (see the 'number-to-file' cross-reference table in " + L("10.2", "10.2") + "). It is best practice to insert values automatically using Quarto inline code rather than copying by hand."),
("How should I write the limitations section?", "Include at least: standard CLPN conflates between-person and within-person effects; observational data cannot rule out unmeasured confounding; conclusions are dependent on the chosen time lag; and sample representativeness. See " + L("10.3", "10.3") + ".")])]
fq = ""
for i, (h, items) in enumerate(FAQ):
    fq += sec(f"q{i+1}", h, "".join(f'<details class="ans faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in items))
page("faq.html", "Frequently Asked Questions (FAQ)", f"<p>Course-wide frequently asked questions ({sum(len(x[1]) for x in FAQ)} items in total), grouped into five categories: Study & Usage, R & Software, Statistical Concepts, CLPN Methodology, and Writing & Reporting. Individual lesson pages also include 'Common Questions & Pitfalls' specific to their topics.</p>", fq)

# =====================================================================  Study Log
lesson_opts = "".join(f'<option value="{E(l["id"] + " " + l["title"])}"></option>' for m in MODULES for l in m["lessons"])
lg = '''<div class="slog-bar nprint">
<button type="button" class="slog-go" id="slogDownload">Download Markdown</button>
<button type="button" class="linkish" id="slogPrint">Print</button>
<button type="button" class="linkish quiet" id="slogClear">Clear entries on this page</button>
</div>
<p class="muted nprint">What you write stays in this browser. If you clear site data, switch browsers, or use a private window, the entries are gone. Download or print the page to keep a copy.</p>
'''
lg += sec("daily", "Session Logs", '''<div class="slog">
<label class="slog-name">Name <span class="muted nprint">Optional; used only in the downloaded file name</span><input id="slogName" type="text" autocomplete="name"></label>
<div id="slogDays"></div>
<p class="nprint"><button type="button" class="linkish" id="addDay">Add session entry</button></p>
</div>''', "slog")
lg += sec("weekly", "Weekly Summaries", '''<div class="slog"><div id="slogWeeks"></div>
<p class="nprint"><button type="button" class="linkish" id="addWeek">Add week</button></p></div>''', "slog")
lg += sec("feynman", "Feynman Check: Explain It in One Paragraph to a Social-Work Colleague with No Statistics Background", '''<div class="slog"><div id="slogFeyn"></div>
<p class="nprint"><button type="button" class="linkish" id="addFeyn">Add another check</button></p></div>''', "slog")
lg += sec("howto", "How to Use", '''<ul>
<li>Fill it in on this page. You do not need to save before you leave; what you write stays in this browser.</li>
<li>Spend 5–10 minutes on it after each study session. For the weekly review, open this page or the Markdown file you downloaded.</li>
<li>The "R errors encountered" column is especially useful: look back after a few weeks and you will see the same errors stop appearing.</li>
<li>To keep a copy that does not disappear with your browser data, click "Download Markdown" or "Print". You can also download the <a href="study_log.md" download>blank Markdown template</a> and fill it in with a text editor.</li>
</ul>''')
lg += f'<datalist id="slogLessons">{lesson_opts}</datalist>\n<script src="../lessons/assets/studylog.js"></script>\n'
page("study_log.html", "Study Log", "<p>Write one entry after each study session and a short summary each week. Fill it in on this page, then download it as Markdown or print it.</p>", lg)
md = "# CLPN From Scratch · Study Log\n\n> Fill in one row after each study session and write a short summary each week. You can save a copy as `study_log_yourname.md`.\n\n## Session Logs\n\n| Date | Lesson | Time Spent | Three things I learned today | What still feels unclear | R errors encountered & how I fixed them | Questions to figure out next |\n|---|---|---|---|---|---|---|\n" + "|  |  |  |  |  |  |  |\n" * 6 + \
     "\n## Weekly Summary (Week ___)\n\n- Lessons completed this week:\n- Quiz accuracy / exercises completed:\n- Most valuable concept (in my own words):\n- Remaining confusion & plan to resolve:\n- Exercises completed & archived:\n- Plan for next week:\n\n## Feynman Check\n\nConcept:\n\nExplain it in one paragraph to a social-work colleague with no statistics background:\n\nWhere I got stuck:\n"
open(D + "materials/study_log.md", "w", encoding="utf-8").write(md)

# =====================================================================  START_HERE.md
_rm = {}
exec(open(SRC + "/common/readmd.py", encoding="utf-8").read(), _rm)
_sh = _rm["reading_md"](open(D + "START_HERE.html", encoding="utf-8").read(), keep_links=True)
_sh = re.sub(r"\AStudy Materials\n+", "", _sh)
_sh = re.sub(r"^This page explains how to study.*$", "Generated by `src/en/build_materials.py` from the same source as [START_HERE.html](START_HERE.html).", _sh, count=1, flags=re.M)
open(D + "START_HERE.md", "w", encoding="utf-8").write(_sh)

dl = sec("pack", "Course Package (Zip)", """
<p><a class="dl" download href="../../downloads/clpn-course-en.zip">clpn-course-en.zip</a></p>
<p>The whole English course in one zip file. Extracting it gives you the folder <code>clpn-course-en/</code>:</p>
<ul>
<li><b>Offline website</b>: <code>index.html</code>, the Study Guide, all lessons, and all study materials. Double-click <code>index.html</code> to open it in your browser; no internet connection needed;</li>
<li><b>Data</b>: <code>data/</code> (simulated data, data dictionary, <code>simulate_data.R</code>, the coefficients used to generate the data; plus a real public dataset, <code>coaches_mhc_raw.csv</code>, CC0, for the Lesson 7.6 exercise);</li>
<li><b>R scripts</b>: <code>R/</code> (the script for each lesson, <code>_setup.R</code>, <code>run_all.R</code> to run everything, the R Code User Guide), <code>R/solutions/</code> (exercise solutions), <code>R/output/</code> (reference results);</li>
<li><code>README.md</code> (folder guide; read this first), <code>clpn-course.Rproj</code> (double-click to open in RStudio), <code>LICENSE</code> (course content CC BY 4.0, code MIT), <code>THIRD_PARTY_NOTICES.md</code>.</li>
</ul>
<p>After extracting, open <code>index.html</code> in your browser to study, and double-click <code>clpn-course.Rproj</code> to run R. Step-by-step instructions are under "How to Use" below.</p>""")
dl += sec("data", "Datasets", """
<p>Simulated panel data with no real personal information. <code>true_B_within.csv</code> and <code>true_B_population.csv</code> are the coefficients behind the simulation (the within-person truth and the population target), not estimates from your sample. A standard CLPN targets the second one (population OLS, which includes trait confounding); the two are not the same matrix. You can also open the files one by one:</p>
<ul>
<li><a href="../data/data_dictionary.html">Data Dictionary</a></li>
<li><a href="../data/clpn_sim_wide.csv">clpn_sim_wide.csv</a></li>
<li><a href="../data/clpn_sim_wide.sav">clpn_sim_wide.sav</a> (SPSS)</li>
<li><a href="../data/simulate_data.R">simulate_data.R</a></li>
</ul>
<p>A <b>real</b> public dataset is also included for the measurement invariance exercise in Lesson 7.6: <a href="../data/coaches_mhc_raw.csv">coaches_mhc_raw.csv</a> (the 14-item Mental Health Continuum Short Form, MHC-SF, from 422 Swiss sports coaches over 3 waves; Ackeret et al., 2023, <a href="https://doi.org/10.5061/dryad.8931zcrws">doi.org/10.5061/dryad.8931zcrws</a>, CC0 1.0). The file is included as published (semicolon-delimited). Read the notes in the <a href="../data/data_dictionary.html">Data Dictionary</a> before you use it: its subscale columns do not match its item columns, and the descriptions of the wave interval contradict each other.</p>
<p>A second real panel is included for the ELSOC case (<a href="../materials/case_elsoc.html">case page</a>): <a href="../data/elsoc_phq8_wide.csv">elsoc_phq8_wide.csv</a> (three waves of the PHQ-8 plus sex and age from the original 2016–2018 sample of the Chilean Longitudinal Social Survey; COES 2022, <a href="https://doi.org/10.7910/DVN/LQMURF">doi.org/10.7910/DVN/LQMURF</a>, CC0 1.0). This preprocessed subset is written by <code>R/data_elsoc.R</code> from the original file, which is also included (<code>data/elsoc/ELSOC_Wide_2016_2021_v1.00_R.RData</code>); the analysis script is <code>R/case_elsoc.R</code>. The citation format is in the last section of the Data Dictionary.</p>""")
dl += sec("howto", "How to Use", local_setup("../") + """
<p>The script link in each lesson opens the <code>.R</code> file itself, so you can read it in your browser. To run it, open the project in RStudio through <code>clpn-course.Rproj</code>.</p>""")
dl += sec("single", "Individual Files", """
<ul>
<li><a href="../materials/study_log.html">Study Log</a> (fill it in on the page, or download the <a href="../materials/study_log.md" download>blank Markdown</a>)</li>
<li><a href="../R/output/L6-4_network.pdf">L6-4 Network Plot PDF</a></li>
<li><a href="../R/README.html">R Code User Guide</a></li>
</ul>""")
page("downloads/index.html", "Download", "<p>The whole English course in one zip file: offline website, data, R scripts, and exercise solutions. Extract it to the <code>clpn-course-en/</code> folder, open <code>index.html</code> to study, and double-click <code>clpn-course.Rproj</code> to run R.</p>", dl)

# =====================================================================  Assessment pages (materials/assess_*.html)
_aspec = importlib.util.spec_from_file_location("assess", os.path.join(SRC, "common/assess.py"))
_as = importlib.util.module_from_spec(_aspec); _aspec.loader.exec_module(_as)
_qspec = importlib.util.spec_from_file_location("quiz", os.path.join(SRC, "common/quiz.py"))
_qz = importlib.util.module_from_spec(_qspec); _qspec.loader.exec_module(_qz)
_banks = _as.load_banks(SRC, REPO)
_RVG = {"ROOT": REPO}
exec(open(SRC + "/common/rvals.py", encoding="utf-8").read(), _RVG)
for _slug, _bank in _banks.items():
    page(_as.fname(_slug), _as.SPEC[_slug][1], _RVG["fillV"](_bank["LEAD"]), _RVG["fillV"](_as.render_body(_slug, _bank, _qz.quiz, sec)))
if _banks:
    page(_as.HUB, "Assessments: Pre-Test, Module Quizzes & Final Exam", "<p>The pre-test shows where you start, each module quiz checks one module, and the final exam covers the whole course. This page explains how to use them, how they are scored, and the scoring rubrics.</p>", _as.render_hub(_banks, sec))
for _f in ("writing", "reading", "case_elsoc"):
    exec(open(SRC + f"/materials/{_f}.py", encoding="utf-8").read(), globals())
for _f in os.listdir(D + "materials"):
    _m = re.fullmatch(r"assess_(\w+)\.html", _f)
    if (_m and _m.group(1) not in _banks) or (_f == _as.HUB and not _banks):
        os.remove(D + "materials/" + _f)

_spec = importlib.util.spec_from_file_location("mdhtml", os.path.join(SRC, "common/mdhtml.py"))
_md = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_md)
MD_DOCS = [
    ("R/README.md", "R Code User Guide"),
    ("data/data_dictionary.md", "Data Dictionary"),
    ("R/output/L10-1_analysis_plan.md", "Analysis Plan"),
    ("R/output/L10-3_results_draft.md", "Results Draft"),
]
for src_rel, fallback in MD_DOCS:
    raw = open(os.path.join(D, src_rel), encoding="utf-8").read()
    title, body = _md.render_md(raw)
    out_rel = src_rel[:-3] + ".html"
    page(out_rel, title or fallback,
         f'<p>Source Markdown: <a href="{os.path.basename(src_rel)}" download><code>{E(os.path.basename(src_rel))}</code></a></p>',
         f'<section class="sec" id="doc">{body}</section>',
         rel=out_rel)
print("EN materials ok:", ", ".join(f for f, _ in PAGES), "+ study_log.md + START_HERE.md + rendered md")
