# CLPN 从零开始

**交叉滞后面板网络分析（Cross-Lagged Panel Network, CLPN）自学课程**，从统计基础一直讲到独立完成并写出一项 CLPN 分析。

- 在线学习：<https://clpn.ruc.edu.kg>（English: <https://clpn.ruc.edu.kg/en/>）
- 离线学习：下载 `downloads/clpn-course.zip`，解压后用浏览器打开 `index.html`（无需联网，公式和字体都已随包提供）

[English](#english)

## 课程内容

11 个模块（M0–M10）、45 节核心课 + 2 节选学，按 16 周设计。假定你学过入门统计，但没用过 R。

| 模块 | 主题 |
|---|---|
| M0 | 课程导论：为什么要学 CLPN |
| M1 | 统计学基础：描述统计、标准化、相关、标准误与假设检验 |
| M2 | R 与 RStudio：从零开始，到描述统计、回归、ggplot2 和可复现报告 |
| M3 | 回归分析：多元回归、标准化系数、逻辑回归、LASSO 与交叉验证 |
| M4 | 纵向与面板数据：设计语言、宽长格式、缺失与流失 |
| M5 | 传统交叉滞后面板模型（CLPM）与 RI-CLPM |
| M6 | 网络心理测量学基础：偏相关网络、正则化估计、中心性 |
| M7 | 交叉滞后面板网络（CLPN）：逐节点估计、可视化、出/入期望影响、设计选择；另有 2 节进阶选学 |
| M8 | 稳定性与准确性检验：bootstrap、边权重区间、CS 系数 |
| M9 | 阅读、批判与报告规范 |
| M10 | 毕业项目：完整的 CLPN 分析 |

每节课的结构相同：① 直觉 → ② 最少数学 → ③ R 代码 → ④ 理解检查 → ⑤ 练习 → 小结。课文里嵌有可交互的小组件和即时反馈的测验；另有前测、各模块阶段测验和期末考核。

学习资料：学习指南（`START_HERE.html`）、双语术语表、速查卡、公式表、常见问题、学习日志、写作工作坊、论文阅读包，以及一个用真实数据完成的案例（ELSOC 抑郁症状网络）。

## 数据与 R 代码

- 课文用的面板数据是**模拟数据**（N = 800，3 个时间点，9 个条目，生成脚本 `data/simulate_data.R`），不含任何真实个人信息。模拟时使用的真实参数也一并提供，便于比较估计与真值。
- 两份 CC0 公开数据：7.6 练习用的教练心理健康追踪数据，以及 ELSOC（智利社会纵向研究）PHQ-8 子集。来源与引用格式见 `data/data_dictionary.md`。
- 每节课对应一个 R 脚本 `R/L<模块>-<课>.R`，练习解答在 `R/solutions/`，参考输出（日志、图、表）在 `R/output/`。用 RStudio 打开 `clpn-course.Rproj` 后 `source()` 即可；需要的 R 包和用法见 `R/README.md`。

## 从源文件构建

网页都由 `src/` 里的 Python 脚本生成，不要手工修改生成的页面。需要 Python 3 和 R（脚本在 R 4.5 上验证）。

```bash
python3 -m venv .venv
Rscript R/run_all.R                                  # 全部 R 脚本 → R/output/（约 40–95 分钟）
.venv/bin/python src/build_lessons.py                # M0–M4 课件
.venv/bin/python src/lessons-m5-10/build_lessons.py  # M5–M10 课件
.venv/bin/python src/build_materials.py              # 学习资料、测评、下载页
.venv/bin/python src/build.py                        # 课程大纲 index.html
.venv/bin/python src/build_dist.py                   # 下载包与发布目录 dist/
```

英文版的构建、各个检查脚本和源文件的结构见 [`src/README.md`](src/README.md)。`dist/` 是一个纯静态的 Cloudflare Workers 站点：复制 `wrangler.example.jsonc` 为 `wrangler.jsonc` 后，可用 `npx wrangler dev` 本地预览，`npx wrangler deploy` 发布（需要 Node 22 或更新版本）。

## 许可

© 2026 ZHANG。课程内容（课文、学习资料、图、模拟数据及数据说明）采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)；代码（R 脚本、`data/simulate_data.R`、`lessons/assets/` 中的 JS/CSS、`src/` 中的构建与检查脚本）采用 [MIT 许可](https://opensource.org/license/mit)。具体哪些路径属于哪一类，以 [LICENSE](LICENSE) 为准。随附的第三方组件（KaTeX、JetBrains Mono）保留各自的许可，见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

---

## English

**CLPN From Scratch** is a self-paced course on Cross-Lagged Panel Network analysis, from statistical foundations to carrying out and writing up a CLPN analysis of your own.

- Online: <https://clpn.ruc.edu.kg/en/>
- Offline: download `downloads/clpn-course-en.zip`, extract it and open `index.html` in a browser. No internet connection is needed; math rendering and fonts are bundled.

The English edition lives in [`en/`](en/index.html) and has the same lessons, materials, data and R scripts as the Chinese course, with English text and English R output. Every page has a language switch.

**What's inside.** 11 modules (M0–M10) with 45 core lessons plus 2 optional advanced lessons, designed for 16 weeks. It assumes introductory statistics and no prior R. Each lesson runs intuition → minimal math → R code → comprehension check → exercises → summary, with interactive widgets and instant-feedback quizzes, plus a pre-test, module quizzes and a final assessment. Materials include a learning guide, bilingual glossary, cheat sheets, formula sheet, FAQ, study log, writing workshop, reading pack and a worked case study on real data (ELSOC depression-symptom network).

**Data.** The panel used in the lessons is simulated (N = 800, 3 waves, 9 items; `data/simulate_data.R`) and contains no real personal data. Two CC0 public datasets are included as well: a coaches' mental-health panel for the 7.6 exercise and a PHQ-8 subset of ELSOC (the Chilean Longitudinal Social Survey). Sources and citation formats are in `data/data_dictionary.md`.

**R.** One script per lesson (`R/L<module>-<lesson>.R`, English versions in `en/R/`), solutions in `R/solutions/`, reference output in `R/output/`. Open `clpn-course.Rproj` and `source()` a script; package list and usage are in `R/README.md`.

**Building.** Pages are generated from `src/` (Chinese) and `src/en/` (English); see the build commands above and [`src/README.md`](src/README.md) for the English build, the checks and the source layout.

**License.** © 2026 ZHANG. Course content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) and code under the [MIT License](https://opensource.org/license/mit); see [LICENSE](LICENSE) for which paths are which, and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for bundled third-party components.

<p align="center"><sub>Dedicated to TyC</sub></p>
