# =====================================================================
# L2-5.R  用 R 做描述统计、相关与回归  (Descriptives, correlation, regression in R)
# =====================================================================
source("R/_setup.R")
log_open("L2-5_log.txt")
dat <- read_course_data()
d <- data.frame(孤独 = rowSums(dat[, paste0(lone_items, "_t1")]),
                抑郁 = rowSums(dat[, paste0(dep_items, "_t1")]),
                社会支持 = dat$social_support_t1, 睡眠 = dat$sleep_hours_t1,
                生活满意度 = dat$life_sat_t1)
print(round(psych::describe(d)[, c("n", "mean", "sd", "min", "max", "skew")], 2))
ct <- suppressWarnings(psych::corr.test(d))                         # 相关矩阵 + p 值
print(round(ct$r, 2)); print(round(ct$p, 4))
fit <- lm(抑郁 ~ 孤独 + 社会支持, data = d)
print(summary(fit))
png_open("L2-5_pairs.png", 1800, 1800); psych::pairs.panels(d, ellipses = FALSE); invisible(dev.off())

# ---- 课文补充：置信区间与缺失值处理演示 ----
print(round(confint(fit), 3))                  # 95% 置信区间
d_na <- d
d_na$孤独[c(3, 10, 25)] <- NA                    # 人为制造 3 个缺失
print(cor(d_na$孤独, d_na$社会支持))                # NA 传染
print(cor(d_na$孤独, d_na$社会支持, use = "pairwise.complete.obs"))
print(nobs(lm(抑郁 ~ 孤独, data = d_na)))        # lm 默认删除缺失个案：800 − 3
log_close()
