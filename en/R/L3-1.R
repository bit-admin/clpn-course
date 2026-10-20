# =====================================================================
# L3-1.R  Simple linear regression: predicting with a straight line
# Model: depression sum score = intercept b0 + slope b1 * social support + residual
# =====================================================================
source("R/_setup.R")
log_open("L3-1_log.txt")
dat <- read_course_data()
dat$dep_sum_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])

fit <- lm(dep_sum_t1 ~ social_support_t1, data = dat)   # lm = linear model; ~ reads as "predicted by"
print(summary(fit))     # Estimate column: intercept and slope; R-squared: coefficient of determination R²
cat("Interpretation: For each 1-point increase in social support, predicted depression changes by", round(coef(fit)[2], 2), "points.\n")

# Residual = observed value - predicted value; Ordinary Least Squares (OLS) minimizes residual sum of squares (RSS)
cat("OLS line residual sum of squares RSS =", round(sum(resid(fit)^2), 1), "\n")
rss_guess <- sum((dat$dep_sum_t1 - (8 - 1.2 * dat$social_support_t1))^2)
cat("\"Hand-drawn\" line y = 8 - 1.2x RSS =", round(rss_guess, 1), "(must be >= OLS)\n")

png_open("L3-1_regression.png", 1400, 1300)
plot(jitter(dat$social_support_t1), jitter(dat$dep_sum_t1), pch = 16, col = rgb(0, 0, 0, .25),
     xlab = "Social support", ylab = "Depression sum score")
abline(fit, col = "red", lwd = 3); abline(8, -1.2, col = "blue", lty = 2, lwd = 2)
legend("topright", c("OLS optimal line", "Hand-drawn line"), col = c("red", "blue"), lty = c(1, 2), lwd = 2)
invisible(dev.off())

# Predicted values: predicted depression sum scores when social support is 2 and 4 (= b0 + b1 * x)
print(predict(fit, newdata = data.frame(social_support_t1 = c(2, 4))))
# Residuals vs fitted values plot (plot(fit, which = 1)): check whether residuals are evenly dispersed around 0
png_open("L3-1_resid_fitted.png", 1400, 1300)
plot(fit, which = 1)
invisible(dev.off())
cat("Plots saved: R/output/L3-1_regression.png, R/output/L3-1_resid_fitted.png\n")
log_close()
