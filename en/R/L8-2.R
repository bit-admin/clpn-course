# =====================================================================
# L8-2.R  Edge-Weight Accuracy: Custom bootnet CLPN Estimator & Manual Bootstrap
# (Edge-weight accuracy: custom bootnet estimator & a manual bootstrap)
# ---------------------------------------------------------------------
# Three refinements compared to preliminary course notes (verified with bootnet 1.6+):
#  (1) The custom estimation function must not rely on global variables (e.g., t1_vars);
#      when running in parallel (nCores > 1), child processes cannot see them.
#      Here we structure data such that the first p columns = T1 and the next p columns = T2,
#      and explicitly call glmnet::cv.glmnet.
#  (2) Data passed to estimateNetwork() contains only 2p columns (T1 items + T2 items in identical order),
#      and labels provides only p node names; the returned matrix must be p x p.
#  (3) bootnet() must explicitly specify statistics = c("edge", "outExpectedInfluence", "inExpectedInfluence");
#      otherwise out-EI and in-EI for directed networks will not be saved.
# Runtime: 1,000 replications x 9 cv.glmnet runs; single-core takes ~7–15 min (depending on hardware,
# including difference tests and manual bootstrap). For initial practice, n_boots can be set to 200.
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(glmnet); library(qgraph) })
log_open("L8-2_log.txt")
dat <- read_course_data()
wide_items <- dat[, c(vars_t(1), vars_t(2))]      # 18 columns: first 9 columns T1, next 9 columns T2
labs <- items
n_boots <- 1000
# Reproducibility: Parallel bootnet (nCores > 1) resamples across worker processes using unseeded RNGs,
# so results drift slightly across runs even with set.seed(). Therefore, we default to single-core (nCores = 1)
# where set.seed() guarantees exact reproducibility (about 5–7x slower).
# If you only want a quick run and do not need bitwise reproducibility, set to max(1, parallel::detectCores() - 1).
n_cores <- 1

# ---- Custom Estimator (clpn_fun) ----
clpn_fun <- function(data) {
  p <- ncol(data) / 2                              # Number of nodes = half the number of columns
  X <- scale(as.matrix(data[, 1:p]))               # T1
  Y <- scale(as.matrix(data[, (p + 1):(2 * p)]))   # T2
  B <- matrix(0, p, p)
  for (j in seq_len(p)) {
    cvfit <- glmnet::cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]
  }
  B                                                # Rows = T1 (from), columns = T2 (to)
}
set.seed(2026)
net <- estimateNetwork(wide_items, default = "none", fun = clpn_fun,
                       directed = TRUE, labels = labs)
B_hat <- net$graph; dimnames(B_hat) <- list(labs, labs)
cat("Estimated network (identical method and seed as L7-2; produces identical results):\n"); print(round(B_hat, 2))

set.seed(2026)
boot <- bootnet(net, nBoots = n_boots, type = "nonparametric", nCores = n_cores,
                statistics = c("edge", "outExpectedInfluence", "inExpectedInfluence"),
                verbose = FALSE)
saveRDS(boot, out("L8-2_boot.rds"))

# ---- Bootstrap Interval Plot for Edge Weights ----
png_open("L8-2_edge_ci.png", 1600, 3200)
print(plot(boot, statistics = "edge", order = "sample", labels = TRUE, plot = "area",
           CIstyle = "quantiles"))
invisible(dev.off())
# Inspect cross-lagged edges only: extract from summary
s <- summary(boot, statistics = "edge")
s <- as.data.frame(s)
s_cl <- s[s$node1 != s$node2, c("node1", "node2", "sample", "mean", "q2.5", "q97.5", "prop0")]
s_cl <- s_cl[order(-abs(s_cl$sample)), ]
cat("\nBootstrap intervals for top 10 cross-lagged edges (q2.5–q97.5 percentiles; prop0 = proportion shrunk to 0):\n")
print(head(s_cl, 10), row.names = FALSE, digits = 3)
write.csv(s_cl, out("L8-2_cl_edge_boot.csv"), row.names = FALSE)

# ---- Bootstrapped Edge-Weight Difference Test ----
top5 <- head(s_cl, 5); top5_id <- paste0(top5$node1, "->", top5$node2)
png_open("L8-2_edge_difference.png", 1800, 1800)
suppressWarnings(print(plot(boot, "edge", plot = "difference", onlyNonZero = TRUE, order = "sample")))
invisible(dev.off())
cat("\nDifference tests between the top 5 CL edges (TRUE = 95% bootstrap interval excludes 0):\n")
dt <- differenceTest(boot, top5_id, top5_id, measure = "edge")
print(dt[dt$id1 < dt$id2, c("id1", "id2", "lower", "upper", "significant")], row.names = FALSE)

# ---- Manual Bootstrap (Package-free to clarify principles; default 200 replications) ----
set.seed(82)
n <- nrow(wide_items); manual_B <- 200
boot_arr <- array(NA, c(9, 9, manual_B), dimnames = list(labs, labs, NULL))
for (b in 1:manual_B) {
  idx <- sample(n, n, replace = TRUE)                    # Resample cases with replacement
  boot_arr[, , b] <- clpn_fun(wide_items[idx, ])         # Re-estimate the entire CLPN on the bootstrap sample
}
lo <- apply(boot_arr, c(1, 2), quantile, .025); hi <- apply(boot_arr, c(1, 2), quantile, .975)
cat("\nManual bootstrap (", manual_B, " replications): lone3 → dep1 interval = [",
    round(lo["lone3", "dep1"], 3), ",", round(hi["lone3", "dep1"], 3), "]; ",
    "proportion shrunk to 0 =", mean(boot_arr["lone3", "dep1", ] == 0), "\n")
cat("Note: LASSO penalizes coefficients toward 0 (shrinkage), so these intervals are not strict\n",
    "95% confidence intervals, but rather serve as reference indices for estimation precision (Epskamp et al., 2018).\n")
log_close()
