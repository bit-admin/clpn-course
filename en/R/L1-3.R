# =====================================================================
# L1-3.R  Standardization & z-Scores
# (Standardization & z-scores)
# z = (x - mean) / SD: converts variables of different scales to "SDs from the mean"
# =====================================================================
source("R/_setup.R")
log_open("L1-3_log.txt")
dat <- read_course_data()

x <- c(8, 10, 9, 14, 7, 12)
z <- (x - mean(x)) / sd(x)                       # Manually calculate z-scores
print(round(cbind(raw_score = x, z_score = z, scale_func = as.numeric(scale(x))), 3))
cat("Mean of z-scores =", round(mean(z), 10), ", SD =", sd(z), "\n\n")

# Two variables on completely different scales: sleep problems (0-3) and life satisfaction (0-100)
zz <- scale(dat[, c("dep3_t1", "life_sat_t1")])   # scale() standardizes each column
print(round(head(cbind(dat[, c("dep3_t1", "life_sat_t1")], zz)), 2))
cat("\nAfter standardization, both columns have mean ≈ 0 and SD = 1, allowing direct comparison of 'relative positions'.\n")
cat("In CLPN, we standardize all items first so regression coefficients are comparable (standardized coefficients).\n")

# Verifying two properties: correlation and skewness are invariant under standardization (third code box in lesson)
cat("\nCorrelation (raw vs. standardized) and dep1_t1 skewness (raw vs. standardized):\n")
print(round(cor(dat$dep3_t1, dat$life_sat_t1), 4))   # Correlation of raw scores
print(round(cor(zz[, 1], zz[, 2]), 4))                 # Correlation of standardized scores
print(round(psych::skew(dat$dep1_t1), 3))              # Skewness: raw scores
print(round(psych::skew(scale(dat$dep1_t1)[, 1]), 3))  # Skewness: standardized scores
log_close()
