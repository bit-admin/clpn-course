# =====================================================================
# run_all.R —— 按课程顺序依次运行所有脚本，并报告哪些成功、哪些失败
# 用法：在 RStudio 打开 clpn-course.Rproj 后 source("R/run_all.R")
#       或终端（在 clpn-course 文件夹里）：Rscript R/run_all.R
#       完整运行约 40–95 分钟（视电脑而定），大部分时间在 bootstrap；
#       bootstrap 为保证可重复，默认单核 nCores = 1，见 L8-2.R 开头说明。
# 课文脚本按课号排序，字母后缀紧跟在同一课之后，所以毕业项目按 L10-1 → L10-2 → L10-2b → L10-3 的依赖顺序运行。
# 先运行全部课文脚本（R/L*.R）和期末答案脚本 R/assess_answers.R，再运行全部答案脚本（R/solutions/*.R）。
# 也运行真实数据案例：R/data_elsoc.R（从随课程提供的原始文件重新写出 data/elsoc_phq8_wide.csv）和 R/case_elsoc.R。
# 课程压缩包 clpn-course.zip 与 GitHub 仓库都带有 R/solutions/；万一缺少，答案部分会跳过并提示。
# =====================================================================
source("R/_setup.R")
lesson_key <- function(f) {                       # L7-5.R → 705；L7-5b.R → 705.02（紧跟在 L7-5.R 之后）
  m <- regmatches(basename(f), regexec("L([0-9]+)-([0-9]+)([a-z]?)", basename(f)))[[1]]
  as.numeric(m[2]) * 100 + as.numeric(m[3]) + ifelse(m[4] == "", 0, (utf8ToInt(m[4]) - 96) / 100) }
files <- list.files("R", pattern = "^L[0-9]+-[0-9]+[a-z]?\\.R$", full.names = TRUE)
files <- files[order(sapply(files, lesson_key))]
if (file.exists("R/assess_answers.R")) files <- c(files, "R/assess_answers.R")   # 期末 C 部分答案（文件名不是 L*.R，单独列出）
for (f_el in c("R/data_elsoc.R", "R/case_elsoc.R"))                              # 真实数据案例（约 1–2 分钟）
  if (file.exists(f_el)) files <- c(files, f_el)
sols <- if (dir.exists("R/solutions")) list.files("R/solutions", pattern = "\\.R$", full.names = TRUE) else character(0)
sols <- sols[order(sapply(sols, lesson_key))]
cat(sprintf("课文脚本 %d 个；答案脚本 %d 个%s\n", length(files), length(sols),
            if (length(sols) == 0) "（R/solutions/ 中没有答案脚本，跳过；答案脚本随课程压缩包 clpn-course.zip 和 GitHub 仓库提供）" else ""))
status <- data.frame()
for (f in c(files, sols)) {
  t0 <- Sys.time()
  ok <- tryCatch({ if (grepl("solutions", f)) source(f, local = new.env(), print.eval = TRUE, echo = FALSE)  # 答案脚本：像逐行运行一样自动打印结果
                  else sys.source(f, envir = new.env()); "OK 成功" },
                 error = function(e) paste("FAIL 失败:", conditionMessage(e)))
  while (sink.number() > 0) sink()
  grDevices::graphics.off()
  setwd(find_root())
  status <- rbind(status, data.frame(script = f, status = ok,
                                     seconds = round(as.numeric(difftime(Sys.time(), t0, units = "secs")))))
  cat(sprintf("%-32s %-8s %5ss\n", f, substr(ok, 1, 60), tail(status$seconds, 1)))
}
write.csv(status, file.path("R", "output", "run_all_status.csv"), row.names = FALSE)
