# Solution L6-2: Exercise 2 (adding direct effect of insomnia -> poor concentration)
# and Exercise 3 (counting edges on course data)
source("R/_setup.R")
log_open("sol_L6-2_log.txt")
pcor_of <- function(d) { P <- -cov2cor(solve(cor(d))); diag(P) <- 1; P }
set.seed(62); n <- 1000                        # Same seed and structure as R/L6-2.R
insomnia <- rnorm(n); fatigue <- 0.6 * insomnia + rnorm(n, 0, .8)
poor_conc <- 0.6 * fatigue + 0.3 * insomnia + rnorm(n, 0, .8)   # Exercise 2: Add direct effect of 0.3
d <- data.frame(insomnia, fatigue, poor_conc)
cat("Correlation:\n"); print(round(cor(d), 2))
cat("Partial correlation:\n"); print(round(pcor_of(d), 2))
cat("-> Insomnia-poor_conc partial correlation =", round(pcor_of(d)[1, 3], 2), "(no longer ≈ 0: a direct edge appears)\n\n")
# Exercise 3: 9 items at T1 from course data
x <- read_course_data()[, vars_t(1)]
R <- cor(x); P <- -cov2cor(solve(R)); diag(P) <- 0
cat("Edges with |r| > 0.1 in correlation network:", sum(abs(R[upper.tri(R)]) > .1), "/ 36\n")
cat("Edges with |pr| > 0.1 in partial correlation network:", sum(abs(P[upper.tri(P)]) > .1), "/ 36\n")
same <- outer(c(rep(1, 4), rep(2, 5)), c(rep(1, 4), rep(2, 5)), "==")
cat("Of which within the same scale/construct:", sum((abs(P) > .1 & same)[upper.tri(P)]), "\n")
log_close()
