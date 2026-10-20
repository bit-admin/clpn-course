# =====================================================================
# L7-4.R  Out-Expected Influence, In-Expected Influence, and Cross-Construct Bridging
#   (out-EI, in-EI, bridge EI)
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L7-4_log.txt")
dat <- read_course_data()
set.seed(2026)
B <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)])
CL <- cl_only(B); p <- ncol(CL)

# ---- Lesson Code ----
outEI <- rowSums(CL)   # Sum row k: edges originating from this node (predicting others)
inEI  <- colSums(CL)   # Sum column j: edges pointing to this node (predicted by others)
comm  <- c(rep("Loneliness", 4), rep("Depression", 5))
bridgeOut <- sapply(seq_len(p), function(k) sum(CL[k, comm != comm[k]]))   # Outgoing edges across constructs only
bridgeIn  <- sapply(seq_len(p), function(j) sum(CL[comm != comm[j], j]))   # Incoming edges across constructs only
res <- data.frame(node = rownames(CL), label = item_en[rownames(CL)], construct = comm,
                  outEI, inEI, bridgeOut, bridgeIn, row.names = NULL)
print(res, digits = 3)
write.csv(res, out("L7-4_EI.csv"), row.names = FALSE)

# Which construct more strongly "predicts" the other?
l2d <- sum(CL[comm == "Loneliness", comm == "Depression"]); d2l <- sum(CL[comm == "Depression", comm == "Loneliness"])
cat("\nLoneliness -> Depression sum of edge weights =", round(l2d, 3), "; Depression -> Loneliness sum of edge weights =", round(d2l, 3), "\n")

# Side-by-side bar plots (z-scores also acceptable; raw values used here)
png_open("L7-4_EI_bars.png", 2000, 1000)
par(mfrow = c(1, 2), mar = c(4, 7, 3, 1))
cols <- ifelse(comm == "Loneliness", "#56B4E9", "#E69F00")
barplot(rev(outEI), horiz = TRUE, las = 1, col = rev(cols), names.arg = rev(paste(rownames(CL), item_en)),
        main = "Out-expected influence (out-EI)", cex.names = .8); abline(v = 0)
barplot(rev(inEI), horiz = TRUE, las = 1, col = rev(cols), names.arg = rev(paste(rownames(CL), item_en)),
        main = "In-expected influence (in-EI)", cex.names = .8); abline(v = 0)
invisible(dev.off())
# Built-in to qgraph: InExpectedInfluence / OutExpectedInfluence for directed networks
g <- qgraph(CL, directed = TRUE, DoNotPlot = TRUE)
png_open("L7-4_centralityPlot.png", 1400, 1400)
suppressWarnings(print(centralityPlot(g, include = c("OutExpectedInfluence", "InExpectedInfluence"),
                     scale = "raw0", print = FALSE)))
invisible(dev.off())
# ---- Comparison with Two Truths (possible only with simulated data) ----
# Population target (data/true_B_population.csv): target of standard CLPN as N -> Inf, including stable trait effects;
# Within-person truth (data/true_B_within.csv): data-generating within-person lagged coefficients.
# EI calculated from the two matrices differs as well.
Bt <- true_B()[rownames(CL), colnames(CL)]; diag(Bt) <- 0
Bw <- as.matrix(read.csv("data/true_B_within.csv", row.names = 1))[rownames(CL), colnames(CL)]; diag(Bw) <- 0
tru <- data.frame(node = rownames(CL), outEI_est = outEI, outEI_pop = rowSums(Bt), outEI_within = rowSums(Bw),
                  inEI_est = inEI, inEI_pop = colSums(Bt), inEI_within = colSums(Bw), row.names = NULL)
cat("\nEstimated EI vs. EI calculated from two truths:\n"); print(tru, digits = 3)
rho <- function(a, b) round(cor(a, b, method = "spearman"), 2)
cat("Spearman correlation between out-EI rank and population target =", rho(outEI, rowSums(Bt)), "; with within-person truth =", rho(outEI, rowSums(Bw)), "\n")
cat("Spearman correlation between in-EI rank and population target =", rho(inEI, colSums(Bt)), "; with within-person truth =", rho(inEI, colSums(Bw)), "\n")
cat("Loneliness -> Depression sum of edge weights: estimated", round(l2d, 3), "; population target", round(sum(Bt[comm == "Loneliness", comm == "Depression"]), 3),
    "; within-person truth", round(sum(Bw[comm == "Loneliness", comm == "Depression"]), 3), "\n")
cat("Depression -> Loneliness sum of edge weights: estimated", round(d2l, 3), "; population target", round(sum(Bt[comm == "Depression", comm == "Loneliness"]), 3),
    "; within-person truth", round(sum(Bw[comm == "Depression", comm == "Loneliness"]), 3), "\n")
write.csv(tru, out("L7-4_EI_truth.csv"), row.names = FALSE)
log_close()
