# =====================================================================
# L3-5.R  Overfitting and regularization: ridge, LASSO, and cross-validation
# The core engine of CLPN: cv.glmnet()
# =====================================================================
source("R/_setup.R")
library(glmnet)
log_open("L3-5_log.txt")
dat <- read_course_data()

# ---- Lesson code: predicting T2 depression total score from 9 T1 items ----
predictors <- vars_t(1)
dat$depress_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
X <- scale(as.matrix(dat[, predictors]))
y <- scale(dat$depress_t2)[, 1]
set.seed(2026)                                  # Cross-validation uses random fold splitting; set seed
cvfit <- cv.glmnet(X, y, alpha = 1, nfolds = 10) # alpha = 1 for LASSO; alpha = 0 for ridge
png_open("L3-5_cvplot.png"); plot(cvfit); invisible(dev.off())   # Cross-validation error across log(lambda)
cat("lambda.min =", signif(cvfit$lambda.min, 3), "; lambda.1se =", signif(cvfit$lambda.1se, 3), "\n")
print(round(cbind(lambda.min = coef(cvfit, s = "lambda.min")[, 1],
                  lambda.1se = coef(cvfit, s = "lambda.1se")[, 1],
                  OLS        = coef(lm(y ~ X))), 3))     # Many LASSO coefficients are exactly 0

# ---- Coefficient paths: as lambda increases, coefficients are shrunk to 0 ----
fit <- glmnet(X, y, alpha = 1)
png_open("L3-5_lasso_path.png"); plot(fit, xvar = "lambda", label = TRUE)
title("LASSO Coefficient Paths", line = 2.5); invisible(dev.off())
ridge <- glmnet(X, y, alpha = 0)
png_open("L3-5_ridge_path.png"); plot(ridge, xvar = "lambda", label = TRUE)
title("Ridge Regression Coefficient Paths (Do Not Reach 0)", line = 2.5); invisible(dev.off())
log_close()
