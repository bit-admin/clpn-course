# =====================================================================
# L2-3.R  Data Frames & Introduction to tidyverse
# (Data frames & tidyverse)
# The native pipe operator |> reads as "and then"
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(tidyverse))
log_open("L2-3_log.txt")
dat <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)  # tibble (enhanced data frame)

phq <- dat |> select(id, gender, starts_with("dep") & ends_with("_t1"))  # Select columns: select()
print(phq, n = 5)

# Reverse scoring example: suppose social support requires reverse scoring (1-5 -> 5-1): new_value = 6 - old_value
dat <- dat |>
  mutate(support_rev = 6 - social_support_t1,                         # Create/modify columns: mutate()
         dep_sum_t1  = rowSums(across(c(dep1_t1:dep5_t1))))           # Generate sum score
dat |>
  mutate(gender_label = if_else(gender == 1, "Female", "Male")) |>
  group_by(gender_label) |>                                                    # Grouping
  summarise(n = n(), dep_mean = mean(dep_sum_t1), sd = sd(dep_sum_t1)) |>  # Summarizing
  print()
n_high <- dat |> filter(dep_sum_t1 >= 10) |> nrow()   # Filter rows: filter()
cat("Number of participants with depression sum score >= 10: ", n_high, "\n", sep = "")

# ---- Lesson Supplement: Differences Between $, [ ], and [[ ]] ----
print(dat$dep1_t1 |> head())            # Vector
print(dat[, "dep1_t1"] |> head(3))      # tibble returns a one-column tibble
print(dat[["dep1_t1"]] |> head())       # Vector (identical behavior for tibble and data.frame)

# ---- Lesson Supplement: Multiple Condition Filtering, Counting, and Sorting ----
print(dat |> filter(gender == 1, age < 30) |> nrow())      # Comma = "AND": females under age 30
print(dat |> count(gender))                                # Count
print(dat |> arrange(desc(dep_sum_t1)) |> select(id, dep_sum_t1) |> head(3))   # Top 3 participants by depression score
log_close()
