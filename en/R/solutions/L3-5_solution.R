# Exercise Solutions L3-5: 15 predictors, n = 150: lm() vs. cv.glmnet(), plotting coefficient paths (matches Lesson 3.5-A reference code)
source("R/_setup.R"); suppressPackageStartupMessages(library(glmnet))
log_open("sol_L3-5_log.txt")
set.seed(25)
n <- 150; p <- 15
X <- matrix(rnorm(n * p), n, p, dimnames = list(NULL, paste0("x", 1:p)))
beta_true <- c(0.5, 0.4, 0.3, rep(0, p - 3))      # Only the first 3 variables have true effects
y <- drop(X %*% beta_true + rnorm(n))
fit_ols <- lm(y ~ X); ols <- coef(fit_ols)[-1]
cvfit <- cv.glmnet(X, y, alpha = 1, nfolds = 10)
las   <- coef(cvfit, s = "lambda.1se")[-1, 1]
las_min <- coef(cvfit, s = "lambda.min")[-1, 1]   # Default rule used in the course CLPN scripts
print(round(cbind(true = beta_true, OLS = ols, LASSO_min = las_min, LASSO_1se = las), 3))
cat("LASSO (lambda.1se) non-zero coefficient count =", sum(las != 0), "; Non-zero count among spurious variables =", sum(las[4:15] != 0), "\n")
cat("LASSO (lambda.min) non-zero coefficient count =", sum(las_min != 0), "; Non-zero count among spurious variables =", sum(las_min[4:15] != 0), "\n")
png_open("sol_L3-5_path.png"); plot(glmnet(X, y), xvar = "lambda", label = TRUE); invisible(dev.off())
# Description: As lambda increases -> all coefficients shrink toward 0; weak/spurious variables hit 0 first, leaving only the strongest predictors.
Xn <- matrix(rnorm(1000 * p), 1000, p); yn <- drop(Xn %*% beta_true + rnorm(1000))   # 1000 new individuals
cat(sprintf("Test data mean squared error: OLS %.3f, LASSO %.3f; OLS training error %.3f\n",
            mean((yn - cbind(1, Xn) %*% coef(fit_ols))^2), mean((yn - predict(cvfit, Xn, s = "lambda.1se"))^2),
            mean(residuals(fit_ols)^2)))

# Exercise 3.5-B: How lambda.min / lambda.1se vary with different seeds on course data
dat <- read_course_data()
Xc <- scale(as.matrix(dat[, vars_t(1)])); yc <- scale(rowSums(dat[, paste0(dep_items, "_t2")]))[, 1]
for (sd in 1:2) { set.seed(sd); cf <- cv.glmnet(Xc, yc, alpha = 1, nfolds = 10); b <- coef(cf, s = "lambda.1se")[-1, 1]
  cat(sprintf("seed = %d: lambda.min = %.4f, lambda.1se = %.4f, non-zero coefficients under 1se: %d, lone1_t1 = %.3f\n", sd, cf$lambda.min, cf$lambda.1se, sum(b != 0), b["lone1_t1"])) }

# Exercise 3.5-C: Ridge regression (alpha = 0), using the same data and seed 2026 as R/L3-5.R
set.seed(2026); cv_las   <- cv.glmnet(Xc, yc, alpha = 1, nfolds = 10)
set.seed(2026); cv_ridge <- cv.glmnet(Xc, yc, alpha = 0, nfolds = 10)
cat(sprintf("\n3.5-C: Ridge regression lambda.min = %.4f (LASSO lambda.min = %.4f)\n", cv_ridge$lambda.min, cv_las$lambda.min))
print(round(cbind(ridge_min = coef(cv_ridge, s = "lambda.min")[, 1],
                  lasso_min = coef(cv_las,   s = "lambda.min")[, 1]), 3))
b_r <- coef(cv_ridge, s = "lambda.min")[-1, 1]
cat("Ridge regression non-zero count under lambda.min =", sum(b_r != 0), "(out of 9); Under LASSO =",
    sum(coef(cv_las, s = "lambda.min")[-1, 1] != 0), "\n")
# Ridge regression shrinks but does not select: all 9 coefficients are non-zero (lone3 is very close to 0 but not 0).
log_close()
