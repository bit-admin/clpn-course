# =====================================================================
# L0-2.R  Why Learn Cross-Lagged Panel Networks: A First Look at the "True Answers"
# (Why CLPN: a first look at the true within-person lag matrix)
# Code box from Lesson 0.2; if you have not installed R yet in Lesson 0.2,
# you can return to run this after installing R in Lesson 2.1.
# The second half ("Quick Run") requires 'glmnet' and 'qgraph'
# (see Lesson 0.2 page or Lesson 2.4 for installation instructions).
# To run: Open clpn-course.Rproj in RStudio, open this file, and click "Source".
# =====================================================================
source("R/_setup.R")
log_open("L0-2_log.txt")      # Console output is also saved to R/output/L0-2_log.txt

# The within-person lag structure programmed into the data simulation (data/simulate_data.R)
B <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))
print(B)                       # Rows = items at T1 (origin of arrow), Columns = items at T2 (destination of arrow)
cat("\nDiagonal: Autoregressions (each item T1 -> T2)\n")
print(diag(B))
CL <- B; diag(CL) <- 0         # Zero out the diagonal, leaving only cross-lagged edges
cat("\nWhich cross-lagged cells are non-zero? (row = origin, col = destination)\n")
print(which(CL != 0, arr.ind = TRUE))
cat("\n'Feeling isolated' T1 -> 'Depressed mood' T2:\n")
print(B["lone3", "dep1"])

# ---- Quick Run: Your First CLPN (run after installing R in Week 2, ~30 min; see Lesson 0.2 page for where each step is taught) ----
# Estimation code is identical to R/L7-3.R (same seed 2026, same lambda.min rule), so results match Lesson 7.3.
library(qgraph)
cat("\n==== Quick Run: First CLPN (T1 -> T2) ====\n")
dat <- read_course_data()                        # Load course simulated data (wide format, one row per participant)
X <- dat[, vars_t(1)]                            # 9 items at T1
Y <- dat[, vars_t(2)]                            # Same 9 items at T2 (same order)
set.seed(2026)                                   # Random CV fold split; set seed for reproducibility
B <- clpn_estimate(X, Y, rule = "lambda.min")    # Nodewise LASSO: regress each T2 item on all T1 items
cat("Estimated B (lambda.min):\n"); print(round(B, 2))
CL <- cl_only(B)                                 # Remove diagonal (autoregressions), keeping cross-lagged edges only
cat("\nNon-zero cells among 72 cross-lagged edges: ", sum(CL != 0), "\n", sep = "")
el <- edge_list(CL)                              # Edge list sorted by |weight| descending
el$from_en <- item_en[el$from]; el$to_en <- item_en[el$to]
cat("\nTop 10 strongest cross-lagged edges:\n"); print(head(el, 10), row.names = FALSE, digits = 3)
png_open("L0-2_quick_clpn.png", 1800, 1500)
qgraph(CL, directed = TRUE, layout = "spring",
       labels = rownames(B), groups = groups_list,
       theme = "colorblind", asize = 4, legend = TRUE,
       nodeNames = item_en[rownames(B)], legend.cex = 0.45,
       title = "My First CLPN (T1 -> T2), lambda.min; autoregressive edges omitted")
invisible(dev.off())
log_close()
