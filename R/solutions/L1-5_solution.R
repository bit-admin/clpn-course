# 练习答案 L1-5：样本量与抽样分布
source("R/_setup.R")
log_open("sol_L1-5_log.txt")
set.seed(15); city <- rnorm(1e5, 10, 3)
for (n in c(20, 100, 500)) cat("n =", n, " 均值抽样分布 SD =", round(sd(replicate(2000, mean(sample(city, n)))), 3), "\n")
# 3 句话参考答案：
# 1) 样本越大，样本统计量越集中在总体值附近（标准误 ∝ 1/√n）。
# 2) 网络有几十条边，每条边都是一个需要估计的参数，各自都有抽样误差。
# 3) 因此网络分析需要较大样本，并且要用 bootstrap 检查边的精确度（模块 8）。

# ---- 练习 1.5-B：手算的 SE 与 95% CI，用 R 验算 ----
m <- 9.2; sdv <- 3.2; n <- 64
se <- sdv / sqrt(n)
cat("\n1.5-B：SE =", se, "；95% CI = [", round(m - 1.96 * se, 2), ",", round(m + 1.96 * se, 2), "]\n")

# ---- 练习 1.5-C：把 R/L1-5.R 的 set.seed(2026) 改成 set.seed(1) 重跑 ----
# 下面是 L1-5.R 主体部分（不画图），只把种子换成 1；与 R/output/L1-5_log.txt 对照
run_l15 <- function() {
  city <- rnorm(100000, mean = 10, sd = 3)
  for (n in c(20, 100, 500)) {
    means <- replicate(2000, mean(sample(city, n)))
    cat("n =", n, "：抽样分布的标准差 =", round(sd(means), 3),
        "；理论标准误 SE = σ/√n =", round(3 / sqrt(n), 3), "\n")
  }
  s <- sample(city, 100); se <- sd(s) / sqrt(100)
  cat("一个 n=100 样本：均值", round(mean(s), 2), " 95% CI = [",
      round(mean(s) - 1.96 * se, 2), ",", round(mean(s) + 1.96 * se, 2), "]\n")
}
cat("\n1.5-C：set.seed(1)\n");  set.seed(1);  run_l15()
cat("\n再运行一次 set.seed(1)：与上面逐字相同\n"); set.seed(1); run_l15()
# “删掉 set.seed() 运行两次”的效果：相当于每次用一个不同的种子，结果每次都不同。
# 这里用两个不同的种子示意（真的不设种子时，你的数字会和任何人都不一样）：
cat("\n不设种子，第一次（示意：种子 101）\n"); set.seed(101); run_l15()
cat("\n不设种子，第二次（示意：种子 202）\n"); set.seed(202); run_l15()
# 结论：具体数字（尤其那个 n = 100 样本的均值和 CI）随种子变化；
# 规律不变：模拟 SD 始终接近 σ/√n，n 越大越窄。所以分析时要固定并报告随机种子。
log_close()
