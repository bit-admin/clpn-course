# =====================================================================
# L5-1.R  CLPM 的直觉：自回归路径与交叉滞后路径（用普通回归近似）
# =====================================================================
source("R/_setup.R")
log_open("L5-1_log.txt")
dat <- read_course_data()
z <- function(x) as.numeric(scale(x))
for (t in 1:3) {
  dat[[paste0("lone", t)]] <- z(rowSums(dat[, paste0(lone_items, "_t", t)]))
  dat[[paste0("dep", t)]]  <- z(rowSums(dat[, paste0(dep_items, "_t", t)]))
}
# 每个 T2 变量一个回归：自回归（自己→自己）+ 交叉滞后（对方→自己）
print(round(coef(lm(lone2 ~ lone1 + dep1, dat)), 3))
print(round(coef(lm(dep2  ~ dep1 + lone1, dat)), 3))
cat("lone1→lone2、dep1→dep2 是自回归 AR；dep1→lone2、lone1→dep2 是交叉滞后 CL。\n")
log_close()
