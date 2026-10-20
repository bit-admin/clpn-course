# Solution L9-2 Exercise 3: Are the top 5 cross-lagged edges identical after controlling for covariates (gender, age)?
source("R/_setup.R")
log_open("sol_L9-2_log.txt")
dat <- read_course_data()
X <- dat[, vars_t(1)]; Y <- dat[, vars_t(2)]
set.seed(2026); B0 <- clpn_estimate(X, Y)
set.seed(2026); B1 <- clpn_estimate(X, Y, covariates = dat[, c("gender", "age")])
top5 <- function(B) { el <- edge_list(cl_only(B)); paste(el$from, "→", el$to)[1:5] }
print(data.frame(`Primary analysis` = top5(B0), `With covariates` = top5(B1), check.names = FALSE))
off <- matrix(TRUE, 9, 9); diag(off) <- FALSE
cat("Are the top 5 edges identical:", identical(top5(B0), top5(B1)),
    "; CL edge weight correlation r =", round(cor(B0[off], B1[off]), 3), "; Maximum difference =", round(max(abs(B0[off] - B1[off])), 3), "\n")
log_close()
