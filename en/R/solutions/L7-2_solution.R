# Solution L7-2: Estimated matrix vs. population target; lambda.min vs. lambda.1se
source("R/_setup.R")
log_open("sol_L7-2_log.txt")
dat <- read_course_data(); Bt <- true_B(); off <- row(Bt) != col(Bt)
set.seed(2026); Bmin <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], "lambda.min")
set.seed(2026); B1se <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], "lambda.1se")
strong <- abs(Bt) >= .10 & off                         # Stronger cross-lagged edges in population target
cat("Stronger CL edges in population target:\n")
print(data.frame(edge = paste(rownames(Bt)[row(Bt)[strong]], "→", colnames(Bt)[col(Bt)[strong]]),
                 true = Bt[strong], min = round(Bmin[strong], 3), `1se` = round(B1se[strong], 3)))
fp <- function(B) sum(B != 0 & abs(Bt) < .05 & off)
cat("False positives (population target |beta| < .05 estimated as non-zero): lambda.min =", fp(Bmin), "; lambda.1se =", fp(B1se), "\n")
cat("Answer: lambda.1se selects a larger lambda -> stronger penalty -> sparser network, fewer false positives but misses weak edges.\n",
    "B[\"dep3\",\"dep4\"] denotes T1 dep3 (Sleep problems) -> T2 dep4 (Fatigue) (row = from, column = to): lambda.min estimate =",
    round(Bmin["dep3", "dep4"], 3), ", population target =", round(Bt["dep3", "dep4"], 3), "\n")
log_close()
