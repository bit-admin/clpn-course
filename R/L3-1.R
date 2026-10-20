# =====================================================================
# L3-1.R  简单线性回归：用一条直线做预测  (Simple linear regression)
# 模型：抑郁总分 = 截距 b0 + 斜率 b1 × 社会支持 + 残差
# =====================================================================
source("R/_setup.R")
log_open("L3-1_log.txt")
dat <- read_course_data()
dat$dep_sum_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])

fit <- lm(dep_sum_t1 ~ social_support_t1, data = dat)   # lm = linear model；~ 读作“被…预测”
print(summary(fit))     # Estimate 列：截距 intercept 与斜率 slope；R-squared：决定系数 R²
cat("解读：社会支持每高 1 分，预测的抑郁总分变化", round(coef(fit)[2], 2), "分。\n")

# 残差（residual）= 实际值 - 预测值；最小二乘法（OLS）让残差平方和最小
cat("OLS 直线的残差平方和 RSS =", round(sum(resid(fit)^2), 1), "\n")
rss_guess <- sum((dat$dep_sum_t1 - (8 - 1.2 * dat$social_support_t1))^2)
cat("“手画”直线 y = 8 - 1.2x 的 RSS =", round(rss_guess, 1), "（一定 ≥ OLS）\n")

png_open("L3-1_regression.png", 1400, 1300)
plot(jitter(dat$social_support_t1), jitter(dat$dep_sum_t1), pch = 16, col = rgb(0, 0, 0, .25),
     xlab = "社会支持 social support", ylab = "抑郁总分 depression")
abline(fit, col = "red", lwd = 3); abline(8, -1.2, col = "blue", lty = 2, lwd = 2)
legend("topright", c("OLS 最优直线", "手画直线"), col = c("red", "blue"), lty = c(1, 2), lwd = 2)
invisible(dev.off())

# 预测值：社会支持为 2 和 4 时的预测抑郁总分（= b0 + b1 × x）
print(predict(fit, newdata = data.frame(social_support_t1 = c(2, 4))))
# 残差 vs 预测值图（plot(fit, which = 1)）：检查残差是否围绕 0 均匀散开
png_open("L3-1_resid_fitted.png", 1400, 1300)
plot(fit, which = 1)
invisible(dev.off())
cat("图已保存：R/output/L3-1_regression.png、R/output/L3-1_resid_fitted.png\n")
log_close()
