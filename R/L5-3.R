# =====================================================================
# L5-3.R  RI-CLPM：分离稳定特质与被试内变化  (Random-intercept CLPM)
# 结构参照 Mulder & Hamaker (2021) 的 lavaan 示例
# =====================================================================
source("R/_setup.R")
library(lavaan)
log_open("L5-3_log.txt")
dat <- read_course_data()
wide <- data.frame(id = dat$id)
for (t in 1:3) {
  wide[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
  wide[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)])
}
riclpm <- '
  # 1) 随机截距（random intercepts）：每个人稳定的“特质水平”，因子载荷固定为 1
  RI_lone =~ 1*lone1 + 1*lone2 + 1*lone3
  RI_dep  =~ 1*dep1  + 1*dep2  + 1*dep3
  # 2) 被试内成分（within-person components）
  wl1 =~ 1*lone1; wl2 =~ 1*lone2; wl3 =~ 1*lone3
  wd1 =~ 1*dep1;  wd2 =~ 1*dep2;  wd3 =~ 1*dep3
  # 3) 被试内的自回归与交叉滞后
  wl2 ~ wl1 + wd1;  wd2 ~ wd1 + wl1
  wl3 ~ wl2 + wd2;  wd3 ~ wd2 + wl2
  # 4) 同期相关与（残差）方差
  wl1 ~~ wd1; wl2 ~~ wd2; wl3 ~~ wd3
  wl1 ~~ wl1; wd1 ~~ wd1; wl2 ~~ wl2; wd2 ~~ wd2; wl3 ~~ wl3; wd3 ~~ wd3
  RI_lone ~~ RI_lone; RI_dep ~~ RI_dep; RI_lone ~~ RI_dep
  # 5) 随机截距与 T1 被试内成分不相关；观测变量的测量误差固定为 0
  RI_lone ~~ 0*wl1 + 0*wd1;  RI_dep ~~ 0*wl1 + 0*wd1
  lone1 ~~ 0*lone1; lone2 ~~ 0*lone2; lone3 ~~ 0*lone3
  dep1 ~~ 0*dep1;   dep2 ~~ 0*dep2;   dep3 ~~ 0*dep3
'
fit_ri <- lavaan(riclpm, data = wide, missing = "fiml", meanstructure = TRUE, int.ov.free = TRUE)
print(summary(fit_ri, standardized = TRUE, fit.measures = TRUE))   # print()：用 source() 或 run_all.R 运行时也写进日志

clpm <- 'lone2 ~ lone1 + dep1; dep2 ~ dep1 + lone1; lone3 ~ lone2 + dep2; dep3 ~ dep2 + lone2
         lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3'
fit_c <- sem(clpm, data = wide, missing = "fiml")
get <- function(f) { pe <- standardizedSolution(f); pe <- pe[pe$op == "~", ]
  setNames(round(pe$est.std, 3), paste(pe$rhs, "→", pe$lhs)) }
cat("\n===== CLPM vs RI-CLPM 标准化路径 =====\nCLPM：\n"); print(get(fit_c))
cat("RI-CLPM（被试内）：\n"); print(get(fit_ri))
print(anova(fit_c, fit_ri))
cat("模拟数据设定了较强的稳定特质：RI-CLPM 的自回归明显变小，说明 CLPM 的“稳定性”\n",
    "很大一部分来自被试间差异。标准 CLPN 也有同样的局限（见 7.5）。\n")
log_close()
