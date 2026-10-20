# -*- coding: utf-8 -*-
"""Assemble dist/ for Cloudflare Workers static assets, and write the download zips
(downloads/clpn-course.zip for Chinese and downloads/clpn-course-en.zip for English).

Run after the HTML builders:
    .venv/bin/python src/build_dist.py
"""
import os, re, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUT_EXT = {".png", ".svg", ".jpg", ".jpeg", ".pdf", ".txt", ".csv", ".log", ".md", ".html"}

PAGE_404 = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>找不到页面 · CLPN 从零开始</title>
<style>
body{margin:0;font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",system-ui,sans-serif;background:#f6f6f4;color:#1a1a1a;line-height:1.7}
main{max-width:40rem;margin:15vh auto;padding:0 20px}
a{color:#003262}
h1{font-weight:600;font-size:1.6rem}
</style>
</head>
<body>
<main>
<h1>找不到这一页</h1>
<p>地址可能写错了，或这一页还没有发布。</p>
<p><a href="/">返回课程大纲</a></p>
<p style="color:#5c5c5c;font-size:.8rem">© 2026 ZHANG. Content <a href="https://creativecommons.org/licenses/by/4.0/" rel="license noopener" target="_blank">CC BY 4.0</a>; code <a href="https://opensource.org/license/mit" rel="license noopener" target="_blank">MIT</a>. <a href="https://github.com/bit-admin/clpn-course" rel="noopener" target="_blank">GitHub</a></p>
</main>
</body>
</html>
"""

PACK_ROOT = "clpn-course"                       # top-level folder inside the Chinese zip
ZIP_NAME = "clpn-course.zip"
PACK_ROOT_EN = "clpn-course-en"                 # top-level folder inside the English zip
ZIP_NAME_EN = "clpn-course-en.zip"
ZIP_DATE = (2026, 1, 1, 0, 0, 0)                # fixed entry time -> reproducible zip
ROOT_FILES = ["index.html", "START_HERE.html", "LICENSE", "THIRD_PARTY_NOTICES.md", "clpn-course.Rproj"]
TREES = ["lessons", "materials", "data", "R/solutions", "R/output"]
LOCAL_ONLY = ()
BUNDLED_RDATA = {"data/elsoc/ELSOC_Wide_2016_2021_v1.00_R.RData"}
LESSON_MD = re.compile(r"^lessons/L[^/]*\.md$")   # reading texts for the website / LLMs, not in the zip

LEARNER_README = ROOT / "src" / "zip" / "README.md"
_g = {}
for _f in ["data1", "data2", "data3", "data4"]:
    exec((ROOT / "src" / f"{_f}.py").read_text(encoding="utf-8"), _g)
fillC = _g["fillC"]

LEARNER_README_EN = ROOT / "src" / "en" / "zip" / "README.md"
_g_en = {}
if (ROOT / "src" / "en" / "data4.py").is_file():
    for _f in ["data1", "data2", "data3", "data4"]:
        exec((ROOT / "src" / "en" / f"{_f}.py").read_text(encoding="utf-8"), _g_en)
fillC_en = _g_en.get("fillC", fillC)

# Links in the zipped copies of the pages that would point at website-only files.
OFFLINE_SUBS = [
    # cross-language switcher link (website-only; each zip is single-language)
    (re.compile(r'<a class="act langSwitch"[^>]*>.*?</a>'), ""),
    # lesson head: <link rel="alternate" type="text/markdown" href="Lx-y.md">
    (re.compile(r'<link rel="alternate" type="text/markdown" href="[^"]*"[^>]*>\n?'), ""),
    # lesson top bar: "纯文本查看" (Lx-y.md) and the "复制给 LLM" button that copies that URL
    (re.compile(r'<a class="act" id="readView" href="[^"]*\.md"[^>]*>.*?</a>'), ""),
    (re.compile(r'<button id="readBtn"[^>]*>.*?</button>'), ""),
    # index: "通过 LLM 学习" box (llm.md is not in the zip)
    (re.compile(r'<div class="llm">.*?</div>\s*</div>\n?', re.S), ""),
    # START_HERE lead: "Markdown 版：START_HERE.md（内容相同）。"
    (re.compile(r'Markdown 版：<a href="START_HERE\.md"[^>]*>.*?</a>（内容相同）。'), ""),
    (re.compile(r'Markdown\s*(?:version|edition)?:\s*<a href="START_HERE\.md"[^>]*>.*?</a>[^.<]*\.?', re.I), ""),
    # sentences telling the reader to fetch clpn-course.zip: offline, they already have it unpacked
    (re.compile(r'整个网站连同数据、R 脚本和练习解答可以打包下载：从 <a href="downloads/index\.html">下载页</a>取得 <code>clpn-course\.zip</code>，解压后双击 <code>index\.html</code> 就能离线学习，'),
     "你现在看的是离线版：这个文件夹里有整个网站以及数据、R 脚本和练习解答，"),
    (re.compile(r'<h3>1\. 下载并解压</h3>\n<p>从<a href="(?:\.\./)*downloads/index\.html">下载页</a>取得 <code>clpn-course\.zip</code>，解压（Windows：右键 →“全部解压缩”；Mac：双击）。得到一个文件夹 <code>clpn-course/</code>，'),
     "<h3>1. 课程文件夹</h3>\n<p>你正在用的文件夹 <code>clpn-course/</code> 就是 <code>clpn-course.zip</code> 解压后得到的，"),
    (re.compile(r'读完后打开 <a href="downloads/index\.html">下载页</a>，取得整门课的压缩包 <code>clpn-course\.zip</code>：解压后双击 <code>index\.html</code> 可离线学习，双击 <code>clpn-course\.Rproj</code> 运行 R。'),
     "你现在看的是离线版；运行 R 时双击本文件夹里的 <code>clpn-course.Rproj</code>。"),
    (re.compile(r'<p>从课程网站的下载页取得 <code>clpn-course\.zip</code>，解压（Windows：右键 →“全部解压缩”；Mac：双击）。得到的 <code>clpn-course/</code> 文件夹里就是全部内容：'),
     "<p>你正在用的 <code>clpn-course/</code> 文件夹（<code>clpn-course.zip</code> 解压后得到）里就是全部内容："),
    (re.compile(r'，包含在<a href="(?:\.\./)*downloads/index\.html">下载页</a>的课程压缩包里。'),
     "，就在这个课程文件夹里。"),
    (re.compile(r'从<a href="(?:\.\./)*downloads/index\.html">下载页</a>取得的 <code>clpn-course\.zip</code> 解压后就是这个文件夹（'),
     "你现在打开的离线版就在这个文件夹里（"),
    # English: the same sentences in the English zip (clpn-course-en.zip)
    (re.compile(r'Then go to the <a href="downloads/index\.html">Download page</a> for the course archive <code>clpn-course-en\.zip</code>: extract it \(you get a folder <code>clpn-course-en/</code>\), double-click <code>index\.html</code> to study offline, and double-click <code>clpn-course\.Rproj</code> to run R\.'),
     "You are using the offline version; to run R, double-click <code>clpn-course.Rproj</code> in this folder."),
    (re.compile(r'You can download the whole site, with the data, R scripts, and exercise solutions, as one package: get <code>clpn-course-en\.zip</code> from the <a href="downloads/index\.html">Download page</a>, extract it to the <code>clpn-course-en/</code> folder, and double-click <code>index\.html</code> to study offline\.'),
     "You are reading the offline version: this folder holds the whole site with the data, R scripts, and exercise solutions."),
    (re.compile(r'<h3>1\. Download and Extract</h3>\s*<p>Get <code>clpn-course-en\.zip</code> from the <a href="(?:\.\./)*downloads/index\.html">Download page</a> and extract it \(Windows: right-click → "Extract All…"; Mac: double-click\)\. You get a folder <code>clpn-course-en/</code> with'),
     "<h3>1. The Course Folder</h3>\n<p>The folder you are using, <code>clpn-course-en/</code>, is what <code>clpn-course-en.zip</code> extracts to. It has"),
    (re.compile(r'<p>Obtain <code>clpn-course-en\.zip</code> from the course website download page, and extract it \(Windows: right-click → &quot;Extract All&quot;; Mac: double-click\)\. The extracted <code>clpn-course-en/</code> folder contains everything:'),
     "<p>The <code>clpn-course-en/</code> folder you are using (extracted from <code>clpn-course-en.zip</code>) contains everything:"),
    (re.compile(r', included in the course archive on the <a href="(?:\.\./)*downloads/index\.html">Download page</a>\.'),
     ", in this course folder."),
    # navigation entries and cards for the download page
    (re.compile(r'<li><a href="(?:\.\./)*downloads/index\.html">[^<]*</a></li>'), ""),
    (re.compile(r'<a href="(?:\.\./)*downloads/index\.html">(?:下载|Download)</a>'), ""),
    (re.compile(r'<a class="mat" href="downloads/index\.html">.*?</a>\s*', re.S), ""),
    # remaining prose links to the download page: keep the words, drop the link
    (re.compile(r'<a href="(?:\.\./)*downloads/index\.html">(.*?)</a>'), r"\1"),
]

# R/README.md is packed as Markdown too: same rewrite of its download sentence
OFFLINE_MD_SUBS = {
    "R/README.md": [
        (re.compile(r'从课程网站的下载页取得 `clpn-course\.zip`，解压（Windows：右键 →“全部解压缩”；Mac：双击）。得到的 `clpn-course/` 文件夹里就是全部内容：'),
         "你正在用的 `clpn-course/` 文件夹（`clpn-course.zip` 解压后得到）里就是全部内容："),
    ],
}
OFFLINE_MD_SUBS_EN = {
    "R/README.md": [
        (re.compile(r'Obtain `clpn-course-en\.zip` from the course website download page, and extract it \(Windows: right-click → "Extract All"; Mac: double-click\)\. The extracted `clpn-course-en/` folder contains everything:'),
         "The `clpn-course-en/` folder you are using (extracted from `clpn-course-en.zip`) contains everything:"),
    ],
}

def offline_html(text):
    for rx, rep in OFFLINE_SUBS:
        text = rx.sub(rep, text)
    return text

def visible(p, base=ROOT):
    return p.is_file() and not any(part.startswith(".") for part in p.relative_to(base).parts)

def script_files(base=ROOT):
    R = base / "R"
    found = [R / "_setup.R", R / "run_all.R", R / "README.md"]
    for ext in ("*.R", "*.Rmd", "*.qmd"):
        found += [p for p in sorted(R.glob(ext)) if p not in found]
    return [p for p in found if p.is_file()]

def pack_entries():
    """(arcname relative to clpn-course/, bytes) for every file in the Chinese zip."""
    paths = [ROOT / f for f in ROOT_FILES] + script_files(ROOT) + [ROOT / "R" / "README.html"]
    for t in TREES:
        paths += [p for p in (ROOT / t).rglob("*") if visible(p, ROOT)]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("build_dist: missing pack files: " + ", ".join(missing))
    entries = {}
    for p in paths:
        rel = p.relative_to(ROOT).as_posix()
        if LESSON_MD.match(rel) or (LOCAL_ONLY and rel.startswith(LOCAL_ONLY)):
            continue
        data = p.read_bytes()
        if rel.endswith(".html"):
            data = offline_html(data.decode("utf-8")).encode("utf-8")
        for rx, rep in OFFLINE_MD_SUBS.get(rel, []):
            text, n = rx.subn(rep, data.decode("utf-8"))
            if not n:
                raise SystemExit(f"build_dist: offline rewrite for {rel} no longer matches")
            data = text.encode("utf-8")
        entries[rel] = data
    bad = [r for r in entries if r.lower().endswith((".rdata", ".rda", ".rds")) and r.startswith("data/") and r not in BUNDLED_RDATA]
    if bad:
        raise SystemExit("build_dist: refusing to pack data files that must stay local: " + ", ".join(bad))
    entries["README.md"] = fillC(LEARNER_README.read_bytes().decode("utf-8")).encode("utf-8")
    return entries

def pack_entries_en():
    """(arcname relative to clpn-course-en/, bytes) for every file in the English zip."""
    en_root = ROOT / "en"
    paths = [en_root / f for f in ROOT_FILES] + script_files(en_root) + [en_root / "R" / "README.html"]
    for t in TREES:
        paths += [p for p in (en_root / t).rglob("*") if visible(p, en_root)]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("build_dist (en): missing pack files: " + ", ".join(missing))
    entries = {}
    for p in paths:
        rel = p.relative_to(en_root).as_posix()
        if LESSON_MD.match(rel) or (LOCAL_ONLY and rel.startswith(LOCAL_ONLY)):
            continue
        data = p.read_bytes()
        if rel.endswith(".html"):
            data = offline_html(data.decode("utf-8")).encode("utf-8")
        for rx, rep in OFFLINE_MD_SUBS_EN.get(rel, []):
            text, n = rx.subn(rep, data.decode("utf-8"))
            if not n:
                raise SystemExit(f"build_dist (en): offline rewrite for {rel} no longer matches")
            data = text.encode("utf-8")
        entries[rel] = data
    # Include the shared bundled ELSOC .RData from repo root if not duplicated under en/data/elsoc/
    for rdata_rel in BUNDLED_RDATA:
        if rdata_rel not in entries and (ROOT / rdata_rel).is_file():
            entries[rdata_rel] = (ROOT / rdata_rel).read_bytes()
    bad = [r for r in entries if r.lower().endswith((".rdata", ".rda", ".rds")) and r.startswith("data/") and r not in BUNDLED_RDATA]
    if bad:
        raise SystemExit("build_dist (en): refusing to pack data files that must stay local: " + ", ".join(bad))
    entries["README.md"] = fillC_en(LEARNER_README_EN.read_bytes().decode("utf-8")).encode("utf-8")
    return entries

def write_zip(entries, dest, pack_root=PACK_ROOT):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(entries):
            info = zipfile.ZipInfo(f"{pack_root}/{rel}", date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, entries[rel])

def copy_site_to_dist(site_root, dist_target):
    scripts = script_files(site_root)
    dist_target.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "llm.md", "START_HERE.md", "START_HERE.html"):
        src = site_root / name
        if src.is_file():
            shutil.copy2(src, dist_target / name)
    for folder in ("lessons", "materials", "downloads", "data"):
        if (site_root / folder).is_dir():
            shutil.copytree(site_root / folder, dist_target / folder, ignore=shutil.ignore_patterns(".DS_Store"), dirs_exist_ok=True)
    dist_r = dist_target / "R"
    dist_r.mkdir(exist_ok=True)
    for p in scripts:
        target = dist_r / p.relative_to(site_root / "R")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
    if (site_root / "R" / "solutions").is_dir():
        shutil.copytree(site_root / "R" / "solutions", dist_r / "solutions", dirs_exist_ok=True)
    readme_html = site_root / "R" / "README.html"
    if readme_html.is_file():
        shutil.copy2(readme_html, dist_r / "README.html")
    out = dist_r / "output"
    out.mkdir(exist_ok=True)
    n_out = 0
    for p in (site_root / "R" / "output").iterdir():
        if p.is_file() and p.suffix.lower() in OUT_EXT:
            shutil.copy2(p, out / p.name)
            n_out += 1
    return n_out

def main():
    dl = ROOT / "downloads"
    dl.mkdir(exist_ok=True)
    entries = pack_entries()
    write_zip(entries, dl / ZIP_NAME, PACK_ROOT)
    en_info = ""
    if (ROOT / "en" / "index.html").is_file():
        entries_en = pack_entries_en()
        write_zip(entries_en, dl / ZIP_NAME_EN, PACK_ROOT_EN)
        size_en = (dl / ZIP_NAME_EN).stat().st_size
        en_info = f"; {ZIP_NAME_EN}: {len(entries_en)} files, {size_en / 1e6:.1f} MB"

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    n_out = copy_site_to_dist(ROOT, DIST)
    if (ROOT / "en" / "index.html").is_file():
        copy_site_to_dist(ROOT / "en", DIST / "en")
    (DIST / "404.html").write_text(PAGE_404, encoding="utf-8")
    (DIST / "_headers").write_text(
        "/R/*.R\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/data/*.R\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/R/*.Rmd\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/R/*.qmd\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/en/R/*.R\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/en/data/*.R\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/en/R/*.Rmd\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/en/R/*.qmd\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/*.md\n"
        "  Content-Type: text/markdown; charset=utf-8\n"
        "/*.txt\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "/*.csv\n"
        "  Content-Type: text/csv; charset=utf-8\n"
        "/*.js\n"
        "  Content-Type: text/javascript; charset=utf-8\n"
        "/*.css\n"
        "  Content-Type: text/css; charset=utf-8\n"
        "/data/*.sav\n"
        "  Content-Type: application/octet-stream\n"
        "  Content-Disposition: attachment\n"
        "/en/data/*.sav\n"
        "  Content-Type: application/octet-stream\n"
        "  Content-Disposition: attachment\n"
        "/data/elsoc/*.RData\n"
        "  Content-Type: application/octet-stream\n"
        "  Content-Disposition: attachment\n",
        encoding="utf-8")
    size = (dl / ZIP_NAME).stat().st_size
    print(f"{ZIP_NAME}: {len(entries)} files, {size / 1e6:.1f} MB{en_info}; output files on site {n_out}")
    print("dist", DIST)

if __name__ == "__main__":
    main()
