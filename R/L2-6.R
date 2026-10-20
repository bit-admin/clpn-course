# =====================================================================
# L2-6.R  ggplot2 绘图与可复现报告  (ggplot2 & reproducible reports)
# 同时会把 R/L2-6_report.Rmd 渲染为 HTML（如果安装了 rmarkdown + pandoc）
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(tidyverse))
dat <- read_course_data()
long <- dat |>
  mutate(孤独 = rowSums(across(paste0(lone_items, "_t1"))),
         抑郁 = rowSums(across(paste0(dep_items, "_t1"))),
         性别 = if_else(gender == 1, "女", "男"))
# ggplot 的语法：数据 + 映射 aes() + 几何对象 geom_*()
p1 <- ggplot(long, aes(x = 孤独, y = 抑郁, colour = 性别)) +
  geom_jitter(alpha = .4, width = .2, height = .2) +
  geom_smooth(method = "lm", formula = y ~ x) +
  labs(title = "T1 孤独感与抑郁", x = "孤独总分", y = "抑郁总分")
ggsave(out("L2-6_scatter.png"), p1, width = 6, height = 4.5, dpi = 200)
p2 <- ggplot(long, aes(x = 抑郁, fill = 性别)) + geom_histogram(binwidth = 1, position = "dodge") +
  labs(title = "抑郁总分分布", x = "抑郁总分", y = "人数")
ggsave(out("L2-6_hist.png"), p2, width = 6, height = 4, dpi = 200)

if (requireNamespace("rmarkdown", quietly = TRUE) && rmarkdown::pandoc_available()) {
  rmarkdown::render("R/L2-6_report.Rmd", output_dir = out_dir, quiet = TRUE,
                    knit_root_dir = getwd())
  cat("报告已生成：R/output/L2-6_report.html\n")
} else cat("未找到 pandoc：请在 RStudio 中打开 L2-6_report.Rmd 点 Knit。\n")

# ---- 课文补充：分组箱线图 → R/output/L2-6_box.png ----
# theme_minimal() 会换掉 _setup.R 设好的中文字体，所以要写 base_family = cn_font
p3 <- ggplot(long, aes(x = 性别, y = 抑郁, fill = 性别)) +
  geom_boxplot(alpha = .6, outlier.shape = NA) +     # 不单独画离群点（下面已画出所有点）
  geom_jitter(width = .15, height = .2, alpha = .2) +
  labs(title = "T1 抑郁总分：按性别", x = NULL, y = "抑郁总分") +
  theme_minimal(base_family = cn_font) + theme(legend.position = "none")
ggsave(out("L2-6_box.png"), p3, width = 5, height = 4, dpi = 150)
