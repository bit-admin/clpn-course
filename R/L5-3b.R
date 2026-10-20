# =====================================================================
# L5-3b.R  RI-CLPM 的结果离真值有多远？(How far is one sample from the truth?)
# 课程数据是模拟的，生成模型已知。本脚本做两件事：
#   1. 用 20 万人的大样本拟合同样的 CLPM 与 RI-CLPM，得到“样本无限大时”的标准化路径（真值）
#   2. 重复生成 200 份 N = 800 的数据，看一份样本的估计会在真值周围波动多大
# 运行约 1–3 分钟。结果写入 R/output/L5-3b_log.txt 与 L5-3b_truth.csv。
# =====================================================================
source("R/_setup.R")
library(lavaan)
log_open("L5-3b_log.txt")

# ---- 读取生成模型 --------------------------------------------------------
# 只执行 data/simulate_data.R 中“定义模型”的部分（N <- 800 之前：B、Psi、gen_panel()、to_likert()），
# 不会重新生成或覆盖课程数据文件。
ex <- parse("data/simulate_data.R")
stop_at <- which(vapply(ex, function(e) identical(deparse(e)[1], "N <- 800"), logical(1)))
stopifnot(length(stop_at) == 1)
sim <- new.env()
for (e in ex[seq_len(stop_at - 1)]) eval(e, sim)

# 把题目得分加成三波总分（与 L5-3.R 相同）
to_sums <- function(X) {
  out <- list()
  for (t in 1:3) {
    lik <- sim$to_likert(X[[t]])
    out[[paste0("lone", t)]] <- rowSums(lik[, 1:4])
    out[[paste0("dep", t)]]  <- rowSums(lik[, 5:9])
  }
  as.data.frame(out)
}

riclpm <- '
  RI_lone =~ 1*lone1 + 1*lone2 + 1*lone3
  RI_dep  =~ 1*dep1  + 1*dep2  + 1*dep3
  wl1 =~ 1*lone1; wl2 =~ 1*lone2; wl3 =~ 1*lone3
  wd1 =~ 1*dep1;  wd2 =~ 1*dep2;  wd3 =~ 1*dep3
  wl2 ~ wl1 + wd1;  wd2 ~ wd1 + wl1
  wl3 ~ wl2 + wd2;  wd3 ~ wd2 + wl2
  wl1 ~~ wd1; wl2 ~~ wd2; wl3 ~~ wd3
  wl1 ~~ wl1; wd1 ~~ wd1; wl2 ~~ wl2; wd2 ~~ wd2; wl3 ~~ wl3; wd3 ~~ wd3
  RI_lone ~~ RI_lone; RI_dep ~~ RI_dep; RI_lone ~~ RI_dep
  RI_lone ~~ 0*wl1 + 0*wd1;  RI_dep ~~ 0*wl1 + 0*wd1
  lone1 ~~ 0*lone1; lone2 ~~ 0*lone2; lone3 ~~ 0*lone3
  dep1 ~~ 0*dep1;   dep2 ~~ 0*dep2;   dep3 ~~ 0*dep3
'
clpm <- 'lone2 ~ lone1 + dep1; dep2 ~ dep1 + lone1; lone3 ~ lone2 + dep2; dep3 ~ dep2 + lone2
         lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3'

# 取出标准化路径；RI-CLPM 的被试内变量名 wl/wd 改写成 lone/dep，便于与 CLPM 对齐
paths <- function(fit) {
  pe <- standardizedSolution(fit)
  pe <- pe[pe$op == "~" | (pe$op == "~~" & pe$lhs == "RI_lone" & pe$rhs == "RI_dep"), ]
  nm <- ifelse(pe$op == "~", paste(pe$rhs, "→", pe$lhs), "RI_lone ~~ RI_dep")
  nm <- gsub("wl", "lone", gsub("wd", "dep", nm))
  setNames(pe$est.std, nm)
}
# 注意：lavaan 0.7 拟合前后会保存并恢复随机数状态。若把 to_sums(gen_panel(...)) 直接作为参数传入，
# 数据要到 lavaan 内部才生成，随机数状态随后被恢复，每次都会抽到同一份样本。
# 所以先用 force(d) 在 lavaan 之外生成数据。
fit_both <- function(d, ...) {
  force(d)
  list(
    CLPM    = paths(sem(clpm, data = d, ...)),
    RICLPM  = paths(lavaan(riclpm, data = d, meanstructure = TRUE, int.ov.free = TRUE, ...)))
}

# ---- 1. 课程数据（与 L5-3.R 相同的模型）-----------------------------------
dat <- read_course_data()
wide <- data.frame(row.names = seq_len(nrow(dat)))
for (t in 1:3) {
  wide[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
  wide[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)])
}
course <- fit_both(wide, missing = "fiml")

# ---- 2. 真值：20 万人的大样本 ---------------------------------------------
set.seed(5302)
truth <- fit_both(to_sums(sim$gen_panel(200000)$X))

# ---- 3. 抽样波动：200 份 N = 800 的样本 -----------------------------------
R_REP <- 200
set.seed(5303)
reps <- lapply(seq_len(R_REP), function(r) {
  res <- tryCatch(suppressWarnings(fit_both(to_sums(sim$gen_panel(800)$X))), error = function(e) NULL)
  res
})
ok <- !vapply(reps, is.null, logical(1))
cat("200 次重复中成功拟合：", sum(ok), "次\n\n")

rows <- list()
for (m in c("CLPM", "RICLPM")) {
  sims <- do.call(rbind, lapply(reps[ok], `[[`, m))
  for (p in names(truth[[m]])) {
    rows[[length(rows) + 1]] <- data.frame(
      model = m, path = p,
      truth = truth[[m]][[p]], course = course[[m]][[p]],
      q05 = unname(quantile(sims[, p], .05)), q95 = unname(quantile(sims[, p], .95)),
      sd = sd(sims[, p]),
      pct = mean(sims[, p] <= course[[m]][[p]]))   # 课程样本的估计在 200 份样本中的百分位
  }
}
tab <- do.call(rbind, rows)
write.csv(tab, out("L5-3b_truth.csv"), row.names = FALSE)

cat("===== 标准化路径：真值（N = 200000）、课程样本、200 份 N = 800 样本的 90% 范围 =====\n")
show <- tab; show[, 3:7] <- round(show[, 3:7], 3); show$pct <- round(tab$pct, 2)
print(show, row.names = FALSE)
cat("\n读法：truth 是样本无限大时的值；course 是课程数据（N = 800）的估计；\n",
    "[q05, q95] 是同一生成模型下 200 份 N = 800 样本的估计范围；pct 是课程样本的估计排在第几个百分位。\n",
    "RI-CLPM 的被试内交叉滞后在 3 波、N = 800 时波动很大：单份样本的方向判断并不可靠。\n")
log_close()
