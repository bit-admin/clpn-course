# 练习答案 L7-6：测量不变性
# 练习 2：课程数据里抑郁 5 题在 3 个波次之间是否纵向不变？
# 练习 3：真实数据（体育教练心理健康追踪，CC0，data/coaches_mhc_raw.csv）中，“社会幸福感”5 题在 3 个波次之间是否不变？
# 只用 lavaan（课程固定版本）；运行时间约 10 秒
source("R/_setup.R")
library(lavaan)
options(width = 110)
log_open("sol_L7-6_log.txt")

# 通用的纵向不变性模型：nm(t, k) 给出第 t 波第 k 道题的变量名
long_model <- function(nm, K, level = c("configural", "metric", "scalar"), free_int = character(0)) {
  level <- match.arg(level); s <- ""
  for (t in 1:3) {
    v <- sapply(K, function(k) nm(t, k))
    lab  <- if (level == "configural") paste0("l", K, "_", t) else paste0("l", K)
    ilab <- if (level == "scalar") paste0("i", K) else paste0("i", K, "_", t)
    ilab[v %in% free_int] <- paste0("free_", v[v %in% free_int])
    s <- paste0(s, "F", t, " =~ ", paste0("NA*", v, " + ", lab, "*", v, collapse = " + "), "\n",
                paste0(v, " ~ ", ilab, "*1", collapse = "\n"), "\n")
  }
  s <- paste0(s, "F1 ~~ 1*F1\nF1 ~ 0*1\n")
  for (t in 2:3) s <- paste0(s, if (level == "configural") paste0("F", t, " ~~ 1*F", t) else paste0("F", t, " ~~ F", t), "\n",
                             if (level == "scalar") paste0("F", t, " ~ NA*1") else paste0("F", t, " ~ 0*1"), "\n")
  for (k in K) s <- paste0(s, nm(1, k), " ~~ ", nm(2, k), " + ", nm(3, k), "\n", nm(2, k), " ~~ ", nm(3, k), "\n")
  s
}
fit_row <- function(fit, name) {
  fm <- fitMeasures(fit, c("chisq.scaled", "df", "cfi.robust", "rmsea.robust"))
  data.frame(model = name, chisq = round(fm[[1]], 2), df = fm[[2]], CFI = round(fm[[3]], 3), RMSEA = round(fm[[4]], 3))
}
three_steps <- function(d, nm, K, ...) {
  f <- lapply(c("configural", "metric", "scalar"), function(lv) cfa(long_model(nm, K, lv), data = d, estimator = "MLR", meanstructure = TRUE, ...))
  tab <- rbind(fit_row(f[[1]], "构形 configural"), fit_row(f[[2]], "度量 metric"), fit_row(f[[3]], "标量 scalar"))
  tab$dCFI <- c(NA, round(diff(tab$CFI), 3)); tab$dRMSEA <- c(NA, round(diff(tab$RMSEA), 3))
  print(tab, row.names = FALSE)
  lrt <- lavTestLRT(f[[1]], f[[2]], f[[3]])
  cat("卡方差异检验 p 值：度量 vs 构形 =", round(lrt[2, "Pr(>Chisq)"], 3), "；标量 vs 度量 =", round(lrt[3, "Pr(>Chisq)"], 3), "\n")
  invisible(f)
}

# ---------------- 练习 2：课程数据，抑郁 5 题 × 3 波 ----------------
cat("===== 练习 2：课程数据，抑郁 5 题的纵向测量不变性（N = 800）=====\n")
dat <- read_course_data()
f2 <- three_steps(dat, function(t, k) paste0("dep", k, "_t", t), 1:5)
pe <- parameterEstimates(f2[[3]])
cat("标量模型中第 2、3 波的抑郁因子均值（第 1 波 = 0）：",
    paste(round(pe$est[pe$op == "~1" & pe$lhs %in% c("F2", "F3")], 3), collapse = "，"), "\n")

# ---------------- 练习 3：教练数据，社会幸福感 5 题（w4–w8）× 3 波 ----------------
cat("\n===== 练习 3：体育教练心理健康追踪数据（Ackeret et al., 2023，CC0）=====\n")
coach <- read.csv2("data/coaches_mhc_raw.csv", dec = ".")   # 分号分隔、小数点是“.”
cat("行数", nrow(coach), "，列数", ncol(coach), "\n")
cat("每一波 14 道题全部作答的人数：",
    paste0("T", 1:3, " = ", sapply(1:3, function(t) sum(complete.cases(coach[, paste0("t", t, "w", 1:14)]))), collapse = "，"), "\n")
cat("三波社会幸福感 5 题都完整的人数：", sum(complete.cases(coach[, paste0("t", rep(1:3, each = 5), "w", 4:8)])), "\n")
# 数据检查：文件自带的分量表均值列（t1emowb、t2socwb 等）和用题目重新计算的均值对不上（见数据字典）
chk <- t(sapply(1:3, function(t) {
  it <- function(k) coach[, paste0("t", t, "w", k)]
  r <- function(a, b) round(cor(a, b, use = "complete.obs"), 2)
  c(emowb_vs_w1to3 = r(rowMeans(it(1:3)), coach[[paste0("t", t, "emowb")]]),
    socwb_vs_w4to8 = r(rowMeans(it(4:8)), coach[[paste0("t", t, "socwb")]]),
    psywb_vs_w9to14 = r(rowMeans(it(9:14)), coach[[paste0("t", t, "psywb")]]),
    WBcont_vs_sum = r(rowSums(it(1:14)), coach[[paste0("t", t, "_WB_cont")]]))
}))
rownames(chk) <- paste0("T", 1:3)
cat("自带的汇总列与按题目重新计算的值之间的相关（应接近 1）：\n"); print(chk)
tot <- sapply(1:3, function(t) rowSums(coach[, paste0("t", t, "w", 1:14)]))
same <- sapply(1:3, function(t) { w <- coach[[paste0("t", t, "_WB_cont")]]; k <- !is.na(tot[, t]) & !is.na(w)
  sprintf("T%d %d / %d 人", t, sum(tot[k, t] - 14 == w[k]), sum(k)) })
cat("*_WB_cont 恰好等于“14 题之和 − 14”（即按 0–5 计分的总分）的人数：", paste(same, collapse = "，"), "\n")
cat("14 题总分的跨波相关（同一个人前后应当相似）：T1–T2 =", round(cor(tot[, 1], tot[, 2], use = "complete.obs"), 2),
    "，T2–T3 =", round(cor(tot[, 2], tot[, 3], use = "complete.obs"), 2), "，T1–T3 =", round(cor(tot[, 1], tot[, 3], use = "complete.obs"), 2), "\n")
cat("→ 题目列本身前后一致（跨波相关高；T2、T3 的 *_WB_cont 就是按 0–5 计分的 14 题总分），但三个分量表均值列和总均值列对不上（只有 T1 的情绪幸福感大致对得上），T1 的 *_WB_cont 也只有一部分人对得上。\n  所以只用题目列（t1w1 … t3w14）自己计算，不用自带的分量表列。\n\n")
nm_c <- function(t, k) paste0("t", t, "w", k)
cat("缺失值用 FIML 处理（missing = \"ml\"），所以 422 人全部进入模型：\n")
f3 <- three_steps(coach, nm_c, 4:8, missing = "ml")
cat("\n标量这一步：卡方检验显著，但 ΔCFI 没有超过 −0.01 → 看看是哪一个截距最不合适（得分检验，ML 重新拟合）：\n")
f3ml <- cfa(long_model(nm_c, 4:8, "scalar"), data = coach, estimator = "ML", missing = "ml", meanstructure = TRUE)
sc <- lavTestScore(f3ml)$uni; sc <- sc[order(-sc$X2), ][1:3, ]
ptab <- parTable(f3ml)
lab_of <- function(p) { r <- ptab[ptab$plabel == p, ]; if (r$op == "~1") paste0(r$lhs, " 的截距") else paste0(r$lhs, " ", r$op, " ", r$rhs) }
print(data.frame(约束 = paste(sapply(sc$lhs, lab_of), "=", sapply(sc$rhs, lab_of)), X2 = round(sc$X2, 2)), row.names = FALSE)
worst <- sub(" 的截距", "", lab_of(sc$rhs[1]))
fp <- cfa(long_model(nm_c, 4:8, "scalar", free_int = worst), data = coach, estimator = "MLR", missing = "ml", meanstructure = TRUE)
pr <- fit_row(fp, paste0("部分标量（放开 ", worst, " 的截距）"))
pr$dCFI <- round(pr$CFI - fitMeasures(f3[[2]], "cfi.robust"), 3)
cat("\n与度量模型比较：\n"); print(pr, row.names = FALSE)
m_full <- parameterEstimates(f3[[3]]); m_part <- parameterEstimates(fp)
gm <- function(p) paste(sprintf("%.3f（SE %.3f）", p$est[p$op == "~1" & p$lhs %in% c("F2", "F3")], p$se[p$op == "~1" & p$lhs %in% c("F2", "F3")]), collapse = "，")
cat("第 2、3 波社会幸福感因子均值（第 1 波 = 0）：完全标量", gm(m_full), "；部分标量", gm(m_part), "\n")
cat("（数据说明里波次间隔有两种说法：3 / 6 个月或 6 / 12 个月，所以这里只比较“是否测的是同一个东西”，不解读变化的速度。）\n")
log_close()
