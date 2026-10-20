# 练习答案 L9-2 练习 3：加入协变量（性别、年龄）后最强 5 条交叉滞后边是否相同
source("R/_setup.R")
log_open("sol_L9-2_log.txt")
dat <- read_course_data()
X <- dat[, vars_t(1)]; Y <- dat[, vars_t(2)]
set.seed(2026); B0 <- clpn_estimate(X, Y)
set.seed(2026); B1 <- clpn_estimate(X, Y, covariates = dat[, c("gender", "age")])
top5 <- function(B) { el <- edge_list(cl_only(B)); paste(el$from, "→", el$to)[1:5] }
print(data.frame(主分析 = top5(B0), 加协变量 = top5(B1)))
off <- matrix(TRUE, 9, 9); diag(off) <- FALSE
cat("最强 5 条边是否完全相同：", identical(top5(B0), top5(B1)),
    "；CL 边权相关 r =", round(cor(B0[off], B1[off]), 3), "；最大差异 =", round(max(abs(B0[off] - B1[off])), 3), "\n")
log_close()
