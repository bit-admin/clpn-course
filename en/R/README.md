# R Code User Guide (CLPN From Scratch)

This folder contains the R scripts for each lesson of the course (`L<module>-<lesson>.R`, e.g., `L7-2.R` = Module 7 Lesson 2; scripts with letter suffixes are supplementary scripts for the same lesson, e.g., `L7-5b.R`), the master script `run_all.R` to run everything in one go, exercise solutions (`solutions/`), and generated outputs (`output/`, which comes pre-populated with reference results and will be overwritten by your own results when you run scripts). All scripts have been tested and verified on R 4.5.

## 1. Install R and RStudio (Do This Once)

**Install R first, then RStudio.** R is the "engine"; RStudio is the "cockpit" (the code editing and execution interface).

### Windows
1. Go to <https://cran.r-project.org/bin/windows/base/>, click "Download R-4.x.x for Windows", double-click the installer, and proceed through default setup steps.
   - (For users experiencing slow connections, a Tsinghua mirror is available: <https://mirrors.tuna.tsinghua.edu.cn/CRAN/bin/windows/base/>)
2. Go to <https://posit.co/download/rstudio-desktop/>, download RStudio Desktop (Windows version), and install it.
3. (Optional) If prompted to compile packages from source, install Rtools: <https://cran.r-project.org/bin/windows/Rtools/>. Precompiled binary versions are typically available for all course packages, so this is usually not required.
4. Note: **Avoid non-ASCII characters or spaces in Windows usernames or folder paths**, e.g., place the course folder at `C:\clpn-course-en\` or `D:\clpn-course-en\`.

### Mac
1. Go to <https://cran.r-project.org/bin/macosx/>: choose `arm64` for Apple Silicon (M1/M2/M3/M4 chips) or `x86_64` for Intel Macs, download the `.pkg` installer, and run it.
2. Go to <https://posit.co/download/rstudio-desktop/>, download RStudio Desktop for macOS, and drag it into your Applications folder.
3. If prompted for command line developer tools, run `xcode-select --install` in Terminal.

## 2. Obtain Course Folder and Open Project

Obtain `clpn-course-en.zip` from the course website download page, and extract it (Windows: right-click → "Extract All"; Mac: double-click). The extracted `clpn-course-en/` folder contains everything:

```text
clpn-course-en/
├── index.html             ← Offline course website: double-click to open in browser
├── README.md              ← Folder overview (read this first)
├── START_HERE.html, lessons/, materials/
├── clpn-course.Rproj      ← Double-click to open the course project in RStudio
├── LICENSE, THIRD_PARTY_NOTICES.md
├── data/                  ← Simulated data, data dictionary, simulate_data.R; real datasets coaches_mhc_raw.csv (7.6), elsoc_phq8_wide.csv and raw file elsoc/ (ELSOC case)
└── R/                     ← This guide, _setup.R, run_all.R, L0-2.R, L1-1.R … L10-3.R, assess_answers.R
    ├── data_elsoc.R, case_elsoc.R   ← Real-data case study (data preparation, CLPN)
    ├── solutions/         ← Exercise solutions
    └── output/            ← Reference results; running scripts will overwrite with your own output
```

Please extract the archive before use; do not run files directly inside the archive preview window. Avoid non-ASCII characters or spaces in the file path (e.g., use `C:\clpn-course-en`). If you cloned the full repository from GitHub, the repository root serves as the course folder and requires no extraction.

Then:

1. Double-click `clpn-course-en/clpn-course.Rproj`. RStudio will open in "Project" mode—setting the working directory automatically to the course root folder, ensuring all relative paths (such as `data/clpn_sim_wide.csv` and the `source("R/_setup.R")` line at the top of each script) resolve correctly. **Do not open scripts by double-clicking `.R` files directly**.
2. (Optional) Select a fast CRAN mirror: in RStudio, go to Tools → Global Options → Packages → Primary CRAN repository and choose a nearby mirror.

## 3. Install Required Packages (Do This Once)

Open `R/L2-4.R` and click **Source**, or paste the following into the R Console:

```r
install.packages(c("tidyverse", "psych", "lavaan", "qgraph", "bootnet", "glmnet",
                   "networktools", "mgm", "igraph", "readxl", "haven", "mice",
                   "knitr", "rmarkdown", "lme4"))
```

## 4. Running Scripts

- Open a lesson script (e.g., `R/L7-2.R`), and click **Source** in the upper-right corner (to run the entire file), or select lines and press **Ctrl+Enter** (Mac: **Cmd+Enter**) to execute line by line. **Stepping through line by line is recommended**, allowing you to read the comments alongside the console output.
- The first line of every script, `source("R/_setup.R")`, handles: locating the course directory (searching upward from the current working directory for a folder containing `data/clpn_sim_wide.csv`), configuring plot fonts, and loading shared helper functions (such as `clpn_estimate()`). This line expects the working directory to be the course directory, so please launch RStudio via `clpn-course.Rproj`. You do not need to run `_setup.R` separately, but reading through it is worthwhile.
- Output: text logs are saved to `R/output/Lx-y_log.txt`, and plots are saved to `R/output/Lx-y_*.png`.
- Run everything in one step: `source("R/run_all.R")`. This runs all lesson scripts and the final exam answer script `assess_answers.R` in syllabus order, followed by all solution scripts (`R/solutions/`). Total runtime is approximately 40–95 minutes (depending on hardware), with almost all execution time spent on bootstrap iterations; bootstrap defaults to a single core to ensure bitwise reproducibility. Results are summarized in `R/output/run_all_status.csv`. Real-data case scripts `data_elsoc.R` and `case_elsoc.R` are also included.

### Scripts with Upstream Dependencies

Running scripts in syllabus order will never encounter dependency issues. The scripts below read output files generated by upstream scripts in `R/output/`. The `R/output/` folder in the course package already contains reference results, so scripts can also be run immediately; however, if you modify and re-run an upstream script, downstream scripts will use your newly generated results. If a required file is missing (e.g., if `R/output/` was deleted), the script stops at the beginning with an informative message indicating which script must be run first.

| Script | Prerequisites |
|---|---|
| L6-5.R, solutions/L6-4_solution.R | L6-4.R (generates depression–anxiety example data `L6-4_dep_anx_items.csv`) |
| L10-1.R | L4-3.R (attrition data example `L4-3_data_with_attrition.csv`) |
| solutions/L4-3_solution.R | L4-3.R (`L4-3_data_with_attrition.csv`) |
| L10-2.R | L10-1.R (`L10-1_clean_data.csv`) |
| L10-2b.R | L10-1.R (`L10-1_clean_data.csv`) and L10-2.R (`L10-2_results.rds`, for edge-by-edge comparison against the primary analysis) |
| L10-3.R | L10-2.R (`L10-2_results.rds`) and L10-2b.R (`L10-2b_results.rds`) |
| solutions/L8-3_solution.R | L8-3.R (`L8-3_CS.csv`) and L8-2.R (`L8-2_boot.rds`) |
| case_elsoc.R | Bundled `data/elsoc_phq8_wide.csv` (written by data_elsoc.R from the bundled raw file) |

The capstone project forms an end-to-end pipeline: **L4-3 → L10-1 → L10-2 → L10-2b → L10-3**, where each step requires the output of the preceding step (L10-2b is the required full-procedure sensitivity analysis). All other lesson scripts (including L7-5b.R) depend only on the course dataset and can be run independently. For the real-data case study, you can run `case_elsoc.R` directly; run `data_elsoc.R` only if you want to verify the data preprocessing step (it reads the bundled raw file offline). See [Real-Data Case Study](../materials/case_elsoc.html) for detailed documentation.

### Computationally Intensive Scripts

`L8-2.R` (~7–15 min), `L8-3.R` (~5–25 min), and `L10-2.R` (~15–40 min)—these perform 1,000 bootstrap iterations, each fitting 9 cross-validated LASSO regressions (timings reflect measured ranges on a single core across different machines). While practicing, you can reduce `n_boots <- 1000` at the top of the script to `200`. The scripts default to `nCores = 1` (single core) so that `set.seed()` yields bitwise reproducible results. Setting this to `max(1, parallel::detectCores() - 1)` speeds up execution several-fold, but parallel resampling in bootnet is not fully governed by `set.seed()`, causing minor variations across runs. `L7-7.R` (optional advanced, group comparison: 3 × 1,000 permutations, ~2–4 min single-core; `NPERM <- 1000` can be lowered to `200`); `L7-6.R` (optional advanced, measurement invariance + sample size simulation) takes ~1 min; `case_elsoc.R` (real-data case study, 200 bootstraps) takes ~1–2 min (changing `B_BOOT <- 200` to `1000` adds several minutes); `L7-5b.R` and `L10-2b.R` (SEM re-estimation) take ~5–10 s each; `L5-3b.R` (RI-CLPM vs. data-generating truth: N = 200,000 population + 200 replications at N = 800) takes ~1–3 min; most other scripts finish within seconds. `data_elsoc.R` takes ~2 s (if downloading the raw file when missing, add several seconds to a minute depending on network speed).

## 5. Overview of Script Files

| Module | Scripts |
|---|---|
| M1 Statistical Foundations | L1-1 … L1-6 |
| M2 R Basics | L2-1 … L2-6 (L2-6 also renders `L2-6_report.Rmd`) |
| M3 Regression | L3-1 … L3-5 (L3-5 = LASSO and cross-validation) |
| M4 Longitudinal Data | L4-1 … L4-3 |
| M5 CLPM / RI-CLPM | L5-1 … L5-4 (L5-3b = comparison of RI-CLPM estimates against data-generating truth; L5-4 = causal inference simulations on confounding, measurement intervals, and stable traits) |
| M6 Network Psychometrics | L6-1 … L6-5 |
| M7 CLPN | L7-1 … L7-5 (L7-2 = core estimation, simplified "LASSO-only" CLPN); L7-5b = Wysocki et al. (2025) full procedure: LASSO edge selection → lavaan unpenalized re-estimation (same-wave residual covariances, FIML, cross-time invariance test) → in-/out-prediction |
| M8 Stability | L8-1 … L8-3 (bootstrap, CS-coefficient) |
| M9 Reporting | L9-2 (sensitivity analysis), L9-3 (reporting checklist + software versions) |
| M10 Capstone Project | L10-1 (data preparation and analysis plan), L10-2 (primary analysis: complete LASSO-only workflow), L10-2b (required sensitivity analysis: Wysocki et al., 2025 full procedure, edge-by-edge comparison against the primary analysis), L10-3 (automated results draft with both procedures side by side) |
| Real-Data Case Study | `case_elsoc.R` (CLPN of PHQ-8 with 200 bootstrap iterations, reading bundled `data/elsoc_phq8_wide.csv`, also executed by `run_all.R`), `data_elsoc.R` (regenerates analysis dataset from bundled raw file; downloads only if missing). Guide: [Real-Data Case Study](../materials/case_elsoc.html) |

Reading-only lessons (9.1) have no dedicated R scripts. `R/assess_answers.R` computes reference solutions for Part C of the final exam (saved to `R/output/assess_answers.csv`, where the course site reads them); work through Part C independently first before comparing with this script. For data specifications, see the [Data Dictionary](../data/data_dictionary.md).

## 6. Frequently Asked Questions

- **Missing font characters / box glyphs in plots**: In `_setup.R`, `plot_font` defaults to `"sans"` (standard clean sans-serif across platforms). If you need specific font rendering on your system, adjust `plot_font` in `_setup.R` to a font installed on your machine (e.g., `"Arial"`, `"Helvetica"`, or `"PingFang SC"` / `"Microsoft YaHei"` if displaying CJK characters).
- **"Cannot find course root" or `cannot open file 'R/_setup.R'`**: Your working directory is not set to the course directory. Always open the project by double-clicking `clpn-course.Rproj`, rather than opening `.R` files directly. Running `getwd()` in the R Console should output a path ending in `.../clpn-course-en` (or `.../clpn-course`). If `data/clpn_sim_wide.csv` is missing from the folder, the zip archive was not fully extracted, or the wrong directory was opened (see Section 2). Alternatively, you can temporarily select Session → Set Working Directory → Choose Directory… in RStudio and navigate to the course root folder.
- **"Missing prerequisite output file(s)"**: Follow the prompt and run the required upstream script first (see "Scripts with Upstream Dependencies").
- **Numbers differ slightly from the course notes**: `cv.glmnet` assigns cross-validation folds randomly; although all scripts set random seeds (`set.seed()`), subtle numerical differences may arise across R or package versions. Bootstrap scripts (L8-2, L8-3, L10-2) run on a single core by default, ensuring bitwise reproducible results under the same environment. **If you switch to parallel execution (`nCores > 1`), `set.seed()` cannot guarantee bitwise reproducibility across worker threads**, which may cause minor variations in the 2nd or 3rd decimal places of bootstrap intervals and CS-coefficients. When a CS-coefficient falls close to a grid boundary (e.g., in-EI), changing seeds or running in parallel can even cause it to jump between adjacent grid steps (e.g., 0.44 vs. 0.52). What matters substantively is the overall direction, magnitude, and stability pattern (see Lesson 9.2).
- **Error: `there is no package called '...'`**: The package has not been installed yet. Run `install.packages("package_name")`.
- **Quarto**: For the Quarto deliverable assigned in Lesson 10.2, navigate in RStudio to File → New File → Quarto Document, and paste code chunks from `L10-2.R`. An R Markdown template, `L2-6_report.Rmd`, is provided in this directory; its syntax and structure are nearly identical.

## 7. Exercise Solutions (`solutions/`)

Solution scripts are located in `R/solutions/`. Each solution script writes its output to `output/sol_<lesson>_log.txt` (and exports figures where applicable). `run_all.R` runs all solution scripts sequentially following the lesson scripts.

| Solution Script | Corresponding Exercise |
|---|---|
| L1-2, L1-3, L1-4, L1-5, L1-6 | Descriptive statistics, z-scores, correlation, sampling simulation, multiple testing (seed change + 200 replications) |
| L2-1 … L2-6 | First script (with intentional syntax error demonstration), vectors, dplyr, data import and checks, descriptives / correlation / regression, ggplot2 (with additional Quarto template `week06.qmd`) |
| L3-1 … L3-5 | Simple linear regression, multiple regression, standardization, logistic regression, LASSO |
| L4-1, L4-2, L4-3 | Variance decomposition and lme4 ICC, data reshaping, attrition analysis and MCAR comparison |
| L5-2, L5-3, L5-4 | CLPM model fitting and constraints, RI-CLPM random intercepts (correlations and 95% CIs), causal inference simulation exercises |
| L6-1, L6-2, L6-4, L6-5 | Adjacency matrix, partial correlation (adding direct effects; counting edges on course data), nodeNames and T1 / T2 network comparison, centrality indices |
| L7-2, L7-4 | CLPN estimation, out- / in-EI |
| L7-6, L7-7 (optional) | Longitudinal measurement invariance (5 depression items in the course data; 5 social well-being items in the coaches data), permutation test of the male vs. female T2 → T3 network |
| L8-1, L8-3 | Custom bootstrap with sample size vs. interval width, CS-coefficient |
| L9-2 | Top 5 strongest edges after controlling for gender and age covariates |

Hands-on exercises for Lessons 6.3, 7.3, 7.5, and 8.2 are completed directly by executing their primary lesson scripts; no separate solution scripts are required.
