# =====================================================================
# case_elsoc.R  真实数据案例：ELSOC 抑郁症状（PHQ-8）的交叉滞后面板网络
# Real-data case: a cross-lagged panel network of PHQ-8 symptoms in ELSOC (Chile, 2016–2018)
# 配套页面：materials/case_elsoc.html。分析文件 data/elsoc_phq8_wide.csv 随课程提供，直接运行即可；
#   它是怎样从原始数据得到的，见 R/data_elsoc.R。
#
# 数据：Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022,
#   "Estudio Longitudinal Social de Chile 2016-2021", https://doi.org/10.7910/DVN/LQMURF,
#   Harvard Dataverse, V1, UNF:6:z/vWFguq9fg03YaOLWFddA== [fileUNF]（CC0 1.0）
# 做的事（与课程第 7–8 模块相同的流程，换成真实数据）：
#   1 描述统计  2 CLPN（2016 → 2017，lambda.min，10 折，种子 2026）  3 出 / 入期望影响
#   4 复现：2017 → 2018  5 敏感性：加性别、年龄（不惩罚）  6 边的 bootstrap（200 次，演示用）
# 输出：R/output/case_elsoc_log.txt、case_elsoc_B.csv、case_elsoc_EI.csv、case_elsoc_boot.csv、case_elsoc_clpn.png
#   （都是汇总结果，不含任何个人数据）
# 运行时间：约 1–2 分钟（大部分在第 6 步；把 B_BOOT 改成 1000 约 5–8 分钟）
# =====================================================================
source("R/_setup.R")
library(glmnet)
library(qgraph)
options(width = 110)
t_start <- Sys.time()

f <- "data/elsoc_phq8_wide.csv"
if (!file.exists(f)) {
  stop("找不到 ", f, "。这个文件随课程提供；如果被删掉了，运行 source(\"R/data_elsoc.R\") 可以\n",
       "从原始文件重新生成（原始文件也不在时，它会从 Harvard Dataverse 下载）。",
       call. = FALSE)
}
log_open("case_elsoc_log.txt")
cat("ELSOC 真实数据案例：PHQ-8 的 CLPN\n")
cat("数据：Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022, \"Estudio Longitudinal Social de Chile 2016-2021\",\n      https://doi.org/10.7910/DVN/LQMURF, Harvard Dataverse, V1\n")
cat("预处理：R/data_elsoc.R（原始样本；负数缺失码设为 NA；PHQ 第 1–8 题）\n\n")

w <- read.csv(f)
phq <- paste0("phq", 1:8)
phq_zh <- c(phq1 = "兴趣减退", phq2 = "情绪低落", phq3 = "睡眠问题", phq4 = "疲乏",
            phq5 = "食欲改变", phq6 = "注意力难集中", phq7 = "自我评价低", phq8 = "动作迟缓")
vt <- function(t) paste0(phq, "_t", t)
a <- w[complete.cases(w[, c(vt(1), vt(2), vt(3))]), ]
cat("== 1 描述统计 ==\n")
cat("分析样本（第 1–3 波 PHQ-8 都完整）N =", nrow(a), "\n")
desc <- data.frame(题目 = phq, 中文 = phq_zh[phq],
                   M_2016 = round(colMeans(a[, vt(1)]), 2), SD_2016 = round(apply(a[, vt(1)], 2, sd), 2),
                   M_2017 = round(colMeans(a[, vt(2)]), 2), M_2018 = round(colMeans(a[, vt(3)]), 2), row.names = NULL)
print(desc, row.names = FALSE)
tot <- sapply(1:3, function(t) rowSums(a[, vt(t)]))
cat(sprintf("PHQ-8 总分（8–40）：2016 M = %.2f，2017 M = %.2f，2018 M = %.2f；2016 与 2017 总分相关 r = %.2f\n\n",
            mean(tot[, 1]), mean(tot[, 2]), mean(tot[, 3]), cor(tot[, 1], tot[, 2])))

cat("== 2 CLPN：2016 → 2017（lambda.min，10 折交叉验证，种子 2026）==\n")
set.seed(2026)
B <- clpn_estimate(a[, vt(1)], a[, vt(2)])
CL <- cl_only(B)
n_cl <- sum(CL != 0)
cat("自回归边（AR）：\n"); print(round(diag(B), 3))
cat(sprintf("非零交叉滞后边：%d / 56 条；最大 |B| = %.3f\n", n_cl, max(abs(CL))))
e <- edge_list(CL)
e$from_zh <- phq_zh[e$from]; e$to_zh <- phq_zh[e$to]; e$weight <- round(e$weight, 3)
cat("最强的 8 条交叉滞后边：\n"); print(head(e[, c("from", "from_zh", "to", "to_zh", "weight")], 8), row.names = FALSE)
write.csv(round(B, 4), out("case_elsoc_B.csv"))

cat("\n== 3 出 / 入期望影响（只算交叉滞后边，不含自回归）==\n")
EI <- data.frame(节点 = phq, 中文 = phq_zh[phq], outEI = round(rowSums(CL), 3), inEI = round(colSums(CL), 3), row.names = NULL)
print(EI[order(-EI$outEI), ], row.names = FALSE)
write.csv(EI, out("case_elsoc_EI.csv"), row.names = FALSE)

cat("\n== 4 复现：2017 → 2018 ==\n")
set.seed(2026)
B23 <- clpn_estimate(a[, vt(2)], a[, vt(3)])
off <- row(B) != col(B)
cat(sprintf("2017 → 2018 非零交叉滞后边：%d / 56 条；与 2016 → 2017 的 56 条交叉滞后边的相关 r = %.2f\n",
            sum(cl_only(B23) != 0), cor(B[off], B23[off])))
top8 <- head(e, 8)
same <- sapply(seq_len(nrow(top8)), function(i) sign(B23[top8$from[i], top8$to[i]]) == sign(top8$weight[i]) && B23[top8$from[i], top8$to[i]] != 0)
cat(sprintf("最强 8 条边中，在 2017 → 2018 里同方向且非零的有 %d 条\n", sum(same)))

cat("\n== 5 敏感性：加入性别、年龄作为协变量（不惩罚）==\n")
ok <- complete.cases(a[, c("female", "age")])
set.seed(2026)
Bc <- clpn_estimate(a[ok, vt(1)], a[ok, vt(2)], covariates = a[ok, c("female", "age")])
cat(sprintf("N = %d；非零交叉滞后边 %d / 56 条；与主分析交叉滞后边的相关 r = %.3f\n",
            sum(ok), sum(cl_only(Bc) != 0), cor(B[off], Bc[off])))

cat("\n== 6 边的非参数 bootstrap（B_BOOT = 200 次，演示用；正式分析请用 ≥ 1000 次）==\n")
B_BOOT <- 200
set.seed(2026)
t_boot <- Sys.time()
boots <- replicate(B_BOOT, {
  i <- sample(nrow(a), replace = TRUE)
  cl_only(clpn_estimate(a[i, vt(1)], a[i, vt(2)]))[off]
})
nm <- paste0(rownames(B)[row(B)[off]], ">", colnames(B)[col(B)[off]])
bt <- data.frame(edge = nm, sample = round(B[off], 3),
                 q2.5 = round(apply(boots, 1, quantile, 0.025), 3), q97.5 = round(apply(boots, 1, quantile, 0.975), 3),
                 prop0 = round(rowMeans(boots == 0), 3))
bt <- bt[order(-abs(bt$sample)), ]
write.csv(bt, out("case_elsoc_boot.csv"), row.names = FALSE)
cat("最强 8 条交叉滞后边的 bootstrap 区间（2.5% 与 97.5% 分位数）与被压成 0 的比例：\n")
print(head(bt, 8), row.names = FALSE)
cat(sprintf("最强 8 条边中，区间不含 0 的有 %d 条\n", sum(head(bt, 8)$q2.5 > 0 | head(bt, 8)$q97.5 < 0)))
boot_secs <- round(as.numeric(difftime(Sys.time(), t_boot, units = "secs")))   # 用时随电脑不同，不写进日志

png_open("case_elsoc_clpn.png")
qgraph(CL, directed = TRUE, layout = "spring", labels = phq, theme = "colorblind", asize = 4,
       nodeNames = unname(phq_zh[phq]), legend = TRUE, legend.cex = 0.5,
       title = "ELSOC PHQ-8：CLPN（2016 → 2017），lambda.min；未显示自回归边")
invisible(dev.off())
cat("\n图：R/output/case_elsoc_clpn.png\n")
log_close()
cat("用时", round(as.numeric(difftime(Sys.time(), t_start, units = "secs"))), "秒（其中 bootstrap", boot_secs, "秒）\n")
