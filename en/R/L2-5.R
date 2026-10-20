# =====================================================================
# L2-5.R  Descriptive Statistics, Correlation & Regression in R
# (Descriptives, correlation, regression in R)
# =====================================================================
source("R/_setup.R")
log_open("L2-5_log.txt")
dat <- read_course_data()
d <- data.frame(Loneliness = rowSums(dat[, paste0(lone_items, "_t1")]),
                Depression = rowSums(dat[, paste0(dep_items, "_t1")]),
                Social_support = dat$social_support_t1, Sleep = dat$sleep_hours_t1,
                Life_satisfaction = dat$life_sat_t1)
print(round(psych::describe(d)[, c("n", "mean", "sd", "min", "max", "skew")], 2))
ct <- suppressWarnings(psych::corr.test(d))                         # Correlation matrix + p-values
print(round(ct$r, 2)); print(round(ct$p, 4))
fit <- lm(Depression ~ Loneliness + Social_support, data = d)
print(summary(fit))
png_open("L2-5_pairs.png", 1800, 1800); psych::pairs.panels(d, ellipses = FALSE); invisible(dev.off())

# ---- Lesson Supplement: Confidence Intervals & Missing Data Demonstration ----
print(round(confint(fit), 3))                  # 95% confidence intervals
d_na <- d
d_na$Loneliness[c(3, 10, 25)] <- NA            # Artificially inject 3 missing values
print(cor(d_na$Loneliness, d_na$Social_support))                # NA propagation
print(cor(d_na$Loneliness, d_na$Social_support, use = "pairwise.complete.obs"))
print(nobs(lm(Depression ~ Loneliness, data = d_na)))        # lm deletes missing cases by default: 800 - 3
log_close()
