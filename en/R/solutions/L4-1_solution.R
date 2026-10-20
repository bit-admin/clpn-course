# Solution L4-1-B: Between-person and within-person components of loneliness sum scores;
# Appendix: Estimating ICC using multilevel models (lme4)
source("R/_setup.R")
log_open("sol_L4-1_log.txt")
dat <- read_course_data()
lone <- sapply(1:3, function(t) rowSums(dat[, paste0(lone_items, "_t", t)]))
dep  <- sapply(1:3, function(t) rowSums(dat[, paste0(dep_items, "_t", t)]))
colnames(lone) <- colnames(dep) <- paste0("T", 1:3)
cat("Loneliness means across 3 waves:\n"); print(round(colMeans(lone), 2))
cat("Loneliness cross-wave correlations:\n"); print(round(cor(lone), 2))
decomp <- function(m) { pm <- rowMeans(m); c(between = var(pm), within = mean(apply(m - pm, 1, var))) }
cat("Rough variance decomposition (variance of person means vs. within-person variance):\n")
print(round(rbind(Loneliness = decomp(lone), Depression = decomp(dep)), 2))
if (requireNamespace("lme4", quietly = TRUE)) {
  icc <- function(m) {
    long <- data.frame(id = rep(seq_len(nrow(m)), 3), y = as.vector(m))
    vc <- as.data.frame(lme4::VarCorr(lme4::lmer(y ~ 1 + (1 | id), data = long)))
    v <- setNames(vc$vcov, vc$grp); c(between = v[["id"]], within = v[["Residual"]], ICC = v[["id"]] / sum(v))
  }
  cat("\nVariance components and ICC from multilevel model (lme4::lmer(y ~ 1 + (1 | id))):\n")
  print(round(rbind(Loneliness = icc(lone), Depression = icc(dep)), 2))
  cat("(The rough method's 'between' ≈ multilevel between + within / 3, because person means across 3 waves still contain within-person noise)\n")
} else cat("lme4 is not installed: install.packages(\"lme4\") to obtain multilevel model estimates.\n")
log_close()
