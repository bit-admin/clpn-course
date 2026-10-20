# Exercise Solutions L2-6: Descriptive table for reporting and two plots (2.6-A); faceting (2.6-B)
# For the full Quarto template, see R/solutions/week06.qmd (open in RStudio and click Render)
source("R/_setup.R")
suppressPackageStartupMessages(library(tidyverse))
log_open("sol_L2-6_log.txt")
dat <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE) |>
  mutate(loneliness = rowSums(across(lone1_t1:lone4_t1)), depression = rowSums(across(dep1_t1:dep5_t1)),
         gender_label = factor(gender, levels = c(0, 1), labels = c("Male", "Female")))
dat |> group_by(gender_label) |>
  summarise(n = n(), lone_mean = mean(loneliness), dep_mean = mean(depression), dep_sd = sd(depression)) |>
  knitr::kable(digits = 2) |> print()
p1 <- ggplot(dat, aes(loneliness, depression)) + geom_jitter(width = .2, height = .2, alpha = .4) +
  geom_smooth(method = "lm", formula = y ~ x) + labs(x = "T1 Loneliness Total Score", y = "T1 Depression Total Score")
ggsave(out("sol_L2-6_facet.png"), p1 + facet_wrap(~ gender_label), width = 7, height = 3.6, dpi = 200)
cat("\nFaceted plot saved: R/output/sol_L2-6_facet.png (one panel per group with identical axes)\n")
log_close()
