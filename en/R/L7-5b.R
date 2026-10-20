# =====================================================================
# L7-5b.R  Full CLPN Pipeline of Wysocki et al. (2025): LASSO Selection -> lavaan Unpenalized Re-Estimation -> Across-Time Invariance Testing -> In/Out-Prediction
#   (Full CLPN pipeline of Wysocki et al., 2025: l1 selection + unpenalized SEM re-fit)
# Corresponds to lessons/L7-5.html (also referenced in Lesson 7.2). The course main thread (7.2–7.4, 8.x, 10.x) uses
# the "LASSO-only" simplified version common in applied research (e.g., Funkhouser et al., 2021);
# this script demonstrates the full workflow recommended in the original paper and compares it with the simplified version.
#   Step 1 Redundancy reduction: The 9 items do not duplicate wording; no merging needed (goldbricker check in R/L9-2.R)
#   Step 2 Nodewise LASSO (10-fold CV, lambda.min), run separately for T1->T2 and T2->T3; conservative rule: retain if non-zero in either wave
#   Step 3 lavaan path model: Retained paths re-estimated without penalty; all concurrent residuals correlated; FIML (missing = "ml");
#          cross-time equality constraints (T1->T2 paths = T2->T3 paths) tested via nested chi-square test and AIC/BIC, selecting final model, pruned at p < .01
#   Step 4 In-prediction / out-prediction (proportion of variance explained), evaluated on final model
# Items are z-standardized first so coefficients are directly comparable to the LASSO-only version and true population coefficients.
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(lavaan))
log_open("L7-5b_log.txt")
dat <- read_course_data()
for (v in c(vars_t(1), vars_t(2), vars_t(3))) dat[[v]] <- as.numeric(scale(dat[[v]]))
p <- length(items)

## ---- Step 1: Redundancy Reduction (not needed here); Step 2: LASSO Selection (two waves) + Conservative Rule ----
set.seed(2026); B12 <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)])
set.seed(2026); B23 <- clpn_estimate(dat[, vars_t(2)], dat[, vars_t(3)])
keep <- (B12 != 0) | (B23 != 0); diag(keep) <- TRUE        # Autoregressions always retained
off <- row(keep) != col(keep)
cat("Step 2 LASSO (lambda.min): T1->T2 non-zero cross-lagged edges:", sum(B12[off] != 0), "; T2->T3:", sum(B23[off] != 0),
    "; cross-lagged paths entering SEM under conservative rule:", sum(keep[off]), "(per lag)\n")

## ---- Step 3: lavaan Unpenalized Re-Estimation ----
build <- function(equal = FALSE) {
  lines <- c()
  for (t in 2:3) for (j in seq_len(p)) {
    preds <- which(keep[, j])
    lab <- if (equal) paste0("b", preds, "_", j, "*") else ""
    lines <- c(lines, paste0(items[j], "_t", t, " ~ ", paste0(lab, items[preds], "_t", t - 1, collapse = " + ")))
  }
  for (t in 2:3) { cmb <- combn(items, 2)                   # All concurrent residuals correlated pairwise within each wave
    lines <- c(lines, paste0(cmb[1, ], "_t", t, " ~~ ", cmb[2, ], "_t", t)) }
  paste(lines, collapse = "\n")
}
fit_free  <- sem(build(FALSE), data = dat, missing = "ml", fixed.x = FALSE)
fit_equal <- sem(build(TRUE),  data = dat, missing = "ml", fixed.x = FALSE)
fm <- fitMeasures(fit_free, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
cat(sprintf("\nStep 3 SEM (unconstrained): chi^2(%d) = %.2f, p %s; CFI = %.3f; TLI = %.3f; RMSEA = %.3f [%.3f, %.3f]; SRMR = %.3f\n",
            fm["df"], fm["chisq"], ifelse(fm["pvalue"] < .001, "< .001", sprintf("= %.3f", fm["pvalue"])),
            fm["cfi"], fm["tli"], fm["rmsea"], fm["rmsea.ci.lower"], fm["rmsea.ci.upper"], fm["srmr"]))

# Cross-time invariance test: each T1->T2 path = corresponding T2->T3 path
cat("\nStep 3 Equality constraints (each T1->T2 path = corresponding T2->T3 path) nested chi^2 test:\n")
av <- anova(fit_equal, fit_free)
cat(sprintf("Delta chi^2(%d) = %.2f, p = %.3f; AIC: constrained %.1f vs unconstrained %.1f; BIC: constrained %.1f vs unconstrained %.1f\n",
            av$`Df diff`[2], av$`Chisq diff`[2], av$`Pr(>Chisq)`[2], AIC(fit_equal), AIC(fit_free), BIC(fit_equal), BIC(fit_free)))
# Select final model: if chi^2 test does not reject equality and neither AIC nor BIC favors unconstrained, use constrained model (pools information across waves for more precise estimation)
use_equal <- av$`Pr(>Chisq)`[2] >= .05 && AIC(fit_equal) <= AIC(fit_free) && BIC(fit_equal) <= BIC(fit_free)
fit_final <- if (use_equal) fit_equal else fit_free
cat("Final model:", if (use_equal) "Constrained model (invariance holds; used for subsequent pruning and prediction)" else "Unconstrained model (invariance does not hold)", "\n")
fmf <- fitMeasures(fit_final, c("chisq", "df", "cfi", "tli", "rmsea", "srmr"))
cat(sprintf("Final model fit: chi^2(%d) = %.2f; CFI = %.3f; TLI = %.3f; RMSEA = %.3f; SRMR = %.3f\n",
            fmf["df"], fmf["chisq"], fmf["cfi"], fmf["tli"], fmf["rmsea"], fmf["srmr"]))

# Extract unpenalized T1->T2 coefficient matrix (Row = T1 predictor, Column = T2 outcome) and p-values
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
Bt <- true_B(); te <- abs(Bt) >= 0.05                      # Edges with |beta| >= 0.05 in population target (data/true_B_population.csv), same as R/L7-2.R
perf <- function(est_nonzero) c(Recovered = sum(est_nonzero[off] & te[off]), False_positives = sum(est_nonzero[off] & !te[off]),
                               Missed = sum(!est_nonzero[off] & te[off]), Total_est_CL = sum(est_nonzero[off]))
cmp <- rbind(`LASSO-only (lambda.min)` = perf(B12 != 0),
             `LASSO + SEM re-estimation, final model (p < .01)` = perf(sig),
             `LASSO + SEM re-estimation, final model (p < .05)` = perf(P12 < .05),
             `Comparison: unconstrained model (p < .01)` = perf(P12_free < .01))
cat("\nComparison of T1->T2 cross-lagged edges with population target (", sum(te[off]), "cross-lagged edges in population target):\n"); print(cmp)
cat("Correlation between SEM re-estimated edge weights and population target (retained paths) =", round(cor(S12[off & keep], Bt[off & keep]), 3),
    "; correlation between LASSO edge weights and population target (same paths) =", round(cor(B12[off & keep], Bt[off & keep]), 3), "\n")
cat("Example: lone3 -> dep1 population target", round(Bt["lone3", "dep1"], 3), "; LASSO", round(B12["lone3", "dep1"], 3),
    "; SEM re-estimation", round(S12["lone3", "dep1"], 3), sprintf("(p = %.3g)", P12["lone3", "dep1"]), "\n")

## ---- Step 4: In-Prediction and Out-Prediction (T1->T2, Final Model) ----
Sig <- lavInspect(fit_final, "cov.ov")                     # Model-implied covariance
S1 <- Sig[vars_t(1), vars_t(1)]; v2 <- diag(Sig)[vars_t(2)]
cons <- ifelse(grepl("^lone", items), "Loneliness", "Depression")
inpred <- function(j, use) { b <- S12[, j] * use; as.numeric(t(b) %*% S1 %*% b) / unname(v2[j]) }
pred <- t(sapply(seq_len(p), function(j) {
  others <- seq_len(p) != j; xc <- cons != cons[j]
  outk <- sapply(seq_len(p), function(k) S12[j, k]^2 * S1[j, j] / unname(v2[k]))
  c(inPred = inpred(j, rep(1, p)), inPred_CL = inpred(j, others), inPred_bridge = inpred(j, xc),
    outPred = mean(outk), outPred_CL = mean(outk[others]), outPred_bridge = mean(outk[xc]))
}))
rownames(pred) <- items
cat("\nStep 4 In-/out-prediction (proportion of explained variance; CL = omitting autoregression):\n"); print(round(pred, 3))
cat("Highest cross-construct out-prediction:", items[which.max(pred[, "outPred_bridge"])],
    "; highest cross-construct in-prediction:", items[which.max(pred[, "inPred_bridge"])], "\n")
write.csv(round(pred, 4), out("L7-5b_in_out_prediction.csv"))

## ---- Comparison with Within-Person Truth (data/true_B_within.csv) ----
# The population target contains 28 edges induced solely by stable traits; SEM re-estimation and p-value pruning cannot eliminate them because they truly exist in the population.
Bw <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))[items, items]
tw <- Bw != 0
perf_w <- function(est_nonzero) c(Recovered = sum(est_nonzero[off] & tw[off]), False_positives = sum(est_nonzero[off] & !tw[off]),
                                 Missed = sum(!est_nonzero[off] & tw[off]), Total_est_CL = sum(est_nonzero[off]))
cmp_w <- rbind(`LASSO-only (lambda.min)` = perf_w(B12 != 0),
               `LASSO + SEM re-estimation, final model (p < .01)` = perf_w(sig),
               `LASSO + SEM re-estimation, final model (p < .05)` = perf_w(P12 < .05))
cat("\nComparison of T1->T2 cross-lagged edges with within-person truth (", sum(tw[off]), "cross-lagged edges in within-person truth):\n"); print(cmp_w)
cat("Correlation between SEM re-estimated edge weights on retained paths and within-person truth =", round(cor(S12[off & keep], Bw[off & keep]), 3), "\n")
log_close()
