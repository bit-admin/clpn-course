# =====================================================================
# L10-2.R  Capstone Project ②: Complete CLPN Analysis Pipeline (One-Click Run)
#          (Full CLPN pipeline)
# Descriptive statistics -> CLPN estimation -> Network plotting -> out/in-EI and bridge EI
# -> Bootstrap edge accuracy -> CS-coefficients -> Sensitivity analyses -> Comparison with true structure
# All output saved to R/output/ with prefix L10-2_. Single-core takes ~15–40 min
# (depending on hardware; includes two 1,000-replication bootstraps; single-core ensures reproducibility).
# =====================================================================
source("R/_setup.R")
need_output("L10-1_clean_data.csv", "R/L10-1.R", chain = "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-3.R")   # Prerequisite check
suppressPackageStartupMessages({ library(glmnet); library(qgraph); library(bootnet) })
log_open("L10-2_log.txt")
SEED <- 2026; N_BOOTS <- 1000; N_CORES <- 1   # Single-core = reproducible (parallel bootnet resampling drifts, see L8-2.R)
dat <- read.csv(out("L10-1_clean_data.csv"))          # From L10-1.R
X <- dat[, vars_t(1)]; Y <- dat[, vars_t(2)]

## 1. Descriptive Statistics --------------------------------------------
desc <- round(psych::describe(cbind(X, Y))[, c("mean", "sd", "skew", "kurtosis")], 2)
print(desc); write.csv(desc, out("L10-2_table1_descriptives.csv"))

## 2. CLPN Estimation ---------------------------------------------------
set.seed(SEED); B <- clpn_estimate(X, Y, rule = "lambda.min")
CL <- cl_only(B)
write.csv(round(B, 3), out("L10-2_table2_B_matrix.csv"))
el <- edge_list(B); el$from_en <- item_en[el$from]; el$to_en <- item_en[el$to]
write.csv(el, out("L10-2_table2_edges_AR_CL.csv"), row.names = FALSE)
cat("\nAutoregressive edges:\n"); print(round(diag(B), 3))
cat("\nStrongest 5 cross-lagged edges:\n"); print(head(el[el$from != el$to, ], 5), row.names = FALSE, digits = 3)

## 3. Network Plot ------------------------------------------------------
png_open("L10-2_fig1_clpn.png", 1800, 1500)
qgraph(CL, directed = TRUE, layout = "spring", groups = groups_list, palette = "colorblind", theme = "colorblind",
       asize = 4, legend = TRUE, nodeNames = paste(items, item_en[items]), legend.cex = .45,
       title = "Figure 1  T1→T2 Cross-Lagged Panel Network (Autoregressive edges not shown)")
invisible(dev.off())

## 4. Centrality --------------------------------------------------------
cen <- data.frame(node = items, label = item_en[items], community = comm,
                  outEI = rowSums(CL), inEI = colSums(CL),
                  bridgeOutEI = sapply(1:9, function(k) sum(CL[k, comm != comm[k]])),
                  bridgeInEI  = sapply(1:9, function(j) sum(CL[comm != comm[j], j])), row.names = NULL)
print(cen, digits = 3); write.csv(cen, out("L10-2_table3_centrality.csv"), row.names = FALSE)
g <- qgraph(CL, directed = TRUE, DoNotPlot = TRUE)
png_open("L10-2_fig2_centrality.png", 1400, 1400)
suppressWarnings(print(centralityPlot(g, include = c("OutExpectedInfluence", "InExpectedInfluence"),
                                      scale = "z-scores", print = FALSE)))
invisible(dev.off())

## 5. Bootstrap Edge Accuracy + 6. Case-Dropping CS ---------------------
clpn_fun <- function(data) {
  p <- ncol(data) / 2
  X <- scale(as.matrix(data[, 1:p])); Y <- scale(as.matrix(data[, (p + 1):(2 * p)]))
  B <- matrix(0, p, p)
  for (j in seq_len(p)) {
    cvfit <- glmnet::cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]
  }
  B
}
set.seed(SEED)
net <- estimateNetwork(cbind(X, Y), default = "none", fun = clpn_fun, directed = TRUE, labels = items)
set.seed(SEED)
boot <- bootnet(net, nBoots = N_BOOTS, type = "nonparametric", nCores = N_CORES, verbose = FALSE,
                statistics = c("edge", "outExpectedInfluence", "inExpectedInfluence"))
png_open("L10-2_fig3_bootstrap_edges.png", 1600, 3200)
suppressWarnings(print(plot(boot, statistics = "edge", order = "sample", labels = TRUE, CIstyle = "quantiles")))
invisible(dev.off())
bs <- as.data.frame(summary(boot, statistics = "edge"))
bs <- bs[order(-abs(bs$sample)), c("node1", "node2", "sample", "q2.5", "q97.5", "prop0")]
write.csv(bs, out("L10-2_table4_bootstrap_edges.csv"), row.names = FALSE)
set.seed(SEED)
cd <- bootnet(net, nBoots = N_BOOTS, type = "case", nCores = N_CORES, verbose = FALSE,
              statistics = c("outExpectedInfluence", "inExpectedInfluence"))
cs <- corStability(cd, verbose = FALSE)
write.csv(data.frame(statistic = names(cs), CS = round(cs, 3)), out("L10-2_table5_CS.csv"), row.names = FALSE)
cat("\nCS-coefficients:\n"); print(round(cs, 2))
png_open("L10-2_fig4_casedrop.png", 1600, 1200); suppressWarnings(print(plot(cd, statistics = names(cs)))); invisible(dev.off())

## 7. Sensitivity Analyses ----------------------------------------------
off <- row(B) != col(B)
set.seed(SEED); B_1se <- clpn_estimate(X, Y, rule = "lambda.1se")
set.seed(SEED); B_cov <- clpn_estimate(X, Y, covariates = dat[, c("gender", "age")])
set.seed(SEED); B_23  <- clpn_estimate(dat[, vars_t(2)], dat[, vars_t(3)])
sens <- data.frame(analysis = c("lambda.1se", "covariates gender+age", "T2→T3 replication"),
  r_with_main = round(c(cor(B[off], B_1se[off]), cor(B[off], B_cov[off]), cor(B[off], B_23[off])), 3),
  n_CL_edges = c(sum(B_1se[off] != 0), sum(B_cov[off] != 0), sum(B_23[off] != 0)))
cat("\nSensitivity analyses (primary analysis CL edges =", sum(B[off] != 0), "):\n"); print(sens)
write.csv(sens, out("L10-2_table6_sensitivity.csv"), row.names = FALSE)

## 8. Comparison with True Structure (Simulated Data Only) ---------------
Bt <- true_B()
cat("\nCorrelation with true population coefficients (CL edges) =", round(cor(B[off], Bt[off]), 3),
    "; AR edges =", round(cor(diag(B), diag(Bt)), 3), "\n")
saveRDS(list(B = B, cen = cen, cs = cs, sens = sens, bs = bs), out("L10-2_results.rds"))
log_close()
