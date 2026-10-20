# Solution L8-3: Deciding how to report findings based on CS-coefficients (requires running L8-3.R first)
source("R/_setup.R")
need_output("L8-3_CS.csv", "R/L8-3.R")   # Prerequisite output check
need_output("L8-2_boot.rds", "R/L8-2.R")  # Parts 2 and 3 use the 1,000 non-parametric bootstrap replications saved in Lesson 8.2
log_open("sol_L8-3_log.txt")
cs <- read.csv(out("L8-3_CS.csv")); print(cs)
step <- diff(seq(0.05, 0.75, length.out = 10))[1]   # One step of bootnet's default drop proportion grid (~0.08)
for (i in seq_len(nrow(cs))) {
  metric <- cs[[1]][i]
  if (cs$CS[i] < .25) cat(sprintf(paste0("CS for %s = %.2f < 0.25: Example of downgraded statement — \"Centrality rankings for %s ",
    "become unstable after dropping a small proportion of cases; therefore, this study draws no conclusions regarding which node is 'most influential' ",
    "and provides only exploratory descriptions.\"\n"), metric, cs$CS[i], metric))
  else if (cs$CS[i] < .5) cat(sprintf("CS for %s = %.2f (0.25–0.5): Acceptable but sub-optimal; interpret rankings with caution; still use \"predict\" rather than \"influence/cause\".\n", metric, cs$CS[i]))
  else if (cs$CS[i] < .5 + step) cat(sprintf("CS for %s = %.2f: Barely reaches 0.5 (only one grid step above cutoff; varying the random seed may drop it to the next step): marginally stable; interpret rankings with caution; still use \"predict\" rather than \"influence/cause\".\n", metric, cs$CS[i]))
  else cat(sprintf("CS for %s = %.2f: Centrality rankings can be reported, but still use \"predict\" rather than \"influence/cause\".\n", metric, cs$CS[i]))
}

# ---- Part 2: Can we state that "the sum of edge weights from Loneliness -> Depression exceeds that of the reverse direction"? ----
# Downgraded statements often use construct-level sums. However, "exceeds" is a comparative claim that must be tested first:
# across the 1,000 bootstrap networks saved in Lesson 8.2, compute the difference = sum(B[Loneliness, Depression]) - sum(B[Depression, Loneliness])
# for each bootstrap sample, and examine the 2.5% and 97.5% quantiles of the difference distribution.
# Only if the interval excludes 0 can one state that "the sum of edge weights in the Loneliness -> Depression direction is greater than in the reverse direction";
# if it includes 0, one can only state that "no difference in the sum of edge weights between the two directions was detected".
# Note: LASSO shrinkage also operates here; this interval merely describes precision (Lesson 8.2), rather than serving as a strict 95% confidence interval.
boot <- readRDS(out("L8-2_boot.rds"))
dir_sums <- function(B) {
  dimnames(B) <- list(items, items)                 # Rows = T1 (from), columns = T2 (to)
  c(lone_to_dep = sum(B[lone_items, dep_items]), dep_to_lone = sum(B[dep_items, lone_items]))
}
s0 <- dir_sums(boot$sample$graph)
sb <- t(sapply(boot$boots, function(b) dir_sums(b$graph)))
d_b <- sb[, "lone_to_dep"] - sb[, "dep_to_lone"]
cat("\nConstruct-level sum of edge weights (original sample): Loneliness -> Depression =", round(s0["lone_to_dep"], 3),
    "; Depression -> Loneliness =", round(s0["dep_to_lone"], 3), "; Difference =", round(s0["lone_to_dep"] - s0["dep_to_lone"], 3), "\n")
cat("Bootstrap quantiles of difference (", length(d_b), " replications): 2.5% =", round(quantile(d_b, .025), 3),
    ", 97.5% =", round(quantile(d_b, .975), 3), "; Proportion of difference <= 0 =", round(mean(d_b <= 0), 3), "\n")
cat(if (quantile(d_b, .025) > 0) "Conclusion: Interval excludes 0; one may state that \"the sum of edge weights in the Loneliness -> Depression direction is greater than in the reverse direction\" (still a predictive relationship, not causal).\n"
    else "Conclusion: Interval includes 0; one can only state that \"no difference in the sum of edge weights between the two directions was detected\".\n")
# When summing signed weights, positive and negative edges can cancel out; to examine "overall connection strength" regardless of sign, one can replace sum() with sum(abs()) and recompute.

# ---- Part 3: Does bootnet's out/inExpectedInfluence exclude autoregressions? ----
# The out-EI / in-EI hand-calculated in Lesson 7.4 excludes autoregressions (the diagonal). Here we compare
# bootnet's values computed on the original sample against two hand-calculated versions: "diagonal excluded" vs. "diagonal retained";
# whichever column it matches reveals which convention bootnet adopts.
B0 <- boot$sample$graph; dimnames(B0) <- list(items, items)
CL0 <- B0; diag(CL0) <- 0
st <- boot$sampleTable
bn_out <- setNames(st$value[st$type == "outExpectedInfluence"], st$node1[st$type == "outExpectedInfluence"])[items]
bn_in  <- setNames(st$value[st$type == "inExpectedInfluence"],  st$node1[st$type == "inExpectedInfluence"])[items]
cmp <- data.frame(node = items,
                  bootnet_out = round(bn_out, 3), hand_out_noAR = round(rowSums(CL0), 3), hand_out_withAR = round(rowSums(B0), 3),
                  bootnet_in  = round(bn_in, 3),  hand_in_noAR  = round(colSums(CL0), 3), hand_in_withAR  = round(colSums(B0), 3))
cat("\nbootnet Expected Influence vs. hand calculation (noAR = autoregressions excluded, withAR = autoregressions retained):\n"); print(cmp, row.names = FALSE)
cat("bootnet out-EI matches hand calculation with autoregressions excluded:", isTRUE(all.equal(unname(bn_out), unname(rowSums(CL0)), tolerance = 1e-6)),
    "; in-EI matches:", isTRUE(all.equal(unname(bn_in), unname(colSums(CL0)), tolerance = 1e-6)), "\n")
log_close()
