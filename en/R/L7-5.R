# =====================================================================
# L7-5.R  Multi-Wave CLPN, Covariates, and Within-Person Disentanglement
#   (Multi-wave CLPN, covariates)
# =====================================================================
source("R/_setup.R")
library(glmnet)
log_open("L7-5_log.txt")
dat <- read_course_data()
set.seed(2026); B12 <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)])   # T1 -> T2
set.seed(2026); B23 <- clpn_estimate(dat[, vars_t(2)], dat[, vars_t(3)])   # T2 -> T3
off <- row(B12) != col(B12)
cat("Correlation between T1->T2 and T2->T3 cross-lagged edge weights =", round(cor(B12[off], B23[off]), 3), "\n")
cat("CL edges non-zero in both networks =", sum(B12[off] != 0 & B23[off] != 0),
    "; present in only one network =", sum(xor(B12[off] != 0, B23[off] != 0)), "\n")
cat("Autoregressive edges:\n"); print(round(rbind(T1T2 = diag(B12), T2T3 = diag(B23)), 3))

# Include gender and age as unpenalized covariates (penalty.factor = 0, see clpn_estimate in _setup.R)
set.seed(2026)
B12c <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], covariates = dat[, c("gender", "age")])
cat("\nMax difference in edge weights before vs. after adding covariates =", round(max(abs(B12c - B12)), 4),
    "; correlation =", round(cor(B12c[off], B12[off]), 4), "\n")
# Direct demonstration of penalty.factor syntax (example for one T2 node)
Z <- cbind(scale(dat[, vars_t(1)]), gender = as.numeric(scale(dat$gender)))
cv1 <- cv.glmnet(Z, scale(dat$dep1_t2)[, 1], penalty.factor = c(rep(1, 9), 0))
print(round(as.matrix(coef(cv1, s = "lambda.min")), 3))
png_open("L7-5_replication.png", 1400, 1400)
plot(B12[off], B23[off], pch = 16, col = "steelblue", xlab = "T1->T2 edge weights", ylab = "T2->T3 edge weights",
     main = paste0("Consistency across two time intervals r = ", round(cor(B12[off], B23[off]), 2)))
abline(0, 1, lty = 2)
invisible(dev.off())
cat("\nLimitation: Standard CLPN is based on observed scores, conflating between-person (stable traits) and within-person effects;\n",
    "Because stable traits were simulated in this dataset, small within-construct edges appear that are absent from the true within-person B.\n")
saveRDS(list(B12 = B12, B23 = B23), out("L7-5_B12_B23.rds"))
log_close()
