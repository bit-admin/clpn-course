# =====================================================================
# L10-1.R  Capstone Project ①: Data Preparation, Codebook, & Analysis Plan
#          (Data prep, codebook, analysis plan)
# =====================================================================
source("R/_setup.R")
need_output("L4-3_data_with_attrition.csv", "R/L4-3.R", chain = "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-2b.R → R/L10-3.R")   # Prerequisite check
suppressPackageStartupMessages(library(tidyverse))
log_open("L10-1_log.txt")
raw <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)

# 1) Data cleaning checks: score ranges, duplicate IDs, missingness
item_cols <- c(vars_t(1), vars_t(2), vars_t(3))
rng <- sapply(raw[item_cols], range)
cat("Score ranges for all items:\n"); print(rng)
# Checking only min and max is insufficient: non-integers (e.g. 2.5) or out-of-range zeros in 1–4 scales
# can still fall within the overall range.
# Therefore, check each value against the set of valid scores (Loneliness: 1, 2, 3, 4; Depression: 0, 1, 2, 3).
allowed <- function(v) if (startsWith(v, "lone")) 1:4 else 0:3
n_bad <- sapply(item_cols, function(v) sum(!is.na(raw[[v]]) & !(raw[[v]] %in% allowed(v))))
cat("Count of values outside permitted sets (out-of-bounds, non-integers): total =", sum(n_bad), "\n")
if (any(n_bad > 0)) print(n_bad[n_bad > 0])
stopifnot(all(n_bad == 0))
cat("Duplicate IDs =", sum(duplicated(raw$id)), "; total missing values =", sum(is.na(raw)), "\n")
# (For reverse-scored items: raw <- raw |> mutate(item_r = 5 - item); no reverse-scored items in this dataset)

# 2) Attrition analysis template (no attrition in this dataset; if using L4-3 attrition data, replace filename directly)
att <- read_csv(out("L4-3_data_with_attrition.csv"), show_col_types = FALSE)  # Requires running L4-3.R first
att$stay <- !is.na(att$dep1_t2)
cat("\n(Attrition data example) Retention rate =", round(mean(att$stay), 3), "\n")
print(att |> group_by(stay) |> summarise(T1_depression = mean(rowSums(across(dep1_t1:dep5_t1))),
                                         T1_loneliness = mean(rowSums(across(lone1_t1:lone4_t1))), n = n()))

# 3) Codebook: variables + descriptive statistics (item text merged in Part 5 at end of script)
dict <- read.csv("data/data_dictionary.csv", fileEncoding = "UTF-8")
cb <- data.frame(variable = item_cols, mean = round(colMeans(raw[item_cols]), 2),
                 sd = round(sapply(raw[item_cols], sd), 2))
write.csv(cb, out("L10-1_codebook_stats.csv"), row.names = FALSE)
clean <- raw |> select(id, all_of(item_cols), gender, age)
write_csv(clean, out("L10-1_clean_data.csv"))

# 4) One-page analysis plan (preregistration template; drafted before examining results!)
plan <- c("# Analysis Plan (Preregistration Template)",
  "Research Question: To what extent do T1 loneliness items uniquely predict T2 depression items, and vice versa? (Avoid causal phrasing such as 'causes' or 'leads to')",
  "Nodes: lone1–lone4, dep1–dep5 (9 items); Time Intervals: T1→T2 (primary analysis), T2→T3 (replication)",
  "Estimation: Nodewise LASSO regression (glmnet), 10-fold CV, lambda.min; set.seed(2026); items z-standardized",
  "Centrality: out-EI, in-EI, bridge out/in-EI (communities = Loneliness/Depression), excluding autoregressive edges",
  "Stability: Nonparametric bootstrap (1,000 replications); case-dropping bootstrap (1,000 replications), interpreting rank order only if CS >= 0.25",
  "Sensitivity: lambda.1se; including gender and age as unpenalized covariates; T2→T3 replication",
  paste0("Sensitivity (Required): Full procedure of Wysocki et al. (2025) (R/L10-2b.R): LASSO edge selection (T1→T2 and T2→T3, fixed to 0 only if 0 in both lags) ",
         "-> unpenalized SEM re-estimation in lavaan (cross-sectional residual covariances within wave, FIML) ",
         "-> cross-time invariance testing (nested chi-square + AIC/BIC) to select final model -> pruning at p < .01 ",
         "-> in-/out-prediction; report edge-by-edge concordance with primary analysis, interpreting discordant edges exploratorily only"),
  "Missing Data: No missing data in this dataset; if present, report attrition analysis and apply multiple imputation (or FIML)")
writeLines(plan, out("L10-1_analysis_plan.md")); cat("\n", plan, sep = "\n")

# 5) Complete codebook: item text, score definitions, waves + descriptive statistics
# In data_dictionary.csv, one row covers three waves for an item (e.g. "lone1_t1 / _t2 / _t3"). Extract item name before matching.
dict$item <- sub("_t1.*$", "", dict$variable)
codebook <- data.frame(variable = item_cols,
                       item = sub("_t[0-9]+$", "", item_cols),
                       wave = as.integer(sub("^.*_t", "", item_cols)))
codebook <- merge(codebook, dict[, c("item", "label", "values")], by = "item", sort = FALSE)
codebook <- merge(codebook, cb, by = "variable", sort = FALSE)
codebook <- codebook[match(item_cols, codebook$variable),
                     c("variable", "wave", "label", "values", "mean", "sd")]
stopifnot(nrow(codebook) == length(item_cols), !anyNA(codebook$label))
write.csv(codebook, out("L10-1_codebook.csv"), row.names = FALSE, fileEncoding = "UTF-8")
cat("\nCodebook (R/output/L10-1_codebook.csv, ", nrow(codebook), " rows; displaying T1 items only):\n", sep = "")
print(codebook[codebook$wave == 1, c("variable", "label", "mean", "sd")], row.names = FALSE)
log_close()
