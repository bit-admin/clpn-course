# =====================================================================
# L1-2.R  分布与描述统计：均值、方差、标准差
# (Distributions & descriptive statistics: mean, variance, SD)
# =====================================================================
source("R/_setup.R")
log_open("L1-2_log.txt")
dat <- read_course_data()

# ---- 1. 手算 vs R 计算：用 6 个人的孤独总分 ----
x <- c(8, 10, 9, 14, 7, 12)                  # 6 个人的孤独感总分（4 题相加，范围 4–16）
n <- length(x)
m <- sum(x) / n                              # 均值 mean = 总和 / 人数
v <- sum((x - m)^2) / (n - 1)                # 样本方差 variance：离均差平方和 / (n-1)
s <- sqrt(v)                                 # 标准差 standard deviation = 方差开根号
cat("手算：均值 =", m, " 方差 =", round(v, 3), " 标准差 =", round(s, 3), "\n")
cat("R 函数：mean() =", mean(x), " var() =", round(var(x), 3), " sd() =", round(sd(x), 3), "\n\n")

# ---- 2. 课程数据：孤独与抑郁总分（T1） ----
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])   # rowSums 按行相加
dat$dep_sum_t1  <- rowSums(dat[, paste0(dep_items, "_t1")])
print(summary(dat[, c("lone_sum_t1", "dep_sum_t1")]))          # 最小值、四分位数、中位数、均值
# psych::describe() 一次给出 n、均值、标准差、偏度（skew）、峰度（kurtosis）
print(round(psych::describe(dat[, vars_t(1)])[, c("n", "mean", "sd", "median", "skew", "kurtosis")], 2))

# ---- 3. 直方图（histogram）：抑郁题明显右偏（right-skewed）----
png_open("L1-2_hist.png", 2000, 900)
par(mfrow = c(1, 2))
# 总分是整数：把区间边界放在两个整数中间（如 -0.5, 0.5, 1.5, …），
# 每根柱子就正好对应一个分数。若写 breaks = 15，R 会自己挑边界，
# 并把最左端的两个分数（抑郁 0 分和 1 分）合进第一根柱子，夸大地板效应。
hist(dat$lone_sum_t1, breaks = seq(3.5, 16.5, 1),  col = "skyblue", main = "孤独总分（T1）", xlab = "得分")
hist(dat$dep_sum_t1,  breaks = seq(-0.5, 15.5, 1), col = "salmon",  main = "抑郁总分（T1）：右偏", xlab = "得分")
print(table(dat$dep_sum_t1))                 # 每个分数各有多少人，与直方图的柱高对照
invisible(dev.off())
cat("\n图已保存：R/output/L1-2_hist.png\n")
cat("解读：社区样本中多数人没有抑郁症状（得 0 分），少数人得分很高 → 右偏。\n")
log_close()
