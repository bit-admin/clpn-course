# 课程网页的源文件与构建（维护者用）

学习者不需要打开本文件夹。所有网页都由脚本生成，下次构建会被覆盖，**不要手工修改**：

- `index.html`、`llm.md`（`src/build.py`）
- `lessons/L*.html`、`lessons/L*.md`（两个 `build_lessons.py`）
- `START_HERE.html`、`START_HERE.md`、`materials/*.html`、`materials/study_log.md`、`downloads/index.html`（`src/build_materials.py`；写作工作坊、论文阅读包、ELSOC 案例的内容在 `src/materials/writing.py`、`src/materials/reading.py`、`src/materials/case_elsoc.py`）
- `R/README.html`、`data/data_dictionary.html`、`R/output/L10-1_analysis_plan.html`、`R/output/L10-3_results_draft.html`：由同名 `.md` 渲染（`build_materials.py` 的 `MD_DOCS`），改 `.md`
- `downloads/clpn-course.zip`、`dist/`（`src/build_dist.py`）
- `R/output/` 下的课文与答案结果由 R 脚本写出（`R/run_all.R`）。`case_elsoc_*` 由 `R/case_elsoc.R` 写出（`run_all.R` 会运行它，读随课程提供的 `data/elsoc_phq8_wide.csv`）；`data_elsoc_log.txt` 和 `data/elsoc_phq8_wide.csv` 由 `R/data_elsoc.R` 从随课程提供的原始文件 `data/elsoc/ELSOC_Wide_2016_2021_v1.00_R.RData` 写出（`run_all.R` 也运行它）。`data/clpn_sim_wide.csv`、`.sav`、`true_B_*.csv` 由 `data/simulate_data.R` 写出

## 英文版

英文站点在 `en/`（目录结构与仓库根相同），由 `src/en/` 生成：`src/en/` 是 `src/` 的镜像，内容源已翻译，构建脚本输出到 `en/`。以中文源为准；改了中文课文，要同步改 `src/en/` 里对应的文件（M5–M10 的英文源拆得更细：`c5.py` → `c5a.py` + `c5b.py`，`c7.py` → `c7_1.py`–`c7_3.py`，`c7b.py` → `c7b_1.py` + `c7b_2.py`，`cextra.py` → `cextra1.py` + `cextra2.py`）。

- 正文里的 `{{V:键}}` 数字仍从**中文** `R/output/` 读（`src/en/common/rvals.py`；种子相同，数值一致），CS 判断等英文措辞也在这个文件里。页面上展示的日志、图和 CSV 来自 `en/R/output/`，由 `en/R/` 的英文脚本写出。
- 英文 R 必须在 `en/` 里运行（`cd en && Rscript R/run_all.R`）。在仓库根运行 `en/R/*.R` 会读中文 `R/_setup.R`，覆盖中文 `R/output/`。
- `src/en/data1–3.py` 中每个 `con` 对的第一个元素保持中文：它是 `src/en/materials/glossary_defs.py`（`DEFS`）的查找键，页面只显示英文术语。
- 每页有语言切换链接；`build_dist.py` 在两个压缩包里都去掉它，另外写出 `downloads/clpn-course-en.zip`（解压为 `clpn-course-en/`，说明文件来自 `src/en/zip/README.md`），并把 `en/` 复制到 `dist/en/`。

```bash
(cd en && Rscript R/run_all.R)                          # 英文日志和图 → en/R/output/
.venv/bin/python src/en/build_lessons.py
.venv/bin/python src/en/lessons-m5-10/build_lessons.py
.venv/bin/python src/en/build_materials.py
.venv/bin/python src/en/build.py
.venv/bin/python src/build_dist.py                      # 两个压缩包和 dist/（含 dist/en/）
python3 src/test/check_numbers.py --strict-a --en
python3 src/test/check_assess.py --complete --en
CLPN_ROOT=en node src/test/check_all.js                 # 浏览器检查英文站点
```

## 构建顺序

在仓库根用虚拟环境（`.venv`，已在 `.gitignore` 中）：

```bash
python3 -m venv .venv
Rscript R/run_all.R                        # 1. 先跑全部 R 脚本，更新 R/output/（约 40–95 分钟，视电脑而定；bootstrap 单核以保证可重复）
.venv/bin/python src/build_lessons.py      # 2. M0–M4 课件（源：src/lessons/L*.html）
.venv/bin/python src/lessons-m5-10/build_lessons.py # 3. M5–M10 课件（源：src/lessons-m5-10/c*.py）
.venv/bin/python src/build_materials.py    # 4. 学习资料、下载页、START_HERE.md
.venv/bin/python src/build.py              # 5. 课程大纲 index.html
.venv/bin/python src/build_dist.py         # 6. downloads/clpn-course.zip（离线网站 + 数据 + R + 解答）与 dist/（Cloudflare 发布目录）
```

- `data1.py`–`data4.py`：大纲数据。课程规模只有一个来源：`data4.py` 的 `COURSE_SIZE`（当前为“45 节核心课 + 2 节选学”）和 `N_WEEKS`（= `PACING` 的行数），由课程 dict 的 `opt=True`（进阶选学课）自动算出；页面源文件里写 `{{C:size}}`、`{{C:weeks}}`、`{{C:all}}`，各构建脚本用 `fillC()` 替换。本文件、`README.md`（以及本地的 `CLAUDE.md`，若存在）是手写的，`build.py` 会检查它们写的课程规模与常量一致。
- `common/shell.py`：全部课程页面和资料页共用的页面外壳（顶栏、目录、全课程导航、翻页）。
- `common/rvals.py`：构建时从 `R/output/` 读入依赖运行设置的 bootstrap / CS 结果，课件中用 `{{V:键名}}` 引用。
- `common/quiz.py`：测验渲染器（```quiz 宏、M5–M10 的测验元组），M0–M4、M5–M10 课件和测评页共用。
- `common/assess.py` + `assess/`：测评页（前测、阶段测验、期末）的规格与题库，由 `build_materials.py` 生成 `materials/assess_*.html`；题库格式见 `assess/README.md`。期末（`assess/final.py`）分 A / B / C 三部分：B 部分的数字写成 `{{V:键}}`，由 `common/rvals.py` 从 `R/output/` 读取；C 部分的答案来自 `R/assess_answers.R` 写出的 `R/output/assess_answers.csv`（`run_all.R` 在课文脚本之后运行它）。没有题库的旧测评页会在构建时删除；有题库时生成测评总页 `materials/assessment.html`（在资料导航和课件侧栏里）。考核比重只写在 `template.html` 的 `#assessment`。
- `lessons-m5-10/cextra.py`：M5–M10 各课的“完整例题”和“常见错误”补充。
- 样式与脚本：`lessons/assets/course.css`、`lesson.js`（全部页面）、`viz.js`（M0–M4 组件）、`viz-m5-10.js`（M5–M10 组件）；KaTeX 与等宽字体在 `lessons/assets/vendor/`（离线可用）。

## 检查

```bash
python3 src/test/check_links.py                                         # 内部链接、锚点、外部资源（中英文两棵树）
python3 src/test/check_numbers.py                                       # 课件中引用的 R 输出是否与日志一致
python3 src/test/check_assess.py --complete                             # 重建之后运行（13 个题库都已存在，所以总是加 --complete）：测评题库的题数、目标映射、与课内测验 / 练习查重、评分标准、过期页面与总页链接；课内测验宏
NODE_PATH=/path/to/node_modules node src/test/check_all.js              # 全部页面：断网模式、JS 错误、KaTeX、坏图、交互（需 puppeteer-core）
node --experimental-websocket src/test/check_pages.js                  # 交互检查，不给参数 = 全站每一页（Node 20 需要该参数；Node 22+ 不需要）
```

检查脚本在 Node 20 上也能运行（`check_pages.js` 需要 `--experimental-websocket`，见上）；本地预览和发布用的 Wrangler 4 需要 Node 22 或更新版本（`package.json` 的 `engines`；Node 20 上可用 `npx -p node@22 wrangler dev`）。

三个 Node 检查都用 `src/test/chrome_path.js` 找 Chrome：先看环境变量 `CHROME_PATH`，再试 Linux、macOS、Windows 的常见安装位置。例：`CHROME_PATH="/Applications/Chromium.app/Contents/MacOS/Chromium" node src/test/check_all.js`。

检查下载包的离线副本（直接 file:// 打开，没有服务器的目录补全或漂亮网址）：

```bash
rm -rf /tmp/clpn-zip && mkdir /tmp/clpn-zip && unzip -q downloads/clpn-course.zip -d /tmp/clpn-zip
NODE_PATH=/path/to/node_modules node src/test/check_offline.js /tmp/clpn-zip/clpn-course        # 每页运行脚本后的全部内部链接、锚点、资源
NODE_PATH=/path/to/node_modules CLPN_ROOT=/tmp/clpn-zip/clpn-course node src/test/check_all.js  # 断网模式全站检查，作用于解压副本
```
