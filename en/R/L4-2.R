# =====================================================================
# L4-2.R  Wide vs. long format: data reshaping
# CLPN requires "properly aligned" T1 matrix d1 and T2 matrix d2
# (same participants, identical item ordering)
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages(library(tidyverse))
log_open("L4-2_log.txt")
wide <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE) |>
  select(id, all_of(c(vars_t(1), vars_t(2), vars_t(3))))   # Retain only id + 27 item columns

# Wide -> Long: column name "lone1_t2" is split by "_t" into item name (.value) and wave (wave)
long <- wide |>
  pivot_longer(-id, names_to = c(".value", "wave"), names_sep = "_t")
print(head(long)); cat("Long format rows =", nrow(long), "(= 800 participants * 3 waves)\n")

# Long -> Wide: reshape back, and verify consistency with original data
wide2 <- long |> pivot_wider(names_from = wave, values_from = all_of(items), names_sep = "_t")
wide2 <- wide2[, names(wide)]
cat("Identical to original data after pivoting back to wide?", isTRUE(all.equal(as.data.frame(wide), as.data.frame(wide2))), "\n")

# Extract d1 and d2 -- use vars_t() to guarantee identical item ordering (safer than ends_with())
d1 <- wide |> select(all_of(vars_t(1)))
d2 <- wide |> select(all_of(vars_t(2)))
stopifnot(nrow(d1) == nrow(d2),
          identical(sub("_t1", "", names(d1)), sub("_t2", "", names(d2))))  # Check ordering
cat("d1 and d2 row counts and item ordering check passed ✔\n")

# ---- Supplementary: Demonstration of two pitfalls ----
# Pitfall 1: ends_with("_t1") selects unwanted columns (raw data also contains social_support_t1, etc.)
print(read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE) |>
        select(ends_with("_t1")) |> names())
# Pitfall 2: Row-binding two files with different sort orders
t1 <- wide |> select(id, ends_with("_t1"))
set.seed(42)
t2 <- wide |> select(id, ends_with("_t2")) |> slice_sample(prop = 1)   # Simulate "T2 file in different order"
bad  <- bind_cols(t1, select(t2, -id))          # Side-by-side by row position
good <- left_join(t1, t2, by = "id")            # Match by ID
print(cor(bad$dep1_t1,  bad$dep1_t2))
print(cor(good$dep1_t1, good$dep1_t2))
log_close()
