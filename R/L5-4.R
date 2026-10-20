# =====================================================================
# L5-4.R  从预测到因果：用三个小模拟看清交叉滞后“能说什么、不能说什么”
#   (From prediction to causation: confounding, time lags, stable traits)
# 对应课件 lessons/L5-4.html。本脚本不使用课程数据，全部是模拟（simulation），
# 因为只有在模拟里我们才知道“真相”是什么。
#   第 1 部分：未测量混杂 U 制造出“显著的交叉滞后”
#   第 2 部分：测量间隔不同，交叉滞后系数大小不同（Δ·a^(Δ-1)·c）
#   第 3 部分：稳定特质（被试间差异）让 CLPM 出现虚假交叉滞后（Lucas, 2023 的要点）
#   第 4 部分：一个检查“危险因果词”的小函数
# =====================================================================
source("R/_setup.R")
log_open("L5-4_log.txt")

coef_row <- function(fit, term) {                 # 取出某个系数的估计值、SE 和 p 值
  s <- summary(fit)$coefficients
  round(s[term, c("Estimate", "Std. Error", "Pr(>|t|)")], 4)
}

## ---------- 第 1 部分：未测量混杂 ----------
cat("========== 第 1 部分：未测量混杂（unmeasured confounding）==========\n")
set.seed(2026)
N  <- 800
U  <- rnorm(N)                                   # 未测量的共同原因（如慢性病严重程度）
L1 <- 0.6 * U + rnorm(N, 0, 0.8)                 # T1 孤独：受 U 影响
D1 <- 0.6 * U + rnorm(N, 0, 0.8)                 # T1 抑郁：受 U 影响
D2 <- 0.5 * D1 + 0.4 * U + rnorm(N, 0, 0.7)      # T2 抑郁：受 D1 和 U 影响；孤独对它【没有】作用
m_naive <- lm(scale(D2) ~ scale(D1) + scale(L1))             # 像 CLPM 那样只控制 T1 抑郁
m_ctrlU <- lm(scale(D2) ~ scale(D1) + scale(L1) + scale(U))  # 假如我们能测到 U
cat("\n模型 A：D2 ~ D1 + L1（没测 U）\n");  print(summary(m_naive)$coefficients |> round(4))
cat("\n模型 B：D2 ~ D1 + L1 + U（控制 U）\n"); print(summary(m_ctrlU)$coefficients |> round(4))
a <- coef_row(m_naive, "scale(L1)"); b <- coef_row(m_ctrlU, "scale(L1)")
cat(sprintf("\n→ 孤独的“交叉滞后”：没控制 U 时 β = %.3f（p %s）；控制 U 后 β = %.3f（p = %.2f）\n",
            a[1], if (a[3] < .001) "< .001" else paste("=", round(a[3], 3)), b[1], b[3]))

# 延伸练习：U 不再直接影响 D2（0.4*U 改成 0）
set.seed(2026)
U  <- rnorm(N); L1 <- 0.6 * U + rnorm(N, 0, 0.8); D1 <- 0.6 * U + rnorm(N, 0, 0.8)
D2b <- 0.5 * D1 + 0 * U + rnorm(N, 0, 0.7)
c0 <- coef_row(lm(scale(D2b) ~ scale(D1) + scale(L1)), "scale(L1)")
cat(sprintf("延伸：把 0.4*U 改成 0 之后，L1 的系数 β = %.3f（p = %.2f）——U 只通过 D1 起作用，而 D1 已被控制。\n", c0[1], c0[3]))

# 重复 500 次：假阳性有多常见？
set.seed(1)
p_vals <- replicate(500, {
  U <- rnorm(N); L1 <- 0.6 * U + rnorm(N, 0, 0.8); D1 <- 0.6 * U + rnorm(N, 0, 0.8)
  D2 <- 0.5 * D1 + 0.4 * U + rnorm(N, 0, 0.7)
  summary(lm(D2 ~ D1 + L1))$coefficients["L1", 4] })
cat(sprintf("重复模拟 500 次（N = 800）：孤独系数 p < .05 的比例 = %.1f%%（真实效应为 0，理想值应为 5%%）\n\n",
            100 * mean(p_vals < .05)))

## ---------- 第 2 部分：时间间隔 ----------
cat("========== 第 2 部分：测量间隔（time lag）==========\n")
lag_effect <- function(a, c, months) {          # 每月过程 x[m+1] = A x[m]，A = [[a,0],[c,a]]
  A <- matrix(c(a, c, 0, a), 2)                  # 按列填：第 1 列 (a, c)，第 2 列 (0, a)
  sapply(months, function(d) { P <- diag(2); for (k in seq_len(d)) P <- P %*% A; P[2, 1] })
}
months <- 1:24
for (pars in list(c(0.8, 0.15), c(0.9, 0.05))) {
  ce <- lag_effect(pars[1], pars[2], months)
  cat(sprintf("每月自回归 a = %.2f，每月交叉效应 c = %.2f：\n", pars[1], pars[2]))
  print(data.frame(间隔_月 = c(1, 3, 6, 12, 24), 交叉滞后 = round(ce[c(1, 3, 6, 12, 24)], 3),
                   公式 = round(c(1, 3, 6, 12, 24) * pars[1]^(c(1, 3, 6, 12, 24) - 1) * pars[2], 3)),
        row.names = FALSE)
  cat(sprintf("  峰值出现在约 %d 个月（理论值 -1/ln(a) = %.1f）\n\n", which.max(ce), -1 / log(pars[1])))
}
png_open("L5-4_lag.png", width = 1800, height = 1100)
plot(months, lag_effect(0.8, 0.15, months), type = "b", pch = 19, ylim = c(0, 0.5),
     xlab = "测量间隔（月）", ylab = "观测到的交叉滞后（孤独→抑郁）",
     main = "同一个按月发生的过程，用不同间隔去测")
lines(months, lag_effect(0.9, 0.05, months), type = "b", pch = 17, col = "firebrick")
legend("topright", c("a = 0.8, c = 0.15", "a = 0.9, c = 0.05"), pch = c(19, 17),
       col = c("black", "firebrick"), bty = "n")
invisible(dev.off())
cat("图已保存：R/output/L5-4_lag.png\n\n")

## ---------- 第 3 部分：稳定特质 → 虚假交叉滞后 ----------
cat("========== 第 3 部分：稳定特质与 CLPM 的假阳性（Lucas, 2023 的要点）==========\n")
# 每个人有稳定的孤独特质 TL 和抑郁特质 TD（二者相关 0.5）；
# 被试内波动只有自回归（0.3），被试内交叉滞后【真实为 0】。
sim_panel <- function(N, trait_sd = 1) {
  TL <- rnorm(N); TD <- 0.5 * TL + sqrt(1 - 0.5^2) * rnorm(N)
  TL <- trait_sd * TL; TD <- trait_sd * TD
  wl <- rnorm(N); wd <- rnorm(N)
  L <- D <- matrix(NA, N, 3)
  for (t in 1:3) {
    if (t > 1) { wl <- 0.3 * wl + rnorm(N, 0, sqrt(1 - 0.09)); wd <- 0.3 * wd + rnorm(N, 0, sqrt(1 - 0.09)) }
    L[, t] <- TL + wl; D[, t] <- TD + wd
  }
  data.frame(L1 = L[, 1], L2 = L[, 2], D1 = D[, 1], D2 = D[, 2])
}
set.seed(42)
for (n in c(200, 800, 3000)) {
  ps <- replicate(200, { d <- sim_panel(n); summary(lm(D2 ~ D1 + L1, data = d))$coefficients["L1", 4] })
  est <- coef(lm(scale(D2) ~ scale(D1) + scale(L1), data = sim_panel(n)))[3]
  cat(sprintf("N = %4d：CLPM 式回归中“孤独 T1 → 抑郁 T2”p < .05 的比例 = %5.1f%%（一次样本的标准化 β ≈ %.3f）\n",
              n, 100 * mean(ps < .05), est))
}
set.seed(42)
ps0 <- replicate(200, { d <- sim_panel(800, trait_sd = 0); summary(lm(D2 ~ D1 + L1, data = d))$coefficients["L1", 4] })
cat(sprintf("对照：没有稳定特质（trait_sd = 0）时，N = 800，p < .05 的比例 = %.1f%%（接近名义水平 5%%，200 次模拟有抽样波动）\n", 100 * mean(ps0 < .05)))
cat("→ 真实的被试内交叉滞后为 0，但只要有相关的稳定特质，CLPM 就会“发现”交叉滞后，样本越大越“显著”。\n",
    "  控制 T1 抑郁并不能消除特质的影响，因为 T1 抑郁只是特质的一个带噪声的测量。\n\n")

## ---------- 第 4 部分：危险词检查 ----------
cat("========== 第 4 部分：检查结论里的“危险因果词” ==========\n")
danger <- c("导致", "引起", "造成", "决定", "驱动", "根本原因", "就能", "必然", "证明", "cause", "lead to", "drive")
check_causal <- function(txt) {
  hits <- danger[sapply(danger, function(w) grepl(w, txt, fixed = TRUE))]
  if (length(hits)) cat(txt, "\n   含有：", paste(hits, collapse = "、"), "\n", sep = "")
  else cat(txt, "\n", sep = "")
  invisible(hits)
}
check_causal("孤独感导致老年人抑郁。")
check_causal("因此减少孤独就能降低抑郁。")
check_causal("控制基线抑郁后，T1 孤独正向预测 T2 抑郁，结果与孤独可能加重抑郁的假设一致。")
log_close()
