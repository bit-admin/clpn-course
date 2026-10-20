# 练习答案 L4-1-B：孤独总分的被试间与被试内；附：用多层模型（lme4）估计 ICC
source("R/_setup.R")
log_open("sol_L4-1_log.txt")
dat <- read_course_data()
lone <- sapply(1:3, function(t) rowSums(dat[, paste0(lone_items, "_t", t)]))
dep  <- sapply(1:3, function(t) rowSums(dat[, paste0(dep_items, "_t", t)]))
colnames(lone) <- colnames(dep) <- paste0("T", 1:3)
cat("孤独 3 波均值：\n"); print(round(colMeans(lone), 2))
cat("孤独跨波相关：\n"); print(round(cor(lone), 2))
decomp <- function(m) { pm <- rowMeans(m); c(between = var(pm), within = mean(apply(m - pm, 1, var))) }
cat("粗略方差分解（个人平均的方差 vs 个人内方差）：\n")
print(round(rbind(孤独 = decomp(lone), 抑郁 = decomp(dep)), 2))
if (requireNamespace("lme4", quietly = TRUE)) {
  icc <- function(m) {
    long <- data.frame(id = rep(seq_len(nrow(m)), 3), y = as.vector(m))
    vc <- as.data.frame(lme4::VarCorr(lme4::lmer(y ~ 1 + (1 | id), data = long)))
    v <- setNames(vc$vcov, vc$grp); c(between = v[["id"]], within = v[["Residual"]], ICC = v[["id"]] / sum(v))
  }
  cat("\n多层模型（lme4::lmer(y ~ 1 + (1 | id))）的方差成分与 ICC：\n")
  print(round(rbind(孤独 = icc(lone), 抑郁 = icc(dep)), 2))
  cat("（粗略法的“被试间”≈ 多层模型被试间 + 被试内/3，因为 3 波的个人平均仍含被试内噪音）\n")
} else cat("未安装 lme4：install.packages(\"lme4\") 后可得到多层模型估计。\n")
log_close()
