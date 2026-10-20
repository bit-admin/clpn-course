# =====================================================================
# L8-1.R  The Idea of the Bootstrap: Simulating "Repeating the Study" with the Sample
#         (The nonparametric bootstrap)
# Approximately 15 lines of code without any external packages to run 1,000
# bootstrap replications on a single correlation coefficient
# =====================================================================
source("R/_setup.R")
log_open("L8-1_log.txt")
dat <- read_course_data()
x <- rowSums(dat[, paste0(lone_items, "_t1")]); y <- rowSums(dat[, paste0(dep_items, "_t2")])
n <- length(x)
set.seed(81)
B <- 1000
r_boot <- numeric(B)                        # Pre-allocate an empty vector for 1,000 results
for (b in 1:B) {
  idx <- sample(1:n, n, replace = TRUE)     # Resample n case indices with replacement
  r_boot[b] <- cor(x[idx], y[idx])          # Recompute the correlation on the bootstrap sample
}
ci <- quantile(r_boot, c(.025, .975))       # Percentile interval
cat("Sample correlation r =", round(cor(x, y), 3), "\n")
cat("Bootstrap 95% percentile interval = [", round(ci[1], 3), ",", round(ci[2], 3), "]\n")
cat("cor.test() 95% CI                = [", paste(round(cor.test(x, y)$conf.int, 3), collapse = ", "), "]\n")
cat("Bootstrap standard error =", round(sd(r_boot), 4), "\n")
png_open("L8-1_boot_r.png", 1500, 1100)
hist(r_boot, breaks = 40, col = "lightblue", main = "Bootstrap distribution of the correlation coefficient (B = 1,000)",
     xlab = "r (T1 Loneliness sum score, T2 Depression sum score)")
abline(v = ci, col = "red", lwd = 2, lty = 2); abline(v = cor(x, y), lwd = 3)
invisible(dev.off())
log_close()
