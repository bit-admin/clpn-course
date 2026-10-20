# =====================================================================
# L2-1.R  第一行 R 代码  (Your first R code)
# 选中一行，按 Ctrl+Enter（Mac: Cmd+Enter）运行，结果出现在下方 Console。
# =====================================================================
# 这是注释：R 会忽略 # 后面的内容
1 + 1
age <- 21                    # <- 是“赋值”（assignment）：把 21 存进名为 age 的对象
age * 365                    # 年龄换算成天数（约）
scores <- c(3, 5, 2, 4)      # c() 把数字组合成向量（vector）
mean(scores)                 # 函数（function）：名字 + 圆括号
# ?mean                      # 打开帮助页面（在 RStudio 里去掉 # 再运行）
sessionInfo()$R.version$version.string

# ---- 以下供课程核对用：把本课课文里的输出写进 R/output/L2-1_log.txt ----
# 课文“控制台输出”“输出”两个框就来自这个日志。初学时只看上面几行即可，这一段可以先跳过。
source("R/_setup.R")                       # 设好工作目录与 log_open()（2.4 课会讲）
log_open("L2-1_log.txt")
print(1 + 1)
print(age * 365)
print(mean(scores))
print(sessionInfo()$R.version$version.string)
# 赋值 vs 比较
x <- 5
print(x == 5)
print(x == 3)
my_age <- 21; friend_age <- 23; teacher_age <- 45
print(my_age + friend_age + teacher_age)
log_close()
