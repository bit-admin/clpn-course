# 练习答案 L1-6-C：换随机种子重复“纯噪声中的多重比较”模拟
source("R/_setup.R")
log_open("sol_L1-6_log.txt")
count_fp <- function(seed) {                    # 与 R/L1-6.R 相同的模拟，只换种子
  set.seed(seed)
  noise <- matrix(rnorm(200 * 20), 200, 20)
  pv <- c()
  for (i in 1:19) for (j in (i + 1):20) pv <- c(pv, cor.test(noise[, i], noise[, j])$p.value)
  sum(pv < .05)
}
fp5 <- sapply(2:6, count_fp)
cat("种子 2–6 的假阳性个数：", fp5, "；平均 =", mean(fp5), "\n")
fp200 <- sapply(1:200, count_fp)
cat("200 个种子的平均假阳性个数 =", round(mean(fp200), 2), "（理论期望 190 × 0.05 = 9.5）\n")
cat("范围：", range(fp200), "；中间 90% 落在", quantile(fp200, c(.05, .95)), "\n")
log_close()
