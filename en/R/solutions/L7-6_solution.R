# Solution L7-6: Measurement Invariance
# Exercise 2: Are the 5 depression items in the course data longitudinally invariant across 3 waves?
# Exercise 3: In real data (Sports Coaches Mental Health Cohort, CC0, data/coaches_mhc_raw.csv),
# are the 5 "social well-being" items invariant across 3 waves?
# Uses lavaan only (course pinned version); runtime approximately 10 seconds
source("R/_setup.R")
library(lavaan)
options(width = 110)
log_open("sol_L7-6_log.txt")

# General longitudinal invariance model: nm(t, k) gives variable name for wave t item k
long_model <- function(nm, K, level = c("configural", "metric", "scalar"), free_int = character(0)) {
  level <- match.arg(level); s <- ""
  for (t in 1:3) {
    v <- sapply(K, function(k) nm(t, k))
    lab  <- if (level == "configural") paste0("l", K, "_", t) else paste0("l", K)
    ilab <- if (level == "scalar") paste0("i", K) else paste0("i", K, "_", t)
    ilab[v %in% free_int] <- paste0("free_", v[v %in% free_int])
    s <- paste0(s, "F", t, " =~ ", paste0("NA*", v, " + ", lab, "*", v, collapse = " + "), "\n",
                paste0(v, " ~ ", ilab, "*1", collapse = "\n"), "\n")
  }
  s <- paste0(s, "F1 ~~ 1*F1\nF1 ~ 0*1\n")
  for (t in 2:3) s <- paste0(s, if (level == "configural") paste0("F", t, " ~~ 1*F", t) else paste0("F", t, " ~~ F", t), "\n",
                             if (level == "scalar") paste0("F", t, " ~ NA*1") else paste0("F", t, " ~ 0*1"), "\n")
  for (k in K) s <- paste0(s, nm(1, k), " ~~ ", nm(2, k), " + ", nm(3, k), "\n", nm(2, k), " ~~ ", nm(3, k), "\n")
  s
}
fit_row <- function(fit, name) {
  fm <- fitMeasures(fit, c("chisq.scaled", "df", "cfi.robust", "rmsea.robust"))
  data.frame(model = name, chisq = round(fm[[1]], 2), df = fm[[2]], CFI = round(fm[[3]], 3), RMSEA = round(fm[[4]], 3))
}
three_steps <- function(d, nm, K, ...) {
  f <- lapply(c("configural", "metric", "scalar"), function(lv) cfa(long_model(nm, K, lv), data = d, estimator = "MLR", meanstructure = TRUE, ...))
  tab <- rbind(fit_row(f[[1]], "configural"), fit_row(f[[2]], "metric"), fit_row(f[[3]], "scalar"))
  tab$dCFI <- c(NA, round(diff(tab$CFI), 3)); tab$dRMSEA <- c(NA, round(diff(tab$RMSEA), 3))
  print(tab, row.names = FALSE)
  lrt <- lavTestLRT(f[[1]], f[[2]], f[[3]])
  cat("Chi-square difference test p-values: metric vs. configural =", round(lrt[2, "Pr(>Chisq)"], 3), "; scalar vs. metric =", round(lrt[3, "Pr(>Chisq)"], 3), "\n")
  invisible(f)
}

# ---------------- Exercise 2: Course data, 5 depression items x 3 waves ----------------
cat("===== Exercise 2: Course data, longitudinal measurement invariance of 5 depression items (N = 800) =====\n")
dat <- read_course_data()
f2 <- three_steps(dat, function(t, k) paste0("dep", k, "_t", t), 1:5)
pe <- parameterEstimates(f2[[3]])
cat("Depression factor means at waves 2 and 3 in scalar model (wave 1 = 0):",
    paste(round(pe$est[pe$op == "~1" & pe$lhs %in% c("F2", "F3")], 3), collapse = ", "), "\n")

# ---------------- Exercise 3: Coach data, 5 social well-being items (w4-w8) x 3 waves ----------------
cat("\n===== Exercise 3: Sports coaches mental health tracking data (Ackeret et al., 2023, CC0) =====\n")
coach <- read.csv2("data/coaches_mhc_raw.csv", dec = ".")   # Semicolon-separated, decimal point is '.'
cat("Number of rows:", nrow(coach), ", number of columns:", ncol(coach), "\n")
cat("Participants with complete responses to all 14 items in each wave:",
    paste0("T", 1:3, " = ", sapply(1:3, function(t) sum(complete.cases(coach[, paste0("t", t, "w", 1:14)]))), collapse = ", "), "\n")
cat("Participants with complete responses across all 3 waves for the 5 social well-being items:", sum(complete.cases(coach[, paste0("t", rep(1:3, each = 5), "w", 4:8)])), "\n")
# Data check: Built-in subscale mean columns (t1emowb, t2socwb, etc.) do not match item-recalculated means (see data dictionary)
chk <- t(sapply(1:3, function(t) {
  it <- function(k) coach[, paste0("t", t, "w", k)]
  r <- function(a, b) round(cor(a, b, use = "complete.obs"), 2)
  c(emowb_vs_w1to3 = r(rowMeans(it(1:3)), coach[[paste0("t", t, "emowb")]]),
    socwb_vs_w4to8 = r(rowMeans(it(4:8)), coach[[paste0("t", t, "socwb")]]),
    psywb_vs_w9to14 = r(rowMeans(it(9:14)), coach[[paste0("t", t, "psywb")]]),
    WBcont_vs_sum = r(rowSums(it(1:14)), coach[[paste0("t", t, "_WB_cont")]]))
}))
rownames(chk) <- paste0("T", 1:3)
cat("Correlations between built-in summary columns and item-recalculated values (should be close to 1):\n"); print(chk)
tot <- sapply(1:3, function(t) rowSums(coach[, paste0("t", t, "w", 1:14)]))
same <- sapply(1:3, function(t) { w <- coach[[paste0("t", t, "_WB_cont")]]; k <- !is.na(tot[, t]) & !is.na(w)
  sprintf("T%d %d / %d participants", t, sum(tot[k, t] - 14 == w[k]), sum(k)) })
cat("Participants whose *_WB_cont exactly equals 'sum of 14 items - 14' (i.e., sum score scored 0-5):", paste(same, collapse = ", "), "\n")
cat("Cross-wave correlations of 14-item sum score (same participant should be similar over time): T1-T2 =", round(cor(tot[, 1], tot[, 2], use = "complete.obs"), 2),
    ", T2-T3 =", round(cor(tot[, 2], tot[, 3], use = "complete.obs"), 2), ", T1-T3 =", round(cor(tot[, 1], tot[, 3], use = "complete.obs"), 2), "\n")
cat("-> The item columns themselves are consistent across waves (high cross-wave correlations; T2 and T3 *_WB_cont exactly match the 14-item sum score scored 0-5), but the three subscale mean columns and overall mean column do not match (only T1 emotional well-being roughly matches), and T1 *_WB_cont only matches for a subset of participants.\n  Therefore, we compute exclusively from the item columns (t1w1 ... t3w14) rather than using the built-in subscale columns.\n\n")
nm_c <- function(t, k) paste0("t", t, "w", k)
cat("Missing data handled via FIML (missing = \"ml\"), so all 422 participants enter the model:\n")
f3 <- three_steps(coach, nm_c, 4:8, missing = "ml")
cat("\nScalar step: Chi-square test is significant, but Delta CFI does not exceed -0.01 -> inspect which intercept is least invariant (score test, re-fitting with ML):\n")
f3ml <- cfa(long_model(nm_c, 4:8, "scalar"), data = coach, estimator = "ML", missing = "ml", meanstructure = TRUE)
sc <- lavTestScore(f3ml)$uni; sc <- sc[order(-sc$X2), ][1:3, ]
ptab <- parTable(f3ml)
lab_of <- function(p) { r <- ptab[ptab$plabel == p, ]; if (r$op == "~1") paste0("intercept of ", r$lhs) else paste0(r$lhs, " ", r$op, " ", r$rhs) }
print(data.frame(Constraint = paste(sapply(sc$lhs, lab_of), "=", sapply(sc$rhs, lab_of)), X2 = round(sc$X2, 2)), row.names = FALSE)
worst <- sub("^intercept of ", "", lab_of(sc$rhs[1]))
fp <- cfa(long_model(nm_c, 4:8, "scalar", free_int = worst), data = coach, estimator = "MLR", missing = "ml", meanstructure = TRUE)
pr <- fit_row(fp, paste0("partial scalar (freeing intercept of ", worst, ")"))
pr$dCFI <- round(pr$CFI - fitMeasures(f3[[2]], "cfi.robust"), 3)
cat("\nComparison with metric model:\n"); print(pr, row.names = FALSE)
m_full <- parameterEstimates(f3[[3]]); m_part <- parameterEstimates(fp)
gm <- function(p) paste(sprintf("%.3f (SE %.3f)", p$est[p$op == "~1" & p$lhs %in% c("F2", "F3")], p$se[p$op == "~1" & p$lhs %in% c("F2", "F3")]), collapse = ", ")
cat("Social well-being factor means at waves 2 and 3 (wave 1 = 0): full scalar", gm(m_full), "; partial scalar", gm(m_part), "\n")
cat("(The dataset documentation mentions two possible wave intervals: 3/6 months or 6/12 months; hence we only evaluate whether the same construct is measured, without interpreting the rate of change.)\n")
log_close()
