# =====================================================================
# L9-2.R  批判性评估：结论对分析决策是否敏感？  (Sensitivity / robustness checks)
# 检查 3 个“研究者自由度”（researcher degrees of freedom）：
#   λ 规则（lambda.min / lambda.1se / EBIC）、随机种子、题目冗余（topological overlap）
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(networktools))
log_open("L9-2_log.txt")
dat <- read_course_data()
X <- dat[, vars_t(1)]; Y <- dat[, vars_t(2)]
off <- matrix(TRUE, 9, 9); diag(off) <- FALSE
rules <- c("lambda.min", "lambda.1se", "ebic")
Bs <- lapply(rules, function(r) { set.seed(2026); clpn_estimate(X, Y, rule = r) }); names(Bs) <- rules
summ <- t(sapply(Bs, function(B) {
  CL <- cl_only(B); el <- edge_list(CL)
  c(CL边数 = sum(CL != 0), 最强边 = paste(el$from[1], "→", el$to[1]),
    outEI最高 = names(which.max(rowSums(CL))), inEI最高 = names(which.max(colSums(CL))))
}))
print(summ)

# 随机种子：cv.glmnet 的分折是随机的 —— 换 20 个种子，边会变吗？
seeds <- 1:20
arr <- sapply(seeds, function(s) { set.seed(s); clpn_estimate(X, Y)[off] })
nz <- rowMeans(arr != 0)
cat("\n换 20 个种子：始终非零的 CL 边 =", sum(nz == 1), "；始终为 0 =", sum(nz == 0),
    "；时有时无 =", sum(nz > 0 & nz < 1), "\n")
cat("→ 报告中必须写明种子；也可用 repeated CV（多次分折取平均）减小随机性。\n")

# 题目冗余：goldbricker() 找出内容/关联模式高度重叠的题目对
gb <- goldbricker(dat[, vars_t(1)], p = 0.05, method = "hittner2003", threshold = 0.25, corMin = 0.5, progressbar = FALSE)
cat("\n可能冗余的题目对（goldbricker）：\n"); print(gb$suggested_reductions)
log_close()
