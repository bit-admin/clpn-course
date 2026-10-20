# =====================================================================
# L3-4.R  逻辑回归简介  (Logistic regression; odds ratio, OR)
# 结果变量是 0/1：T2 是否寻求专业帮助（help_seek_t2）
# =====================================================================
source("R/_setup.R")
log_open("L3-4_log.txt")
dat <- read_course_data()
dat$dep_sum_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
fit <- glm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat, family = binomial)
print(summary(fit))
OR <- exp(cbind(OR = coef(fit), confint.default(fit)))   # exp(系数) = 比值比 odds ratio
print(round(OR, 3))
cat("解读：抑郁总分每高 1 分，求助的“发生比”（odds）乘以", round(OR[2, 1], 2), "。\n")
cat("OR = 1.5 表示发生比增加 50%；OR = 0.67（=1/1.5）表示发生比降低约 33%。\n")

# ---- 对数几率尺度上的 95% Wald 区间（讲义“和真相对照”：是否覆盖真值 0.18 与 0.4）----
cat("\n系数（log-odds）的 95% Wald 区间：\n")
print(round(confint.default(fit), 3))

# ---- 把系数翻译成概率：不同抑郁分与性别的预测概率 ----
cat("\n预测概率（type = \"response\"）：\n")
nd <- expand.grid(dep_sum_t2 = c(0, 5, 10, 15), gender = 0:1)
nd$p <- round(predict(fit, newdata = nd, type = "response"), 3)
print(nd)

# ---- 线性概率模型（练习 3.4-D (1)）：预测值的范围 ----
lpm <- lm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat)
cat("\n线性概率模型 lm() 的预测值范围：\n")
print(round(range(fitted(lpm)), 2))

# ---- 带 LASSO 的逻辑回归：glmnet(family = "binomial") ----
# 本脚本前面没有随机步骤；set.seed(2026) 固定交叉验证的分组
library(glmnet)
X <- scale(as.matrix(dat[, vars_t(1)]))      # 9 道 T1 题目（标准化）
set.seed(2026)
cv <- cv.glmnet(X, dat$help_seek_t2, family = "binomial", nfolds = 10)
cat("\nglmnet 逻辑回归 LASSO，lambda.min 的系数：\n")
print(round(as.matrix(coef(cv, s = "lambda.min")), 3))
cat("lambda.1se 的系数：\n")
print(round(as.matrix(coef(cv, s = "lambda.1se")), 3))
cat("非零系数个数（不含截距）：lambda.min =", sum(coef(cv, s = "lambda.min")[-1] != 0),
    "；lambda.1se =", sum(coef(cv, s = "lambda.1se")[-1] != 0), "\n")
log_close()
