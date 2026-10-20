# -*- coding: utf-8 -*-
"""核对课件中引用的 R 结果是否与 R/output/ 中的当前输出一致。
检查 A：M0–M4 课件中手工粘贴的“输出”框（pre.out），每一行都必须能在 R/output/ 的某个文件中找到。
检查 A0：M0–M4 的每个 ```out 框都必须在标题里说明来源：写明日志（标题含 output 或 log，如
       “输出（R/output/L3-1_log.txt，节选）”），或标明是示意（标题含“示意”或“预期”）。没有标题、或标题两者都不是，
       都算错误（--strict-a 时返回 1），报告课号与标题。
检查 B：正文中带 ≥2 位小数的数字，若在本课（及同模块）R 输出里找不到同样四舍五入的数，列出供人工复核
       （很多是手算例子或假设数字，属正常；本检查用于发现过期的数字）。
检查 B（严格）：STRICT_B 中列出的课（新写的 7.6 等，数字全部从 RV / 日志读取），正文里任何带 ≥2 位小数的数
       （包括 .05 这种省略 0 的写法）都必须在 R/output/ 中找得到，否则算错误；只允许 STRICT_B 里列出的经验阈值。
用法：python3 src/test/check_numbers.py [--strict-a]   （--strict-a：检查 A0、A 或严格检查 B 有错误时返回 1）"""
import re, glob, os, html, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EN = "--en" in sys.argv
ROOT = os.path.join(REPO, "en") if EN else REPO
read_outs = lambda d: {f: open(f, encoding="utf-8", errors="replace").read() for f in glob.glob(d + "/R/output/*") if f.endswith((".txt", ".csv", ".md"))}
# 检查 A 只对照本语言的 R/output/（英文版：en/R/output/）；检查 B 的数字池两边都用（英文正文的 {{V:}} 数字读自中文 R/output/，数值相同）
outs = read_outs(ROOT)
ALL = "\n".join(list(outs.values()) + (list(read_outs(REPO).values()) if EN else []))
norm = lambda s: re.sub(r"\s+", " ", s).strip()
ALLN = norm("\n".join(outs.values()))
def nums_in(text):
    return re.findall(r"[-−]?\d+\.\d+(?:e[-+]?\d+)?", text)
POOL = set()
for x in nums_in(ALL):
    try: v = float(x.replace("−", "-"))
    except: continue
    for d in (1, 2, 3, 4, 5, 6): POOL.add(f"{round(v, d):.{d}f}")
# 严格检查 B 的课程，以及允许出现的“规则数字”（经验阈值、模拟设定，不是运行结果）
STRICT_B = {
    # 7.6：Cheung & Rensvold / Chen (2007) 的经验阈值（ΔCFI、ΔRMSEA、ΔSRMR，含 Chen 对 N ≤ 300 的更严格版本）
    "L7-6": {"0.01", "0.015", "0.02", "0.08", "0.005", "0.010", "0.030", "0.025"},
    # 7.7 里明确是“教学用的假设数字”或模拟设定，不是运行结果：
    #   0.05 = α 与 72 × 0.05 的算术；0.20 = 模拟里埋入的差异；0.08 = 测验题 (81+1)/1001 的近似；
    #   0.09–0.27 = cextra 里“10 次洗牌”手算例题的假设数字
    "L7-7": {"0.05", "0.20", "0.08", "0.09", "0.11", "0.12", "0.13", "0.14", "0.15", "0.17", "0.18", "0.21", "0.24", "0.27"},
}
badA = 0; badB = 0; badT = 0; report = []
SRC = os.path.join(REPO, "src", "en", "lessons") if EN else os.path.join(REPO, "src", "lessons")
is_m04 = lambda lid: re.fullmatch(r"L[0-4]-\d+", lid) is not None
is_illus = lambda title: any(w in title.lower() for w in (("illustrative", "expected") if EN else ("示意", "预期")))
OUTRE = re.compile(r"^```out[ \t]*(.*)$", re.M)
if EN:   # A1：英文 ```out 框与中文一一对应，中文写明来自 R/output/ 的框，英文不能改标成示意（否则逃过检查 A）
    for f in sorted(glob.glob(os.path.join(REPO, "src", "lessons", "L*.html"))):
        b = os.path.basename(f); fe = os.path.join(SRC, b)
        if not os.path.exists(fe): continue
        zt = OUTRE.findall(open(f, encoding="utf-8").read()); et = OUTRE.findall(open(fe, encoding="utf-8").read())
        if len(zt) != len(et):
            badT += 1; report.append(f"A1 {b[:-5]}: ```out 框数量与中文不同（中文 {len(zt)}，英文 {len(et)}）"); continue
        for a, c in zip(zt, et):
            if ("示意" in a or "预期" in a) != is_illus(c):
                badT += 1; report.append(f"A1 {b[:-5]}: [{c}] 与中文 [{a}] 的“示意 / 来自日志”不一致")
# A0（源文件）：没有标题的 ```out 框（生成的页面里没有 ctitle，下面的循环看不到它们）
for f in sorted(glob.glob(os.path.join(SRC, "L*.html"))):
    lid = os.path.basename(f)[:-5]
    if not is_m04(lid): continue
    for n, line in enumerate(open(f, encoding="utf-8"), 1):
        if re.fullmatch(r"```out\s*", line.rstrip("\n")):
            badT += 1; report.append(f"A0 {lid}: 第 {n} 行的 ```out 框没有标题（应写明 R/output/ 日志，或标明“示意”/“预期”）")
for page in sorted(glob.glob(ROOT + "/lessons/L*.html")):
    lid = os.path.basename(page)[:-5]
    t = open(page, encoding="utf-8").read()
    # A：手工输出框（M0–M4 的 ```out 宏）
    for blk in re.findall(r'<div class="ctitle">([^<]*)</div><pre class="out"><code>(.*?)</code></pre>', t, re.S):
        title, body = blk
        title = html.unescape(title)
        if is_illus(title): continue
        if "output" not in title.lower() and "log" not in title.lower():   # 只核对声明来自 R/output 的输出框
            if is_m04(lid):   # A0：M0–M4 的输出框必须声明来源
                badT += 1; report.append(f"A0 {lid}: [{title}] 标题既没有写明 R/output/ 日志，也没有标明“示意”/“预期”")
            continue
        body = html.unescape(body)
        for line in body.split("\n"):
            L = norm(line)
            if len(L) < 6 or not re.search(r"\d", L) or L.startswith("#"): continue
            if L not in ALLN:
                badA += 1; report.append(f"A {lid}: [{title[:30]}] {L[:110]}")
    # B：正文数字
    m = re.search(r"<main>(.*)</main>", t, re.S); body = m.group(1)
    body = re.sub(r"<pre.*?</pre>|<script.*?</script>|<nav.*?</nav>|<span class=\"katex.*?</span></span>", "", body, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", body))
    mod = lid.split("-")[0]
    own = ALL   # 所有 R 输出（跨课引用很常见）
    pool = POOL
    txt = re.sub(r"10\.\d{4,5}/\S+", " ", txt)   # 去掉 DOI
    miss = sorted({x for x in nums_in(txt) if len(x.split(".")[1]) >= 2 and f"{float(x.replace('−','-')):.{len(x.split('.')[1])}f}" not in pool})
    if miss and lid not in STRICT_B: report.append(f"B {lid}: " + " ".join(miss))
    if lid in STRICT_B:
        cand = set(nums_in(txt)) | {"0" + x for x in re.findall(r"(?<![\d.])\.\d{2,}", txt)}
        bad = sorted({x for x in cand if len(x.split(".")[1]) >= 2 and x.lstrip("-−") not in STRICT_B[lid]
                      and f"{float(x.replace('−','-')):.{len(x.split('.')[1])}f}" not in pool})
        if bad:
            badB += len(bad); report.append(f"B-STRICT {lid}: " + " ".join(bad))
        unused = sorted(a for a in STRICT_B[lid] if a not in cand)   # 允许清单里多余的数字也算错，避免清单越积越长
        if unused:
            badB += len(unused); report.append(f"B-STRICT {lid}: 允许清单里的数字在正文中没有出现：" + " ".join(unused))
print("\n".join(report)); print(f"检查 A0 未说明来源的 M0–M4 输出框：{badT}"); print(f"检查 A 不匹配行数：{badA}"); print(f"严格检查 B（{'、'.join(STRICT_B)}）找不到来源的数字：{badB}")
sys.exit(1 if ("--strict-a" in sys.argv and (badA or badB or badT)) else 0)
