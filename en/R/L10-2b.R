# =====================================================================
# L10-2b.R  Capstone Project ② Supplement: Required Sensitivity Analysis —
#           Full CLPN Pipeline of Wysocki et al. (2025)
#   (Required sensitivity analysis: full CLPN pipeline of Wysocki et al., 2025)
# The primary analysis (R/L10-2.R) is the simplified "LASSO-only" CLPN: edges selected
# and already shrunk by LASSO are directly treated as network edge weights.
# The full procedure recommended by methodological literature adds a crucial step:
# use LASSO only to select which paths to constrain to 0, then re-estimate the remaining
# paths unpenalized within SEM.
# This script applies the full procedure to the Capstone Project data (R/output/L10-1_clean_data.csv)
# and evaluates concordance against primary analysis edges item by item:
#   Step 1 Redundancy merging: All 9 items exhibit distinct wording; no merging (goldbricker check in R/L9-2.R)
#   Step 2 Nodewise LASSO (10-fold CV, rule matching primary analysis), run separately for T1→T2 and T2→T3;
#          conservative rule: constrain to 0 only if 0 in both lags
#   Step 3 lavaan path model: Retained paths re-estimated unpenalized; cross-sectional residual covariances
#          within wave; FIML (missing = "ml"); nested chi-square test and AIC/BIC for cross-time invariance
#          (T1→T2 paths = T2→T3 paths) to select final model; prune at p < .01
#   Step 4 in-/out-prediction (proportion of variance explained) using the final model
#   Step 5 Concordance check with primary analysis: How many of the strongest edges survive in the full procedure?
#          Does the construct-level asymmetry between the two directions hold?
# Syntax matches R/L7-5b.R (Lesson 7.5), substituting the cleaned Capstone data and adding Step 5.
# Dependencies: R/L10-1.R (cleaned data) and R/L10-2.R (primary analysis results for Step 5 comparison).
# Runtime: Two lavaan model fits plus 18 cross-validated LASSO runs, typically < 1 minute.
# Output: R/output/L10-2b_log.txt, L10-2b_edges.csv, L10-2b_summary.csv, L10-2b_in_out_prediction.csv, L10-2b_results.rds
# =====================================================================
source("R/_setup.R")
need_output("L10-1_clean_data.csv", "R/L10-1.R", chain = "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-2b.R → R/L10-3.R")   # Prerequisite check
need_output("L10-2_results.rds", "R/L10-2.R", chain = "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-2b.R → R/L10-3.R")
suppressPackageStartupMessages(library(lavaan))
log_open("L10-2b_log.txt")
SEED <- 2026; RULE <- "lambda.min"; ALPHA <- .01      # Consistent with analysis plan and R/L10-2.R; ALPHA = pruning significance level
dat <- read.csv(out("L10-1_clean_data.csv"))          # From L10-1.R
for (v in c(vars_t(1), vars_t(2), vars_t(3))) dat[[v]] <- as.numeric(scale(dat[[v]]))   # z-standardization ensures comparability with primary analysis
p <- length(items)
res <- readRDS(out("L10-2_results.rds"))              # Primary analysis: res$B (LASSO coefficient matrix), res$bs (bootstrap edge table)
B_main <- res$B
off <- row(B_main) != col(B_main)

## ---- Step 2: LASSO Edge Selection (Both Lags) + Conservative Rule ----
set.seed(SEED); B12 <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], rule = RULE)
set.seed(SEED); B23 <- clpn_estimate(dat[, vars_t(2)], dat[, vars_t(3)], rule = RULE)
cat("Check: Is the T1→T2 LASSO coefficient matrix in this script identical to the L10-2.R primary analysis? ",
    isTRUE(all.equal(B12, B_main, check.attributes = FALSE)), "\n")
keep <- (B12 != 0) | (B23 != 0); diag(keep) <- TRUE        # Retain autoregressive paths by default
cat("Step 2 LASSO (", RULE, "): T1→T2 non-zero cross-lagged edges: ", sum(B12[off] != 0),
    "; T2→T3: ", sum(B23[off] != 0),
    "; cross-lagged paths entering SEM under conservative rule: ", sum(keep[off]),
    " (per lag, out of ", sum(off), " possible positions)\n", sep = "")

## ---- Step 3: lavaan Unpenalized Re-estimation ----
build <- function(equal = FALSE) {
  lines <- c()
  for (t in 2:3) for (j in seq_len(p)) {
    preds <- which(keep[, j])
    lab <- if (equal) paste0("b", preds, "_", j, "*") else ""
    lines <- c(lines, paste0(items[j], "_t", t, " ~ ", paste0(lab, items[preds], "_t", t - 1, collapse = " + ")))
  }
  for (t in 2:3) { cmb <- combn(items, 2)                   # Residual covariances among all pairs within each wave
    lines <- c(lines, paste0(cmb[1, ], "_t", t, " ~~ ", cmb[2, ], "_t", t)) }
  paste(lines, collapse = "\n")
}
fit_free  <- sem(build(FALSE), data = dat, missing = "ml", fixed.x = FALSE)
fit_equal <- sem(build(TRUE),  data = dat, missing = "ml", fixed.x = FALSE)
fm <- fitMeasures(fit_free, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
cat(sprintf("\nStep 3 SEM (unconstrained): χ²(%d) = %.2f, p %s; CFI = %.3f; TLI = %.3f; RMSEA = %.3f [%.3f, %.3f]; SRMR = %.3f\n",
            fm["df"], fm["chisq"], ifelse(fm["pvalue"] < .001, "< .001", sprintf("= %.3f", fm["pvalue"])),
            fm["cfi"], fm["tli"], fm["rmsea"], fm["rmsea.ci.lower"], fm["rmsea.ci.upper"], fm["srmr"]))
cat("\nStep 3 Nested χ² test for cross-time invariance (each T1→T2 path = corresponding T2→T3 path):\n")
av <- anova(fit_equal, fit_free)
ic <- c(AIC_equal = AIC(fit_equal), AIC_free = AIC(fit_free), BIC_equal = BIC(fit_equal), BIC_free = BIC(fit_free))
cat(sprintf("Δχ²(%d) = %.2f, p = %.3f; AIC: constrained %.1f vs unconstrained %.1f; BIC: constrained %.1f vs unconstrained %.1f\n",
            av$`Df diff`[2], av$`Chisq diff`[2], av$`Pr(>Chisq)`[2], ic["AIC_equal"], ic["AIC_free"], ic["BIC_equal"], ic["BIC_free"]))
# Select final model: if chi-square test does not reject invariance and neither AIC nor BIC favors unconstrained, retain constrained
use_equal <- av$`Pr(>Chisq)`[2] >= .05 && ic["AIC_equal"] <= ic["AIC_free"] && ic["BIC_equal"] <= ic["BIC_free"]
fit_final <- if (use_equal) fit_equal else fit_free
cat("Final model: ", if (use_equal) "Constrained model (invariance holds; used for subsequent pruning and prediction)" else "Unconstrained model (invariance rejected; reporting T1→T2 lag below)", "\n")
fmf <- fitMeasures(fit_final, c("chisq", "df", "cfi", "tli", "rmsea", "srmr"))
cat(sprintf("Final model fit: χ²(%d) = %.2f; CFI = %.3f; TLI = %.3f; RMSEA = %.3f; SRMR = %.3f\n",
            fmf["df"], fmf["chisq"], fmf["cfi"], fmf["tli"], fmf["rmsea"], fmf["srmr"]))

# Extract unpenalized coefficients, SEs, and p-values for T1→T2 (rows = T1 predictors, cols = T2 outcomes)
# Paths not entering SEM: coefficient 0, p-value NA
coef12 <- function(fit) {
  pe <- parameterEstimates(fit)
  reg <- pe[pe$op == "~" & grepl("_t2$", pe$lhs), ]
  S <- SE <- matrix(0, p, p, dimnames = list(items, items)); P <- matrix(NA_real_, p, p, dimnames = list(items, items))
  for (r in seq_len(nrow(reg))) { k <- sub("_t1$", "", reg$rhs[r]); j <- sub("_t2$", "", reg$lhs[r])
    S[k, j] <- reg$est[r]; SE[k, j] <- reg$se[r]; P[k, j] <- reg$pvalue[r] }
  list(S = S, SE = SE, P = P)
}
cf <- coef12(fit_final); S12 <- cf$S; P12 <- cf$P
sig <- !is.na(P12) & P12 < ALPHA                           # Retained paths after pruning
S_pruned <- S12 * sig                                      # Pruned coefficient matrix (non-significant set to 0)
lone <- 1:4; dep <- 5:9
n_sig <- c(total = sum(sig[off]), lone_to_dep = sum(sig[lone, dep]), dep_to_lone = sum(sig[dep, lone]),
           within_construct = sum(sig[off]) - sum(sig[lone, dep]) - sum(sig[dep, lone]))
cat(sprintf("\nCross-lagged edges retained after pruning at p < %.2f: %d edges (Loneliness→Depression: %d, Depression→Loneliness: %d, within-construct: %d); at p < .05: %d edges\n",
            ALPHA, n_sig[1], n_sig[2], n_sig[3], n_sig[4], sum(!is.na(P12[off]) & P12[off] < .05)))

## ---- Step 4: in-prediction & out-prediction (T1→T2, Final Model) ----
Sig <- lavInspect(fit_final, "cov.ov")                     # Model-implied covariance matrix
S1 <- Sig[vars_t(1), vars_t(1)]; v2 <- diag(Sig)[vars_t(2)]
cons <- ifelse(grepl("^lone", items), "Loneliness", "Depression")
inpred <- function(j, use) { b <- S12[, j] * use; as.numeric(t(b) %*% S1 %*% b) / unname(v2[j]) }
pred <- t(sapply(seq_len(p), function(j) {
  others <- seq_len(p) != j; xc <- cons != cons[j]
  outk <- sapply(seq_len(p), function(k) S12[j, k]^2 * S1[j, j] / unname(v2[k]))
  c(inPred = inpred(j, rep(1, p)), inPred_CL = inpred(j, others), inPred_xconstruct = inpred(j, xc),
    outPred = mean(outk), outPred_CL = mean(outk[others]), outPred_xconstruct = mean(outk[xc]))
}))
rownames(pred) <- items
cat("\nStep 4 in-/out-prediction (proportion of explained variance; CL = excluding autoregression):\n"); print(round(pred, 3))
cat("Highest cross-construct out-prediction: ", items[which.max(pred[, "outPred_xconstruct"])],
    "; highest cross-construct in-prediction: ", items[which.max(pred[, "inPred_xconstruct"])], "\n")
write.csv(round(pred, 4), out("L10-2b_in_out_prediction.csv"))

## ---- Step 5: Item-by-Item Concordance Check with Primary Analysis (LASSO-Only) ----
bs <- res$bs                                               # Bootstrap edge table from primary analysis (node1 → node2)
e <- data.frame(from = rep(items, times = p), to = rep(items, each = p), stringsAsFactors = FALSE)
e <- e[e$from != e$to, ]
ix <- cbind(e$from, e$to)
e$from_en <- item_en[e$from]; e$to_en <- item_en[e$to]
e$lasso <- B_main[ix]; e$lasso_t23 <- B23[ix]                 # LASSO coefficients for T1→T2 and T2→T3 lags
bkey <- paste(bs$node1, bs$node2)
e$boot_q2.5 <- bs$q2.5[match(paste(e$from, e$to), bkey)]; e$boot_q97.5 <- bs$q97.5[match(paste(e$from, e$to), bkey)]
e$in_sem <- keep[ix]; e$sem_est <- S12[ix]; e$sem_se <- cf$SE[ix]; e$sem_p <- P12[ix]
e$kept_p01 <- sig[ix]
cff <- coef12(fit_free); e$free_est <- cff$S[ix]; e$free_p <- cff$P[ix]   # Comparison: unconstrained model T1→T2 lag
Bt <- true_B(); Bw <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))   # Two truths available only in simulated data (Lessons 7.1, 7.5)
e$true_pop <- Bt[ix]; e$true_within <- Bw[ix]
e <- e[order(-abs(e$lasso), -abs(e$sem_est)), ]
rownames(e) <- NULL
write.csv(e, out("L10-2b_edges.csv"), row.names = FALSE, fileEncoding = "UTF-8")

TOP <- 10
top <- head(e[e$lasso != 0, ], TOP)
excl0 <- !is.na(e$boot_q2.5) & (e$boot_q2.5 > 0 | e$boot_q97.5 < 0)   # Primary analysis bootstrap interval excludes 0
cat("\nStep 5 Concordance check: Results for top ", TOP, " primary analysis cross-lagged edges in full procedure:\n", sep = "")
tab <- data.frame(Edge = paste0(top$from, " → ", top$to), Items = paste0(top$from_en, " → ", top$to_en),
                  LASSO = round(top$lasso, 3), Bootstrap_CI = sprintf("[%.3f, %.3f]", top$boot_q2.5, top$boot_q97.5),
                  SEM_refit = round(top$sem_est, 3), p = signif(top$sem_p, 2), Retained = ifelse(top$kept_p01, "Yes", "No"))
print(tab, row.names = FALSE)
cat(sprintf("Retained %d out of top %d edges; retained %d out of top 3 edges\n", TOP, sum(top$kept_p01), sum(head(top$kept_p01, 3))))
if (use_equal && any(!top$kept_p01)) {                     # In constrained model, coefficients represent common values across both lags
  dr <- top[!top$kept_p01, ]
  cat("Breakdown of un-retained edges across lags (constrained model estimates common value across lags):\n")
  print(data.frame(Edge = paste0(dr$from, " → ", dr$to), LASSO_T1T2 = round(dr$lasso, 3), LASSO_T2T3 = round(dr$lasso_t23, 3),
                   Free_T1T2 = round(dr$free_est, 3), Free_p = signif(dr$free_p, 2), Constrained = round(dr$sem_est, 3)),
        row.names = FALSE)
}
both <- sum(e$lasso != 0 & e$kept_p01); lasso_only <- sum(e$lasso != 0 & !e$kept_p01); sem_only <- sum(e$lasso == 0 & e$kept_p01)
cat(sprintf("Of the %d non-zero edges in primary analysis, %d were retained in full procedure and %d were dropped; %d edges were retained in full procedure but 0 in primary analysis\n",
            sum(e$lasso != 0), both, lasso_only, sem_only))
cat(sprintf("Of the %d edges whose primary analysis bootstrap CI excludes 0, %d were retained in full procedure\n", sum(excl0), sum(excl0 & e$kept_p01)))
r_ls <- cor(B_main[off], S12[off])
cat("Correlation between primary analysis LASSO coefficients and SEM re-estimated coefficients (all ", sum(off), " cross-lagged positions; unentered set to 0) = ", round(r_ls, 3), "\n", sep = "")
sums <- c(ld_lasso = sum(B_main[lone, dep]), dl_lasso = sum(B_main[dep, lone]),
          ld_full = sum(S_pruned[lone, dep]), dl_full = sum(S_pruned[dep, lone]))
cat(sprintf("Construct-level sum of edge weights: Loneliness→Depression primary %.2f, full procedure (pruned) %.2f; Depression→Loneliness primary %.2f, full procedure %.2f\n",
            sums["ld_lasso"], sums["ld_full"], sums["dl_lasso"], sums["dl_full"]))

# Comparison with true structure (simulated data only): Two truths (Lessons 7.1, 7.5). Definition of population target "true edges" matches R/L7-2.R and R/L7-5b.R: |β| ≥ 0.05
te <- abs(Bt) >= 0.05
perf2 <- function(nz, tr) c(Recovered = sum(nz[off] & tr[off]), False_Positives = sum(nz[off] & !tr[off]), Missed = sum(!nz[off] & tr[off]), Estimated_Edges = sum(nz[off]))
perf <- function(nz) perf2(nz, te)
cmp <- rbind(`Primary analysis: LASSO-only` = perf(B_main != 0), `Full procedure: SEM re-fit + p < .01 pruning` = perf(sig))
cat("\nComparison with population target (data/true_B_population.csv cross-lagged edges with |β| ≥ 0.05, n = ", sum(te[off]), "):\n", sep = ""); print(cmp)
tw <- Bw[items, items] != 0                                # Within-person truth: actual lagged coefficients used in data simulation
cmp_w <- rbind(`Primary analysis: LASSO-only` = perf2(B_main != 0, tw), `Full procedure: SEM re-fit + p < .01 pruning` = perf2(sig, tw))
cat("Comparison with within-person truth (data/true_B_within.csv non-zero cross-lagged edges, n = ", sum(tw[off]), "; remaining 'false positives' largely stem from stable traits):\n", sep = ""); print(cmp_w)

summ <- c(n_lasso_main = sum(B_main[off] != 0), n_cl12 = sum(B12[off] != 0), n_cl23 = sum(B23[off] != 0), n_keep = sum(keep[off]),
          free_chisq = unname(fm["chisq"]), free_df = unname(fm["df"]), free_p = unname(fm["pvalue"]),
          free_cfi = unname(fm["cfi"]), free_tli = unname(fm["tli"]), free_rmsea = unname(fm["rmsea"]),
          free_rmsea_lo = unname(fm["rmsea.ci.lower"]), free_rmsea_hi = unname(fm["rmsea.ci.upper"]), free_srmr = unname(fm["srmr"]),
          eq_dchisq = av$`Chisq diff`[2], eq_ddf = av$`Df diff`[2], eq_p = av$`Pr(>Chisq)`[2],
          aic_equal = unname(ic["AIC_equal"]), aic_free = unname(ic["AIC_free"]), bic_equal = unname(ic["BIC_equal"]), bic_free = unname(ic["BIC_free"]),
          use_equal = as.numeric(use_equal),
          fin_chisq = unname(fmf["chisq"]), fin_df = unname(fmf["df"]), fin_cfi = unname(fmf["cfi"]), fin_tli = unname(fmf["tli"]),
          fin_rmsea = unname(fmf["rmsea"]), fin_srmr = unname(fmf["srmr"]),
          n_sig01 = n_sig[[1]], n_sig01_ld = n_sig[[2]], n_sig01_dl = n_sig[[3]], n_sig01_within = n_sig[[4]],
          n_sig05 = sum(!is.na(P12[off]) & P12[off] < .05),
          n_both = both, n_lasso_only = lasso_only, n_sem_only = sem_only,
          top_n = TOP, top_kept = sum(top$kept_p01), top3_kept = sum(head(top$kept_p01, 3)),
          n_boot_excl0 = sum(excl0), n_boot_excl0_kept = sum(excl0 & e$kept_p01),
          r_lasso_sem = r_ls, sums,
          n_true = sum(te[off]), found_lasso = cmp[1, 1], fp_lasso = cmp[1, 2], found_full = cmp[2, 1], fp_full = cmp[2, 2],
          n_true_w = sum(tw[off]), found_lasso_w = cmp_w[1, 1], fp_lasso_w = cmp_w[1, 2], found_full_w = cmp_w[2, 1], fp_full_w = cmp_w[2, 2])
write.csv(data.frame(statistic = names(summ), value = unname(summ)), out("L10-2b_summary.csv"), row.names = FALSE)
saveRDS(list(edges = e, summary = summ, S12 = S12, P12 = P12, keep = keep, use_equal = use_equal, pred = pred),
        out("L10-2b_results.rds"))
log_close()
