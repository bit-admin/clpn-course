# =====================================================================
# L8-3.R  个案删除 bootstrap 与 CS 系数  (Case-dropping bootstrap & CS-coefficient)
# CS = 最多能删掉多少比例的个案，仍有 95% 的把握使中心性与原样本相关 ≥ 0.7
# 参考：CS 不应低于 0.25，最好高于 0.5（Epskamp, Borsboom & Fried, 2018）
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(glmnet) })
log_open("L8-3_log.txt")
dat <- read_course_data()
wide_items <- dat[, c(vars_t(1), vars_t(2))]
# 可重复性：bootnet 的并行（nCores > 1）在各工作进程中用未设种子的随机数重抽样，
# 即使 set.seed() 结果每次也会略有不同。因此默认单核（nCores = 1），set.seed() 后结果完全可重复（约慢 5–7 倍）。
# 只想快速看看、不需要可重复时，可改为 max(1, parallel::detectCores() - 1)。
n_boots <- 1000; n_cores <- 1
clpn_fun <- function(data) {                       # 与 L8-2 相同的估计函数
  p <- ncol(data) / 2
  X <- scale(as.matrix(data[, 1:p])); Y <- scale(as.matrix(data[, (p + 1):(2 * p)]))
  B <- matrix(0, p, p)
  for (j in seq_len(p)) {
    cvfit <- glmnet::cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]
  }
  B
}
set.seed(2026)
net <- estimateNetwork(wide_items, default = "none", fun = clpn_fun, directed = TRUE, labels = items)

# ---- 课件代码 ----
set.seed(2026)
cd <- bootnet(net, nBoots = n_boots, type = "case", nCores = n_cores,
              statistics = c("outExpectedInfluence", "inExpectedInfluence"), verbose = FALSE)
cs <- corStability(cd); cat("\n")
saveRDS(cd, out("L8-3_casedrop.rds"))
write.csv(data.frame(指标 = names(cs), CS = round(cs, 3)), out("L8-3_CS.csv"), row.names = FALSE)
png_open("L8-3_casedrop.png", 1600, 1200)
suppressWarnings(print(plot(cd, statistics = c("outExpectedInfluence", "inExpectedInfluence"))))
invisible(dev.off())
# 判断标准只有 0.25 / 0.5 两档（Epskamp et al., 2018）。CS 只能取删除比例网格上的值
# （bootnet 默认 0.05–0.75 共 10 档，相邻两档相差约 0.08），所以刚过 0.5 一档时要特别说明：换种子就可能落到下一档。
step <- diff(seq(0.05, 0.75, length.out = 10))[1]
for (k in names(cs)) {
  verdict <- if (cs[k] >= .5 + step) "稳定（≥ 0.5），可以解释排序" else if (cs[k] >= .5)
    "刚达到 0.5，只比界值高一个网格档：边缘稳定，换随机种子可能落到下一档，解释排序须谨慎" else if (cs[k] >= .25)
    "勉强可接受（0.25–0.5），解释排序须谨慎" else "不稳定（< 0.25），不应解释排序"
  cat(sprintf("%-22s CS = %.2f → %s\n", k, cs[k], verdict))
}
log_close()
