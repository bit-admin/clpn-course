# =====================================================================
# data_elsoc.R  下载并预处理 ELSOC 真实数据（真实数据案例，见 materials/case_elsoc.html）
# Download & preprocess the ELSOC panel (Estudio Longitudinal Social de Chile 2016–2021)
#
# 数据来源（Harvard Dataverse 推荐的引用格式）：
#   Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022,
#   "Estudio Longitudinal Social de Chile 2016-2021", https://doi.org/10.7910/DVN/LQMURF,
#   Harvard Dataverse, V1, UNF:6:z/vWFguq9fg03YaOLWFddA== [fileUNF]
#   许可：CC0 1.0（Dataverse 数据集页面的标注），可以再分发。
#   本脚本固定使用 V1 的文件 ELSOC_Wide_2016_2021_v1.00_R.RData（4.8 MB，MD5 校验）。
#
# 原始文件 data/elsoc/ELSOC_Wide_2016_2021_v1.00_R.RData 和预处理后的分析文件 data/elsoc_phq8_wide.csv
# 都随课程提供（仓库和 clpn-course.zip 里都有）。本脚本记录分析文件是怎样从原始文件得到的：
# 原始文件在、且 MD5 正确时直接用它（不需要联网）；不在时才从 Harvard Dataverse 下载（不需要注册）。
# 然后重新写出 data/elsoc_phq8_wide.csv，结果应与随课程提供的文件完全相同。run_all.R 会运行本脚本。
#
# 处理：只保留原始样本（2016 年招募）；负数缺失码（−999 / −888 / −777 / −666）设为 NA；
# 取 2016、2017、2018 三波的 PHQ 第 1–8 题（PHQ-8）和性别、年龄；不保留原始编号。
# 为什么去掉第 9 题：第 9 题问的是“想到死亡或伤害自己”，属于需要临床跟进的高风险条目，
# 不适合在教学练习里当作普通节点分析，研究中常用的 PHQ-8 也不含这一题。
#
# 输出：data/elsoc_phq8_wide.csv（分析用）、R/output/data_elsoc_log.txt（运行记录）
# 下一步：R/case_elsoc.R（CLPN 分析）。运行时间：下载约 5–60 秒（看网速），处理约 2 秒。
# =====================================================================
source("R/_setup.R")
t_start <- Sys.time()

DOI       <- "10.7910/DVN/LQMURF"
VERSION   <- "V1"
FILE_ID   <- 6160174
FILE_NAME <- "ELSOC_Wide_2016_2021_v1.00_R.RData"
FILE_MD5  <- "a5a45571d39cf9db12e1949fdcb6fff2"
URL       <- paste0("https://dataverse.harvard.edu/api/access/datafile/", FILE_ID)
DATA_DIR  <- "data/elsoc"
dir.create(DATA_DIR, showWarnings = FALSE, recursive = TRUE)
raw_file  <- file.path(DATA_DIR, FILE_NAME)

# 下载失败时给出中文说明后停止（网络不通、被代理拦截、服务器维护等）
download_failed <- function(why) {
  cat("\n================ 下载失败 ================\n",
      "没能从 Harvard Dataverse 下载 ELSOC 数据。\n",
      "原因（R 给出的信息）：", why, "\n\n",
      "可以这样做：\n",
      "1. 检查网络：在浏览器里打开 https://doi.org/", DOI, " ，看能不能打开。\n",
      "2. 如果在学校或公司网络里，可能需要设置代理；也可以换一个网络（例如手机热点）再试。\n",
      "3. 服务器偶尔维护，过一会儿重新运行本脚本即可。\n",
      "4. 也可以手动下载：在上面的网页里找到文件 ", FILE_NAME, "，\n",
      "   下载后放进课程文件夹的 ", DATA_DIR, "/ 里，再运行本脚本（会跳过下载这一步）。\n",
      "==========================================\n", sep = "")
  stop("ELSOC 数据下载失败，见上面的说明。", call. = FALSE)
}

md5_ok <- function(f) file.exists(f) && unname(tools::md5sum(f)) == FILE_MD5

# ---- 第 1 步：下载（已经下载过且校验正确就跳过）----------------------
if (md5_ok(raw_file)) {
  cat("已找到下载好的文件，跳过下载：", raw_file, "\n")
} else {
  cat("正在从 Harvard Dataverse 下载", FILE_NAME, "（约 4.8 MB）……\n")
  tmp <- tempfile(fileext = ".RData")
  old_timeout <- options(timeout = max(300, getOption("timeout")))
  res <- tryCatch(download.file(URL, tmp, mode = "wb", quiet = TRUE),
                  error = function(e) conditionMessage(e),
                  warning = function(w) conditionMessage(w))
  options(old_timeout)
  if (!identical(res, 0L) && !identical(res, 0)) {
    unlink(tmp); download_failed(as.character(res))
  }
  if (unname(tools::md5sum(tmp)) != FILE_MD5) {
    unlink(tmp)
    download_failed(paste0("下载的文件不完整或不是预期的版本（MD5 校验不一致）。",
                           "数据集如有新版本，本脚本仍固定使用 ", VERSION, "。"))
  }
  file.copy(tmp, raw_file, overwrite = TRUE); unlink(tmp)
  cat("下载完成，MD5 校验通过。\n")
}

# ---- 第 2 步：读入并预处理 -------------------------------------------
log_open("data_elsoc_log.txt")
cat("ELSOC 数据预处理记录\n")
cat("数据：Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022,\n",
    "      \"Estudio Longitudinal Social de Chile 2016-2021\", https://doi.org/", DOI, ",\n",
    "      Harvard Dataverse, ", VERSION, "（CC0 1.0）\n", sep = "")
cat("文件：", FILE_NAME, "  MD5 = ", FILE_MD5, "（校验通过）\n\n", sep = "")

env <- new.env()
obj <- load(raw_file, envir = env)
d <- get(obj[1], envir = env)
cat("原始数据：", nrow(d), "行 ×", ncol(d), "列\n")
cat("样本构成（muestra）：原始样本", sum(d$muestra == 1), "人，补充样本（2018 年起）",
    sum(d$muestra == 2), "人\n")

clean <- function(x) { x <- as.numeric(x); x[x < 0] <- NA; x }   # 负数是各种缺失码
phq_zh <- c("兴趣减退", "情绪低落", "睡眠问题", "疲乏", "食欲改变", "注意力难集中", "自我评价低", "动作迟缓")
cat("\nPHQ 题目（ELSOC 的题目顺序与标准 PHQ-9 第 6、7 题互换；1 = 从不 … 5 = 每天）：\n")
for (i in 1:8) {
  v <- sprintf("s11_%02d_w01", i)
  cat(sprintf("  phq%d  %-6s  %s\n", i, phq_zh[i], sub(" \\(estado de animo\\) \\(2016\\)", "", attr(d[[v]], "label"))))
}
cat("  （第 9 题“想到死亡或伤害自己”不导出：高风险条目，不作为教学练习的节点。）\n")

keep <- d$muestra == 1                       # 只用原始样本，三波都有机会参加
w <- data.frame(id = seq_len(sum(keep)),     # 新编号；不保留原始编号 idencuesta
                female = as.integer(clean(d$m0_sexo_w01[keep]) == 2),
                age = clean(d$m0_edad_w01[keep]))
for (t in 1:3) for (i in 1:8)
  w[[sprintf("phq%d_t%d", i, t)]] <- clean(d[[sprintf("s11_%02d_w%02d", i, t)]][keep])

phq_t <- function(t) sprintf("phq%d_t%d", 1:8, t)
cc <- function(ts) complete.cases(w[, unlist(lapply(ts, phq_t))])
cat("\n原始样本 N =", nrow(w), "\n")
for (t in 1:3) cat(sprintf("  第 %d 波（%d 年）PHQ-8 完整：%d 人\n", t, 2015 + t, sum(cc(t))))
cat("  第 1–2 波都完整：", sum(cc(1:2)), "人；第 1–3 波都完整：", sum(cc(1:3)), "人（CLPN 分析用）\n")
a <- w[cc(1:3), ]
cat(sprintf("  第 1–3 波完整者：女性 %d 人（%.1f%%），2016 年年龄 M = %.1f，SD = %.1f，范围 %d–%d\n",
            sum(a$female, na.rm = TRUE), 100 * mean(a$female, na.rm = TRUE),
            mean(a$age, na.rm = TRUE), sd(a$age, na.rm = TRUE), min(a$age, na.rm = TRUE), max(a$age, na.rm = TRUE)))

out_csv <- "data/elsoc_phq8_wide.csv"
write.csv(w, out_csv, row.names = FALSE)
cat("\n已写出", out_csv, "：", nrow(w), "行 ×", ncol(w), "列（随课程提供的就是这个文件）\n")
cat("下一步：source(\"R/case_elsoc.R\")\n")
log_close()
cat("用时", round(as.numeric(difftime(Sys.time(), t_start, units = "secs")), 1), "秒\n")
