# 练习答案 L6-4：加入 nodeNames 的网络图（练习 1）；T1 与 T2 网络对比（练习 2）
source("R/_setup.R")
need_output("L6-4_dep_anx_items.csv", "R/L6-4.R")   # 前置结果检查
suppressPackageStartupMessages({ library(bootnet); library(qgraph) })
log_open("sol_L6-4_log.txt")
items16 <- read.csv(out("L6-4_dep_anx_items.csv"))      # 由 R/L6-4.R 生成
net <- estimateNetwork(items16, default = "EBICglasso", tuning = 0.5, corMethod = "cor_auto", verbose = FALSE)
png_open("sol_L6-4_nodenames.png", 2200, 1400)
plot(net, layout = "spring", groups = list(抑郁 = 1:9, 焦虑 = 10:16),
     nodeNames = c(paste("抑郁题", 1:9), paste("焦虑题", 1:7)), legend.cex = 0.4, palette = "colorblind")
invisible(dev.off())
cat("练习 1：图已保存 R/output/sol_L6-4_nodenames.png\n")
# 练习 2：课程数据 T1 与 T2 的横断面网络
dat <- read_course_data()
x1 <- dat[, vars_t(1)]; x2 <- dat[, vars_t(2)]; names(x1) <- names(x2) <- items
n1 <- estimateNetwork(x1, default = "EBICglasso", corMethod = "cor_auto", verbose = FALSE)
n2 <- estimateNetwork(x2, default = "EBICglasso", corMethod = "cor_auto", verbose = FALSE)
L  <- averageLayout(n1, n2); mx <- max(abs(c(n1$graph, n2$graph)))
png_open("sol_L6-4_T1_T2.png", 2400, 1100)
par(mfrow = c(1, 2))
plot(n1, layout = L, maximum = mx, groups = groups_list, title = "T1")
plot(n2, layout = L, maximum = mx, groups = groups_list, title = "T2")
invisible(dev.off())
ut <- upper.tri(n1$graph)
cat("练习 2：T1 边数 =", sum(n1$graph[ut] != 0), "；T2 边数 =", sum(n2$graph[ut] != 0),
    "；两网络边权相关 =", round(cor(n1$graph[ut], n2$graph[ut]), 3), "\n")
log_close()
