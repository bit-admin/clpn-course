# =====================================================================
# L1-6.R  Hypothesis Testing, p-Values & Effect Sizes
# (Hypothesis testing, p-values, effect sizes)
# =====================================================================
source("R/_setup.R")
log_open("L1-6_log.txt")
dat <- read_course_data()
dat$dep_sum_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])

# 1) t-test: Do female and male participants differ in depression sum scores?
tt <- t.test(dep_sum_t1 ~ gender, data = dat)
print(tt)
# Effect size Cohen's d = difference in means / pooled standard deviation (pooled SD)
m <- tapply(dat$dep_sum_t1, dat$gender, mean); s <- tapply(dat$dep_sum_t1, dat$gender, sd)
n <- table(dat$gender)
sp <- sqrt(((n[1] - 1) * s[1]^2 + (n[2] - 1) * s[2]^2) / (sum(n) - 2))
cat("Cohen's d =", round((m[2] - m[1]) / sp, 3), "(0.2 small / 0.5 medium / 0.8 large)\n\n")

# 2) Multiple testing problem: 20 completely unrelated variables -> 190 pairwise correlations
set.seed(1)
noise <- matrix(rnorm(200 * 20), 200, 20)
pv <- c()
for (i in 1:19) for (j in (i + 1):20) pv <- c(pv, cor.test(noise[, i], noise[, j])$p.value)
cat("In pure noise, out of 190 correlations, those with p < .05 count:", sum(pv < .05), "(expected ~9.5 false positives)\n")
cat("Number significant after Bonferroni correction:", sum(p.adjust(pv, "bonferroni") < .05), "\n")
cat("-> This is one key reason network analysis relies on regularization (Lessons 3.5 / 6.3).\n")
log_close()
