# =====================================================================
# L7-1.R  Model Logic of CLPN: Unpacking CLPM to the Item Level
#   (CLPN logic, 4-node toy example)
# 4 nodes -> 4 regression equations (one for each T2 node) -> 4x4 directed weight matrix
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L7-1_log.txt")
dat <- read_course_data()
four <- c("lone1", "lone3", "dep1", "dep2")
X <- scale(dat[, paste0(four, "_t1")]); Y <- scale(dat[, paste0(four, "_t2")])
B <- matrix(0, 4, 4, dimnames = list(four, four))   # Row = T1 predictor (from), Column = T2 outcome (to)
for (j in 1:4) {
  fit <- lm(Y[, j] ~ X)                             # Equation j: T2 node j ~ all T1 nodes
  B[, j] <- coef(fit)[-1]                           # Drop intercept, place into column j
  cat(sprintf("%s_T2 = %s\n", four[j],
              paste(sprintf("%+.2f*%s_T1", coef(fit)[-1], four), collapse = " ")))
}
cat("\nWeight matrix B (diagonal = autoregressive AR, off-diagonal = cross-lagged CL):\n"); print(round(B, 2))
cat("An 8-node CLPN: 8 regressions; up to 8*7 = 56 cross-lagged edges.\n")
CL <- B; diag(CL) <- 0
png_open("L7-1_toy_clpn.png", 1400, 1300)
qgraph(CL, directed = TRUE, edge.labels = TRUE, asize = 5, layout = "circle",
       groups = list(Loneliness = 1:2, Depression = 3:4), theme = "colorblind",
       title = "4-node CLPN (OLS, unregularized; autoregressions omitted)")
invisible(dev.off())
log_close()
