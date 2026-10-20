# =====================================================================
# L10-2.R  毕业项目②：完整 CLPN 分析流程（一键运行）  (Full CLPN pipeline)
# 描述统计 → CLPN 估计 → 作图 → out/in-EI 与桥接 EI → bootstrap 边准确性
# → CS 系数 → 敏感性分析 → 与真实结构对照
# 所有输出以 L10-2_ 开头保存在 R/output/。单核运行约 15–40 分钟（视电脑而定；两次 1000 次 bootstrap；单核以保证可重复）。
# =====================================================================
source("R/_setup.R")
need_output("L10-1_clean_data.csv", "R/L10-1.R", chain = "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-3.R")   # 前置结果检查
suppressPackageStartupMessages({ library(glmnet); library(qgraph); library(bootnet) })
log_open("L10-2_log.txt")
SEED <- 2026; N_BOOTS <- 1000; N_CORES <- 1   # 单核 = 可重复（并行时 bootnet 重抽样不受 set.seed 控制，见 L8-2.R）
dat <- read.csv(out("L10-1_clean_data.csv"))          # 来自 L10-1.R
X <- dat[, vars_t(1)]; Y <- dat[, vars_t(2)]

## 1. 描述统计 ----------------------------------------------------------
desc <- round(psych::describe(cbind(X, Y))[, c("mean", "sd", "skew", "kurtosis")], 2)
print(desc); write.csv(desc, out("L10-2_table1_descriptives.csv"))

## 2. CLPN 估计 ---------------------------------------------------------
set.seed(SEED); B <- clpn_estimate(X, Y, rule = "lambda.min")
CL <- cl_only(B)
write.csv(round(B, 3), out("L10-2_table2_B_matrix.csv"))
el <- edge_list(B); el$from_zh <- item_zh[el$from]; el$to_zh <- item_zh[el$to]
write.csv(el, out("L10-2_table2_edges_AR_CL.csv"), row.names = FALSE)
cat("\n自回归边：\n"); print(round(diag(B), 3))
cat("\n最强 5 条交叉滞后边：\n"); print(head(el[el$type != "AR 自回归", ], 5), row.names = FALSE, digits = 3)

## 3. 网络图 ------------------------------------------------------------
png_open("L10-2_fig1_clpn.png", 1800, 1500)
qgraph(CL, directed = TRUE, layout = "spring", groups = groups_list, palette = "colorblind", theme = "colorblind",
       asize = 4, legend = TRUE, nodeNames = paste(items, item_zh[items]), legend.cex = .45,
       title = "图 1  T1→T2 交叉滞后面板网络（未显示自回归边）")
invisible(dev.off())

## 4. 中心性 ------------------------------------------------------------
cen <- data.frame(node = items, zh = item_zh[items], community = comm,
                  outEI = rowSums(CL), inEI = colSums(CL),
                  bridgeOutEI = sapply(1:9, function(k) sum(CL[k, comm != comm[k]])),
                  bridgeInEI  = sapply(1:9, function(j) sum(CL[comm != comm[j], j])), row.names = NULL)
print(cen, digits = 3); write.csv(cen, out("L10-2_table3_centrality.csv"), row.names = FALSE)
g <- qgraph(CL, directed = TRUE, DoNotPlot = TRUE)
png_open("L10-2_fig2_centrality.png", 1400, 1400)
suppressWarnings(print(centralityPlot(g, include = c("OutExpectedInfluence", "InExpectedInfluence"),
                                      scale = "z-scores", print = FALSE)))
invisible(dev.off())

## 5. bootstrap 边准确性 + 6. case-dropping CS --------------------------
clpn_fun <- function(data) {
  p <- ncol(data) / 2
  X <- scale(as.matrix(data[, 1:p])); Y <- scale(as.matrix(data[, (p + 1):(2 * p)]))
  B <- matrix(0, p, p)
  for (j in seq_len(p)) {
    cvfit <- glmnet::cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]
  }
  B
}
set.seed(SEED)
net <- estimateNetwork(cbind(X, Y), default = "none", fun = clpn_fun, directed = TRUE, labels = items)
set.seed(SEED)
boot <- bootnet(net, nBoots = N_BOOTS, type = "nonparametric", nCores = N_CORES, verbose = FALSE,
                statistics = c("edge", "outExpectedInfluence", "inExpectedInfluence"))
png_open("L10-2_fig3_bootstrap_edges.png", 1600, 3200)
suppressWarnings(print(plot(boot, statistics = "edge", order = "sample", labels = TRUE, CIstyle = "quantiles")))
invisible(dev.off())
bs <- as.data.frame(summary(boot, statistics = "edge"))
bs <- bs[order(-abs(bs$sample)), c("node1", "node2", "sample", "q2.5", "q97.5", "prop0")]
write.csv(bs, out("L10-2_table4_bootstrap_edges.csv"), row.names = FALSE)
set.seed(SEED)
cd <- bootnet(net, nBoots = N_BOOTS, type = "case", nCores = N_CORES, verbose = FALSE,
              statistics = c("outExpectedInfluence", "inExpectedInfluence"))
cs <- corStability(cd, verbose = FALSE)
write.csv(data.frame(statistic = names(cs), CS = round(cs, 3)), out("L10-2_table5_CS.csv"), row.names = FALSE)
cat("\nCS 系数：\n"); print(round(cs, 2))
png_open("L10-2_fig4_casedrop.png", 1600, 1200); suppressWarnings(print(plot(cd, statistics = names(cs)))); invisible(dev.off())

## 7. 敏感性分析 ---------------------------------------------------------
off <- row(B) != col(B)
set.seed(SEED); B_1se <- clpn_estimate(X, Y, rule = "lambda.1se")
set.seed(SEED); B_cov <- clpn_estimate(X, Y, covariates = dat[, c("gender", "age")])
set.seed(SEED); B_23  <- clpn_estimate(dat[, vars_t(2)], dat[, vars_t(3)])
sens <- data.frame(analysis = c("lambda.1se", "协变量 gender+age", "T2→T3 复现"),
  r_with_main = round(c(cor(B[off], B_1se[off]), cor(B[off], B_cov[off]), cor(B[off], B_23[off])), 3),
  n_CL_edges = c(sum(B_1se[off] != 0), sum(B_cov[off] != 0), sum(B_23[off] != 0)))
cat("\n敏感性分析（主分析 CL 边数 =", sum(B[off] != 0), "）：\n"); print(sens)
write.csv(sens, out("L10-2_table6_sensitivity.csv"), row.names = FALSE)

## 8. 与真实结构对照（仅模拟数据）---------------------------------------
Bt <- true_B()
cat("\n与真实总体系数的相关（CL 边）=", round(cor(B[off], Bt[off]), 3),
    "；AR 边 =", round(cor(diag(B), diag(Bt)), 3), "\n")
saveRDS(list(B = B, cen = cen, cs = cs, sens = sens, bs = bs), out("L10-2_results.rds"))
log_close()
