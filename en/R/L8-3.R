# =====================================================================
# L8-3.R  Case-Dropping Bootstrap & CS-Coefficient
# (Case-dropping bootstrap & CS-coefficient)
# CS = maximum proportion of cases that can be dropped while retaining 95%
# confidence that centrality correlates with the original sample at r >= 0.7
# Benchmark guidelines: CS should not fall below 0.25, and preferably exceed 0.5
# (Epskamp, Borsboom & Fried, 2018)
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(glmnet) })
log_open("L8-3_log.txt")
dat <- read_course_data()
wide_items <- dat[, c(vars_t(1), vars_t(2))]
# Reproducibility: Parallel bootnet (nCores > 1) resamples across worker processes using unseeded RNGs,
# so results drift slightly across runs even with set.seed(). Therefore, we default to single-core (nCores = 1)
# where set.seed() guarantees exact reproducibility (about 5–7x slower).
# If you only want a quick run and do not need bitwise reproducibility, set to max(1, parallel::detectCores() - 1).
n_boots <- 1000; n_cores <- 1
clpn_fun <- function(data) {                       # Identical estimation function as in L8-2
  p <- ncol(data) / 2
  X <- scale(as.matrix(data[, 1:p])); Y <- scale(as.matrix(data[, (p + 1):(2 * p)]))
  B <- matrix(0, p, p)
  for (j in seq_len(p)) {
    cvfit <- glmnet::cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]
  }
  B
}
set.seed(2026)
net <- estimateNetwork(wide_items, default = "none", fun = clpn_fun, directed = TRUE, labels = items)

# ---- Course Code ----
set.seed(2026)
cd <- bootnet(net, nBoots = n_boots, type = "case", nCores = n_cores,
              statistics = c("outExpectedInfluence", "inExpectedInfluence"), verbose = FALSE)
cs <- corStability(cd); cat("\n")
saveRDS(cd, out("L8-3_casedrop.rds"))
write.csv(data.frame(statistic = names(cs), CS = round(cs, 3)), out("L8-3_CS.csv"), row.names = FALSE)
png_open("L8-3_casedrop.png", 1600, 1200)
suppressWarnings(print(plot(cd, statistics = c("outExpectedInfluence", "inExpectedInfluence"))))
invisible(dev.off())
# Evaluation guidelines have only two thresholds: 0.25 and 0.5 (Epskamp et al., 2018). CS values can only
# land on the grid of drop proportions (bootnet defaults to 10 levels from 0.05 to 0.75, spacing ~0.08).
# Therefore, when barely exceeding 0.5, note explicitly: varying the random seed may cause it to drop to the next level.
step <- diff(seq(0.05, 0.75, length.out = 10))[1]
for (k in names(cs)) {
  verdict <- if (cs[k] >= .5 + step) "stable (>= 0.5); centrality rankings can be interpreted" else if (cs[k] >= .5)
    "just reaches 0.5 (one grid step above cutoff): marginally stable; altering seed may drop to lower step; interpret rankings with caution" else if (cs[k] >= .25)
    "minimally acceptable (0.25-0.5); interpret rankings with caution" else "unstable (< 0.25); do not interpret rankings"
  cat(sprintf("%-22s CS = %.2f -> %s\n", k, cs[k], verdict))
}
log_close()
