# Exercise Solutions L1-2
#   1.2-A: Loneliness item scores for 6 residents: 2, 4, 1, 3, 4, 4 — Mean, median, variance, SD + histogram (horizontal axis 1–4)
#   1.2-C: T2 depression sum score (dep1_t2–dep5_t2) mean, median, SD, and proportion of score 0
#   (1.2-B is a discussion question; see lecture notes for main points; commentary included below)
source("R/_setup.R")
log_open("sol_L1-2_log.txt")

# ---- 1.2-A Manual calculation verified with R ----
x <- c(2, 4, 1, 3, 4, 4)
# Step 1 Mean: (2+4+1+3+4+4)/6 = 18/6 = 3
# Step 2 Median: Sorted 1, 2, 3, 4, 4, 4; middle two values are 3 and 4 -> (3+4)/2 = 3.5
# Step 3 Deviations from mean: -1, 1, -2, 0, 1, 1; Squared: 1, 1, 4, 0, 1, 1; Sum of squares = 8
# Step 4 Variance = 8 / (6-1) = 1.6; Standard deviation = sqrt(1.6) ≈ 1.26
stopifnot(mean(x) == 3, median(x) == 3.5, abs(var(x) - 1.6) < 1e-9)
cat("1.2-A: Mean =", mean(x), " Median =", median(x), " Variance =", var(x), " SD =", round(sd(x), 2), "\n")
print(table(factor(x, levels = 1:4)))        # Score 1: 1 person, Score 2: 1 person, Score 3: 1 person, Score 4: 3 persons
# Histogram: One bin per integer score (breaks at 0.5, 1.5, ..., 4.5)
png_open("sol_L1-2_hist.png", 1200, 1000)
hist(x, breaks = seq(0.5, 4.5, 1), col = "grey", main = "Loneliness Item Scores for 6 Residents", xlab = "Score (1–4)", ylab = "Count")
invisible(dev.off())
cat("Left-skewed: Mean 3 < Median 3.5; half the participants chose the maximum score 4 -> signs of ceiling effect\n\n")

# ---- 1.2-C T2 Depression Sum Score ----
dat <- read_course_data()
dep_sum_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
cat("1.2-C: T2 Depression Sum Score\n")
cat("Mean =", round(mean(dep_sum_t2), 2), " Median =", median(dep_sum_t2),
    " SD =", round(sd(dep_sum_t2), 2), "\n")
cat("Proportion of 0s =", round(mean(dep_sum_t2 == 0), 3), "\n")   # Mean of logical values = proportion of TRUE
# Mean (approx 3.78) > Median (3): Right-skewed, same as T1.

# 1.2-B Discussion points: In a community sample, most people are asymptomatic -> depression items have many 0s -> right-skewed (floor effect);
# Consequences: Mean is pulled upward by a few high scores; should report median and proportions concurrently; restricted variance -> Pearson correlation attenuated
# -> Network analysis frequently uses polychoric correlation (cor_auto) or Spearman correlation (Lesson 1.4).
log_close()
