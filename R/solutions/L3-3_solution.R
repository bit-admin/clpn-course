# 练习答案 L3-3：标准化后重跑 3.2 的模型，按 APA 报告
source("R/_setup.R")
log_open("sol_L3-3_log.txt")
dat <- read_course_data()
d <- as.data.frame(scale(data.frame(dep2 = rowSums(dat[, paste0(dep_items, "_t2")]),
  lone = rowSums(dat[, paste0(lone_items, "_t1")]), support = dat$social_support_t1, sleep = dat$sleep_hours_t1)))
fit <- lm(dep2 ~ lone + support + sleep, d); s <- summary(fit)$coef; ci <- confint(fit)
# APA 写法：p 不写成 0.000；小于 .001 时写 p < .001，否则保留三位小数、去掉前导 0
fmt_p <- function(p) ifelse(p < .001, "p < .001", paste("p =", sub("^0", "", sprintf("%.3f", p))))
for (v in c("lone", "support", "sleep"))
  cat(sprintf("%s: β = %.2f, 95%% CI [%.2f, %.2f], %s\n", v, s[v, 1], ci[v, 1], ci[v, 2], fmt_p(s[v, 4])))
cat(sprintf("APA：控制社会支持与睡眠后，T1 孤独感正向预测 T2 抑郁，β = %.2f, 95%% CI [%.2f, %.2f], %s。\n",
    s["lone", 1], ci["lone", 1], ci["lone", 2], fmt_p(s["lone", 4])))

# ---- 3.3-A：讲义参考代码的表格形式（β、95% CI、p）与 R² ----
cat("\n3.3-A：β、95% CI、p（同一模型的表格形式）\n")
print(round(cbind(beta = coef(fit), ci, p = s[, 4]), 3))
cat("R² =", round(summary(fit)$r.squared, 3), "\n")

# ---- 3.3-B (1)：从 m3（未标准化）手算 T1 抑郁的 β = b × s_x / s_y ----
raw <- data.frame(dep2 = rowSums(dat[, paste0(dep_items, "_t2")]),
                  lone1 = rowSums(dat[, paste0(lone_items, "_t1")]),
                  dep1 = rowSums(dat[, paste0(dep_items, "_t1")]))
m3 <- lm(dep2 ~ lone1 + dep1, data = raw)
cat("\n3.3-B：b(T1 抑郁) =", round(coef(m3)["dep1"], 3), " s(T1 抑郁) =", round(sd(raw$dep1), 3),
    " s(T2 抑郁) =", round(sd(raw$dep2), 3), "\n")
cat("β = b × s_x / s_y =", round(coef(m3)["dep1"] * sd(raw$dep1) / sd(raw$dep2), 3),
    "；标准化后直接估计：", round(coef(lm(dep2 ~ lone1 + dep1, data = as.data.frame(scale(raw))))["dep1"], 3), "\n")
# 3.3-B (2)：0/1 变量的 SD 约 0.5，“女性 vs 男性”差 1 个原始单位 ≈ β / s(性别) 个 y 的标准差
cat("性别（0/1）的 SD =", round(sd(dat$gender), 3), "\n")
log_close()
