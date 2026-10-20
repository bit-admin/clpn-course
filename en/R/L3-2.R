# =====================================================================
# L3-2.R  Multiple regression and "controlling for other variables"
# Key link: A cross-lagged edge in CLPN = a regression coefficient
#           "controlling for all other T1 variables"
# =====================================================================
source("R/_setup.R")
log_open("L3-2_log.txt")
dat <- read_course_data()
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])
dat$dep_sum_t1  <- rowSums(dat[, paste0(dep_items, "_t1")])
dat$dep_sum_t2  <- rowSums(dat[, paste0(dep_items, "_t2")])

m1 <- lm(dep_sum_t2 ~ lone_sum_t1, data = dat)                                   # Loneliness alone
m2 <- lm(dep_sum_t2 ~ lone_sum_t1 + social_support_t1 + sleep_hours_t1, data = dat)
m3 <- lm(dep_sum_t2 ~ lone_sum_t1 + dep_sum_t1, data = dat)                      # Controlling for T1 depression!
cat("Loneliness coefficients: alone", round(coef(m1)[2], 3), "; +support+sleep", round(coef(m2)[2], 3),
    "; +T1 depression (cross-lagged)", round(coef(m3)[2], 3), "\n\n")
print(summary(m3))
cat("m3 is a \"mini-CLPM\": T2 depression ~ T1 depression (autoregression) + T1 loneliness (cross-lagged).\n")

# ---- Full coefficients of m2 and hand-calculated VIF for loneliness (second code box in lesson) ----
cat("\nm2 coefficients (loneliness + social support + sleep) and VIF for loneliness:\n")
print(round(summary(m2)$coefficients, 3))
r2_lone <- summary(lm(lone_sum_t1 ~ social_support_t1 + sleep_hours_t1, data = dat))$r.squared
print(round(1 / (1 - r2_lone), 3))      # VIF = 1 / (1 - R²)

# ---- Multicollinearity demonstration: an almost duplicate predictor (third code box in lesson) ----
# No random numbers were used earlier in this script, so set.seed(1) here yields results identical to R/solutions/L3-2_solution.R
cat("\nCollinearity demo: loneliness sum score + slight noise \"copy\"\n")
set.seed(1)
dat$lone_copy <- dat$lone_sum_t1 + rnorm(800, 0, 0.3)   # Loneliness sum score + slight noise
print(round(cor(dat$lone_sum_t1, dat$lone_copy), 3))
print(round(summary(lm(dep_sum_t2 ~ lone_sum_t1, data = dat))$coefficients[2, 1:2], 3))
print(round(summary(lm(dep_sum_t2 ~ lone_sum_t1 + lone_copy, data = dat))$coefficients[, 1:2], 3))

# ---- Two-step understanding of \"controlling\" (Frisch–Waugh) ----
cat("\nFrisch–Waugh: Portion of loneliness unrelated to T1 depression -> predicting T2 depression\n")
ex <- resid(lm(lone_sum_t1 ~ dep_sum_t1, data = dat))   # Portion of loneliness unrelated to T1 depression
print(round(coef(lm(dat$dep_sum_t2 ~ ex))[2], 4))       # = coefficient of loneliness in m3
log_close()
