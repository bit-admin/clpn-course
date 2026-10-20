# =====================================================================
# assess_answers.R  期末考试 C 部分（R 小任务）的参考答案
# 期末页面 materials/assess_final.html 的 C 部分答案从本脚本的输出 R/output/assess_answers.csv 读取，不手写。
# 学习者做期末时请先自己在 R 里算，不要先运行本脚本。
# run_all.R 在全部课文脚本之后、答案脚本之前运行它（文件名不是 L*.R，所以单独列出）。
# 运行时间：几秒（EBIC 不做交叉验证，结果逐位可重复）。
# =====================================================================
source("R/_setup.R")
library(glmnet)
log_open("assess_answers_log.txt")
dat <- read_course_data()
B <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], rule = "ebic")   # T1 → T2，EBIC（γ = 0.5）
ans <- data.frame(
  key = c("C1", "C2", "C3", "C4", "C5"),
  value = c(mean(dat$lone1_t1),                            # C1 第 1 波 lone1 的均值
            cor(dat$lone3_t1, dat$dep1_t2),                # C2 T1 lone3 与 T2 dep1 的相关
            sum(dat$gender == 1),                          # C3 女性人数（gender = 1）
            sd(dat$dep1_t1),                               # C4 第 1 波 dep1 的标准差
            sum(cl_only(B) != 0)),                         # C5 EBIC 估计的 T1→T2 网络中非零交叉滞后边的条数
  task = c("mean(lone1_t1)", "cor(lone3_t1, dep1_t2)", "sum(gender == 1)", "sd(dep1_t1)",
           "sum(cl_only(clpn_estimate(T1, T2, rule = \"ebic\")) != 0)"))
ans$value <- round(ans$value, 3)
print(ans, row.names = FALSE)
write.csv(ans, out("assess_answers.csv"), row.names = FALSE)
log_close()
