# R 代码使用说明（CLPN 自学课程）

本文件夹包含课程每一课的 R 脚本（`L模块-课.R`，例如 `L7-2.R` = 第 7 模块第 2 课；带字母后缀的是同一课的补充脚本，如 `L7-5b.R`）、一键运行全部的 `run_all.R`、练习答案（`solutions/`）和运行结果（`output/`，已带参考结果，运行脚本时会被你的结果覆盖）。所有脚本都已在 R 4.5 上实际运行通过。

## 一、安装 R 和 RStudio（只需做一次）

**先装 R，再装 RStudio。** R 是“发动机”，RStudio 是“驾驶舱”（写代码的界面）。

### Windows
1. 打开 <https://cran.r-project.org/bin/windows/base/>，下载 “Download R-4.x.x for Windows”，双击安装，一路“下一步”。
   - 国内网速慢可用清华镜像：<https://mirrors.tuna.tsinghua.edu.cn/CRAN/bin/windows/base/>
2. 打开 <https://posit.co/download/rstudio-desktop/>，下载 RStudio Desktop（Windows 版）并安装。
3. （可选）若安装某些包时提示需要编译，可安装 Rtools：<https://cran.r-project.org/bin/windows/Rtools/>。本课程的包通常有现成的二进制版本，一般不需要。
4. 注意：**Windows 用户名或文件夹路径最好不要含中文和空格**，例如把课程放在 `D:\clpn-course\`。

### Mac
1. 打开 <https://cran.r-project.org/bin/macosx/>：M1/M2/M3 芯片选 `arm64` 版本，Intel 芯片选 `x86_64` 版本，下载 `.pkg` 安装。
2. 打开 <https://posit.co/download/rstudio-desktop/> 下载 Mac 版 RStudio，拖进“应用程序”。
3. 若提示需要命令行工具，在“终端”运行 `xcode-select --install`。

## 二、取得课程文件夹并打开项目

从课程网站的下载页取得 `clpn-course.zip`，解压（Windows：右键 →“全部解压缩”；Mac：双击）。得到的 `clpn-course/` 文件夹里就是全部内容：

```text
clpn-course/
├── index.html             ← 课程网站的离线版：双击用浏览器打开
├── README.md              ← 文件夹说明（先看这个）
├── START_HERE.html、lessons/、materials/
├── clpn-course.Rproj      ← 双击它，用 RStudio 打开课程项目
├── LICENSE、THIRD_PARTY_NOTICES.md
├── data/                  ← 模拟数据、数据字典、simulate_data.R；真实数据 coaches_mhc_raw.csv（7.6）、elsoc_phq8_wide.csv 与原始文件 elsoc/（ELSOC 案例）
└── R/                     ← 本说明、_setup.R、run_all.R、L0-2.R、L1-1.R … L10-3.R、assess_answers.R
    ├── data_elsoc.R、case_elsoc.R   ← 真实数据案例（预处理、CLPN）
    ├── solutions/         ← 练习解答
    └── output/            ← 参考结果；运行脚本会用你的结果覆盖
```

请先解压再使用，不要在压缩包预览窗口里直接打开文件；路径里最好不要有中文和空格（如 `D:\clpn-course`）。从 GitHub 获取整个仓库的，仓库根目录就是同样的课程文件夹，不需要解压。

然后：

1. 双击 `clpn-course/clpn-course.Rproj`，RStudio 会以“项目”方式打开——此时工作目录自动就是课程文件夹，所有相对路径（如 `data/clpn_sim_wide.csv`、每个脚本第一行的 `source("R/_setup.R")`）都能找到。**不要直接双击 `.R` 文件打开**。
2. （可选）设置国内镜像加快下载：RStudio 菜单 Tools → Global Options → Packages → Primary CRAN repository 选 China (Tsinghua)。

## 三、安装课程需要的包（只需做一次）

打开 `R/L2-4.R` 点 Source，或在 Console 中粘贴：

```r
install.packages(c("tidyverse", "psych", "lavaan", "qgraph", "bootnet", "glmnet",
                   "networktools", "mgm", "igraph", "readxl", "haven", "mice",
                   "knitr", "rmarkdown", "lme4"))
```

## 四、运行脚本

- 打开某一课的脚本（如 `R/L7-2.R`），点右上角 **Source**（运行整个文件），或选中几行按 **Ctrl+Enter**（Mac：**Cmd+Enter**）逐行运行。**推荐逐行运行**，边看注释边看结果。
- 每个脚本第一行 `source("R/_setup.R")` 会：确认课程文件夹（从当前工作目录往上找含有 `data/clpn_sim_wide.csv` 的文件夹）、设置中文字体、加载常用函数（如 `clpn_estimate()`）。这一行本身要求工作目录就是 `clpn-course` 文件夹，所以请通过 `clpn-course.Rproj` 打开 RStudio。你不需要单独打开 `_setup.R`，但值得读一读。
- 结果：文字输出保存为 `R/output/Lx-y_log.txt`，图保存为 `R/output/Lx-y_*.png`。
- 一键运行全部：`source("R/run_all.R")`。它按课号运行全部课文脚本和期末答案脚本 `assess_answers.R`，再运行全部答案脚本（`R/solutions/`）。约 40–95 分钟（视电脑而定），几乎全部时间在 bootstrap；bootstrap 默认单核以保证可重复。结果汇总在 `R/output/run_all_status.csv`。真实数据案例 `data_elsoc.R`、`case_elsoc.R` 也在其中。

### 有先后依赖的脚本

按课号顺序运行就不会出问题。下面这些脚本要读取前面脚本在 `R/output/` 生成的文件；压缩包里的 `R/output/` 已带参考结果，所以直接运行也能读到；但如果你修改并重新运行了前置脚本，后面的脚本就会用你的新结果。如果需要的文件不存在（例如删掉了 `R/output/`），脚本会在开头停下，并用中文说明先运行哪个脚本。

| 脚本 | 需要先运行 |
|---|---|
| L6-5.R、solutions/L6-4_solution.R | L6-4.R（生成抑郁–焦虑示例数据 `L6-4_dep_anx_items.csv`） |
| L10-1.R | L4-3.R（流失数据示例 `L4-3_data_with_attrition.csv`） |
| solutions/L4-3_solution.R | L4-3.R（`L4-3_data_with_attrition.csv`） |
| L10-2.R | L10-1.R（`L10-1_clean_data.csv`） |
| L10-2b.R | L10-1.R（`L10-1_clean_data.csv`）和 L10-2.R（`L10-2_results.rds`，用于逐边对照主分析） |
| L10-3.R | L10-2.R（`L10-2_results.rds`）和 L10-2b.R（`L10-2b_results.rds`） |
| solutions/L8-3_solution.R | L8-3.R（`L8-3_CS.csv`）和 L8-2.R（`L8-2_boot.rds`） |
| case_elsoc.R | 随课程提供的 `data/elsoc_phq8_wide.csv`（由 data_elsoc.R 从随课程提供的原始文件写出） |

毕业项目是一条链：**L4-3 → L10-1 → L10-2 → L10-2b → L10-3**，每一步都需要上一步的结果（L10-2b 是必做的完整流程敏感性分析）。其余课文脚本（包括 L7-5b.R）只依赖课程数据，可以单独运行。真实数据案例直接运行 `case_elsoc.R` 即可；想核对预处理再运行 `data_elsoc.R`（读随课程提供的原始文件，不需要联网）。说明见 [真实数据案例](../materials/case_elsoc.html)。

### 比较慢的脚本
`L8-2.R`（约 7–15 分钟）、`L8-3.R`（约 5–25 分钟）、`L10-2.R`（约 15–40 分钟）——这是 1000 次 bootstrap，每次都要做 9 个交叉验证 LASSO（以上为不同电脑上的单核实测范围）。上课练习时可把开头的 `n_boots <- 1000` 改成 `200`。脚本默认 `nCores = 1`（单核），这样 `set.seed()` 后结果逐位可重复；改成 `max(1, parallel::detectCores() - 1)` 可以快几倍，但 bootnet 的并行重抽样不受 `set.seed()` 控制，结果每次略有不同。`L7-7.R`（进阶选学，组间比较：3 × 1000 次置换，单核约 2–4 分钟，可把 `NPERM <- 1000` 改成 `200`）；`L7-6.R`（进阶选学，不变性 + 样本量模拟）约 1 分钟；`case_elsoc.R`（真实数据案例，200 次 bootstrap）约 1–2 分钟，把它开头的 `B_BOOT <- 200` 改成 `1000` 大约再要几分钟；`L7-5b.R` 与 `L10-2b.R`（SEM 重估）各约 5–10 秒；`L5-3b.R`（RI-CLPM 与真值对照：20 万人的大样本 + 200 次 N = 800 重复）约 1–3 分钟；其余脚本大多几秒内完成。`data_elsoc.R` 约 2 秒（原始文件不在、需要下载时，视网速再加几秒到 1 分钟）。

## 五、文件一览

| 模块 | 脚本 |
|---|---|
| M1 统计基础 | L1-1 … L1-6 |
| M2 R 入门 | L2-1 … L2-6（L2-6 另渲染 `L2-6_report.Rmd`） |
| M3 回归 | L3-1 … L3-5（L3-5 = LASSO 与交叉验证） |
| M4 纵向数据 | L4-1 … L4-3 |
| M5 CLPM / RI-CLPM | L5-1 … L5-4（L5-3b = RI-CLPM 结果与生成模型真值的对照；L5-4 = 混杂、时间间隔、稳定特质三个因果推断模拟） |
| M6 网络心理测量 | L6-1 … L6-5 |
| M7 CLPN | L7-1 … L7-5（L7-2 = 核心估计，“仅 LASSO”简化版）；L7-5b = Wysocki et al.（2025）完整流程：LASSO 选边 → lavaan 无惩罚重估（同波残差相关、FIML、跨时间等值检验）→ in-/out-prediction |
| M8 稳定性 | L8-1 … L8-3（bootstrap、CS 系数） |
| M9 报告 | L9-2（敏感性分析）、L9-3（报告清单 + 软件版本） |
| M10 毕业项目 | L10-1（数据准备与分析计划）、L10-2（主分析：仅 LASSO 的完整分析流程）、L10-2b（必做的敏感性分析：Wysocki et al., 2025 完整流程，逐边对照主分析）、L10-3（自动生成结果草稿，两种分析并列） |
| 真实数据案例 | `case_elsoc.R`（PHQ-8 的 CLPN 与 200 次 bootstrap，读随课程提供的 `data/elsoc_phq8_wide.csv`，`run_all.R` 也会运行它）、`data_elsoc.R`（从随课程提供的原始文件重新生成分析文件；原始文件不在时才联网下载）。页面：[真实数据案例](../materials/case_elsoc.html) |

纯阅读课（9.1）没有单独脚本。`R/assess_answers.R` 计算期末考试 C 部分的参考答案（写到 `R/output/assess_answers.csv`，课程网站从这里读取）；做期末时请先自己算，再运行它对照。数据说明见 [数据字典](../data/data_dictionary.md)。

## 六、常见问题

- **图里中文显示为方框**：Mac 上 `_setup.R` 使用“PingFang SC”字体；Windows 使用系统默认字体。若仍乱码，把 `_setup.R` 里 `cn_font` 改成你电脑上有的中文字体名（如 `"Microsoft YaHei"`、`"SimHei"`）。
- **“找不到课程文件夹”或 `cannot open file 'R/_setup.R'`**：工作目录不是课程文件夹。请通过双击 `clpn-course.Rproj` 打开 RStudio，而不是直接双击 `.R` 文件；在 Console 运行 `getwd()` 应显示 `…/clpn-course`。如果 `clpn-course` 里没有 `data/clpn_sim_wide.csv`，说明压缩包没有完整解压，或打开的不是解压后的文件夹（见第二节）。也可以临时用 Session → Set Working Directory → Choose Directory… 选中 `clpn-course` 文件夹。
- **“缺少前置结果文件”**：按提示先运行它点名的脚本（见“有先后依赖的脚本”）。
- **结果和讲义上的数字略有不同**：`cv.glmnet` 的交叉验证分组是随机的；脚本都用了 `set.seed()`，但不同 R / 包版本可能有细微差别。bootstrap 脚本（L8-2、L8-3、L10-2）默认单核运行，固定种子后结果逐位可重现（同一 R / 包版本下）。**如果你改为并行（`nCores > 1`），`set.seed()` 不能保证逐位重现**，区间和 CS 系数会在小数点后两三位上不同；CS 系数恰在网格临界值附近时（如 in-EI），换种子或并行甚至会在相邻两个网格值（0.44 / 0.52）之间跳动。重要的是结论的方向和稳定性（见 L9-2）。
- **报错 `there is no package called ...`**：说明这个包没装，运行 `install.packages("包名")`。
- **Quarto**：10.2 课要求的 Quarto 项目可在 RStudio 中 File → New File → Quarto Document 新建，把 `L10-2.R` 的代码分段粘贴进去即可；本文件夹提供的是 R Markdown 示例 `L2-6_report.Rmd`，写法基本相同。

## 七、练习答案（`solutions/`）

答案脚本在 `R/solutions/`。每个答案脚本把结果写入 `output/sol_<课>_log.txt`（个别另存图）。`run_all.R` 会在主脚本之后依次运行全部答案脚本。

| 答案脚本 | 对应练习 |
|---|---|
| L1-2、L1-3、L1-4、L1-5、L1-6 | 描述统计、z 分数、相关、抽样模拟、多重比较（换种子 + 200 次重复） |
| L2-1 … L2-6 | 第一个脚本（含报错演示）、向量、dplyr、导入与检查、描述 / 相关 / 回归、ggplot2（另有 Quarto 模板 `week06.qmd`） |
| L3-1 … L3-5 | 回归、多元回归、标准化、逻辑回归、LASSO |
| L4-1、L4-2、L4-3 | 方差分解与 lme4 ICC、数据整形、流失分析与 MCAR 对照 |
| L5-2、L5-3、L5-4 | CLPM 拟合与约束、RI-CLPM 随机截距（相关及 95% CI）、因果推断模拟练习 |
| L6-1、L6-2、L6-4、L6-5 | 邻接矩阵、偏相关（加入直接作用；课程数据上数边）、nodeNames 与 T1 / T2 网络对比、中心性 |
| L7-2、L7-4 | CLPN 估计、出 / 入 EI |
| L7-6、L7-7（选学） | 纵向测量不变性（课程数据抑郁 5 题；教练数据“社会幸福感”5 题）、男女 T2 → T3 网络的置换检验 |
| L8-1、L8-3 | 自写 bootstrap 与样本量—区间宽度、CS 系数 |
| L9-2 | 加入性别、年龄协变量后的最强 5 条边 |

6.3、7.3、7.5、8.2 的动手练习直接运行对应主脚本即可完成，没有单独的答案脚本。
