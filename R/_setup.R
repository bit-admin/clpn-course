# =====================================================================
# _setup.R —— 所有课程脚本共用的“准备工作”（common setup）
# 每个 Lx-y.R 脚本第一行都会 source("R/_setup.R")，你不需要单独运行它。
# 它做 4 件事：
#   1) 找到课程根目录（clpn-course 文件夹），并把它设为工作目录（working directory）
#   2) 建好输出文件夹 R/output/
#   3) 设置中文字体，避免图里的中文变成方框“□□”
#   4) 定义几个本课程反复用到的小函数（helper functions），例如 clpn_estimate()
# =====================================================================

## 1) 找课程根目录：从当前目录往上找，直到发现 data/clpn_sim_wide.csv
find_root <- function() {
  d <- normalizePath(getwd())
  for (i in 1:4) {
    if (file.exists(file.path(d, "data", "clpn_sim_wide.csv"))) return(d)
    d <- dirname(d)
  }
  stop("找不到课程文件夹！请在 RStudio 中打开 clpn-course.Rproj 后再运行。\n",
       "Cannot find course root: open clpn-course.Rproj in RStudio first.")
}
setwd(find_root())

## 2) 输出文件夹
out_dir <- file.path("R", "output")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
out <- function(name) file.path(out_dir, name)   # out("L1-2_hist.png") -> "R/output/L1-2_hist.png"
# 有先后依赖的脚本在开头调用它：前置结果文件不存在时，停下并说明应先运行哪个脚本
# need_output("L6-4_dep_anx_items.csv", "R/L6-4.R")
need_output <- function(files, script, chain = NULL) {
  miss <- files[!file.exists(out(files))]
  if (length(miss) == 0) return(invisible(TRUE))
  stop("\n缺少前置结果文件：", paste(out(miss), collapse = "、"),
       "\n请先运行 ", script, " 生成它，再运行本脚本。",
       if (!is.null(chain)) paste0("\n完整运行顺序：", chain) else "",
       "\n（也可以运行 source(\"R/run_all.R\")，按课程顺序一次运行全部脚本。）", call. = FALSE)
}

## 3) 中文字体（Windows / Mac / Linux 不同）
cn_font <- switch(Sys.info()[["sysname"]],
                  Windows = "sans",               # Windows 的 png() 默认能显示中文
                  Darwin  = "PingFang SC",        # Mac 自带的“苹方”
                  "Noto Sans CJK SC")             # Linux：需安装 fonts-noto-cjk
# 打开一个 PNG 画布；画完后必须 dev.off() 才会真正写入文件
png_open <- function(name, width = 1800, height = 1400, res = 220) {
  if (.Platform$OS.type == "windows") png(out(name), width, height, res = res)
  else png(out(name), width, height, res = res, type = if (capabilities("cairo")) "cairo" else NULL,
           family = cn_font)
  par(family = cn_font)
}
if (requireNamespace("ggplot2", quietly = TRUE))
  ggplot2::theme_set(ggplot2::theme_bw(base_family = cn_font))

## 4) 课程常用对象与函数 ---------------------------------------------------
items     <- c("lone1", "lone2", "lone3", "lone4", "dep1", "dep2", "dep3", "dep4", "dep5")
lone_items <- items[1:4]; dep_items <- items[5:9]
item_zh   <- c(lone1 = "缺少陪伴", lone2 = "被冷落", lone3 = "与人隔绝", lone4 = "无人理解",
               dep1 = "情绪低落", dep2 = "兴趣丧失", dep3 = "睡眠问题", dep4 = "疲乏", dep5 = "无价值感")
comm      <- c(rep("孤独", 4), rep("抑郁", 5))          # 每个节点属于哪个构念（社群 community）
groups_list <- list(孤独 = 1:4, 抑郁 = 5:9)              # qgraph 的分组参数
vars_t    <- function(t) paste0(items, "_t", t)          # vars_t(1) -> "lone1_t1" ... "dep5_t1"
read_course_data <- function() read.csv("data/clpn_sim_wide.csv")
true_B    <- function() as.matrix(read.csv("data/true_B_population.csv", row.names = 1))

# ---- CLPN 估计函数（逐节点 LASSO 回归 nodewise regression；“仅 LASSO”CLPN，
#      即 Wysocki et al., 2025 完整流程的第 1 步；SEM 重估见 R/L7-5b.R）----
# X: T 时刻题目矩阵；Y: T+1 时刻题目矩阵（同样的题目顺序、同样的个案）
# rule: "lambda.min"（交叉验证误差最小）或 "lambda.1se"（更稀疏，更保守）
#       或 "ebic"（用扩展 BIC 选 λ，见 7.2 课 / 9.2 课）
# 返回 p × p 矩阵 B：B[k, j] = 从 T 的 k 指向 T+1 的 j
clpn_estimate <- function(X, Y, rule = "lambda.min", nfolds = 10, covariates = NULL,
                          gamma = 0.5) {
  # 输入检查：X、Y 必须是同样的人（行数相同）、同样的题目、同样的顺序，且没有缺失值
  stem <- function(M) sub("_t[0-9]+$", "", colnames(M))   # "lone1_t1" -> "lone1"
  if (ncol(X) != ncol(Y) || nrow(X) != nrow(Y))
    stop("X 是 ", nrow(X), " 行 × ", ncol(X), " 列，Y 是 ", nrow(Y), " 行 × ", ncol(Y),
         " 列：两者必须是同一批人、同一组题目（4.2 课：用 vars_t(1)、vars_t(2) 选列）。", call. = FALSE)
  if (!is.null(colnames(X)) && !is.null(colnames(Y)) && !identical(stem(X), stem(Y)))
    stop("X 与 Y 的题目顺序不一致（去掉 _t1、_t2 后缀后比较）：\n  X：", paste(stem(X), collapse = " "),
         "\n  Y：", paste(stem(Y), collapse = " "),
         "\n请用 dat[, vars_t(1)] 和 dat[, vars_t(2)] 按同一份题目清单选列（4.2 课）。", call. = FALSE)
  for (nm in c("X", "Y", "covariates")) {
    M <- get(nm)
    if (!is.null(M) && anyNA(M))
      stop(nm, " 中有 ", sum(is.na(M)), " 个缺失值（NA），涉及 ", sum(!stats::complete.cases(M)), " 个人；",
           "glmnet 不能处理缺失值。\n请先处理缺失：例如对 X、Y（和协变量）一起做 na.omit() 只保留完整个案，",
           "或先做多重插补（4.3 课），并在报告中说明处理方法。", call. = FALSE)
  }
  X <- scale(as.matrix(X)); Y <- scale(as.matrix(Y))
  p <- ncol(X); labs <- if (is.null(colnames(X))) paste0("V", seq_len(p)) else stem(X)
  Z <- X; pf <- rep(1, p)
  if (!is.null(covariates)) {                     # 协变量：不惩罚（penalty.factor = 0）
    C <- scale(as.matrix(covariates)); Z <- cbind(X, C); pf <- c(pf, rep(0, ncol(C)))
  }
  B <- matrix(0, p, p, dimnames = list(labs, labs))
  for (j in seq_len(p)) {
    if (rule == "ebic") {
      fit <- glmnet::glmnet(Z, Y[, j], alpha = 1, penalty.factor = pf)
      n <- nrow(Z); rss <- (1 - fit$dev.ratio) * fit$nulldev
      ebic <- n * log(rss / n) + fit$df * log(n) + 2 * gamma * fit$df * log(ncol(Z))
      b <- as.numeric(coef(fit, s = fit$lambda[which.min(ebic)]))[-1]
    } else {
      cvfit <- glmnet::cv.glmnet(Z, Y[, j], alpha = 1, nfolds = nfolds, penalty.factor = pf)
      b <- as.numeric(coef(cvfit, s = rule))[-1]
    }
    B[, j] <- b[1:p]                               # 只保留题目的系数（去掉截距和协变量）
  }
  B
}
# 把对角线（自回归）去掉，只留交叉滞后边
cl_only <- function(B) { diag(B) <- 0; B }
# 把矩阵变成“边列表”（edge list）：from, to, weight
edge_list <- function(B, drop_zero = TRUE) {
  e <- data.frame(from = rep(rownames(B), times = ncol(B)),
                  to   = rep(colnames(B), each = nrow(B)),
                  weight = as.vector(B))
  e$type <- ifelse(e$from == e$to, "AR 自回归", "CL 交叉滞后")
  if (drop_zero) e <- e[e$weight != 0, ]
  e[order(-abs(e$weight)), ]
}
# 记录日志：同时打印到屏幕并写入 R/output/<name>.txt
log_open  <- function(name) sink(out(name), split = TRUE)
log_close <- function() sink()
