# 练习答案 L7-7：男性与女性的 T2 → T3 网络一样吗？（置换 200 次，单核约 10–20 秒）
source("R/_setup.R")
library(glmnet)
options(width = 110)
log_open("sol_L7-7_log.txt")
dat <- read_course_data()
NPERM <- 200
est <- function(d) clpn_estimate(d[, vars_t(2)], d[, vars_t(3)], rule = "ebic")   # T2 → T3
off <- matrix(TRUE, 9, 9); diag(off) <- FALSE
stats <- function(B1, B2) list(M = max(abs((B1 - B2)[off])), S = abs(sum(abs(B1[off])) - sum(abs(B2[off]))),
                               D = B1 - B2, S1 = sum(abs(B1[off])), S2 = sum(abs(B2[off])))
g <- dat$gender
B1 <- est(dat[g == 0, ]); B2 <- est(dat[g == 1, ]); obs <- stats(B1, B2)
set.seed(2026)
nullM <- nullS <- numeric(NPERM); exceed <- matrix(0, 9, 9)
for (b in 1:NPERM) {
  gb <- sample(g)
  s <- stats(est(dat[gb == 0, ]), est(dat[gb == 1, ]))
  nullM[b] <- s$M; nullS[b] <- s$S; exceed <- exceed + (abs(s$D) >= abs(obs$D) - 1e-12)
}
pD <- (exceed + 1) / (NPERM + 1)
w <- which(abs(obs$D) == obs$M & off, arr.ind = TRUE)[1, ]
cat(sprintf("T2 → T3，男 %d 人 vs 女 %d 人，置换 %d 次\n", sum(g == 0), sum(g == 1), NPERM))
cat(sprintf("M = %.3f（%s → %s：男 %.3f，女 %.3f），置换 p = %.3f\n", obs$M, rownames(B1)[w[1]], colnames(B1)[w[2]],
            B1[w[1], w[2]], B2[w[1], w[2]], (sum(nullM >= obs$M - 1e-12) + 1) / (NPERM + 1)))
cat(sprintf("S = %.3f（男 %.3f，女 %.3f），置换 p = %.3f\n", obs$S, obs$S1, obs$S2, (sum(nullS >= obs$S - 1e-12) + 1) / (NPERM + 1)))
cat(sprintf("72 条边中未校正 p < .05 的有 %d 条；200 次置换时最小可能的 p = %.4f\n", sum(pD[off] < 0.05), 1 / (NPERM + 1)))
cat(sprintf("事先指定的一条边 lone3 → dep1：男 %.3f，女 %.3f，单条边置换 p = %.3f\n", B1["lone3", "dep1"], B2["lone3", "dep1"], pD["lone3", "dep1"]))
log_close()
