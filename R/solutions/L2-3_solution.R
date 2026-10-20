# 练习答案 L2-3：选题、反向计分、总分、按性别求均值（2.3-A）；孤独与抑郁“双高”名单（2.3-B）
source("R/_setup.R"); suppressPackageStartupMessages(library(tidyverse))
log_open("sol_L2-3_log.txt")
dat <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)
# ---- 2.3-A ----
res <- dat |>
  select(id, gender, starts_with("dep") & ends_with("_t1"), social_support_t1) |>
  mutate(support_rev = 6 - social_support_t1,                 # 1–5 → 5–1
         dep_sum_t1  = rowSums(across(dep1_t1:dep5_t1)),
         性别        = factor(gender, levels = c(0, 1), labels = c("男", "女")))
res |>
  group_by(性别) |>
  summarise(人数 = n(), 抑郁均值 = mean(dep_sum_t1), 支持缺乏均值 = mean(support_rev)) |>
  print()
print(cor(res$social_support_t1, res$support_rev))    # -1：反向只是翻转方向
# ---- 2.3-B ----
high <- dat |>
  mutate(lone_sum_t1 = rowSums(across(lone1_t1:lone4_t1)),
         dep_sum_t1  = rowSums(across(dep1_t1:dep5_t1))) |>
  filter(lone_sum_t1 >= 13, dep_sum_t1 >= 10) |>
  arrange(desc(dep_sum_t1)) |>
  select(id, lone_sum_t1, dep_sum_t1)
cat("\n孤独总分 ≥ 13 且抑郁总分 ≥ 10 的人数：", nrow(high), "\n")
print(high, n = 5)
log_close()
