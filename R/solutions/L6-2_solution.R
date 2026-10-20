# 练习答案 L6-2：练习 2（加入失眠 → 注意力差的直接作用）与练习 3（课程数据上数边）
source("R/_setup.R")
log_open("sol_L6-2_log.txt")
pcor_of <- function(d) { P <- -cov2cor(solve(cor(d))); diag(P) <- 1; P }
set.seed(62); n <- 1000                        # 与 R/L6-2.R 相同的种子与结构
失眠 <- rnorm(n); 疲劳 <- 0.6 * 失眠 + rnorm(n, 0, .8)
注意力差 <- 0.6 * 疲劳 + 0.3 * 失眠 + rnorm(n, 0, .8)   # 练习 2：加入直接作用 0.3
d <- data.frame(失眠, 疲劳, 注意力差)
cat("相关：\n"); print(round(cor(d), 2))
cat("偏相关：\n"); print(round(pcor_of(d), 2))
cat("→ 失眠–注意力差的偏相关 =", round(pcor_of(d)[1, 3], 2), "（不再 ≈ 0：出现一条直接边）\n\n")
# 练习 3：课程数据 T1 的 9 道题
x <- read_course_data()[, vars_t(1)]
R <- cor(x); P <- -cov2cor(solve(R)); diag(P) <- 0
cat("相关网络中 |r| > 0.1 的边：", sum(abs(R[upper.tri(R)]) > .1), "/ 36\n")
cat("偏相关网络中 |pr| > 0.1 的边：", sum(abs(P[upper.tri(P)]) > .1), "/ 36\n")
same <- outer(c(rep(1, 4), rep(2, 5)), c(rep(1, 4), rep(2, 5)), "==")
cat("其中位于同一量表内部的：", sum((abs(P) > .1 & same)[upper.tri(P)]), "\n")
log_close()
