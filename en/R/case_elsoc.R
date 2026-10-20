# =====================================================================
# case_elsoc.R — Real-data case study: cross-lagged panel network of depressive symptoms (PHQ-8) in ELSOC
# Real-data case: a cross-lagged panel network of PHQ-8 symptoms in ELSOC (Chile, 2016–2018)
# Companion page: materials/case_elsoc.html. The analysis file data/elsoc_phq8_wide.csv is bundled with the course;
#   it can be run directly. To see how it was derived from raw data, see R/data_elsoc.R.
#
# Data: Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022,
#   "Estudio Longitudinal Social de Chile 2016-2021", https://doi.org/10.7910/DVN/LQMURF,
#   Harvard Dataverse, V1, UNF:6:z/vWFguq9fg03YaOLWFddA== [fileUNF] (CC0 1.0)
# Procedure (same workflow as Modules 7–8, applied to real data):
#   1 Descriptive statistics  2 CLPN (2016 -> 2017, lambda.min, 10-fold CV, seed 2026)  3 Out-/in-expected influence
#   4 Replication: 2017 -> 2018  5 Sensitivity: add sex and age as covariates (unpenalized)  6 Nonparametric edge bootstrap (200 iterations, for demonstration)
# Output: R/output/case_elsoc_log.txt, case_elsoc_B.csv, case_elsoc_EI.csv, case_elsoc_boot.csv, case_elsoc_clpn.png
#   (all summary results, containing no personal data)
# Runtime: ~1–2 minutes (mostly spent on Step 6; changing B_BOOT to 1000 takes ~5–8 minutes)
# =====================================================================
source("R/_setup.R")
library(glmnet)
library(qgraph)
options(width = 110)
t_start <- Sys.time()

f <- "data/elsoc_phq8_wide.csv"
if (!file.exists(f) && file.exists(file.path("..", f))) f <- file.path("..", f)
if (!file.exists(f)) {
  stop("Cannot find ", f, ". This file is bundled with the course; if removed, running source(\"R/data_elsoc.R\")\n",
       "will regenerate it from the raw file (and download from Harvard Dataverse if the raw file is missing).",
       call. = FALSE)
}
log_open("case_elsoc_log.txt")
cat("ELSOC Real-Data Case: CLPN of PHQ-8\n")
cat("Data: Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022, \"Estudio Longitudinal Social de Chile 2016-2021\",\n      https://doi.org/10.7910/DVN/LQMURF, Harvard Dataverse, V1\n")
cat("Preprocessing: R/data_elsoc.R (original sample; negative missing codes set to NA; PHQ items 1–8)\n\n")

w <- read.csv(f)
phq <- paste0("phq", 1:8)
phq_en <- c(phq1 = "Little interest", phq2 = "Depressed mood", phq3 = "Sleep problems", phq4 = "Fatigue",
            phq5 = "Appetite change", phq6 = "Trouble concentrating", phq7 = "Low self-worth", phq8 = "Psychomotor retardation")
vt <- function(t) paste0(phq, "_t", t)
a <- w[complete.cases(w[, c(vt(1), vt(2), vt(3))]), ]
cat("== 1 Descriptive Statistics ==\n")
cat("Analysis sample (complete PHQ-8 across Waves 1–3) N =", nrow(a), "\n")
desc <- data.frame(item = phq, label = phq_en[phq],
                   M_2016 = round(colMeans(a[, vt(1)]), 2), SD_2016 = round(apply(a[, vt(1)], 2, sd), 2),
                   M_2017 = round(colMeans(a[, vt(2)]), 2), M_2018 = round(colMeans(a[, vt(3)]), 2), row.names = NULL)
print(desc, row.names = FALSE)
tot <- sapply(1:3, function(t) rowSums(a[, vt(t)]))
cat(sprintf("PHQ-8 total score (8–40): 2016 M = %.2f, 2017 M = %.2f, 2018 M = %.2f; correlation between 2016 and 2017 total scores r = %.2f\n\n",
            mean(tot[, 1]), mean(tot[, 2]), mean(tot[, 3]), cor(tot[, 1], tot[, 2])))

cat("== 2 CLPN: 2016 -> 2017 (lambda.min, 10-fold cross-validation, seed 2026) ==\n")
set.seed(2026)
B <- clpn_estimate(a[, vt(1)], a[, vt(2)])
CL <- cl_only(B)
n_cl <- sum(CL != 0)
cat("Autoregressive edges (AR):\n"); print(round(diag(B), 3))
cat(sprintf("Non-zero cross-lagged edges: %d / 56 edges; maximum |B| = %.3f\n", n_cl, max(abs(CL))))
e <- edge_list(CL)
e$from_en <- phq_en[e$from]; e$to_en <- phq_en[e$to]; e$weight <- round(e$weight, 3)
cat("Strongest 8 cross-lagged edges:\n"); print(head(e[, c("from", "from_en", "to", "to_en", "weight")], 8), row.names = FALSE)
write.csv(round(B, 4), out("case_elsoc_B.csv"))

cat("\n== 3 Out- / In-Expected Influence (cross-lagged edges only, excluding autoregressions) ==\n")
EI <- data.frame(node = phq, label = phq_en[phq], outEI = round(rowSums(CL), 3), inEI = round(colSums(CL), 3), row.names = NULL)
print(EI[order(-EI$outEI), ], row.names = FALSE)
write.csv(EI, out("case_elsoc_EI.csv"), row.names = FALSE)

cat("\n== 4 Replication: 2017 -> 2018 ==\n")
set.seed(2026)
B23 <- clpn_estimate(a[, vt(2)], a[, vt(3)])
off <- row(B) != col(B)
cat(sprintf("2017 -> 2018 non-zero cross-lagged edges: %d / 56 edges; correlation with 2016 -> 2017 56 cross-lagged edges r = %.2f\n",
            sum(cl_only(B23) != 0), cor(B[off], B23[off])))
top8 <- head(e, 8)
same <- sapply(seq_len(nrow(top8)), function(i) sign(B23[top8$from[i], top8$to[i]]) == sign(top8$weight[i]) && B23[top8$from[i], top8$to[i]] != 0)
cat(sprintf("Among the 8 strongest edges, %d have the same sign and remain non-zero in 2017 -> 2018\n", sum(same)))

cat("\n== 5 Sensitivity: adding sex and age as covariates (unpenalized) ==\n")
ok <- complete.cases(a[, c("female", "age")])
set.seed(2026)
Bc <- clpn_estimate(a[ok, vt(1)], a[ok, vt(2)], covariates = a[ok, c("female", "age")])
cat(sprintf("N = %d; non-zero cross-lagged edges %d / 56 edges; correlation with primary cross-lagged edges r = %.3f\n",
            sum(ok), sum(cl_only(Bc) != 0), cor(B[off], Bc[off])))

cat("\n== 6 Nonparametric edge bootstrap (B_BOOT = 200 iterations, for demonstration; use >= 1000 for formal analysis) ==\n")
B_BOOT <- 200
set.seed(2026)
t_boot <- Sys.time()
boots <- replicate(B_BOOT, {
  i <- sample(nrow(a), replace = TRUE)
  cl_only(clpn_estimate(a[i, vt(1)], a[i, vt(2)]))[off]
})
nm <- paste0(rownames(B)[row(B)[off]], ">", colnames(B)[col(B)[off]])
bt <- data.frame(edge = nm, sample = round(B[off], 3),
                 q2.5 = round(apply(boots, 1, quantile, 0.025), 3), q97.5 = round(apply(boots, 1, quantile, 0.975), 3),
                 prop0 = round(rowMeans(boots == 0), 3))
bt <- bt[order(-abs(bt$sample)), ]
write.csv(bt, out("case_elsoc_boot.csv"), row.names = FALSE)
cat("Bootstrap intervals (2.5% and 97.5% quantiles) and proportion shrunk to 0 for the 8 strongest cross-lagged edges:\n")
print(head(bt, 8), row.names = FALSE)
cat(sprintf("Among the 8 strongest edges, %d have intervals excluding 0\n", sum(head(bt, 8)$q2.5 > 0 | head(bt, 8)$q97.5 < 0)))
boot_secs <- round(as.numeric(difftime(Sys.time(), t_boot, units = "secs")))   # Time depends on machine; omitted from log

png_open("case_elsoc_clpn.png")
qgraph(CL, directed = TRUE, layout = "spring", labels = phq, theme = "colorblind", asize = 4,
       nodeNames = unname(phq_en[phq]), legend = TRUE, legend.cex = 0.5,
       title = "ELSOC PHQ-8: CLPN (2016 -> 2017), lambda.min; autoregressive edges omitted")
invisible(dev.off())
cat("\nFigure: R/output/case_elsoc_clpn.png\n")
log_close()
cat("Time elapsed: ", round(as.numeric(difftime(Sys.time(), t_start, units = "secs"))), " seconds (bootstrap took ", boot_secs, " seconds)\n", sep = "")
