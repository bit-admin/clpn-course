# =====================================================================
# L10-2b.R  毕业项目②补充：必做的敏感性分析 —— Wysocki 等人（2025）的完整 CLPN 流程
#   (Required sensitivity analysis: full CLPN pipeline of Wysocki et al., 2025)
# 主分析（R/L10-2.R）是“仅 LASSO”的简化版：LASSO 选出、并已收缩的系数直接当作边权。
# 方法论文推荐的完整流程多一步：用 LASSO 只决定哪些路径固定为 0，再在 SEM 中无惩罚地重估其余路径。
# 本脚本在毕业项目数据（R/output/L10-1_clean_data.csv）上做完整流程，并逐条对照主分析的边：
#   第 1 步 冗余合并：本数据 9 道题措辞互不重复，不合并（goldbricker 检查见 R/L9-2.R）
#   第 2 步 逐节点 LASSO（10 折 CV，规则与主分析相同），T1→T2、T2→T3 各做一次；保守规则：两段都为 0 才固定为 0
#   第 3 步 lavaan 路径模型：保留的路径无惩罚重估；同一波内所有残差相关；FIML（missing = "ml"）；
#           跨时间等值约束（T1→T2 路径 = T2→T3 路径）的嵌套 χ² 检验与 AIC / BIC，选出最终模型，按 p < .01 修剪
#   第 4 步 in-/out-prediction（被解释方差的比例），用最终模型
#   第 5 步 与主分析对照：主分析最强的边有几条在完整流程中保留？两个方向的边权和是否仍然一个大、一个小？
# 写法与 R/L7-5b.R 相同（7.5 课），只是数据换成毕业项目的清理后数据，并加上第 5 步。
# 依赖：R/L10-1.R（清理后数据）和 R/L10-2.R（主分析结果，用于第 5 步的对照）。
# 运行时间：两次 lavaan 拟合加 18 次交叉验证 LASSO，通常 1 分钟以内。
# 输出：R/output/L10-2b_log.txt、L10-2b_edges.csv、L10-2b_summary.csv、L10-2b_in_out_prediction.csv、L10-2b_results.rds
# =====================================================================
source("R/_setup.R")
need_output("L10-1_clean_data.csv", "R/L10-1.R", chain = "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-2b.R → R/L10-3.R")   # 前置结果检查
need_output("L10-2_results.rds", "R/L10-2.R", chain = "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-2b.R → R/L10-3.R")
suppressPackageStartupMessages(library(lavaan))
log_open("L10-2b_log.txt")
SEED <- 2026; RULE <- "lambda.min"; ALPHA <- .01      # 与分析计划、R/L10-2.R 保持一致；ALPHA = 修剪用的显著性水平
dat <- read.csv(out("L10-1_clean_data.csv"))          # 来自 L10-1.R
for (v in c(vars_t(1), vars_t(2), vars_t(3))) dat[[v]] <- as.numeric(scale(dat[[v]]))   # z 标准化，系数与主分析可比
p <- length(items)
res <- readRDS(out("L10-2_results.rds"))              # 主分析：res$B（LASSO 系数矩阵）、res$bs（bootstrap 边表）
B_main <- res$B
off <- row(B_main) != col(B_main)

## ---- 第 2 步：LASSO 选边（两段）+ 保守规则 ----
set.seed(SEED); B12 <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], rule = RULE)
set.seed(SEED); B23 <- clpn_estimate(dat[, vars_t(2)], dat[, vars_t(3)], rule = RULE)
cat("核对：本脚本 T1→T2 的 LASSO 与 L10-2.R 主分析的系数矩阵相同吗？",
    isTRUE(all.equal(B12, B_main, check.attributes = FALSE)), "\n")
keep <- (B12 != 0) | (B23 != 0); diag(keep) <- TRUE        # 自回归始终保留
cat("第 2 步 LASSO（", RULE, "）：T1→T2 非零交叉滞后边 ", sum(B12[off] != 0), " 条；T2→T3 ", sum(B23[off] != 0),
    " 条；保守规则下进入 SEM 的交叉滞后路径 ", sum(keep[off]), " 条（每段，共 ", sum(off), " 个位置）\n", sep = "")

## ---- 第 3 步：lavaan 无惩罚重估 ----
build <- function(equal = FALSE) {
  lines <- c()
  for (t in 2:3) for (j in seq_len(p)) {
    preds <- which(keep[, j])
    lab <- if (equal) paste0("b", preds, "_", j, "*") else ""
    lines <- c(lines, paste0(items[j], "_t", t, " ~ ", paste0(lab, items[preds], "_t", t - 1, collapse = " + ")))
  }
  for (t in 2:3) { cmb <- combn(items, 2)                   # 同一波内所有残差两两相关
    lines <- c(lines, paste0(cmb[1, ], "_t", t, " ~~ ", cmb[2, ], "_t", t)) }
  paste(lines, collapse = "\n")
}
fit_free  <- sem(build(FALSE), data = dat, missing = "ml", fixed.x = FALSE)
fit_equal <- sem(build(TRUE),  data = dat, missing = "ml", fixed.x = FALSE)
fm <- fitMeasures(fit_free, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
cat(sprintf("\n第 3 步 SEM（不约束）：χ²(%d) = %.2f，p %s；CFI = %.3f；TLI = %.3f；RMSEA = %.3f [%.3f, %.3f]；SRMR = %.3f\n",
            fm["df"], fm["chisq"], ifelse(fm["pvalue"] < .001, "< .001", sprintf("= %.3f", fm["pvalue"])),
            fm["cfi"], fm["tli"], fm["rmsea"], fm["rmsea.ci.lower"], fm["rmsea.ci.upper"], fm["srmr"]))
cat("\n第 3 步 等值约束（T1→T2 的每条路径 = T2→T3 的同一路径）的嵌套 χ² 检验：\n")
av <- anova(fit_equal, fit_free)
ic <- c(AIC_equal = AIC(fit_equal), AIC_free = AIC(fit_free), BIC_equal = BIC(fit_equal), BIC_free = BIC(fit_free))
cat(sprintf("Δχ²(%d) = %.2f，p = %.3f；AIC：约束 %.1f vs 不约束 %.1f；BIC：约束 %.1f vs 不约束 %.1f\n",
            av$`Df diff`[2], av$`Chisq diff`[2], av$`Pr(>Chisq)`[2], ic["AIC_equal"], ic["AIC_free"], ic["BIC_equal"], ic["BIC_free"]))
# 选最终模型：χ² 检验不拒绝等值、且 AIC 与 BIC 都不反对时，用约束模型（两段信息合并，估计更精确）
use_equal <- av$`Pr(>Chisq)`[2] >= .05 && ic["AIC_equal"] <= ic["AIC_free"] && ic["BIC_equal"] <= ic["BIC_free"]
fit_final <- if (use_equal) fit_equal else fit_free
cat("最终模型：", if (use_equal) "约束模型（等值成立，后面的修剪与 prediction 都用它）" else "不约束模型（等值不成立；下面报告 T1→T2 段）", "\n")
fmf <- fitMeasures(fit_final, c("chisq", "df", "cfi", "tli", "rmsea", "srmr"))
cat(sprintf("最终模型拟合：χ²(%d) = %.2f；CFI = %.3f；TLI = %.3f；RMSEA = %.3f；SRMR = %.3f\n",
            fmf["df"], fmf["chisq"], fmf["cfi"], fmf["tli"], fmf["rmsea"], fmf["srmr"]))

# 取出 T1→T2 的无惩罚系数、标准误和 p 值（行 = T1 预测变量，列 = T2 结果）；未进入 SEM 的路径：系数 0，p 记为 NA
coef12 <- function(fit) {
  pe <- parameterEstimates(fit)
  reg <- pe[pe$op == "~" & grepl("_t2$", pe$lhs), ]
  S <- SE <- matrix(0, p, p, dimnames = list(items, items)); P <- matrix(NA_real_, p, p, dimnames = list(items, items))
  for (r in seq_len(nrow(reg))) { k <- sub("_t1$", "", reg$rhs[r]); j <- sub("_t2$", "", reg$lhs[r])
    S[k, j] <- reg$est[r]; SE[k, j] <- reg$se[r]; P[k, j] <- reg$pvalue[r] }
  list(S = S, SE = SE, P = P)
}
cf <- coef12(fit_final); S12 <- cf$S; P12 <- cf$P
sig <- !is.na(P12) & P12 < ALPHA                           # 修剪后保留的路径
S_pruned <- S12 * sig                                      # 修剪后的系数矩阵（不显著的置 0）
lone <- 1:4; dep <- 5:9
n_sig <- c(全部 = sum(sig[off]), 孤独到抑郁 = sum(sig[lone, dep]), 抑郁到孤独 = sum(sig[dep, lone]),
           构念内 = sum(sig[off]) - sum(sig[lone, dep]) - sum(sig[dep, lone]))
cat(sprintf("\n按 p < %.2f 修剪后保留的交叉滞后边：%d 条（孤独→抑郁 %d，抑郁→孤独 %d，构念内 %d）；p < .05 时为 %d 条\n",
            ALPHA, n_sig[1], n_sig[2], n_sig[3], n_sig[4], sum(!is.na(P12[off]) & P12[off] < .05)))

## ---- 第 4 步：in-prediction 与 out-prediction（T1→T2，最终模型）----
Sig <- lavInspect(fit_final, "cov.ov")                     # 模型隐含协方差
S1 <- Sig[vars_t(1), vars_t(1)]; v2 <- diag(Sig)[vars_t(2)]
cons <- ifelse(grepl("^lone", items), "孤独", "抑郁")
inpred <- function(j, use) { b <- S12[, j] * use; as.numeric(t(b) %*% S1 %*% b) / unname(v2[j]) }
pred <- t(sapply(seq_len(p), function(j) {
  others <- seq_len(p) != j; xc <- cons != cons[j]
  outk <- sapply(seq_len(p), function(k) S12[j, k]^2 * S1[j, j] / unname(v2[k]))
  c(inPred = inpred(j, rep(1, p)), inPred_CL = inpred(j, others), inPred_跨构念 = inpred(j, xc),
    outPred = mean(outk), outPred_CL = mean(outk[others]), outPred_跨构念 = mean(outk[xc]))
}))
rownames(pred) <- items
cat("\n第 4 步 in-/out-prediction（被解释方差比例；CL = 不含自回归）：\n"); print(round(pred, 3))
cat("跨构念 out-prediction 最高：", items[which.max(pred[, "outPred_跨构念"])],
    "；跨构念 in-prediction 最高：", items[which.max(pred[, "inPred_跨构念"])], "\n")
write.csv(round(pred, 4), out("L10-2b_in_out_prediction.csv"))

## ---- 第 5 步：与主分析（仅 LASSO）逐条对照 ----
bs <- res$bs                                               # 主分析的 bootstrap 边表（node1 → node2）
e <- data.frame(from = rep(items, times = p), to = rep(items, each = p), stringsAsFactors = FALSE)
e <- e[e$from != e$to, ]
ix <- cbind(e$from, e$to)
e$from_zh <- item_zh[e$from]; e$to_zh <- item_zh[e$to]
e$lasso <- B_main[ix]; e$lasso_t23 <- B23[ix]                 # 主分析（T1→T2）与 T2→T3 段的 LASSO 系数
bkey <- paste(bs$node1, bs$node2)
e$boot_q2.5 <- bs$q2.5[match(paste(e$from, e$to), bkey)]; e$boot_q97.5 <- bs$q97.5[match(paste(e$from, e$to), bkey)]
e$in_sem <- keep[ix]; e$sem_est <- S12[ix]; e$sem_se <- cf$SE[ix]; e$sem_p <- P12[ix]
e$kept_p01 <- sig[ix]
cff <- coef12(fit_free); e$free_est <- cff$S[ix]; e$free_p <- cff$P[ix]   # 对照：不约束模型的 T1→T2 段
Bt <- true_B(); Bw <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))   # 仅模拟数据才有的两种真值（7.1、7.5 课）
e$true_pop <- Bt[ix]; e$true_within <- Bw[ix]
e <- e[order(-abs(e$lasso), -abs(e$sem_est)), ]
rownames(e) <- NULL
write.csv(e, out("L10-2b_edges.csv"), row.names = FALSE, fileEncoding = "UTF-8")

TOP <- 10
top <- head(e[e$lasso != 0, ], TOP)
excl0 <- !is.na(e$boot_q2.5) & (e$boot_q2.5 > 0 | e$boot_q97.5 < 0)   # 主分析 bootstrap 区间不含 0
cat("\n第 5 步 主分析最强的", TOP, "条交叉滞后边在完整流程中的结果：\n")
tab <- data.frame(边 = paste0(top$from, " → ", top$to), 题目 = paste0(top$from_zh, " → ", top$to_zh),
                  LASSO = round(top$lasso, 3), bootstrap区间 = sprintf("[%.3f, %.3f]", top$boot_q2.5, top$boot_q97.5),
                  SEM重估 = round(top$sem_est, 3), p = signif(top$sem_p, 2), 保留 = ifelse(top$kept_p01, "是", "否"))
print(tab, row.names = FALSE)
cat(sprintf("最强 %d 条中保留 %d 条；最强 3 条中保留 %d 条\n", TOP, sum(top$kept_p01), sum(head(top$kept_p01, 3))))
if (use_equal && any(!top$kept_p01)) {                     # 约束模型的系数是两段的共同值：看没保留的边在两段中各是多少
  dr <- top[!top$kept_p01, ]
  cat("没有保留的边在两段中的情况（约束模型的系数是两段的共同值）：\n")
  print(data.frame(边 = paste0(dr$from, " → ", dr$to), LASSO_T1T2 = round(dr$lasso, 3), LASSO_T2T3 = round(dr$lasso_t23, 3),
                   不约束模型_T1T2 = round(dr$free_est, 3), 不约束_p = signif(dr$free_p, 2), 约束模型 = round(dr$sem_est, 3)),
        row.names = FALSE)
}
both <- sum(e$lasso != 0 & e$kept_p01); lasso_only <- sum(e$lasso != 0 & !e$kept_p01); sem_only <- sum(e$lasso == 0 & e$kept_p01)
cat(sprintf("主分析 %d 条非零边中，完整流程保留 %d 条、未保留 %d 条；完整流程保留、主分析为 0 的有 %d 条\n",
            sum(e$lasso != 0), both, lasso_only, sem_only))
cat(sprintf("主分析 bootstrap 区间不含 0 的 %d 条边中，完整流程保留 %d 条\n", sum(excl0), sum(excl0 & e$kept_p01)))
r_ls <- cor(B_main[off], S12[off])
cat("主分析 LASSO 系数与 SEM 重估系数的相关（全部", sum(off), "个交叉滞后位置；未进入 SEM 的记为 0）=", round(r_ls, 3), "\n")
sums <- c(ld_lasso = sum(B_main[lone, dep]), dl_lasso = sum(B_main[dep, lone]),
          ld_full = sum(S_pruned[lone, dep]), dl_full = sum(S_pruned[dep, lone]))
cat(sprintf("构念层面的边权和：孤独→抑郁 主分析 %.2f，完整流程（修剪后）%.2f；抑郁→孤独 主分析 %.2f，完整流程 %.2f\n",
            sums["ld_lasso"], sums["ld_full"], sums["dl_lasso"], sums["dl_full"]))

# 与真实结构对照（仅模拟数据）：两种真值（7.1、7.5 课）。总体目标值的“真实边”定义与 R/L7-2.R、R/L7-5b.R 相同：|β| ≥ 0.05
te <- abs(Bt) >= 0.05
perf2 <- function(nz, tr) c(找回 = sum(nz[off] & tr[off]), 假阳性 = sum(nz[off] & !tr[off]), 漏掉 = sum(!nz[off] & tr[off]), 估计边数 = sum(nz[off]))
perf <- function(nz) perf2(nz, te)
cmp <- rbind(`主分析：仅 LASSO` = perf(B_main != 0), `完整流程：SEM 重估 + p < .01 修剪` = perf(sig))
cat("\n与总体目标值的比较（data/true_B_population.csv 中 |β| ≥ 0.05 的交叉滞后边", sum(te[off]), "条）：\n"); print(cmp)
tw <- Bw[items, items] != 0                                # 被试内真值：生成数据时真正用到的滞后系数
cmp_w <- rbind(`主分析：仅 LASSO` = perf2(B_main != 0, tw), `完整流程：SEM 重估 + p < .01 修剪` = perf2(sig, tw))
cat("与被试内真值的比较（data/true_B_within.csv 中非 0 的交叉滞后边", sum(tw[off]), "条；其余的“假阳性”多数是稳定特质造成的边）：\n"); print(cmp_w)

summ <- c(n_lasso_main = sum(B_main[off] != 0), n_cl12 = sum(B12[off] != 0), n_cl23 = sum(B23[off] != 0), n_keep = sum(keep[off]),
          free_chisq = unname(fm["chisq"]), free_df = unname(fm["df"]), free_p = unname(fm["pvalue"]),
          free_cfi = unname(fm["cfi"]), free_tli = unname(fm["tli"]), free_rmsea = unname(fm["rmsea"]),
          free_rmsea_lo = unname(fm["rmsea.ci.lower"]), free_rmsea_hi = unname(fm["rmsea.ci.upper"]), free_srmr = unname(fm["srmr"]),
          eq_dchisq = av$`Chisq diff`[2], eq_ddf = av$`Df diff`[2], eq_p = av$`Pr(>Chisq)`[2],
          aic_equal = unname(ic["AIC_equal"]), aic_free = unname(ic["AIC_free"]), bic_equal = unname(ic["BIC_equal"]), bic_free = unname(ic["BIC_free"]),
          use_equal = as.numeric(use_equal),
          fin_chisq = unname(fmf["chisq"]), fin_df = unname(fmf["df"]), fin_cfi = unname(fmf["cfi"]), fin_tli = unname(fmf["tli"]),
          fin_rmsea = unname(fmf["rmsea"]), fin_srmr = unname(fmf["srmr"]),
          n_sig01 = n_sig[[1]], n_sig01_ld = n_sig[[2]], n_sig01_dl = n_sig[[3]], n_sig01_within = n_sig[[4]],
          n_sig05 = sum(!is.na(P12[off]) & P12[off] < .05),
          n_both = both, n_lasso_only = lasso_only, n_sem_only = sem_only,
          top_n = TOP, top_kept = sum(top$kept_p01), top3_kept = sum(head(top$kept_p01, 3)),
          n_boot_excl0 = sum(excl0), n_boot_excl0_kept = sum(excl0 & e$kept_p01),
          r_lasso_sem = r_ls, sums,
          n_true = sum(te[off]), found_lasso = cmp[1, 1], fp_lasso = cmp[1, 2], found_full = cmp[2, 1], fp_full = cmp[2, 2],
          n_true_w = sum(tw[off]), found_lasso_w = cmp_w[1, 1], fp_lasso_w = cmp_w[1, 2], found_full_w = cmp_w[2, 1], fp_full_w = cmp_w[2, 2])
write.csv(data.frame(statistic = names(summ), value = unname(summ)), out("L10-2b_summary.csv"), row.names = FALSE)
saveRDS(list(edges = e, summary = summ, S12 = S12, P12 = P12, keep = keep, use_equal = use_equal, pred = pred),
        out("L10-2b_results.rds"))
log_close()
