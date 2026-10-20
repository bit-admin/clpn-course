# =====================================================================
# L6-3.R  Regularized Network Estimation: EBICglasso and Hyperparameter gamma
#   (Regularized GGM, gamma)
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(qgraph) })
log_open("L6-3_log.txt")
dat <- read_course_data()
items_t1 <- dat[, vars_t(1)]; names(items_t1) <- items
res <- data.frame()
nets <- list()
# Note: When N = 800 is relatively large, EBICglasso may warn "A dense regularized network was selected"
# (the selected lambda is very small -> network is relatively dense). This is a warning rather than an error, suppressed below with suppressWarnings().
for (g in c(0, 0.25, 0.5)) {
  net <- suppressWarnings(estimateNetwork(items_t1, default = "EBICglasso", tuning = g,
                         corMethod = "cor_auto", verbose = FALSE))  # cor_auto: ordinal items -> polychoric correlations
  nets[[as.character(g)]] <- net
  res <- rbind(res, data.frame(gamma = g, edges = sum(net$graph[upper.tri(net$graph)] != 0)))
}
print(res)
# In the course data, associations among loneliness items and depression items are strong, so the 3 gammas may select identical networks.
# Below, we use simulated data with a known true network, weaker edges, and n = 150, where the effect of gamma is more apparent:
set.seed(63)
tn <- genGGM(12, p = 0.2, nei = 1, propPositive = 0.8, constant = 1.5)   # True network (12 edges)
Xs <- ggmGenerator()(150, tn)
cat("True number of edges in simulated data =", sum(tn[upper.tri(tn)] != 0), "\n")
for (g in c(0, 0.25, 0.5)) {
  ns <- suppressWarnings(estimateNetwork(Xs, default = "EBICglasso", tuning = g, verbose = FALSE))
  est <- ns$graph[upper.tri(ns$graph)] != 0; tru <- tn[upper.tri(tn)] != 0
  cat("gamma =", g, ": estimated edges =", sum(est), "; false positives =", sum(est & !tru), "\n")
}
cat("Larger gamma -> sparser network, fewer false-positive edges, but may also miss true weak edges.\n")
# Comparison: unregularized partial correlation network (dense with small edges)
pcor_full <- qgraph::getWmat(qgraph(cor_auto(items_t1, verbose = FALSE), graph = "pcor", DoNotPlot = TRUE))
cat("Number of non-zero edges in unregularized partial correlation network =", sum(abs(pcor_full[upper.tri(pcor_full)]) > 0), "/ 36\n")
png_open("L6-3_gamma.png", 2400, 900)
par(mfrow = c(1, 3)); L <- averageLayout(nets[[1]], nets[[2]], nets[[3]])
for (g in names(nets)) plot(nets[[g]], layout = L, groups = groups_list, maximum = 0.5,
                            legend = FALSE, title = paste("gamma =", g))
invisible(dev.off())
# Check: lambda selected by EBIC under each gamma, and its position in the lambda sequence (whether at minimum)
cat("\nLambda selected by EBIC (course data, N = 800):\n")
for (g in names(nets)) {
  r <- nets[[g]]$results
  if (!is.list(r) || is.null(r$lambda) || is.null(r$ebic))  # Recompute if bootnet didn't save full results
    r <- qgraph::EBICglasso(cor_auto(items_t1, verbose = FALSE), n = nrow(items_t1),
                            gamma = as.numeric(g), returnAllResults = TRUE)
  lam <- r$lambda; i <- which.min(r$ebic)
  cat("gamma =", g, ": lambda =", signif(lam[i], 4), "; sequence of", length(lam), "lambdas (",
      signif(min(lam), 4), "–", signif(max(lam), 4), "), selected is #",
      rank(-lam)[i], "from largest to smallest; at minimum of sequence:", if (lam[i] == min(lam)) "Yes" else "No", "\n")
}
log_close()
