# =====================================================================
# L6-5.R  中心性：强度、期望影响与桥接中心性  (Strength, EI, bridge centrality)
# =====================================================================
source("R/_setup.R")
need_output("L6-4_dep_anx_items.csv", "R/L6-4.R")   # 前置结果检查
suppressPackageStartupMessages({ library(bootnet); library(qgraph); library(networktools) })
log_open("L6-5_log.txt")
d16 <- read.csv(out("L6-4_dep_anx_items.csv"))     # 需先运行 L6-4.R
net <- estimateNetwork(d16, default = "EBICglasso", tuning = 0.5, corMethod = "cor_auto", verbose = FALSE)
W <- net$graph
strength <- colSums(abs(W))                         # 强度 = Σ|w|
EI       <- colSums(W)                              # 期望影响 = Σw（保留正负号）
print(round(data.frame(strength, EI), 3))
cat("例：只有 +0.3 和 −0.3 两条边的节点：强度 = 0.6，EI = 0\n")
png_open("L6-5_centrality.png", 1400, 1400)
suppressWarnings(print(centralityPlot(net, include = c("Strength", "ExpectedInfluence"), scale = "z-scores", print = FALSE)))
invisible(dev.off())
# 桥接中心性（bridge centrality）：需要事先指定社群（communities）。
# 上面的 16 题数据由 genGGM() 生成，真实网络是一个“环形格子”（每个节点只和编号相邻的节点相连），
# 并没有“抑郁”“焦虑”两个社群；在它上面算桥接，排名只反映编号在环上的位置。所以桥接改用课程数据：
# T1 的孤独 4 题 + 抑郁 5 题，社群按量表指定。
dat <- read_course_data()
t1 <- dat[, vars_t(1)]; colnames(t1) <- items        # items = 9 道题的名字（_setup.R）
net_c <- estimateNetwork(t1, default = "EBICglasso", tuning = 0.5, corMethod = "cor_auto", verbose = FALSE)
comm <- ifelse(items %in% lone_items, "孤独", "抑郁")
b <- bridge(net_c$graph, communities = comm)
bei <- sort(b$`Bridge Expected Influence (1-step)`, decreasing = TRUE)
cat("\n课程数据 T1（9 题，EBICglasso）的桥接 EI：\n")
print(round(bei, 3)); cat("桥接 EI 前 2 名：", names(bei)[1:2], "（", item_zh[names(bei)[1:2]], "）\n")
cat("跨社群的边（|w| > 0）：\n")
Wc <- net_c$graph
for (k in lone_items) for (j in dep_items) if (abs(Wc[k, j]) > 0)
  cat(sprintf("  %s（%s）— %s（%s）：%.3f\n", k, item_zh[k], j, item_zh[j], Wc[k, j]))
png_open("L6-5_bridge.png", 1400, 1400); suppressWarnings(print(plot(b, include = "Bridge Expected Influence (1-step)"))); invisible(dev.off())
log_close()
