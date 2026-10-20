# 练习答案 L2-1：第一份脚本（2.1-A）、读帮助页面（2.1-B）、最小可复现例子（2.1-C）
source("R/_setup.R")
log_open("sol_L2-1_log.txt")
# ---- 2.1-A week02.R ----
my_age <- 21                 # 换成你的真实年龄
print(my_age * 365)          # 约等于天数（没算闰年）
print(my_age * 365.25)       # 稍微精确一点
a <- 3; b <- 4.5; c_val <- 10   # 不用 c 作名字，避免和 c() 混淆
print(a + b + c_val)
# 故意写错（用 tryCatch 包起来，这样脚本不会停下；你自己练习时直接运行 sum(a, b, c_vall) 即可）
msg <- tryCatch(sum(a, b, c_vall), error = function(e) conditionMessage(e))
cat("故意写错得到的报错：", msg, "\n→ 对象名多打了一个 l，R 找不到这个对象。\n\n")
# ---- 2.1-B round() 的“五成双” ----
cat("round(2.5) =", round(2.5), "；round(3.5) =", round(3.5), "；round(0.125, 2) =", round(0.125, 2), "\n")
cat("（R 对正好在中间的数取最近的偶数：IEC 60559 标准）\n\n")
# ---- 2.1-C 最小可复现例子 ----
x <- c(1, 2, NA)
cat("mean(x) =", mean(x), "；mean(x, na.rm = TRUE) =", mean(x, na.rm = TRUE), "\n")
cat("R 版本：", R.version.string, "\n")
log_close()
