# =====================================================================
# L6-4.R  用 qgraph 与 bootnet 估计并可视化网络  (estimateNetwork + qgraph)
# 课件示例用“抑郁 9 题 + 焦虑 7 题”：这里先模拟这样一份横断面数据
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(qgraph) })
log_open("L6-4_log.txt")
set.seed(64)
# genGGM 生成一个“真实”网络；ggmGenerator 根据网络生成 4 级定序数据（nLevels = 4）
true_net <- genGGM(16, p = 0.15, nei = 2, propPositive = 0.9, constant = 1.5)
gen <- ggmGenerator(ordinal = TRUE, nLevels = 4)
items <- as.data.frame(gen(600, true_net))
colnames(items) <- c(paste0("D", 1:9), paste0("A", 1:7))   # D = 抑郁 depression, A = 焦虑 anxiety
write.csv(items, out("L6-4_dep_anx_items.csv"), row.names = FALSE)

# ---- 课件代码 ----
net <- estimateNetwork(items, default = "EBICglasso",
                       tuning = 0.5, corMethod = "cor_auto", verbose = FALSE)
png_open("L6-4_network.png", 1800, 1400)
plot(net, layout = "spring",
     groups = list(抑郁 = 1:9, 焦虑 = 10:16),
     legend = TRUE, palette = "colorblind", title = "抑郁–焦虑 EBICglasso 网络")
invisible(dev.off())
# 可投稿 PDF（矢量图）：cairo_pdf 支持中文
if (capabilities("cairo")) {
  cairo_pdf(out("L6-4_network.pdf"), 8, 6, family = cn_font)
  plot(net, layout = "spring", groups = list(抑郁 = 1:9, 焦虑 = 10:16), legend = TRUE, palette = "colorblind")
  invisible(dev.off())
}
cat("估计网络边数 =", sum(net$graph[upper.tri(net$graph)] != 0), "\n")
saveRDS(net, out("L6-4_net.rds"))
log_close()
