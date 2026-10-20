# 练习答案 L8-3：根据 CS 系数决定如何表述（需先运行 L8-3.R）
source("R/_setup.R")
need_output("L8-3_CS.csv", "R/L8-3.R")   # 前置结果检查
need_output("L8-2_boot.rds", "R/L8-2.R")  # 第 2、3 部分要用 8.2 课保存的 1000 次非参数 bootstrap
log_open("sol_L8-3_log.txt")
cs <- read.csv(out("L8-3_CS.csv")); print(cs)
step <- diff(seq(0.05, 0.75, length.out = 10))[1]   # bootnet 默认删除比例网格的一档（约 0.08）
for (i in seq_len(nrow(cs))) {
  if (cs$CS[i] < .25) cat(sprintf(paste0("%s 的 CS = %.2f < 0.25：降级表述示例——“%s 的中心性排序在删除少量个案后",
    "即不稳定，因此本研究不对哪个节点‘最具影响力’作出结论，仅作探索性描述。”\n"), cs$指标[i], cs$CS[i], cs$指标[i]))
  else if (cs$CS[i] < .5) cat(sprintf("%s 的 CS = %.2f（0.25–0.5）：可接受但未达理想，排序只作谨慎解释，仍应使用“预测”而非“影响/导致”。\n", cs$指标[i], cs$CS[i]))
  else if (cs$CS[i] < .5 + step) cat(sprintf("%s 的 CS = %.2f：刚达到 0.5，只比界值高一个网格档（换随机种子可能落到下一档）：边缘稳定，解释排序须谨慎，仍应使用“预测”而非“影响/导致”。\n", cs$指标[i], cs$CS[i]))
  else cat(sprintf("%s 的 CS = %.2f：可以报告排序，但仍应使用“预测”而非“影响/导致”。\n", cs$指标[i], cs$CS[i]))
}

# ---- 第 2 部分：“孤独 → 抑郁的边权总和高于反方向”能不能写？----
# 降级表述里常用构念层面的总和。但“高于”是一个比较，要先检验：在 8.2 课保存的 1000 个
# bootstrap 网络里，逐个计算 差值 = Σ B[孤独, 抑郁] − Σ B[抑郁, 孤独]，看差值分布的 2.5% 与 97.5% 分位数。
# 区间不含 0，才可以写“孤独 → 抑郁方向的边权总和大于反方向”；含 0，只能写“没有检出方向差异”。
# 注意：LASSO 的收缩同样作用在这里，这个区间只是对精确度的描述（8.2 课），不是严格的 95% 置信区间。
boot <- readRDS(out("L8-2_boot.rds"))
dir_sums <- function(B) {
  dimnames(B) <- list(items, items)                 # 行 = T1（from），列 = T2（to）
  c(lone_to_dep = sum(B[lone_items, dep_items]), dep_to_lone = sum(B[dep_items, lone_items]))
}
s0 <- dir_sums(boot$sample$graph)
sb <- t(sapply(boot$boots, function(b) dir_sums(b$graph)))
d_b <- sb[, "lone_to_dep"] - sb[, "dep_to_lone"]
cat("\n构念层面的边权总和（原样本）：孤独 → 抑郁 =", round(s0["lone_to_dep"], 3),
    "；抑郁 → 孤独 =", round(s0["dep_to_lone"], 3), "；差值 =", round(s0["lone_to_dep"] - s0["dep_to_lone"], 3), "\n")
cat("差值的 bootstrap 分位数（", length(d_b), "次）：2.5% =", round(quantile(d_b, .025), 3),
    "，97.5% =", round(quantile(d_b, .975), 3), "；差值 ≤ 0 的比例 =", round(mean(d_b <= 0), 3), "\n")
cat(if (quantile(d_b, .025) > 0) "结论：区间不含 0，可以写“孤独 → 抑郁方向的边权总和大于反方向”（仍是预测关系，不是因果）。\n"
    else "结论：区间含 0，只能写“两个方向的边权总和没有检出差异”。\n")
# 带符号求和时，正负边会互相抵消；想看“连接有多强”而不管方向符号，可以把 sum() 换成 sum(abs())，再算一遍。

# ---- 第 3 部分：bootnet 的 out/inExpectedInfluence 去掉了自回归吗？----
# 7.4 课手算的 out-EI / in-EI 不含自回归（对角线）。这里把 bootnet 在原样本上算出的值，
# 与“去掉对角线”和“保留对角线”两种手算结果对照；与哪一列一致，就说明 bootnet 用的是哪种口径。
B0 <- boot$sample$graph; dimnames(B0) <- list(items, items)
CL0 <- B0; diag(CL0) <- 0
st <- boot$sampleTable
bn_out <- setNames(st$value[st$type == "outExpectedInfluence"], st$node1[st$type == "outExpectedInfluence"])[items]
bn_in  <- setNames(st$value[st$type == "inExpectedInfluence"],  st$node1[st$type == "inExpectedInfluence"])[items]
cmp <- data.frame(node = items,
                  bootnet_out = round(bn_out, 3), hand_out_noAR = round(rowSums(CL0), 3), hand_out_withAR = round(rowSums(B0), 3),
                  bootnet_in  = round(bn_in, 3),  hand_in_noAR  = round(colSums(CL0), 3), hand_in_withAR  = round(colSums(B0), 3))
cat("\nbootnet 的期望影响 vs 手算（noAR = 去掉自回归，withAR = 保留自回归）：\n"); print(cmp, row.names = FALSE)
cat("bootnet 的 out-EI 与“去掉自回归”的手算一致：", isTRUE(all.equal(unname(bn_out), unname(rowSums(CL0)), tolerance = 1e-6)),
    "；in-EI 一致：", isTRUE(all.equal(unname(bn_in), unname(colSums(CL0)), tolerance = 1e-6)), "\n")
log_close()
