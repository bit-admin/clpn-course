# Exercise Solutions L2-1: First script (2.1-A), reading help pages (2.1-B), minimal reproducible example (2.1-C)
source("R/_setup.R")
log_open("sol_L2-1_log.txt")
# ---- 2.1-A week02.R ----
my_age <- 21                 # Replace with your actual age
print(my_age * 365)          # Approximate days (ignoring leap years)
print(my_age * 365.25)       # Slightly more precise
a <- 3; b <- 4.5; c_val <- 10   # Avoid using c as a name to prevent confusion with c()
print(a + b + c_val)
# Intentional typo (wrapped in tryCatch so the script won't halt; in personal practice run sum(a, b, c_vall) directly)
msg <- tryCatch(sum(a, b, c_vall), error = function(e) conditionMessage(e))
cat("Error from intentional typo: ", msg, "\n-> Extra 'l' in the object name; R cannot find this object.\n\n")
# ---- 2.1-B round() and 'round half to even' ----
cat("round(2.5) =", round(2.5), "; round(3.5) =", round(3.5), "; round(0.125, 2) =", round(0.125, 2), "\n")
cat("(R rounds numbers exactly at the midpoint to the nearest even number: IEC 60559 standard)\n\n")
# ---- 2.1-C Minimal reproducible example ----
x <- c(1, 2, NA)
cat("mean(x) =", mean(x), "; mean(x, na.rm = TRUE) =", mean(x, na.rm = TRUE), "\n")
cat("R version: ", R.version.string, "\n")
log_close()
