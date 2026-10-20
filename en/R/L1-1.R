# =====================================================================
# L1-1.R  Variables & Measurement: Where Data Comes From
# (Variables & measurement)
# Goal: First look at the course data, understand what variable each column represents,
#       and identify its level of measurement.
# To run: Open clpn-course.Rproj in RStudio, open this file, and click "Source".
# =====================================================================
source("R/_setup.R")          # Common setup (locate course root, plot font, helper functions)
log_open("L1-1_log.txt")      # Save console output to R/output/L1-1_log.txt

dat <- read_course_data()     # Load data frame: 800 rows (cases/participants) x 34 columns (variables)
cat("Number of cases (rows) =", nrow(dat), "; Number of variables (columns) =", ncol(dat), "\n\n")

# head() inspects first 6 rows; str() shows column data types (integer / numeric / character)
print(head(dat[, 1:10]))
str(dat[, c("id", "lone1_t1", "dep1_t1", "gender", "age", "social_support_t1")])

# Data dictionary / codebook: definitions for each variable
dict <- read.csv("data/data_dictionary.csv")
print(dict[, c("variable", "label", "values")])

# Summary of measurement levels (manually compiled to match the lesson)
lv <- data.frame(
  Variable = c("id", "gender", "lone1_t1", "dep1_t1", "age", "life_sat_t1"),
  Level_of_measurement = c("Nominal (identifier label)", "Nominal (binary 0/1)", "Ordinal (Likert 1-4)",
                           "Ordinal (0-3)", "Ratio", "Often treated as interval"))
print(lv)

# What values does each item take? table() calculates frequencies
for (v in c("lone1_t1", "dep1_t1")) { cat("\nValue distribution for", v, ":\n"); print(table(dat[[v]])) }

# Internal consistency reliability Cronbach's alpha (Lesson "Two More Lines"): Loneliness 4 items, Depression 5 items, T1
# In a script (Source / Rscript), results are not displayed automatically, so we use print(); when running line-by-line in the console, print() can be omitted
cat("\nCronbach's alpha (T1): Loneliness 4 items, Depression 5 items\n")
lone_t1 <- dat[, c("lone1_t1", "lone2_t1", "lone3_t1", "lone4_t1")]
print(round(psych::alpha(lone_t1)$total$raw_alpha, 2))          # Loneliness 4 items
print(round(psych::alpha(dat[, paste0("dep", 1:5, "_t1")])$total$raw_alpha, 2))   # Depression 5 items
log_close()
