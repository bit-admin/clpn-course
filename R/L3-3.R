# =====================================================================
# L3-3.R  标准化系数与结果解释  (Standardized coefficients, APA reporting)
# =====================================================================
source("R/_setup.R")
log_open("L3-3_log.txt")
dat <- read_course_data()
d <- data.frame(dep2  = rowSums(dat[, paste0(dep_items, "_t2")]),
                lone1 = rowSums(dat[, paste0(lone_items, "_t1")]),
                dep1  = rowSums(dat[, paste0(dep_items, "_t1")]))
dz <- as.data.frame(scale(d))                     # 所有变量先标准化 → 系数即 β
fit <- lm(dep2 ~ lone1 + dep1, data = dz)
ci <- confint(fit)                                # 95% 置信区间
s <- summary(fit)$coefficients
for (v in c("lone1", "dep1")) {
  cat(sprintf("%s: β = %.2f, 95%% CI [%.2f, %.2f], p %s\n", v, s[v, 1], ci[v, 1], ci[v, 2],
              ifelse(s[v, 4] < .001, "< .001", sprintf("= %.3f", s[v, 4]))))
}
cat("\nAPA 示例：控制 T1 抑郁后，T1 孤独感正向预测 T2 抑郁（β = ",
    round(s["lone1", 1], 2), "）。注意用“预测”而非“导致”。\n", sep = "")

# ---- 比较 m2 的 b 与 β（不同单位的预测变量；讲义第二个代码框）----
cat("\nm2：孤独 + 社会支持 + 睡眠预测 T2 抑郁，未标准化 b 与标准化 β\n")
d$support <- dat$social_support_t1
d$sleep   <- dat$sleep_hours_t1
f_b    <- lm(dep2 ~ lone1 + support + sleep, data = d)
f_beta <- lm(dep2 ~ lone1 + support + sleep, data = as.data.frame(scale(d)))
print(round(cbind(b = coef(f_b), beta = coef(f_beta)), 3))

# ---- 手算 β，以及换单位实验（讲义第三个代码框）----
cat("\n手算孤独的 β = b × sd(x) / sd(y)：\n")
print(round(coef(f_b)["lone1"] * sd(d$lone1) / sd(d$dep2), 3))
d$sleep_min <- d$sleep * 60                      # 睡眠改用分钟
cat("睡眠改用分钟后的 b（= 小时的 b / 60）：\n")
print(round(coef(lm(dep2 ~ lone1 + support + sleep_min, data = d))["sleep_min"], 4))
log_close()
