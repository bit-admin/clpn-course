# Solution L5-3 Exercise 3: Variance of random intercepts and between-person correlation
source("R/_setup.R")
suppressPackageStartupMessages(library(lavaan))
log_open("sol_L5-3_log.txt")
dat <- read_course_data()
wide <- data.frame(id = dat$id)
for (t in 1:3) {
  wide[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
  wide[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)])
}
riclpm <- '
  RI_lone =~ 1*lone1 + 1*lone2 + 1*lone3
  RI_dep  =~ 1*dep1  + 1*dep2  + 1*dep3
  wl1 =~ 1*lone1; wl2 =~ 1*lone2; wl3 =~ 1*lone3
  wd1 =~ 1*dep1;  wd2 =~ 1*dep2;  wd3 =~ 1*dep3
  wl2 ~ wl1 + wd1;  wd2 ~ wd1 + wl1
  wl3 ~ wl2 + wd2;  wd3 ~ wd2 + wl2
  wl1 ~~ wd1; wl2 ~~ wd2; wl3 ~~ wd3
  wl1 ~~ wl1; wd1 ~~ wd1; wl2 ~~ wl2; wd2 ~~ wd2; wl3 ~~ wl3; wd3 ~~ wd3
  RI_lone ~~ RI_lone; RI_dep ~~ RI_dep; RI_lone ~~ RI_dep
  RI_lone ~~ 0*wl1 + 0*wd1;  RI_dep ~~ 0*wl1 + 0*wd1
  lone1 ~~ 0*lone1; lone2 ~~ 0*lone2; lone3 ~~ 0*lone3
  dep1 ~~ 0*dep1;   dep2 ~~ 0*dep2;   dep3 ~~ 0*dep3
'
fit <- lavaan(riclpm, data = wide, missing = "fiml", meanstructure = TRUE, int.ov.free = TRUE)
ss <- standardizedSolution(fit)
ri <- ss[ss$op == "~~" & ss$lhs %in% c("RI_lone", "RI_dep") & ss$rhs %in% c("RI_lone", "RI_dep"), c("lhs", "op", "rhs", "est.std")]
pe <- parameterEstimates(fit)
ri$unstandardized_est <- pe$est[match(paste(ri$lhs, ri$rhs), paste(pe$lhs, pe$rhs))]
ri$est.std <- round(ri$est.std, 3); ri$unstandardized_est <- round(ri$unstandardized_est, 3); print(ri, row.names = FALSE)
r_ri <- ri$est.std[ri$lhs == "RI_lone" & ri$rhs == "RI_dep"]
ci <- ss[ss$lhs == "RI_lone" & ss$rhs == "RI_dep", c("ci.lower", "ci.upper")]
cat("\nCorrelation between the two random intercepts (stable traits) =", sprintf("%.3f", r_ri), ", 95% CI [", round(ci[[1]], 2), ",", round(ci[[2]], 2), "]",
    "(true latent trait correlation set in simulation is 0.50)\n")
# Proportion of stable variance: random intercept variance / observed sum score variance
for (v in c("lone", "dep")) {
  vri <- pe$est[pe$lhs == paste0("RI_", v) & pe$rhs == paste0("RI_", v)]
  vtot <- mean(sapply(1:3, function(t) var(wide[[paste0(v, t)]])))
  cat(sprintf("%s: Random intercept variance = %.2f, mean observed sum score variance = %.2f, proportion of stable variance ≈ %.2f\n", v, vri, vtot, vri / vtot))
}
log_close()
