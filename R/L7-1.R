# =====================================================================
# L7-1.R  CLPN 的模型逻辑：把 CLPM 拆到题目层面  (CLPN logic, 4-node toy example)
# 4 个节点 → 4 个回归方程（每个 T2 节点一个）→ 4×4 有向权重矩阵
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L7-1_log.txt")
dat <- read_course_data()
four <- c("lone1", "lone3", "dep1", "dep2")
X <- scale(dat[, paste0(four, "_t1")]); Y <- scale(dat[, paste0(four, "_t2")])
B <- matrix(0, 4, 4, dimnames = list(four, four))   # 行 = T1 预测变量（from），列 = T2 结果（to）
for (j in 1:4) {
  fit <- lm(Y[, j] ~ X)                             # 方程 j：T2 的节点 j ~ 所有 T1 节点
  B[, j] <- coef(fit)[-1]                           # 去掉截距，放进第 j 列
  cat(sprintf("%s_T2 = %s\n", four[j],
              paste(sprintf("%+.2f×%s_T1", coef(fit)[-1], four), collapse = " ")))
}
cat("\n权重矩阵 B（对角线 = 自回归 AR，非对角线 = 交叉滞后 CL）：\n"); print(round(B, 2))
cat("8 个节点的 CLPN：8 个回归；最多 8×7 = 56 条交叉滞后边。\n")
CL <- B; diag(CL) <- 0
png_open("L7-1_toy_clpn.png", 1400, 1300)
qgraph(CL, directed = TRUE, edge.labels = TRUE, asize = 5, layout = "circle",
       groups = list(孤独 = 1:2, 抑郁 = 3:4), theme = "colorblind",
       title = "4 节点 CLPN（OLS，未正则化；不画自回归）")
invisible(dev.off())
log_close()
