# Solution L7-4: Which construct more strongly "predicts" the other?
source("R/_setup.R")
log_open("sol_L7-4_log.txt")
dat <- read_course_data()
set.seed(2026); CL <- cl_only(clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)]))
l2d <- CL[lone_items, dep_items]; d2l <- CL[dep_items, lone_items]
cat("Loneliness -> Depression: non-zero edges =", sum(l2d != 0), ", sum =", round(sum(l2d), 3), "\n")
cat("Depression -> Loneliness: non-zero edges =", sum(d2l != 0), ", sum =", round(sum(d2l), 3), "\n")
cat("Comparison with population target: Loneliness -> Depression =", round(sum(true_B()[lone_items, dep_items]), 3),
    "; Depression -> Loneliness =", round(sum(true_B()[dep_items, lone_items]), 3), "\n")
cat("Answer: rowSums(CL) = out-EI, colSums(CL) = in-EI; autoregressive edges are excluded because they are much larger than CL edges and would mask cross-lagged differences.\n")
log_close()
