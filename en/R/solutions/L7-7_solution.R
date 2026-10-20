# Solution L7-7: Are the T2 -> T3 networks identical between men and women?
# (200 permutations, single-core runtime approx. 10-20 seconds)
source("R/_setup.R")
library(glmnet)
options(width = 110)
log_open("sol_L7-7_log.txt")
dat <- read_course_data()
NPERM <- 200
est <- function(d) clpn_estimate(d[, vars_t(2)], d[, vars_t(3)], rule = "ebic")   # T2 -> T3
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
cat(sprintf("T2 -> T3, Men %d vs. Women %d, %d permutations\n", sum(g == 0), sum(g == 1), NPERM))
cat(sprintf("M = %.3f (%s -> %s: Men %.3f, Women %.3f), permutation p = %.3f\n", obs$M, rownames(B1)[w[1]], colnames(B1)[w[2]],
            B1[w[1], w[2]], B2[w[1], w[2]], (sum(nullM >= obs$M - 1e-12) + 1) / (NPERM + 1)))
cat(sprintf("S = %.3f (Men %.3f, Women %.3f), permutation p = %.3f\n", obs$S, obs$S1, obs$S2, (sum(nullS >= obs$S - 1e-12) + 1) / (NPERM + 1)))
cat(sprintf("Across 72 edges, %d have unadjusted p < .05; minimum possible p with 200 permutations is %.4f\n", sum(pD[off] < 0.05), 1 / (NPERM + 1)))
cat(sprintf("A priori specified edge lone3 -> dep1: Men %.3f, Women %.3f, single-edge permutation p = %.3f\n", B1["lone3", "dep1"], B2["lone3", "dep1"], pD["lone3", "dep1"]))
log_close()
