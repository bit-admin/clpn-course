# =====================================================================
# L1-4.R  Covariance & Correlation
# (Covariance & correlation)
# =====================================================================
source("R/_setup.R")
log_open("L1-4_log.txt")
dat <- read_course_data()
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])
dat$dep_sum_t1  <- rowSums(dat[, paste0(dep_items, "_t1")])

x <- dat$lone_sum_t1; y <- dat$dep_sum_t1
cov_hand <- sum((x - mean(x)) * (y - mean(y))) / (length(x) - 1)  # Covariance
r_hand   <- cov_hand / (sd(x) * sd(y))                             # Correlation = covariance / (sd(x) * sd(y))
cat("Covariance: Manual =", round(cov_hand, 3), " cov() =", round(cov(x, y), 3), "\n")
cat("Correlation r: Manual =", round(r_hand, 3), " cor() =", round(cor(x, y), 3), "\n\n")

# Correlation matrix
vars <- c("lone_sum_t1", "dep_sum_t1", "social_support_t1", "sleep_hours_t1", "life_sat_t1")
print(round(cor(dat[, vars]), 2))
# Spearman rank correlation is suitable for ordinal data
cat("\nSpearman r(Loneliness, Depression) =", round(cor(x, y, method = "spearman"), 3), "\n")

png_open("L1-4_scatter.png", 1400, 1300)
set.seed(14)                         # jitter() is random: set seed so the plot is identical every time
plot(jitter(x), jitter(y), pch = 16, col = rgb(0, 0, 1, .3),
     xlab = "Loneliness Total Score T1", ylab = "Depression Total Score T1", main = paste0("r = ", round(r_hand, 2)))
abline(lm(y ~ x), col = "red", lwd = 2)
invisible(dev.off())
cat("Reminder: Correlation is not causation.\n")

# Ordinal items: comparing three correlation types (second code box in lesson) -- Depressed mood, Sleep problems (0-3 scale)
cat("\ndep1_t1 and dep3_t1: Pearson / Spearman / Polychoric correlation\n")
x2 <- dat[, c("dep1_t1", "dep3_t1")]
print(round(cor(x2)[1, 2], 3))                        # Pearson
print(round(cor(x2, method = "spearman")[1, 2], 3))   # Spearman
print(round(psych::polychoric(x2)$rho[1, 2], 3))      # Polychoric correlation
log_close()
