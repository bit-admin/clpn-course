# 练习答案 L2-2：睡眠向量与 zscore()（2.2-A）；课程数据上的向量运算（2.2-B）；多类别因子（2.2-C）
source("R/_setup.R"); log_open("sol_L2-2_log.txt")
# ---- 2.2-A 睡眠向量 ----
sleep <- c(7, 5.5, 8, NA, 6, 4.5, 7.5, NA, 9, 5)
mean(sleep, na.rm = TRUE)                    # 6.5625
which(sleep < 6)                             # 2 6 10（第几位）
sleep[sleep < 6 & !is.na(sleep)]             # 5.5 4.5 5.0（具体时长）
zscore <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- sd(x, na.rm = TRUE)
  (x - m) / s                                # 最后一行就是返回值
}
all.equal(zscore(sleep), as.numeric(scale(sleep)))   # TRUE
stopifnot(isTRUE(all.equal(zscore(sleep), as.numeric(scale(sleep)))))
cat("zscore() 与 scale() 结果一致 ✔\n\n")
# ---- 2.2-B 在课程数据上 ----
dat <- read.csv("data/clpn_sim_wide.csv")
d1 <- dat$dep1_t1
sum(d1 == 3)                 # (1) 得 3 分的人数
mean(d1 >= 2)                # (2) 得 2 分及以上的比例
z <- zscore(d1)
round(c(mean(z), sd(z)), 10) # (3) 0 和 1
cat("\n")
# ---- 2.2-C 多类别因子 ----
service <- c(1, 3, 2, 2, 1, 3, 3)
service_f <- factor(service, levels = 1:3, labels = c("个案", "小组", "社区"))
table(service_f)             # 个案 2，小组 2，社区 3
round(mean(service), 2)      # 2.14：数值上能算，但“平均服务类型”没有意义
log_close()
