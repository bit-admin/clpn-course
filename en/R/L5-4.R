# =====================================================================
# L5-4.R  From prediction to causation: confounding, time lags, and stable traits
#   (What cross-lags can and cannot tell us)
# Companion to lesson lessons/L5-4.html. This script does not use course data;
# it relies entirely on simulations because only in simulations do we know the "ground truth."
#   Part 1: Unmeasured confounding U manufactures a "significant cross-lag"
#   Part 2: Different measurement lags produce different cross-lagged coefficients (Delta * a^(Delta-1) * c)
#   Part 3: Stable traits (between-person differences) cause CLPM to show spurious cross-lags (core point in Lucas, 2023)
#   Part 4: A simple helper to check for "risky causal language"
# =====================================================================
source("R/_setup.R")
log_open("L5-4_log.txt")

coef_row <- function(fit, term) {                 # Extract estimate, SE, and p-value for a coefficient
  s <- summary(fit)$coefficients
  round(s[term, c("Estimate", "Std. Error", "Pr(>|t|)")], 4)
}

## ---------- Part 1: Unmeasured confounding ----------
cat("========== Part 1: Unmeasured confounding ==========\n")
set.seed(2026)
N  <- 800
U  <- rnorm(N)                                   # Unmeasured common cause (e.g., chronic illness severity)
L1 <- 0.6 * U + rnorm(N, 0, 0.8)                 # T1 loneliness: influenced by U
D1 <- 0.6 * U + rnorm(N, 0, 0.8)                 # T1 depression: influenced by U
D2 <- 0.5 * D1 + 0.4 * U + rnorm(N, 0, 0.7)      # T2 depression: influenced by D1 and U; loneliness has NO effect on it
m_naive <- lm(scale(D2) ~ scale(D1) + scale(L1))             # Like CLPM, controlling only for T1 depression
m_ctrlU <- lm(scale(D2) ~ scale(D1) + scale(L1) + scale(U))  # If we could measure and control for U
cat("\nModel A: D2 ~ D1 + L1 (U unmeasured)\n");  print(summary(m_naive)$coefficients |> round(4))
cat("\nModel B: D2 ~ D1 + L1 + U (controlling for U)\n"); print(summary(m_ctrlU)$coefficients |> round(4))
a <- coef_row(m_naive, "scale(L1)"); b <- coef_row(m_ctrlU, "scale(L1)")
cat(sprintf("\n→ Cross-lag of loneliness: without controlling for U, β = %.3f (p %s); controlling for U, β = %.3f (p = %.2f)\n",
            a[1], if (a[3] < .001) "< .001" else paste("=", round(a[3], 3)), b[1], b[3]))

# Extension exercise: U no longer directly affects D2 (change 0.4*U to 0)
set.seed(2026)
U  <- rnorm(N); L1 <- 0.6 * U + rnorm(N, 0, 0.8); D1 <- 0.6 * U + rnorm(N, 0, 0.8)
D2b <- 0.5 * D1 + 0 * U + rnorm(N, 0, 0.7)
c0 <- coef_row(lm(scale(D2b) ~ scale(D1) + scale(L1)), "scale(L1)")
cat(sprintf("Extension: changing 0.4*U to 0 yields L1 coefficient β = %.3f (p = %.2f) — U operates only through D1, which is already controlled.\n", c0[1], c0[3]))

# Replicate 500 times: how common are false positives?
set.seed(1)
p_vals <- replicate(500, {
  U <- rnorm(N); L1 <- 0.6 * U + rnorm(N, 0, 0.8); D1 <- 0.6 * U + rnorm(N, 0, 0.8)
  D2 <- 0.5 * D1 + 0.4 * U + rnorm(N, 0, 0.7)
  summary(lm(D2 ~ D1 + L1))$coefficients["L1", 4] })
cat(sprintf("500 simulation replications (N = 800): proportion of loneliness coefficient with p < .05 = %.1f%% (true effect is 0; nominal rate is 5%%)\n\n",
            100 * mean(p_vals < .05)))

## ---------- Part 2: Time lag ----------
cat("========== Part 2: Measurement interval (time lag) ==========\n")
lag_effect <- function(a, c, months) {          # Monthly process x[m+1] = A x[m], A = [[a,0],[c,a]]
  A <- matrix(c(a, c, 0, a), 2)                  # Fill by columns: col 1 (a, c), col 2 (0, a)
  sapply(months, function(d) { P <- diag(2); for (k in seq_len(d)) P <- P %*% A; P[2, 1] })
}
months <- 1:24
for (pars in list(c(0.8, 0.15), c(0.9, 0.05))) {
  ce <- lag_effect(pars[1], pars[2], months)
  cat(sprintf("Monthly autoregression a = %.2f, monthly cross-effect c = %.2f:\n", pars[1], pars[2]))
  print(data.frame(Lag_months = c(1, 3, 6, 12, 24), Cross_lag = round(ce[c(1, 3, 6, 12, 24)], 3),
                   Formula = round(c(1, 3, 6, 12, 24) * pars[1]^(c(1, 3, 6, 12, 24) - 1) * pars[2], 3)),
        row.names = FALSE)
  cat(sprintf("  Peak occurs at approximately %d months (theoretical value -1/ln(a) = %.1f)\n\n", which.max(ce), -1 / log(pars[1])))
}
png_open("L5-4_lag.png", width = 1800, height = 1100)
plot(months, lag_effect(0.8, 0.15, months), type = "b", pch = 19, ylim = c(0, 0.5),
     xlab = "Measurement lag (months)", ylab = "Observed cross-lag (Loneliness -> Depression)",
     main = "Same monthly process measured across different lags")
lines(months, lag_effect(0.9, 0.05, months), type = "b", pch = 17, col = "firebrick")
legend("topright", c("a = 0.8, c = 0.15", "a = 0.9, c = 0.05"), pch = c(19, 17),
       col = c("black", "firebrick"), bty = "n")
invisible(dev.off())
cat("Plot saved: R/output/L5-4_lag.png\n\n")

## ---------- Part 3: Stable traits -> spurious cross-lags ----------
cat("========== Part 3: Stable traits and false positives in CLPM (Lucas, 2023) ==========\n")
# Each person has stable loneliness trait TL and depression trait TD (correlated at 0.5);
# within-person fluctuations have autoregression only (0.3); true within-person cross-lag is 0.
sim_panel <- function(N, trait_sd = 1) {
  TL <- rnorm(N); TD <- 0.5 * TL + sqrt(1 - 0.5^2) * rnorm(N)
  TL <- trait_sd * TL; TD <- trait_sd * TD
  wl <- rnorm(N); wd <- rnorm(N)
  L <- D <- matrix(NA, N, 3)
  for (t in 1:3) {
    if (t > 1) { wl <- 0.3 * wl + rnorm(N, 0, sqrt(1 - 0.09)); wd <- 0.3 * wd + rnorm(N, 0, sqrt(1 - 0.09)) }
    L[, t] <- TL + wl; D[, t] <- TD + wd
  }
  data.frame(L1 = L[, 1], L2 = L[, 2], D1 = D[, 1], D2 = D[, 2])
}
set.seed(42)
for (n in c(200, 800, 3000)) {
  ps <- replicate(200, { d <- sim_panel(n); summary(lm(D2 ~ D1 + L1, data = d))$coefficients["L1", 4] })
  est <- coef(lm(scale(D2) ~ scale(D1) + scale(L1), data = sim_panel(n)))[3]
  cat(sprintf("N = %4d: In CLPM-style regression, proportion of \"Loneliness T1 -> Depression T2\" with p < .05 = %5.1f%% (standardized β for single sample ≈ %.3f)\n",
              n, 100 * mean(ps < .05), est))
}
set.seed(42)
ps0 <- replicate(200, { d <- sim_panel(800, trait_sd = 0); summary(lm(D2 ~ D1 + L1, data = d))$coefficients["L1", 4] })
cat(sprintf("Control: without stable traits (trait_sd = 0), N = 800, proportion with p < .05 = %.1f%% (close to nominal 5%%, 200 replications have sampling fluctuation)\n", 100 * mean(ps0 < .05)))
cat("→ True within-person cross-lag is 0, but with correlated stable traits, CLPM will \"detect\" cross-lags; larger samples become more \"significant\".\n",
    "  Controlling for T1 depression cannot eliminate trait influence, because T1 depression is merely a noisy measurement of the trait.\n\n")

## ---------- Part 4: Checking for risky causal words ----------
cat("========== Part 4: Checking for \"risky causal words\" in conclusions ==========\n")
danger <- c("cause", "lead to", "result in", "determine", "drive", "root cause", "will definitely", "inevitably", "prove")
check_causal <- function(txt) {
  hits <- danger[sapply(danger, function(w) grepl(w, txt, fixed = TRUE))]
  if (length(hits)) cat(txt, "\n   Contains: ", paste(hits, collapse = ", "), "\n", sep = "")
  else cat(txt, "\n", sep = "")
  invisible(hits)
}
check_causal("Loneliness causes depression in older adults.")
check_causal("Therefore reducing loneliness will lead to reduced depression.")
check_causal("After controlling for baseline depression, T1 loneliness positively predicted T2 depression, consistent with the hypothesis that loneliness may worsen depression.")
log_close()
