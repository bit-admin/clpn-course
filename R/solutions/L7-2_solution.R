# 练习答案 L7-2：估计矩阵 vs 总体目标值；lambda.min vs lambda.1se
source("R/_setup.R")
log_open("sol_L7-2_log.txt")
dat <- read_course_data(); Bt <- true_B(); off <- row(Bt) != col(Bt)
set.seed(2026); Bmin <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], "lambda.min")
set.seed(2026); B1se <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], "lambda.1se")
strong <- abs(Bt) >= .10 & off                         # 总体目标值中较强的交叉滞后边
cat("总体目标值中较强的 CL 边：\n")
print(data.frame(edge = paste(rownames(Bt)[row(Bt)[strong]], "→", colnames(Bt)[col(Bt)[strong]]),
                 true = Bt[strong], min = round(Bmin[strong], 3), `1se` = round(B1se[strong], 3)))
fp <- function(B) sum(B != 0 & abs(Bt) < .05 & off)
cat("假阳性（总体目标值 |β| < .05 却被估计为非零）：lambda.min =", fp(Bmin), "；lambda.1se =", fp(B1se), "\n")
cat("答：lambda.1se 选更大的 λ → 惩罚更强 → 网络更稀疏，假阳性更少但会漏掉弱边。\n",
    "B[\"dep3\",\"dep4\"] 表示 T1 dep3（睡眠问题）→ T2 dep4（疲乏）（行 = from，列 = to）：lambda.min 估计 =",
    round(Bmin["dep3", "dep4"], 3), "，总体目标值 =", round(Bt["dep3", "dep4"], 3), "\n")
log_close()
