# =====================================================================
# L0-2.R  为什么要学交叉滞后网络：偷看课程数据的“真实答案”
# (Why CLPN: a first look at the true within-person lag matrix)
# 讲义 0.2 的代码框；0.2 课时你还没装 R，可以等 2.1 课装好后再回来运行。
# 后半段“先跑一遍”需要 glmnet 和 qgraph 两个包（安装方法见 0.2 课页面或 2.4 课）。
# 运行：在 RStudio 中打开 clpn-course.Rproj，打开本文件，点 “Source”。
# =====================================================================
source("R/_setup.R")
log_open("L0-2_log.txt")      # 屏幕输出同时保存到 R/output/L0-2_log.txt

# 生成模拟数据时写进程序的被试内滞后结构（data/simulate_data.R）
B <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))
print(B)                       # 行 = T1 的题目（箭头起点），列 = T2 的题目（箭头终点）
cat("\n对角线：自回归（每道题自己 T1 → T2）\n")
print(diag(B))
CL <- B; diag(CL) <- 0         # 把对角线清零，只剩交叉滞后边
cat("\n哪些交叉滞后格子不是 0？（row = 起点，col = 终点）\n")
print(which(CL != 0, arr.ind = TRUE))
cat("\n“与人隔绝”T1 → “情绪低落”T2：\n")
print(B["lone3", "dep1"])

# ---- 先跑一遍：第一个 CLPN（第 2 周装好 R 之后做，约 30 分钟；每一步在后面哪一课讲，见 0.2 课页面）----
# 估计的写法与 R/L7-3.R 完全相同（同一个种子 2026、同一个 lambda.min 规则），所以结果与 7.3 课一致。
library(qgraph)
cat("\n==== 先跑一遍：第一个 CLPN（T1 → T2）====\n")
dat <- read_course_data()                        # 读入课程模拟数据（宽格式，一行一个人）
X <- dat[, vars_t(1)]                            # T1 的 9 道题
Y <- dat[, vars_t(2)]                            # T2 的同样 9 道题（同样顺序）
set.seed(2026)                                   # 交叉验证随机分折，设种子保证结果可重复
B <- clpn_estimate(X, Y, rule = "lambda.min")    # 逐节点 LASSO：每道 T2 题对全部 T1 题做一次回归
cat("估计的 B（lambda.min）：\n"); print(round(B, 2))
CL <- cl_only(B)                                 # 去掉对角线（自回归），只留交叉滞后边
cat("\n72 个交叉滞后格子中不为 0 的：", sum(CL != 0), " 条\n", sep = "")
el <- edge_list(CL)                              # 边列表，按 |权重| 从大到小排
el$from_zh <- item_zh[el$from]; el$to_zh <- item_zh[el$to]
cat("\n最强的 10 条交叉滞后边：\n"); print(head(el, 10), row.names = FALSE, digits = 3)
png_open("L0-2_quick_clpn.png", 1800, 1500)
qgraph(CL, directed = TRUE, layout = "spring",
       labels = rownames(B), groups = groups_list,
       theme = "colorblind", asize = 4, legend = TRUE,
       nodeNames = item_zh[rownames(B)], legend.cex = 0.45,
       title = "我的第一个 CLPN（T1 → T2），lambda.min；未显示自回归边")
invisible(dev.off())
log_close()
