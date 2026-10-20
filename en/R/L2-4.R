# =====================================================================
# L2-4.R  Installing Packages, Importing Data & Project Management
# (Packages, importing data, projects)
# =====================================================================
source("R/_setup.R")
log_open("L2-4_log.txt")
# 1) Installing packages: run once (already installed packages will not be reinstalled)
pkgs <- c("tidyverse", "psych", "lavaan", "qgraph", "bootnet", "glmnet",
          "networktools", "mgm", "igraph", "readxl", "haven", "mice", "knitr", "rmarkdown",
          "lme4")
need <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(need) > 0) install.packages(need)        # Only install missing packages
for (p in pkgs) cat(sprintf("%-13s %s\n", p, utils::packageDescription(p)$Version))

# 2) Load before each session using library()
suppressPackageStartupMessages({ library(tidyverse); library(haven) })

# 3) Import CSV and SPSS (.sav) files -- paths are relative to the project directory (relative paths)
dat  <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)
spss <- read_sav("data/clpn_sim_wide.sav")
glimpse(dat[, 1:8])
cat("Do CSV and SAV match? ", all.equal(as.numeric(dat$dep1_t1), as.numeric(spss$dep1_t1)), "\n", sep = "")
# Recommended project structure: clpn-course/ data/  R/  R/output/  (already organized in this course)
log_close()
