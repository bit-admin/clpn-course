# 练习答案 L1-4：把“预期的”相关矩阵与真实数据对照
source("R/_setup.R")
log_open("sol_L1-4_log.txt")
dat <- read_course_data()
d <- data.frame(孤独 = rowSums(dat[, paste0(lone_items, "_t1")]),
                睡眠时长 = dat$sleep_hours_t1,
                抑郁 = rowSums(dat[, paste0(dep_items, "_t1")]),
                社会支持 = dat$social_support_t1)
expected <- matrix(c("1", "-", "+", "-",
                     "-", "1", "-", "+",
                     "+", "-", "1", "-",
                     "-", "+", "-", "1"), 4, byrow = TRUE, dimnames = list(names(d), names(d)))
print(expected, quote = FALSE); print(round(cor(d), 2))
# 混杂例子（confounding）：“社区活动中心越多的街道，求助热线来电越多”——
# 两者都受“人口规模”影响；控制人口后关联可能消失。

# ---- 练习 1.4-C：T1 的 9 道题目之间的相关矩阵 ----
cat("\n1.4-C：T1 九道题的相关矩阵\n")
R <- round(cor(dat[, vars_t(1)]), 2)
print(R)
# (1) 相关最强的一对题目（只看下三角，避开对角线和重复）
low <- R; low[upper.tri(low, diag = TRUE)] <- NA
idx <- which(low == max(low, na.rm = TRUE), arr.ind = TRUE)
cat("(1) 相关最强：", paste(rownames(R)[idx[, 1]], "—", colnames(R)[idx[, 2]], collapse = "；"),
    " r =", max(low, na.rm = TRUE), "\n")
# (2) 跨构念（行 = 孤独题，列 = 抑郁题）的 4 × 5 块
cross <- R[paste0(lone_items, "_t1"), paste0(dep_items, "_t1")]
print(cross)
idx2 <- which(cross == max(cross), arr.ind = TRUE)
cat("(2) 跨构念最强：", paste(rownames(cross)[idx2[, 1]], "—", colnames(cross)[idx2[, 2]], collapse = "；"),
    " r =", max(cross), "\n")
# (3) dep2_t1（兴趣丧失）与 dep4_t1（疲乏无力）：三种相关
x3 <- dat[, c("dep2_t1", "dep4_t1")]
cat("(3) 皮尔逊 =", round(cor(x3)[1, 2], 3),
    " 斯皮尔曼 =", round(cor(x3, method = "spearman")[1, 2], 3),
    " 多分格 =", round(psych::polychoric(x3)$rho[1, 2], 3), "\n")
# 多分格相关最大：0–3 分只有 4 个等级且有地板效应，皮尔逊把粗糙等级当精确数值，相关被压低；
# 多分格相关估计的是背后连续倾向之间的相关。
log_close()
