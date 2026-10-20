# 练习答案 L5-2：APA 报告 CLPM 交叉滞后路径与拟合指标；等值约束检验（anova(fit_eq, fit)）
source("R/_setup.R"); library(lavaan)
log_open("sol_L5-2_log.txt")
dat <- read_course_data(); w <- data.frame(row.names = dat$id)
for (t in 1:3) { w[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
                 w[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)]) }
fit <- sem('lone2 ~ lone1 + dep1; dep2 ~ dep1 + lone1; lone3 ~ lone2 + dep2; dep3 ~ dep2 + lone2
            lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3', data = w, missing = "fiml")
ss <- standardizedSolution(fit); ss <- ss[ss$op == "~" & substr(ss$lhs, 1, 3) != substr(ss$rhs, 1, 3), ]
for (i in seq_len(nrow(ss))) cat(sprintf("%s → %s：β = %.2f, 95%% CI [%.2f, %.2f], p %s\n", ss$rhs[i], ss$lhs[i],
  ss$est.std[i], ss$ci.lower[i], ss$ci.upper[i], ifelse(ss$pvalue[i] < .001, "< .001", sprintf("= %.3f", ss$pvalue[i]))))
fm <- fitMeasures(fit, c("chisq", "df", "cfi", "rmsea", "srmr"))
cat(sprintf("拟合：χ²(%d) = %.2f, CFI = %.3f, RMSEA = %.3f, SRMR = %.3f\n", fm["df"], fm["chisq"], fm["cfi"], fm["rmsea"], fm["srmr"]))
# 解读要点：CFI 低、RMSEA 高 → CLPM 拟合不佳；原因之一是忽略了稳定特质（见 L5-3 RI-CLPM）。

# ---- 练习“等值约束检验”：T1→T2 与 T2→T3 的同类路径约束相等 ----
clpm_eq <- '
  lone2 ~ a*lone1 + c*dep1
  dep2  ~ b*dep1  + d*lone1
  lone3 ~ a*lone2 + c*dep2      # 同一标签 = 约束相等
  dep3  ~ b*dep2  + d*lone2
  lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3
'
fit_eq <- sem(clpm_eq, data = w, missing = "fiml")
cat("\n嵌套模型 χ² 差异检验 anova(fit_eq, fit)：\n")
print(anova(fit_eq, fit))
lrt <- anova(fit_eq, fit)
cat(sprintf("Δχ²(%d) = %.2f, p = %.3f\n", lrt[2, "Df diff"], lrt[2, "Chisq diff"], lrt[2, "Pr(>Chisq)"]))
cat(sprintf("AIC：等值模型 %.0f，不约束模型 %.0f；BIC：等值模型 %.0f，不约束模型 %.0f\n",
            AIC(fit_eq), AIC(fit), BIC(fit_eq), BIC(fit)))
fe <- fitMeasures(fit_eq, c("chisq", "df", "pvalue", "cfi", "rmsea"))
cat(sprintf("等值模型本身的拟合：χ²(%d) = %.2f, CFI = %.3f, RMSEA = %.3f\n", fe["df"], fe["chisq"], fe["cfi"], fe["rmsea"]))
log_close()
