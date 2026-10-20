# =====================================================================
# L5-1.R  Intuition of the CLPM: autoregressive and cross-lagged paths (approximated via ordinary regression)
# =====================================================================
source("R/_setup.R")
log_open("L5-1_log.txt")
dat <- read_course_data()
z <- function(x) as.numeric(scale(x))
for (t in 1:3) {
  dat[[paste0("lone", t)]] <- z(rowSums(dat[, paste0(lone_items, "_t", t)]))
  dat[[paste0("dep", t)]]  <- z(rowSums(dat[, paste0(dep_items, "_t", t)]))
}
# One regression per T2 variable: autoregression (self -> self) + cross-lag (other -> self)
print(round(coef(lm(lone2 ~ lone1 + dep1, dat)), 3))
print(round(coef(lm(dep2  ~ dep1 + lone1, dat)), 3))
cat("lone1->lone2 and dep1->dep2 are autoregressive (AR); dep1->lone2 and lone1->dep2 are cross-lagged (CL).\n")
log_close()
