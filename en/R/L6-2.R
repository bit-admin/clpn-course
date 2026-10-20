# =====================================================================
# L6-2.R  Partial Correlation Networks and Gaussian Graphical Models (GGMs)
#   (Partial correlations & GGM)
# Example: Insomnia -> Fatigue -> Poor concentration (chain structure)
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L6-2_log.txt")
set.seed(62)
n <- 1000
insomnia <- rnorm(n)
fatigue <- 0.6 * insomnia + rnorm(n, 0, .8)
poor_conc <- 0.6 * fatigue + rnorm(n, 0, .8)       # Poor concentration is driven solely by fatigue
d <- data.frame(insomnia, fatigue, poor_conc)
cat("Correlation:\n"); print(round(cor(d), 2))
P <- solve(cor(d))                                 # Precision matrix = inverse of correlation matrix
pc <- -cov2cor(P); diag(pc) <- 1                   # Partial correlation = standardize and negate off-diagonals
cat("\nPartial correlation:\n"); print(round(pc, 2))
cat("Insomnia-poor_conc: correlation =", round(cor(insomnia, poor_conc), 2), ", partial correlation ≈", round(pc[1, 3], 2),
    "-> controlling for fatigue, the two are conditionally independent; no edge in the GGM.\n")
# Partial correlation <-> multiple regression: the coefficient of insomnia in poor_conc ~ insomnia + fatigue is also ≈ 0
print(round(coef(lm(poor_conc ~ insomnia + fatigue)), 3))
png_open("L6-2_cor_vs_pcor.png", 2000, 1000)
par(mfrow = c(1, 2))
qgraph(cor(d), graph = "cor",  labels = names(d), edge.labels = TRUE, theme = "colorblind", title = "Correlation Network", layout = "circle")
qgraph(cor(d), graph = "pcor", labels = names(d), edge.labels = TRUE, theme = "colorblind", title = "Partial Correlation Network", layout = "circle")
invisible(dev.off())
log_close()
