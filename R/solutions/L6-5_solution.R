# 练习答案 L6-5：桥接 EI 前 2 名与谨慎解释
source("R/_setup.R"); suppressPackageStartupMessages({ library(bootnet); library(networktools) })
log_open("sol_L6-5_log.txt")
# 与 R/L6-5.R 相同：桥接用课程数据 T1 的 9 题（genGGM 生成的 16 题数据没有真正的社群结构）
dat <- read_course_data()
t1 <- dat[, vars_t(1)]; colnames(t1) <- items
net <- estimateNetwork(t1, default = "EBICglasso", tuning = .5, corMethod = "cor_auto", verbose = FALSE)
b <- bridge(net$graph, communities = ifelse(items %in% lone_items, "孤独", "抑郁"))
top <- sort(b$`Bridge Expected Influence (1-step)`, decreasing = TRUE)[1:2]; print(round(top, 3))
cat("谨慎解释：", names(top)[1], "（", item_zh[names(top)[1]], "）和", names(top)[2], "（", item_zh[names(top)[2]], "）",
    "与另一构念的同期联系最强（横断面、关联性），它们可能是孤独与抑郁共同出现的“连接点”候选，\n",
    "但这不是因果证据，也不说明时间方向；还需检查稳定性（bootnet）。\n")
log_close()
