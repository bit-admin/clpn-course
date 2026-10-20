# Solution L5-4 Exercise 3: Measurement intervals and cross-lagged effects
# (monthly autoregression 0.9, monthly cross-lagged effect 0.05)
source("R/_setup.R")
log_open("sol_L5-4_log.txt")
a <- 0.9; cl <- 0.05
A <- matrix(c(a, cl, 0, a), 2)                  # Monthly coefficient matrix [[a, 0], [c, a]]
cross <- function(d) { P <- diag(2); for (k in seq_len(d)) P <- P %*% A; P[2, 1] }
for (d in c(1, 3, 6, 12)) cat(sprintf("Interval %2d months: Matrix power yields %.3f; formula Delta*a^(Delta-1)*c = %.3f\n", d, cross(d), d * a^(d - 1) * cl))
cat(sprintf("Peak is around %.1f months (-1/ln(a)); maximum across months 1-24 occurs at month %d\n", -1 / log(a), which.max(sapply(1:24, cross))))
log_close()
