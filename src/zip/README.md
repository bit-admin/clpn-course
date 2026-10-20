# CLPN 从零开始 · 课程文件夹

这个文件夹就是整门课：网站（离线版）、数据、R 脚本和练习解答都在这里，不需要联网。

## 一、先看什么

1. 用浏览器打开 `START_HERE.html`（学习指南：怎样学、按什么顺序、{{C:weeks}} 周计划）。
2. 再打开 `index.html`（课程大纲），从这里进入每一节课。

双击即可，不需要安装任何东西。

## 二、文件夹里有什么

| 位置 | 内容 |
| --- | --- |
| `index.html`、`START_HERE.html` | 课程大纲、学习指南 |
| `lessons/`、`materials/` | {{C:size}}的交互课件；术语表、速查卡、公式表、FAQ、学习日志、写作工作坊、论文阅读包、真实数据案例、测评 |
| `data/` | 模拟数据（800 人 × 3 波）、数据字典（`data_dictionary.html`）；两份真实公开数据：7.6 练习用的 `coaches_mhc_raw.csv` 和 ELSOC 案例用的 `elsoc_phq8_wide.csv` 及其原始文件 `elsoc/`（都是 CC0，来源与引用见数据字典） |
| `R/` | 每节课的 R 脚本、`_setup.R`、`run_all.R`、`assess_answers.R`、真实数据案例的 `data_elsoc.R` 与 `case_elsoc.R`、使用说明 `README.html` |
| `R/solutions/` | 练习解答 |
| `R/output/` | 参考结果（网页上的图和日志）；运行脚本会用你的结果覆盖 |
| `clpn-course.Rproj` | RStudio 项目文件 |
| `LICENSE`、`THIRD_PARTY_NOTICES.md` | 许可协议 |

## 三、运行 R

1. 先安装 R，再安装 RStudio（步骤见 `R/README.html`）。
2. 双击 `clpn-course.Rproj`，用 RStudio 打开课程项目。不要直接双击 `.R` 文件。
3. 打开 `R/L2-4.R` 点 Source，安装课程用到的包（只需一次）。
4. 每节课打开对应的 `R/Lx-y.R`（例如 `R/L1-1.R`），逐行运行（Ctrl/Cmd + Enter）。

## 四、运行顺序

按课号顺序运行即可。有先后依赖的：

- L6-4 → L6-5
- L4-3 → L10-1 → L10-2 → L10-3
- L8-3 → 练习解答 L8-3

缺少前置结果文件时，脚本会停下并告诉你先运行哪个脚本。

一次运行全部课文脚本和练习解答：在 RStudio 的 Console 里输入

```r
source("R/run_all.R")
```

约 40–95 分钟，结果汇总在 `R/output/run_all_status.csv`。真实数据案例的两个脚本也在其中，说明见 `materials/case_elsoc.html`。

## 五、许可

© 2026 ZHANG。课程内容（文字、课件、图、数据及说明）采用 CC BY 4.0；代码（R 脚本、网页脚本等）采用 MIT 许可。详见 `LICENSE`。
