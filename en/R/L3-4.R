# =====================================================================
# L3-4.R  Introduction to logistic regression (odds ratio, OR)
# Outcome is binary (0/1): whether professional help was sought at T2 (help_seek_t2)
# =====================================================================
source("R/_setup.R")
log_open("L3-4_log.txt")
dat <- read_course_data()
dat$dep_sum_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
fit <- glm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat, family = binomial)
print(summary(fit))
OR <- exp(cbind(OR = coef(fit), confint.default(fit)))   # exp(coefficients) = odds ratio
print(round(OR, 3))
cat("Interpretation: For each 1-point increase in depression sum score, the odds of seeking help are multiplied by", round(OR[2, 1], 2), ".\n")
cat("OR = 1.5 indicates a 50% increase in odds; OR = 0.67 (= 1/1.5) indicates an approximately 33% decrease in odds.\n")

# ---- 95% Wald intervals on the log-odds scale (lesson 'comparing with truth': whether covering true values 0.18 and 0.4) ----
cat("\n95% Wald intervals for coefficients (log-odds):\n")
print(round(confint.default(fit), 3))

# ---- Translating coefficients into probabilities: predicted probabilities across depression scores and gender ----
cat("\nPredicted probabilities (type = \"response\"):\n")
nd <- expand.grid(dep_sum_t2 = c(0, 5, 10, 15), gender = 0:1)
nd$p <- round(predict(fit, newdata = nd, type = "response"), 3)
print(nd)

# ---- Linear probability model (Exercise 3.4-D (1)): range of predicted values ----
lpm <- lm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat)
cat("\nRange of fitted values from linear probability model lm():\n")
print(round(range(fitted(lpm)), 2))

# ---- Logistic regression with LASSO: glmnet(family = \"binomial\") ----
# No random steps earlier in this script; set.seed(2026) fixes cross-validation folds
library(glmnet)
X <- scale(as.matrix(dat[, vars_t(1)]))      # 9 T1 items (standardized)
set.seed(2026)
cv <- cv.glmnet(X, dat$help_seek_t2, family = "binomial", nfolds = 10)
cat("\nglmnet logistic regression LASSO, coefficients at lambda.min:\n")
print(round(as.matrix(coef(cv, s = "lambda.min")), 3))
cat("Coefficients at lambda.1se:\n")
print(round(as.matrix(coef(cv, s = "lambda.1se")), 3))
cat("Number of non-zero coefficients (excluding intercept): lambda.min =", sum(coef(cv, s = "lambda.min")[-1] != 0),
    "; lambda.1se =", sum(coef(cv, s = "lambda.1se")[-1] != 0), "\n")
log_close()
