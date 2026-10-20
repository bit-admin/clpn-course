# Exercise Solutions L3-3: Rerunning Lesson 3.2 models after standardization and reporting in APA style
source("R/_setup.R")
log_open("sol_L3-3_log.txt")
dat <- read_course_data()
d <- as.data.frame(scale(data.frame(dep2 = rowSums(dat[, paste0(dep_items, "_t2")]),
  lone = rowSums(dat[, paste0(lone_items, "_t1")]), support = dat$social_support_t1, sleep = dat$sleep_hours_t1)))
fit <- lm(dep2 ~ lone + support + sleep, d); s <- summary(fit)$coef; ci <- confint(fit)
# APA style: p-values are never reported as 0.000; when p < .001 report 'p < .001', otherwise keep 3 decimal places without leading zero
fmt_p <- function(p) ifelse(p < .001, "p < .001", paste("p =", sub("^0", "", sprintf("%.3f", p))))
for (v in c("lone", "support", "sleep"))
  cat(sprintf("%s: beta = %.2f, 95%% CI [%.2f, %.2f], %s\n", v, s[v, 1], ci[v, 1], ci[v, 2], fmt_p(s[v, 4])))
cat(sprintf("APA: Controlling for social support and sleep duration, T1 loneliness positively predicted T2 depression, beta = %.2f, 95%% CI [%.2f, %.2f], %s.\n",
    s["lone", 1], ci["lone", 1], ci["lone", 2], fmt_p(s["lone", 4])))

# ---- 3.3-A: Tabular format from lecture notes (beta, 95% CI, p) and R^2 ----
cat("\n3.3-A: beta, 95% CI, p (tabular format for the same model)\n")
print(round(cbind(beta = coef(fit), ci, p = s[, 4]), 3))
cat("R^2 =", round(summary(fit)$r.squared, 3), "\n")

# ---- 3.3-B (1): Hand-calculating beta = b * s_x / s_y for T1 depression from m3 (unstandardized) ----
raw <- data.frame(dep2 = rowSums(dat[, paste0(dep_items, "_t2")]),
                  lone1 = rowSums(dat[, paste0(lone_items, "_t1")]),
                  dep1 = rowSums(dat[, paste0(dep_items, "_t1")]))
m3 <- lm(dep2 ~ lone1 + dep1, data = raw)
cat("\n3.3-B: b(T1 depression) =", round(coef(m3)["dep1"], 3), " s(T1 depression) =", round(sd(raw$dep1), 3),
    " s(T2 depression) =", round(sd(raw$dep2), 3), "\n")
cat("beta = b * s_x / s_y =", round(coef(m3)["dep1"] * sd(raw$dep1) / sd(raw$dep2), 3),
    "; Estimated directly after standardization: ", round(coef(lm(dep2 ~ lone1 + dep1, data = as.data.frame(scale(raw))))["dep1"], 3), "\n")
# 3.3-B (2): A 0/1 variable has SD approx 0.5; "Female vs. Male" differs by 1 raw unit ≈ beta / s(gender) SDs of y
cat("Gender (0/1) SD =", round(sd(dat$gender), 3), "\n")
log_close()
