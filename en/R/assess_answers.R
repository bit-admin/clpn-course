# =====================================================================
# assess_answers.R — Reference answers for Part C (R tasks) of the final exam
# Part C answers on the final exam page materials/assess_final.html are read
# from this script's output R/output/assess_answers.csv, not hand-coded.
# When taking the final exam, learners should calculate these in R themselves first rather than running this script beforehand.
# run_all.R runs this after all lesson scripts and before solution scripts (listed separately as its filename is not L*.R).
# Runtime: a few seconds (EBIC does not use cross-validation, so results are bitwise reproducible).
# =====================================================================
source("R/_setup.R")
library(glmnet)
log_open("assess_answers_log.txt")
dat <- read_course_data()
B <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], rule = "ebic")   # T1 -> T2, EBIC (gamma = 0.5)
ans <- data.frame(
  key = c("C1", "C2", "C3", "C4", "C5"),
  value = c(mean(dat$lone1_t1),                            # C1: Mean of lone1 at Wave 1
            cor(dat$lone3_t1, dat$dep1_t2),                # C2: Correlation between T1 lone3 and T2 dep1
            sum(dat$gender == 1),                          # C3: Number of females (gender == 1)
            sd(dat$dep1_t1),                               # C4: Standard deviation of dep1 at Wave 1
            sum(cl_only(B) != 0)),                         # C5: Number of non-zero cross-lagged edges in the T1->T2 network estimated via EBIC
  task = c("mean(lone1_t1)", "cor(lone3_t1, dep1_t2)", "sum(gender == 1)", "sd(dep1_t1)",
           "sum(cl_only(clpn_estimate(T1, T2, rule = \"ebic\")) != 0)"))
ans$value <- round(ans$value, 3)
print(ans, row.names = FALSE)
write.csv(ans, out("assess_answers.csv"), row.names = FALSE)
log_close()
