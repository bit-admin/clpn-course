# =====================================================================
# L2-2.R  R 基本语法：向量、数据类型与函数  (Vectors, data types, functions)
# =====================================================================
source("R/_setup.R")
log_open("L2-2_log.txt")
sleep <- c(7, 5.5, 8, NA, 6, 4.5, 7.5, NA, 9, 5)   # NA = 缺失值（missing value）
print(class(sleep))                                # "numeric" 数值型
print(mean(sleep))                                 # 有 NA 时结果是 NA！
print(mean(sleep, na.rm = TRUE))                   # na.rm = TRUE：先去掉 NA
print(which(sleep < 6))                            # 第几个人睡眠少于 6 小时
print(sleep[sleep < 6 & !is.na(sleep)])            # 逻辑索引（logical indexing）

# 其他数据类型：字符（character）、逻辑（logical）、因子（factor）
name   <- c("小李", "小王"); is_student <- c(TRUE, FALSE)
gender <- factor(c(1, 0), levels = c(0, 1), labels = c("男", "女"))
print(gender)

# 自己写函数（function）
zscore <- function(x) (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
print(round(cbind(我的zscore = zscore(sleep), scale函数 = as.numeric(scale(sleep))), 3))

# ---- 课文补充：更多索引与向量化 ----
print(length(sleep))          # 元素个数
print(sum(is.na(sleep)))      # 缺失个数
print(sleep * 60)             # 向量化：每个值都换成分钟
print(sleep[c(1, 3)])         # 第 1、3 个
print(sleep < 6)              # 逐个比较，NA 的比较结果仍是 NA
print(sum(sleep < 6, na.rm = TRUE))   # TRUE 当作 1：少于 6 小时的人数

# ---- 课文补充：类型陷阱 ----
# 警告（warning）不会进入 sink() 日志，这里把它接住，按控制台的样子打印出来
wmsg <- ""
v <- withCallingHandlers(as.numeric(c("3", "4", "五")),    # 字符转数字：转不了的变成 NA
                         warning = function(w) { wmsg <<- conditionMessage(w); invokeRestart("muffleWarning") })
print(v); cat("Warning message:\n", wmsg, "\n", sep = "")
dat <- read.csv("data/clpn_sim_wide.csv")
g <- factor(dat$gender, levels = c(0, 1), labels = c("男", "女"))
print(table(g))
log_close()
