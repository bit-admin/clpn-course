# =====================================================================
# L9-3.R  报告规范：可被复核的方法与结果  (Reporting: versions, seeds, settings)
# 自动生成一份“分析信息清单”，可直接粘贴到方法部分/补充材料
# =====================================================================
source("R/_setup.R")
log_open("L9-3_reporting_info.txt")
pk <- c("glmnet", "qgraph", "bootnet", "networktools", "lavaan", "psych", "tidyverse")
cat("== 软件 Software ==\n", R.version.string, "\n")
# 版本号用包自己的写法（DESCRIPTION 里的 Version，如 glmnet 的 "4.1-8"）。
# as.character(packageVersion(p)) 会把连字符改成点（"4.1.8"），与 sessionInfo() 和 CRAN 上的写法不一致。
for (p in pk) cat(sprintf("  %s %s\n", p, utils::packageDescription(p)$Version))
cat("\n== CLPN 方法部分必须报告的要素（勾选清单）==\n",
"[ ] 数据：样本量、波次、间隔、题目内容与计分\n",
"[ ] 缺失与流失处理（列表删除 / 多重插补 / FIML）\n",
"[ ] 标准化：所有题目在估计前 z 标准化\n",
"[ ] 估计：每个 T2 题目对全部 T1 题目做 LASSO（glmnet，alpha = 1）\n",
"[ ] λ 选择：10 折交叉验证 lambda.min（或 lambda.1se / EBIC，γ = ?）\n",
"[ ] 随机种子：set.seed(2026)\n",
"[ ] 协变量及是否惩罚（penalty.factor）\n",
"[ ] 中心性：out-EI / in-EI（不含自回归边），桥接 EI 的社群定义\n",
"[ ] 稳定性：非参数 bootstrap（次数）、case-dropping CS 系数\n",
"[ ] 敏感性分析：λ 规则、种子、去除冗余题目、T2→T3 复现\n",
"[ ] 软件版本（见上）与代码/数据共享链接（OSF）\n")
# sessionInfo() 会列出所有已加载的包（tidyverse 会带进来上百个），全文很长。
# 日志里只放开头部分：R 版本、平台、语言环境和直接加载（attached）的包，到 "loaded via a namespace" 为止，
# 通常 20 多行；后面间接载入的几十个包不放进日志。完整内容单独存一份，附在补充材料里。
# 先加载分析用到的包，sessionInfo() 才会把它们列在 "other attached packages" 下。
suppressPackageStartupMessages(for (p in pk) library(p, character.only = TRUE))
si <- capture.output(print(sessionInfo()))
# 课程仓库里公开的这份输出删去了本机的数值库路径、语言环境和时区（Matrix products … tzcode 这几行）。
# 你自己的研究不必删：这些信息有助于复现，只是公开前要想好是否愿意公开。
a <- grep("^Matrix products", si)[1]; b <- grep("^attached base packages", si)[1]
if (!is.na(a) && !is.na(b) && b > a) si <- c(si[seq_len(a - 1)], "（本机路径、语言环境与时区已略去）", "", si[b:length(si)])
writeLines(si, out("sessionInfo_full.txt"))
k <- grep("^loaded via a namespace", si)[1]
n_show <- if (is.na(k)) min(25, length(si)) else k - 1
cat("\n== sessionInfo()（前", n_show, "行；完整的", length(si), "行见 R/output/sessionInfo_full.txt）==\n")
cat(head(si, n_show), sep = "\n")
log_close()
