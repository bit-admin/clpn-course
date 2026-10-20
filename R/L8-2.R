# =====================================================================
# L8-2.R  边权重准确性：bootnet 自定义 CLPN 估计函数 + 手写 bootstrap
# (Edge-weight accuracy: custom bootnet estimator & a manual bootstrap)
# ---------------------------------------------------------------------
# 与课件草稿相比的 3 处修正（已实测通过，bootnet 1.6+）：
#  (1) 估计函数内部不能依赖全局变量（如 t1_vars）——并行（nCores > 1）时
#      子进程看不到它们。这里改为“前 p 列 = T1，后 p 列 = T2”，并写 glmnet::cv.glmnet。
#  (2) estimateNetwork() 的数据只放 2p 列（T1 题目 + T2 题目，同样顺序），
#      labels 只给 p 个节点名；返回的矩阵必须是 p × p。
#  (3) bootnet() 要显式写 statistics = c("edge", "outExpectedInfluence", "inExpectedInfluence")，
#      否则不会保存有向网络的出/入 EI。
# 运行时间：1000 次 × 9 个 cv.glmnet；单核约 7–15 分钟（视电脑而定，含差异检验与手写 bootstrap）。初次练习可把 n_boots 改成 200。
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(glmnet); library(qgraph) })
log_open("L8-2_log.txt")
dat <- read_course_data()
wide_items <- dat[, c(vars_t(1), vars_t(2))]      # 18 列：前 9 列 T1，后 9 列 T2
labs <- items
n_boots <- 1000
# 可重复性：bootnet 的并行（nCores > 1）在各工作进程中用未设种子的随机数重抽样，
# 即使 set.seed() 结果每次也会略有不同。因此默认单核（nCores = 1），set.seed() 后结果完全可重复（约慢 5–7 倍）。
# 只想快速看看、不需要可重复时，可改为 max(1, parallel::detectCores() - 1)。
n_cores <- 1

# ---- 自定义估计函数（custom estimator）----
clpn_fun <- function(data) {
  p <- ncol(data) / 2                              # 节点数 = 列数的一半
  X <- scale(as.matrix(data[, 1:p]))               # T1
  Y <- scale(as.matrix(data[, (p + 1):(2 * p)]))   # T2
  B <- matrix(0, p, p)
  for (j in seq_len(p)) {
    cvfit <- glmnet::cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]
  }
  B                                                # 行 = T1（from），列 = T2（to）
}
set.seed(2026)
net <- estimateNetwork(wide_items, default = "none", fun = clpn_fun,
                       directed = TRUE, labels = labs)
B_hat <- net$graph; dimnames(B_hat) <- list(labs, labs)
cat("估计的网络（与 L7-2 相同方法与种子，结果相同）：\n"); print(round(B_hat, 2))

set.seed(2026)
boot <- bootnet(net, nBoots = n_boots, type = "nonparametric", nCores = n_cores,
                statistics = c("edge", "outExpectedInfluence", "inExpectedInfluence"),
                verbose = FALSE)
saveRDS(boot, out("L8-2_boot.rds"))

# ---- 边权重的 bootstrap 区间图 ----
png_open("L8-2_edge_ci.png", 1600, 3200)
print(plot(boot, statistics = "edge", order = "sample", labels = TRUE, plot = "area",
           CIstyle = "quantiles"))
invisible(dev.off())
# 只看交叉滞后边：从 summary 中取出
s <- summary(boot, statistics = "edge")
s <- as.data.frame(s)
s_cl <- s[s$node1 != s$node2, c("node1", "node2", "sample", "mean", "q2.5", "q97.5", "prop0")]
s_cl <- s_cl[order(-abs(s_cl$sample)), ]
cat("\n最强 10 条交叉滞后边的 bootstrap 区间（q2.5–q97.5 百分位；prop0 = 被压为 0 的比例）：\n")
print(head(s_cl, 10), row.names = FALSE, digits = 3)
write.csv(s_cl, out("L8-2_cl_edge_boot.csv"), row.names = FALSE)

# ---- 边权重差异检验（bootstrapped difference test）----
top5 <- head(s_cl, 5); top5_id <- paste0(top5$node1, "->", top5$node2)
png_open("L8-2_edge_difference.png", 1800, 1800)
suppressWarnings(print(plot(boot, "edge", plot = "difference", onlyNonZero = TRUE, order = "sample")))
invisible(dev.off())
cat("\n最强 5 条 CL 边之间的差异检验（TRUE = 95% bootstrap 区间不含 0）：\n")
dt <- differenceTest(boot, top5_id, top5_id, measure = "edge")
print(dt[dt$id1 < dt$id2, c("id1", "id2", "lower", "upper", "significant")], row.names = FALSE)

# ---- 手写版 bootstrap（不依赖 bootnet，帮助你理解原理；默认 200 次）----
set.seed(82)
n <- nrow(wide_items); manual_B <- 200
boot_arr <- array(NA, c(9, 9, manual_B), dimnames = list(labs, labs, NULL))
for (b in 1:manual_B) {
  idx <- sample(n, n, replace = TRUE)                    # 有放回重抽个案
  boot_arr[, , b] <- clpn_fun(wide_items[idx, ])         # 在新样本上重新估计整个 CLPN
}
lo <- apply(boot_arr, c(1, 2), quantile, .025); hi <- apply(boot_arr, c(1, 2), quantile, .975)
cat("\n手写 bootstrap（", manual_B, "次）：lone3 → dep1 的区间 = [",
    round(lo["lone3", "dep1"], 3), ",", round(hi["lone3", "dep1"], 3), "]；",
    "被压为 0 的比例 =", mean(boot_arr["lone3", "dep1", ] == 0), "\n")
cat("注意：LASSO 会把系数往 0 压（收缩 shrinkage），所以这些区间不是严格的 95% 置信区间，\n",
    "只能作为“估计精确度”的参考（Epskamp et al., 2018）。\n")
log_close()
