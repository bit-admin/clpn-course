# =====================================================================
# L3-2.R  多元回归与“控制其他变量”  (Multiple regression & "controlling for")
# 关键联系：CLPN 的一条交叉滞后边 = 一个“控制了所有其他 T1 变量”的回归系数
# =====================================================================
source("R/_setup.R")
log_open("L3-2_log.txt")
dat <- read_course_data()
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])
dat$dep_sum_t1  <- rowSums(dat[, paste0(dep_items, "_t1")])
dat$dep_sum_t2  <- rowSums(dat[, paste0(dep_items, "_t2")])

m1 <- lm(dep_sum_t2 ~ lone_sum_t1, data = dat)                                   # 只有孤独
m2 <- lm(dep_sum_t2 ~ lone_sum_t1 + social_support_t1 + sleep_hours_t1, data = dat)
m3 <- lm(dep_sum_t2 ~ lone_sum_t1 + dep_sum_t1, data = dat)                      # 控制 T1 抑郁！
cat("孤独的系数：单独", round(coef(m1)[2], 3), "；+支持+睡眠", round(coef(m2)[2], 3),
    "；+T1 抑郁（交叉滞后）", round(coef(m3)[2], 3), "\n\n")
print(summary(m3))
cat("m3 就是一个“迷你 CLPM”：T2 抑郁 ~ T1 抑郁（自回归）+ T1 孤独（交叉滞后）。\n")

# ---- m2 的完整系数，并手算孤独的 VIF（讲义第二个代码框）----
cat("\nm2 的系数（孤独 + 社会支持 + 睡眠）与孤独的 VIF：\n")
print(round(summary(m2)$coefficients, 3))
r2_lone <- summary(lm(lone_sum_t1 ~ social_support_t1 + sleep_hours_t1, data = dat))$r.squared
print(round(1 / (1 - r2_lone), 3))      # VIF = 1 / (1 - R²)

# ---- 多重共线性演示：一个几乎重复的预测变量（讲义第三个代码框）----
# 本脚本前面没有用到随机数，所以这里 set.seed(1) 的结果与 R/solutions/L3-2_solution.R 相同
cat("\n共线性演示：孤独总分 + 一点点噪音的“副本”\n")
set.seed(1)
dat$lone_copy <- dat$lone_sum_t1 + rnorm(800, 0, 0.3)   # 孤独总分 + 一点点噪音
print(round(cor(dat$lone_sum_t1, dat$lone_copy), 3))
print(round(summary(lm(dep_sum_t2 ~ lone_sum_t1, data = dat))$coefficients[2, 1:2], 3))
print(round(summary(lm(dep_sum_t2 ~ lone_sum_t1 + lone_copy, data = dat))$coefficients[, 1:2], 3))

# ---- “控制”的两步理解（Frisch–Waugh）----
cat("\nFrisch–Waugh：孤独中与 T1 抑郁无关的部分 → 预测 T2 抑郁\n")
ex <- resid(lm(lone_sum_t1 ~ dep_sum_t1, data = dat))   # 孤独中与 T1 抑郁无关的部分
print(round(coef(lm(dat$dep_sum_t2 ~ ex))[2], 4))       # = m3 中孤独的系数
log_close()
