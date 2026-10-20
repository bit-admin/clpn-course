# =====================================================================
# L7-5b.R  Wysocki 等人（2025）的完整 CLPN 流程：LASSO 选边 → lavaan 无惩罚重估 → 跨时间等值检验 → in/out-prediction
#   (Full CLPN pipeline of Wysocki et al., 2025: l1 selection + unpenalized SEM re-fit)
# 对应课件 lessons/L7-5.html（也在 7.2 课中引用）。课程主线（7.2–7.4、8.x、10.x）用的是应用研究中常见的
# “仅 LASSO”简化版（如 Funkhouser et al., 2021）；本脚本演示原论文推荐的完整做法，并与简化版比较。
#   第 1 步 冗余合并：本数据 9 道题措辞互不重复，不合并（goldbricker 检查见 R/L9-2.R）
#   第 2 步 逐节点 LASSO（10 折 CV，lambda.min），T1→T2、T2→T3 各做一次；保守规则：两段都为 0 才固定为 0
#   第 3 步 lavaan 路径模型：保留的路径无惩罚重估；同一波内所有残差相关；FIML（missing = "ml"）；
#           跨时间等值约束（T1→T2 路径 = T2→T3 路径）的嵌套 χ² 检验与 AIC / BIC，选出最终模型，按 p < .01 修剪
#   第 4 步 in-prediction / out-prediction（被解释方差的比例），用最终模型
# 题目先 z 标准化，使系数与 LASSO 简化版、真实总体系数可比。
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(lavaan))
log_open("L7-5b_log.txt")
dat <- read_course_data()
for (v in c(vars_t(1), vars_t(2), vars_t(3))) dat[[v]] <- as.numeric(scale(dat[[v]]))
p <- length(items)

## ---- 第 1 步：冗余合并（本数据不需要）；第 2 步：LASSO 选边（两段）+ 保守规则 ----
set.seed(2026); B12 <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)])
set.seed(2026); B23 <- clpn_estimate(dat[, vars_t(2)], dat[, vars_t(3)])
keep <- (B12 != 0) | (B23 != 0); diag(keep) <- TRUE        # 自回归始终保留
off <- row(keep) != col(keep)
cat("第 2 步 LASSO（lambda.min）：T1→T2 非零交叉滞后边", sum(B12[off] != 0), "条；T2→T3", sum(B23[off] != 0),
    "条；保守规则下进入 SEM 的交叉滞后路径", sum(keep[off]), "条（每段）\n")

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

# 跨时间等值检验：T1→T2 的每条路径 = T2→T3 的同一路径
cat("\n第 3 步 等值约束（T1→T2 的每条路径 = T2→T3 的同一路径）的嵌套 χ² 检验：\n")
av <- anova(fit_equal, fit_free)
cat(sprintf("Δχ²(%d) = %.2f，p = %.3f；AIC：约束 %.1f vs 不约束 %.1f；BIC：约束 %.1f vs 不约束 %.1f\n",
            av$`Df diff`[2], av$`Chisq diff`[2], av$`Pr(>Chisq)`[2], AIC(fit_equal), AIC(fit_free), BIC(fit_equal), BIC(fit_free)))
# 选最终模型：χ² 检验不拒绝等值、且 AIC 与 BIC 都不反对时，用约束模型（两段信息合并，估计更精确）
use_equal <- av$`Pr(>Chisq)`[2] >= .05 && AIC(fit_equal) <= AIC(fit_free) && BIC(fit_equal) <= BIC(fit_free)
fit_final <- if (use_equal) fit_equal else fit_free
cat("最终模型：", if (use_equal) "约束模型（等值成立，后面的修剪与 prediction 都用它）" else "不约束模型（等值不成立）", "\n")
fmf <- fitMeasures(fit_final, c("chisq", "df", "cfi", "tli", "rmsea", "srmr"))
cat(sprintf("最终模型拟合：χ²(%d) = %.2f；CFI = %.3f；TLI = %.3f；RMSEA = %.3f；SRMR = %.3f\n",
            fmf["df"], fmf["chisq"], fmf["cfi"], fmf["tli"], fmf["rmsea"], fmf["srmr"]))

# 取出 T1→T2 的无惩罚系数矩阵（行 = T1 预测变量，列 = T2 结果）与 p 值
coef12 <- function(fit) {
  pe <- parameterEstimates(fit)
  reg <- pe[pe$op == "~" & grepl("_t2$", pe$lhs), ]
  S <- P <- matrix(0, p, p, dimnames = list(items, items)); P[] <- 1
  for (r in seq_len(nrow(reg))) { k <- sub("_t1$", "", reg$rhs[r]); j <- sub("_t2$", "", reg$lhs[r])
    S[k, j] <- reg$est[r]; P[k, j] <- reg$pvalue[r] }
  list(S = S, P = P)
}
cf <- coef12(fit_final); S12 <- cf$S; P12 <- cf$P
P12_free <- coef12(fit_free)$P
sig <- P12 < .01
Bt <- true_B(); te <- abs(Bt) >= 0.05                      # 总体目标值（data/true_B_population.csv）中 |β| ≥ 0.05 的边，与 R/L7-2.R 相同
perf <- function(est_nonzero) c(找回 = sum(est_nonzero[off] & te[off]), 假阳性 = sum(est_nonzero[off] & !te[off]),
                               漏掉 = sum(!est_nonzero[off] & te[off]), 估计CL边 = sum(est_nonzero[off]))
cmp <- rbind(`仅 LASSO（lambda.min）` = perf(B12 != 0),
             `LASSO + SEM 重估，最终模型（p < .01）` = perf(sig),
             `LASSO + SEM 重估，最终模型（p < .05）` = perf(P12 < .05),
             `对照：不约束模型（p < .01）` = perf(P12_free < .01))
cat("\nT1→T2 交叉滞后边与总体目标值的比较（总体目标值中的交叉滞后边", sum(te[off]), "条）：\n"); print(cmp)
cat("SEM 重估后的边权与总体目标值的相关（被保留的路径）=", round(cor(S12[off & keep], Bt[off & keep]), 3),
    "；LASSO 边权与总体目标值的相关（同一批路径）=", round(cor(B12[off & keep], Bt[off & keep]), 3), "\n")
cat("举例：lone3 → dep1 总体目标值", round(Bt["lone3", "dep1"], 3), "；LASSO", round(B12["lone3", "dep1"], 3),
    "；SEM 重估", round(S12["lone3", "dep1"], 3), sprintf("（p = %.3g）", P12["lone3", "dep1"]), "\n")

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
write.csv(round(pred, 4), out("L7-5b_in_out_prediction.csv"))

## ---- 对照被试内真值（data/true_B_within.csv）----
# 总体目标值里有 28 条只由稳定特质造成的边；SEM 重估和 p 值修剪去不掉它们，因为它们在总体中确实存在。
Bw <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))[items, items]
tw <- Bw != 0
perf_w <- function(est_nonzero) c(找回 = sum(est_nonzero[off] & tw[off]), 假阳性 = sum(est_nonzero[off] & !tw[off]),
                                 漏掉 = sum(!est_nonzero[off] & tw[off]), 估计CL边 = sum(est_nonzero[off]))
cmp_w <- rbind(`仅 LASSO（lambda.min）` = perf_w(B12 != 0),
               `LASSO + SEM 重估，最终模型（p < .01）` = perf_w(sig),
               `LASSO + SEM 重估，最终模型（p < .05）` = perf_w(P12 < .05))
cat("\nT1→T2 交叉滞后边与被试内真值的比较（被试内真值中的交叉滞后边", sum(tw[off]), "条）：\n"); print(cmp_w)
cat("被保留路径上 SEM 重估边权与被试内真值的相关 =", round(cor(S12[off & keep], Bw[off & keep]), 3), "\n")
log_close()
