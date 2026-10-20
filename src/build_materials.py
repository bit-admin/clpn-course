# -*- coding: utf-8 -*-
"""生成学习资料页 materials/*.html、根目录学习指南 START_HERE.html（及由它同源生成的 START_HERE.md）、materials/study_log.md。
与课件共用 lessons/assets/course.css、lesson.js 与本地 KaTeX，离线可用，可直接打印。
运行：python3 src/build_materials.py"""
import html, importlib.util, os, re
SRC = os.path.dirname(os.path.abspath(__file__))   # 内容源目录：src/（英文版镜像为 src/en/）
LANG = "en" if os.path.basename(SRC) == "en" else "zh"
REPO = os.path.dirname(os.path.dirname(SRC)) if LANG == "en" else os.path.dirname(SRC)
ROOT = REPO + "/en" if LANG == "en" else REPO       # 站点根：中文版是仓库根，英文版是 en/
D = ROOT + "/"
g = {}
for f in ["data1", "data2", "data3", "data4"]:
    exec(open(SRC + "/" + f + ".py", encoding="utf-8").read(), g)
exec(open(SRC + "/common/shell.py", encoding="utf-8").read(), g)
exec(open(SRC + "/materials/glossary_defs.py", encoding="utf-8").read(), g)
MODULES, PACING, DEFS, course_nav, COPY_NOTE = g["MODULES"], g["PACING"], g["DEFS"], g["course_nav"], g["COPY_NOTE"]
fillC = g["fillC"]   # 课程规模宏 {{C:…}}（src/data4.py）
E = html.escape
anchor = lambda i: "L" + i.replace(".", "-")
LES = {l["id"]: (m, l) for m in MODULES for l in m["lessons"]}
def L(i, txt=None): return f'<a href="../lessons/{anchor(i)}.html">{txt or (i + " " + E(LES[i][1]["title"]))}</a>'
def Ls(*ids): return "、".join(L(i, i) for i in ids)
os.makedirs(D + "materials", exist_ok=True)
os.makedirs(D + "downloads", exist_ok=True)

PAGES = [("START_HERE.html", "学习指南"), ("materials/glossary.html", "术语表"), ("materials/cheatsheets.html", "速查卡"),
         ("materials/formulas.html", "公式表"), ("materials/faq.html", "常见问题 FAQ"), ("materials/study_log.html", "学习日志"), ("materials/writing.html", "写作工作坊"), ("materials/reading.html", "论文阅读包"), ("materials/case_elsoc.html", "真实数据案例"), ("materials/assessment.html", "测评"),
         ("downloads/index.html", "下载")]

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
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} · CLPN 从零开始</title>
<link rel="stylesheet" href="{assets}/vendor/fonts/fonts.css">
{kt}<link rel="stylesheet" href="{assets}/course.css">
<script defer src="{assets}/lesson.js"></script>
<script>addEventListener("beforeprint",function(){{document.querySelectorAll("details.faq").forEach(function(d){{d.open=true}})}});</script>
</head>
<body class="matpage" style="--c:#003262">
<div class="progressline"></div>
<div class="topbar"><button id="tocBtn" type="button" aria-label="打开目录">目录</button><a class="home" href="{href("index.html")}#materials">CLPN 课程大纲</a><span class="crumb">学习资料 / {E(title)}</span><span class="sp"></span>
<a class="act langSwitch" href="{href("en/" + rel)}">English</a><button id="printBtn" type="button" onclick="window.print()">打印</button><button id="themeBtn" type="button" aria-label="切换深浅色">深色</button></div>
<div class="wrap">
<nav class="toc" aria-label="目录"><div class="toc-local"></div>{course_nav(MODULES, None, base=href("lessons") + "/", mat=href("."), docs=False)}<div class="allnav"><b>学习资料</b><ul class="matnav">{nav}</ul></div></nav>
<main>
<header class="lhero"><div class="mnum">学习资料 · Study materials</div><h1>{E(title)}</h1><div class="lead">{lead}</div></header>
{body}
<p class="foot">CLPN 从零开始 · <a href="{href("index.html")}#materials">返回大纲</a></p>
<p class="copy">{COPY_NOTE}</p>
</main></div>
</body></html>
'''
    open(os.path.join(D, rel), "w", encoding="utf-8").write(fillC(html_))

def sec(id_, h, body, cls=""): return f'<section class="sec {cls}" id="{id_}"><h2>{h}</h2>{body}</section>'


# 在自己的电脑上运行 R：下载页与学习指南共用同一段说明（pre = 页面到网站根目录的相对前缀）
def local_setup(pre):
    return f"""
<h3>1. 下载并解压</h3>
<p>从<a href="{pre}downloads/index.html">下载页</a>取得 <code>clpn-course.zip</code>，解压（Windows：右键 →“全部解压缩”；Mac：双击）。得到一个文件夹 <code>clpn-course/</code>，学习和运行 R 需要的东西都在里面：</p>
<div class="codeblk"><pre class="out"><code>clpn-course/
├── index.html             ← 课程网站的离线版：双击用浏览器打开，不需要联网
├── README.md              ← 文件夹说明（先看这个）
├── START_HERE.html        ← 学习指南
├── lessons/、materials/   ← 课件与学习资料
├── clpn-course.Rproj      ← 双击它，用 RStudio 打开课程项目
├── LICENSE、THIRD_PARTY_NOTICES.md
├── data/                  ← 模拟数据、数据字典、simulate_data.R、true_B_*.csv；7.6 练习用的真实数据 coaches_mhc_raw.csv
└── R/
    ├── README.md / .html  ← R 代码使用说明
    ├── _setup.R、run_all.R
    ├── L0-2.R、L1-1.R … L10-3.R、L2-6_report.Rmd、assess_answers.R
    ├── data_elsoc.R、case_elsoc.R   ← 真实数据案例（预处理、CLPN）
    ├── solutions/         ← 练习解答
    └── output/            ← 参考结果（网页上的图、日志）；运行脚本会用你的结果覆盖</code></pre></div>
<p>请先解压再使用，不要在压缩包的预览窗口里直接打开文件。路径里最好不要有中文和空格（例如放在 <code>D:\\clpn-course</code>）。从 GitHub 获取整个仓库的，仓库根目录就是同样的课程文件夹。</p>
<h3>2. 打开项目</h3>
<ol>
<li>按 <a href="{pre}R/README.html">R 代码使用说明</a> 安装 R 和 RStudio（先装 R，再装 RStudio）。</li>
<li>双击 <code>clpn-course/clpn-course.Rproj</code>。RStudio 以“项目”方式打开，工作目录就是 <code>clpn-course</code> 文件夹。每个脚本第一行的 <code>source("R/_setup.R")</code> 都依赖这一点：不要直接双击 <code>.R</code> 文件打开。</li>
<li>打开 <code>R/L2-4.R</code> 点 Source，安装课程需要的包（只需一次）。</li>
<li>打开 <code>R/L1-1.R</code>，逐行运行（Ctrl/Cmd + Enter），确认能看到输出。之后每节课打开对应的 <code>R/Lx-y.R</code>（0.1 课和 9.1 课没有脚本）。</li>
</ol>
<h3>3. 运行顺序与依赖</h3>
<p>按课号顺序运行即可。下面这些脚本要读取前面脚本在 <code>R/output/</code> 生成的文件。压缩包里的 <code>R/output/</code> 已带有参考结果，所以直接运行也能读到；但如果你修改并重新运行了前置脚本，后面的脚本就会用你的新结果。如果需要的文件不存在（例如删掉了 <code>R/output/</code>），脚本会在开头停下，并告诉你先运行哪个脚本。</p>
<div class="tablewrap"><table><tr><th>脚本</th><th>需要先运行</th></tr>
<tr><td><code>L6-5.R</code>、<code>solutions/L6-4_solution.R</code>、<code>solutions/L6-5_solution.R</code></td><td><code>L6-4.R</code></td></tr>
<tr><td><code>L10-1.R</code> → <code>L10-2.R</code> → <code>L10-3.R</code></td><td>依次：<code>L4-3.R</code> → <code>L10-1.R</code> → <code>L10-2.R</code> → <code>L10-3.R</code>（每一步都需要上一步的结果）</td></tr>
<tr><td><code>solutions/L8-3_solution.R</code></td><td><code>L8-2.R</code>（读 <code>L8-2_boot.rds</code>）和 <code>L8-3.R</code></td></tr>
<tr><td><code>case_elsoc.R</code></td><td>随课程提供的 <code>data/elsoc_phq8_wide.csv</code>（由 <code>data_elsoc.R</code> 从随课程提供的原始文件写出）</td></tr>
<tr><td>其余脚本</td><td>无</td></tr>
</table></div>
<p><b>一次运行全部</b>：<code>source("R/run_all.R")</code>。它按课号运行全部课文脚本和期末答案脚本，再运行全部答案脚本（<code>R/solutions/</code>）。约 40–95 分钟（视电脑而定），大部分时间是 L8-2、L8-3、L10-2 的 bootstrap；结果汇总在 <code>R/output/run_all_status.csv</code>。其中也包括真实数据案例的 <code>data_elsoc.R</code> 和 <code>case_elsoc.R</code>。</p>
<p>bootstrap 默认<b>单核</b>运行（<code>nCores = 1</code>）、固定种子，在同一 R / 包版本下结果逐位可重复，与网页上的数字一致。改成并行会快几倍，但结果不再可重复：区间端点一般只在小数点后两三位上变化，CS 系数却可能整档跳动（课程数据的 in-EI 会在 0.44 和 0.52 之间变化，正好跨过 0.5 的参考线）。</p>"""

# =====================================================================  学习指南
hours = round(sum(l["time"] for m in MODULES for l in m["lessons"] if not l.get("opt")) / 60)   # 只算核心课，与 index.html、llm.md 同口径（选学课 opt=True 不计课时）
modrows = "".join(f'<tr><td><b>{m["id"]}</b></td><td>{E(m["title"])}<br><span class="muted">{E(m["en"])}</span></td><td>{len(m["lessons"])}</td><td>{" ".join(L(l["id"], l["id"]) for l in m["lessons"])}</td></tr>' for m in MODULES)
pace = "".join(f'<tr><td>第 {w} 周</td><td>{E(a)}</td><td>{E(b)}</td></tr>' for w, a, b in PACING)
guide = sec("site", "一、这个网站上有什么", r"""
<p>课程在浏览器里学。下表是站上的页面。整个网站连同数据、R 脚本和练习解答可以打包下载：从 <a href="downloads/index.html">下载页</a>取得 <code>clpn-course.zip</code>，解压后双击 <code>index.html</code> 就能离线学习，运行 R 见下面第五节。</p>
<div class="tablewrap"><table><tr><th>页面</th><th>是什么</th><th>什么时候用</th></tr>
<tr><td><a href="index.html">课程大纲</a></td><td>11 个模块、全部课程的目标、概念、练习，带进度勾选</td><td>每次学习的起点</td></tr>
<tr><td>课件</td><td>{{C:size}}，都是交互课件（直觉 → 数学 → R 代码 → 测验 → 练习 → 小结）。从大纲点「学习 1.1」这类链接进入</td><td>每节课的主体</td></tr>
<tr><td>学习资料</td><td>本指南、<a href="materials/glossary.html">术语表</a>、<a href="materials/cheatsheets.html">速查卡</a>、<a href="materials/formulas.html">公式表</a>、<a href="materials/faq.html">常见问题</a>、<a href="materials/study_log.html">学习日志</a></td><td>随时查阅</td></tr>
<tr><td><a href="downloads/index.html">下载</a></td><td>整门课的压缩包：离线网站、数据、R 脚本、练习解答</td><td>要离线学习或在自己的电脑上运行 R 时</td></tr>
<tr><td><a href="materials/writing.html">写作工作坊</a>、<a href="materials/reading.html">论文阅读包</a></td><td>方法、结果、局限的改写范例；精选论文与阅读问题</td><td>学 9.3 和 10.3 时；写毕业项目论文时</td></tr>
<tr><td><a href="materials/case_elsoc.html">真实数据案例</a></td><td>ELSOC 抑郁症状（PHQ-8）的 CLPN。分析文件随课程提供</td><td>学完 7.4 和 8.2 之后；写毕业项目时对照</td></tr>
<tr><td><a href="materials/assessment.html">测评</a></td><td>前测、每个模块的阶段测验、期末考试，附评分标准</td><td>开学前、每学完一个模块、学完 10.3 后</td></tr>
<tr><td><a href="R/README.html">R 代码使用说明</a></td><td>安装 R 和 RStudio、打开项目、运行脚本</td><td>学到 R 代码时</td></tr>
<tr><td><a href="data/data_dictionary.html">数据字典</a></td><td>模拟的 N = 800、三波“孤独—抑郁”数据，每个变量的含义</td><td>做练习时对照</td></tr>
</table></div>
<p>进度（“标记本课为已完成”）保存在浏览器里，换浏览器或清除缓存会丢失，重要的学习记录请写进学习日志。</p>""")
guide += sec("order", "二、按什么顺序学", r"""
<p>模块编号代表知识的逻辑顺序：M0 总览 → M1 统计基础 → M2 R 编程 → M3 回归与正则化 → M4 纵向数据 → M5 CLPM → M6 网络心理测量 → M7 CLPN → M8 稳定性 → M9 批判阅读与报告 → M10 毕业项目。实际学习时，<b>M1 统计和 M2 R 并排学（第 2–5 周交替进行），M3 回归在它们之后</b>：学完一个统计概念，马上在 R 里做一遍。每节课页面顶部都列出了先修课，可以点击跳转。</p>
<div class="tablewrap"><table><tr><th>模块</th><th>主题</th><th>课数</th><th>课程</th></tr>""" + modrows + r"""</table></div>""")
guide += sec("lesson", "三、每节课怎么学（约 2–3 小时）", r"""
<ol><li><b>读目标（2 分钟）：</b>看“本课学习目标”和“核心概念”。不认识的词先查<a href="materials/glossary.html">术语表</a>。</li>
<li><b>① 直觉（20–30 分钟）：</b>不要跳过。先在脑子里形成画面，再看公式。交互组件一定要动手拖一拖。</li>
<li><b>② 最少数学（15–30 分钟）：</b>拿纸笔跟着算一遍“完整例题”。公式汇总在<a href="materials/formulas.html">公式表</a>。</li>
<li><b>③ R 代码（30–60 分钟）：</b>双击 <code>clpn-course.Rproj</code> 打开 RStudio 项目，打开对应的 <code>R/Lx-y.R</code>，<b>逐行运行</b>（Ctrl/Cmd + Enter），把输出和网页上的输出对照。页面底部可以展开完整脚本。</li>
<li><b>④ 即时测验（10 分钟）：</b>答错会先给提示，答错两次才显示答案。</li>
<li><b>⑤ 练习（1–2 小时）：</b>自己先做，再看参考答案；需要写代码的练习，答案在 <code>R/solutions/</code>。写作类练习对照课文给出的评分要点逐条自评，改一遍再存档。每课的练习脚本和输出建议整理在同一个文件夹里，毕业项目时还会用到。</li>
<li><b>小结与日志（10 分钟）：</b>点“标记本课为已完成”，在<a href="materials/study_log.html">学习日志</a>里写下三句话：学到了什么、哪里还不懂、下一步想弄清什么。</li></ol>
<div class="box key"><b class="bt">卡住了怎么办？</b><p>①先看本课的“常见错误”和“常见问题与误区”；②查 <a href="materials/faq.html">FAQ</a>；③R 报错时，把报错的最后一行复制到搜索引擎；④仍然不行，按 """ + L("2.1", "2.1 课") + r""" 的“最小可复现例子”格式整理好，到同学、同事或 R 社区论坛（如 Posit Community、Stack Overflow）提问。卡住超过 30 分钟就该换个办法，不要硬耗。整理最小例子的过程中，常常就已经找到了原因。</p></div>""")
guide += sec("plan", "四、{{C:weeks}} 周周计划", r"""
<p><b>标准节奏：{{C:weeks}} 周，每周学 3 次</b>（第 14、15 周各 4 次），每次 60–150 分钟，另加每周 2–3 小时练习，合计每周约 5–7 小时；核心课的课文学习共约 """ + str(hours) + r""" 小时（不含选学课和练习）。假期集中学习可压缩到约 12 周（每周学 4 次）；与学期课程同时进行可放宽到约 19 周（在第 5、8、13 周后各加一个缓冲周）。进阶选学课 {{C:optlist}} 不在标准节奏里：学有余力时在第 13 周之后自学，宽松版放在第 13 周后的缓冲周，压缩版不含。</p>
<div class="tablewrap"><table><tr><th>周次</th><th>课程</th><th>重点</th></tr>""" + pace + r"""</table></div>
<p class="muted">每周结束时：在学习日志中写周小结；把本周的练习脚本和输出归档；用大纲页的进度条检查是否跟上计划。</p>""")
guide += sec("r", "五、在自己的电脑上运行 R", local_setup(""))
guide += sec("progress", "六、进度与自查", r"""
<ul><li>每周固定留出 30 分钟回顾：重读学习日志里“还不懂的地方”一栏，能自己解决的划掉，解决不了的写清楚卡在哪一步，带进下一周。</li>
<li>练习的结果保存为脚本加输出（或一份 Quarto 报告），不要只留截图。几周后回头核对，或者在毕业项目里复用代码，都要靠它。</li>
<li>写作类练习（解读段落、审稿意见、方法与结果）先写，再对照课文和<a href="materials/writing.html">写作工作坊</a>的评分要点逐条打分，改一遍。能找到同学或同事互相读一遍更好：请对方指出哪一句读起来像因果结论。</li>
<li>第 5 周和第 8 周做阶段测验（M1 + M2、M3 + M4），第 15–16 周是毕业项目（""" + Ls("10.1", "10.2", "10.3") + r"""）。项目开始前，先写好一页分析计划并存档（带日期）；正式分析之后如有改动，在报告里逐条说明改了什么、为什么改。</li></ul>""")
guide += sec("assess", "七、测评：前测、阶段测验与期末", r"""
<ul><li><b>开始之前</b>：做一次<a href="materials/assess_pre.html">前测</a>（约 20 分钟，不计分）。它会建议你走 {{C:weeks}} 周标准节奏，还是在第 5、8、13 周后各加一个缓冲周的 19 周节奏。</li>
<li><b>每学完一个模块</b>：做这个模块的阶段测验（15–25 分钟）。一次答对 70% 及以上就继续；不到 70% 的，按错题解释里的链接回去复习。</li>
<li><b>学完 10.3</b>：做期末考试（约 90 分钟），和前测对照，看看自己进步了多少。</li>
<li>每次的“一次答对”题数记进<a href="materials/study_log.html">学习日志</a>。评分标准见<a href="materials/assessment.html">测评总页</a>。</li></ul>""")
guide = guide.replace('href="../lessons/', 'href="lessons/')
page("START_HERE.html", "学习指南：怎样使用这门课", "<p>这一页说明怎样在网站上学习：站上有什么、按什么顺序学、每节课怎么学、{{C:weeks}} 周怎么安排。Markdown 版：<a href=\"START_HERE.md\" download><code>START_HERE.md</code></a>（内容相同）。</p>", guide, rel="START_HERE.html")

# =====================================================================  术语表
seen = {}
for m in MODULES:
    for l in m["lessons"]:
        for z, e in l["con"]:
            if z not in seen: seen[z] = (e, l["id"], m)
gl = ""
for m in MODULES:
    rows = [(z, e, i) for z, (e, i, mm) in seen.items() if mm is m]
    if not rows: continue
    gl += sec("g-" + m["id"], f'{m["id"]} {E(m["title"])}', '<div class="tablewrap"><table class="gloss"><tr><th>中文</th><th>English</th><th>一句话释义</th><th>正式讲解</th></tr>' +
              "".join(f'<tr><td><b>{E(z)}</b></td><td>{E(e)}</td><td>{E(DEFS[z])}</td><td>{L(i, i)}</td></tr>' for z, e, i in rows) + "</table></div>")
gsearch = '<div class="card glsearch"><label>查找术语（中文或英文）：<input id="glq" type="search" placeholder="例如：偏相关 / bootstrap"></label> <span class="muted" id="gln"></span></div>' \
          '<script>document.addEventListener("DOMContentLoaded",function(){var q=document.getElementById("glq"),n=document.getElementById("gln");if(!q)return;q.addEventListener("input",function(){var v=q.value.trim().toLowerCase(),k=0;document.querySelectorAll("table.gloss tr").forEach(function(tr){if(!tr.querySelector("td"))return;var on=!v||tr.textContent.toLowerCase().indexOf(v)>=0;tr.style.display=on?"":"none";if(on)k++;});n.textContent=v?("找到 "+k+" 条"):"";});});</script>'
page("glossary.html", "中英双语术语表", f"<p>全课程 {len(seen)} 个核心术语，按模块排列，附一句话释义和正式讲解该术语的课（点击可跳转；有些术语在此之前已作为预告出现过）。打印时自动去掉导航栏，适合打印成小册子放在手边。</p>", gsearch + gl)

# =====================================================================  速查卡
def card(id_, title, body): return f'<section class="sec cheat" id="{id_}"><h2>{title}</h2>{body}</section>'
def tbl(head, rows): return '<div class="tablewrap"><table><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table></div>"
C = lambda s: f"<code>{E(s)}</code>"
cs = card("r", "速查卡 1 · R 基础", tbl(["想做什么", "代码", "备注"], [
["赋值 / 查看", C("x <- c(3, 5, 4); x"), "R 区分大小写；中文只写在引号里"],
["均值 / 标准差 / 有缺失时", C("mean(x); sd(x); mean(x, na.rm = TRUE)"), "sd() 用 n − 1"],
["读数据 / 看结构", C('dat <- read.csv("data/clpn_sim_wide.csv"); str(dat)'), "路径相对于项目文件夹"],
["行数列数 / 前几行 / 概要", C("dim(dat); head(dat); summary(dat)"), "导入后先体检（2.4 课）"],
["取一列 / 取行", C('dat$age; dat[dat$gender == 1, ]'), "比较用 ==，不是 ="],
["数缺失", C("colSums(is.na(dat))"), "不要写 x == NA"],
["按行求和（总分）", C("rowSums(dat[, paste0(lone_items, \"_t1\")])"), "mutate 里不要用 sum()"],
["dplyr 管道", C("dat |> filter(age >= 60) |> group_by(gender) |> summarise(M = mean(age))"), "结果记得赋值"],
["宽 → 长", C('pivot_longer(dat, cols = matches("^(lone|dep)\\\\d_t\\\\d$"), names_to = c(".value", "wave"), names_sep = "_t")'), "只转 9 道题目的列；gender、age 等其他列原样保留。行数 = 人数 × 波数"],
["相关 / 相关矩阵", C("cor(x, y); round(cor(d), 2)"), "缺失：use = \"pairwise.complete.obs\""],
["回归 / 结果 / 区间", C("fit <- lm(y ~ x1 + x2, data = d); summary(fit); confint(fit)"), "逻辑回归：glm(..., family = binomial)"],
["标准化", C("scale(x)[, 1]"), "scale() 返回矩阵"],
["画图", C("ggplot(d, aes(x, y)) + geom_point()"), "+ 放在行末"],
["保存图", C('ggsave("R/output/fig.png", width = 12, height = 9, units = "cm", dpi = 300)'), ""],
["随机种子 / 版本", C("set.seed(2026); sessionInfo()"), "写进方法部分"],
["求助", C("?cor; example(cor)"), "先看 Usage 和 Examples"]]) +
'<p class="muted">三条最常见的报错：<b>object not found</b>（没创建或拼错）· <b>could not find function</b>（拼错或没 library）· <b>unexpected symbol / input</b>（中文标点、括号不配对）。详见 ' + L("2.1", "2.1 课") + "。</p>")
cs += card("reg", "速查卡 2 · 回归结果怎么读", tbl(["输出中的项", "含义", "报告写法"], [
["Estimate（b）", "其他预测变量不变时，x 每高 1 个单位，y 平均高 b", "b = 0.32"],
["Std.all / β", "标准化系数：x 高 1 SD，y 平均高 β SD", "β = .25（APA：不超过 1 的统计量去掉小数点前的 0；中文期刊常写 0.25，全文一致即可）"],
["Std. Error", "b 的抽样不确定性", "通常放在表里"],
["t value = b / SE", "离 0 有几个标准误", "t(797) = 7.82"],
["Pr(>|t|)", "假如零假设 b = 0 成立，得到与当前结果一样极端或更极端结果的概率", "p &lt; .001（不写 p = 0）"],
["confint()", "95% 置信区间；不含 0 ⇔ p &lt; .05", "95% CI [0.24, 0.40]"],
["R² / 调整 R²", "模型解释的结果变异比例", "R² = .10"],
["glm 的 Estimate", "log-odds；exp() 后为 OR", "OR = 1.65，95% CI [...]"],
["OR", "x 高 1 单位，几率乘以 OR（不是概率）", "几率增加 (OR − 1) × 100%"]]) +
'<div class="box key"><b class="bt">一句话模板</b><p>“控制<u>协变量</u>后，<u>预测变量</u>正向 / 负向预测<u>结果</u>（b = __，95% CI [__, __]，p = __）；模型解释了<u>结果</u> __% 的变异。”</p></div>'
'<div class="box warnbox"><b class="bt">五个别犯的错</b><ul><li>把 b 说成因果（“导致”“使得”）。</li><li>p &gt; .05 写成“没有关系”。</li><li>用 β 跨样本比较。</li><li>相关显著、回归不显著不是矛盾，而是“控制”的结果（' + L("2.5", "2.5") + '）。</li><li>OR 当作风险比。</li></ul></div>')
cs += card("pipe", "速查卡 3 · CLPN 分析流程", tbl(["步骤", "做什么", "关键代码 / 文件", "课"], [
["0 计划", "研究问题、节点、λ 规则、种子、稳定性标准写进分析计划", C("R/output/L10-1_analysis_plan.md"), Ls("10.1")],
["1 数据", "导入、检查范围与缺失、流失分析；按 id 对齐 T1 / T2", C("read.csv(); colSums(is.na())"), Ls("2.4", "4.2", "4.3")],
["2 描述", "均值、SD、偏度；题目相关", C("psych::describe()"), Ls("2.5")],
["3 冗余检查", "内容高度重叠的题目", C("networktools::goldbricker()"), Ls("9.2")],
["4 估计", "每个 T2 节点做一次 LASSO 回归，题目先标准化，10 折 CV", C("set.seed(2026); B <- clpn_estimate(X, Y, rule = \"lambda.min\")"), Ls("7.2")],
["5 作图", "有向图；自回归不画或画成环；固定 maximum", C("qgraph(cl_only(B), directed = TRUE)"), Ls("7.3")],
["6 中心性", "出 / 入 EI、桥接 EI，不含自回归", C("rowSums(cl_only(B)); colSums(cl_only(B))"), Ls("7.4")],
["7 准确性", "非参数 bootstrap 边权区间（B ≥ 1000）", C("bootnet(..., fun = 自定义估计函数)"), Ls("8.2")],
["8 稳定性", "个案删除 bootstrap，CS ≥ 0.25 才解释排序", C("corStability()"), Ls("8.3")],
["9 敏感性", "lambda.1se、加协变量、T2 → T3 复现", C("clpn_estimate(..., covariates = )"), Ls("7.5", "9.2")],
["10 报告", "方法写全每个设置；每个数字可追溯到输出文件", C("sessionInfo()"), Ls("9.3", "10.3")]]) +
'<div class="box story"><b class="bt">三条底线</b><ul><li>CLPN 的边是<b>时间上的预测</b>，不是因果。</li><li>标准 CLPN 混合了被试间与被试内效应（' + L("5.3", "5.3") + "、" + L("7.5", "7.5") + '）。</li><li>没有稳定性检验的中心性排序不能解释。</li></ul></div>')
cs += card("report", "速查卡 4 · 报告检查表", '<p class="muted">基于课程 ' + L("9.3", "9.3 课") + '（参考 Burger 等人 2023 的网络分析报告规范）。逐项核对：</p><ul class="checklist">' + "".join(f"<li>[ ] {x}</li>" for x in [
"<b>样本</b>：N、招募方式、各波人数与流失率、流失分析结果", "<b>设计</b>：波数、时间间隔，以及为何选择这个间隔",
"<b>节点</b>：题目全文或简称、来源量表、为何选这些节点；冗余检查（goldbricker）", "<b>缺失处理</b>：方法（列表删除 / 插补 / FIML）及理由",
"<b>预处理</b>：是否标准化；定序题目的处理", "<b>估计</b>：软件与版本（R、glmnet、bootnet）；逐节点 LASSO；λ 规则（lambda.min / 1se）；CV 折数；随机种子",
"<b>协变量</b>：有哪些、是否惩罚（penalty.factor = 0）", "<b>中心性</b>：指标名称；是否含自回归；桥接的社群划分",
"<b>准确性</b>：bootstrap 类型与次数；边权区间图", "<b>稳定性</b>：case-dropping 次数；CS 系数与判断标准（0.7 / 95% / 0.25）",
"<b>敏感性分析</b>：做了哪些、主要结论是否保持", "<b>图</b>：图注说明颜色、粗细（maximum）、阈值、布局；自回归如何呈现",
"<b>表</b>：完整 B 矩阵（可放补充材料）；非零交叉滞后边表", "<b>措辞</b>：用“预测”而非“导致 / 驱动”；不把单题写成构念",
"<b>局限</b>：被试间 / 被试内混合、未测量混杂、间隔、样本代表性", "<b>开放</b>：代码与（模拟或可共享的）数据；预注册（如有）"]) + "</ul>")
page("cheatsheets.html", "一页速查卡", "<p>四张速查卡：<a href=\"#r\">R 基础</a> · <a href=\"#reg\">回归结果怎么读</a> · <a href=\"#pipe\">CLPN 分析流程</a> · <a href=\"#report\">报告检查表</a>。打印时每张卡单独一页。</p>", cs)

# =====================================================================  公式表
def F(name, tex, note, les): return f'<tr><td><b>{name}</b></td><td>\\(\\displaystyle {tex}\\)</td><td>{note}</td><td>{Ls(*les)}</td></tr>'
def ftab(rows): return '<div class="tablewrap"><table class="ftab"><tr><th>名称</th><th>公式</th><th>说明</th><th>课</th></tr>' + "".join(rows) + "</table></div>"
fm = sec("f1", "描述统计与推断", ftab([
F("均值", r"\bar x=\frac{1}{n}\sum_{i=1}^{n}x_i", "", ["1.2"]),
F("样本方差 / 标准差", r"s^2=\frac{1}{n-1}\sum_{i}(x_i-\bar x)^2,\quad s=\sqrt{s^2}", "R 的 var()、sd()", ["1.2"]),
F("z 分数", r"z_i=\frac{x_i-\bar x}{s}", "均值 0、SD 1", ["1.3"]),
F("协方差", r"\operatorname{cov}(x,y)=\frac{1}{n-1}\sum_i(x_i-\bar x)(y_i-\bar y)", "", ["1.4"]),
F("皮尔逊相关", r"r=\frac{\operatorname{cov}(x,y)}{s_x s_y}", "−1 ≤ r ≤ 1", ["1.4"]),
F("均值的标准误", r"SE_{\bar x}=\frac{s}{\sqrt n}", "n 变 4 倍，SE 减半", ["1.5"]),
F("95% 置信区间", r"\bar x\pm1.96\times SE", "大样本近似", ["1.5"]),
F("独立样本 t", r"t=\frac{\bar x_1-\bar x_2}{s_p\sqrt{1/n_1+1/n_2}}", "", ["1.6"]),
F("Cohen's d", r"d=\frac{\bar x_1-\bar x_2}{s_p}", "0.2 / 0.5 / 0.8", ["1.6"]),
F("多重比较的期望假阳性", r"E[\text{假阳性}]=m\times\alpha", "190 × 0.05 = 9.5", ["1.6"])]))
fm += sec("f2", "回归与正则化", ftab([
F("简单回归", r"\hat y=b_0+b_1x,\quad b_1=\frac{\operatorname{cov}(x,y)}{s_x^2},\quad b_0=\bar y-b_1\bar x", "最小二乘", ["3.1"]),
F("决定系数", r"R^2=1-\frac{\sum(y_i-\hat y_i)^2}{\sum(y_i-\bar y)^2}", "简单回归中 R² = r²", ["3.1"]),
F("多元回归", r"y=b_0+b_1x_1+\dots+b_kx_k+e", "", ["3.2"]),
F("VIF", r"\mathrm{VIF}_j=\frac{1}{1-R_j^2}", "&gt; 5–10 提示共线性", ["3.2"]),
F("标准化系数", r"\beta=b\,\frac{s_x}{s_y}", "", ["3.3"]),
F("逻辑回归", r"\operatorname{logit}(p)=\ln\frac{p}{1-p}=b_0+b_1x", r"\(p=1/(1+e^{-\text{logit}})\)", ["3.4"]),
F("几率比", r"\mathrm{OR}=e^{b_1}", "", ["3.4"]),
F("岭回归", r"\min_b\ \frac{1}{2n}\sum_i(y_i-x_i^\top b)^2+\lambda\cdot\frac{1}{2}\sum_j b_j^2", "glmnet 中 α = 0；按 glmnet 的约定，岭惩罚带 1/2 系数", ["3.5"]),
F("LASSO", r"\min_b\ \frac{1}{2n}\sum_i(y_i-x_i^\top b)^2+\lambda\sum_j|b_j|", "glmnet 中 α = 1", ["3.5", "7.2"]),
F("软阈值（正交时）", r"\hat\beta_j=\operatorname{sign}(\hat\beta_j^{OLS})\max(|\hat\beta_j^{OLS}|-\lambda,0)", "", ["6.3"])]))
fm += sec("f3", "纵向模型", ftab([
F("ICC", r"ICC=\frac{\sigma^2_{\text{between}}}{\sigma^2_{\text{between}}+\sigma^2_{\text{within}}}", "", ["4.1"]),
F("Rubin 合并（点估计）", r"\bar Q=\frac1m\sum_{l=1}^m\hat Q_l", "多重插补", ["4.3"]),
F("Rubin 合并（方差）", r"T=\bar U+\left(1+\frac1m\right)B", "组内 + 组间方差", ["4.3"]),
F("CLPM", r"L_{t+1}=a_LL_t+c\,D_t+e,\quad D_{t+1}=a_DD_t+d\,L_t+e", "a 自回归，c、d 交叉滞后", ["5.1"]),
F("RI-CLPM 分解", r"x_{it}=\mu_t+RI_i+w_{it}", "动态模型建在 w 上", ["5.3"]),
F("间隔 Δ 的交叉效应", r"A=\begin{pmatrix}a&0\\c&a\end{pmatrix}\ \Rightarrow\ (A^{\Delta})_{21}=\Delta\,a^{\Delta-1}c", "假设：每单位时间两变量自回归同为 a，只有单向交叉效应 c（L → D），x<sub>t+1</sub> = A x<sub>t</sub>；先升后降", ["5.4"])]))
fm += sec("f4", "网络与 CLPN", ftab([
F("偏相关（3 变量）", r"r_{xy\cdot z}=\frac{r_{xy}-r_{xz}r_{yz}}{\sqrt{(1-r_{xz}^2)(1-r_{yz}^2)}}", "", ["6.2"]),
F("由精度矩阵得偏相关", r"K=\Sigma^{-1},\quad\rho_{ij}=-\frac{k_{ij}}{\sqrt{k_{ii}k_{jj}}}", "注意负号", ["6.2"]),
F("graphical lasso", r"\max_K\ \log\det K-\operatorname{tr}(SK)-\lambda\sum_{i\ne j}|k_{ij}|", "", ["6.3"]),
F("EBIC（图模型）", r"\mathrm{EBIC}=-2\ell+E\ln N+4\gamma E\ln p", "EBICglasso 用：E 为边数，p 为节点数，γ 常取 0.5", ["6.3"]),
F("EBIC（逐节点回归）", r"\mathrm{EBIC}_j=N\ln(\mathrm{RSS}_j/N)+k_j\ln N+2\gamma k_j\ln p", "<code>clpn_estimate(rule = \"ebic\")</code> 用：k<sub>j</sub> 为第 j 个回归的非零系数个数，p 为预测变量数", ["7.2", "9.2"]),
F("强度 / 期望影响", r"S_i=\sum_{j}|w_{ij}|,\quad EI_i=\sum_j w_{ij}", "", ["6.5"]),
F("CLPN 逐节点回归", r"z(y_{j,t+1})=\sum_{k=1}^{p}B_{kj}\,z(y_{k,t})+e_j", "B[k, j]：k → j", ["7.1", "7.2"]),
F("出 / 入 EI", r"\text{outEI}_k=\sum_{j\ne k}B_{kj},\quad\text{inEI}_j=\sum_{k\ne j}B_{kj}", "两者总和相等", ["7.4"]),
F("桥接出 EI", r"\text{bridgeOutEI}_k=\sum_{j\notin C(k)}B_{kj}", "C(k)：k 所在社群", ["7.4"])]))
fm += sec("f5", "Bootstrap 与稳定性", ftab([
F("百分位区间", r"[\hat\theta^*_{(0.025)},\ \hat\theta^*_{(0.975)}]", "B ≥ 1000", ["8.1"]),
F("bootstrap 标准误", r"SE^*=\operatorname{sd}(\hat\theta^*_1,\dots,\hat\theta^*_B)", "", ["8.1"]),
F("区间宽度与样本量", r"\text{宽度}\propto1/\sqrt N", "", ["8.1"]),
F("CS 系数", r"CS=\max\{q:\ P(\operatorname{cor}(\hat c_{\text{原}},\hat c_{\text{删}q})\ge0.7)\ge0.95\}", "≥ 0.25 可解释，≥ 0.5 较好", ["8.3"])]))
page("formulas.html", "公式表", "<p>全课程用到的公式，一页汇总。每个公式都注明出处课程，点击可回到讲解。符号：n / N 为样本量，p 为节点数，λ 为惩罚强度，B 为 CLPN 系数矩阵。</p>", fm, math=True)

# =====================================================================  FAQ
FAQ = [
("学习与使用", [
("我完全没学过统计和编程，真的能学会吗？", "能。课程从均值和“什么是变量”讲起（" + L("1.1", "1.1") + "），R 从安装讲起（" + L("2.1", "2.1") + "）。关键是按顺序学、每节课都动手跑代码，每周保持 5–7 小时。"),
("一定要按顺序学吗？", "建议按 <a href=\"../START_HERE.html#plan\">{{C:weeks}} 周计划</a> 学。每节课页面顶部列出了先修课；已经掌握的内容可以只做测验，测验全对再跳过。"),
("进度为什么不见了？", "“已完成”标记保存在浏览器的本地存储里，换浏览器、无痕模式或清除缓存都会丢失。重要的记录请写进<a href=\"study_log.html\">学习日志</a>。"),
("练习答案在哪里？", "每节课的练习都有可展开的参考答案。需要写代码的练习，完整答案在 <code>R/solutions/</code>，包含在<a href=\"../downloads/index.html\">下载页</a>的课程压缩包里。运行结果在 <code>R/output/sol_*_log.txt</code>。")]),
("R 与软件", [
("安装包时报错怎么办？", "先确认网络正常，并在 RStudio 中把 CRAN 镜像设为国内镜像（Tools → Global Options → Packages）。Windows 用户名或路径中有中文时容易出错，建议把课程放在 <code>D:\\clpn-course\\</code> 这样的路径下。详见 <a href=\"../R/README.html\">R 代码使用说明</a>。"),
("为什么我运行的数字和网页上不完全一样？", "大多数脚本设置了随机种子，结果应该完全一致。bootstrap 相关的脚本（8.2、8.3、10.2）默认单核运行，固定种子后结果也完全一致；如果你把 nCores 改成大于 1（并行），种子不能控制各子进程，每次运行的结果都会不同。边权重区间的端点通常只在小数点后两三位上变化，但 CS 系数不是连续变化的：它只能取删除比例网格上的值（相邻两档相差约 0.08），所以可能整档跳动。课程数据的 in-EI 就会在 0.44 和 0.52 之间跳，一次在 0.5 以上、一次在 0.5 以下，判断结论随之改变。需要报告的结果请用单核、固定种子运行。另外，R 或软件包版本不同也可能带来细微差异。"),
("中文显示成方框或乱码？", "图中的中文：<code>_setup.R</code> 会尝试设置中文字体；如果仍有问题，见 " + L("2.6", "2.6") + " 的常见错误。读入的中文乱码：多半是 GBK 编码，见 " + L("2.4", "2.4") + "。"),
("Quarto 和 R Markdown 用哪个？", "都可以。课程示例用 Quarto（<code>R/solutions/week06.qmd</code>）；如果没有安装 Quarto，同样的内容可以改为 .Rmd 文件，用 rmarkdown 渲染。"),
("_setup.R 里有什么？", "找到课程根目录、设置输出文件夹和中文字体、定义题目名称和常用函数（<code>clpn_estimate()</code>、<code>cl_only()</code>、<code>edge_list()</code> 等）。值得读一遍，但不需要修改。")]),
("统计概念", [
("p 值到底是什么？", "假如零假设为真，看到当前或更极端数据的概率。它不是“零假设为真的概率”，也不衡量效应大小。见 " + L("1.6", "1.6") + "。"),
("相关显著但回归不显著，是不是算错了？", "不是。回归系数是控制其他变量后的“独特”关联，与相关回答的是不同的问题。课程数据中的社会支持就是一个例子（" + L("2.5", "2.5") + "）。"),
("为什么要用 LASSO，不用普通回归？", "节点多时普通回归会有大量“碰巧不为 0”的小系数（过拟合、假阳性）。LASSO 把小系数压成 0，得到更稀疏、更易解释的网络。代价是保留下来的系数偏小。见 " + L("3.5", "3.5") + "、" + L("6.3", "6.3") + "。"),
("lambda.min 和 lambda.1se 选哪个？", "lambda.min 预测误差最小、边更多；lambda.1se 更保守、边更少。事先在分析计划中选定一个作为主分析（本课程用 lambda.min），另一个作为敏感性分析。见 " + L("7.2", "7.2") + "。"),
("被试间和被试内有什么区别？", "被试间：比别人更孤独的人是否也更抑郁；被试内：比自己平时更孤独的时候，之后是否更抑郁。标准 CLPM / CLPN 把两者混在一起。见 " + L("4.1", "4.1") + "、" + L("5.3", "5.3") + "。")]),
("CLPN 方法", [
("CLPN 的边能说明因果吗？", "不能直接说明。边是“控制所有 T1 节点后的时间预测”，可能受稳定特质、未测量混杂和间隔选择的影响。写作中用“预测”“与……一致”，不用“导致”“驱动”。见 " + L("5.4", "5.4") + "。"),
("至少需要多少样本？", "没有公认的“N 至少是节点数的几倍”这类硬性规则。N/p（样本量 ÷ 节点数）只是快速核算用的粗略指标：它越小，每个逐节点回归的信息越少，网络越稀疏、越不稳定。9 个节点就有 81 个系数；课程数据 N/p = 800/9 ≈ 89。真正需要多大样本，取决于假定的真实网络（边有多强、有多少条）和你要回答的问题，要用模拟来回答：Constantin、Schuurman 与 Vermunt（2026）给出了网络模型样本量规划的一般蒙特卡罗方法，" + L("7.6", "7.6") + " 课做了一个简化版。数据收集完之后，再用 bootstrap 和 CS 检查稳定性，见 " + L("8.2", "8.2") + "、" + L("8.3", "8.3") + "。"),
("只有两波数据可以做 CLPN 吗？", "可以估计 T1 → T2 网络，但无法在另一时间段检验复现，也无法用 RI-CLPM 分离稳定特质（至少需要 3 波）。局限部分要写明。"),
("中心性排序第一的节点就是干预靶点吗？", "不是。需要先确认 CS ≥ 0.25（最好 ≥ 0.5）、与第二名的差异经 bootstrap 检验显著，而且即便如此，它也只是“预测作用强”。是否适合干预需要干预研究来检验。见 " + L("6.5", "6.5") + "、" + L("7.4", "7.4") + "。"),
("课程数据是真实的吗？", "课文用的面板不是，是按设定的真实结构模拟的 N = 800、三波社区成年居民数据（<code>data/simulate_data.R</code>），所以可以检验方法能否找回真实结构（总体目标值与被试内真值，见 " + L("7.2", "7.2") + "）。数据字典见 <a href=\"../data/data_dictionary.html\">数据字典</a>。另外有两份真实的公开数据：7.6 课的练习用体育教练心理健康追踪（CC0，文件在课程包里）；<a href=\"case_elsoc.html\">ELSOC 案例</a>用智利社会纵向研究的 PHQ-8（CC0，预处理后的分析文件在课程包里）。两份的来源、许可和引用格式都写在数据字典里。")]),
("写作与报告", [
("方法部分最容易漏写什么？", "λ 规则、CV 折数、随机种子、是否标准化、协变量是否惩罚、中心性是否包含自回归、bootstrap 次数和 CS 标准。对照<a href=\"cheatsheets.html#report\">报告检查表</a>逐项检查。"),
("结果中的数字怎样保证不出错？", "每个数字都应能追溯到某个输出文件（" + L("10.2", "10.2") + " 的“数字—文件”对照表）。最好用 Quarto 行内代码自动插入，不要手抄。"),
("怎样写局限？", "至少包括：标准 CLPN 混合了被试间与被试内效应；观察数据无法排除未测量混杂；结论依赖于时间间隔；样本的代表性。见 " + L("10.3", "10.3") + "。")])]
fq = ""
for i, (h, items) in enumerate(FAQ):
    fq += sec(f"q{i+1}", h, "".join(f'<details class="ans faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in items))
page("faq.html", "常见问题 FAQ", f"<p>全课程层面的常见问题（共 {sum(len(x[1]) for x in FAQ)} 条），分为学习与使用、R 与软件、统计概念、CLPN 方法、写作与报告五类。各课页面中还有针对本课内容的“常见问题与误区”。</p>", fq)

# =====================================================================  学习日志
lesson_opts = "".join(f'<option value="{E(l["id"] + " " + l["title"])}"></option>' for m in MODULES for l in m["lessons"])
lg = '''<div class="slog-bar nprint">
<button type="button" class="slog-go" id="slogDownload">下载 Markdown</button>
<button type="button" class="linkish" id="slogPrint">打印</button>
<button type="button" class="linkish quiet" id="slogClear">清除本页记录</button>
</div>
<p class="muted nprint">写过的内容留在这个浏览器里。清除网站数据、换浏览器或使用无痕窗口后，这里的记录会消失。下载或打印才能留下一份。</p>
'''
lg += sec("daily", "每次学习记录", '''<div class="slog">
<label class="slog-name">姓名 <span class="muted nprint">可留空，只用于下载的文件名</span><input id="slogName" type="text" autocomplete="name"></label>
<div id="slogDays"></div>
<p class="nprint"><button type="button" class="linkish" id="addDay">增加一条记录</button></p>
</div>''', "slog")
lg += sec("weekly", "每周小结", '''<div class="slog"><div id="slogWeeks"></div>
<p class="nprint"><button type="button" class="linkish" id="addWeek">增加一周</button></p></div>''', "slog")
lg += sec("feynman", "费曼检查：用一段话讲给没学过统计的社工同事听", '''<div class="slog"><div id="slogFeyn"></div>
<p class="nprint"><button type="button" class="linkish" id="addFeyn">再写一条</button></p></div>''', "slog")
lg += sec("howto", "怎样使用", '''<ul>
<li>在本页填写。离开页面不必另外保存，写过的字留在这个浏览器里。</li>
<li>每次学习结束花 5–10 分钟。每周回顾时打开这一页，或打开下载的 Markdown。</li>
<li>“遇到的 R 报错”一栏特别有用：几周后回看，同样的错误不再出现。</li>
<li>要留下不随浏览器消失的一份，点“下载 Markdown”或“打印”。也可以另取 <a href="study_log.md" download>空白 Markdown</a>，在编辑器里写。</li>
</ul>''')
lg += f'<datalist id="slogLessons">{lesson_opts}</datalist>\n<script src="../lessons/assets/studylog.js"></script>\n'
page("study_log.html", "学习日志", "<p>每次学习后记一条，每周写一段小结。在这一页填写，然后下载 Markdown 或打印。</p>", lg)
md = "# CLPN 从零开始 · 学习日志\n\n> 每次学习后填写一行；每周写一段小结。可复制本文件为 `study_log_我的名字.md`。\n\n## 每次学习记录\n\n| 日期 | 课程 | 用时 | 今天学到的三件事 | 还不懂的地方 | 遇到的 R 报错及解决办法 | 下一步想弄清的问题 |\n|---|---|---|---|---|---|---|\n" + "|  |  |  |  |  |  |  |\n" * 6 + \
     "\n## 每周小结（第 ___ 周）\n\n- 本周完成的课程：\n- 测验正确率 / 练习完成情况：\n- 最有收获的一个概念（用自己的话解释）：\n- 仍然困惑的地方，以及打算怎样解决：\n- 本周完成并归档的练习：\n- 下周计划：\n\n## 费曼检查\n\n概念：\n\n用一段话讲给没学过统计的社工同事听：\n\n我卡住的地方：\n"
open(D + "materials/study_log.md", "w", encoding="utf-8").write(md)

# =====================================================================  START_HERE.md
# 与 START_HERE.html 同源：直接把刚生成的学习指南页面收成 Markdown（保留链接），不再单独维护一份文字。
_rm = {}
exec(open(SRC + "/common/readmd.py", encoding="utf-8").read(), _rm)
_sh = _rm["reading_md"](open(D + "START_HERE.html", encoding="utf-8").read(), keep_links=True)
_sh = re.sub(r"\A学习资料 · Study materials\n+", "", _sh)
_sh = re.sub(r"^这一页说明怎样在网站上学习.*$", "本文件由 `src/build_materials.py` 从 [START_HERE.html](START_HERE.html) 同源生成，内容与网页版相同。", _sh, count=1, flags=re.M)
open(D + "START_HERE.md", "w", encoding="utf-8").write(_sh)

dl = sec("pack", "课程压缩包", """
<p><a class="dl" download href="clpn-course.zip">clpn-course.zip</a></p>
<p>整门课一个压缩包。解压后得到 <code>clpn-course/</code> 文件夹：</p>
<ul>
<li><b>离线网站</b>：<code>index.html</code>、学习指南、全部课件和学习资料，双击 <code>index.html</code> 用浏览器打开即可，不需要联网；</li>
<li><b>数据</b>：<code>data/</code>（模拟数据、数据字典、<code>simulate_data.R</code>、生成数据时用的系数；另有 7.6 练习用的一份真实公开数据 <code>coaches_mhc_raw.csv</code>，CC0）；</li>
<li><b>R 脚本</b>：<code>R/</code>（各课配套脚本、<code>_setup.R</code>、一键运行全部的 <code>run_all.R</code>、R 代码使用说明）、<code>R/solutions/</code>（练习解答）、<code>R/output/</code>（参考结果）；</li>
<li><code>README.md</code>（文件夹说明，先看这个）、<code>clpn-course.Rproj</code>（双击用 RStudio 打开）、<code>LICENSE</code>（课程内容 CC BY 4.0，代码 MIT）、<code>THIRD_PARTY_NOTICES.md</code>。</li>
</ul>
<p>解压后：浏览器打开 <code>index.html</code> 学习；双击 <code>clpn-course.Rproj</code> 运行 R。详细步骤见本页下方“怎样使用”。</p>""")
dl += sec("data", "数据", """
<p>模拟的面板数据，不含真实个人信息。<code>true_B_within.csv</code> 与 <code>true_B_population.csv</code> 是生成数据时用的系数，不是你自己的估计结果。标准 CLPN 对准的是后者（总体 OLS，含特质混杂），两者不是同一张矩阵。也可以单独打开：</p>
<ul>
<li><a href="../data/data_dictionary.html">数据字典</a></li>
<li><a href="../data/clpn_sim_wide.csv">clpn_sim_wide.csv</a></li>
<li><a href="../data/clpn_sim_wide.sav">clpn_sim_wide.sav</a>（SPSS）</li>
<li><a href="../data/simulate_data.R">simulate_data.R</a></li>
</ul>
<p>另有一份<b>真实</b>的公开数据，供 7.6 课的测量不变性练习使用：<a href="../data/coaches_mhc_raw.csv">coaches_mhc_raw.csv</a>（瑞士 422 名体育教练、3 波的心理健康连续体简版 MHC-SF 14 题；Ackeret et al., 2023，<a href="https://doi.org/10.5061/dryad.8931zcrws">doi.org/10.5061/dryad.8931zcrws</a>，CC0 1.0）。文件按原样收录（分号分隔），使用前请先读<a href="../data/data_dictionary.html">数据字典</a>的说明：自带的分量表列与题目列对不上，波次间隔的说明也前后矛盾。</p>
<p>还有一份真实面板供 ELSOC 案例（<a href="../materials/case_elsoc.html">案例页</a>）使用：<a href="../data/elsoc_phq8_wide.csv">elsoc_phq8_wide.csv</a>（智利社会纵向研究 2016–2018 年原始样本的 PHQ-8 三波与性别、年龄；COES 2022，<a href="https://doi.org/10.7910/DVN/LQMURF">doi.org/10.7910/DVN/LQMURF</a>，CC0 1.0）。这是预处理后的子集，由 <code>R/data_elsoc.R</code> 从同样附带的原始文件 <code>data/elsoc/ELSOC_Wide_2016_2021_v1.00_R.RData</code> 写出；分析脚本是 <code>R/case_elsoc.R</code>。引用格式见数据字典最后一节。</p>""")
dl += sec("howto", "怎样使用", local_setup("../") + """
<p>课内“配套脚本”链接指向单个 <code>.R</code> 文件，可在浏览器中直接阅读；要运行，请在 RStudio 里通过 <code>clpn-course.Rproj</code> 打开。</p>""")
dl += sec("single", "单份文件", """
<ul>
<li><a href="../materials/study_log.html">学习日志</a>（可在页面填写；<a href="../materials/study_log.md" download>空白 Markdown</a>）</li>
<li><a href="../R/output/L6-4_network.pdf">L6-4 网络图 PDF</a></li>
<li><a href="../R/README.html">R 使用说明</a></li>
</ul>""")
page("downloads/index.html", "下载", "<p>整门课一个压缩包：离线网站、数据、R 脚本和练习解答。解压后打开 <code>index.html</code> 学习，双击 <code>clpn-course.Rproj</code> 运行 R。</p>", dl)

# =====================================================================  测评页（materials/assess_*.html）
# 题库在 src/assess/<slug>.py，规格与渲染在 src/common/assess.py；没有题库文件时不生成任何页面。
_aspec = importlib.util.spec_from_file_location("assess", os.path.join(SRC, "common/assess.py"))
_as = importlib.util.module_from_spec(_aspec); _aspec.loader.exec_module(_as)
_qspec = importlib.util.spec_from_file_location("quiz", os.path.join(SRC, "common/quiz.py"))
_qz = importlib.util.module_from_spec(_qspec); _qspec.loader.exec_module(_qz)
_banks = _as.load_banks(SRC, REPO)
_RVG = {"ROOT": REPO}
exec(open(SRC + "/common/rvals.py", encoding="utf-8").read(), _RVG)   # 期末 B 部分引用的 R 结果 {{V:键}}
for _slug, _bank in _banks.items():
    page(_as.fname(_slug), _as.SPEC[_slug][1], _RVG["fillV"](_bank["LEAD"]), _RVG["fillV"](_as.render_body(_slug, _bank, _qz.quiz, sec)))
if _banks:
    page(_as.HUB, "测评：前测、阶段测验与期末", "<p>前测看起点，阶段测验检查每个模块，期末覆盖全课程。本页说明怎么用、怎么计分和评分标准。</p>", _as.render_hub(_banks, sec))
# 写作工作坊与论文阅读包（源文件在 src/materials/，可用本文件的 page、sec、L、_qz、_RVG）
for _f in ("writing", "reading", "case_elsoc"):
    exec(open(SRC + f"/materials/{_f}.py", encoding="utf-8").read(), globals())
# 删除已经没有题库的旧测评页（以及没有题库时的总页），避免过期页面留在站上和压缩包里
for _f in os.listdir(D + "materials"):
    _m = re.fullmatch(r"assess_(\w+)\.html", _f)
    if (_m and _m.group(1) not in _banks) or (_f == _as.HUB and not _banks):
        os.remove(D + "materials/" + _f)

# 把学员会打开的 Markdown 渲染成同一套页面。学习日志已有专门的 study_log.html，不覆盖。
# START_HERE.html 是学习指南本身，不要再把 START_HERE.md 渲染成同名 HTML。
_spec = importlib.util.spec_from_file_location("mdhtml", os.path.join(SRC, "common/mdhtml.py"))
_md = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_md)
MD_DOCS = [
    ("R/README.md", "R 代码使用说明"),
    ("data/data_dictionary.md", "数据字典"),
    ("R/output/L10-1_analysis_plan.md", "分析计划"),
    ("R/output/L10-3_results_draft.md", "结果草稿"),
]
for src_rel, fallback in MD_DOCS:
    raw = open(os.path.join(D, src_rel), encoding="utf-8").read()
    title, body = _md.render_md(raw)
    out_rel = src_rel[:-3] + ".html"
    page(out_rel, title or fallback,
         f'<p>原文：<a href="{os.path.basename(src_rel)}" download><code>{E(os.path.basename(src_rel))}</code></a></p>',
         f'<section class="sec" id="doc">{body}</section>',
         rel=out_rel)
print("materials ok:", ", ".join(f for f, _ in PAGES), "+ study_log.md + START_HERE.md + rendered md")
