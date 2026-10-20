# =====================================================================
# L9-2.R  Critical Appraisal: Are Conclusions Sensitive to Analytical Decisions?
#         (Sensitivity / robustness checks)
# Examining 3 "researcher degrees of freedom":
#   λ selection rules (lambda.min / lambda.1se / EBIC), random seeds, and item redundancy (topological overlap)
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(networktools))
log_open("L9-2_log.txt")
dat <- read_course_data()
X <- dat[, vars_t(1)]; Y <- dat[, vars_t(2)]
off <- matrix(TRUE, 9, 9); diag(off) <- FALSE
rules <- c("lambda.min", "lambda.1se", "ebic")
Bs <- lapply(rules, function(r) { set.seed(2026); clpn_estimate(X, Y, rule = r) }); names(Bs) <- rules
summ <- t(sapply(Bs, function(B) {
  CL <- cl_only(B); el <- edge_list(CL)
  c(CL_edges = sum(CL != 0), strongest_edge = paste(el$from[1], "→", el$to[1]),
    highest_outEI = names(which.max(rowSums(CL))), highest_inEI = names(which.max(colSums(CL))))
}))
print(summ)

# Random seeds: cv.glmnet splits folds randomly — do edges change across 20 random seeds?
seeds <- 1:20
arr <- sapply(seeds, function(s) { set.seed(s); clpn_estimate(X, Y)[off] })
nz <- rowMeans(arr != 0)
cat("\nAcross 20 random seeds: always non-zero CL edges =", sum(nz == 1),
    "; always 0 =", sum(nz == 0),
    "; intermittent =", sum(nz > 0 & nz < 1), "\n")
cat("→ Reports must explicitly state the random seed; repeated CV can also be used to mitigate randomness.\n")

# Item redundancy: goldbricker() identifies item pairs with highly overlapping content/correlation profiles
gb <- goldbricker(dat[, vars_t(1)], p = 0.05, method = "hittner2003", threshold = 0.25, corMin = 0.5, progressbar = FALSE)
cat("\nPotentially redundant item pairs (goldbricker):\n"); print(gb$suggested_reductions)
log_close()
