# Solution L4-3: Supplementary attrition analysis (4.3-A); MCAR control group (4.3-B);
# Omission of key variables from imputation model (4.3-C)
source("R/_setup.R")
log_open("sol_L4-3_log.txt")
dat <- read_course_data()                      # Attrition generation process identical to R/L4-3.R
dat$dep_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])
dat$dep_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
dat$lone_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])
set.seed(43)
p_drop <- plogis(-2.0 + 0.25 * (dat$dep_t1 - mean(dat$dep_t1)))
drop <- rank(-(p_drop + runif(nrow(dat), 0, .3))) <= 0.2 * nrow(dat)
dat$dropout <- as.integer(drop)
# ---- 4.3-A: Supplementary comparison of T1 loneliness and age ----
for (v in c("dep_t1", "lone_t1", "age")) {
  tt <- t.test(dat[[v]] ~ dat$dropout)
  cat(sprintf("%-8s Retained M = %.2f, Dropout M = %.2f; Welch t(%.1f) = %.2f, p = %s\n", v, tt$estimate[1], tt$estimate[2],
              tt$parameter, tt$statistic, format.pval(tt$p.value, digits = 3, eps = .001)))
}
d <- with(dat, (mean(dep_t1[dropout == 1]) - mean(dep_t1[dropout == 0])) / sd(dep_t1))
cat("Standardized difference in T1 depression (using total-sample SD) d ≈", round(d, 2), "\n")
sp <- with(dat, sqrt(((sum(dropout == 1) - 1) * var(dep_t1[dropout == 1]) + (sum(dropout == 0) - 1) * var(dep_t1[dropout == 0])) /
                     (nrow(dat) - 2)))                          # Pooled within-group SD
cat("Standardized difference in T1 depression (using pooled within-group SD, i.e., conventional Cohen's d) d ≈",
    round(with(dat, (mean(dep_t1[dropout == 1]) - mean(dep_t1[dropout == 0])) / sp), 2), "\n\n")
# ---- 4.3-B: MCAR comparison ----
set.seed(1)
drop_mcar <- sample(c(rep(TRUE, 160), rep(FALSE, 640)))
cat("Complete data: T2 depression mean =", round(mean(dat$dep_t2), 2), "; r(T1 loneliness, T2 depression) =", round(cor(dat$lone_t1, dat$dep_t2), 3), "\n")
cat("MCAR listwise deletion: T2 depression mean =", round(mean(dat$dep_t2[!drop_mcar]), 2),
    "; r =", round(cor(dat$lone_t1[!drop_mcar], dat$dep_t2[!drop_mcar]), 3), "\n")
tm <- t.test(dat$dep_t1 ~ drop_mcar)
cat("MCAR attrition analysis (T1 depression): p =", round(tm$p.value, 3), "(mostly non-significant)\n")
# ---- 4.3-C: Omission of key variables from imputation model ----
need_output("L4-3_data_with_attrition.csv", "R/L4-3.R")
o <- read.csv(out("L4-3_data_with_attrition.csv"))
o$dep_t1  <- rowSums(o[, paste0(dep_items, "_t1")])
o$dep_t2  <- rowSums(o[, paste0(dep_items, "_t2")])
o$lone_t1 <- rowSums(o[, paste0(lone_items, "_t1")])
imp_a <- mice::mice(o[, c("dep_t1", "lone_t1", "gender", "dep_t2")], m = 5, printFlag = FALSE, seed = 1)
imp_b <- mice::mice(o[, c("lone_t1", "gender", "dep_t2")], m = 5, printFlag = FALSE, seed = 1)
ea <- summary(mice::pool(with(imp_a, lm(dep_t2 ~ 1))))$estimate
eb <- summary(mice::pool(with(imp_b, lm(dep_t2 ~ 1))))$estimate
cat("\n4.3-C T2 depression mean after multiple imputation (true value", round(mean(dat$dep_t2), 2), "; listwise deletion",
    round(mean(o$dep_t2, na.rm = TRUE), 2), "):\n")
cat("(a) Imputation model includes dep_t1, lone_t1, gender:", round(ea, 2), "\n")
cat("(b) Omitting dep_t1, using only lone_t1 and gender:  ", round(eb, 2), "\n")
log_close()
