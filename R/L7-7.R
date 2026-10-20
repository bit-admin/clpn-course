# =====================================================================
# L7-7.R  组间比较：两组的 CLPN 一样吗？（Group comparison with a permutation test）
# 进阶选学课。手写置换检验（permutation test），不需要新的 R 包。
# 第 1 部分：课程数据，男 vs 女（生成数据时两性的网络完全相同 → 演示“没有差异”时的结果）
# 第 2 部分：模拟两组各 600 人，第 2 组 lone3 → dep1 的系数 +0.20（演示“有差异”时能不能发现）
# 第 3 部分：同样的差异，每组只有 300 人（演示样本量不够时会怎样）
# 为了速度和可重复性，每次估计用 EBIC 选 λ（clpn_estimate(rule = "ebic")，不做交叉验证）。
# 运行时间：单核约 2–4 分钟（3 部分 × 1000 次置换；把 NPERM 改小可以更快，但 p 值会更粗）
# =====================================================================
source("R/_setup.R")
library(glmnet)
options(width = 110)
log_open("L7-7_log.txt")
dat <- read_course_data()
NPERM <- 1000                                # 每部分置换次数

# ---- 小工具 ----------------------------------------------------------
est <- function(d) clpn_estimate(d[, vars_t(1)], d[, vars_t(2)], rule = "ebic")
off <- matrix(TRUE, length(items), length(items)); diag(off) <- FALSE   # 交叉滞后边的位置
# 三个检验统计量（van Borkulo et al., 2023 的思路，用在 CLPN 的交叉滞后边上）：
#   M  = 两组之间“差得最多的那一条边”的差值绝对值（network structure invariance）
#   S  = 两组交叉滞后边绝对值之和（整体连接强度）的差值绝对值（global strength invariance）
#   D  = 每一条边的差值（edge invariance），72 条
stats <- function(B1, B2) {
  D <- B1 - B2
  list(M = max(abs(D[off])), S = abs(sum(abs(B1[off])) - sum(abs(B2[off]))), D = D,
       S1 = sum(abs(B1[off])), S2 = sum(abs(B2[off])))
}
perm_test <- function(d, grp, nperm = NPERM) {
  lev <- sort(unique(grp))
  B1 <- est(d[grp == lev[1], ]); B2 <- est(d[grp == lev[2], ])
  obs <- stats(B1, B2)
  nullM <- nullS <- numeric(nperm); exceedD <- matrix(0, nrow(B1), ncol(B1))
  for (b in seq_len(nperm)) {
    g <- sample(grp)                           # 洗牌：打乱组别标签，每组人数不变
    s <- stats(est(d[g == lev[1], ]), est(d[g == lev[2], ]))
    nullM[b] <- s$M; nullS[b] <- s$S
    exceedD <- exceedD + (abs(s$D) >= abs(obs$D) - 1e-12)
  }
  pD <- (exceedD + 1) / (nperm + 1)
  list(B1 = B1, B2 = B2, obs = obs, nullM = nullM, nullS = nullS,
       pM = (sum(nullM >= obs$M - 1e-12) + 1) / (nperm + 1),
       pS = (sum(nullS >= obs$S - 1e-12) + 1) / (nperm + 1),
       pD = pD, n = table(grp))
}
edge_table <- function(r, k = 6) {
  e <- data.frame(from = rownames(r$B1)[row(r$B1)[off]], to = colnames(r$B1)[col(r$B1)[off]],
                  B_g1 = round(r$B1[off], 3), B_g2 = round(r$B2[off], 3), diff = round(r$obs$D[off], 3),
                  p = round(r$pD[off], 3))
  e$p_holm <- round(p.adjust(e$p, "holm"), 3)
  e[order(-abs(e$diff), e$p), ][1:k, ]
}
report <- function(r, labs) {
  cat("各组人数：", paste0(labs, " ", r$n, " 人", collapse = "，"), "\n")
  w <- which(abs(r$obs$D) == r$obs$M & off, arr.ind = TRUE)[1, ]
  cat(sprintf("M（差得最多的边）= %.3f：%s → %s（%s %.3f，%s %.3f）；置换 p = %.3f\n", r$obs$M,
              rownames(r$B1)[w[1]], colnames(r$B1)[w[2]], labs[1], r$B1[w[1], w[2]], labs[2], r$B2[w[1], w[2]], r$pM))
  cat(sprintf("S（整体强度之差）= %.3f（%s %.3f，%s %.3f）；置换 p = %.3f\n", r$obs$S, labs[1], r$obs$S1, labs[2], r$obs$S2, r$pS))
  cat(sprintf("单条边：72 条交叉滞后边中，未校正 p < .05 的有 %d 条；Holm 校正后 %d 条\n",
              sum(r$pD[off] < 0.05), sum(p.adjust(r$pD[off], "holm") < 0.05)))
  cat(sprintf("置换零分布：M 的 95%% 分位数 = %.3f，S 的 95%% 分位数 = %.3f\n", quantile(r$nullM, 0.95), quantile(r$nullS, 0.95)))
  cat("差值最大的 6 条边（diff = 第 1 组 − 第 2 组；p 为单条边的置换 p，p_holm 为 Holm 校正后）：\n")
  print(edge_table(r), row.names = FALSE)
}

# =====================================================================
# 第 1 部分：课程数据，男 vs 女
# 生成数据时，两性只在抑郁题的“均值”上有差异（女性 +0.2），交叉滞后网络完全相同。
# =====================================================================
cat("===== 第 1 部分：课程数据，男 vs 女（每部分置换", NPERM, "次，EBIC）=====\n")
t0 <- Sys.time()
set.seed(2026)
rA <- perm_test(dat, dat$gender)
report(rA, c("男", "女"))
cat(sprintf("用时 %.0f 秒\n", as.numeric(difftime(Sys.time(), t0, units = "secs"))))

# =====================================================================
# 第 2 部分：模拟“确实不同”的两组
# 两组都按课程数据的总体网络 true_B_population 生成；
# 第 2 组把 lone3 → dep1 的系数加 0.20（0.118 → 0.318），其余完全相同。
# 第 3 部分：同样的差异，但每组只有 300 人：还能发现吗？
# =====================================================================
Bp <- true_B()
R1 <- cor(dat[, vars_t(1)]); R2 <- cor(dat[, vars_t(2)])
Se <- R2 - t(Bp) %*% R1 %*% Bp; Se <- (Se + t(Se)) / 2      # 两组共用同一个残差协方差
rmvn <- function(n, S) matrix(rnorm(n * ncol(S)), n) %*% chol(S)
sim_group <- function(n, B) {
  X <- rmvn(n, R1); Y <- X %*% B + rmvn(n, Se)
  setNames(as.data.frame(cbind(X, Y)), c(vars_t(1), vars_t(2)))
}
run_sim <- function(n, delta, seed) {
  t0 <- Sys.time(); set.seed(seed)
  Bg2 <- Bp; Bg2["lone3", "dep1"] <- Bg2["lone3", "dep1"] + delta
  sim <- rbind(sim_group(n, Bp), sim_group(n, Bg2))
  r <- perm_test(sim, rep(c(1, 2), each = n))
  report(r, c("第1组", "第2组"))
  cat(sprintf("事先指定的那一条边 lone3 → dep1：第1组 %.3f，第2组 %.3f，差值 %.3f，单条边置换 p = %.3f\n",
              r$B1["lone3", "dep1"], r$B2["lone3", "dep1"], r$obs$D["lone3", "dep1"], r$pD["lone3", "dep1"]))
  cat(sprintf("用时 %.0f 秒\n", as.numeric(difftime(Sys.time(), t0, units = "secs"))))
  r
}
cat("\n===== 第 2 部分：模拟两组各 600 人，第 2 组 lone3 → dep1 +0.20 =====\n")
rB <- run_sim(600, 0.20, 2027)
cat("\n===== 第 3 部分：同样的差异，每组只有 300 人 =====\n")
rC <- run_sim(300, 0.20, 2028)
cat(sprintf("\n提示：1000 次置换时，最小可能的 p = 1/1001 = %.4f；72 条边做 Holm 校正，最小的 p 要乘以 72 → %.3f，\n", 1 / (NPERM + 1), 72 / (NPERM + 1)),
    "所以“72 条全检 + Holm”在 1000 次置换下不可能显著。单条边检验应只用于事先指定的少数几条边。\n")

# ---- 输出 ------------------------------------------------------------
rs <- list(rA, rB, rC)
summ <- data.frame(part = c("1 课程数据 男 vs 女", "2 模拟 每组600 lone3-dep1 +0.20", "3 模拟 每组300 lone3-dep1 +0.20"),
                   n1 = sapply(rs, function(r) r$n[[1]]), n2 = sapply(rs, function(r) r$n[[2]]), nperm = NPERM,
                   M = round(sapply(rs, function(r) r$obs$M), 3), p_M = round(sapply(rs, function(r) r$pM), 3),
                   S = round(sapply(rs, function(r) r$obs$S), 3), p_S = round(sapply(rs, function(r) r$pS), 3),
                   p_lone3_dep1 = round(sapply(rs, function(r) r$pD["lone3", "dep1"]), 3),
                   edges_p05 = sapply(rs, function(r) sum(r$pD[off] < 0.05)),
                   edges_holm05 = sapply(rs, function(r) sum(p.adjust(r$pD[off], "holm") < 0.05)))
print(summ, row.names = FALSE)
write.csv(summ, out("L7-7_perm_summary.csv"), row.names = FALSE)
png_open("L7-7_null_M.png", 2400, 1000)
par(mfrow = c(1, 3), mar = c(4.2, 4.2, 4, 1))
for (r in list(list(rA, "课程数据：男 vs 女"), list(rB, "模拟：每组 600 人，有差异"), list(rC, "模拟：每组 300 人，有差异"))) {
  hist(r[[1]]$nullM, breaks = 30, col = "grey85", border = "white", xlim = range(c(r[[1]]$nullM, r[[1]]$obs$M * 1.05)),
       main = "", xlab = "M（打乱组别后，差得最多的边）", ylab = "次数")
  title(r[[2]], line = 2)
  mtext(sprintf("红线 = 观测到的 M = %.3f，置换 p = %.3f", r[[1]]$obs$M, r[[1]]$pM), side = 3, line = 0.5, col = "firebrick", cex = 0.85)
  abline(v = r[[1]]$obs$M, col = "firebrick", lwd = 3)
}
invisible(dev.off())
log_close()
