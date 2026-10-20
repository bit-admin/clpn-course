# =====================================================================
# simulate_data.R — Simulate 3-wave loneliness <-> depression panel data for the course
# Simulate a 3-wave loneliness <-> depression panel with a KNOWN structure
# ---------------------------------------------------------------------
# Why use simulated data?
#   Because we know the "ground truth" in advance. After learning CLPN,
#   you can compare your estimated network with the true network to verify whether
#   the method can "recover" the true edges.
#
# How to run: Open clpn-course.Rproj in RStudio, then source("data/simulate_data.R")
#   Or in a terminal: Rscript data/simulate_data.R    (working directory = clpn-course folder)
# Outputs (all inside the data/ folder):
#   clpn_sim_wide.csv        Primary dataset (wide format), N = 800, 3 waves, 9 items + covariates
#   clpn_sim_wide.sav        Same dataset in SPSS format (for the Lesson 2.4 .sav import exercise)
#   true_B_within.csv        The "within-person truth": data-generating within-person lagged coefficients (row = T, col = T+1)
#   true_B_population.csv    The "population target": what standard CLPN targets in the population (including trait confounding),
#                            obtained by running nodewise OLS on standardized T1 items predicting each T2 item in an N = 200,000 super-sample
#   data_dictionary.csv      Bilingual data dictionary (see also data_dictionary.md)
# =====================================================================

set.seed(20261016)          # Random seed: ensures identical simulated data on every run

## ---- 0. Item (node) definitions ------------------------------------
items <- c("lone1", "lone2", "lone3", "lone4", "dep1", "dep2", "dep3", "dep4", "dep5")
p <- length(items)          # 9 nodes
is_lone <- grepl("lone", items)

## ---- 1. True within-person lagged structure B -----------------------
# Convention (consistent with qgraph): B[k, j] = coefficient from item k at time T predicting item j at time T+1
B <- matrix(0, p, p, dimnames = list(items, items))
diag(B) <- ifelse(is_lone, 0.35, 0.30)       # Autoregressions (AR)
# Cross-lagged edges (CL) — designed with "Loneliness -> Depression" slightly stronger than "Depression -> Loneliness"
B["lone3", "dep1"] <-  0.18   # Feeling isolated -> Depressed mood
B["lone1", "dep2"] <-  0.14   # Lack of companionship -> Loss of interest
B["lone4", "dep5"] <-  0.12   # No one understands me -> Worthlessness
B["dep2",  "lone3"] <- 0.12   # Loss of interest -> Feeling isolated (social withdrawal)
B["dep3",  "dep4"] <-  0.16   # Sleep problems -> Fatigue
B["dep1",  "dep5"] <-  0.10   # Depressed mood -> Worthlessness
B["lone2", "lone4"] <- 0.10   # Feeling left out -> No one understands me
B["dep4",  "lone2"] <- -0.15  # Fatigue -> Feeling left out (one negative edge, used to illustrate the difference between EI and strength)

## ---- 2. Contemporaneous residual (innovation) covariance Psi --------
# Items within the same construct covary together (correlation .35), across constructs .15
R_in <- matrix(0.15, p, p); R_in[is_lone, is_lone] <- 0.35; R_in[!is_lone, !is_lone] <- 0.35
diag(R_in) <- 1

# Stationary distribution: Sigma = t(B) %*% Sigma %*% B + Psi, solved iteratively
# Scale Psi so that Var(W) ≈ 1
Sigma <- diag(p)
for (it in 1:500) {
  Psi   <- R_in * sqrt(outer(1 - diag(t(B) %*% Sigma %*% B), 1 - diag(t(B) %*% Sigma %*% B)))
  Sigma <- t(B) %*% Sigma %*% B + Psi
}

## ---- 3. Stable traits (random intercept, between-person) ------------
# Loneliness trait and depression trait correlate at .50; trait variance per item is ~0.40 (relative to within-person variance 1)
gen_panel <- function(N) {
  trait <- MASS::mvrnorm(N, c(0, 0), matrix(c(1, .5, .5, 1), 2))
  RI <- cbind(trait[, rep(1, 4)], trait[, rep(2, 5)]) * sqrt(0.40) +
        matrix(rnorm(N * p, 0, sqrt(0.05)), N, p)
  female <- rbinom(N, 1, 0.55)
  W <- vector("list", 3)
  W[[1]] <- MASS::mvrnorm(N, rep(0, p), Sigma)
  for (t in 2:3) W[[t]] <- W[[t - 1]] %*% B + MASS::mvrnorm(N, rep(0, p), Psi)
  # Observed continuous latent scores = trait + within-person deviation + females score 0.2 higher on depression items
  X <- lapply(W, function(w) { x <- RI + w; x[, !is_lone] <- x[, !is_lone] + 0.2 * female; x })
  list(X = X, female = female, trait = trait)
}

# Categorize continuous scores into Likert categories
# Loneliness: 1 = Never ... 4 = Often (similar to UCLA-3); Depression: 0 = Not at all ... 3 = Nearly every day (similar to PHQ-9), right-skewed
to_likert <- function(x) {
  out <- x
  sdx <- 1.2
  out[, is_lone]  <- as.integer(cut(x[, is_lone] / sdx,  c(-Inf, -0.6, 0.4, 1.2, Inf))) # 1..4
  out[, !is_lone] <- as.integer(cut(x[, !is_lone] / sdx, c(-Inf, 0.1, 0.9, 1.6, Inf))) - 1L # 0..3
  out
}

## ---- 4. Course primary dataset: N = 800 -----------------------------
N <- 800
sim <- gen_panel(N)
wide <- data.frame(id = sprintf("P%03d", 1:N))
for (t in 1:3) {
  lik <- to_likert(sim$X[[t]]); colnames(lik) <- paste0(items, "_t", t)
  wide <- cbind(wide, lik)
}
wide$gender <- sim$female                                   # 0 = male, 1 = female
wide$age    <- pmin(pmax(round(rnorm(N, 45, 15)), 18), 85)  # Age
# Social support (1–5, higher is better): negatively correlated with loneliness trait
wide$social_support_t1 <- round(pmin(pmax(3.4 - 0.55 * sim$trait[, 1] + rnorm(N, 0, .6), 1), 5), 1)
# Sleep duration (hours): negatively correlated with T1 sleep problems item
wide$sleep_hours_t1 <- round(pmin(pmax(7.2 - 0.5 * wide$dep3_t1 + rnorm(N, 0, .9), 3), 11), 1)
# Life satisfaction (0–100)
wide$life_sat_t1 <- round(pmin(pmax(65 - 6 * sim$trait[, 2] - 4 * sim$trait[, 1] + rnorm(N, 0, 12), 0), 100))
# T2 professional help seeking (0/1): higher depression increases probability of seeking help (generated via logistic regression)
dep_t2_sum <- rowSums(wide[, paste0(items[!is_lone], "_t2")])
wide$help_seek_t2 <- rbinom(N, 1, plogis(-2.2 + 0.18 * dep_t2_sum + 0.4 * wide$gender))

write.csv(wide, "data/clpn_sim_wide.csv", row.names = FALSE)
if (requireNamespace("haven", quietly = TRUE)) haven::write_sav(wide, "data/clpn_sim_wide.sav")

## ---- 5. "Ground truth": population-level T1 -> T2 regression coefficients ----
# Note: Observed data conflate stable traits, so standard CLPN (based on observed scores) targets the population target, not within-person B.
# We compute what the OLS coefficients of CLPN would be asymptotically using a massive sample of 200,000 individuals.
big <- gen_panel(200000)
Xb <- scale(to_likert(big$X[[1]])); Yb <- scale(to_likert(big$X[[2]]))
Bpop <- solve(crossprod(Xb), crossprod(Xb, Yb)); dimnames(Bpop) <- list(items, items)
write.csv(round(B, 3),    "data/true_B_within.csv")
write.csv(round(Bpop, 3), "data/true_B_population.csv")

cat("Data generated: data/clpn_sim_wide.csv  (N =", N, ")\n")
cat("Population target T1->T2 coefficients (target for standard CLPN):\n"); print(round(Bpop, 2))
