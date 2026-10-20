# =====================================================================
# L7-5.R  多波 CLPN、协变量与被试内问题  (Multi-wave CLPN, covariates)
# =====================================================================
source("R/_setup.R")
library(glmnet)
log_open("L7-5_log.txt")
dat <- read_course_data()
set.seed(2026); B12 <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)])   # T1 → T2
set.seed(2026); B23 <- clpn_estimate(dat[, vars_t(2)], dat[, vars_t(3)])   # T2 → T3
off <- row(B12) != col(B12)
cat("T1→T2 与 T2→T3 交叉滞后边权重的相关 =", round(cor(B12[off], B23[off]), 3), "\n")
cat("两个网络中同时非零的 CL 边 =", sum(B12[off] != 0 & B23[off] != 0),
    "；只在其一中出现 =", sum(xor(B12[off] != 0, B23[off] != 0)), "\n")
cat("自回归：\n"); print(round(rbind(T1T2 = diag(B12), T2T3 = diag(B23)), 3))

# 加入性别与年龄作为“不受惩罚”的协变量（penalty.factor = 0，见 _setup.R 中 clpn_estimate）
set.seed(2026)
B12c <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], covariates = dat[, c("gender", "age")])
cat("\n加协变量前后边权重的最大差异 =", round(max(abs(B12c - B12)), 4),
    "；相关 =", round(cor(B12c[off], B12[off]), 4), "\n")
# 直接看 penalty.factor 的写法（一个 T2 节点的例子）
Z <- cbind(scale(dat[, vars_t(1)]), gender = as.numeric(scale(dat$gender)))
cv1 <- cv.glmnet(Z, scale(dat$dep1_t2)[, 1], penalty.factor = c(rep(1, 9), 0))
print(round(as.matrix(coef(cv1, s = "lambda.min")), 3))
png_open("L7-5_replication.png", 1400, 1400)
plot(B12[off], B23[off], pch = 16, col = "steelblue", xlab = "T1→T2 边权重", ylab = "T2→T3 边权重",
     main = paste0("两个时间段 CLPN 的一致性 r = ", round(cor(B12[off], B23[off]), 2)))
abline(0, 1, lty = 2)
invisible(dev.off())
cat("\n局限：标准 CLPN 基于观测得分，混合了被试间（稳定特质）与被试内效应；\n",
    "本数据设定了稳定特质，所以同一构念内会出现由特质带来的小边（真实被试内 B 中没有）。\n")
saveRDS(list(B12 = B12, B23 = B23), out("L7-5_B12_B23.rds"))
log_close()
