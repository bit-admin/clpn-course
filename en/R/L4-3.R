# =====================================================================
# L4-3.R  Missing data and participant attrition
# Artificially induce 20% attrition (participants with higher depression more prone to drop out = MAR/MNAR mechanism) to observe bias
# =====================================================================
source("R/_setup.R")
log_open("L4-3_log.txt")
dat <- read_course_data()
dat$dep_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])
dat$dep_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
dat$lone_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])

set.seed(43)
p_drop <- plogis(-2.0 + 0.25 * (dat$dep_t1 - mean(dat$dep_t1)))   # Higher T1 depression -> higher dropout probability
drop <- rank(-(p_drop + runif(nrow(dat), 0, .3))) <= 0.2 * nrow(dat)  # Exactly 20% attrition
dat$dropout <- as.integer(drop)
obs <- dat; obs[drop, grep("_t2$|_t3$", names(obs))] <- NA       # Dropouts have missing T2/T3 data
obs$dep_t2[drop] <- NA
cat("Attrition rate =", mean(drop), "\n")
cat("T2 depression mean: full data", round(mean(dat$dep_t2), 2),
    "; after listwise deletion", round(mean(obs$dep_t2, na.rm = TRUE), 2), "(underestimated)\n")
cat("r(T1 loneliness, T2 depression): full", round(cor(dat$lone_t1, dat$dep_t2), 3),
    "; listwise deletion", round(cor(obs$lone_t1, obs$dep_t2, use = "complete.obs"), 3), "\n\n")
# Attrition analysis: compare T1 characteristics between dropouts and retainees
print(t.test(dep_t1 ~ dropout, data = dat))
print(chisq.test(table(dat$gender, dat$dropout)))
# Multiple imputation (mice) -- for conceptual understanding
imp <- mice::mice(obs[, c("dep_t1", "lone_t1", "gender", "dep_t2")], m = 5, printFlag = FALSE, seed = 1)
est <- mice::pool(with(imp, lm(dep_t2 ~ 1)))
cat("\nT2 depression mean after multiple imputation ≈", round(summary(est)$estimate, 2), "(closer to truth)\n")
write.csv(obs[, !names(obs) %in% c("dep_t1", "dep_t2", "lone_t1")], out("L4-3_data_with_attrition.csv"),
          row.names = FALSE)
# FIML (Full Information Maximum Likelihood): in lavaan, simply specify missing = "ml", but include auxiliary variables related to missingness
suppressPackageStartupMessages(library(lavaan))
o <- obs
f0 <- suppressWarnings(sem("dep_t2 ~~ dep_t2", data = o, missing = "ml", meanstructure = TRUE))
cat("\nFIML (a) dep_t2 only:\n"); print(parameterEstimates(f0)[2, c("lhs", "op", "est")], digits = 4)
m  <- "dep_t2 ~~ dep_t1 + lone_t1
       dep_t1 ~~ lone_t1"
f1 <- sem(m, data = o[, c("dep_t1", "dep_t2", "lone_t1")], missing = "ml", meanstructure = TRUE)
pe <- parameterEstimates(f1); cat("FIML (b) including T1 depression and T1 loneliness:\n"); print(pe[pe$op == "~1", c("lhs", "est", "se")], digits = 4)
ss <- standardizedSolution(f1)
cat("FIML estimated r(T1 loneliness, T2 depression) =", sprintf("%.3f", ss$est.std[ss$lhs == "dep_t2" & ss$rhs == "lone_t1"]), "\n")
# Exception: when attrition depends solely on predictors (T1 depression), complete-case regression coefficients are not systematically biased
# (compare with the mean and correlation above: both were distorted by listwise deletion)
b_full <- coef(lm(dep_t2 ~ dep_t1 + lone_t1, data = dat))
b_cc   <- coef(lm(dep_t2 ~ dep_t1 + lone_t1, data = obs))     # lm() uses listwise deletion by default
cat("\nRegression coefficients for dep_t2 ~ dep_t1 + lone_t1 (full data vs. listwise deletion):\n")
print(round(rbind(`Full data` = b_full, `Listwise deletion` = b_cc), 3))
log_close()
