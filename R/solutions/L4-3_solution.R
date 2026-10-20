# 练习答案 L4-3：流失分析补充（4.3-A）；MCAR 对照组（4.3-B）；插补模型漏掉关键变量（4.3-C）
source("R/_setup.R")
log_open("sol_L4-3_log.txt")
dat <- read_course_data()                      # 与 R/L4-3.R 完全相同的流失制造过程
dat$dep_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])
dat$dep_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
dat$lone_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])
set.seed(43)
p_drop <- plogis(-2.0 + 0.25 * (dat$dep_t1 - mean(dat$dep_t1)))
drop <- rank(-(p_drop + runif(nrow(dat), 0, .3))) <= 0.2 * nrow(dat)
dat$dropout <- as.integer(drop)
# ---- 4.3-A：补充比较 T1 孤独与年龄 ----
for (v in c("dep_t1", "lone_t1", "age")) {
  tt <- t.test(dat[[v]] ~ dat$dropout)
  cat(sprintf("%-8s 留存 M = %.2f，流失 M = %.2f；Welch t(%.1f) = %.2f，p = %s\n", v, tt$estimate[1], tt$estimate[2],
              tt$parameter, tt$statistic, format.pval(tt$p.value, digits = 3, eps = .001)))
}
d <- with(dat, (mean(dep_t1[dropout == 1]) - mean(dep_t1[dropout == 0])) / sd(dep_t1))
cat("T1 抑郁的标准化差异（用全样本 SD）d ≈", round(d, 2), "\n")
sp <- with(dat, sqrt(((sum(dropout == 1) - 1) * var(dep_t1[dropout == 1]) + (sum(dropout == 0) - 1) * var(dep_t1[dropout == 0])) /
                     (nrow(dat) - 2)))                          # 合并的组内 SD（pooled SD）
cat("T1 抑郁的标准化差异（用合并组内 SD，即通常的 Cohen's d）d ≈",
    round(with(dat, (mean(dep_t1[dropout == 1]) - mean(dep_t1[dropout == 0])) / sp), 2), "\n\n")
# ---- 4.3-B：MCAR 对照 ----
set.seed(1)
drop_mcar <- sample(c(rep(TRUE, 160), rep(FALSE, 640)))
cat("完整数据：T2 抑郁均值 =", round(mean(dat$dep_t2), 2), "；r(T1孤独, T2抑郁) =", round(cor(dat$lone_t1, dat$dep_t2), 3), "\n")
cat("MCAR 列表删除：T2 抑郁均值 =", round(mean(dat$dep_t2[!drop_mcar]), 2),
    "；r =", round(cor(dat$lone_t1[!drop_mcar], dat$dep_t2[!drop_mcar]), 3), "\n")
tm <- t.test(dat$dep_t1 ~ drop_mcar)
cat("MCAR 流失分析（T1 抑郁）：p =", round(tm$p.value, 3), "（多半不显著）\n")
# ---- 4.3-C：插补模型漏掉关键变量 ----
need_output("L4-3_data_with_attrition.csv", "R/L4-3.R")
o <- read.csv(out("L4-3_data_with_attrition.csv"))
o$dep_t1  <- rowSums(o[, paste0(dep_items, "_t1")])
o$dep_t2  <- rowSums(o[, paste0(dep_items, "_t2")])
o$lone_t1 <- rowSums(o[, paste0(lone_items, "_t1")])
imp_a <- mice::mice(o[, c("dep_t1", "lone_t1", "gender", "dep_t2")], m = 5, printFlag = FALSE, seed = 1)
imp_b <- mice::mice(o[, c("lone_t1", "gender", "dep_t2")], m = 5, printFlag = FALSE, seed = 1)
ea <- summary(mice::pool(with(imp_a, lm(dep_t2 ~ 1))))$estimate
eb <- summary(mice::pool(with(imp_b, lm(dep_t2 ~ 1))))$estimate
cat("\n4.3-C 多重插补后的 T2 抑郁均值（真实值", round(mean(dat$dep_t2), 2), "；列表删除",
    round(mean(o$dep_t2, na.rm = TRUE), 2), "）：\n")
cat("(a) 插补模型含 dep_t1、lone_t1、gender：", round(ea, 2), "\n")
cat("(b) 去掉 dep_t1，只用 lone_t1、gender：  ", round(eb, 2), "\n")
log_close()
