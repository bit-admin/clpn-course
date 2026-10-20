# =====================================================================
# L3-5.R  过拟合与正则化：岭回归、LASSO 与交叉验证
# (Overfitting & regularization: ridge, LASSO, cross-validation)
# 这是 CLPN 的核心工具：cv.glmnet()
# =====================================================================
source("R/_setup.R")
library(glmnet)
log_open("L3-5_log.txt")
dat <- read_course_data()

# ---- 课件代码：用 9 道 T1 题目预测 T2 抑郁总分 ----
predictors <- vars_t(1)
dat$depress_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
X <- scale(as.matrix(dat[, predictors]))
y <- scale(dat$depress_t2)[, 1]
set.seed(2026)                                  # 交叉验证会随机分组，所以要设种子
cvfit <- cv.glmnet(X, y, alpha = 1, nfolds = 10) # alpha = 1 即 LASSO；alpha = 0 即岭回归 ridge
png_open("L3-5_cvplot.png"); plot(cvfit); invisible(dev.off())   # 交叉验证误差随 log(λ) 变化
cat("lambda.min =", signif(cvfit$lambda.min, 3), "；lambda.1se =", signif(cvfit$lambda.1se, 3), "\n")
print(round(cbind(lambda.min = coef(cvfit, s = "lambda.min")[, 1],
                  lambda.1se = coef(cvfit, s = "lambda.1se")[, 1],
                  OLS        = coef(lm(y ~ X))), 3))     # 很多 LASSO 系数恰好为 0

# ---- 系数路径图（coefficient path）：λ 增大，系数逐渐被压到 0 ----
fit <- glmnet(X, y, alpha = 1)
png_open("L3-5_lasso_path.png"); plot(fit, xvar = "lambda", label = TRUE)
title("LASSO 系数路径", line = 2.5); invisible(dev.off())
ridge <- glmnet(X, y, alpha = 0)
png_open("L3-5_ridge_path.png"); plot(ridge, xvar = "lambda", label = TRUE)
title("岭回归系数路径（不会变成 0）", line = 2.5); invisible(dev.off())
log_close()
