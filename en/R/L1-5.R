# =====================================================================
# L1-5.R  Sampling, Standard Error & Confidence Intervals
# (Sampling, SE & confidence intervals)
# Simulation with a "virtual city": larger sample sizes yield narrower sampling distributions of the sample mean.
# =====================================================================
source("R/_setup.R")
log_open("L1-5_log.txt")
set.seed(2026)
city <- rnorm(100000, mean = 10, sd = 3)          # Population: loneliness scores of 100,000 residents
sizes <- c(20, 100, 500)
png_open("L1-5_sampling.png", 2100, 800)
par(mfrow = c(1, 3))
for (n in sizes) {
  means <- replicate(2000, mean(sample(city, n)))  # Draw 2,000 samples, calculating the mean each time -> sampling distribution
  hist(means, breaks = 40, xlim = c(8, 12), col = "grey80",
       main = paste0("n = ", n, ", SD(mean) = ", round(sd(means), 3)), xlab = "Sample mean")
  cat("n =", n, ": Sampling distribution SD =", round(sd(means), 3),
      "; Theoretical SE = sigma/sqrt(n) =", round(3 / sqrt(n), 3), "\n")
}
invisible(dev.off())
# 95% confidence interval for a single sample
s <- sample(city, 100)
se <- sd(s) / sqrt(100)
cat("\nA single n = 100 sample: Mean =", round(mean(s), 2), " 95% CI = [",
    round(mean(s) - 1.96 * se, 2), ", ", round(mean(s) + 1.96 * se, 2), "]\n")
print(t.test(s)$conf.int)
log_close()
