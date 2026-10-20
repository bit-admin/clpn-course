# =====================================================================
# L4-3.R  缺失数据与样本流失  (Missing data & attrition)
# 人为制造 20% 流失（抑郁高的人更容易流失 = MAR/MNAR 型），观察偏差
# =====================================================================
source("R/_setup.R")
log_open("L4-3_log.txt")
dat <- read_course_data()
dat$dep_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])
dat$dep_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
dat$lone_t1 <- rowSums(dat[, paste0(lone_items, "_t1")])

set.seed(43)
p_drop <- plogis(-2.0 + 0.25 * (dat$dep_t1 - mean(dat$dep_t1)))   # T1 越抑郁，流失概率越高
drop <- rank(-(p_drop + runif(nrow(dat), 0, .3))) <= 0.2 * nrow(dat)  # 恰好 20% 流失
dat$dropout <- as.integer(drop)
obs <- dat; obs[drop, grep("_t2$|_t3$", names(obs))] <- NA       # 流失者 T2/T3 数据缺失
obs$dep_t2[drop] <- NA
cat("流失率 =", mean(drop), "\n")
cat("T2 抑郁均值：完整数据", round(mean(dat$dep_t2), 2),
    "；列表删除（listwise deletion）后", round(mean(obs$dep_t2, na.rm = TRUE), 2), "（被低估）\n")
cat("r(T1孤独, T2抑郁)：完整", round(cor(dat$lone_t1, dat$dep_t2), 3),
    "；列表删除", round(cor(obs$lone_t1, obs$dep_t2, use = "complete.obs"), 3), "\n\n")
# 流失分析：比较流失者与留存者的 T1 特征
print(t.test(dep_t1 ~ dropout, data = dat))
print(chisq.test(table(dat$gender, dat$dropout)))
# 多重插补（multiple imputation, mice）——了解即可
imp <- mice::mice(obs[, c("dep_t1", "lone_t1", "gender", "dep_t2")], m = 5, printFlag = FALSE, seed = 1)
est <- mice::pool(with(imp, lm(dep_t2 ~ 1)))
cat("\n多重插补后 T2 抑郁均值 ≈", round(summary(est)$estimate, 2), "（更接近真实值）\n")
write.csv(obs[, !names(obs) %in% c("dep_t1", "dep_t2", "lone_t1")], out("L4-3_data_with_attrition.csv"),
          row.names = FALSE)
# FIML（全信息最大似然）：lavaan 中只需 missing = "ml"，但要带上与缺失有关的辅助变量
suppressPackageStartupMessages(library(lavaan))
o <- obs
f0 <- suppressWarnings(sem("dep_t2 ~~ dep_t2", data = o, missing = "ml", meanstructure = TRUE))
cat("\nFIML (a) 只有 dep_t2：\n"); print(parameterEstimates(f0)[2, c("lhs", "op", "est")], digits = 4)
m  <- "dep_t2 ~~ dep_t1 + lone_t1
       dep_t1 ~~ lone_t1"
f1 <- sem(m, data = o[, c("dep_t1", "dep_t2", "lone_t1")], missing = "ml", meanstructure = TRUE)
pe <- parameterEstimates(f1); cat("FIML (b) 纳入 T1 抑郁、T1 孤独：\n"); print(pe[pe$op == "~1", c("lhs", "est", "se")], digits = 4)
ss <- standardizedSolution(f1)
cat("FIML 估计的 r(T1 孤独, T2 抑郁) =", sprintf("%.3f", ss$est.std[ss$lhs == "dep_t2" & ss$rhs == "lone_t1"]), "\n")
# 例外：流失只取决于预测变量（T1 抑郁）时，完整个案的回归系数不受系统影响
# （对比上面的均值和相关：它们都被列表删除扭曲了）
b_full <- coef(lm(dep_t2 ~ dep_t1 + lone_t1, data = dat))
b_cc   <- coef(lm(dep_t2 ~ dep_t1 + lone_t1, data = obs))     # lm() 默认列表删除
cat("\n回归 dep_t2 ~ dep_t1 + lone_t1 的系数（完整数据 vs 列表删除）：\n")
print(round(rbind(完整数据 = b_full, 列表删除 = b_cc), 3))
log_close()
