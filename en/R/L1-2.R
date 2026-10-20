# =====================================================================
# L1-2.R  Distributions & Descriptive Statistics: Mean, Variance, SD
# (Distributions & descriptive statistics: mean, variance, SD)
# =====================================================================
source("R/_setup.R")
log_open("L1-2_log.txt")
dat <- read_course_data()

# ---- 1. Manual vs. R Calculation: Loneliness Sum Scores for 6 Participants ----
x <- c(8, 10, 9, 14, 7, 12)                  # Loneliness sum scores for 6 participants (4 items summed, range 4-16)
n <- length(x)
m <- sum(x) / n                              # Mean = sum / sample size
v <- sum((x - m)^2) / (n - 1)                # Sample variance: sum of squared deviations / (n - 1)
s <- sqrt(v)                                 # Standard deviation = square root of variance
cat("Manual: Mean =", m, " Variance =", round(v, 3), " SD =", round(s, 3), "\n")
cat("R functions: mean() =", mean(x), " var() =", round(var(x), 3), " sd() =", round(sd(x), 3), "\n\n")

# ---- 2. Course Data: Loneliness and Depression Sum Scores (T1) ----
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])   # rowSums computes sums across rows
dat$dep_sum_t1  <- rowSums(dat[, paste0(dep_items, "_t1")])
print(summary(dat[, c("lone_sum_t1", "dep_sum_t1")]))          # Min, quartiles, median, mean, max
# psych::describe() provides n, mean, SD, skew, and kurtosis simultaneously
print(round(psych::describe(dat[, vars_t(1)])[, c("n", "mean", "sd", "median", "skew", "kurtosis")], 2))

# ---- 3. Histograms: Depressive Symptoms Are Clearly Right-Skewed ----
png_open("L1-2_hist.png", 2000, 900)
par(mfrow = c(1, 2))
# Sum scores are integers: placing bin boundaries halfway between integers (e.g., -0.5, 0.5, 1.5, ...),
# ensures each bar corresponds to exactly one integer score. If writing breaks = 15, R picks arbitrary boundaries,
# merging the leftmost two scores (depression 0 and 1) into the first bar, exaggerating floor effects.
hist(dat$lone_sum_t1, breaks = seq(3.5, 16.5, 1),  col = "skyblue", main = "Loneliness Total Score (T1)", xlab = "Score")
hist(dat$dep_sum_t1,  breaks = seq(-0.5, 15.5, 1), col = "salmon",  main = "Depression Total Score (T1): Right-skewed", xlab = "Score")
print(table(dat$dep_sum_t1))                 # Count of participants at each score, comparing with histogram bar heights
invisible(dev.off())
cat("\nFigure saved: R/output/L1-2_hist.png\n")
cat("Interpretation: In a community sample, most participants report no depressive symptoms (score of 0), while few score very high -> right-skewed.\n")
log_close()
