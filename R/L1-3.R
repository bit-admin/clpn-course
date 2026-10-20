# =====================================================================
# L1-3.R  标准化与 z 分数  (Standardization & z-scores)
# z = (x - 均值) / 标准差 ：把不同量尺的变量换算成“离平均几个标准差”
# =====================================================================
source("R/_setup.R")
log_open("L1-3_log.txt")
dat <- read_course_data()

x <- c(8, 10, 9, 14, 7, 12)
z <- (x - mean(x)) / sd(x)                       # 手动计算 z 分数
print(round(cbind(原始分 = x, z分数 = z, scale函数 = as.numeric(scale(x))), 3))
cat("z 分数的均值 =", round(mean(z), 10), "，标准差 =", sd(z), "\n\n")

# 两个量尺完全不同的变量：睡眠问题（0–3）与生活满意度（0–100）
zz <- scale(dat[, c("dep3_t1", "life_sat_t1")])   # scale() 对每一列做标准化
print(round(head(cbind(dat[, c("dep3_t1", "life_sat_t1")], zz)), 2))
cat("\n标准化后两列的均值都≈0、标准差都=1，可以直接比较“相对位置”。\n")
cat("CLPN 中我们会先把所有题目标准化，这样回归系数才可比（标准化系数 standardized coefficient）。\n")

# 验证两条性质：标准化前后相关不变、偏度不变（讲义第三个代码框）
cat("\n相关（原始分 / 标准化后）与 dep1_t1 的偏度（原始分 / 标准化后）：\n")
print(round(cor(dat$dep3_t1, dat$life_sat_t1), 4))   # 原始分的相关
print(round(cor(zz[, 1], zz[, 2]), 4))                 # 标准化后的相关
print(round(psych::skew(dat$dep1_t1), 3))              # 偏度：原始分
print(round(psych::skew(scale(dat$dep1_t1)[, 1]), 3))  # 偏度：标准化后
log_close()
