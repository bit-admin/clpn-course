# 练习答案 L2-6：报告用的描述表与两张图（2.6-A）；分面（2.6-B）
# 完整的 Quarto 模板见 R/solutions/week06.qmd（在 RStudio 中打开后点 Render）
source("R/_setup.R")
suppressPackageStartupMessages(library(tidyverse))
log_open("sol_L2-6_log.txt")
dat <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE) |>
  mutate(孤独 = rowSums(across(lone1_t1:lone4_t1)), 抑郁 = rowSums(across(dep1_t1:dep5_t1)),
         性别 = factor(gender, levels = c(0, 1), labels = c("男", "女")))
dat |> group_by(性别) |>
  summarise(n = n(), 孤独均值 = mean(孤独), 抑郁均值 = mean(抑郁), 抑郁SD = sd(抑郁)) |>
  knitr::kable(digits = 2) |> print()
p1 <- ggplot(dat, aes(孤独, 抑郁)) + geom_jitter(width = .2, height = .2, alpha = .4) +
  geom_smooth(method = "lm", formula = y ~ x) + labs(x = "T1 孤独总分", y = "T1 抑郁总分")
ggsave(out("sol_L2-6_facet.png"), p1 + facet_wrap(~ 性别), width = 7, height = 3.6, dpi = 200)
cat("\n分面图已保存：R/output/sol_L2-6_facet.png（两组各一张小图、坐标轴相同）\n")
log_close()
