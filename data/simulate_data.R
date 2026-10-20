# =====================================================================
# simulate_data.R —— 生成课程用的“孤独感 <-> 抑郁”三波模拟面板数据
# Simulate a 3-wave loneliness <-> depression panel with a KNOWN structure
# ---------------------------------------------------------------------
# 为什么要用模拟数据（simulated data）？
#   因为我们“事先知道真实答案”（ground truth）。学完 CLPN 后，
#   你可以把自己估计出来的网络和真实网络对照，检查方法能否“找回”（recover）真实边。
#
# 运行方式：在 RStudio 中打开 clpn-course.Rproj，然后 source("data/simulate_data.R")
#   或在终端：Rscript data/simulate_data.R    （工作目录 = clpn-course 文件夹）
# 输出（全部在 data/ 文件夹）：
#   clpn_sim_wide.csv        主数据（宽格式 wide），N = 800，3 波，9 题 + 协变量
#   clpn_sim_wide.sav        同一份数据的 SPSS 格式（2.4 课练习导入 .sav）
#   true_B_within.csv        生成模型中“被试内”的真实滞后系数矩阵（行=T，列=T+1）
#   true_B_population.csv    CLPN 的“目标答案”：在 20 万人的超大样本里，
#                            用标准化 T1 题目对每个 T2 题目做 OLS 得到的总体系数
#   data_dictionary.csv      中英双语数据字典（另见 data_dictionary.md）
# =====================================================================

set.seed(20261016)          # 随机种子（random seed）：保证每次生成完全相同的数据

## ---- 0. 题目（节点 node）定义 -------------------------------------------
items <- c("lone1", "lone2", "lone3", "lone4", "dep1", "dep2", "dep3", "dep4", "dep5")
p <- length(items)          # 9 个节点
is_lone <- grepl("lone", items)

## ---- 1. 真实的被试内滞后结构 B（within-person lagged structure）----------
# 约定（与 qgraph 一致）：B[k, j] = 从 T 时刻的题目 k 指向 T+1 时刻的题目 j 的系数
B <- matrix(0, p, p, dimnames = list(items, items))
diag(B) <- ifelse(is_lone, 0.35, 0.30)       # 自回归（autoregressive, AR）
# 交叉滞后边（cross-lagged, CL）—— 设计成“孤独 → 抑郁”略强于“抑郁 → 孤独”
B["lone3", "dep1"] <-  0.18   # 与人隔绝 → 情绪低落
B["lone1", "dep2"] <-  0.14   # 缺少陪伴 → 兴趣丧失
B["lone4", "dep5"] <-  0.12   # 无人理解 → 无价值感
B["dep2",  "lone3"] <- 0.12   # 兴趣丧失 → 与人隔绝（社交退缩 social withdrawal）
B["dep3",  "dep4"] <-  0.16   # 睡眠问题 → 疲乏
B["dep1",  "dep5"] <-  0.10   # 情绪低落 → 无价值感
B["lone2", "lone4"] <- 0.10   # 被冷落 → 无人理解
B["dep4",  "lone2"] <- -0.15  # 疲乏 → 被冷落（一条负边，用于演示 EI 与强度的区别）

## ---- 2. 同期残差（innovation）协方差 Psi -----------------------------------
# 同一构念内的题目同时变化（相关 .35），跨构念 .15
R_in <- matrix(0.15, p, p); R_in[is_lone, is_lone] <- 0.35; R_in[!is_lone, !is_lone] <- 0.35
diag(R_in) <- 1

# 平稳分布（stationary distribution）：Sigma = t(B) %*% Sigma %*% B + Psi，迭代求解
# 先把 Psi 设为让 Var(W) ≈ 1 的大小
Sigma <- diag(p)
for (it in 1:500) {
  Psi   <- R_in * sqrt(outer(1 - diag(t(B) %*% Sigma %*% B), 1 - diag(t(B) %*% Sigma %*% B)))
  Sigma <- t(B) %*% Sigma %*% B + Psi
}

## ---- 3. 稳定特质（random intercept, 被试间 between-person）--------------
# 孤独特质与抑郁特质相关 .50；每题的特质方差约 0.45（相对被试内方差 1）
gen_panel <- function(N) {
  trait <- MASS::mvrnorm(N, c(0, 0), matrix(c(1, .5, .5, 1), 2))
  RI <- cbind(trait[, rep(1, 4)], trait[, rep(2, 5)]) * sqrt(0.40) +
        matrix(rnorm(N * p, 0, sqrt(0.05)), N, p)
  female <- rbinom(N, 1, 0.55)
  W <- vector("list", 3)
  W[[1]] <- MASS::mvrnorm(N, rep(0, p), Sigma)
  for (t in 2:3) W[[t]] <- W[[t - 1]] %*% B + MASS::mvrnorm(N, rep(0, p), Psi)
  # 观察到的连续潜在得分 = 特质 + 被试内偏离 + 女性在抑郁题上高 0.2
  X <- lapply(W, function(w) { x <- RI + w; x[, !is_lone] <- x[, !is_lone] + 0.2 * female; x })
  list(X = X, female = female, trait = trait)
}

# 把连续得分切成李克特等级（Likert categories）
# 孤独：1 = 从不 … 4 = 经常（类似 UCLA-3）；抑郁：0 = 完全不会 … 3 = 几乎每天（类似 PHQ-9），右偏
to_likert <- function(x) {
  out <- x
  sdx <- 1.2
  out[, is_lone]  <- as.integer(cut(x[, is_lone] / sdx,  c(-Inf, -0.6, 0.4, 1.2, Inf))) # 1..4
  out[, !is_lone] <- as.integer(cut(x[, !is_lone] / sdx, c(-Inf, 0.1, 0.9, 1.6, Inf))) - 1L # 0..3
  out
}

## ---- 4. 课程主数据：N = 800 ---------------------------------------------
N <- 800
sim <- gen_panel(N)
wide <- data.frame(id = sprintf("P%03d", 1:N))
for (t in 1:3) {
  lik <- to_likert(sim$X[[t]]); colnames(lik) <- paste0(items, "_t", t)
  wide <- cbind(wide, lik)
}
wide$gender <- sim$female                                   # 0 = 男 male, 1 = 女 female
wide$age    <- pmin(pmax(round(rnorm(N, 45, 15)), 18), 85)  # 年龄
# 社会支持（1–5，越高越好）：与孤独特质负相关
wide$social_support_t1 <- round(pmin(pmax(3.4 - 0.55 * sim$trait[, 1] + rnorm(N, 0, .6), 1), 5), 1)
# 睡眠时长（小时）：与 T1 睡眠问题题目负相关
wide$sleep_hours_t1 <- round(pmin(pmax(7.2 - 0.5 * wide$dep3_t1 + rnorm(N, 0, .9), 3), 11), 1)
# 生活满意度（0–100）
wide$life_sat_t1 <- round(pmin(pmax(65 - 6 * sim$trait[, 2] - 4 * sim$trait[, 1] + rnorm(N, 0, 12), 0), 100))
# T2 是否寻求专业帮助（0/1）：抑郁越高越可能求助（逻辑回归 logistic 生成）
dep_t2_sum <- rowSums(wide[, paste0(items[!is_lone], "_t2")])
wide$help_seek_t2 <- rbinom(N, 1, plogis(-2.2 + 0.18 * dep_t2_sum + 0.4 * wide$gender))

write.csv(wide, "data/clpn_sim_wide.csv", row.names = FALSE)
if (requireNamespace("haven", quietly = TRUE)) haven::write_sav(wide, "data/clpn_sim_wide.sav")

## ---- 5. “真实答案”：总体层面的 T1 -> T2 回归系数 -------------------------
# 注意：观察数据里混有稳定特质，所以 CLPN（基于观察得分）的目标并不等于被试内 B。
# 我们用 20 万人的大样本计算“如果样本无限大，CLPN 的 OLS 系数会是多少”。
big <- gen_panel(200000)
Xb <- scale(to_likert(big$X[[1]])); Yb <- scale(to_likert(big$X[[2]]))
Bpop <- solve(crossprod(Xb), crossprod(Xb, Yb)); dimnames(Bpop) <- list(items, items)
write.csv(round(B, 3),    "data/true_B_within.csv")
write.csv(round(Bpop, 3), "data/true_B_population.csv")

cat("数据已生成：data/clpn_sim_wide.csv  (N =", N, ")\n")
cat("总体层面 T1->T2 系数（CLPN 的目标答案）：\n"); print(round(Bpop, 2))
