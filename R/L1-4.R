# =====================================================================
# L1-4.R  协方差与相关  (Covariance & correlation)
# =====================================================================
source("R/_setup.R")
log_open("L1-4_log.txt")
dat <- read_course_data()
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])
dat$dep_sum_t1  <- rowSums(dat[, paste0(dep_items, "_t1")])

x <- dat$lone_sum_t1; y <- dat$dep_sum_t1
cov_hand <- sum((x - mean(x)) * (y - mean(y))) / (length(x) - 1)  # 协方差 covariance
r_hand   <- cov_hand / (sd(x) * sd(y))                             # 相关 = 协方差 / (sdx*sdy)
cat("协方差：手算", round(cov_hand, 3), " cov()", round(cov(x, y), 3), "\n")
cat("相关 r：手算", round(r_hand, 3), " cor()", round(cor(x, y), 3), "\n\n")

# 相关矩阵（correlation matrix）
vars <- c("lone_sum_t1", "dep_sum_t1", "social_support_t1", "sleep_hours_t1", "life_sat_t1")
print(round(cor(dat[, vars]), 2))
# 斯皮尔曼相关（Spearman）适合定序数据
cat("\nSpearman r(孤独, 抑郁) =", round(cor(x, y, method = "spearman"), 3), "\n")

png_open("L1-4_scatter.png", 1400, 1300)
set.seed(14)                         # jitter() 是随机的：固定种子，图每次都一样
plot(jitter(x), jitter(y), pch = 16, col = rgb(0, 0, 1, .3),
     xlab = "孤独总分 T1", ylab = "抑郁总分 T1", main = paste0("r = ", round(r_hand, 2)))
abline(lm(y ~ x), col = "red", lwd = 2)
invisible(dev.off())
cat("提醒：相关 ≠ 因果（correlation is not causation）。\n")

# 定序题目：三种相关的比较（讲义第二个代码框）——情绪低落、睡眠问题（0–3 分）
cat("\ndep1_t1 与 dep3_t1：皮尔逊 / 斯皮尔曼 / 多分格相关\n")
x2 <- dat[, c("dep1_t1", "dep3_t1")]
print(round(cor(x2)[1, 2], 3))                        # 皮尔逊
print(round(cor(x2, method = "spearman")[1, 2], 3))   # 斯皮尔曼
print(round(psych::polychoric(x2)$rho[1, 2], 3))      # 多分格相关（polychoric）
log_close()
