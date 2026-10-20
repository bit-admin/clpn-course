# =====================================================================
# L7-2.R  用 glmnet 逐节点估计 CLPN  (Nodewise LASSO estimation of a CLPN)
# 方法：应用研究中常见的“仅 LASSO”CLPN（如 Funkhouser et al., 2021）—— 对每个 T2 题目，
#       用所有 T1 题目做 LASSO 回归（cv.glmnet），系数直接拼成有向网络 B。
#       这相当于 Wysocki et al.（2025）完整流程的第 1 步（选边）；SEM 重估等后续步骤见 R/L7-5b.R。
# =====================================================================
source("R/_setup.R")
library(glmnet)
log_open("L7-2_log.txt")
dat <- read_course_data()
d1 <- dat[, vars_t(1)]                 # T1 题目
d2 <- dat[, vars_t(2)]                 # T2 题目（同样顺序！）

# ---- 课件代码（逐行解释）----
X <- scale(as.matrix(d1))              # 标准化：系数才可比（标准化系数）
Y <- scale(as.matrix(d2))
p <- ncol(X); labs <- sub("_t1", "", colnames(X))
B <- matrix(0, p, p, dimnames = list(labs, labs))  # 行 = T1 预测变量，列 = T2 结果变量
set.seed(2026)                         # cv.glmnet 随机分折 → 设种子保证可重复
for (j in seq_len(p)) {                # 对每个 T2 节点 j 做一次回归
  cvfit <- cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
  B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]  # 去掉截距
}
AR <- diag(B)                          # 自回归边
CL <- B; diag(CL) <- 0                 # 交叉滞后边
cat("估计的 B（lambda.min）：\n"); print(round(B, 2))

# ---- 与已知答案比较（模拟数据的好处）----
# 课程数据有两种“真值”，不是同一个矩阵：
#   总体目标值 data/true_B_population.csv：标准 CLPN 在样本无限大时收敛到的系数，含稳定特质造成的部分；
#   被试内真值 data/true_B_within.csv：生成数据时用的被试内滞后系数。
# CLPN 的总体目标 ≠ 被试内过程。下面先对照总体目标值，脚本末尾再对照被试内真值。
Bt <- true_B()
cat("\n总体目标值（data/true_B_population.csv，标准 CLPN 在样本无限大时的目标）：\n"); print(round(Bt, 2))
compare <- function(Best, Btrue, thr = 0.05) {
  # 把 |Btrue| ≥ thr 视为“应当找回的边”。对总体目标值用 0.05（总体矩阵里没有恰好为 0 的格子，
  # 0.05 是人为的门槛；同构念内由稳定特质造成的 0.05–0.07 的小边也会被算进来）。
  te <- abs(Btrue) >= thr; ee <- Best != 0; off <- row(Best) != col(Best)
  c(真实CL边 = sum(te & off), 找回 = sum(te & ee & off), 漏掉 = sum(te & !ee & off),
    假阳性 = sum(!te & ee & off), 估计CL边总数 = sum(ee & off),
    与真值相关 = round(cor(Best[off], Btrue[off]), 3))
}
set.seed(2026); B_1se  <- clpn_estimate(d1, d2, rule = "lambda.1se")
B_ebic <- clpn_estimate(d1, d2, rule = "ebic")
tab <- rbind(lambda.min = compare(B, Bt), lambda.1se = compare(B_1se, Bt), EBIC = compare(B_ebic, Bt))
cat("\n方法表现（对照总体目标值，只看交叉滞后边）：\n"); print(tab)
cat("lambda.1se 与 EBIC 更稀疏：假阳性更少，但可能漏掉总体目标中的弱边。\n")
cat("提醒：B[\"lone3\", \"dep1\"] =", round(B["lone3", "dep1"], 3), "表示 T1 与人隔绝 → T2 情绪低落。\n")

write.csv(round(B, 4), out("L7-2_B_lambda_min.csv"))
write.csv(round(B_1se, 4), out("L7-2_B_lambda_1se.csv"))
write.csv(edge_list(B), out("L7-2_edgelist.csv"), row.names = FALSE)
saveRDS(B, out("L7-2_B.rds"))
png_open("L7-2_est_vs_true.png", 2400, 1200)
off <- row(B) != col(B)
Bw <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))[labs, labs]   # 被试内真值
par(mfrow = c(1, 2))
plot(Bt[off], B[off], pch = 16, col = ifelse(B[off] == 0, "grey60", "blue"),
     xlab = "总体目标值 population target", ylab = "估计系数 estimated (lambda.min)",
     main = "交叉滞后边：估计 vs 总体目标值")
abline(0, 1, lty = 2); abline(h = 0, v = 0, col = "grey")
plot(Bw[off], B[off], pch = 16, col = ifelse(B[off] == 0, "grey60", "blue"),
     xlab = "被试内真值 within-person lag", ylab = "估计系数 estimated (lambda.min)",
     main = "交叉滞后边：估计 vs 被试内真值")
abline(0, 1, lty = 2); abline(h = 0, v = 0, col = "grey")
invisible(dev.off())

# ---- 两种真值下的找回情况：总体目标值 vs 被试内真值 ----
cat("\n被试内真值（data/true_B_within.csv，生成数据时用的被试内滞后系数）：\n"); print(round(Bw, 2))
tgt <- abs(Bt) >= 0.05 & off                       # 总体目标值中的“边”
win <- Bw != 0 & off                               # 被试内真值中的边（非零即为边）
trait <- tgt & !win                                # 只在总体目标中出现：稳定特质造成的边
same_con <- outer(sub("\\d$", "", labs), sub("\\d$", "", labs), "==")   # 同一构念（lone / dep）
cat("\n总体目标值中 |β| ≥ 0.05 的交叉滞后边", sum(tgt), "条 = 被试内真值中也有的", sum(tgt & win),
    "条 + 被试内真值中为 0 的", sum(trait), "条\n")
cat("后", sum(trait), "条中同构念边", sum(trait & same_con), "条；绝对值范围",
    sprintf("%.3f", min(abs(Bt[trait]))), "–", sprintf("%.3f", max(abs(Bt[trait]))), "\n")
cat("被试内真值中的边，有", sum(win & !tgt), "条在总体目标值中低于 0.05\n")
B_ebic_r <- B_ebic; dimnames(B_ebic_r) <- dimnames(B)
rules <- list(lambda.min = B, lambda.1se = B_1se, EBIC = B_ebic_r)
rec <- do.call(rbind, lapply(names(rules), function(r) {
  Bh <- rules[[r]]
  one <- function(truth, Btrue, thr) {
    v <- compare(Bh, Btrue, thr)
    data.frame(rule = r, truth = truth, n_true = v[[1]], hit = v[[2]], miss = v[[3]], fp = v[[4]],
               n_est = v[[5]], r = v[[6]], trait_hit = sum(Bh != 0 & trait))
  }
  rbind(one("population", Bt, 0.05), one("within", Bw, 1e-8))
}))
cat("\n两种真值下的找回情况（只看交叉滞后边；population = 总体目标值 |β| ≥ 0.05，within = 被试内真值非零）：\n")
print(rec, row.names = FALSE)
cat("trait_hit = 估计为非零、且只在总体目标值中存在（被试内真值为 0）的边数。\n")
cat("对照被试内真值时，这些边全部算作假阳性：它们在总体中确实存在，但不是被试内过程。\n")
write.csv(rec, out("L7-2_recovery_two_truths.csv"), row.names = FALSE)
write.csv(round(B_ebic_r, 4), out("L7-2_B_ebic.csv"))
log_close()
