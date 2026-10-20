# Exercise Solutions L1-6-C: Repeating the "multiple comparisons in pure noise" simulation across seeds
source("R/_setup.R")
log_open("sol_L1-6_log.txt")
count_fp <- function(seed) {                    # Same simulation as R/L1-6.R, varying only the seed
  set.seed(seed)
  noise <- matrix(rnorm(200 * 20), 200, 20)
  pv <- c()
  for (i in 1:19) for (j in (i + 1):20) pv <- c(pv, cor.test(noise[, i], noise[, j])$p.value)
  sum(pv < .05)
}
fp5 <- sapply(2:6, count_fp)
cat("False positive counts for seeds 2–6: ", fp5, "; Mean =", mean(fp5), "\n")
fp200 <- sapply(1:200, count_fp)
cat("Average false positive count across 200 seeds =", round(mean(fp200), 2), "(theoretical expectation: 190 x 0.05 = 9.5)\n")
cat("Range: ", range(fp200), "; Middle 90% falls within ", quantile(fp200, c(.05, .95)), "\n")
log_close()
