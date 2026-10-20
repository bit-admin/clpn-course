# =====================================================================
# L1-6.R  假设检验、p 值与效应量  (Hypothesis testing, p-values, effect sizes)
# =====================================================================
source("R/_setup.R")
log_open("L1-6_log.txt")
dat <- read_course_data()
dat$dep_sum_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])

# 1) t 检验：女性与男性的抑郁总分是否不同？
tt <- t.test(dep_sum_t1 ~ gender, data = dat)
print(tt)
# 效应量 Cohen's d = 均值差 / 合并标准差（pooled SD）
m <- tapply(dat$dep_sum_t1, dat$gender, mean); s <- tapply(dat$dep_sum_t1, dat$gender, sd)
n <- table(dat$gender)
sp <- sqrt(((n[1] - 1) * s[1]^2 + (n[2] - 1) * s[2]^2) / (sum(n) - 2))
cat("Cohen's d =", round((m[2] - m[1]) / sp, 3), "（0.2 小 / 0.5 中 / 0.8 大）\n\n")

# 2) 多重比较问题（multiple comparisons）：20 个毫无关系的变量 → 190 个相关
set.seed(1)
noise <- matrix(rnorm(200 * 20), 200, 20)
pv <- c()
for (i in 1:19) for (j in (i + 1):20) pv <- c(pv, cor.test(noise[, i], noise[, j])$p.value)
cat("纯噪声中，190 个相关里 p < .05 的有", sum(pv < .05), "个（期望约 9.5 个假阳性 false positives）\n")
cat("Bonferroni 校正后显著的有", sum(p.adjust(pv, "bonferroni") < .05), "个\n")
cat("→ 这就是网络分析需要“正则化”（模块 3.5 / 6.3）的原因之一。\n")
log_close()
