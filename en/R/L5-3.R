# =====================================================================
# L5-3.R  RI-CLPM: separating stable trait differences from within-person fluctuations
# Syntax structure follows the lavaan example in Mulder & Hamaker (2021)
# =====================================================================
source("R/_setup.R")
library(lavaan)
log_open("L5-3_log.txt")
dat <- read_course_data()
wide <- data.frame(id = dat$id)
for (t in 1:3) {
  wide[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
  wide[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)])
}
riclpm <- '
  # 1) Random intercepts: stable individual "trait levels", factor loadings fixed to 1
  RI_lone =~ 1*lone1 + 1*lone2 + 1*lone3
  RI_dep  =~ 1*dep1  + 1*dep2  + 1*dep3
  # 2) Within-person components
  wl1 =~ 1*lone1; wl2 =~ 1*lone2; wl3 =~ 1*lone3
  wd1 =~ 1*dep1;  wd2 =~ 1*dep2;  wd3 =~ 1*dep3
  # 3) Within-person autoregressions and cross-lags
  wl2 ~ wl1 + wd1;  wd2 ~ wd1 + wl1
  wl3 ~ wl2 + wd2;  wd3 ~ wd2 + wl2
  # 4) Synchronous covariances and (residual) variances
  wl1 ~~ wd1; wl2 ~~ wd2; wl3 ~~ wd3
  wl1 ~~ wl1; wd1 ~~ wd1; wl2 ~~ wl2; wd2 ~~ wd2; wl3 ~~ wl3; wd3 ~~ wd3
  RI_lone ~~ RI_lone; RI_dep ~~ RI_dep; RI_lone ~~ RI_dep
  # 5) Random intercepts uncorrelated with T1 within-person components; indicator measurement errors fixed to 0
  RI_lone ~~ 0*wl1 + 0*wd1;  RI_dep ~~ 0*wl1 + 0*wd1
  lone1 ~~ 0*lone1; lone2 ~~ 0*lone2; lone3 ~~ 0*lone3
  dep1 ~~ 0*dep1;   dep2 ~~ 0*dep2;   dep3 ~~ 0*dep3
'
fit_ri <- lavaan(riclpm, data = wide, missing = "fiml", meanstructure = TRUE, int.ov.free = TRUE)
print(summary(fit_ri, standardized = TRUE, fit.measures = TRUE))   # print(): ensures output is logged when running via source() or run_all.R

clpm <- 'lone2 ~ lone1 + dep1; dep2 ~ dep1 + lone1; lone3 ~ lone2 + dep2; dep3 ~ dep2 + lone2
         lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3'
fit_c <- sem(clpm, data = wide, missing = "fiml")
get <- function(f) { pe <- standardizedSolution(f); pe <- pe[pe$op == "~", ]
  setNames(round(pe$est.std, 3), paste(pe$rhs, "→", pe$lhs)) }
cat("\n===== CLPM vs. RI-CLPM Standardized Paths =====\nCLPM:\n"); print(get(fit_c))
cat("RI-CLPM (within-person):\n"); print(get(fit_ri))
print(anova(fit_c, fit_ri))
cat("Simulated data were generated with strong stable traits: RI-CLPM autoregressions drop markedly, showing that\n",
    "much of the CLPM's \"stability\" arises from between-person differences. Standard CLPN shares this limitation (Lesson 7.5).\n")
log_close()
