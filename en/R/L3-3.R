# =====================================================================
# L3-3.R  Standardized coefficients and results interpretation
# =====================================================================
source("R/_setup.R")
log_open("L3-3_log.txt")
dat <- read_course_data()
d <- data.frame(dep2  = rowSums(dat[, paste0(dep_items, "_t2")]),
                lone1 = rowSums(dat[, paste0(lone_items, "_t1")]),
                dep1  = rowSums(dat[, paste0(dep_items, "_t1")]))
dz <- as.data.frame(scale(d))                     # Standardize all variables first -> coefficients are beta
fit <- lm(dep2 ~ lone1 + dep1, data = dz)
ci <- confint(fit)                                # 95% confidence intervals
s <- summary(fit)$coefficients
for (v in c("lone1", "dep1")) {
  cat(sprintf("%s: β = %.2f, 95%% CI [%.2f, %.2f], p %s\n", v, s[v, 1], ci[v, 1], ci[v, 2],
              ifelse(s[v, 4] < .001, "< .001", sprintf("= %.3f", s[v, 4]))))
}
cat("\nAPA style example: After controlling for T1 depression, T1 loneliness positively predicted T2 depression (β = ",
    round(s["lone1", 1], 2), "). Note the use of \"predicted\" rather than \"caused\".\n", sep = "")

# ---- Compare b and beta for m2 (predictors with different units; second code box in lesson) ----
cat("\nm2: Loneliness + social support + sleep predicting T2 depression, unstandardized b and standardized beta:\n")
d$support <- dat$social_support_t1
d$sleep   <- dat$sleep_hours_t1
f_b    <- lm(dep2 ~ lone1 + support + sleep, data = d)
f_beta <- lm(dep2 ~ lone1 + support + sleep, data = as.data.frame(scale(d)))
print(round(cbind(b = coef(f_b), beta = coef(f_beta)), 3))

# ---- Hand-calculate beta, and unit conversion experiment (third code box in lesson) ----
cat("\nHand-calculate beta for loneliness = b * sd(x) / sd(y):\n")
print(round(coef(f_b)["lone1"] * sd(d$lone1) / sd(d$dep2), 3))
d$sleep_min <- d$sleep * 60                      # Convert sleep to minutes
cat("b after converting sleep to minutes (= b in hours / 60):\n")
print(round(coef(lm(dep2 ~ lone1 + support + sleep_min, data = d))["sleep_min"], 4))
log_close()
