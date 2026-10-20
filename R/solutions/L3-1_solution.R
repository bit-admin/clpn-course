# 练习答案 L3-1：社会支持预测抑郁；手画直线 vs OLS
source("R/_setup.R")
log_open("sol_L3-1_log.txt")
dat <- read_course_data(); dat$dep <- rowSums(dat[, paste0(dep_items, "_t1")])
fit <- lm(dep ~ social_support_t1, dat); print(coef(fit))
my_line <- c(10, -1.8)          # 例：在散点图上手画的直线 y = 10 - 1.8x
rss <- function(b) sum((dat$dep - (b[1] + b[2] * dat$social_support_t1))^2)
cat("手画 RSS =", round(rss(my_line)), "；OLS RSS =", round(rss(coef(fit))), "（OLS 永远最小）\n")

# ---- 3.1-A 用讲义代码框里的起始值 my_b0 = 7, my_b1 = -1 ----
cat("\n3.1-A：讲义模板直线 y = 7 - 1x 的 RSS =", round(rss(c(7, -1)), 1),
    "；OLS 截距 =", round(coef(fit)[1], 2), " 斜率 =", round(coef(fit)[2], 2),
    " RSS =", round(rss(coef(fit)), 1), "\n")
# 为什么手画的线常比 OLS 陡：SD 线斜率 = -sd(y)/sd(x)，OLS 斜率 = r × sd(y)/sd(x)
r <- cor(dat$social_support_t1, dat$dep)
cat("SD 线斜率 =", round(-sd(dat$dep) / sd(dat$social_support_t1), 2),
    "；OLS 斜率 = r × sd(y)/sd(x) =", round(r * sd(dat$dep) / sd(dat$social_support_t1), 2), "\n")

# ---- 3.1-B 报告所需的数字 ----
sm <- summary(fit)
cat("\n3.1-B：b =", round(coef(fit)[2], 2), " SE =", round(sm$coefficients[2, 2], 2),
    " p =", signif(sm$coefficients[2, 4], 3), " R² =", round(sm$r.squared, 3), "\n")

# ---- 3.1-C 纸笔题用 R 验算 ----
x <- c(1, 2, 3, 4); y <- c(2, 4, 5, 5)
b1 <- sum((x - mean(x)) * (y - mean(y))) / sum((x - mean(x))^2)
b0 <- mean(y) - b1 * mean(x)
e  <- y - (b0 + b1 * x)
cat("\n3.1-C：b1 =", b1, " b0 =", b0, "\n残差：", e, "；残差之和 =", sum(e), "\n")
print(coef(lm(y ~ x)))         # 与 lm() 对照
log_close()
