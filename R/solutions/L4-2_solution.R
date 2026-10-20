# 练习答案 L4-2：3 波 × 6 题 宽 ↔ 长，并拆出 d1、d2（4.2-A）；长格式画 9 道题的均值折线（4.2-B）
source("R/_setup.R"); suppressPackageStartupMessages(library(tidyverse))
log_open("sol_L4-2_log.txt")
# ---- 4.2-A ----
wide <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)
six  <- c("lone1", "lone2", "lone3", "dep1", "dep2", "dep3")
w6 <- wide |> select(id, all_of(paste0(rep(six, 3), "_t", rep(1:3, each = 6))))   # 1 + 18 列

l6 <- w6 |> pivot_longer(-id, names_to = c(".value", "wave"), names_sep = "_t")
cat("长格式 l6 的维度：", dim(l6), "\n")                              # 2400 行 × 8 列

w6b <- l6 |> pivot_wider(names_from = wave, values_from = all_of(six), names_sep = "_t")
same <- isTRUE(all.equal(as.data.frame(w6), as.data.frame(w6b[, names(w6)])))
cat("转回宽格式后与原数据相同？", same, "\n")                          # TRUE
stopifnot(same)

d1 <- w6 |> select(id, all_of(paste0(six, "_t1")))
d2 <- w6 |> select(id, all_of(paste0(six, "_t2")))
stopifnot(nrow(d1) == nrow(d2), identical(d1$id, d2$id))
X <- as.matrix(d1[, -1]); Y <- as.matrix(d2[, -1])   # 去掉 id，得到 CLPN 用的两个矩阵
cat("d1、d2 各", nrow(d1), "行，ID 完全对应 ✔；X、Y 维度：", dim(X), "/", dim(Y), "\n\n")

# ---- 4.2-B ----
long <- wide |>                                       # 与 R/L4-2.R 相同：id + 27 个题目列 → 长格式
  select(id, all_of(c(vars_t(1), vars_t(2), vars_t(3)))) |>
  pivot_longer(-id, names_to = c(".value", "wave"), names_sep = "_t")
means <- long |>
  pivot_longer(lone1:dep5, names_to = "item", values_to = "score") |>
  group_by(wave, item) |>
  summarise(m = mean(score), .groups = "drop")
print(means |> pivot_wider(names_from = wave, values_from = m, names_prefix = "T") |>
        mutate(across(starts_with("T"), function(x) round(x, 2))), n = 9)
p <- ggplot(means, aes(x = wave, y = m, colour = item, group = item)) +
  geom_line() + geom_point() +
  labs(x = "波次", y = "题目均值")
ggsave(out("sol_L4-2_means.png"), p, width = 6, height = 4, dpi = 200)
cat("均值折线图已保存：R/output/sol_L4-2_means.png\n")
log_close()
