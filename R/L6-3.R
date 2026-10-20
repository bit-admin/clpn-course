# =====================================================================
# L6-3.R  正则化网络估计：EBICglasso 与超参数 γ  (Regularized GGM, gamma)
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(qgraph) })
log_open("L6-3_log.txt")
dat <- read_course_data()
items_t1 <- dat[, vars_t(1)]; names(items_t1) <- items
res <- data.frame()
nets <- list()
# 注意：N = 800 较大时，EBICglasso 可能提示 “A dense regularized network was selected”
# （选到的 λ 很小 → 网络较稠密）。这是一个“提醒”而不是错误，所以下面用 suppressWarnings() 隐藏。
for (g in c(0, 0.25, 0.5)) {
  net <- suppressWarnings(estimateNetwork(items_t1, default = "EBICglasso", tuning = g,
                         corMethod = "cor_auto", verbose = FALSE))  # cor_auto：定序题目→多分格相关
  nets[[as.character(g)]] <- net
  res <- rbind(res, data.frame(gamma = g, 边数 = sum(net$graph[upper.tri(net$graph)] != 0)))
}
print(res)
# 本课程数据中，孤独题之间、抑郁题之间的关联都较强，3 个 γ 选出的网络可能完全相同。
# 下面用一个“已知真实网络、边较弱、n = 150”的模拟数据，γ 的作用会更明显：
set.seed(63)
tn <- genGGM(12, p = 0.2, nei = 1, propPositive = 0.8, constant = 1.5)   # 真实网络（12 条边）
Xs <- ggmGenerator()(150, tn)
cat("模拟数据真实边数 =", sum(tn[upper.tri(tn)] != 0), "\n")
for (g in c(0, 0.25, 0.5)) {
  ns <- suppressWarnings(estimateNetwork(Xs, default = "EBICglasso", tuning = g, verbose = FALSE))
  est <- ns$graph[upper.tri(ns$graph)] != 0; tru <- tn[upper.tri(tn)] != 0
  cat("γ =", g, "：估计边数 =", sum(est), "；其中假阳性 =", sum(est & !tru), "\n")
}
cat("γ 越大 → 网络越稀疏（sparse），假阳性边越少，但也可能漏掉真实的弱边。\n")
# 对比：不正则化的偏相关网络（满屏小边）
pcor_full <- qgraph::getWmat(qgraph(cor_auto(items_t1, verbose = FALSE), graph = "pcor", DoNotPlot = TRUE))
cat("非正则化偏相关网络的非零边数 =", sum(abs(pcor_full[upper.tri(pcor_full)]) > 0), "/ 36\n")
png_open("L6-3_gamma.png", 2400, 900)
par(mfrow = c(1, 3)); L <- averageLayout(nets[[1]], nets[[2]], nets[[3]])
for (g in names(nets)) plot(nets[[g]], layout = L, groups = groups_list, maximum = 0.5,
                            legend = FALSE, title = paste("γ =", g))
invisible(dev.off())
# 核对：EBIC 在每个 γ 下选中的 λ，以及它在 λ 序列中的位置（是否落在序列最小端）
cat("\nEBIC 选中的 λ（课程数据，N = 800）：\n")
for (g in names(nets)) {
  r <- nets[[g]]$results
  if (!is.list(r) || is.null(r$lambda) || is.null(r$ebic))  # 万一 bootnet 没有保存全部结果，就直接重算
    r <- qgraph::EBICglasso(cor_auto(items_t1, verbose = FALSE), n = nrow(items_t1),
                            gamma = as.numeric(g), returnAllResults = TRUE)
  lam <- r$lambda; i <- which.min(r$ebic)
  cat("γ =", g, "：λ =", signif(lam[i], 4), "；序列共", length(lam), "个 λ（",
      signif(min(lam), 4), "–", signif(max(lam), 4), "），选中的是从大到小第",
      rank(-lam)[i], "个；是否为序列最小端：", if (lam[i] == min(lam)) "是" else "否", "\n")
}
log_close()
