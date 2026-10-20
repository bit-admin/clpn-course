# -*- coding: utf-8 -*-
"""测验 HTML 渲染器：M0–M4 课件、M5–M10 课件和 materials/ 测评页共用。
输出的标记由 lessons/assets/lesson.js 的 initQuizzes() 驱动（答错给提示，两次后可看答案，.quizscore 计分）。

两种输入格式：
  quiz(body)          ```quiz 宏的正文（M0–M4 课件、src/assess/ 题库）。行首标记：
                      Q: 题干   - 错误选项 || 反馈   + 正确选项 || 反馈（恰好一个 +）
                      N: 答案 | 容差（数值题）   T: 答案1 || 答案2（文本题）   H: 提示   E: 解释
                      不带标记的行接在上一个字段后面。
  quiz_tuples(qs)     M5–M10 的元组列表 (题干, 选项列表, 正确选项下标, 反馈列表)，选项前自动加 A. B. C.
parse_quiz(body) 只解析不渲染，供 src/test/check_assess.py 检查题库。
加载方式（与 mdhtml.py 相同）：importlib.util.spec_from_file_location("quiz", ".../src/common/quiz.py")。"""
import html
E = html.escape

def parse_quiz(body):
    """把 ```quiz 正文解析成 dict：q, opts [[是否正确, 文本, 反馈]], exp, hint, kind (mc/num/txt), ans, tol。"""
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
    """```quiz 宏 → 一道题的 HTML（mc / num / txt）。"""
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
        out += '<div class="numrow"><input type="text" aria-label="你的答案" placeholder="输入答案"><button type="button" class="qbtn">检查</button></div>'
        if hint: out += f'<div class="qhint" hidden>{hint}</div>'
    out += '<div class="fb" role="status"></div>'
    if exp: out += f'<div class="qexp" hidden>{exp}</div>'
    return out + "</div>"

def quiz_tuples(qs):
    """M5–M10 元组 → 与 M0–M4 相同格式的单选题 HTML，题与题之间换行。"""
    out = []
    for q in qs:
        qt, opts, c, fbs = q
        lis = "".join(f'<li><button type="button" data-ok="{1 if k == c else 0}">{chr(65+k)}. {o}</button>' + (f'<div class="ofb" hidden>{fbs[k]}</div>' if k < len(fbs) and fbs[k] else "") + "</li>" for k, o in enumerate(opts))
        out.append(f'<div class="quiz" data-kind="mc"><p class="qtext">{qt}</p><ul class="opts">{lis}</ul><div class="fb" role="status"></div></div>')
    return "\n".join(out)
