# =====================================================================
# L10-3.R  Capstone Project ③: Auto-Generated "Results Section" Draft
#          (Auto-filled results draft)
# Principle: Every single number in the Results section must be traceable to code output
# — so let the code fill the numbers.
# =====================================================================
source("R/_setup.R")
CHAIN <- "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-2b.R → R/L10-3.R"
need_output("L10-2_results.rds", "R/L10-2.R", chain = CHAIN)   # Prerequisite check
need_output("L10-2b_results.rds", "R/L10-2b.R", chain = CHAIN)  # Required full procedure sensitivity analysis
res <- readRDS(out("L10-2_results.rds"))            # Requires running L10-2.R first
B <- res$B; CL <- cl_only(B); cen <- res$cen; cs <- res$cs
el <- edge_list(CL)[1:3, ]
f <- function(x) sprintf("%.2f", x)
fr <- function(r) ifelse(abs(r) < 1 & abs(round(r, 2)) >= 1, sprintf("%.3f", r), sprintf("%.2f", r))  # Avoid writing 0.997 as 1.00
# Required sensitivity analysis: Full procedure of Wysocki et al. (2025) (R/L10-2b.R).
# Reported alongside primary analysis, with numbers filled programmatically.
fp <- readRDS(out("L10-2b_results.rds")); s <- fp$summary
f3p <- function(p) ifelse(p < .001, "< 0.001", sprintf("= %.3f", p))
ic_txt <- if (s["aic_equal"] <= s["aic_free"] && s["bic_equal"] <= s["bic_free"]) "both AIC and BIC favored the constrained model" else
  if (s["aic_equal"] > s["aic_free"] && s["bic_equal"] > s["bic_free"]) "both AIC and BIC favored the unconstrained model" else
  sprintf("AIC favored the %s model while BIC favored the %s model",
          ifelse(s["aic_equal"] <= s["aic_free"], "constrained", "unconstrained"),
          ifelse(s["bic_equal"] <= s["bic_free"], "constrained", "unconstrained"))
top <- head(fp$edges[fp$edges$lasso != 0, ], s["top_n"])
drop <- top[!top$kept_p01, ]
drop_txt <- if (nrow(drop) == 0) "all of these edges were retained" else
  paste0("those not retained were: ", paste(sprintf("T1 '%s' → T2 '%s' (primary analysis β = %s; full procedure β = %s, p %s)",
                                                   drop$from_en, drop$to_en, f(drop$lasso), f(drop$sem_est), f3p(drop$sem_p)), collapse = "; "))
fp_par <- paste0(
  sprintf("Full Procedure Sensitivity Analysis. In accordance with the full procedure recommended by Wysocki et al. (2025), nodewise LASSO regressions were first conducted separately for the T1→T2 and T2→T3 lags. The %d cross-lagged paths non-zero in either lag were entered into a path model (the remainder fixed to zero) and re-estimated without penalization in lavaan (cross-sectional residual covariances within wave, FIML). ",
          s["n_keep"]),
  sprintf("Nested testing of cross-time invariance constraints yielded Δχ²(%d) = %.2f, p %s, and %s; therefore, the %s was retained as the final model (χ²(%d) = %.2f, CFI = %.3f, TLI = %.3f, RMSEA = %.3f, SRMR = %.3f). ",
          s["eq_ddf"], s["eq_dchisq"], f3p(s["eq_p"]), ic_txt,
          ifelse(fp$use_equal, "constrained model specifying equal paths across lags", "unconstrained model estimating lag-specific paths (T1→T2 lag reported below)"),
          s["fin_df"], s["fin_chisq"], s["fin_cfi"], s["fin_tli"], s["fin_rmsea"], s["fin_srmr"]),
  sprintf("Pruning at p < .01 retained %d cross-lagged edges (%d Loneliness→Depression, %d Depression→Loneliness, %d within-construct). ",
          s["n_sig01"], s["n_sig01_ld"], s["n_sig01_dl"], s["n_sig01_within"]),
  sprintf("Of the %d non-zero cross-lagged edges in the primary analysis, %d were retained in the full procedure; among the %d strongest edges in the primary analysis, %d were retained (%s). ",
          s["n_lasso_main"], s["n_both"], s["top_n"], s["top_kept"], drop_txt),
  sprintf("Following pruning, the sum of edge weights from Loneliness to Depression was %s, and from Depression to Loneliness was %s (compared to %s and %s in the primary analysis).",
          f(s["ld_full"]), f(s["dl_full"]), f(s["ld_lasso"]), f(s["dl_lasso"])))
txt <- c(
  "## Results (Draft with Programmatically Inserted Values)", "",
  sprintf("The cross-lagged panel network comprised 9 nodes, yielding %d non-zero cross-lagged edges out of 72 possible directed edges. Autoregressive edges ranged from %s to %s.",
          sum(CL != 0), f(min(diag(B))), f(max(diag(B)))),
  sprintf("The three strongest cross-lagged edges were: T1 '%s' → T2 '%s' (β = %s), T1 '%s' → T2 '%s' (β = %s), and T1 '%s' → T2 '%s' (β = %s).",
          item_en[el$from[1]], item_en[el$to[1]], f(el$weight[1]), item_en[el$from[2]], item_en[el$to[2]], f(el$weight[2]),
          item_en[el$from[3]], item_en[el$to[3]], f(el$weight[3])),
  sprintf("The sum of edge weights from Loneliness to Depression was %s, whereas that from Depression to Loneliness was %s.",
          f(sum(CL[1:4, 5:9])), f(sum(CL[5:9, 1:4]))),
  sprintf("The node with the highest out-expected influence was '%s' (out-EI = %s), and the node with the highest in-expected influence was '%s' (in-EI = %s).",
          cen$label[which.max(cen$outEI)], f(max(cen$outEI)), cen$label[which.max(cen$inEI)], f(max(cen$inEI))),
  sprintf("Case-dropping bootstrap revealed that the CS-coefficient was %s for out-EI and %s for in-EI; %s",
          f(cs["outExpectedInfluence"]), f(cs["inExpectedInfluence"]),
          paste0(ifelse(min(cs) < .25, "centrality rankings with CS < 0.25 were not interpreted. ", "both reached acceptable stability levels. "),
                 paste0(sapply(names(cs)[abs(cs - .5) < diff(seq(0.05, 0.75, length.out = 10))[1]], function(k)
                   sprintf("The CS for %s was close to the 0.5 threshold (marginally stable; changing the random seed may shift it to an adjacent grid level), and its rank order should be interpreted with caution.",
                           ifelse(k == "inExpectedInfluence", "in-EI", "out-EI"))), collapse = ""))),
  sprintf("In sensitivity analyses, the edge-weight correlations between the primary analysis and networks estimated via lambda.1se, including covariates, and across T2→T3 were %s, respectively.",
          paste(fr(res$sens$r_with_main), collapse = ", ")),
  "", fp_par,
  "", "(Methodological Caveat: Observed-score CLPN conflates between-person and within-person effects; findings reflect predictive relationships rather than causal processes.)")
writeLines(txt, out("L10-3_results_draft.md"))
cat(txt, sep = "\n")
log_close()
