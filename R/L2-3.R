# =====================================================================
# L2-3.R  数据框与 tidyverse 入门  (Data frames & tidyverse)
# 管道符 |> 读作“然后”（and then）
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(tidyverse))
log_open("L2-3_log.txt")
dat <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)  # tibble（加强版数据框）

phq <- dat |> select(id, gender, starts_with("dep") & ends_with("_t1"))  # 选列 select
print(phq, n = 5)

# 反向计分（reverse scoring）示例：假设社会支持需要反向（1–5 → 5–1）：新值 = 6 - 原值
dat <- dat |>
  mutate(support_rev = 6 - social_support_t1,                         # 新建/修改列 mutate
         dep_sum_t1  = rowSums(across(c(dep1_t1:dep5_t1))))           # 生成总分
dat |>
  mutate(性别 = if_else(gender == 1, "女", "男")) |>
  group_by(性别) |>                                                    # 分组
  summarise(人数 = n(), 抑郁均值 = mean(dep_sum_t1), 标准差 = sd(dep_sum_t1)) |>  # 汇总
  print()
n_high <- dat |> filter(dep_sum_t1 >= 10) |> nrow()   # 筛选行 filter
cat("抑郁总分 ≥ 10 的人数：", n_high, "\n")

# ---- 课文补充：$ 与 [ ] 的区别 ----
print(dat$dep1_t1 |> head())            # 向量
print(dat[, "dep1_t1"] |> head(3))      # tibble 返回的是一列的 tibble
print(dat[["dep1_t1"]] |> head())       # 向量（对 tibble 和 data.frame 都一样）

# ---- 课文补充：多条件筛选、计数、排序 ----
print(dat |> filter(gender == 1, age < 30) |> nrow())      # 逗号 = “并且”：30 岁以下女性
print(dat |> count(gender))                                # 计数
print(dat |> arrange(desc(dep_sum_t1)) |> select(id, dep_sum_t1) |> head(3))   # 抑郁总分最高的 3 人
log_close()
