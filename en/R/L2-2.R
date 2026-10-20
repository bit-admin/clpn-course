# =====================================================================
# L2-2.R  Basic R Syntax: Vectors, Data Types & Functions
# (Vectors, data types, functions)
# =====================================================================
source("R/_setup.R")
log_open("L2-2_log.txt")
sleep <- c(7, 5.5, 8, NA, 6, 4.5, 7.5, NA, 9, 5)   # NA = missing value
print(class(sleep))                                # "numeric"
print(mean(sleep))                                 # Returns NA when NAs are present!
print(mean(sleep, na.rm = TRUE))                   # na.rm = TRUE: remove NAs first
print(which(sleep < 6))                            # Indices of participants sleeping < 6 hours
print(sleep[sleep < 6 & !is.na(sleep)])            # Logical indexing

# Other data types: character, logical, factor
name   <- c("Alex", "Sam"); is_student <- c(TRUE, FALSE)
gender <- factor(c(1, 0), levels = c(0, 1), labels = c("Male", "Female"))
print(gender)

# Writing custom functions
zscore <- function(x) (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
print(round(cbind(my_zscore = zscore(sleep), scale_func = as.numeric(scale(sleep))), 3))

# ---- Lesson Supplement: More Indexing & Vectorization ----
print(length(sleep))          # Number of elements
print(sum(is.na(sleep)))      # Number of missing values
print(sleep * 60)             # Vectorization: convert each value to minutes
print(sleep[c(1, 3)])         # Elements 1 and 3
print(sleep < 6)              # Element-wise comparison; NA remains NA
print(sum(sleep < 6, na.rm = TRUE))   # TRUE treated as 1: count of participants sleeping < 6 hours

# ---- Lesson Supplement: Type Traps ----
# Warnings do not enter sink() logs; here we catch and print formatted as in the console
wmsg <- ""
v <- withCallingHandlers(as.numeric(c("3", "4", "five")),    # Characters to numbers: unparseable become NA
                         warning = function(w) { wmsg <<- conditionMessage(w); invokeRestart("muffleWarning") })
print(v); cat("Warning message:\n", wmsg, "\n", sep = "")
dat <- read.csv("data/clpn_sim_wide.csv")
g <- factor(dat$gender, levels = c(0, 1), labels = c("Male", "Female"))
print(table(g))
log_close()
