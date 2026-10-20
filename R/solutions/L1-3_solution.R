# 练习答案 L1-3：手算 z 分数；不同量尺的比较（练习 1.3-A、1.3-B）
source("R/_setup.R")
log_open("sol_L1-3_log.txt")
x <- c(2, 4, 1, 3, 4, 4)                       # 1.2 练习 A 的 6 个数
z <- (x - mean(x)) / sd(x)
cat("均值 =", mean(x), " SD =", round(sd(x), 3), "\n")
print(round(z, 2)); cat("z 分数之和 =", round(sum(z), 10), "（应为 0）\n")
print(round(scale(x)[, 1], 2))                 # 与 scale() 对照
dat <- read_course_data()
zz <- scale(dat[, c("dep3_t1", "life_sat_t1")])
cat("\n第 10 个人：原始分\n"); print(dat[10, c("dep3_t1", "life_sat_t1")])
cat("z 分数：\n"); print(round(zz[10, ], 2))
# 偏态时 |z| 不能直接读成“有多罕见”：直接看频数和百分位
cat("\ndep3_t1 各分数人数：\n"); print(table(dat$dep3_t1))
cat("dep3_t1 = 0 的比例：", round(mean(dat$dep3_t1 == 0), 3), "\n")
cat("life_sat_t1 >= 75 的比例：", round(mean(dat$life_sat_t1 >= 75), 3), "\n")
cat("正态分布下 z = 0.72 以上的比例：", round(1 - pnorm(0.72), 3), "\n")
cat("→ dep3 严重右偏：0 分是最常见的回答，|z| = 0.84 并不说明“罕见”。\n")
log_close()
