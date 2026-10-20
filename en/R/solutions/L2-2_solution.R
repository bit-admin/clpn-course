# Exercise Solutions L2-2: Sleep vector and zscore() (2.2-A); vector operations on course data (2.2-B); multi-category factors (2.2-C)
source("R/_setup.R"); log_open("sol_L2-2_log.txt")
# ---- 2.2-A Sleep vector ----
sleep <- c(7, 5.5, 8, NA, 6, 4.5, 7.5, NA, 9, 5)
mean(sleep, na.rm = TRUE)                    # 6.5625
which(sleep < 6)                             # 2 6 10 (indices)
sleep[sleep < 6 & !is.na(sleep)]             # 5.5 4.5 5.0 (actual values)
zscore <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- sd(x, na.rm = TRUE)
  (x - m) / s                                # The last expression is the return value
}
all.equal(zscore(sleep), as.numeric(scale(sleep)))   # TRUE
stopifnot(isTRUE(all.equal(zscore(sleep), as.numeric(scale(sleep)))))
cat("zscore() and scale() yield identical results.\n\n")
# ---- 2.2-B On course data ----
dat <- read.csv("data/clpn_sim_wide.csv")
d1 <- dat$dep1_t1
sum(d1 == 3)                 # (1) Count of individuals scoring 3
mean(d1 >= 2)                # (2) Proportion of individuals scoring 2 or higher
z <- zscore(d1)
round(c(mean(z), sd(z)), 10) # (3) 0 and 1
cat("\n")
# ---- 2.2-C Multi-category factor ----
service <- c(1, 3, 2, 2, 1, 3, 3)
service_f <- factor(service, levels = 1:3, labels = c("Casework", "Group", "Community"))
table(service_f)             # Casework: 2, Group: 2, Community: 3
round(mean(service), 2)      # 2.14: Numerically computable, but "mean service type" is meaningless
log_close()
