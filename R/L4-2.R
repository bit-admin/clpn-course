# =====================================================================
# L4-2.R  宽格式与长格式：数据整形  (Wide vs long format; reshaping)
# CLPN 需要“对齐好的” T1 矩阵 d1 与 T2 矩阵 d2（同样的人、同样的题目顺序）
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(tidyverse))
log_open("L4-2_log.txt")
wide <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE) |>
  select(id, all_of(c(vars_t(1), vars_t(2), vars_t(3))))   # 只保留 id + 27 个题目列

# 宽 → 长：列名 "lone1_t2" 按 "_t" 拆成 题目名(.value) 和 波次(wave)
long <- wide |>
  pivot_longer(-id, names_to = c(".value", "wave"), names_sep = "_t")
print(head(long)); cat("长格式行数 =", nrow(long), "（= 800 人 × 3 波）\n")

# 长 → 宽：再变回来，并检查与原数据一致
wide2 <- long |> pivot_wider(names_from = wave, values_from = all_of(items), names_sep = "_t")
wide2 <- wide2[, names(wide)]
cat("转回宽格式后与原数据完全相同？", isTRUE(all.equal(as.data.frame(wide), as.data.frame(wide2))), "\n")

# 拆出 d1 与 d2 —— 用 vars_t() 保证题目顺序一致（比 ends_with() 更安全）
d1 <- wide |> select(all_of(vars_t(1)))
d2 <- wide |> select(all_of(vars_t(2)))
stopifnot(nrow(d1) == nrow(d2),
          identical(sub("_t1", "", names(d1)), sub("_t2", "", names(d2))))  # 检查顺序
cat("d1、d2 行数与题目顺序检查通过 ✔\n")

# ---- 课文补充：两个陷阱的演示 ----
# 陷阱 1：ends_with("_t1") 会选中你不想要的列（原始数据里还有 social_support_t1 等）
print(read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE) |>
        select(ends_with("_t1")) |> names())
# 陷阱 2：按行号拼接两个排序不同的文件
t1 <- wide |> select(id, ends_with("_t1"))
set.seed(42)
t2 <- wide |> select(id, ends_with("_t2")) |> slice_sample(prop = 1)   # 模拟“T2 文件顺序不同”
bad  <- bind_cols(t1, select(t2, -id))          # 按行号并排
good <- left_join(t1, t2, by = "id")            # 按 ID 匹配
print(cor(bad$dep1_t1,  bad$dep1_t2))
print(cor(good$dep1_t1, good$dep1_t2))
log_close()
