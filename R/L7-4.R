# =====================================================================
# L7-4.R  出期望影响、入期望影响与跨构念桥接  (out-EI, in-EI, bridge EI)
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L7-4_log.txt")
dat <- read_course_data()
set.seed(2026)
B <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)])
CL <- cl_only(B); p <- ncol(CL)

# ---- 课件代码 ----
outEI <- rowSums(CL)   # 第 k 行求和：从该节点出发的边（预测他人）
inEI  <- colSums(CL)   # 第 j 列求和：指向该节点的边（被他人预测）
comm  <- c(rep("孤独", 4), rep("抑郁", 5))
bridgeOut <- sapply(seq_len(p), function(k) sum(CL[k, comm != comm[k]]))   # 只算跨构念的出边
bridgeIn  <- sapply(seq_len(p), function(j) sum(CL[comm != comm[j], j]))   # 只算跨构念的入边
res <- data.frame(节点 = rownames(CL), 中文 = item_zh[rownames(CL)], 构念 = comm,
                  outEI, inEI, bridgeOut, bridgeIn, row.names = NULL)
print(res, digits = 3)
write.csv(res, out("L7-4_EI.csv"), row.names = FALSE)

# 哪个构念更多地“预测”另一个？
l2d <- sum(CL[comm == "孤独", comm == "抑郁"]); d2l <- sum(CL[comm == "抑郁", comm == "孤独"])
cat("\n孤独 → 抑郁 边权之和 =", round(l2d, 3), "；抑郁 → 孤独 边权之和 =", round(d2l, 3), "\n")

# 并排条形图（z 分数也可以；这里用原始值）
png_open("L7-4_EI_bars.png", 2000, 1000)
par(mfrow = c(1, 2), mar = c(4, 7, 3, 1))
cols <- ifelse(comm == "孤独", "#56B4E9", "#E69F00")
barplot(rev(outEI), horiz = TRUE, las = 1, col = rev(cols), names.arg = rev(paste(rownames(CL), item_zh)),
        main = "出期望影响 out-EI", cex.names = .8); abline(v = 0)
barplot(rev(inEI), horiz = TRUE, las = 1, col = rev(cols), names.arg = rev(paste(rownames(CL), item_zh)),
        main = "入期望影响 in-EI", cex.names = .8); abline(v = 0)
invisible(dev.off())
# qgraph 自带：有向网络的 InExpectedInfluence / OutExpectedInfluence
g <- qgraph(CL, directed = TRUE, DoNotPlot = TRUE)
png_open("L7-4_centralityPlot.png", 1400, 1400)
suppressWarnings(print(centralityPlot(g, include = c("OutExpectedInfluence", "InExpectedInfluence"),
                     scale = "raw0", print = FALSE)))
invisible(dev.off())
# ---- 与两种真值对照（只有模拟数据能做）----
# 总体目标值 data/true_B_population.csv：标准 CLPN 在样本无限大时的目标，含稳定特质的作用；
# 被试内真值 data/true_B_within.csv：生成数据时用的被试内滞后系数。两者算出的 EI 也不同。
Bt <- true_B()[rownames(CL), colnames(CL)]; diag(Bt) <- 0
Bw <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))[rownames(CL), colnames(CL)]; diag(Bw) <- 0
tru <- data.frame(节点 = rownames(CL), outEI_估计 = outEI, outEI_总体目标 = rowSums(Bt), outEI_被试内 = rowSums(Bw),
                  inEI_估计 = inEI, inEI_总体目标 = colSums(Bt), inEI_被试内 = colSums(Bw), row.names = NULL)
cat("\n估计的 EI 与两种真值算出的 EI：\n"); print(tru, digits = 3)
rho <- function(a, b) round(cor(a, b, method = "spearman"), 2)
cat("out-EI 排序与总体目标值的斯皮尔曼相关 =", rho(outEI, rowSums(Bt)), "；与被试内真值 =", rho(outEI, rowSums(Bw)), "\n")
cat("in-EI 排序与总体目标值的斯皮尔曼相关 =", rho(inEI, colSums(Bt)), "；与被试内真值 =", rho(inEI, colSums(Bw)), "\n")
cat("孤独 → 抑郁 边权之和：估计", round(l2d, 3), "；总体目标值", round(sum(Bt[comm == "孤独", comm == "抑郁"]), 3),
    "；被试内真值", round(sum(Bw[comm == "孤独", comm == "抑郁"]), 3), "\n")
cat("抑郁 → 孤独 边权之和：估计", round(d2l, 3), "；总体目标值", round(sum(Bt[comm == "抑郁", comm == "孤独"]), 3),
    "；被试内真值", round(sum(Bw[comm == "抑郁", comm == "孤独"]), 3), "\n")
write.csv(tru, out("L7-4_EI_truth.csv"), row.names = FALSE)
log_close()
