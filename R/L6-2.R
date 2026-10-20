# =====================================================================
# L6-2.R  偏相关网络与高斯图模型（GGM）  (Partial correlations & GGM)
# 例子：失眠 → 疲劳 → 注意力差（链式结构 chain）
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L6-2_log.txt")
set.seed(62)
n <- 1000
失眠 <- rnorm(n)
疲劳 <- 0.6 * 失眠 + rnorm(n, 0, .8)
注意力差 <- 0.6 * 疲劳 + rnorm(n, 0, .8)          # 注意力差只受疲劳影响
d <- data.frame(失眠, 疲劳, 注意力差)
cat("相关 correlation：\n"); print(round(cor(d), 2))
P <- solve(cor(d))                                 # 精度矩阵 precision matrix = 相关矩阵的逆
pc <- -cov2cor(P); diag(pc) <- 1                   # 偏相关 = 标准化后取负号
cat("\n偏相关 partial correlation：\n"); print(round(pc, 2))
cat("失眠–注意力差：相关 =", round(cor(失眠, 注意力差), 2), "，偏相关 ≈", round(pc[1, 3], 2),
    "→ 控制疲劳后两者条件独立（conditional independence），GGM 中没有边。\n")
# 偏相关 ↔ 多元回归：注意力差 ~ 失眠 + 疲劳 中失眠的系数也≈0
print(round(coef(lm(注意力差 ~ 失眠 + 疲劳)), 3))
png_open("L6-2_cor_vs_pcor.png", 2000, 1000)
par(mfrow = c(1, 2))
qgraph(cor(d), graph = "cor",  labels = names(d), edge.labels = TRUE, theme = "colorblind", title = "相关网络", layout = "circle")
qgraph(cor(d), graph = "pcor", labels = names(d), edge.labels = TRUE, theme = "colorblind", title = "偏相关网络", layout = "circle")
invisible(dev.off())
log_close()
