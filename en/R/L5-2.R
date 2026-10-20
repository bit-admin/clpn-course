# =====================================================================
# L5-2.R  Fitting CLPM with lavaan and evaluating model fit
# =====================================================================
source("R/_setup.R")
library(lavaan)
log_open("L5-2_log.txt")
dat <- read_course_data()
wide <- data.frame(id = dat$id)
for (t in 1:3) {                                   # Construct sum scores
  wide[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
  wide[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)])
}
clpm <- '
  lone2 ~ lone1 + dep1      # T2 loneliness predicted by T1 loneliness (AR) and T1 depression (CL)
  dep2  ~ dep1  + lone1
  lone3 ~ lone2 + dep2
  dep3  ~ dep2  + lone2
  lone1 ~~ dep1             # ~~ denotes (residual) covariance
  lone2 ~~ dep2
  lone3 ~~ dep3
'
fit <- sem(clpm, data = wide, missing = "fiml")   # FIML: full information maximum likelihood for missing data
print(summary(fit, standardized = TRUE, fit.measures = TRUE))   # print(): ensures output is logged when running via source() or run_all.R
pe <- parameterEstimates(fit, standardized = TRUE)
print(pe[pe$op == "~", c("lhs", "op", "rhs", "std.all", "ci.lower", "ci.upper", "pvalue")], digits = 3)
print(round(fitMeasures(fit, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr")), 3))
cat("Note: CFI >= .95, RMSEA <= .06, and SRMR <= .08 are commonly used benchmarks for \"good fit\".\n")
# Standardized estimates should be paired with standardized confidence intervals:
# standardizedSolution() uses the delta method to compute SE and 95% CI for est.std
# (the ci.lower / ci.upper from parameterEstimates() above belong to unstandardized estimates and cannot be interpreted alongside std.all)
cat("\nStandardized solution (standardizedSolution): standardized regression estimates and 95% CIs\n")
ssol <- standardizedSolution(fit)
print(ssol[ssol$op == "~", c("lhs", "op", "rhs", "est.std", "se", "ci.lower", "ci.upper", "pvalue")], digits = 3)
saveRDS(wide, out("L5_sumscores.rds"))
log_close()
