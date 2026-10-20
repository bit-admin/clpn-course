# =====================================================================
# L7-7.R  Between-Group Comparisons: Are Two Group CLPNs Identical?
#   (Group comparison with a permutation test)
# Advanced optional lesson. Handcrafted permutation test without requiring new R packages.
# Part 1: Course data, Male vs. Female (data-generating lagged network is identical -> demonstrates null scenario)
# Part 2: Simulated two groups of 600 participants each, Group 2 lone3 -> dep1 coefficient +0.20 (demonstrates detecting true differences)
# Part 3: Identical difference, but with only 300 participants per group (demonstrates power under insufficient sample size)
# For speed and reproducibility, each estimation uses EBIC to select lambda (clpn_estimate(rule = "ebic"), without cross-validation).
# Runtime: single core ~2–4 minutes (3 parts x 1000 permutations; reducing NPERM is faster but yields coarser p-values)
# =====================================================================
source("R/_setup.R")
library(glmnet)
options(width = 110)
log_open("L7-7_log.txt")
dat <- read_course_data()
NPERM <- 1000                                # Permutations per part

# ---- Helpers ---------------------------------------------------------
est <- function(d) clpn_estimate(d[, vars_t(1)], d[, vars_t(2)], rule = "ebic")
off <- matrix(TRUE, length(items), length(items)); diag(off) <- FALSE   # Cross-lagged edge positions
# Three test statistics (following logic of van Borkulo et al., 2023, adapted for CLPN cross-lagged edges):
#   M = absolute difference of the single most divergent edge between two groups (network structure invariance)
#   S = absolute difference in the sum of absolute cross-lagged edge weights (global strength invariance)
#   D = difference for every individual edge (edge invariance), 72 edges
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
    g <- sample(grp)                           # Shuffle group labels while preserving group sample sizes
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
  cat("Sample size per group:", paste0(labs, " n = ", r$n, collapse = ", "), "\n")
  w <- which(abs(r$obs$D) == r$obs$M & off, arr.ind = TRUE)[1, ]
  cat(sprintf("M (maximum edge difference) = %.3f: %s -> %s (%s %.3f, %s %.3f); permutation p = %.3f\n", r$obs$M,
              rownames(r$B1)[w[1]], colnames(r$B1)[w[2]], labs[1], r$B1[w[1], w[2]], labs[2], r$B2[w[1], w[2]], r$pM))
  cat(sprintf("S (global strength difference) = %.3f (%s %.3f, %s %.3f); permutation p = %.3f\n", r$obs$S, labs[1], r$obs$S1, labs[2], r$obs$S2, r$pS))
  cat(sprintf("Individual edges: Out of 72 cross-lagged edges, uncorrected p < .05 for %d edge(s); Holm-corrected for %d edge(s)\n",
              sum(r$pD[off] < 0.05), sum(p.adjust(r$pD[off], "holm") < 0.05)))
  cat(sprintf("Permutation null distribution: 95th percentile of M = %.3f, 95th percentile of S = %.3f\n", quantile(r$nullM, 0.95), quantile(r$nullS, 0.95)))
  cat("Top 6 edges with largest differences (diff = Group 1 - Group 2; p = uncorrected edge permutation p, p_holm = Holm-corrected):\n")
  print(edge_table(r), row.names = FALSE)
}

# =====================================================================
# Part 1: Course Data, Male vs. Female
# In data simulation, genders differed only in depression item means (females +0.2); cross-lagged networks are identical.
# =====================================================================
cat("===== Part 1: Course Data, Male vs. Female (", NPERM, "permutations per part, EBIC) =====\n")
t0 <- Sys.time()
set.seed(2026)
rA <- perm_test(dat, dat$gender)
report(rA, c("Male", "Female"))
cat(sprintf("Elapsed time: %.0f seconds\n", as.numeric(difftime(Sys.time(), t0, units = "secs"))))

# =====================================================================
# Part 2: Simulating Truly Different Groups
# Both groups generated from course population target true_B_population;
# Group 2 has lone3 -> dep1 coefficient increased by +0.20 (0.118 -> 0.318), all else identical.
# Part 3: Same difference, but only 300 participants per group: can it still be detected?
# =====================================================================
Bp <- true_B()
R1 <- cor(dat[, vars_t(1)]); R2 <- cor(dat[, vars_t(2)])
Se <- R2 - t(Bp) %*% R1 %*% Bp; Se <- (Se + t(Se)) / 2      # Both groups share identical residual covariance
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
  report(r, c("Group 1", "Group 2"))
  cat(sprintf("A priori specified edge lone3 -> dep1: Group 1 %.3f, Group 2 %.3f, difference %.3f, single-edge permutation p = %.3f\n",
              r$B1["lone3", "dep1"], r$B2["lone3", "dep1"], r$obs$D["lone3", "dep1"], r$pD["lone3", "dep1"]))
  cat(sprintf("Elapsed time: %.0f seconds\n", as.numeric(difftime(Sys.time(), t0, units = "secs"))))
  r
}
cat("\n===== Part 2: Simulating Two Groups of 600 Each, Group 2 lone3 -> dep1 +0.20 =====\n")
rB <- run_sim(600, 0.20, 2027)
cat("\n===== Part 3: Same Difference, with Only 300 Participants Per Group =====\n")
rC <- run_sim(300, 0.20, 2028)
cat(sprintf("\nNote: With 1000 permutations, minimum possible p = 1/1001 = %.4f; for 72 edges with Holm correction, minimum p is multiplied by 72 -> %.3f,\n", 1 / (NPERM + 1), 72 / (NPERM + 1)),
    "meaning testing all 72 edges with Holm correction cannot reach significance under 1000 permutations. Single-edge tests should be reserved for a few a priori specified edges.\n")

# ---- Output ----------------------------------------------------------
rs <- list(rA, rB, rC)
summ <- data.frame(part = c("1 Course data Male vs Female", "2 Sim n=600 lone3-dep1 +0.20", "3 Sim n=300 lone3-dep1 +0.20"),
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
for (r in list(list(rA, "Course data: Male vs. Female"), list(rB, "Simulation: n = 600 per group, with difference"), list(rC, "Simulation: n = 300 per group, with difference"))) {
  hist(r[[1]]$nullM, breaks = 30, col = "grey85", border = "white", xlim = range(c(r[[1]]$nullM, r[[1]]$obs$M * 1.05)),
       main = "", xlab = "M (maximum edge difference across permuted groups)", ylab = "Frequency")
  title(r[[2]], line = 2)
  mtext(sprintf("Red line = observed M = %.3f, permutation p = %.3f", r[[1]]$obs$M, r[[1]]$pM), side = 3, line = 0.5, col = "firebrick", cex = 0.85)
  abline(v = r[[1]]$obs$M, col = "firebrick", lwd = 3)
}
invisible(dev.off())
log_close()
