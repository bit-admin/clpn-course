# =====================================================================
# L8-1.R  Bootstrap 的思想：用样本模拟“再做一次研究”  (The nonparametric bootstrap)
# 不用任何包，约 15 行代码对一个相关系数做 1000 次 bootstrap
# =====================================================================
source("R/_setup.R")
log_open("L8-1_log.txt")
dat <- read_course_data()
x <- rowSums(dat[, paste0(lone_items, "_t1")]); y <- rowSums(dat[, paste0(dep_items, "_t2")])
n <- length(x)
set.seed(81)
B <- 1000
r_boot <- numeric(B)                        # 先准备一个装 1000 个结果的空向量
for (b in 1:B) {
  idx <- sample(1:n, n, replace = TRUE)     # 有放回地（with replacement）抽 n 个个案编号
  r_boot[b] <- cor(x[idx], y[idx])          # 在“新样本”上重新计算相关
}
ci <- quantile(r_boot, c(.025, .975))       # 百分位区间（percentile interval）
cat("样本相关 r =", round(cor(x, y), 3), "\n")
cat("bootstrap 95% 百分位区间 = [", round(ci[1], 3), ",", round(ci[2], 3), "]\n")
cat("cor.test() 的 95% CI       = [", paste(round(cor.test(x, y)$conf.int, 3), collapse = ", "), "]\n")
cat("bootstrap 标准误 =", round(sd(r_boot), 4), "\n")
png_open("L8-1_boot_r.png", 1500, 1100)
hist(r_boot, breaks = 40, col = "lightblue", main = "相关系数的 1000 次 bootstrap 分布",
     xlab = "r（T1 孤独总分, T2 抑郁总分）")
abline(v = ci, col = "red", lwd = 2, lty = 2); abline(v = cor(x, y), lwd = 3)
invisible(dev.off())
log_close()
