# Exercise Solutions L3-4: Logistic regression and odds ratios (OR)
#   3.4-A: help_seek_t2 ~ T2 depression sum score + gender; interpreting gender OR
#   3.4-B: Adding T1 loneliness sum score; predicted probabilities for two women (T2 depression = 5, loneliness = 6 vs. 12)
#   3.4-C: Probability and odds conversions (paper-and-pencil exercise, verified with R)
#   3.4-D: Linear probability model fitted value range; lambda.min and lambda.1se in glmnet(family = "binomial")
source("R/_setup.R")
log_open("sol_L3-4_log.txt")
dat <- read_course_data()
dat$dep_sum_t2  <- rowSums(dat[, paste0(dep_items, "_t2")])
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])

# ---- 3.4-A ----
fit <- glm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat, family = binomial)
cat("3.4-A: OR and 95% Wald CI\n")
print(round(exp(cbind(OR = coef(fit), confint.default(fit))), 3))
cat("Gender p =", signif(summary(fit)$coefficients["gender", 4], 3), "\n")
# (1) Controlling for T2 depression, the odds of women seeking professional help are approximately 1.89 times those of men.
# (2) OR = 1.5: odds increase by 50%; OR = 0.67: odds become 0.67 times the baseline (approx 33% reduction); the two are reciprocals.

# ---- 3.4-B ----
fit2 <- glm(help_seek_t2 ~ dep_sum_t2 + gender + lone_sum_t1, data = dat, family = binomial)
cat("\n3.4-B: OR and 95% Wald CI after adding T1 loneliness sum score\n")
print(round(exp(cbind(OR = coef(fit2), confint.default(fit2))), 3))
cat("Loneliness p =", round(summary(fit2)$coefficients["lone_sum_t1", 4], 3), "\n")
p_two <- predict(fit2, newdata = data.frame(dep_sum_t2 = 5, gender = 1, lone_sum_t1 = c(6, 12)), type = "response")
cat("Predicted probabilities for two women (T2 depression = 5) with loneliness 6 vs. 12: ", round(p_two, 3), "\n")
# In the simulated data, help-seeking was generated solely from depression and gender; controlling for them leaves loneliness with virtually no additional predictive power.

# ---- 3.4-C ----
p <- c(0.05, 0.25, 0.6)
cat("\n3.4-C: Probability", p, "-> Odds", round(p / (1 - p), 4), "\n")
o <- c(0.5, 4)
cat("Odds", o, "-> Probability", round(o / (1 + o), 3), "\n")

# ---- 3.4-D (1) Linear probability model ----
lpm <- lm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat)
cat("\n3.4-D (1): Linear probability model predicted value range", round(range(fitted(lpm)), 2), "\n")
# Happened not to exceed [0, 1] bounds here; however, extrapolating to higher depression scores can yield values > 1; the true relation is sigmoidal and residual variance changes with fitted values -> logistic regression recommended.

# ---- 3.4-D (2) Binary classification with glmnet: same code and seed as R/L3-4.R ----
library(glmnet)
X <- scale(as.matrix(dat[, vars_t(1)]))
set.seed(2026)
cv <- cv.glmnet(X, dat$help_seek_t2, family = "binomial", nfolds = 10)
b_min <- coef(cv, s = "lambda.min")[-1, 1]; b_1se <- coef(cv, s = "lambda.1se")[-1, 1]
cat("\n3.4-D (2): Non-zero items under lambda.min: ", names(b_min)[b_min != 0], "(total of", sum(b_min != 0), "items)\n")
cat("Count of non-zero items under lambda.1se: ", sum(b_1se != 0), "\n")
log_close()
