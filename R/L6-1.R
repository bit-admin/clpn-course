# =====================================================================
# L6-1.R  网络的语言：节点、边、权重与邻接矩阵  (Nodes, edges, weights matrix)
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L6-1_log.txt")
labs5 <- c("孤独", "失眠", "疲劳", "低落", "支持")
# 无向网络（undirected）：权重矩阵对称（symmetric），W[i,j] = W[j,i]
W <- matrix(c( 0, .3,  0, .4, -.3,
              .3,  0, .5,  0,   0,
               0, .5,  0, .2,   0,
              .4,  0, .2,  0, -.2,
             -.3,  0,  0, -.2,  0), 5, 5, byrow = TRUE, dimnames = list(labs5, labs5))
print(W); cat("对称吗？", isSymmetric(W), "\n")
cat("密度 density = 非零边数 / 可能边数 =", sum(W[upper.tri(W)] != 0), "/", choose(5, 2), "\n")
png_open("L6-1_undirected.png", 1400, 1300)
qgraph(W, labels = labs5, edge.labels = TRUE, theme = "colorblind", label.font = 1,
       title = "无向网络：蓝/实线=正边，红/虚线=负边（colorblind 主题）")
invisible(dev.off())
# 有向网络（directed）：W[i, j] 表示从 i（行）指向 j（列）
D <- matrix(0, 3, 3, dimnames = list(labs5[1:3], labs5[1:3])); D["孤独", "失眠"] <- .4; D["失眠", "疲劳"] <- .5
png_open("L6-1_directed.png", 1200, 1100)
qgraph(D, directed = TRUE, edge.labels = TRUE, asize = 6, theme = "colorblind", title = "有向网络：D[\"孤独\",\"失眠\"] = 孤独 → 失眠")
invisible(dev.off())
log_close()
