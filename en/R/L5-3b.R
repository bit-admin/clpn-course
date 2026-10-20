# =====================================================================
# L5-3b.R  How far is one sample from the truth in RI-CLPM?
# Course data are simulated, so the data-generating model is known. This script does two things:
#   1. Fit the same CLPM and RI-CLPM to a massive sample of N = 200,000 to obtain standardized paths when sample size is infinite (truth)
#   2. Repeatedly generate 200 samples of N = 800 to see how much a single sample's estimates fluctuate around the truth
# Takes about 1–3 minutes to run. Output written to R/output/L5-3b_log.txt and L5-3b_truth.csv.
# =====================================================================
source("R/_setup.R")
library(lavaan)
log_open("L5-3b_log.txt")

# ---- Load data-generating model ------------------------------------------
# Execute only the "model definition" portion of data/simulate_data.R (before N <- 800: B, Psi, gen_panel(), to_likert()),
# without regenerating or overwriting the course data file.
ex <- parse("data/simulate_data.R")
stop_at <- which(vapply(ex, function(e) identical(deparse(e)[1], "N <- 800"), logical(1)))
stopifnot(length(stop_at) == 1)
sim <- new.env()
for (e in ex[seq_len(stop_at - 1)]) eval(e, sim)

# Sum items into 3-wave construct scores (same as L5-3.R)
to_sums <- function(X) {
  out <- list()
  for (t in 1:3) {
    lik <- sim$to_likert(X[[t]])
    out[[paste0("lone", t)]] <- rowSums(lik[, 1:4])
    out[[paste0("dep", t)]]  <- rowSums(lik[, 5:9])
  }
  as.data.frame(out)
}

riclpm <- '
  RI_lone =~ 1*lone1 + 1*lone2 + 1*lone3
  RI_dep  =~ 1*dep1  + 1*dep2  + 1*dep3
  wl1 =~ 1*lone1; wl2 =~ 1*lone2; wl3 =~ 1*lone3
  wd1 =~ 1*dep1;  wd2 =~ 1*dep2;  wd3 =~ 1*dep3
  wl2 ~ wl1 + wd1;  wd2 ~ wd1 + wl1
  wl3 ~ wl2 + wd2;  wd3 ~ wd2 + wl2
  wl1 ~~ wd1; wl2 ~~ wd2; wl3 ~~ wd3
  wl1 ~~ wl1; wd1 ~~ wd1; wl2 ~~ wl2; wd2 ~~ wd2; wl3 ~~ wl3; wd3 ~~ wd3
  RI_lone ~~ RI_lone; RI_dep ~~ RI_dep; RI_lone ~~ RI_dep
  RI_lone ~~ 0*wl1 + 0*wd1;  RI_dep ~~ 0*wl1 + 0*wd1
  lone1 ~~ 0*lone1; lone2 ~~ 0*lone2; lone3 ~~ 0*lone3
  dep1 ~~ 0*dep1;   dep2 ~~ 0*dep2;   dep3 ~~ 0*dep3
'
clpm <- 'lone2 ~ lone1 + dep1; dep2 ~ dep1 + lone1; lone3 ~ lone2 + dep2; dep3 ~ dep2 + lone2
         lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3'

# Extract standardized paths; rewrite RI-CLPM within-person variable names wl/wd to lone/dep to align with CLPM
paths <- function(fit) {
  pe <- standardizedSolution(fit)
  pe <- pe[pe$op == "~" | (pe$op == "~~" & pe$lhs == "RI_lone" & pe$rhs == "RI_dep"), ]
  nm <- ifelse(pe$op == "~", paste(pe$rhs, "→", pe$lhs), "RI_lone ~~ RI_dep")
  nm <- gsub("wl", "lone", gsub("wd", "dep", nm))
  setNames(pe$est.std, nm)
}
# Note: lavaan saves and restores random number generator state during estimation. If to_sums(gen_panel(...)) is passed directly
# as an argument, data generation occurs inside lavaan and the RNG state is subsequently restored, drawing the identical sample every time.
# Therefore, use force(d) to generate data outside lavaan first.
fit_both <- function(d, ...) {
  force(d)
  list(
    CLPM    = paths(sem(clpm, data = d, ...)),
    RICLPM  = paths(lavaan(riclpm, data = d, meanstructure = TRUE, int.ov.free = TRUE, ...)))
}

# ---- 1. Course dataset (same model as L5-3.R) -----------------------------
dat <- read_course_data()
wide <- data.frame(row.names = seq_len(nrow(dat)))
for (t in 1:3) {
  wide[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
  wide[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)])
}
course <- fit_both(wide, missing = "fiml")

# ---- 2. Truth: large sample of N = 200,000 -------------------------------
set.seed(5302)
truth <- fit_both(to_sums(sim$gen_panel(200000)$X))

# ---- 3. Sampling variability: 200 samples of N = 800 ----------------------
R_REP <- 200
set.seed(5303)
reps <- lapply(seq_len(R_REP), function(r) {
  res <- tryCatch(suppressWarnings(fit_both(to_sums(sim$gen_panel(800)$X))), error = function(e) NULL)
  res
})
ok <- !vapply(reps, is.null, logical(1))
cat("Successfully converged across 200 replications:", sum(ok), "times\n\n")

rows <- list()
for (m in c("CLPM", "RICLPM")) {
  sims <- do.call(rbind, lapply(reps[ok], `[[`, m))
  for (p in names(truth[[m]])) {
    rows[[length(rows) + 1]] <- data.frame(
      model = m, path = p,
      truth = truth[[m]][[p]], course = course[[m]][[p]],
      q05 = unname(quantile(sims[, p], .05)), q95 = unname(quantile(sims[, p], .95)),
      sd = sd(sims[, p]),
      pct = mean(sims[, p] <= course[[m]][[p]]))   # Percentile rank of course sample estimate across 200 samples
  }
}
tab <- do.call(rbind, rows)
write.csv(tab, out("L5-3b_truth.csv"), row.names = FALSE)

cat("===== Standardized paths: truth (N = 200,000), course sample, and 90% range across 200 samples of N = 800 =====\n")
show <- tab; show[, 3:7] <- round(show[, 3:7], 3); show$pct <- round(tab$pct, 2)
print(show, row.names = FALSE)
cat("\nInterpretation: truth is the value when sample size is infinite; course is the estimate from course data (N = 800);\n",
    "[q05, q95] is the 90% range of estimates across 200 samples of N = 800 under the same data-generating model;\n",
    "pct is the percentile rank of the course sample estimate.\n",
    "Within-person cross-lagged paths in RI-CLPM fluctuate widely with 3 waves and N = 800: directional claims from a single sample are unreliable.\n")
log_close()
