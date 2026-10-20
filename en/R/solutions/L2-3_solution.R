# Exercise Solutions L2-3: Selecting items, reverse scoring, sum scores, group means by gender (2.3-A); "dual-high" loneliness and depression roster (2.3-B)
source("R/_setup.R"); suppressPackageStartupMessages(library(tidyverse))
log_open("sol_L2-3_log.txt")
dat <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)
# ---- 2.3-A ----
res <- dat |>
  select(id, gender, starts_with("dep") & ends_with("_t1"), social_support_t1) |>
  mutate(support_rev  = 6 - social_support_t1,                 # 1–5 -> 5–1
         dep_sum_t1   = rowSums(across(dep1_t1:dep5_t1)),
         gender_label = factor(gender, levels = c(0, 1), labels = c("Male", "Female")))
res |>
  group_by(gender_label) |>
  summarise(n = n(), dep_mean = mean(dep_sum_t1), lack_support_mean = mean(support_rev)) |>
  print()
print(cor(res$social_support_t1, res$support_rev))    # -1: reverse scoring simply flips the direction
# ---- 2.3-B ----
high <- dat |>
  mutate(lone_sum_t1 = rowSums(across(lone1_t1:lone4_t1)),
         dep_sum_t1  = rowSums(across(dep1_t1:dep5_t1))) |>
  filter(lone_sum_t1 >= 13, dep_sum_t1 >= 10) |>
  arrange(desc(dep_sum_t1)) |>
  select(id, lone_sum_t1, dep_sum_t1)
cat("\nNumber of participants with loneliness >= 13 and depression >= 10: ", nrow(high), "\n")
print(high, n = 5)
log_close()
