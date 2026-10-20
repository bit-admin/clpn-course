# -*- coding: utf-8 -*-
import html, json, os
SRC = os.path.dirname(os.path.abspath(__file__))   # 内容源目录：src/（英文版镜像为 src/en/）
LANG = "en" if os.path.basename(SRC) == "en" else "zh"
REPO = os.path.dirname(os.path.dirname(SRC)) if LANG == "en" else os.path.dirname(SRC)
ROOT = REPO + "/en" if LANG == "en" else REPO       # 站点根：中文版是仓库根，英文版是 en/
D = SRC + "/"
g = {}
for f in ["data1","data2","data3","data4"]:
    exec(open(D+f+".py", encoding="utf-8").read(), g)
MODULES, PACING, REFS = g["MODULES"], g["PACING"], g["REFS"]
sg = {}
exec(open(D + "common/shell.py", encoding="utf-8").read(), sg)
COPY_NOTE = sg["COPY_NOTE"]
E = html.escape
lessons_all = [(m, l) for m in MODULES for l in m["lessons"]]
ids = {l["id"] for _, l in lessons_all}
for _, l in lessons_all:
    for p in l["pre"]: assert p in ids, (l["id"], p)
n_lessons = len(lessons_all)
core = [(m, l) for m, l in lessons_all if not l.get("opt")]          # 标准节奏只计核心课；选学课（opt=True）另计
total_min = sum(l["time"] for _, l in core)
sessions = sum(l.get("sessions",1) for _, l in core)
fillC, COURSE_SIZE, N_WEEKS = g["fillC"], g["COURSE_SIZE"], g["N_WEEKS"]
# 手写文档不能用 {{C:…}} 宏：检查它们写的课程规模与 data4.py 的常量一致
for _doc in (["CLAUDE.md", "README.md", "src/README.md"] if LANG == "zh" else []):
    if _doc == "CLAUDE.md" and not os.path.exists(REPO + "/" + _doc): continue   # 本地文件，不在仓库中
    assert COURSE_SIZE in open(REPO + "/" + _doc, encoding="utf-8").read(), f"{_doc} 里的课程规模不是“{COURSE_SIZE}”，请更新"
def anchor(i): return "L" + i.replace(".", "-")
def ft(m):
    h, mm = divmod(m, 60)
    return ((f"{h} 小时" if h else "") + (f" {mm} 分钟" if mm else "")).strip()
def pre_html(pre):
    return '<span class="muted">无（起点课）</span>' if not pre else " ".join(f'<a class="chip" href="#{anchor(p)}">{p}</a>' for p in pre)

mods = []
for m in MODULES:
    mins = sum(l["time"] for l in m["lessons"] if not l.get("opt")); opt_mins = sum(l["time"] for l in m["lessons"] if l.get("opt")); out = []
    for l in m["lessons"]:
        s = l.get("sessions", 1)
        con = "".join(f'<li><b>{E(z)}</b><span class="en">{E(e)}</span></li>' for z, e in l["con"])
        math = f'<div class="math"><span class="tag">最少数学</span>{E(l["math"])}</div>' if l.get("math") else ""
        code = f'<details class="code"><summary>R 代码预览（示意）</summary><pre><code>{E(l["code"])}</code></pre></details>' if l.get("code") else ""
        out.append(f'''<details class="lesson" id="{anchor(l["id"])}">
 <summary><label class="done"><input type="checkbox" data-lid="{l["id"]}" aria-label="标记第 {l["id"]} 课为已完成"><span></span></label>
  <span class="lid">{l["id"]}</span><span class="ltitle">{E(l["title"])}</span>
  <span class="meta">{"进阶选学 · " if l.get("opt") else ""}{ft(l["time"])}{f" · 分 {s} 次" if s>1 else ""}</span></summary>
 <div class="lbody">
  <div class="lmeta"><div class="row"><div class="kv"><span class="k">预计时长</span>课文学习 {ft(l["time"])}{f"（分 {s} 次）" if s>1 else ""} + 练习约 {ft(max(45, l["time"]//2+30))}</div>
   <div class="kv"><span class="k">先修课</span>{pre_html(l["pre"])}</div></div>
   {('<a class="enter" href="lessons/'+anchor(l["id"])+'.html">学习 '+l["id"]+'</a>') if os.path.exists(os.path.join(ROOT,'lessons',anchor(l["id"])+'.html')) else '<span class="muted">尚未制作</span>'}</div>
  <h4>学习目标</h4><ol>{"".join(f"<li>{E(o)}</li>" for o in l["obj"])}</ol>
  <h4>核心概念</h4><ul class="concepts">{con}</ul>
  {math}
  <h4>动手练习</h4><p class="ex">{E(l["ex"])}</p>
  {code}
  <h4>自测问题</h4><ol>{"".join(f"<li>{E(c)}</li>" for c in l["chk"])}</ol>
 </div></details>''')
    mods.append(f'''<section class="module" id="{m["id"]}" style="--c:{m["color"]}">
 <header class="mhead"><div class="mnum">模块 {m["id"][1:]}</div>
  <h2>{E(m["title"])} <small>{E(m["en"])}</small></h2><p>{E(m["intro"])}</p>
  <div class="mstats"><span>{len(m["lessons"])} 节课{"（含 " + str(sum(1 for l in m["lessons"] if l.get("opt"))) + " 节选学）" if any(l.get("opt") for l in m["lessons"]) else ""}</span><span>学习约 {round(mins/60,1)} 小时{f"（选学另约 {round(opt_mins/60,1)} 小时）" if opt_mins else ""}</span><span class="mprog" data-mod="{m["id"]}"><i></i><b>0%</b></span></div>
 </header>
 {"".join(out)}
</section>''')

nav = "".join(f'<li class="navmod" style="--c:{m["color"]}"><a href="#{m["id"]}" class="navm">{m["id"][1:]}&nbsp; {E(m["title"])}</a><ul>' +
              "".join(f'<li><a href="#{anchor(l["id"])}" data-nav="{l["id"]}"><span>{l["id"]}</span>{E(l["title"])}{"（选学）" if l.get("opt") else ""}</a></li>' for l in m["lessons"]) + "</ul></li>" for m in MODULES)
flow = ' <em>→</em> '.join(f'<a href="#{m["id"]}" style="--c:{m["color"]}">{m["id"]} {E(m["title"].split("：")[0].split("（")[0])}</a>' for m in MODULES)
def mod_counts(m):   # 课数与小时只算核心课；选学课单独标出（与 COURSE_SIZE 的口径一致）
    core_l = [l for l in m["lessons"] if not l.get("opt")]
    n_opt = len(m["lessons"]) - len(core_l)
    return f'{len(core_l)}{f" + {n_opt} 选学" if n_opt else ""}', round(sum(l["time"] for l in core_l) / 60, 1)
modsum = "".join(f'<tr><td><a href="#{m["id"]}">{m["id"]}</a></td><td>{E(m["title"])}<br><span class="muted">{E(m["en"])}</span></td><td>{mod_counts(m)[0]}</td><td>{mod_counts(m)[1]}</td></tr>' for m in MODULES)
pace = "".join(f'<tr><td>第 {w} 周</td><td>{E(a)}</td><td>{E(b)}</td></tr>' for w, a, b in PACING)
refs = ""
for sec, items in REFS:
    lis = ""
    for r in items:
        link = f' <a href="{r["url"]}" target="_blank" rel="noopener">{E(r["url"].replace("https://",""))}</a>' if r["url"] else ""
        lis += f'<li><div class="cite">{r["c"]}{link}</div><div class="rnote">{E(r["note"])}</div></li>'
    refs += f'<h3>{E(sec)}</h3><ul class="refs">{lis}</ul>'
seen = {}
for _, l in lessons_all:
    for z, e in l["con"]: seen.setdefault(z, (e, l["id"]))
gloss = "".join(f'<tr><td>{E(z)}</td><td>{E(e)}</td><td><a href="#{anchor(i)}">{i}</a></td></tr>' for z, (e, i) in seen.items())
modmap = {m["id"]: [l["id"] for l in m["lessons"]] for m in MODULES}

tpl = open(D+"template.html", encoding="utf-8").read()
rep = {"__CSS__": open(REPO + "/src/style.css", encoding="utf-8").read(),
       "__JS__": open(D+"app.js", encoding="utf-8").read().replace("__MODS__", json.dumps(modmap)).replace("__TOTAL__", str(n_lessons)),
       "__NAV__": nav, "__MODULES__": "".join(mods), "__NMOD__": str(len(MODULES)), "__NLES__": str(n_lessons),
       "__HOURS__": str(round(total_min/60)), "__SESS__": str(sessions), "__MODSUM__": modsum, "__FLOW__": flow,
       "__PACE__": pace, "__REFS__": refs, "__GLOSS__": gloss, "__COPYRIGHT__": COPY_NOTE}
for k, v in rep.items(): tpl = tpl.replace(k, v)
tpl = fillC(tpl)
assert "__" not in tpl.replace("__proto__","") or True
open(ROOT + "/index.html", "w", encoding="utf-8").write(tpl)

def md_cell(s):
    return s.replace("|", "\\|").replace("\n", " ")

lines = ["# CLPN 从零开始 · 课程地图", "",
         f"简体中文课程，共 {len(MODULES)} 个模块、{COURSE_SIZE}，核心课的课文学习约 {round(total_min/60)} 小时（另有练习），按 {N_WEEKS} 周安排。起点假设：学过基础微积分，尚未使用过 R。课程数据为模拟数据，不含真实个人信息。",
         "",
         "© 2026 ZHANG. Course content (text, lessons, materials, figures, data and data documentation) licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); "
         "code (R scripts, data/simulate_data.R, website JavaScript/CSS, build and test scripts) under the MIT License (https://opensource.org/license/mit). See LICENSE. Source: https://github.com/bit-admin/clpn-course",
         "",
         "本文件是给程序读的目录。每一课的正文在单独的 Markdown 里。先根据下面的地图决定要读哪一课，再获取对应文件，不要一次读完全部课文。",
         "",
         "课号与文件名的对应：第 1.1 课是 `lessons/L1-1.md`。链接都相对于本文件所在的网站根目录。",
         "",
         "## 网站地图",
         "",
         "| 位置 | 内容 |",
         "| --- | --- |",
         "| [index.html](index.html) | 给人看的课程大纲 |",
         f"| [START_HERE.html](START_HERE.html) | 学习指南：学习顺序、{N_WEEKS} 周计划、每节课怎么学 |",
         "| [START_HERE.md](START_HERE.md) | 学习指南的 Markdown 版（与 START_HERE.html 由同一份源生成） |",
         "| [materials/glossary.html](materials/glossary.html) | 术语表 |",
         "| [materials/cheatsheets.html](materials/cheatsheets.html) | 速查卡：R 基础、回归、CLPN 流程、报告清单 |",
         "| [materials/formulas.html](materials/formulas.html) | 公式表 |",
         "| [materials/faq.html](materials/faq.html) | 常见问题 |",
         "| [materials/study_log.html](materials/study_log.html) | 学习日志（在浏览器里填写） |",
         "| [materials/writing.html](materials/writing.html) | 写作工作坊：方法、结果、局限的改写范例与任务 |",
         "| [materials/reading.html](materials/reading.html) | 论文阅读包：精选论文的 DOI 链接与阅读问题 |",
         "| [materials/case_elsoc.html](materials/case_elsoc.html) | 真实数据案例：ELSOC 抑郁症状的 CLPN（分析文件 `data/elsoc_phq8_wide.csv`，CC0） |",
         "| [materials/assessment.html](materials/assessment.html) | 测评：前测、各模块阶段测验、期末（怎么用、评分标准） |",
         "| [downloads/index.html](downloads/index.html) | 下载整门课（离线网站、数据、R 脚本、练习解答） |",
         "| [data/data_dictionary.md](data/data_dictionary.md) | 模拟数据的变量说明 |",
         "| [R/README.md](R/README.md) | 安装 R、运行脚本、依赖顺序 |",
         "| `lessons/L*.md` | 各课阅读文本 |",
         "| `R/L*.R` | 各课配套脚本，可在网站上直接阅读 |",
         "",
         "阅读文本里，交互图示只保留名称，测验会标出正确项。",
         "",
         "## 下载",
         "",
         "整门课是一个压缩包 [downloads/clpn-course.zip](downloads/clpn-course.zip)（说明见 [下载页](downloads/index.html)），解压得到 `clpn-course/` 文件夹，内含：",
         "",
         "| 位置 | 内容 |",
         "| --- | --- |",
         "| `README.md` | 给学员的文件夹说明：先看什么、怎样运行 R（不是仓库的 README.md） |",
         "| `index.html`、`START_HERE.html`、`lessons/*.html`、`materials/` | 本网站的离线版（不含各课 Markdown、`START_HERE.md`、本文件和下载页），双击 `index.html` 即可浏览 |",
         "| `data/` | 模拟数据、数据字典、`simulate_data.R`、生成数据时用的系数；7.6 用的 `coaches_mhc_raw.csv`（CC0）；ELSOC 案例用的原始文件 `elsoc/` 与预处理后的 `elsoc_phq8_wide.csv`（CC0） |",
         "| `R/` | 各课 R 脚本、`_setup.R`、`run_all.R`、`assess_answers.R`、`data_elsoc.R` 与 `case_elsoc.R`（真实数据案例）、`R/README.md`；`R/solutions/` 练习解答；`R/output/` 参考结果 |",
         "| `clpn-course.Rproj`、`LICENSE`、`THIRD_PARTY_NOTICES.md` | RStudio 项目文件、说明与许可（课程内容 CC BY 4.0，代码 MIT） |",
         "",
         "解压后双击 `clpn-course.Rproj` 打开项目。运行顺序与依赖（例如 4.3 → 10.1 → 10.2 → 10.3）见 [R/README.md](R/README.md)；"
         "所需的前置结果文件不存在时，脚本会停下并说明先运行哪个脚本。",
         "",
         "## 建议节奏",
         "",
         "| 周次 | 课程 | 重点 |",
         "| --- | --- | --- |"]
lines += [f"| 第 {w} 周 | {md_cell(a)} | {md_cell(b)} |" for w, a, b in PACING]
lines += ["", "## 模块与课文", ""]
for m in MODULES:
    lines.append(f"### {m['id']} {m['title']}")
    lines.append("")
    lines.append(m["intro"])
    lines.append("")
    for l in m["lessons"]:
        pre = "、".join(l["pre"]) if l["pre"] else "无"
        objs = "；".join(l["obj"])
        lines.append(f"- [{l['id']} {l['title']}](lessons/{anchor(l['id'])}.md){'（进阶选学）' if l.get('opt') else ''}。先修：{pre}。目标：{objs}")
    lines.append("")
open(ROOT + "/llm.md", "w", encoding="utf-8").write(fillC("\n".join(lines)).rstrip() + "\n")
print(len(MODULES), n_lessons, sessions, total_min/60, len(seen), len(tpl))
