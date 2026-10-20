# =====================================================================
# L7-3.R  CLPN 可视化与解读  (Plotting & interpreting a CLPN)
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L7-3_log.txt")
dat <- read_course_data()
set.seed(2026)
B <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], rule = "lambda.min")  # 与 L7-2 相同的估计
CL <- cl_only(B); labs <- rownames(B)

# ---- 课件代码：有向网络图（不画自回归环 self-loops）----
png_open("L7-3_clpn.png", 1800, 1500)
qgraph(CL, directed = TRUE, layout = "spring",
       labels = labs, groups = list(孤独 = 1:4, 抑郁 = 5:9),
       theme = "colorblind", asize = 4, legend = TRUE,
       nodeNames = paste(labs, item_zh[labs]), legend.cex = 0.45,
       title = "CLPN（T1 → T2），lambda.min；未显示自回归边")
invisible(dev.off())
# 只显示 |β| ≥ 0.05 的边（显示阈值 display threshold：只改变图，不改变模型，须在图注说明）
png_open("L7-3_clpn_threshold.png", 1800, 1500)
qgraph(CL, directed = TRUE, layout = "spring", labels = labs, groups = groups_list,
       theme = "colorblind", asize = 4, threshold = 0.05, legend = TRUE, curveAll = TRUE, curve = 0.4,
       title = "仅显示 |β| ≥ 0.05 的交叉滞后边（图注须说明）")
invisible(dev.off())

# 表格：自回归边 + 最强交叉滞后边
cat("自回归边（AR）：\n"); print(round(diag(B), 3))
el <- edge_list(CL)
el$from_zh <- item_zh[el$from]; el$to_zh <- item_zh[el$to]
cat("\n最强的 10 条交叉滞后边：\n"); print(head(el, 10), row.names = FALSE, digits = 3)
write.csv(el, out("L7-3_cl_edges.csv"), row.names = FALSE)
top_x <- el[comm[match(el$from, items)] != comm[match(el$to, items)], ][1, ]   # 最强的跨构念边
cat(sprintf("\n谨慎写法示例：“控制所有 T1 题目后，T1 的‘%s’对 T2 的‘%s’有最强的独特（跨构念）预测作用（β = %.2f）”，\n而不是“%s导致%s”。\n",
    top_x$from_zh, top_x$to_zh, top_x$weight, top_x$from_zh, top_x$to_zh))
log_close()
