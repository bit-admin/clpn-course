# Exercise Solutions L1-4: Comparing the "expected" correlation matrix with actual data
source("R/_setup.R")
log_open("sol_L1-4_log.txt")
dat <- read_course_data()
d <- data.frame(Loneliness = rowSums(dat[, paste0(lone_items, "_t1")]),
                Sleep_Duration = dat$sleep_hours_t1,
                Depression = rowSums(dat[, paste0(dep_items, "_t1")]),
                Social_Support = dat$social_support_t1)
expected <- matrix(c("1", "-", "+", "-",
                     "-", "1", "-", "+",
                     "+", "-", "1", "-",
                     "-", "+", "-", "1"), 4, byrow = TRUE, dimnames = list(names(d), names(d)))
print(expected, quote = FALSE); print(round(cor(d), 2))
# Confounding example: "Neighborhoods with more community activity centers receive more helpline calls" —
# Both are influenced by "population size"; controlling for population, the association may disappear.

# ---- Exercise 1.4-C: Correlation matrix among the 9 items at T1 ----
cat("\n1.4-C: Correlation matrix among the 9 items at T1\n")
R <- round(cor(dat[, vars_t(1)]), 2)
print(R)
# (1) Strongest pair of correlated items (lower triangle only, excluding diagonal and duplicates)
low <- R; low[upper.tri(low, diag = TRUE)] <- NA
idx <- which(low == max(low, na.rm = TRUE), arr.ind = TRUE)
cat("(1) Strongest correlation: ", paste(rownames(R)[idx[, 1]], "—", colnames(R)[idx[, 2]], collapse = "; "),
    " r =", max(low, na.rm = TRUE), "\n")
# (2) Cross-construct block (rows = loneliness items, cols = depression items): 4 x 5 block
cross <- R[paste0(lone_items, "_t1"), paste0(dep_items, "_t1")]
print(cross)
idx2 <- which(cross == max(cross), arr.ind = TRUE)
cat("(2) Strongest cross-construct correlation: ", paste(rownames(cross)[idx2[, 1]], "—", colnames(cross)[idx2[, 2]], collapse = "; "),
    " r =", max(cross), "\n")
# (3) dep2_t1 (Loss of interest) and dep4_t1 (Fatigue): Three types of correlation
x3 <- dat[, c("dep2_t1", "dep4_t1")]
cat("(3) Pearson =", round(cor(x3)[1, 2], 3),
    " Spearman =", round(cor(x3, method = "spearman")[1, 2], 3),
    " Polychoric =", round(psych::polychoric(x3)$rho[1, 2], 3), "\n")
# Polychoric correlation is the highest: 0–3 scores have only 4 categories with floor effects; Pearson treats coarse ordinal categories as precise continuous values, attenuating the correlation;
# Polychoric correlation estimates the correlation between the underlying latent continuous tendencies.
log_close()
