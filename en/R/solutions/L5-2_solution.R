# Solution L5-2: APA reporting of CLPM cross-lagged paths and fit indices;
# equality constraint test (anova(fit_eq, fit))
source("R/_setup.R"); library(lavaan)
log_open("sol_L5-2_log.txt")
dat <- read_course_data(); w <- data.frame(row.names = dat$id)
for (t in 1:3) { w[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
                 w[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)]) }
fit <- sem('lone2 ~ lone1 + dep1; dep2 ~ dep1 + lone1; lone3 ~ lone2 + dep2; dep3 ~ dep2 + lone2
            lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3', data = w, missing = "fiml")
ss <- standardizedSolution(fit); ss <- ss[ss$op == "~" & substr(ss$lhs, 1, 3) != substr(ss$rhs, 1, 3), ]
for (i in seq_len(nrow(ss))) cat(sprintf("%s → %s: beta = %.2f, 95%% CI [%.2f, %.2f], p %s\n", ss$rhs[i], ss$lhs[i],
  ss$est.std[i], ss$ci.lower[i], ss$ci.upper[i], ifelse(ss$pvalue[i] < .001, "< .001", sprintf("= %.3f", ss$pvalue[i]))))
fm <- fitMeasures(fit, c("chisq", "df", "cfi", "rmsea", "srmr"))
cat(sprintf("Fit: chi^2(%d) = %.2f, CFI = %.3f, RMSEA = %.3f, SRMR = %.3f\n", fm["df"], fm["chisq"], fm["cfi"], fm["rmsea"], fm["srmr"]))
# Key takeaway: Low CFI and high RMSEA -> poor CLPM fit; one primary reason is ignoring stable traits (see Lesson 5.3 RI-CLPM).

# ---- Exercise: "Equality constraint test" - constraining corresponding paths across T1->T2 and T2->T3 to be equal ----
clpm_eq <- '
  lone2 ~ a*lone1 + c*dep1
  dep2  ~ b*dep1  + d*lone1
  lone3 ~ a*lone2 + c*dep2      # Identical labels = equality constraints
  dep3  ~ b*dep2  + d*lone2
  lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3
'
fit_eq <- sem(clpm_eq, data = w, missing = "fiml")
cat("\nNested model chi^2 difference test anova(fit_eq, fit):\n")
print(anova(fit_eq, fit))
lrt <- anova(fit_eq, fit)
cat(sprintf("Delta chi^2(%d) = %.2f, p = %.3f\n", lrt[2, "Df diff"], lrt[2, "Chisq diff"], lrt[2, "Pr(>Chisq)"]))
cat(sprintf("AIC: constrained model %.0f, unconstrained model %.0f; BIC: constrained model %.0f, unconstrained model %.0f\n",
            AIC(fit_eq), AIC(fit), BIC(fit_eq), BIC(fit)))
fe <- fitMeasures(fit_eq, c("chisq", "df", "pvalue", "cfi", "rmsea"))
cat(sprintf("Fit of constrained model itself: chi^2(%d) = %.2f, CFI = %.3f, RMSEA = %.3f\n", fe["df"], fe["chisq"], fe["cfi"], fe["rmsea"]))
log_close()
