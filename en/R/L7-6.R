# =====================================================================
# L7-6.R  Measurement Invariance and Sample Size Planning
#   (Measurement invariance & sample-size planning)
# Advanced optional lesson. Uses only lavaan (fixed course version), no semTools required.
# Part 1: Longitudinal measurement invariance across 3 waves for 4 loneliness items (configural -> metric -> scalar)
# Part 2: Multi-group measurement invariance of 5 depression items between males and females (group.equal)
# Part 3: Artificially induced intercept shift on wave 3 lone2: see how scalar invariance fails and how partial invariance salvages it
# Part 4: Sample size planning via simulation: how large must N be to recover 8 "target edges"?
# Runtime: ~1 minute (mostly Part 4; changing REPS to 50 takes ~2–3 minutes)
# =====================================================================
source("R/_setup.R")
library(lavaan)
library(glmnet)
options(width = 110)                         # Prevent wide tables from wrapping in log
log_open("L7-6_log.txt")
dat <- read_course_data()

# ---- Helper: Extract fit indices to report ----------------------------
fit_row <- function(fit, name) {
  fm <- fitMeasures(fit, c("chisq.scaled", "df", "pvalue.scaled", "cfi.robust", "rmsea.robust"))
  data.frame(model = name, chisq = round(fm[["chisq.scaled"]], 2), df = fm[["df"]],
             p = round(fm[["pvalue.scaled"]], 3), CFI = round(fm[["cfi.robust"]], 3),
             RMSEA = round(fm[["rmsea.robust"]], 3))
}
# Comparison between adjacent models: Delta CFI >= -0.01 and Delta RMSEA <= 0.015 -> more constrained level supported (Chen, 2007)
compare_step <- function(tab) {
  tab$dCFI <- c(NA, round(diff(tab$CFI), 3))
  tab$dRMSEA <- c(NA, round(diff(tab$RMSEA), 3))
  tab$judge <- c("(Baseline)", ifelse(tab$dCFI[-1] >= -0.01 & tab$dRMSEA[-1] <= 0.015, "Supported", "Not supported"))
  tab
}

# =====================================================================
# Part 1: Longitudinal Measurement Invariance (4 Loneliness items x 3 waves)
# One loneliness factor per wave (F1, F2, F3); residuals of the same item correlated across waves
# =====================================================================
lone_model <- function(level = c("configural", "metric", "scalar"), free_int = character(0)) {
  level <- match.arg(level)
  s <- ""
  for (t in 1:3) {
    v <- paste0(lone_items, "_t", t)
    # Factor loadings: configural freely estimated; metric / scalar constrained equal via shared labels l1–l4
    lab <- if (level == "configural") paste0("l", 1:4, "_", t) else paste0("l", 1:4)
    s <- paste0(s, "F", t, " =~ ", paste0("NA*", v, " + ", lab, "*", v, collapse = " + "), "\n")
    # Intercepts: scalar constrained equal via shared labels i1–i4; items in free_int left unconstrained (partial invariance)
    ilab <- if (level == "scalar") paste0("i", 1:4) else paste0("i", 1:4, "_", t)
    ilab[v %in% free_int] <- paste0("i_free_", v[v %in% free_int])
    s <- paste0(s, paste0(v, " ~ ", ilab, "*1", collapse = "\n"), "\n")
  }
  # Identification: wave 1 factor variance = 1, mean = 0; once loadings are equal, waves 2 and 3 variances can be freely estimated;
  # once intercepts are equal, factor means can be freely estimated
  s <- paste0(s, "F1 ~~ 1*F1\nF1 ~ 0*1\n")
  for (t in 2:3) {
    s <- paste0(s, if (level == "configural") paste0("F", t, " ~~ 1*F", t, "\n") else paste0("F", t, " ~~ F", t, "\n"))
    s <- paste0(s, if (level == "scalar") paste0("F", t, " ~ NA*1\n") else paste0("F", t, " ~ 0*1\n"))
  }
  for (it in lone_items)                       # Residual covariance of the same item across waves
    s <- paste0(s, it, "_t1 ~~ ", it, "_t2 + ", it, "_t3\n", it, "_t2 ~~ ", it, "_t3\n")
  s
}
fit_long <- function(d, level, free_int = character(0))
  cfa(lone_model(level, free_int), data = d, estimator = "MLR", meanstructure = TRUE)

cat("===== Part 1: Longitudinal Measurement Invariance of 4 Loneliness Items (N =", nrow(dat), ", 3 waves, MLR) =====\n")
f_conf <- fit_long(dat, "configural"); f_metr <- fit_long(dat, "metric"); f_scal <- fit_long(dat, "scalar")
tab1 <- compare_step(rbind(fit_row(f_conf, "Configural"), fit_row(f_metr, "Metric"), fit_row(f_scal, "Scalar")))
print(tab1, row.names = FALSE)
cat("\nNested model chi-square difference test (Satorra-Bentler correction):\n")
lrt1 <- lavTestLRT(f_conf, f_metr, f_scal)
print(round(as.data.frame(lrt1)[, c("Df", "Chisq diff", "Df diff", "Pr(>Chisq)")], 3))
cat("\nLoneliness factor means across 3 waves in scalar model (Wave 1 fixed to 0):\n")
pe <- parameterEstimates(f_scal)
print(transform(pe[pe$op == "~1" & pe$lhs %in% c("F1", "F2", "F3"), c("lhs", "est", "se", "pvalue")],
                est = round(est, 3), se = round(se, 3), pvalue = round(pvalue, 3)), row.names = FALSE)

# =====================================================================
# Part 2: Multi-Group Measurement Invariance (5 Depression items, T1, Male vs. Female)
# lavaan group.equal adds constraints concisely: unconstrained -> equal loadings -> equal loadings + intercepts
# =====================================================================
cat("\n===== Part 2: Multi-Group Measurement Invariance of 5 Depression Items (T1) Across Genders =====\n")
dat$sex <- factor(dat$gender, levels = c(0, 1), labels = c("Male", "Female"))
cat("Sample size per group:"); print(table(dat$sex))
dep_model <- paste("Dep =~", paste0(dep_items, "_t1", collapse = " + "))
g_conf <- cfa(dep_model, data = dat, group = "sex", estimator = "MLR")
g_metr <- cfa(dep_model, data = dat, group = "sex", estimator = "MLR", group.equal = "loadings")
g_scal <- cfa(dep_model, data = dat, group = "sex", estimator = "MLR", group.equal = c("loadings", "intercepts"))
tab2 <- compare_step(rbind(fit_row(g_conf, "Configural"), fit_row(g_metr, "Metric"), fit_row(g_scal, "Scalar")))
print(tab2, row.names = FALSE)
lrt2 <- lavTestLRT(g_conf, g_metr, g_scal)
print(round(as.data.frame(lrt2)[, c("Df", "Chisq diff", "Df diff", "Pr(>Chisq)")], 3))
pe2 <- parameterEstimates(g_scal)
lm2 <- pe2[pe2$op == "~1" & pe2$lhs == "Dep" & pe2$group == 2, ]
cat(sprintf("\nWith scalar invariance established, females have a higher depression factor mean than males by %.3f (SE = %.3f, p = %.3f); male factor mean fixed to 0.\n",
            lm2$est, lm2$se, lm2$pvalue))
cat("(In the simulated data, females had an identical +0.2 added to each depression item: difference is at the factor level rather than item-specific, so invariance holds.)\n")

# =====================================================================
# Part 3: Creating a Non-Invariant Example
# Suppose Wave 3 lone2 ('Feeling left out') wording was altered to make endorsement easier:
# each participant gains +0.5 on this item, but true loneliness did not change.
# Intercept changed -> scalar invariance should fail.
# =====================================================================
cat("\n===== Part 3: Artificially Adding +0.5 to Wave 3 lone2 Intercept =====\n")
bad <- dat; bad$lone2_t3 <- bad$lone2_t3 + 0.5
b_conf <- fit_long(bad, "configural"); b_metr <- fit_long(bad, "metric"); b_scal <- fit_long(bad, "scalar")
b_part <- fit_long(bad, "scalar", free_int = "lone2_t3")
tab3 <- compare_step(rbind(fit_row(b_conf, "Configural"), fit_row(b_metr, "Metric"), fit_row(b_scal, "Scalar")))
print(tab3, row.names = FALSE)
pt <- fit_row(b_part, "Partial scalar (free lone2_t3 intercept)")
pt$dCFI <- round(pt$CFI - tab3$CFI[2], 3); pt$dRMSEA <- round(pt$RMSEA - tab3$RMSEA[2], 3)
pt$judge <- ifelse(pt$dCFI >= -0.01 & pt$dRMSEA <= 0.015, "Supported", "Not supported")
cat("\nPartial invariance model compared with metric model:\n"); print(pt, row.names = FALSE)
lrt3 <- lavTestLRT(b_metr, b_scal)
cat("\nMetric vs. scalar (modified data): chi-square difference p =", format.pval(lrt3[2, "Pr(>Chisq)"], digits = 3), "\n")
# Use score test (Lagrange multiplier test) to identify the most problematic equality constraint:
# It estimates how much chi-square drops if this single constraint is freed.
# Evaluated under standard ML estimation, so re-fit with ML first.
b_scal_ml <- cfa(lone_model("scalar"), data = bad, estimator = "ML", meanstructure = TRUE)
mi <- lavTestScore(b_scal_ml)$uni
mi <- mi[order(-mi$X2), ][1:3, ]
pt_tab <- parTable(b_scal_ml)
lab_of <- function(p) { r <- pt_tab[pt_tab$plabel == p, ]; if (r$op == "~1") paste0("Intercept of ", r$lhs) else paste0(r$lhs, " ", r$op, " ", r$rhs) }
cat("Top 3 most problematic equality constraints (larger X2 indicates greater misfit):\n")
print(data.frame(Constraint = paste(sapply(mi$lhs, lab_of), "=", sapply(mi$rhs, lab_of)), X2 = round(mi$X2, 2)), row.names = FALSE)
pb <- parameterEstimates(b_scal); pp <- parameterEstimates(b_part)
mean_F3 <- function(p) round(p$est[p$op == "~1" & p$lhs == "F3"], 3)
cat(sprintf("\nWave 3 loneliness factor mean: Original data %.3f; Modified with forced scalar invariance %.3f; Modified with partial invariance %.3f\n",
            mean_F3(pe), mean_F3(pb), mean_F3(pp)))
cat("-> If intercepts are forced to be equal, item wording changes are mistaken for 'everyone becoming more lonely'.\n")

write.csv(rbind(cbind(part = "1 Longitudinal", tab1), cbind(part = "2 Multi-group gender", tab2),
                cbind(part = "3 Modified", rbind(tab3, pt))),
          out("L7-6_invariance_fit.csv"), row.names = FALSE)

# =====================================================================
# Part 4: Sample Size Planning (by simulation)
# Logic: Assume a 'true' network, generate many datasets of size N, estimate a CLPN on each,
#        and count how many target edges are recovered and how many near-zero edges are falsely detected.
# The true network here uses true_B_population (the course population target); in practice use pilot data or literature estimates.
# =====================================================================
cat("\n===== Part 4: Sample Size Simulation =====\n")
REPS <- 20                                   # 20 repetitions per N; change to 50 for smoother curves
N_GRID <- c(150, 300, 500, 800, 1200)
B <- true_B()
R1 <- cor(dat[, vars_t(1)]); R2 <- cor(dat[, vars_t(2)])
Se <- R2 - t(B) %*% R1 %*% B                 # Residual covariance: standardizes simulated T2 item variances to ~1
Se <- (Se + t(Se)) / 2
off <- row(B) != col(B)
target <- off & abs(B) >= 0.08               # 8 "target edges" (cross-lagged and within-construct edges set in generative model)
near0  <- off & abs(B) < 0.02                # Near-zero edges: non-zero estimate counts as false discovery
cat("Target edges", sum(target), ":", paste(edge_list(B * target)$from, "->", edge_list(B * target)$to, collapse = ", "), "\n")
cat("Near-zero edges (|B| < 0.02):", sum(near0), "\n")
rmvn <- function(n, S) matrix(rnorm(n * ncol(S)), n) %*% chol(S)
# Single cross-validation retrieves both lambda.min and lambda.1se rules
est_both <- function(X, Y) {
  X <- scale(X); Y <- scale(Y); p <- ncol(X)
  Bm <- B1 <- matrix(0, p, p)
  for (j in 1:p) {
    cv <- cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    Bm[, j] <- as.numeric(coef(cv, s = "lambda.min"))[-1]
    B1[, j] <- as.numeric(coef(cv, s = "lambda.1se"))[-1]
  }
  list(min = Bm, `1se` = B1)
}
score <- function(Bh) c(power = mean(Bh[target] != 0 & sign(Bh[target]) == sign(B[target])),
                        all8 = all(Bh[target] != 0), fpr = mean(Bh[near0] != 0),
                        r = cor(Bh[off], B[off]))
set.seed(2026)
res <- list()
for (N in N_GRID) for (rep in 1:REPS) {
  X <- rmvn(N, R1); Y <- X %*% B + rmvn(N, Se)
  e <- est_both(X, Y)
  for (rule in names(e)) res[[length(res) + 1]] <- data.frame(N = N, rep = rep, rule = rule, t(score(e[[rule]])))
}
res <- do.call(rbind, res)
pw <- aggregate(cbind(power, all8, fpr, r) ~ N + rule, data = res, FUN = mean)
pw <- pw[order(pw$rule, pw$N), ]
pw[, c("power", "all8", "fpr", "r")] <- round(pw[, c("power", "all8", "fpr", "r")], 2)
names(pw) <- c("N", "rule", "power_target", "p_all8", "fpr_near0", "r_with_true")
cat("Each N repeated", REPS, "times. power_target = proportion of target edges recovered (non-zero and correct sign); p_all8 = proportion of all 8 edges recovered;\n",
    "fpr_near0 = proportion of near-zero edges falsely identified as non-zero; r_with_true = correlation between estimated and true cross-lagged edges.\n")
print(pw, row.names = FALSE)
write.csv(pw, out("L7-6_power.csv"), row.names = FALSE)
cat(sprintf("\nSimulation completed %d CLPN estimations in total (9 cross-validated LASSOs each).\n", length(N_GRID) * REPS))
png_open("L7-6_power.png", 1800, 1100)
par(mfrow = c(1, 2), mar = c(4.2, 4.2, 3, 1))
for (k in c("power_target", "fpr_near0")) {
  plot(NA, xlim = range(N_GRID), ylim = c(0, 1), xlab = "Sample size N", ylab = "Proportion",
       main = if (k == "power_target") "Recovery rate of target edges (power)" else "False discovery rate of near-zero edges")
  for (rule in c("min", "1se")) {
    s <- pw[pw$rule == rule, ]
    lines(s$N, s[[k]], type = "b", pch = 16, lwd = 2, col = if (rule == "min") "steelblue" else "darkorange")
  }
  if (k == "power_target") abline(h = 0.8, lty = 2, col = "grey50")
  legend(if (k == "power_target") "bottomright" else "topleft", c("lambda.min", "lambda.1se"), col = c("steelblue", "darkorange"), lwd = 2, pch = 16, bty = "n")
}
invisible(dev.off())
log_close()
