# =====================================================================
# L4-1.R  纵向设计的语言：波次、被试内与被试间  (Waves; within vs between)
# 用课程数据直观看到：总变异 = 被试间（稳定差异）+ 被试内（随时间波动）
# =====================================================================
source("R/_setup.R")
log_open("L4-1_log.txt")
dat <- read_course_data()
dep <- sapply(1:3, function(t) rowSums(dat[, paste0(dep_items, "_t", t)]))  # 800 × 3 矩阵
colnames(dep) <- paste0("T", 1:3)
print(round(colMeans(dep), 2))                     # 每波的平均抑郁
print(round(cor(dep), 2))                          # 跨波相关（重测稳定性 rank-order stability）
person_mean <- rowMeans(dep)                       # 每个人 3 波的平均 = 被试间部分
within <- dep - person_mean                        # 偏离自己平均的部分 = 被试内部分
cat("\n被试间方差（between）≈", round(var(person_mean), 2),
    "；被试内方差（within）≈", round(mean(apply(within, 1, var)), 2), "\n")
png_open("L4-1_spaghetti.png", 1600, 1200)
set.seed(3); idx <- sample(nrow(dep), 30)
matplot(1:3, t(dep[idx, ]), type = "l", lty = 1, col = rgb(0, 0, 1, .4), xaxt = "n",
        xlab = "波次 wave", ylab = "抑郁总分", main = "30 个人的抑郁轨迹（意大利面图 spaghetti plot）")
axis(1, 1:3, paste0("T", 1:3)); lines(1:3, colMeans(dep), lwd = 4, col = "red")
invisible(dev.off())

# ---- 课文补充：被试间相关 vs 被试内相关；多层模型的方差成分 ----
lone <- sapply(1:3, function(t) rowSums(dat[, paste0(lone_items, "_t", t)]))
print(cor(rowMeans(lone), rowMeans(dep)))                            # 被试间：个人平均之间的相关
print(cor(as.vector(lone - rowMeans(lone)), as.vector(dep - rowMeans(dep))))   # 被试内：偏离之间的相关
# 用多层模型估计方差成分与 ICC（需要 lme4 包：install.packages("lme4")）
long <- data.frame(id = rep(1:800, 3), y = as.vector(dep))
m <- lme4::lmer(y ~ 1 + (1 | id), data = long)
print(as.data.frame(lme4::VarCorr(m))[, c("grp", "vcov")])
log_close()
