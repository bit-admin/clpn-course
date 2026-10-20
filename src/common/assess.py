# -*- coding: utf-8 -*-
"""测评页（前测、11 个模块阶段测验、期末）的规格与渲染。由 src/build_materials.py 调用。

题库放在 src/assess/<slug>.py（纯数据，格式见 src/assess/README.md），可选 LEAD / INTRO / OUTRO 三段 HTML。
题库执行时可用 ROOT 和 ANS（期末 C 部分答案）；页面里的 {{V:键}} 由 build_materials.py 用 src/common/rvals.py 的当前 R 输出替换。某个 slug 的题库文件
存在时才生成 materials/assess_<slug>.html；一个题库都没有时，本模块不生成任何页面。
考核比重只写在 src/template.html 的 #assessment 表里，测评页和题库都不重复写比重。"""
import html, importlib.util, os
E = html.escape

# (slug, 页面标题, 自动判分题数, 简答题数)。数量与 BATCH3 计划 §2 一致，src/test/check_assess.py 按此核对。
# M7 另有 4 道进阶题（7.6 / 7.7，adv=True），不计入 10 道。期末自动题 = A 部分 25 + C 部分 5。
SPECS = [
    ("pre", "前测：开始之前看看自己的起点", 14, 0),
    ("m0", "M0 阶段测验", 6, 0),
    ("m1", "M1 阶段测验", 10, 1),
    ("m2", "M2 阶段测验", 8, 1),
    ("m3", "M3 阶段测验", 10, 1),
    ("m4", "M4 阶段测验", 8, 1),
    ("m5", "M5 阶段测验", 10, 1),
    ("m6", "M6 阶段测验", 10, 1),
    ("m7", "M7 阶段测验", 10, 1),
    ("m8", "M8 阶段测验", 8, 1),
    ("m9", "M9 阶段测验", 6, 1),
    ("m10", "M10 阶段测验", 4, 0),
    ("final", "期末考试", 30, 4),
]
SPEC = {s[0]: s for s in SPECS}
# 什么时候做（按大纲 #pacing 的标准节奏）
WHEN = {"pre": "第 1 周，学 0.1 之前", "m0": "第 1 周，学完 0.2", "m1": "第 5 周（与 M2 一起，原“复习 A”）",
        "m2": "第 5 周（与 M1 一起）", "m3": "第 8 周（与 M4 一起，原“复习 B”）", "m4": "第 8 周（与 M3 一起）",
        "m5": "第 10 周，学完 5.4", "m6": "第 11 周，学完 6.5", "m7": "第 13 周，学完 7.5（7.6 / 7.7 选学后再做进阶题）",
        "m8": "第 14 周，学完 8.3", "m9": "第 15 周，学完 9.3", "m10": "第 16 周，项目定稿前", "final": "第 16 周，学完 10.3"}
MINUTES = {"pre": "约 20 分钟", "final": "约 90 分钟"}
HUB = "assessment.html"
def fname(slug): return f"assess_{slug}.html"

def answers(root):
    """R/assess_answers.R 写出的期末 C 部分答案：{"C1": "2.191", ...}；文件不存在时为空。"""
    import csv
    p = os.path.join(root, "R", "output", "assess_answers.csv")
    if not os.path.exists(p): return {}
    with open(p, encoding="utf-8") as fh:
        return {r["key"]: f"{float(r['value']):g}" for r in csv.DictReader(fh)}

def load_banks(src, root):
    """读取 src/assess/<slug>.py，返回 {slug: dict(ITEMS=[], SHORT=[], INTRO="", LEAD="")}，按 SPECS 顺序。"""
    banks = {}
    for slug, *_ in SPECS:
        p = os.path.join(src, "assess", slug + ".py")
        if not os.path.exists(p): continue
        g = {"ROOT": root, "ANS": answers(root)}   # 期末 C 部分的答案来自 R/output/assess_answers.csv（R/assess_answers.R）
        exec(open(p, encoding="utf-8").read(), g)
        banks[slug] = dict(ITEMS=g.get("ITEMS", []), SHORT=g.get("SHORT", []), INTRO=g.get("INTRO", ""), LEAD=g.get("LEAD", ""),
                           OUTRO=g.get("OUTRO") or "", PARTS=g.get("PARTS"))
    return banks

def short_html(n, s, label="简答"):
    """简答题：题干 + 折叠的参考答案与评分标准（打印时 details.faq 自动展开）。
    评分标准二选一：rubric = 0–3 四级；dims = 期末 B 部分的 4 个维度 [(维度, 分值, 本题要点)]，合计 10 分。"""
    if s.get("dims"):
        rows = "".join(f"<tr><td>{d}</td><td>{E(str(pt))}</td><td>{k}</td></tr>" for d, pt, k in s["dims"])
        tab = f'<div class="tablewrap"><table><tr><th>维度</th><th>分值</th><th>本题要点</th></tr>{rows}</table></div>'
    else:
        rub = "".join(f"<tr><td>{E(str(lv))}</td><td>{d}</td></tr>" for lv, d in s["rubric"])
        tab = f'<div class="tablewrap"><table><tr><th>等级</th><th>标准</th></tr>{rub}</table></div>'
    return (f'<div class="exitem"><h4>{label} {n}</h4>{s["q"]}'
            f'<details class="faq"><summary>参考答案与评分标准</summary>{s["answer"]}{tab}</details></div>')

def render_body(slug, bank, quiz, sec):
    """一个测评页的正文。quiz = src/common/quiz.py 的 quiz()；sec = build_materials.py 的 sec()。"""
    body = bank["INTRO"]
    auto = [it for it in bank["ITEMS"] if not it.get("adv")]
    adv = [it for it in bank["ITEMS"] if it.get("adv")]
    if bank.get("PARTS"):   # 期末：按 PARTS = [(part, 标题, 说明 HTML)] 分节；part == "short" 的一节放简答题
        first = True
        for pid, title, intro in bank["PARTS"]:
            if pid == "short":
                body += sec("part" + pid, title, intro + "\n".join(short_html(n, s, "题") for n, s in enumerate(bank["SHORT"], 1)))
                continue
            qs = ('<p class="quizscore"></p>' if first else "") + "\n".join(quiz(it["q"]) for it in auto if it.get("part") == pid)
            body += sec("part" + pid, title, intro + qs); first = False
    else:
        qs = '<p class="quizscore"></p>' + "\n".join(quiz(it["q"]) for it in auto)
        body += sec("auto", "自动判分题", qs)
        if adv: body += sec("adv", "进阶选学题（7.6 / 7.7）", "\n".join(quiz(it["q"]) for it in adv))
        if bank["SHORT"]: body += sec("short", "简答题", "\n".join(short_html(n, s) for n, s in enumerate(bank["SHORT"], 1)))
    body += bank["OUTRO"]
    if slug != "pre":
        body += sec("next", "做完以后", '<p>一次答对 70% 及以上就进入下一个模块；不到 70% 的，按错题解释里的链接回去复习，过几天再做一次。把一次答对的题数记进<a href="study_log.html">学习日志</a>。'
                    '计分方式和评分标准见<a href="assessment.html">测评总页</a>。</p>')
    return body

def render_hub(banks, sec):
    """测评总页 materials/assessment.html 的正文：怎么用、各测评一览（只链接已生成的页面）、计分与评分标准。"""
    rows = ""
    for slug, title, n_auto, n_short in SPECS:
        name = f'<a href="{fname(slug)}">{E(title)}</a>' if slug in banks else f'{E(title)}<br><span class="muted">（即将加入）</span>'
        qty = f"{n_auto} 道自动判分" + (f" + {n_short} 道简答" if n_short else "")
        rows += f"<tr><td>{name}</td><td>{WHEN[slug]}</td><td>{qty}</td><td>{MINUTES.get(slug, '15–25 分钟')}</td></tr>"
    body = sec("use", "一、测评怎么用", """
<p>这门课有三种测评，目的都是让你<b>看清自己哪里已经会了、哪里还不会</b>：</p>
<ul><li><b>前测</b>（pre-test）：开始学习之前做一次，看看自己的起点，并据此选择 {{C:weeks}} 周还是更宽松的 19 周节奏。前测<b>不计分</b>，推荐做，但不强制。</li>
<li><b>阶段测验</b>（module quiz）：每学完一个模块做一次。题目是新写的，不是课内“理解检查”的原题。</li>
<li><b>期末考试</b>（final exam）：学完 10.3 后做，覆盖全课程，其中一部分题目与前测考同样的知识点，可以对照自己的进步。</li></ul>
<p>答题方式和课内测验一样：答错会先给提示，答错两次后可以点“查看答案与解释”。解释里有链接，指回讲解这个知识点的课。</p>
<div class="box warnbox"><b class="bt">关于答案</b><p>本课程为纯离线网页，测验的目的是帮你找出薄弱环节。请先独立作答，再展开答案与解析核对。</p></div>""")
    body += sec("list", "二、全部测评一览", '<div class="tablewrap"><table><tr><th>测评</th><th>什么时候做</th><th>题量</th><th>时长</th></tr>' + rows + "</table></div>")
    body += sec("score", "三、怎么计分", """
<p>每个测评页顶部会显示“本页测验：已答对 x / n 题（其中一次答对 y 题）”。<b>以“一次答对”的题数为准</b>：答错一次以后再答对，说明这个知识点还不牢固。</p>
<ul><li>把每次的“一次答对”题数和用时记进<a href="study_log.html">学习日志</a>的周小结。分数不会自动保存，刷新页面后会清零。</li>
<li>阶段测验一次答对的比例达到 70% 及以上，就可以进入下一个模块；不到 70% 的，按每道错题解释里的链接回去复习，过几天再做一次。</li>
<li>简答题没有自动判分：先自己写，再展开“参考答案与评分标准”，按 0–3 级给自己打分；不满意的，过几天再重写一遍，再打一次分。</li>
<li>各部分在总评中的具体安排，见<a href="../index.html#assessment">课程大纲的“考核与反馈”</a>。</li></ul>""")
    body += sec("rubric", "四、评分标准", """
<h3>简答题（阶段测验与期末通用的 0–3 级标准）</h3>
<div class="tablewrap"><table><tr><th>等级</th><th>标准</th></tr>
<tr><td>3</td><td>结论正确；用对了关键术语；引用了题目给出的数字或证据；没有过度解读（例如把相关说成因果、把群体结论套到个人）</td></tr>
<tr><td>2</td><td>结论基本正确，但术语不够准确，或者缺少数字 / 证据支持</td></tr>
<tr><td>1</td><td>只答对一部分，或者有一处明显的概念错误</td></tr>
<tr><td>0</td><td>没有作答，或者结论错误</td></tr></table></div>
<p>每道简答题下面还有针对这道题的具体评分要点。</p>
<h3>期末 B 部分（解读题，每题 10 分）</h3>
<div class="tablewrap"><table><tr><th>维度</th><th>分值</th></tr>
<tr><td>结论正确</td><td>4</td></tr><tr><td>引用了正确的数字与区间</td><td>3</td></tr>
<tr><td>方向与 B[k, j] 的读法正确（T 时刻的 k 指向 T+1 时刻的 j）</td><td>2</td></tr>
<tr><td>没有因果或个体层面的过度解读</td><td>1</td></tr></table></div>
<h3>毕业项目</h3>
<p>评分维度见<a href="../index.html#assessment">课程大纲的“考核与反馈”</a>。</p>""")
    return body
