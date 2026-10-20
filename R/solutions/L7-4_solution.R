# 练习答案 L7-4：哪一个构念更多地“预测”另一个？
source("R/_setup.R")
log_open("sol_L7-4_log.txt")
dat <- read_course_data()
set.seed(2026); CL <- cl_only(clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)]))
l2d <- CL[lone_items, dep_items]; d2l <- CL[dep_items, lone_items]
cat("孤独→抑郁：非零边", sum(l2d != 0), "条，总和", round(sum(l2d), 3), "\n")
cat("抑郁→孤独：非零边", sum(d2l != 0), "条，总和", round(sum(d2l), 3), "\n")
cat("与总体目标值对照：孤独→抑郁", round(sum(true_B()[lone_items, dep_items]), 3),
    "；抑郁→孤独", round(sum(true_B()[dep_items, lone_items]), 3), "\n")
cat("答：rowSums(CL) = out-EI，colSums(CL) = in-EI；不含自回归边是因为它们远大于 CL 边，会淹没差异。\n")
log_close()
