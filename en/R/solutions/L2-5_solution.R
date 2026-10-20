# Exercise Solutions L2-5: Replicating Module 1 hand calculations (2.5-A); item-level correlation matrix (2.5-B); missing data and glm() summary (2.5-C)
source("R/_setup.R")
log_open("sol_L2-5_log.txt")
x <- c(8, 10, 9, 14, 7, 12)                   # The 6 loneliness scores hand-calculated in Lesson 1.2
cat("mean =", mean(x), " var =", var(x), " sd =", round(sd(x), 3), "\n\n")
dat <- read_course_data()
d <- data.frame(loneliness = rowSums(dat[, paste0(lone_items, "_t1")]), depression = rowSums(dat[, paste0(dep_items, "_t1")]),
                social_support = dat$social_support_t1, sleep = dat$sleep_hours_t1, life_sat = dat$life_sat_t1)
print(round(psych::describe(d)[, c("n", "mean", "sd", "min", "max", "skew")], 2))
print(round(cor(d), 2))
print(summary(lm(depression ~ loneliness, data = d))$coefficients |> round(4))
# ---- 2.5-B Item level ----
R <- cor(dat[, vars_t(1)]); colnames(R) <- rownames(R) <- items
rng <- function(m) round(range(m), 2)
cat("\nWithin loneliness items: ", rng(R[1:4, 1:4][upper.tri(R[1:4, 1:4])]),
    "\nWithin depression items: ", rng(R[5:9, 5:9][upper.tri(R[5:9, 5:9])]),
    "\nBetween loneliness and depression: ", rng(R[1:4, 5:9]), "\n")
w <- which(R[1:4, 5:9] == max(R[1:4, 5:9]), arr.ind = TRUE)
cat("Strongest cross-construct correlation: ", items[w[1]], "—", items[4 + w[2]], "=", round(max(R[1:4, 5:9]), 2), "\n")
sk <- psych::describe(dat[, vars_t(1)])$skew
cat("skew Loneliness items: ", round(range(sk[1:4]), 2), "; Depression items: ", round(range(sk[5:9]), 2), "\n")
# ---- 2.5-C (1) Three use options ----
d_na <- d
d_na$loneliness[c(3, 10, 25)] <- NA
v3 <- c("loneliness", "depression", "social_support")
for (u in c("everything", "complete.obs", "pairwise.complete.obs")) {
  cat("\nuse =", u, "\n"); print(round(cor(d_na[, v3], use = u), 4))
}
# ---- 2.5-C (2) glm() coefficient table and OR ----
dat$dep_sum_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
fit_glm <- glm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat, family = binomial)
cat("\n"); print(round(summary(fit_glm)$coefficients, 4))
cat("OR = exp(b):\n"); print(round(exp(coef(fit_glm)), 3))
log_close()
