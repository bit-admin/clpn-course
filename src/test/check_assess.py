# -*- coding: utf-8 -*-
"""检查测评题库 src/assess/*.py 和课内测验宏（不需要浏览器）。
1. 课内测验：src/lessons/L*.html 里每个 ```quiz 都能解析；单选恰好一个正确项，数值题答案和容差是数字，文本题有答案。
2. 题库文件名必须是 src/common/assess.py 的 SPECS 里的 slug；自动判分题、简答题数量与 SPECS 一致。
3. 每题有 obj = "课号-目标序号"，且能在 src/data1–3.py 该课的 obj 列表里找到。
   尚未写进大纲的课只能用 PLANNED 里明确列出的课号（写进 data 后以 data 为准）。
4. 题干不重复：题库内部互不重复；自动判分题不与课内测验题干重复，简答题不与课内练习题面重复
   （读生成的 lessons/L*.html，去标签、去空白后比较）。所以要在重建之后运行本检查。
5. 简答题有参考答案和 0–3 共 4 级评分标准（期末 B 部分用 dims：4 个维度、合计 10 分）；有 PARTS 的题库，每题的 part 都在 PARTS 里。
6. 考核比重只在 src/template.html #assessment：题库和 src/common/assess.py 里不得出现比重 / 权重语境的百分数
   （“比重”、考核语境的“权重”或“权重 …%”、“占 …%”“考核 …%”）。网络里的“边权重”“权重矩阵”不受限制。普通百分数（如“95% 区间”）不受限制。
7. 页面与链接：materials/ 里每个 assess_*.html 都要有对应题库（没有就是过期页面）；每个测评页都要从测评总页
   materials/assessment.html 链接；总页要在资料导航（build_materials.py 的 PAGES）里。
用法：python3 src/test/check_assess.py [--complete]   （--complete：SPECS 里每个题库文件都必须存在）
先重建（至少 build_lessons 两个脚本和 build_materials.py），再运行本检查。"""
import glob, html, importlib.util, os, re, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EN = "--en" in sys.argv
ROOT = os.path.join(REPO, "en") if EN else REPO
SRC = os.path.join(REPO, "src", "en") if EN else os.path.join(REPO, "src")
def load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(SRC, rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
qz, asm = load("quiz", "common/quiz.py"), load("assess", "common/assess.py")
g = {"ROOT": REPO}
for f in ["data1", "data2", "data3", "data4"]:
    exec(open(os.path.join(SRC, f + ".py"), encoding="utf-8").read(), g)
OBJ = {l["id"]: l["obj"] for m in g["MODULES"] for l in m["lessons"]}
# 已获批、但还没写进 src/data3.py 的课：课号 → 目标条数（写进 data 后自动以 data 为准，可以删掉这里的条目）
PLANNED = {"7.6": 4, "7.7": 5}
NOBJ = {**{k: v for k, v in PLANNED.items() if k not in OBJ}, **{k: len(v) for k, v in OBJ.items()}}
errs, warn = [], []
norm = lambda s: re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", "", s)))
isnum = lambda x: re.fullmatch(r"-?\d+(\.\d+)?", x.strip() or "x") is not None

def check_item(where, p):
    if not p["q"]: errs.append(f"{where}: 没有题干 Q:")
    if p["kind"] == "mc":
        n = sum(o[0] for o in p["opts"])
        if n != 1: errs.append(f"{where}: 单选题需要恰好一个正确选项（现有 {n} 个）")
        if len(p["opts"]) < 2: errs.append(f"{where}: 单选题至少要 2 个选项")
    elif p["kind"] == "num":
        if not (isnum(p["ans"]) and isnum(p["tol"])): errs.append(f"{where}: 数值题答案 / 容差不是数字（{p['ans']} | {p['tol']}）")
    elif not p["ans"].strip(): errs.append(f"{where}: 文本题没有答案 T:")

# 1. 课内测验宏
FENCE = re.compile(r"^```(\w+)[ \t]*(.*?)\n(.*?)^```[ \t]*$", re.S | re.M)
nles = 0
for f in sorted(glob.glob(os.path.join(SRC, "lessons/L*.html"))):
    for k, m in enumerate((m for m in FENCE.finditer(open(f, encoding="utf-8").read()) if m.group(1) == "quiz"), 1):
        nles += 1; check_item(f"{os.path.basename(f)} 测验 {k}", qz.parse_quiz(m.group(3)))
lesson_stems, lesson_ex = set(), set()
for f in glob.glob(os.path.join(ROOT, "lessons/L*.html")):
    t = open(f, encoding="utf-8").read()
    lesson_stems |= {norm(s) for s in re.findall(r'<p class="qtext">(.*?)</p>', t, re.S)}
    lesson_ex |= {norm(s) for s in re.findall(r'<div class="exitem"><h4>.*?</h4>(.*?)<details', t, re.S)}
lesson_ex.discard("")

# 2–6. 题库
slugs = {s[0] for s in asm.SPECS}
for f in sorted(glob.glob(os.path.join(SRC, "assess/*.py"))):
    b = os.path.basename(f)[:-3]
    if b not in slugs: errs.append(f"src/assess/{b}.py: 文件名不在 SPECS 里（可用：{', '.join(s[0] for s in asm.SPECS)}）")
banks = asm.load_banks(SRC, REPO)
if "--complete" in sys.argv:
    for s in asm.SPECS:
        if s[0] not in banks: errs.append(f"缺少题库 src/assess/{s[0]}.py")
seen = {}
def check_obj(where, o):
    m = re.fullmatch(r"(\d+\.\d+)-(\d+)", o or "")
    if not m: errs.append(f"{where}: obj 应写成“课号-目标序号”，如 1.4-2（现为 {o!r}）"); return
    lid, k = m.group(1), int(m.group(2))
    if lid not in NOBJ: errs.append(f"{where}: obj {o}：没有 {lid} 这节课")
    elif not 1 <= k <= NOBJ[lid]: errs.append(f"{where}: obj {o}：{lid} 只有 {NOBJ[lid]} 条目标")
def check_stem(where, stem, short=False):
    s = norm(stem)
    if not s: return
    if not short and s in lesson_stems: errs.append(f"{where}: 题干与课内测验重复")
    if short and (s in lesson_ex or (len(s) >= 30 and any(s in e or e in s for e in lesson_ex if len(e) >= 30))):
        errs.append(f"{where}: 题面与课内练习重复")
    if s in seen: errs.append(f"{where}: 题干与 {seen[s]} 重复")
    seen[s] = where
nitems = nshort = 0
for slug, bank in banks.items():
    _, title, n_auto, n_short = asm.SPEC[slug]
    auto = [it for it in bank["ITEMS"] if not it.get("adv")]
    if len(auto) != n_auto: errs.append(f"{slug}: 自动判分题应为 {n_auto} 道，现有 {len(auto)} 道")
    if len(bank["SHORT"]) != n_short: errs.append(f"{slug}: 简答题应为 {n_short} 道，现有 {len(bank['SHORT'])} 道")
    if any(it.get("adv") for it in bank["ITEMS"]) and slug != "m7": errs.append(f"{slug}: 进阶题（adv）只放在 m7")
    for k, it in enumerate(bank["ITEMS"], 1):
        w = f"{slug} 第 {k} 题"; nitems += 1
        p = qz.parse_quiz(it.get("q", "")); check_item(w, p); check_obj(w, it.get("obj")); check_stem(w, p["q"])
    for k, s in enumerate(bank["SHORT"], 1):
        w = f"{slug} 简答 {k}"; nshort += 1
        check_obj(w, s.get("obj")); check_stem(w, s.get("q", ""), short=True)
        if not s.get("answer"): errs.append(f"{w}: 没有参考答案")
        if s.get("dims"):   # 期末 B 部分：4 个维度，合计 10 分
            if len(s["dims"]) != 4 or sum(d[1] for d in s["dims"]) != 10: errs.append(f"{w}: 维度评分应为 4 个维度、合计 10 分")
        else:
            lv = sorted(str(r[0]) for r in s.get("rubric", []))
            if lv != ["0", "1", "2", "3"]: errs.append(f"{w}: 评分标准应为 0–3 共 4 级（现为 {lv}）")
    if bank.get("PARTS"):
        known = {p[0] for p in bank["PARTS"]}
        for k, it in enumerate(bank["ITEMS"], 1):
            if it.get("part") not in known: errs.append(f"{slug} 第 {k} 题: part {it.get('part')!r} 不在 PARTS 里（题目不会显示）")
# “权重”在网络课里多指边权重（权重矩阵、边权重），只在考核语境或带百分数时才算考核比重
WEIGHT = re.compile(r"比重|(?:考核|总评|成绩|计分)[^。；\n]{0,8}权重|权重[^。；\n]{0,12}?\d+\s*%|占[^。；\n]{0,12}?\d+\s*%|考核[^。；\n]{0,24}?\d+\s*%")
for f in sorted(glob.glob(os.path.join(SRC, "assess/*.py"))) + [os.path.join(SRC, "common/assess.py")]:
    for ln, line in enumerate(open(f, encoding="utf-8"), 1):
        if WEIGHT.search(line) and "不重复写比重" not in line:
            errs.append(f"{os.path.relpath(f, REPO)}:{ln}: 不要在这里写考核比重（只在 src/template.html #assessment）")
# 7. 过期页面与链接
for f in sorted(glob.glob(os.path.join(ROOT, "materials/assess_*.html"))):
    slug = os.path.basename(f)[len("assess_"):-len(".html")]
    if slug not in banks: errs.append(f"materials/assess_{slug}.html：没有对应题库 src/assess/{slug}.py（过期页面，重建会删除）")
if banks:
    hub = os.path.join(ROOT, "materials/assessment.html")
    if not os.path.exists(hub): errs.append("有题库但没有测评总页 materials/assessment.html（先重建）")
    else:
        ht = open(hub, encoding="utf-8").read()
        for slug in banks:
            if f'href="{asm.fname(slug)}"' not in ht: errs.append(f"测评总页没有链接到 {asm.fname(slug)}")
    if '"materials/assessment.html"' not in open(os.path.join(SRC, "build_materials.py"), encoding="utf-8").read():
        errs.append("测评总页不在资料导航 PAGES 里（build_materials.py）")
if 'id="assessment"' not in open(os.path.join(SRC, "template.html"), encoding="utf-8").read():
    errs.append("template.html 里找不到 #assessment 考核表")

print(f"课内测验宏 {nles} 道；题库 {len(banks)}/{len(asm.SPECS)} 个，自动判分题 {nitems} 道，简答 {nshort} 道")
for e in errs: print("ERROR", e)
print("check_assess:", "OK" if not errs else f"{len(errs)} 个问题")
sys.exit(1 if errs else 0)
