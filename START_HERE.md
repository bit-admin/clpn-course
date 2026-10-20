# 学习指南：怎样使用这门课

本文件由 `src/build_materials.py` 从 [START_HERE.html](START_HERE.html) 同源生成，内容与网页版相同。

## 一、这个网站上有什么

课程在浏览器里学。下表是站上的页面。整个网站连同数据、R 脚本和练习解答可以打包下载：从 [下载页](downloads/index.html)取得 `clpn-course.zip`，解压后双击 `index.html` 就能离线学习，运行 R 见下面第五节。

| 页面 | 是什么 | 什么时候用 |
| --- | --- | --- |
| [课程大纲](index.html) | 11 个模块、全部课程的目标、概念、练习，带进度勾选 | 每次学习的起点 |
| 课件 | 45 节核心课 + 2 节选学，都是交互课件（直觉 → 数学 → R 代码 → 测验 → 练习 → 小结）。从大纲点「学习 1.1」这类链接进入 | 每节课的主体 |
| 学习资料 | 本指南、[术语表](materials/glossary.html)、[速查卡](materials/cheatsheets.html)、[公式表](materials/formulas.html)、[常见问题](materials/faq.html)、[学习日志](materials/study_log.html) | 随时查阅 |
| [下载](downloads/index.html) | 整门课的压缩包：离线网站、数据、R 脚本、练习解答 | 要离线学习或在自己的电脑上运行 R 时 |
| [写作工作坊](materials/writing.html)、[论文阅读包](materials/reading.html) | 方法、结果、局限的改写范例；精选论文与阅读问题 | 学 9.3 和 10.3 时；写毕业项目论文时 |
| [真实数据案例](materials/case_elsoc.html) | ELSOC 抑郁症状（PHQ-8）的 CLPN。分析文件随课程提供 | 学完 7.4 和 8.2 之后；写毕业项目时对照 |
| [测评](materials/assessment.html) | 前测、每个模块的阶段测验、期末考试，附评分标准 | 开学前、每学完一个模块、学完 10.3 后 |
| [R 代码使用说明](R/README.html) | 安装 R 和 RStudio、打开项目、运行脚本 | 学到 R 代码时 |
| [数据字典](data/data_dictionary.html) | 模拟的 N = 800、三波“孤独—抑郁”数据，每个变量的含义 | 做练习时对照 |

进度（“标记本课为已完成”）保存在浏览器里，换浏览器或清除缓存会丢失，重要的学习记录请写进学习日志。

## 二、按什么顺序学

模块编号代表知识的逻辑顺序：M0 总览 → M1 统计基础 → M2 R 编程 → M3 回归与正则化 → M4 纵向数据 → M5 CLPM → M6 网络心理测量 → M7 CLPN → M8 稳定性 → M9 批判阅读与报告 → M10 毕业项目。实际学习时，**M1 统计和 M2 R 并排学（第 2–5 周交替进行），M3 回归在它们之后**：学完一个统计概念，马上在 R 里做一遍。每节课页面顶部都列出了先修课，可以点击跳转。

| 模块 | 主题 | 课数 | 课程 |
| --- | --- | --- | --- |
| **M0** | 课程导论：为什么要学 CLPN Course Overview | 2 | [0.1](lessons/L0-1.html) [0.2](lessons/L0-2.html) |
| **M1** | 统计学基础 Statistics Foundations | 6 | [1.1](lessons/L1-1.html) [1.2](lessons/L1-2.html) [1.3](lessons/L1-3.html) [1.4](lessons/L1-4.html) [1.5](lessons/L1-5.html) [1.6](lessons/L1-6.html) |
| **M2** | R 与 RStudio：从零开始 R & RStudio from Zero | 6 | [2.1](lessons/L2-1.html) [2.2](lessons/L2-2.html) [2.3](lessons/L2-3.html) [2.4](lessons/L2-4.html) [2.5](lessons/L2-5.html) [2.6](lessons/L2-6.html) |
| **M3** | 回归分析 Regression | 5 | [3.1](lessons/L3-1.html) [3.2](lessons/L3-2.html) [3.3](lessons/L3-3.html) [3.4](lessons/L3-4.html) [3.5](lessons/L3-5.html) |
| **M4** | 纵向与面板数据 Longitudinal / Panel Data | 3 | [4.1](lessons/L4-1.html) [4.2](lessons/L4-2.html) [4.3](lessons/L4-3.html) |
| **M5** | 传统交叉滞后面板模型（CLPM）与 RI-CLPM Cross-Lagged Panel Models | 4 | [5.1](lessons/L5-1.html) [5.2](lessons/L5-2.html) [5.3](lessons/L5-3.html) [5.4](lessons/L5-4.html) |
| **M6** | 网络心理测量学基础 Network Psychometrics | 5 | [6.1](lessons/L6-1.html) [6.2](lessons/L6-2.html) [6.3](lessons/L6-3.html) [6.4](lessons/L6-4.html) [6.5](lessons/L6-5.html) |
| **M7** | 交叉滞后面板网络（CLPN） Cross-Lagged Panel Networks | 7 | [7.1](lessons/L7-1.html) [7.2](lessons/L7-2.html) [7.3](lessons/L7-3.html) [7.4](lessons/L7-4.html) [7.5](lessons/L7-5.html) [7.6](lessons/L7-6.html) [7.7](lessons/L7-7.html) |
| **M8** | 稳定性与准确性检验 Stability & Accuracy | 3 | [8.1](lessons/L8-1.html) [8.2](lessons/L8-2.html) [8.3](lessons/L8-3.html) |
| **M9** | 阅读、批判与报告规范 Reading, Critique & Reporting | 3 | [9.1](lessons/L9-1.html) [9.2](lessons/L9-2.html) [9.3](lessons/L9-3.html) |
| **M10** | 毕业项目：完整的 CLPN 分析 Capstone Mini-Project | 3 | [10.1](lessons/L10-1.html) [10.2](lessons/L10-2.html) [10.3](lessons/L10-3.html) |

## 三、每节课怎么学（约 2–3 小时）

1. **读目标（2 分钟）：**看“本课学习目标”和“核心概念”。不认识的词先查[术语表](materials/glossary.html)。

2. **① 直觉（20–30 分钟）：**不要跳过。先在脑子里形成画面，再看公式。交互组件一定要动手拖一拖。

3. **② 最少数学（15–30 分钟）：**拿纸笔跟着算一遍“完整例题”。公式汇总在[公式表](materials/formulas.html)。

4. **③ R 代码（30–60 分钟）：**双击 `clpn-course.Rproj` 打开 RStudio 项目，打开对应的 `R/Lx-y.R`，**逐行运行**（Ctrl/Cmd + Enter），把输出和网页上的输出对照。页面底部可以展开完整脚本。

5. **④ 即时测验（10 分钟）：**答错会先给提示，答错两次才显示答案。

6. **⑤ 练习（1–2 小时）：**自己先做，再看参考答案；需要写代码的练习，答案在 `R/solutions/`。写作类练习对照课文给出的评分要点逐条自评，改一遍再存档。每课的练习脚本和输出建议整理在同一个文件夹里，毕业项目时还会用到。

7. **小结与日志（10 分钟）：**点“标记本课为已完成”，在[学习日志](materials/study_log.html)里写下三句话：学到了什么、哪里还不懂、下一步想弄清什么。

**卡住了怎么办？**

①先看本课的“常见错误”和“常见问题与误区”；②查 [FAQ](materials/faq.html)；③R 报错时，把报错的最后一行复制到搜索引擎；④仍然不行，按 [2.1 课](lessons/L2-1.html) 的“最小可复现例子”格式整理好，到同学、同事或 R 社区论坛（如 Posit Community、Stack Overflow）提问。卡住超过 30 分钟就该换个办法，不要硬耗。整理最小例子的过程中，常常就已经找到了原因。

## 四、16 周周计划

**标准节奏：16 周，每周学 3 次**（第 14、15 周各 4 次），每次 60–150 分钟，另加每周 2–3 小时练习，合计每周约 5–7 小时；核心课的课文学习共约 85 小时（不含选学课和练习）。假期集中学习可压缩到约 12 周（每周学 4 次）；与学期课程同时进行可放宽到约 19 周（在第 5、8、13 周后各加一个缓冲周）。进阶选学课 7.6、7.7 不在标准节奏里：学有余力时在第 13 周之后自学，宽松版放在第 13 周后的缓冲周，压缩版不含。

| 周次 | 课程 | 重点 |
| --- | --- | --- |
| 第 1 周 | 0.1 · 0.2 · 1.1 | 启动：课程地图、为什么学 CLPN、变量与测量 |
| 第 2 周 | 1.2 · 1.3 · 2.1 · 0.2 先跑一遍 | 描述统计、z 分数；安装 R（第 2–5 周 M1 统计与 M2 R 并排学）；装好 R 后做 0.2 课的“先跑一遍”（约 30 分钟）：复制现成代码，跑出第一张 CLPN 图 |
| 第 3 周 | 2.2 · 1.4 · 2.3 | R 语法；协方差与相关；数据框 |
| 第 4 周 | 1.5 · 1.6 · 2.4 | 标准误、置信区间、p 值；包与导入数据 |
| 第 5 周 | 2.5 · 2.6 · 阶段测验 | 用 R 复现统计基础；绘图与报告；M1、M2 阶段测验 |
| 第 6 周 | 3.1 · 3.2 · 3.3 | M1、M2 之后进入 M3 回归：简单回归、多元回归、标准化系数 |
| 第 7 周 | 3.4 · 3.5 · 4.1 | 逻辑回归、正则化与 LASSO；纵向设计 |
| 第 8 周 | 4.2 · 4.3 · 阶段测验 | 数据整形、缺失与流失；M3、M4 阶段测验（期中） |
| 第 9 周 | 5.1 · 5.2 · 5.3 | CLPM 直觉、lavaan 实操、RI-CLPM |
| 第 10 周 | 5.4 · 6.1 · 6.2 | 因果推断边界；网络语言；偏相关与 GGM |
| 第 11 周 | 6.3 · 6.4 · 6.5 | 正则化网络、qgraph / bootnet、中心性 |
| 第 12 周 | 7.1 · 7.2（2 次） | CLPN 模型逻辑；glmnet 逐节点估计 |
| 第 13 周 | 7.3 · 7.4 · 7.5 | CLPN 可视化、出/入 EI、多波与设计选择；进阶选学 7.6、7.7 不占标准课时，可在本周之后自学 |
| 第 14 周 | 8.1 · 8.2（2 次）· 8.3 | bootstrap、边准确性、CS 系数（本周学 4 次） |
| 第 15 周 | 9.1 · 9.2 · 9.3 · 10.1 | 读论文、批判、报告规范；项目设计（本周学 4 次） |
| 第 16 周 | 10.2（2 次）· 10.3 | 毕业项目分析、写作与汇报 |

每周结束时：在学习日志中写周小结；把本周的练习脚本和输出归档；用大纲页的进度条检查是否跟上计划。

## 五、在自己的电脑上运行 R

### 1. 下载并解压

从[下载页](downloads/index.html)取得 `clpn-course.zip`，解压（Windows：右键 →“全部解压缩”；Mac：双击）。得到一个文件夹 `clpn-course/`，学习和运行 R 需要的东西都在里面：

```text
clpn-course/
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
    └── output/            ← 参考结果（网页上的图、日志）；运行脚本会用你的结果覆盖
```

请先解压再使用，不要在压缩包的预览窗口里直接打开文件。路径里最好不要有中文和空格（例如放在 `D:\clpn-course`）。从 GitHub 获取整个仓库的，仓库根目录就是同样的课程文件夹。

### 2. 打开项目

1. 按 [R 代码使用说明](R/README.html) 安装 R 和 RStudio（先装 R，再装 RStudio）。

2. 双击 `clpn-course/clpn-course.Rproj`。RStudio 以“项目”方式打开，工作目录就是 `clpn-course` 文件夹。每个脚本第一行的 `source("R/_setup.R")` 都依赖这一点：不要直接双击 `.R` 文件打开。

3. 打开 `R/L2-4.R` 点 Source，安装课程需要的包（只需一次）。

4. 打开 `R/L1-1.R`，逐行运行（Ctrl/Cmd + Enter），确认能看到输出。之后每节课打开对应的 `R/Lx-y.R`（0.1 课和 9.1 课没有脚本）。

### 3. 运行顺序与依赖

按课号顺序运行即可。下面这些脚本要读取前面脚本在 `R/output/` 生成的文件。压缩包里的 `R/output/` 已带有参考结果，所以直接运行也能读到；但如果你修改并重新运行了前置脚本，后面的脚本就会用你的新结果。如果需要的文件不存在（例如删掉了 `R/output/`），脚本会在开头停下，并告诉你先运行哪个脚本。

| 脚本 | 需要先运行 |
| --- | --- |
| `L6-5.R`、`solutions/L6-4_solution.R`、`solutions/L6-5_solution.R` | `L6-4.R` |
| `L10-1.R` → `L10-2.R` → `L10-3.R` | 依次：`L4-3.R` → `L10-1.R` → `L10-2.R` → `L10-3.R`（每一步都需要上一步的结果） |
| `solutions/L8-3_solution.R` | `L8-2.R`（读 `L8-2_boot.rds`）和 `L8-3.R` |
| `case_elsoc.R` | 随课程提供的 `data/elsoc_phq8_wide.csv`（由 `data_elsoc.R` 从随课程提供的原始文件写出） |
| 其余脚本 | 无 |

**一次运行全部**：`source("R/run_all.R")`。它按课号运行全部课文脚本和期末答案脚本，再运行全部答案脚本（`R/solutions/`）。约 40–95 分钟（视电脑而定），大部分时间是 L8-2、L8-3、L10-2 的 bootstrap；结果汇总在 `R/output/run_all_status.csv`。其中也包括真实数据案例的 `data_elsoc.R` 和 `case_elsoc.R`。

bootstrap 默认**单核**运行（`nCores = 1`）、固定种子，在同一 R / 包版本下结果逐位可重复，与网页上的数字一致。改成并行会快几倍，但结果不再可重复：区间端点一般只在小数点后两三位上变化，CS 系数却可能整档跳动（课程数据的 in-EI 会在 0.44 和 0.52 之间变化，正好跨过 0.5 的参考线）。

## 六、进度与自查

- 每周固定留出 30 分钟回顾：重读学习日志里“还不懂的地方”一栏，能自己解决的划掉，解决不了的写清楚卡在哪一步，带进下一周。

- 练习的结果保存为脚本加输出（或一份 Quarto 报告），不要只留截图。几周后回头核对，或者在毕业项目里复用代码，都要靠它。

- 写作类练习（解读段落、审稿意见、方法与结果）先写，再对照课文和[写作工作坊](materials/writing.html)的评分要点逐条打分，改一遍。能找到同学或同事互相读一遍更好：请对方指出哪一句读起来像因果结论。

- 第 5 周和第 8 周做阶段测验（M1 + M2、M3 + M4），第 15–16 周是毕业项目（[10.1](lessons/L10-1.html)、[10.2](lessons/L10-2.html)、[10.3](lessons/L10-3.html)）。项目开始前，先写好一页分析计划并存档（带日期）；正式分析之后如有改动，在报告里逐条说明改了什么、为什么改。

## 七、测评：前测、阶段测验与期末

- **开始之前**：做一次[前测](materials/assess_pre.html)（约 20 分钟，不计分）。它会建议你走 16 周标准节奏，还是在第 5、8、13 周后各加一个缓冲周的 19 周节奏。

- **每学完一个模块**：做这个模块的阶段测验（15–25 分钟）。一次答对 70% 及以上就继续；不到 70% 的，按错题解释里的链接回去复习。

- **学完 10.3**：做期末考试（约 90 分钟），和前测对照，看看自己进步了多少。

- 每次的“一次答对”题数记进[学习日志](materials/study_log.html)。评分标准见[测评总页](materials/assessment.html)。

© 2026 ZHANG. Content [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); code [MIT](https://opensource.org/license/mit). [GitHub](https://github.com/bit-admin/clpn-course)
