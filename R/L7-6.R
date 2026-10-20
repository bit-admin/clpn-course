# =====================================================================
# L7-6.R  测量不变性与样本量规划  (Measurement invariance & sample-size planning)
# 进阶选学课。只用 lavaan（课程固定版本），不需要 semTools。
# 第 1 部分：孤独 4 题在 3 个波次之间的纵向测量不变性（构形 → 度量 → 标量）
# 第 2 部分：抑郁 5 题在男女之间的多组测量不变性（group.equal）
# 第 3 部分：人为制造“第 3 波 lone2 的截距变了”，看标量不变性如何失败、部分不变性如何补救
# 第 4 部分：用模拟做样本量规划：N 多大，才能找回 8 条“目标边”？
# 运行时间：约 1 分钟（大部分在第 4 部分；把 REPS 改成 50 约 2–3 分钟）
# =====================================================================
source("R/_setup.R")
library(lavaan)
library(glmnet)
options(width = 110)                         # 让宽表格在日志里不换行
log_open("L7-6_log.txt")
dat <- read_course_data()

# ---- 小工具：取出要报告的拟合指标 ------------------------------------
fit_row <- function(fit, name) {
  fm <- fitMeasures(fit, c("chisq.scaled", "df", "pvalue.scaled", "cfi.robust", "rmsea.robust"))
  data.frame(model = name, chisq = round(fm[["chisq.scaled"]], 2), df = fm[["df"]],
             p = round(fm[["pvalue.scaled"]], 3), CFI = round(fm[["cfi.robust"]], 3),
             RMSEA = round(fm[["rmsea.robust"]], 3))
}
# 相邻两个模型的比较：ΔCFI ≥ −0.01 且 ΔRMSEA ≤ 0.015 → 认为“更严格的这一级成立”（Chen, 2007）
compare_step <- function(tab) {
  tab$dCFI <- c(NA, round(diff(tab$CFI), 3))
  tab$dRMSEA <- c(NA, round(diff(tab$RMSEA), 3))
  tab$judge <- c("（基准）", ifelse(tab$dCFI[-1] >= -0.01 & tab$dRMSEA[-1] <= 0.015, "成立", "不成立"))
  tab
}

# =====================================================================
# 第 1 部分：纵向测量不变性（孤独 4 题 × 3 波）
# 每一波一个“孤独”因子 F1、F2、F3；同一道题在不同波次的残差允许相关（同一道题自己的特点）
# =====================================================================
lone_model <- function(level = c("configural", "metric", "scalar"), free_int = character(0)) {
  level <- match.arg(level)
  s <- ""
  for (t in 1:3) {
    v <- paste0(lone_items, "_t", t)
    # 载荷：configural 每波自由；metric / scalar 用相同标签 l1–l4 → 跨波次相等
    lab <- if (level == "configural") paste0("l", 1:4, "_", t) else paste0("l", 1:4)
    s <- paste0(s, "F", t, " =~ ", paste0("NA*", v, " + ", lab, "*", v, collapse = " + "), "\n")
    # 截距：scalar 用相同标签 i1–i4 → 跨波次相等；free_int 中的题目不加约束（部分不变性）
    ilab <- if (level == "scalar") paste0("i", 1:4) else paste0("i", 1:4, "_", t)
    ilab[v %in% free_int] <- paste0("i_free_", v[v %in% free_int])
    s <- paste0(s, paste0(v, " ~ ", ilab, "*1", collapse = "\n"), "\n")
  }
  # 识别：第 1 波因子方差 = 1、均值 = 0；载荷相等以后，第 2、3 波方差才可以自由估计；截距相等以后，均值才可以自由估计
  s <- paste0(s, "F1 ~~ 1*F1\nF1 ~ 0*1\n")
  for (t in 2:3) {
    s <- paste0(s, if (level == "configural") paste0("F", t, " ~~ 1*F", t, "\n") else paste0("F", t, " ~~ F", t, "\n"))
    s <- paste0(s, if (level == "scalar") paste0("F", t, " ~ NA*1\n") else paste0("F", t, " ~ 0*1\n"))
  }
  for (it in lone_items)                       # 同一道题跨波次的残差相关
    s <- paste0(s, it, "_t1 ~~ ", it, "_t2 + ", it, "_t3\n", it, "_t2 ~~ ", it, "_t3\n")
  s
}
fit_long <- function(d, level, free_int = character(0))
  cfa(lone_model(level, free_int), data = d, estimator = "MLR", meanstructure = TRUE)

cat("===== 第 1 部分：孤独 4 题的纵向测量不变性（N =", nrow(dat), "，3 波，MLR）=====\n")
f_conf <- fit_long(dat, "configural"); f_metr <- fit_long(dat, "metric"); f_scal <- fit_long(dat, "scalar")
tab1 <- compare_step(rbind(fit_row(f_conf, "构形 configural"), fit_row(f_metr, "度量 metric"), fit_row(f_scal, "标量 scalar")))
print(tab1, row.names = FALSE)
cat("\n嵌套模型的卡方差异检验（Satorra–Bentler 校正）：\n")
lrt1 <- lavTestLRT(f_conf, f_metr, f_scal)
print(round(as.data.frame(lrt1)[, c("Df", "Chisq diff", "Df diff", "Pr(>Chisq)")], 3))
cat("\n标量模型中 3 个波次的孤独因子均值（第 1 波固定为 0）：\n")
pe <- parameterEstimates(f_scal)
print(transform(pe[pe$op == "~1" & pe$lhs %in% c("F1", "F2", "F3"), c("lhs", "est", "se", "pvalue")],
                est = round(est, 3), se = round(se, 3), pvalue = round(pvalue, 3)), row.names = FALSE)

# =====================================================================
# 第 2 部分：多组测量不变性（抑郁 5 题，T1，男 vs 女）
# lavaan 的 group.equal 一行就能加约束：先不约束 → 载荷相等 → 载荷 + 截距相等
# =====================================================================
cat("\n===== 第 2 部分：抑郁 5 题（T1）在男女之间的多组测量不变性 =====\n")
dat$sex <- factor(dat$gender, levels = c(0, 1), labels = c("男", "女"))
cat("各组人数："); print(table(dat$sex))
dep_model <- paste("Dep =~", paste0(dep_items, "_t1", collapse = " + "))
g_conf <- cfa(dep_model, data = dat, group = "sex", estimator = "MLR")
g_metr <- cfa(dep_model, data = dat, group = "sex", estimator = "MLR", group.equal = "loadings")
g_scal <- cfa(dep_model, data = dat, group = "sex", estimator = "MLR", group.equal = c("loadings", "intercepts"))
tab2 <- compare_step(rbind(fit_row(g_conf, "构形 configural"), fit_row(g_metr, "度量 metric"), fit_row(g_scal, "标量 scalar")))
print(tab2, row.names = FALSE)
lrt2 <- lavTestLRT(g_conf, g_metr, g_scal)
print(round(as.data.frame(lrt2)[, c("Df", "Chisq diff", "Df diff", "Pr(>Chisq)")], 3))
pe2 <- parameterEstimates(g_scal)
lm2 <- pe2[pe2$op == "~1" & pe2$lhs == "Dep" & pe2$group == 2, ]
cat(sprintf("\n标量不变性成立后，女性的抑郁因子均值比男性高 %.3f（SE = %.3f，p = %.3f）；男性组均值固定为 0。\n",
            lm2$est, lm2$se, lm2$pvalue))
cat("（模拟数据中，女性每道抑郁题都加了同样的 +0.2：差异在“因子”层面，不是某道题的问题，所以不变性成立。）\n")

# =====================================================================
# 第 3 部分：制造一个“不成立”的例子
# 假设第 3 波问卷把 lone2“被冷落”的措辞改得更容易认同：每个人在这道题上都 +0.5 分，
# 但真实的孤独程度没有变。这是“截距”变了 → 标量不变性应当失败。
# =====================================================================
cat("\n===== 第 3 部分：人为让第 3 波 lone2 的截距 +0.5 =====\n")
bad <- dat; bad$lone2_t3 <- bad$lone2_t3 + 0.5
b_conf <- fit_long(bad, "configural"); b_metr <- fit_long(bad, "metric"); b_scal <- fit_long(bad, "scalar")
b_part <- fit_long(bad, "scalar", free_int = "lone2_t3")
tab3 <- compare_step(rbind(fit_row(b_conf, "构形 configural"), fit_row(b_metr, "度量 metric"), fit_row(b_scal, "标量 scalar")))
print(tab3, row.names = FALSE)
pt <- fit_row(b_part, "部分标量 partial（放开 lone2_t3 截距）")
pt$dCFI <- round(pt$CFI - tab3$CFI[2], 3); pt$dRMSEA <- round(pt$RMSEA - tab3$RMSEA[2], 3)
pt$judge <- ifelse(pt$dCFI >= -0.01 & pt$dRMSEA <= 0.015, "成立", "不成立")
cat("\n与度量模型比较的部分不变性模型：\n"); print(pt, row.names = FALSE)
lrt3 <- lavTestLRT(b_metr, b_scal)
cat("\n度量 vs 标量（被改动的数据）：卡方差异 p =", format.pval(lrt3[2, "Pr(>Chisq)"], digits = 3), "\n")
# 用得分检验（score test，又叫拉格朗日乘子检验）找出“哪一个等值约束最不合适”：
# 它估计“如果单独放开这一条约束，卡方能下降多少”。得分检验在普通 ML 估计下计算，所以先用 ML 重新拟合一次。
b_scal_ml <- cfa(lone_model("scalar"), data = bad, estimator = "ML", meanstructure = TRUE)
mi <- lavTestScore(b_scal_ml)$uni
mi <- mi[order(-mi$X2), ][1:3, ]
pt_tab <- parTable(b_scal_ml)
lab_of <- function(p) { r <- pt_tab[pt_tab$plabel == p, ]; if (r$op == "~1") paste0(r$lhs, " 的截距") else paste0(r$lhs, " ", r$op, " ", r$rhs) }
cat("最不合适的 3 个等值约束（X2 越大越不合适）：\n")
print(data.frame(约束 = paste(sapply(mi$lhs, lab_of), "=", sapply(mi$rhs, lab_of)), X2 = round(mi$X2, 2)), row.names = FALSE)
pb <- parameterEstimates(b_scal); pp <- parameterEstimates(b_part)
mean_F3 <- function(p) round(p$est[p$op == "~1" & p$lhs == "F3"], 3)
cat(sprintf("\n第 3 波孤独因子均值：原始数据 %.3f；改动后、强加标量不变性 %.3f；改动后、部分不变性 %.3f\n",
            mean_F3(pe), mean_F3(pb), mean_F3(pp)))
cat("→ 如果硬把截距设成相等，一道题的措辞变化会被误当成“大家变得更孤独了”。\n")

write.csv(rbind(cbind(part = "1 纵向 longitudinal", tab1), cbind(part = "2 多组 gender", tab2),
                cbind(part = "3 改动后 modified", rbind(tab3, pt))),
          out("L7-6_invariance_fit.csv"), row.names = FALSE)

# =====================================================================
# 第 4 部分：样本量规划（sample-size planning by simulation）
# 思路：先假定一个“真实”网络，按它生成很多份大小为 N 的数据，每份都估计一次 CLPN，
#       数一数“目标边”被找回了多少、本来几乎为 0 的边被误报了多少。
# 这里的真实网络用 true_B_population（课程数据的总体目标）；实际研究中用预实验（pilot）或文献里的估计值。
# =====================================================================
cat("\n===== 第 4 部分：样本量模拟 =====\n")
REPS <- 20                                   # 每个 N 重复 20 次；想要更平滑的曲线可以改成 50
N_GRID <- c(150, 300, 500, 800, 1200)
B <- true_B()
R1 <- cor(dat[, vars_t(1)]); R2 <- cor(dat[, vars_t(2)])
Se <- R2 - t(B) %*% R1 %*% B                 # 残差协方差：让模拟出的 T2 题目方差约等于 1
Se <- (Se + t(Se)) / 2
off <- row(B) != col(B)
target <- off & abs(B) >= 0.08               # 8 条“目标边”（生成模型里设定的交叉滞后与构念内边）
near0  <- off & abs(B) < 0.02                # 几乎为 0 的边：被估成非 0 就算“误报”
cat("目标边", sum(target), "条：", paste(edge_list(B * target)$from, "→", edge_list(B * target)$to, collapse = "，"), "\n")
cat("几乎为 0 的边（|B| < 0.02）", sum(near0), "条\n")
rmvn <- function(n, S) matrix(rnorm(n * ncol(S)), n) %*% chol(S)
# 一次交叉验证同时取 lambda.min 与 lambda.1se 两种规则的结果
est_both <- function(X, Y) {
  X <- scale(X); Y <- scale(Y); p <- ncol(X)
  Bm <- B1 <- matrix(0, p, p)
  for (j in 1:p) {
    cv <- cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    Bm[, j] <- as.numeric(coef(cv, s = "lambda.min"))[-1]
    B1[, j] <- as.numeric(coef(cv, s = "lambda.1se"))[-1]
  }
  list(min = Bm, `1se` = B1)
}
score <- function(Bh) c(power = mean(Bh[target] != 0 & sign(Bh[target]) == sign(B[target])),
                        all8 = all(Bh[target] != 0), fpr = mean(Bh[near0] != 0),
                        r = cor(Bh[off], B[off]))
set.seed(2026)
res <- list()
for (N in N_GRID) for (rep in 1:REPS) {
  X <- rmvn(N, R1); Y <- X %*% B + rmvn(N, Se)
  e <- est_both(X, Y)
  for (rule in names(e)) res[[length(res) + 1]] <- data.frame(N = N, rep = rep, rule = rule, t(score(e[[rule]])))
}
res <- do.call(rbind, res)
pw <- aggregate(cbind(power, all8, fpr, r) ~ N + rule, data = res, FUN = mean)
pw <- pw[order(pw$rule, pw$N), ]
pw[, c("power", "all8", "fpr", "r")] <- round(pw[, c("power", "all8", "fpr", "r")], 2)
names(pw) <- c("N", "rule", "power_target", "p_all8", "fpr_near0", "r_with_true")
cat("每个 N 重复", REPS, "次。power_target = 目标边被找回（非 0 且方向正确）的比例；p_all8 = 8 条全部找回的比例；\n",
    "fpr_near0 = 几乎为 0 的边被误报为非 0 的比例；r_with_true = 估计与真实交叉滞后边的相关。\n")
print(pw, row.names = FALSE)
write.csv(pw, out("L7-6_power.csv"), row.names = FALSE)
cat(sprintf("\n模拟共 %d 次 CLPN 估计（每次 9 个交叉验证 LASSO）。\n", length(N_GRID) * REPS))
png_open("L7-6_power.png", 1800, 1100)
par(mfrow = c(1, 2), mar = c(4.2, 4.2, 3, 1))
for (k in c("power_target", "fpr_near0")) {
  plot(NA, xlim = range(N_GRID), ylim = c(0, 1), xlab = "样本量 N", ylab = "比例",
       main = if (k == "power_target") "目标边的找回率（统计功效）" else "近零边的误报率")
  for (rule in c("min", "1se")) {
    s <- pw[pw$rule == rule, ]
    lines(s$N, s[[k]], type = "b", pch = 16, lwd = 2, col = if (rule == "min") "steelblue" else "darkorange")
  }
  if (k == "power_target") abline(h = 0.8, lty = 2, col = "grey50")
  legend(if (k == "power_target") "bottomright" else "topleft", c("lambda.min", "lambda.1se"), col = c("steelblue", "darkorange"), lwd = 2, pch = 16, bty = "n")
}
invisible(dev.off())
log_close()
