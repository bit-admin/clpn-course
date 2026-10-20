# =====================================================================
# L2-6.R  ggplot2 Plotting & Reproducible Reports
# (ggplot2 & reproducible reports)
# Also renders R/L2-6_report.Rmd to HTML (if rmarkdown + pandoc are installed)
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(tidyverse))
dat <- read_course_data()
long <- dat |>
  mutate(Loneliness = rowSums(across(paste0(lone_items, "_t1"))),
         Depression = rowSums(across(paste0(dep_items, "_t1"))),
         Gender = if_else(gender == 1, "Female", "Male"))
# ggplot syntax: data + aes() mapping + geom_*() geometric objects
p1 <- ggplot(long, aes(x = Loneliness, y = Depression, colour = Gender)) +
  geom_jitter(alpha = .4, width = .2, height = .2) +
  geom_smooth(method = "lm", formula = y ~ x) +
  labs(title = "T1 Loneliness and Depression", x = "Loneliness Total Score", y = "Depression Total Score")
ggsave(out("L2-6_scatter.png"), p1, width = 6, height = 4.5, dpi = 200)
p2 <- ggplot(long, aes(x = Depression, fill = Gender)) + geom_histogram(binwidth = 1, position = "dodge") +
  labs(title = "Depression Total Score Distribution", x = "Depression Total Score", y = "Count")
ggsave(out("L2-6_hist.png"), p2, width = 6, height = 4, dpi = 200)

if (requireNamespace("rmarkdown", quietly = TRUE) && rmarkdown::pandoc_available()) {
  rmarkdown::render("R/L2-6_report.Rmd", output_dir = out_dir, quiet = TRUE,
                    knit_root_dir = getwd())
  cat("Report generated: R/output/L2-6_report.html\n")
} else cat("Pandoc not found: Open L2-6_report.Rmd in RStudio and click Knit.\n")

# ---- Lesson Supplement: Grouped Boxplot -> R/output/L2-6_box.png ----
# theme_minimal() overrides the default font configured in _setup.R, so specify base_family = plot_font
p3 <- ggplot(long, aes(x = Gender, y = Depression, fill = Gender)) +
  geom_boxplot(alpha = .6, outlier.shape = NA) +     # Do not plot outliers separately (all points are jittered below)
  geom_jitter(width = .15, height = .2, alpha = .2) +
  labs(title = "T1 Depression Total Score: By Gender", x = NULL, y = "Depression Total Score") +
  theme_minimal(base_family = plot_font) + theme(legend.position = "none")
ggsave(out("L2-6_box.png"), p3, width = 5, height = 4, dpi = 150)
