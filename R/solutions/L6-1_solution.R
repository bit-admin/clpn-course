# 练习答案 L6-1：自己写 5×5 权重矩阵并用 qgraph 画出
source("R/_setup.R"); library(qgraph)
log_open("sol_L6-1_log.txt")
labs <- c("孤独", "失眠", "疲劳", "低落", "社交")
W <- matrix(0, 5, 5, dimnames = list(labs, labs))
W["孤独", "低落"] <- .4; W["失眠", "疲劳"] <- .5; W["疲劳", "低落"] <- .3; W["孤独", "社交"] <- -.35
W <- W + t(W)                                 # 无向网络 → 对称
stopifnot(isSymmetric(W))
png_open("sol_L6-1_network.png", 1300, 1200); qgraph(W, labels = labs, edge.labels = TRUE, theme = "colorblind"); invisible(dev.off())
# 答：无向网络矩阵对称；有向网络中 [i, j] = 从 i 指向 j；粗细 = |权重|，颜色 = 正（蓝）/负（红）。
log_close()
