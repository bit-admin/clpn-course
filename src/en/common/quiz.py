# -*- coding: utf-8 -*-
"""Quiz HTML renderer shared across M0–M4 lessons, M5–M10 lessons, and assessment pages."""
import html
E = html.escape

def parse_quiz(body):
    """Parse a ```quiz block into dict(q, opts, exp, hint, kind, ans, tol)."""
    q, opts, exp, hint, kind, ans, tol, cur = "", [], "", "", "mc", "", "0", None
    for line in body.split("\n"):
        s = line.strip()
        if not s: continue
        if s.startswith("Q:"): q = s[2:].strip(); cur = "q"
        elif s.startswith("E:"): exp = s[2:].strip(); cur = "e"
        elif s.startswith("H:"): hint = s[2:].strip(); cur = "h"
        elif s.startswith("N:"): kind = "num"; a = s[2:].split("|"); ans = a[0].strip(); tol = a[1].strip() if len(a) > 1 else "0"; cur = None
        elif s.startswith("T:"): kind = "txt"; ans = s[2:].strip(); cur = None
        elif s[:2] in ("- ", "+ "):
            parts = s[2:].split("||", 1); opts.append([s[0] == "+", parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""]); cur = "o"
        else:
            if cur == "q": q += " " + s
            elif cur == "e": exp += " " + s
            elif cur == "h": hint += " " + s
            elif cur == "o": opts[-1][2] += " " + s
    return dict(q=q, opts=opts, exp=exp, hint=hint, kind=kind, ans=ans, tol=tol)

def quiz(body):
    """```quiz macro -> HTML for one question (mc / num / txt)."""
    p = parse_quiz(body)
    q, opts, exp, hint, kind, ans, tol = p["q"], p["opts"], p["exp"], p["hint"], p["kind"], p["ans"], p["tol"]
    out = f'<div class="quiz" data-kind="{kind}"'
    if kind == "num": out += f' data-ans="{E(ans)}" data-tol="{E(tol)}"'
    if kind == "txt": out += f' data-ans="{E(ans)}"'
    out += f'><p class="qtext">{q}</p>'
    if kind == "mc":
        assert sum(o[0] for o in opts) == 1, ("quiz needs exactly one right option", q)
        out += '<ul class="opts">' + "".join(f'<li><button type="button" data-ok="{1 if ok else 0}">{t}</button>' + (f'<div class="ofb" hidden>{fb}</div>' if fb else "") + "</li>" for ok, t, fb in opts) + "</ul>"
    else:
        out += '<div class="numrow"><input type="text" aria-label="Your answer" placeholder="Enter answer"><button type="button" class="qbtn">Check</button></div>'
        if hint: out += f'<div class="qhint" hidden>{hint}</div>'
    out += '<div class="fb" role="status"></div>'
    if exp: out += f'<div class="qexp" hidden>{exp}</div>'
    return out + "</div>"

def quiz_tuples(qs):
    """M5–M10 tuple list -> multiple-choice quiz HTML."""
    out = []
    for q in qs:
        qt, opts, c, fbs = q
        lis = "".join(f'<li><button type="button" data-ok="{1 if k == c else 0}">{chr(65+k)}. {o}</button>' + (f'<div class="ofb" hidden>{fbs[k]}</div>' if k < len(fbs) and fbs[k] else "") + "</li>" for k, o in enumerate(opts))
        out.append(f'<div class="quiz" data-kind="mc"><p class="qtext">{qt}</p><ul class="opts">{lis}</ul><div class="fb" role="status"></div></div>')
    return "\n".join(out)
