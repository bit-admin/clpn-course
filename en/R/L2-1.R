# =====================================================================
# L2-1.R  Your First Line of R Code
# (Your first R code)
# Select a line and press Ctrl+Enter (Mac: Cmd+Enter) to run; output appears in the Console below.
# =====================================================================
# This is a comment: R ignores everything after #
1 + 1
age <- 21                    # <- is "assignment": store 21 into an object named age
age * 365                    # Age converted to days (approximate)
scores <- c(3, 5, 2, 4)      # c() combines numbers into a vector
mean(scores)                 # Function: name followed by parentheses
# ?mean                      # Open the help page (uncomment in RStudio to run)
sessionInfo()$R.version$version.string

# ---- Below is for course verification: writes lesson console outputs to R/output/L2-1_log.txt ----
# The console output boxes in the lesson come from this log. Beginners only need to read the lines above; this section can be skipped initially.
source("R/_setup.R")                       # Sets working directory and defines log_open() (covered in Lesson 2.4)
log_open("L2-1_log.txt")
print(1 + 1)
print(age * 365)
print(mean(scores))
print(sessionInfo()$R.version$version.string)
# Assignment vs. Comparison
x <- 5
print(x == 5)
print(x == 3)
my_age <- 21; friend_age <- 23; teacher_age <- 45
print(my_age + friend_age + teacher_age)
log_close()
