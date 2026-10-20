# =====================================================================
# L7-2.R  Nodewise CLPN Estimation with glmnet (Nodewise LASSO estimation of a CLPN)
# Method: The "LASSO-only" CLPN commonly used in applied research (e.g., Funkhouser et al., 2021) —
#         for each T2 item, run LASSO regression (cv.glmnet) on all T1 items,
#         assembling coefficients directly into a directed network B.
#         This corresponds to Step 1 (edge selection) of the full procedure in Wysocki et al. (2025);
#         subsequent steps including unpenalized SEM re-estimation are covered in R/L7-5b.R.
# =====================================================================
source("R/_setup.R")
library(glmnet)
log_open("L7-2_log.txt")
dat <- read_course_data()
d1 <- dat[, vars_t(1)]                 # T1 items
d2 <- dat[, vars_t(2)]                 # T2 items (same item order!)

# ---- Lesson Code (line-by-line explanation) ----
X <- scale(as.matrix(d1))              # Standardize: coefficients become comparable (standardized coefficients)
Y <- scale(as.matrix(d2))
p <- ncol(X); labs <- sub("_t1", "", colnames(X))
B <- matrix(0, p, p, dimnames = list(labs, labs))  # Row = T1 predictor, Column = T2 outcome
set.seed(2026)                         # cv.glmnet uses random folds -> set seed for reproducibility
for (j in seq_len(p)) {                # Run one regression for each T2 node j
  cvfit <- cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
  B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]  # Drop intercept
}
AR <- diag(B)                          # Autoregressive edges
CL <- B; diag(CL) <- 0                 # Cross-lagged edges
cat("Estimated B (lambda.min):\n"); print(round(B, 2))

# ---- Comparison with Known Truths (Advantage of Simulated Data) ----
# The course dataset has two distinct "truths" (they are not the same matrix):
#   Population target (data/true_B_population.csv): coefficients to which standard CLPN converges
#     as sample size approaches infinity, including components induced by stable traits;
#   Within-person truth (data/true_B_within.csv): data-generating within-person lagged coefficients.
# CLPN's population target != within-person process. We first compare against the population target,
# and then against the within-person truth at the end of the script.
Bt <- true_B()
cat("\nPopulation target (data/true_B_population.csv, target of standard CLPN as N -> Inf):\n"); print(round(Bt, 2))
compare <- function(Best, Btrue, thr = 0.05) {
  # Treat |Btrue| >= thr as "edges that should be recovered". For the population target, 0.05 is used
  # (there are no exact zeros in the population matrix; 0.05 is a heuristic cutoff; small edges of
  # 0.05–0.07 within the same construct arising from stable traits will also be included).
  te <- abs(Btrue) >= thr; ee <- Best != 0; off <- row(Best) != col(Best)
  c(True_CL_edges = sum(te & off), Recovered = sum(te & ee & off), Missed = sum(te & !ee & off),
    False_positives = sum(!te & ee & off), Total_est_CL = sum(ee & off),
    r_with_truth = round(cor(Best[off], Btrue[off]), 3))
}
set.seed(2026); B_1se  <- clpn_estimate(d1, d2, rule = "lambda.1se")
B_ebic <- clpn_estimate(d1, d2, rule = "ebic")
tab <- rbind(lambda.min = compare(B, Bt), lambda.1se = compare(B_1se, Bt), EBIC = compare(B_ebic, Bt))
cat("\nMethod performance (vs. population target, cross-lagged edges only):\n"); print(tab)
cat("lambda.1se and EBIC are sparser: fewer false positives, but may miss weak edges in the population target.\n")
cat("Note: B[\"lone3\", \"dep1\"] =", round(B["lone3", "dep1"], 3), "indicates T1 Feeling isolated -> T2 Depressed mood.\n")

write.csv(round(B, 4), out("L7-2_B_lambda_min.csv"))
write.csv(round(B_1se, 4), out("L7-2_B_lambda_1se.csv"))
write.csv(edge_list(B), out("L7-2_edgelist.csv"), row.names = FALSE)
saveRDS(B, out("L7-2_B.rds"))
png_open("L7-2_est_vs_true.png", 2400, 1200)
off <- row(B) != col(B)
Bw <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))[labs, labs]   # Within-person truth
par(mfrow = c(1, 2))
plot(Bt[off], B[off], pch = 16, col = ifelse(B[off] == 0, "grey60", "blue"),
     xlab = "Population target", ylab = "Estimated coefficient (lambda.min)",
     main = "Cross-lagged edges: Estimated vs. Population target")
abline(0, 1, lty = 2); abline(h = 0, v = 0, col = "grey")
plot(Bw[off], B[off], pch = 16, col = ifelse(B[off] == 0, "grey60", "blue"),
     xlab = "Within-person truth (lag)", ylab = "Estimated coefficient (lambda.min)",
     main = "Cross-lagged edges: Estimated vs. Within-person truth")
abline(0, 1, lty = 2); abline(h = 0, v = 0, col = "grey")
invisible(dev.off())

# ---- Edge Recovery Under Two Truths: Population Target vs. Within-Person Truth ----
cat("\nWithin-person truth (data/true_B_within.csv, data-generating within-person lagged coefficients):\n"); print(round(Bw, 2))
tgt <- abs(Bt) >= 0.05 & off                       # "Edges" in population target
win <- Bw != 0 & off                               # Edges in within-person truth (non-zero = edge)
trait <- tgt & !win                                # Present only in population target: edges induced by stable traits
same_con <- outer(sub("\\d$", "", labs), sub("\\d$", "", labs), "==")   # Same construct (lone / dep)
cat("\nAmong the", sum(tgt), "cross-lagged edges with |beta| >= 0.05 in the population target:",
    sum(tgt & win), "are also present in the within-person truth +", sum(trait),
    "are zero in the within-person truth\n")
cat("Of the latter", sum(trait), "edges,", sum(trait & same_con), "are within-construct edges; absolute value range:",
    sprintf("%.3f", min(abs(Bt[trait]))), "–", sprintf("%.3f", max(abs(Bt[trait]))), "\n")
cat("Among the edges in the within-person truth,", sum(win & !tgt), "have |beta| < 0.05 in the population target\n")
B_ebic_r <- B_ebic; dimnames(B_ebic_r) <- dimnames(B)
rules <- list(lambda.min = B, lambda.1se = B_1se, EBIC = B_ebic_r)
rec <- do.call(rbind, lapply(names(rules), function(r) {
  Bh <- rules[[r]]
  one <- function(truth, Btrue, thr) {
    v <- compare(Bh, Btrue, thr)
    data.frame(rule = r, truth = truth, n_true = v[[1]], hit = v[[2]], miss = v[[3]], fp = v[[4]],
               n_est = v[[5]], r = v[[6]], trait_hit = sum(Bh != 0 & trait))
  }
  rbind(one("population", Bt, 0.05), one("within", Bw, 1e-8))
}))
cat("\nEdge recovery under two truths (cross-lagged edges only; population = population target |beta| >= 0.05, within = non-zero in within-person truth):\n")
print(rec, row.names = FALSE)
cat("trait_hit = number of edges estimated as non-zero that exist only in the population target (within-person truth is zero).\n")
cat("When evaluated against the within-person truth, all these edges count as false positives: they truly exist in the population, but do not reflect within-person processes.\n")
write.csv(rec, out("L7-2_recovery_two_truths.csv"), row.names = FALSE)
write.csv(round(B_ebic_r, 4), out("L7-2_B_ebic.csv"))
log_close()
