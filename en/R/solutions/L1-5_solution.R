# Exercise Solutions L1-5: Sample size and sampling distribution
source("R/_setup.R")
log_open("sol_L1-5_log.txt")
set.seed(15); city <- rnorm(1e5, 10, 3)
for (n in c(20, 100, 500)) cat("n =", n, " Sampling distribution SD of mean =", round(sd(replicate(2000, mean(sample(city, n)))), 3), "\n")
# 3-sentence reference answer:
# 1) The larger the sample, the more concentrated the sample statistic is around the population value (standard error ∝ 1/√n).
# 2) A network contains dozens of edges; each edge is a parameter to be estimated, each carrying its own sampling error.
# 3) Therefore, network analysis requires a relatively large sample size and uses bootstrap to inspect edge precision (Module 8).

# ---- Exercise 1.5-B: Hand-calculated SE and 95% CI, verified with R ----
m <- 9.2; sdv <- 3.2; n <- 64
se <- sdv / sqrt(n)
cat("\n1.5-B: SE =", se, "; 95% CI = [", round(m - 1.96 * se, 2), ",", round(m + 1.96 * se, 2), "]\n")

# ---- Exercise 1.5-C: Re-run with set.seed(1) replacing set.seed(2026) in R/L1-5.R ----
# Below is the main part of L1-5.R (omitting plots), changing only the seed to 1; compare with R/output/L1-5_log.txt
run_l15 <- function() {
  city <- rnorm(100000, mean = 10, sd = 3)
  for (n in c(20, 100, 500)) {
    means <- replicate(2000, mean(sample(city, n)))
    cat("n =", n, ": Sampling distribution SD =", round(sd(means), 3),
        "; Theoretical SE = sigma/sqrt(n) =", round(3 / sqrt(n), 3), "\n")
  }
  s <- sample(city, 100); se <- sd(s) / sqrt(100)
  cat("One n=100 sample: Mean =", round(mean(s), 2), " 95% CI = [",
      round(mean(s) - 1.96 * se, 2), ",", round(mean(s) + 1.96 * se, 2), "]\n")
}
cat("\n1.5-C: set.seed(1)\n");  set.seed(1);  run_l15()
cat("\nRunning set.seed(1) again: Exactly identical to above\n"); set.seed(1); run_l15()
# The effect of "deleting set.seed() and running twice": Equivalent to using a different seed each time, producing different numbers each time.
# Here illustrated with two different seeds (when genuinely omitting a seed, your numbers will differ from anyone else's):
cat("\nWithout fixed seed, Run 1 (Illustration: seed 101)\n"); set.seed(101); run_l15()
cat("\nWithout fixed seed, Run 2 (Illustration: seed 202)\n"); set.seed(202); run_l15()
# Conclusion: Specific numbers (especially the mean and CI for that n = 100 sample) vary with the seed;
# The underlying pattern remains unchanged: simulated SD consistently approximates sigma/sqrt(n), narrowing as n increases. Always fix and report random seeds in analyses.
log_close()
