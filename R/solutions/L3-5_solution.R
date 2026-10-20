# 练习答案 L3-5：15 个预测变量、n = 150：lm() vs cv.glmnet()，画系数路径（与课件 3.5-A 参考代码一致）
source("R/_setup.R"); suppressPackageStartupMessages(library(glmnet))
log_open("sol_L3-5_log.txt")
set.seed(25)
n <- 150; p <- 15
X <- matrix(rnorm(n * p), n, p, dimnames = list(NULL, paste0("x", 1:p)))
beta_true <- c(0.5, 0.4, 0.3, rep(0, p - 3))      # 只有前 3 个变量真的有作用
y <- drop(X %*% beta_true + rnorm(n))
fit_ols <- lm(y ~ X); ols <- coef(fit_ols)[-1]
cvfit <- cv.glmnet(X, y, alpha = 1, nfolds = 10)
las   <- coef(cvfit, s = "lambda.1se")[-1, 1]
las_min <- coef(cvfit, s = "lambda.min")[-1, 1]   # 课程 CLPN 脚本默认用的规则
print(round(cbind(true = beta_true, OLS = ols, LASSO_min = las_min, LASSO_1se = las), 3))
cat("LASSO（lambda.1se）非零系数个数 =", sum(las != 0), "；假变量中的非零个数 =", sum(las[4:15] != 0), "\n")
cat("LASSO（lambda.min）非零系数个数 =", sum(las_min != 0), "；假变量中的非零个数 =", sum(las_min[4:15] != 0), "\n")
png_open("sol_L3-5_path.png"); plot(glmnet(X, y), xvar = "lambda", label = TRUE); invisible(dev.off())
# 描述：λ 增大 → 所有系数向 0 收缩，弱/假的变量最先变成 0，最后只剩最强的几个。
Xn <- matrix(rnorm(1000 * p), 1000, p); yn <- drop(Xn %*% beta_true + rnorm(1000))   # 1000 个新个体
cat(sprintf("新数据均方误差：OLS %.3f，LASSO %.3f；OLS 训练误差 %.3f\n",
            mean((yn - cbind(1, Xn) %*% coef(fit_ols))^2), mean((yn - predict(cvfit, Xn, s = "lambda.1se"))^2),
            mean(residuals(fit_ols)^2)))

# 练习 3.5-B：换随机种子，课程数据上的 λ.min / λ.1se 会怎样变化
dat <- read_course_data()
Xc <- scale(as.matrix(dat[, vars_t(1)])); yc <- scale(rowSums(dat[, paste0(dep_items, "_t2")]))[, 1]
for (sd in 1:2) { set.seed(sd); cf <- cv.glmnet(Xc, yc, alpha = 1, nfolds = 10); b <- coef(cf, s = "lambda.1se")[-1, 1]
  cat(sprintf("seed = %d：lambda.min = %.4f，lambda.1se = %.4f，1se 下非零系数 %d 个，lone1_t1 = %.3f\n", sd, cf$lambda.min, cf$lambda.1se, sum(b != 0), b["lone1_t1"])) }

# 练习 3.5-C：岭回归（alpha = 0），与 R/L3-5.R 相同的数据、相同的种子 2026
set.seed(2026); cv_las   <- cv.glmnet(Xc, yc, alpha = 1, nfolds = 10)
set.seed(2026); cv_ridge <- cv.glmnet(Xc, yc, alpha = 0, nfolds = 10)
cat(sprintf("\n3.5-C：岭回归 lambda.min = %.4f（LASSO lambda.min = %.4f）\n", cv_ridge$lambda.min, cv_las$lambda.min))
print(round(cbind(ridge_min = coef(cv_ridge, s = "lambda.min")[, 1],
                  lasso_min = coef(cv_las,   s = "lambda.min")[, 1]), 3))
b_r <- coef(cv_ridge, s = "lambda.min")[-1, 1]
cat("岭回归 lambda.min 下非零系数个数 =", sum(b_r != 0), "（共 9 个）；LASSO 下 =",
    sum(coef(cv_las, s = "lambda.min")[-1, 1] != 0), "\n")
# 岭回归只收缩、不筛选：9 个系数都不为 0（lone3 很接近 0 但不是 0）。
log_close()
