# 练习答案 L8-1：自己写 15 行 bootstrap（练习 1）；样本量与区间宽度（练习 3）
source("R/_setup.R")
log_open("sol_L8-1_log.txt")
dat <- read_course_data()
x <- rowSums(dat[, paste0(lone_items, "_t1")]); y <- rowSums(dat[, paste0(dep_items, "_t2")])
n <- length(x); set.seed(2024)
r_boot <- numeric(1000)
for (b in 1:1000) { idx <- sample(n, n, replace = TRUE); r_boot[b] <- cor(x[idx], y[idx]) }
cat("bootstrap 95% 区间：", round(quantile(r_boot, c(.025, .975)), 3),
    "；cor.test：", round(cor.test(x, y)$conf.int, 3), "\n\n")
# 练习 3：ρ = 0.3，N = 50 / 200 / 400 时 bootstrap 区间的宽度（各重复 20 个样本取平均）
set.seed(3)
width <- function(N) mean(replicate(20, {
  a <- rnorm(N); b <- 0.3 * a + sqrt(1 - 0.09) * rnorm(N)
  rb <- replicate(1000, { i <- sample(N, N, TRUE); cor(a[i], b[i]) })
  diff(quantile(rb, c(.025, .975))) }))
w <- sapply(c(50, 200, 400), width)
print(data.frame(N = c(50, 200, 400), 平均区间宽度 = round(w, 3), `宽度×√N` = round(w * sqrt(c(50, 200, 400)), 2), check.names = FALSE))
cat("→ 宽度 × √N 大致不变：区间宽度 ∝ 1/√N。\n")
log_close()
