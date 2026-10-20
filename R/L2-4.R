# =====================================================================
# L2-4.R  安装包、导入数据与项目管理  (Packages, importing data, projects)
# =====================================================================
source("R/_setup.R")
log_open("L2-4_log.txt")
# 1) 安装包：只需做一次（已安装的包不会重复安装）
pkgs <- c("tidyverse", "psych", "lavaan", "qgraph", "bootnet", "glmnet",
          "networktools", "mgm", "igraph", "readxl", "haven", "mice", "knitr", "rmarkdown",
          "lme4")
need <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(need) > 0) install.packages(need)        # 只安装缺少的
for (p in pkgs) cat(sprintf("%-13s %s\n", p, utils::packageDescription(p)$Version))

# 2) 每次使用前用 library() 加载
suppressPackageStartupMessages({ library(tidyverse); library(haven) })

# 3) 导入 CSV 和 SPSS (.sav) 文件 —— 路径是“相对项目文件夹”的相对路径（relative path）
dat  <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)
spss <- read_sav("data/clpn_sim_wide.sav")
glimpse(dat[, 1:8])
cat("CSV 与 SAV 是否同一份数据？", all.equal(as.numeric(dat$dep1_t1), as.numeric(spss$dep1_t1)), "\n")
# 推荐的项目结构：clpn-course/ data/  R/  R/output/  （本课程已经建好）
log_close()
