# 练习答案 L5-4 练习 3：测量间隔与交叉滞后（每月自回归 0.9、每月交叉效应 0.05）
source("R/_setup.R")
log_open("sol_L5-4_log.txt")
a <- 0.9; cl <- 0.05
A <- matrix(c(a, cl, 0, a), 2)                  # 每月系数矩阵 [[a, 0], [c, a]]
cross <- function(d) { P <- diag(2); for (k in seq_len(d)) P <- P %*% A; P[2, 1] }
for (d in c(1, 3, 6, 12)) cat(sprintf("间隔 %2d 个月：矩阵幂得到 %.3f；公式 Δ·a^(Δ-1)·c = %.3f\n", d, cross(d), d * a^(d - 1) * cl))
cat(sprintf("峰值约在 %.1f 个月（-1/ln(a)）；1–24 个月中最大值出现在第 %d 个月\n", -1 / log(a), which.max(sapply(1:24, cross))))
log_close()
