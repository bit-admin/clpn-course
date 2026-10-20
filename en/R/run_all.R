# =====================================================================
# run_all.R — Run all course scripts sequentially in order and report success or failure
# Usage: Open clpn-course.Rproj in RStudio, then source("R/run_all.R")
#        Or in a terminal (from the clpn-course folder): Rscript R/run_all.R
#        A full run takes ~40–95 minutes (depending on the computer), mostly spent on bootstrapping;
#        To ensure bitwise reproducibility, bootstrapping defaults to single-core (nCores = 1); see notes at the beginning of L8-2.R.
# Lesson scripts are sorted by lesson number, with letter suffixes immediately following their parent lesson,
# so the capstone project runs in dependency order: L10-1 -> L10-2 -> L10-2b -> L10-3.
# All lesson scripts (R/L*.R) and the final assessment answers script (R/assess_answers.R) are run first,
# followed by all solution scripts (R/solutions/*.R).
# Also runs the real-data case study: R/data_elsoc.R (rewrites data/elsoc_phq8_wide.csv from the bundled raw file)
# and R/case_elsoc.R.
# Both clpn-course.zip and the GitHub repository include R/solutions/; if missing, solutions will be skipped with a notice.
# =====================================================================
source("R/_setup.R")
lesson_key <- function(f) {                       # L7-5.R -> 705; L7-5b.R -> 705.02 (immediately following L7-5.R)
  m <- regmatches(basename(f), regexec("L([0-9]+)-([0-9]+)([a-z]?)", basename(f)))[[1]]
  as.numeric(m[2]) * 100 + as.numeric(m[3]) + ifelse(m[4] == "", 0, (utf8ToInt(m[4]) - 96) / 100) }
files <- list.files("R", pattern = "^L[0-9]+-[0-9]+[a-z]?\\.R$", full.names = TRUE)
files <- files[order(sapply(files, lesson_key))]
if (file.exists("R/assess_answers.R")) files <- c(files, "R/assess_answers.R")   # Final Part C answers (not named L*.R, listed separately)
for (f_el in c("R/data_elsoc.R", "R/case_elsoc.R"))                              # Real-data case study (~1–2 min)
  if (file.exists(f_el)) files <- c(files, f_el)
sols <- if (dir.exists("R/solutions")) list.files("R/solutions", pattern = "\\.R$", full.names = TRUE) else character(0)
sols <- sols[order(sapply(sols, lesson_key))]
cat(sprintf("Lesson scripts: %d; solution scripts: %d%s\n", length(files), length(sols),
            if (length(sols) == 0) " (No solution scripts found in R/solutions/, skipping; solutions are provided with clpn-course.zip and the GitHub repository)" else ""))
status <- data.frame()
for (f in c(files, sols)) {
  t0 <- Sys.time()
  ok <- tryCatch({ if (grepl("solutions", f)) source(f, local = new.env(), print.eval = TRUE, echo = FALSE)  # Solution scripts: print results automatically like interactive line-by-line execution
                  else sys.source(f, envir = new.env()); "OK" },
                 error = function(e) paste("FAIL:", conditionMessage(e)))
  while (sink.number() > 0) sink()
  grDevices::graphics.off()
  setwd(find_root())
  status <- rbind(status, data.frame(script = f, status = ok,
                                     seconds = round(as.numeric(difftime(Sys.time(), t0, units = "secs")))))
  cat(sprintf("%-32s %-8s %5ss\n", f, substr(ok, 1, 60), tail(status$seconds, 1)))
}
write.csv(status, file.path("R", "output", "run_all_status.csv"), row.names = FALSE)
