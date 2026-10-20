# 练习答案 L2-5：复现模块 1 的手算（2.5-A）；题目层面的相关矩阵（2.5-B）；缺失值与 glm() 的 summary（2.5-C）
source("R/_setup.R")
log_open("sol_L2-5_log.txt")
x <- c(8, 10, 9, 14, 7, 12)                   # 1.2 课手算过的 6 个孤独分
cat("mean =", mean(x), " var =", var(x), " sd =", round(sd(x), 3), "\n\n")
dat <- read_course_data()
d <- data.frame(孤独 = rowSums(dat[, paste0(lone_items, "_t1")]), 抑郁 = rowSums(dat[, paste0(dep_items, "_t1")]),
                社会支持 = dat$social_support_t1, 睡眠 = dat$sleep_hours_t1, 生活满意度 = dat$life_sat_t1)
print(round(psych::describe(d)[, c("n", "mean", "sd", "min", "max", "skew")], 2))
print(round(cor(d), 2))
print(summary(lm(抑郁 ~ 孤独, data = d))$coefficients |> round(4))
# ---- 2.5-B 题目层面 ----
R <- cor(dat[, vars_t(1)]); colnames(R) <- rownames(R) <- items
rng <- function(m) round(range(m), 2)
cat("\n孤独题之间：", rng(R[1:4, 1:4][upper.tri(R[1:4, 1:4])]),
    "\n抑郁题之间：", rng(R[5:9, 5:9][upper.tri(R[5:9, 5:9])]),
    "\n孤独—抑郁之间：", rng(R[1:4, 5:9]), "\n")
w <- which(R[1:4, 5:9] == max(R[1:4, 5:9]), arr.ind = TRUE)
cat("跨构念最高：", items[w[1]], "—", items[4 + w[2]], "=", round(max(R[1:4, 5:9]), 2), "\n")
sk <- psych::describe(dat[, vars_t(1)])$skew
cat("skew 孤独题：", round(range(sk[1:4]), 2), "；抑郁题：", round(range(sk[5:9]), 2), "\n")
# ---- 2.5-C (1) 三种 use 选项 ----
d_na <- d
d_na$孤独[c(3, 10, 25)] <- NA
v3 <- c("孤独", "抑郁", "社会支持")
for (u in c("everything", "complete.obs", "pairwise.complete.obs")) {
  cat("\nuse =", u, "\n"); print(round(cor(d_na[, v3], use = u), 4))
}
# ---- 2.5-C (2) glm() 的系数表与 OR ----
dat$dep_sum_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
fit_glm <- glm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat, family = binomial)
cat("\n"); print(round(summary(fit_glm)$coefficients, 4))
cat("OR = exp(b)：\n"); print(round(exp(coef(fit_glm)), 3))
log_close()
