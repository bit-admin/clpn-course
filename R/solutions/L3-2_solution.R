# 练习答案 L3-2：孤独单独预测 vs 加入社会支持与睡眠
source("R/_setup.R")
log_open("sol_L3-2_log.txt")
dat <- read_course_data()
dat$lone <- rowSums(dat[, paste0(lone_items, "_t1")]); dat$dep2 <- rowSums(dat[, paste0(dep_items, "_t2")])
b1 <- coef(lm(dep2 ~ lone, dat))["lone"]
b2 <- coef(lm(dep2 ~ lone + social_support_t1 + sleep_hours_t1, dat))["lone"]
cat("孤独系数：单独", round(b1, 3), "→ 控制支持与睡眠后", round(b2, 3), "\n")
# 解释：孤独与社会支持、睡眠相关；单独模型里孤独的系数“替”它们承担了一部分预测，
# 控制后剩下的是孤独“独特的”预测作用。CLPN 的每条边正是这种“控制其他所有 T1 题目”的系数。

# 课件 3.2 的多重共线性极端例子：孤独总分 + 一点点噪音的“副本”
dat <- read_course_data()
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")]); dat$dep_sum_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
set.seed(1)
dat$lone_copy <- dat$lone_sum_t1 + rnorm(800, 0, 0.3)
cat("\n共线性演示：r(孤独, 副本) =", round(cor(dat$lone_sum_t1, dat$lone_copy), 3), "\n")
print(round(summary(lm(dep_sum_t2 ~ lone_sum_t1, data = dat))$coefficients[2, 1:2], 3))
print(round(summary(lm(dep_sum_t2 ~ lone_sum_t1 + lone_copy, data = dat))$coefficients[, 1:2], 3))

# ---- 练习 3.2-A 的第二部分：再加 T1 抑郁（m4）----
dat$dep_sum_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])
m4 <- lm(dep_sum_t2 ~ lone_sum_t1 + social_support_t1 + sleep_hours_t1 + dep_sum_t1, data = dat)
cat("\n3.2-A：m4（孤独 + 支持 + 睡眠 + T1 抑郁）的系数\n")
print(round(coef(m4), 3))
# 孤独系数降到约 0.128，与 m3（只控制 T1 抑郁）的 0.140 接近：真正“分走”预测力的是 T1 抑郁。

# ---- 练习 3.2-B：CLPN 的一条边就是一个偏回归系数 ----
d <- as.data.frame(scale(dat[, c(vars_t(1), "dep1_t2")]))     # 先标准化，便于和总体目标值比较
f <- lm(dep1_t2 ~ ., data = d)                               # “.” 表示其余所有列
cat("\n3.2-B：dep1_t2 ~ 9 道 T1 题（标准化系数）\n")
print(round(coef(f), 3))
cat("总体目标值（data/true_B_population.csv 的 dep1 列）\n")
print(round(true_B()[, "dep1"], 3))
lone_b <- coef(f)[paste0(lone_items, "_t1")]
cat("孤独题中系数最大：", names(which.max(lone_b)), round(max(lone_b), 3), "\n")
# 9 道 T1 题各自的 VIF（用其他 8 道题预测它）
X1 <- dat[, vars_t(1)]
vif9 <- sapply(names(X1), function(v) 1 / (1 - summary(lm(reformulate(setdiff(names(X1), v), v), data = X1))$r.squared))
cat("VIF：\n"); print(round(vif9, 2))
cat("lone4_t1 的 VIF =", round(vif9["lone4_t1"], 2), "；全部在", round(min(vif9), 2), "–", round(max(vif9), 2),
    "之间，远低于 5 的警戒线\n")
log_close()
