# =====================================================================
# L9-3.R  Reporting Standards: Verifiable Methods & Reproducible Results
#         (Reporting: versions, seeds, settings)
# Automatically generates an "Analysis Information Checklist" suitable for
# direct inclusion in Method sections or Supplementary Materials.
# =====================================================================
source("R/_setup.R")
log_open("L9-3_reporting_info.txt")
pk <- c("glmnet", "qgraph", "bootnet", "networktools", "lavaan", "psych", "tidyverse")
cat("== Software ==\n", R.version.string, "\n")
# Package versions use each package's own specification (the Version field in DESCRIPTION, e.g. "4.1-8" for glmnet).
# as.character(packageVersion(p)) replaces hyphens with dots ("4.1.8"), which diverges from sessionInfo() and CRAN notation.
for (p in pk) cat(sprintf("  %s %s\n", p, utils::packageDescription(p)$Version))
cat("\n== Essential Reporting Elements for CLPN Method Sections (Checklist) ==\n",
"[ ] Data: Sample size, number of waves, time lags, item wording, and scoring\n",
"[ ] Missing data & attrition handling (listwise deletion / multiple imputation / FIML)\n",
"[ ] Standardization: All items z-standardized prior to estimation\n",
"[ ] Estimation: Nodewise LASSO regression of each T2 item on all T1 items (glmnet, alpha = 1)\n",
"[ ] λ selection: 10-fold cross-validation lambda.min (or lambda.1se / EBIC, with gamma = ?)\n",
"[ ] Random seed: set.seed(2026)\n",
"[ ] Covariates and penalty specification (penalty.factor)\n",
"[ ] Centrality: out-EI / in-EI (excluding autoregressive edges), community definitions for bridge EI\n",
"[ ] Stability: Nonparametric bootstrap (number of replications), case-dropping CS-coefficient\n",
"[ ] Sensitivity analyses: λ tuning rules, random seeds, item redundancy trimming, T2→T3 replication\n",
"[ ] Software versions (see above) and code/data sharing repository links (e.g., OSF)\n")
# sessionInfo() enumerates all loaded packages (tidyverse alone attaches dozens), producing an extensive printout.
# The log retains only the opening segment: R version, platform, locale, and directly attached packages,
# truncating before "loaded via a namespace" (typically ~20 lines). Indirectly loaded packages are omitted from the log.
# The full session information is saved separately for supplementary materials.
# Packages must be loaded first so that sessionInfo() classifies them under "other attached packages".
suppressPackageStartupMessages(for (p in pk) library(p, character.only = TRUE))
si <- capture.output(print(sessionInfo()))
# In the public course repository, local BLAS/LAPACK paths, locale, and timezone strings (Matrix products ... tzcode) are omitted.
# In your own research, you do not need to omit these: they facilitate reproduction; decide beforehand whether you wish to disclose them.
a <- grep("^Matrix products", si)[1]; b <- grep("^attached base packages", si)[1]
if (!is.na(a) && !is.na(b) && b > a) si <- c(si[seq_len(a - 1)], "(Local paths, locale, and timezone omitted)", "", si[b:length(si)])
writeLines(si, out("sessionInfo_full.txt"))
k <- grep("^loaded via a namespace", si)[1]
n_show <- if (is.na(k)) min(25, length(si)) else k - 1
cat("\n== sessionInfo() (first ", n_show, " lines; full ", length(si), " lines in R/output/sessionInfo_full.txt) ==\n", sep = "")
cat(head(si, n_show), sep = "\n")
log_close()
