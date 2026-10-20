# =====================================================================
# L5-2.R  用 lavaan 拟合 CLPM 并评估模型拟合  (CLPM in lavaan; model fit)
# =====================================================================
source("R/_setup.R")
library(lavaan)
log_open("L5-2_log.txt")
dat <- read_course_data()
wide <- data.frame(id = dat$id)
for (t in 1:3) {                                   # 构念总分（construct scores）
  wide[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
  wide[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)])
}
clpm <- '
  lone2 ~ lone1 + dep1      # T2 孤独 被 T1 孤独（AR）和 T1 抑郁（CL）预测
  dep2  ~ dep1  + lone1
  lone3 ~ lone2 + dep2
  dep3  ~ dep2  + lone2
  lone1 ~~ dep1             # ~~ 表示（残差）相关
  lone2 ~~ dep2
  lone3 ~~ dep3
'
fit <- sem(clpm, data = wide, missing = "fiml")   # FIML：全信息最大似然，处理缺失
print(summary(fit, standardized = TRUE, fit.measures = TRUE))   # print()：用 source() 或 run_all.R 运行时也写进日志
pe <- parameterEstimates(fit, standardized = TRUE)
print(pe[pe$op == "~", c("lhs", "op", "rhs", "std.all", "ci.lower", "ci.upper", "pvalue")], digits = 3)
print(round(fitMeasures(fit, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr")), 3))
cat("提示：CFI ≥ .95、RMSEA ≤ .06、SRMR ≤ .08 常被当作“拟合良好”的参考。\n")
# 标准化估计要配标准化的置信区间：standardizedSolution() 按 delta 法为 est.std 计算 SE 和 95% CI
# （上面 parameterEstimates() 的 ci.lower / ci.upper 属于未标准化估计，不能和 std.all 并排解读）
cat("\n标准化解（standardizedSolution）：回归路径的标准化估计及其 95% CI\n")
ssol <- standardizedSolution(fit)
print(ssol[ssol$op == "~", c("lhs", "op", "rhs", "est.std", "se", "ci.lower", "ci.upper", "pvalue")], digits = 3)
saveRDS(wide, out("L5_sumscores.rds"))
log_close()
