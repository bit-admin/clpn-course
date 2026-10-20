# =====================================================================
# L1-1.R  变量与测量：数据从哪里来  (Variables & measurement)
# 目标：第一次“看一眼”课程数据，认识每一列是什么变量（variable）、
#       属于什么测量水平（level of measurement）。
# 运行：在 RStudio 中打开 clpn-course.Rproj，打开本文件，点 “Source”。
# =====================================================================
source("R/_setup.R")          # 共用准备工作（找文件夹、字体、常用函数）
log_open("L1-1_log.txt")      # 把屏幕输出同时保存到 R/output/L1-1_log.txt

dat <- read_course_data()     # 读入数据框（data frame）：800 行（人）× 34 列（变量）
cat("行数（个案 cases）=", nrow(dat), "；列数（变量 variables）=", ncol(dat), "\n\n")

# head() 看前 6 行；str() 看每列的类型（integer 整数 / numeric 数值 / character 字符）
print(head(dat[, 1:10]))
str(dat[, c("id", "lone1_t1", "dep1_t1", "gender", "age", "social_support_t1")])

# 数据字典（data dictionary / codebook）：每个变量的中英文含义
dict <- read.csv("data/data_dictionary.csv")
print(dict[, c("variable", "label_zh", "values")])

# 测量水平小结（手动整理，便于对照讲义）
lv <- data.frame(
  变量 = c("id", "gender", "lone1_t1", "dep1_t1", "age", "life_sat_t1"),
  测量水平 = c("定类 nominal（标签）", "定类 nominal（0/1）", "定序 ordinal（李克特 1–4）",
           "定序 ordinal（0–3）", "定比 ratio", "常当作定距 interval"))
print(lv)

# 每道题有哪些取值？table() 统计频数（frequency）
for (v in c("lone1_t1", "dep1_t1")) { cat("\n", v, "的取值分布：\n"); print(table(dat[[v]])) }

# 内部一致性信度 Cronbach's α（讲义“再加两行”）：孤独 4 题、抑郁 5 题，T1
# 在脚本里（Source / Rscript）结果不会自动显示，所以用 print()；在控制台逐行运行时可以省略 print()
cat("\nCronbach's α（T1）：孤独 4 题、抑郁 5 题\n")
lone_t1 <- dat[, c("lone1_t1", "lone2_t1", "lone3_t1", "lone4_t1")]
print(round(psych::alpha(lone_t1)$total$raw_alpha, 2))          # 孤独 4 题
print(round(psych::alpha(dat[, paste0("dep", 1:5, "_t1")])$total$raw_alpha, 2))   # 抑郁 5 题
log_close()
