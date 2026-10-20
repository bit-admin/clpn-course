# -*- coding: utf-8 -*-
"""Specifications and rendering for English assessment pages (pre-test, 11 module quizzes, final exam)."""
import html, importlib.util, os
E = html.escape

SPECS = [
    ("pre", "Pre-test: check your starting point", 14, 0),
    ("m0", "M0 module quiz", 6, 0),
    ("m1", "M1 module quiz", 10, 1),
    ("m2", "M2 module quiz", 8, 1),
    ("m3", "M3 module quiz", 10, 1),
    ("m4", "M4 module quiz", 8, 1),
    ("m5", "M5 module quiz", 10, 1),
    ("m6", "M6 module quiz", 10, 1),
    ("m7", "M7 module quiz", 10, 1),
    ("m8", "M8 module quiz", 8, 1),
    ("m9", "M9 module quiz", 6, 1),
    ("m10", "M10 module quiz", 4, 0),
    ("final", "Final Exam", 30, 4),
]
SPEC = {s[0]: s for s in SPECS}
WHEN = {
    "pre": "Week 1, before Lesson 0.1",
    "m0": "Week 1, after Lesson 0.2",
    "m1": "Week 5 (together with M2)",
    "m2": "Week 5 (together with M1)",
    "m3": "Week 8 (together with M4)",
    "m4": "Week 8 (together with M3)",
    "m5": "Week 10, after Lesson 5.4",
    "m6": "Week 11, after Lesson 6.5",
    "m7": "Week 13, after Lesson 7.5 (advanced questions after the optional 7.6 / 7.7)",
    "m8": "Week 14, after Lesson 8.3",
    "m9": "Week 15, after Lesson 9.3",
    "m10": "Week 16, before you finalize the capstone project",
    "final": "Week 16, after Lesson 10.3",
}
MINUTES = {"pre": "~20 min", "final": "~90 min"}
HUB = "assessment.html"
def fname(slug): return f"assess_{slug}.html"

def answers(root):
    """Part C answers written by R/assess_answers.R."""
    import csv
    p = os.path.join(root, "R", "output", "assess_answers.csv")
    if not os.path.exists(p): return {}
    with open(p, encoding="utf-8") as fh:
        return {r["key"]: f"{float(r['value']):g}" for r in csv.DictReader(fh)}

def load_banks(src, root):
    """Load src/en/assess/<slug>.py in SPECS order."""
    banks = {}
    for slug, *_ in SPECS:
        p = os.path.join(src, "assess", slug + ".py")
        if not os.path.exists(p): continue
        g = {"ROOT": root, "ANS": answers(root)}
        exec(open(p, encoding="utf-8").read(), g)
        banks[slug] = dict(ITEMS=g.get("ITEMS", []), SHORT=g.get("SHORT", []), INTRO=g.get("INTRO", ""), LEAD=g.get("LEAD", ""),
                           OUTRO=g.get("OUTRO") or "", PARTS=g.get("PARTS"))
    return banks

def short_html(n, s, label="Short answer"):
    """Short-answer item with collapsible reference answer and scoring rubric."""
    if s.get("dims"):
        rows = "".join(f"<tr><td>{d}</td><td>{E(str(pt))}</td><td>{k}</td></tr>" for d, pt, k in s["dims"])
        tab = f'<div class="tablewrap"><table><tr><th>Dimension</th><th>Points</th><th>Points to look for</th></tr>{rows}</table></div>'
    else:
        rub = "".join(f"<tr><td>{E(str(lv))}</td><td>{d}</td></tr>" for lv, d in s["rubric"])
        tab = f'<div class="tablewrap"><table><tr><th>Level</th><th>Criteria</th></tr>{rub}</table></div>'
    return (f'<div class="exitem"><h4>{label} {n}</h4>{s["q"]}'
            f'<details class="faq"><summary>Reference answer &amp; rubric</summary>{s["answer"]}{tab}</details></div>')

def render_body(slug, bank, quiz, sec):
    """Render the body of one assessment page."""
    body = bank["INTRO"]
    auto = [it for it in bank["ITEMS"] if not it.get("adv")]
    adv = [it for it in bank["ITEMS"] if it.get("adv")]
    if bank.get("PARTS"):
        first = True
        for pid, title, intro in bank["PARTS"]:
            if pid == "short":
                body += sec("part" + pid, title, intro + "\n".join(short_html(n, s, "Question") for n, s in enumerate(bank["SHORT"], 1)))
                continue
            qs = ('<p class="quizscore"></p>' if first else "") + "\n".join(quiz(it["q"]) for it in auto if it.get("part") == pid)
            body += sec("part" + pid, title, intro + qs); first = False
    else:
        qs = '<p class="quizscore"></p>' + "\n".join(quiz(it["q"]) for it in auto)
        body += sec("auto", "Auto-graded questions", qs)
        if adv: body += sec("adv", "Optional advanced questions (7.6 / 7.7)", "\n".join(quiz(it["q"]) for it in adv))
        if bank["SHORT"]: body += sec("short", "Short-answer questions", "\n".join(short_html(n, s) for n, s in enumerate(bank["SHORT"], 1)))
    body += bank["OUTRO"]
    if slug != "pre":
        body += sec("next", "When you finish", '<p>If you got at least 70% right on the first try, move on to the next module; if not, follow the links in the explanations of the questions you missed, review those lessons, and take the quiz again in a few days. Write your first-try score in your <a href="study_log.html">study log</a>. '
                    'For how scoring works and the rubrics, see the <a href="assessment.html">assessments page</a>.</p>')
    return body

def render_hub(banks, sec):
    """Render the body of materials/assessment.html."""
    rows = ""
    for slug, title, n_auto, n_short in SPECS:
        name = f'<a href="{fname(slug)}">{E(title)}</a>' if slug in banks else f'{E(title)}<br><span class="muted">(coming soon)</span>'
        qty = f"{n_auto} auto-graded" + (f" + {n_short} short-answer" if n_short else "")
        rows += f"<tr><td>{name}</td><td>{WHEN[slug]}</td><td>{qty}</td><td>{MINUTES.get(slug, '15–25 min')}</td></tr>"
    body = sec("use", "1. How to use the assessments", """
<p>The course has three kinds of assessment. All of them are there to help you <b>see clearly what you already know and what you don't yet</b>:</p>
<ul><li><b>Pre-test</b>: take it once before you start, to see your starting point and choose between the {{C:weeks}}-week pace and the more relaxed 19-week pace. The pre-test is <b>ungraded</b>: recommended, but optional.</li>
<li><b>Module quizzes</b>: take one after you finish each module. The questions are new, not repeats of the Concept Check questions in the lessons.</li>
<li><b>Final exam</b>: take it after Lesson 10.3. It covers the whole course, and some of its questions test the same points as the pre-test, so you can see your progress.</li></ul>
<p>You answer the questions the same way as the quizzes in the lessons: a wrong answer first gets a hint, and after two wrong answers you can click "Show Answer &amp; Explanation." The explanation links back to the lesson that teaches the point.</p>
<div class="box warnbox"><b class="bt">About the answers</b><p>The course is a set of offline web pages, and the quizzes are there to help you find your weak spots. Answer on your own first, then open the answers and explanations to check.</p></div>""")
    body += sec("list", "2. All assessments at a glance", '<div class="tablewrap"><table><tr><th>Assessment</th><th>When</th><th>Questions</th><th>Time</th></tr>' + rows + "</table></div>")
    body += sec("score", "3. How scoring works", """
<p>The top of each assessment page shows "Quiz score on this page: x / n correct (y correct on first try)." <b>Your score is the number correct on the first try</b>: if you needed a second try, the point is not yet solid.</p>
<ul><li>Write each first-try score and the time you took in the weekly summary of your <a href="study_log.html">study log</a>. Scores are not saved automatically and reset when you reload the page.</li>
<li>Once you get at least 70% of a module quiz right on the first try, you can move on to the next module; if not, follow the links in the explanations of the questions you missed, review, and take the quiz again a few days later.</li>
<li>Short-answer questions are not scored automatically: write your answer first, then open "Reference answer &amp; rubric" and score yourself on the 0–3 scale. If you are not happy with it, rewrite it a few days later and score it again.</li>
<li>For how each part counts toward the overall grade, see <a href="../index.html#assessment">Assessment and Feedback in the syllabus</a>.</li></ul>""")
    body += sec("rubric", "4. Rubrics", """
<h3>Short-answer questions (the 0–3 scale used in the module quizzes and the final)</h3>
<div class="tablewrap"><table><tr><th>Level</th><th>Criteria</th></tr>
<tr><td>3</td><td>Correct conclusion; key terms used correctly; cites the numbers or evidence given in the question; no over-interpretation (e.g. calling a correlation causal, or applying a group-level conclusion to an individual)</td></tr>
<tr><td>2</td><td>Conclusion basically correct, but the terms are imprecise or the numbers / evidence are missing</td></tr>
<tr><td>1</td><td>Only partly correct, or one clear conceptual error</td></tr>
<tr><td>0</td><td>No answer, or a wrong conclusion</td></tr></table></div>
<p>Each short-answer question also lists the specific points to look for in that question.</p>
<h3>Final exam Part B (interpretation questions, 10 points each)</h3>
<div class="tablewrap"><table><tr><th>Dimension</th><th>Points</th></tr>
<tr><td>Correct conclusion</td><td>4</td></tr><tr><td>Cites the correct numbers and intervals</td><td>3</td></tr>
<tr><td>Reads the direction and B[k, j] correctly (k at time T → j at time T+1)</td><td>2</td></tr>
<tr><td>No causal or individual-level over-interpretation</td><td>1</td></tr></table></div>
<h3>Capstone project</h3>
<p>For the scoring dimensions, see <a href="../index.html#assessment">Assessment and Feedback in the syllabus</a>.</p>""")
    return body
