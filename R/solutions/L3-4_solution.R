# 练习答案 L3-4：逻辑回归与 OR
#   3.4-A：help_seek_t2 ~ T2 抑郁总分 + 性别，解释性别的 OR
#   3.4-B：再加入 T1 孤独总分；两名女性（T2 抑郁 5 分，孤独 6 vs 12）的预测概率
#   3.4-C：概率与几率互换（纸笔题，R 验算）
#   3.4-D：线性概率模型的预测值范围；glmnet(family = "binomial") 的 lambda.min 与 lambda.1se
source("R/_setup.R")
log_open("sol_L3-4_log.txt")
dat <- read_course_data()
dat$dep_sum_t2  <- rowSums(dat[, paste0(dep_items, "_t2")])
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])

# ---- 3.4-A ----
fit <- glm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat, family = binomial)
cat("3.4-A：OR 与 95% Wald CI\n")
print(round(exp(cbind(OR = coef(fit), confint.default(fit))), 3))
cat("性别 p =", signif(summary(fit)$coefficients["gender", 4], 3), "\n")
# (1) 控制 T2 抑郁后，女性寻求专业帮助的几率（odds）约为男性的 1.89 倍。
# (2) OR = 1.5：几率增加 50%；OR = 0.67：几率变为原来的 0.67 倍（约减少 33%），两者互为倒数。

# ---- 3.4-B ----
fit2 <- glm(help_seek_t2 ~ dep_sum_t2 + gender + lone_sum_t1, data = dat, family = binomial)
cat("\n3.4-B：加入 T1 孤独总分后的 OR 与 95% Wald CI\n")
print(round(exp(cbind(OR = coef(fit2), confint.default(fit2))), 3))
cat("孤独 p =", round(summary(fit2)$coefficients["lone_sum_t1", 4], 3), "\n")
p_two <- predict(fit2, newdata = data.frame(dep_sum_t2 = 5, gender = 1, lone_sum_t1 = c(6, 12)), type = "response")
cat("两名女性（T2 抑郁 5 分）孤独 6 分 vs 12 分的预测概率：", round(p_two, 3), "\n")
# 模拟数据中“是否求助”只由抑郁和性别生成，所以控制它们之后孤独感几乎没有额外预测力。

# ---- 3.4-C ----
p <- c(0.05, 0.25, 0.6)
cat("\n3.4-C：概率", p, "→ 几率", round(p / (1 - p), 4), "\n")
o <- c(0.5, 4)
cat("几率", o, "→ 概率", round(o / (1 + o), 3), "\n")

# ---- 3.4-D (1) 线性概率模型 ----
lpm <- lm(help_seek_t2 ~ dep_sum_t2 + gender, data = dat)
cat("\n3.4-D (1)：线性概率模型的预测值范围", round(range(fitted(lpm)), 2), "\n")
# 碰巧没越界；但外推到更高的抑郁分可能 > 1，真实关系是 S 形，残差方差随预测值变化 → 推荐逻辑回归。

# ---- 3.4-D (2) glmnet 的二分类版本：与 R/L3-4.R 相同的代码与种子 ----
library(glmnet)
X <- scale(as.matrix(dat[, vars_t(1)]))
set.seed(2026)
cv <- cv.glmnet(X, dat$help_seek_t2, family = "binomial", nfolds = 10)
b_min <- coef(cv, s = "lambda.min")[-1, 1]; b_1se <- coef(cv, s = "lambda.1se")[-1, 1]
cat("\n3.4-D (2)：lambda.min 非零的题目：", names(b_min)[b_min != 0], "（共", sum(b_min != 0), "道）\n")
cat("lambda.1se 非零的题目个数：", sum(b_1se != 0), "\n")
log_close()
