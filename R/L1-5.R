# =====================================================================
# L1-5.R  抽样、标准误与置信区间  (Sampling, SE & confidence intervals)
# 用“虚拟城市”模拟：样本越大，样本均值的分布越窄。
# =====================================================================
source("R/_setup.R")
log_open("L1-5_log.txt")
set.seed(2026)
city <- rnorm(100000, mean = 10, sd = 3)          # 总体 population：10 万居民的孤独分
sizes <- c(20, 100, 500)
png_open("L1-5_sampling.png", 2100, 800)
par(mfrow = c(1, 3))
for (n in sizes) {
  means <- replicate(2000, mean(sample(city, n)))  # 抽 2000 次样本，每次算均值 → 抽样分布
  hist(means, breaks = 40, xlim = c(8, 12), col = "grey80",
       main = paste0("n = ", n, "，SD(均值) = ", round(sd(means), 3)), xlab = "样本均值")
  cat("n =", n, "：抽样分布的标准差 =", round(sd(means), 3),
      "；理论标准误 SE = σ/√n =", round(3 / sqrt(n), 3), "\n")
}
invisible(dev.off())
# 一个样本的 95% 置信区间（confidence interval）
s <- sample(city, 100)
se <- sd(s) / sqrt(100)
cat("\n一个 n=100 样本：均值", round(mean(s), 2), " 95% CI = [",
    round(mean(s) - 1.96 * se, 2), ",", round(mean(s) + 1.96 * se, 2), "]\n")
print(t.test(s)$conf.int)
log_close()
