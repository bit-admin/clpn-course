# Solution L4-2: 3 waves x 6 items wide <-> long, extracting d1 and d2 (4.2-A);
# plotting mean trajectory lines for 9 items using long format (4.2-B)
source("R/_setup.R"); suppressPackageStartupMessages(library(tidyverse))
log_open("sol_L4-2_log.txt")
# ---- 4.2-A ----
wide <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)
six  <- c("lone1", "lone2", "lone3", "dep1", "dep2", "dep3")
w6 <- wide |> select(id, all_of(paste0(rep(six, 3), "_t", rep(1:3, each = 6))))   # 1 + 18 columns

l6 <- w6 |> pivot_longer(-id, names_to = c(".value", "wave"), names_sep = "_t")
cat("Dimensions of long-format l6:", dim(l6), "\n")                              # 2400 rows x 8 cols

w6b <- l6 |> pivot_wider(names_from = wave, values_from = all_of(six), names_sep = "_t")
same <- isTRUE(all.equal(as.data.frame(w6), as.data.frame(w6b[, names(w6)])))
cat("Identical to original data after pivoting back to wide format?", same, "\n") # TRUE
stopifnot(same)

d1 <- w6 |> select(id, all_of(paste0(six, "_t1")))
d2 <- w6 |> select(id, all_of(paste0(six, "_t2")))
stopifnot(nrow(d1) == nrow(d2), identical(d1$id, d2$id))
X <- as.matrix(d1[, -1]); Y <- as.matrix(d2[, -1])   # Drop id to obtain the two matrices for CLPN
cat("d1 and d2 have", nrow(d1), "rows each, IDs perfectly aligned ✔; X and Y dimensions:", dim(X), "/", dim(Y), "\n\n")

# ---- 4.2-B ----
long <- wide |>                                       # Same as R/L4-2.R: id + 27 item columns -> long format
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
  labs(x = "Wave", y = "Item Mean")
ggsave(out("sol_L4-2_means.png"), p, width = 6, height = 4, dpi = 200)
cat("Mean trajectory plot saved to: R/output/sol_L4-2_means.png\n")
log_close()
