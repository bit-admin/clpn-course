# =====================================================================
# L10-1.R  毕业项目①：数据准备、代码本与分析计划  (Data prep, codebook, analysis plan)
# =====================================================================
source("R/_setup.R")
need_output("L4-3_data_with_attrition.csv", "R/L4-3.R", chain = "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-2b.R → R/L10-3.R")   # 前置结果检查
suppressPackageStartupMessages(library(tidyverse))
log_open("L10-1_log.txt")
raw <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)

# 1) 数据清理检查：取值范围、重复 ID、缺失
item_cols <- c(vars_t(1), vars_t(2), vars_t(3))
rng <- sapply(raw[item_cols], range)
cat("所有题目取值范围：\n"); print(rng)
# 只看最小、最大值不够：2.5 这样的非整数、或 1–4 分题里混进的 0，都可能落在范围以内。
# 所以逐个值检查：每个题目的取值必须属于允许的取值集合（孤独 1, 2, 3, 4；抑郁 0, 1, 2, 3）。
allowed <- function(v) if (startsWith(v, "lone")) 1:4 else 0:3
n_bad <- sapply(item_cols, function(v) sum(!is.na(raw[[v]]) & !(raw[[v]] %in% allowed(v))))
cat("不在允许取值集合内的值的个数（越界值、非整数都会被计入）：合计 =", sum(n_bad), "\n")
if (any(n_bad > 0)) print(n_bad[n_bad > 0])
stopifnot(all(n_bad == 0))
cat("重复 ID 数 =", sum(duplicated(raw$id)), "；缺失值总数 =", sum(is.na(raw)), "\n")
# （若有反向题：raw <- raw |> mutate(item_r = 5 - item)；本数据无反向题）

# 2) 流失分析模板（本数据无流失；如用 L4-3 的流失数据可直接替换文件名）
att <- read_csv(out("L4-3_data_with_attrition.csv"), show_col_types = FALSE)  # 需先运行 L4-3.R
att$stay <- !is.na(att$dep1_t2)
cat("\n（流失数据示例）留存率 =", round(mean(att$stay), 3), "\n")
print(att |> group_by(stay) |> summarise(T1抑郁 = mean(rowSums(across(dep1_t1:dep5_t1))),
                                          T1孤独 = mean(rowSums(across(lone1_t1:lone4_t1))), n = n()))

# 3) 代码本 codebook：变量 + 描述统计（题目原文等说明在脚本末尾并入，见第 5 部分）
dict <- read.csv("data/data_dictionary.csv", fileEncoding = "UTF-8")
cb <- data.frame(variable = item_cols, mean = round(colMeans(raw[item_cols]), 2),
                 sd = round(sapply(raw[item_cols], sd), 2))
write.csv(cb, out("L10-1_codebook_stats.csv"), row.names = FALSE)
clean <- raw |> select(id, all_of(item_cols), gender, age)
write_csv(clean, out("L10-1_clean_data.csv"))

# 4) 一页分析计划（在看结果之前写好！）
plan <- c("# 分析计划（简易预注册）",
  "研究问题：T1 的孤独感题目在多大程度上独特地预测 T2 的抑郁症状题目，反之亦然？（避免“导致”）",
  "节点：lone1–lone4、dep1–dep5（9 个）；时间段：T1→T2（主分析），T2→T3（复现）",
  "估计：逐节点 LASSO（glmnet），10 折 CV，lambda.min；set.seed(2026)；题目 z 标准化",
  "中心性：out-EI、in-EI、桥接 out/in-EI（社群 = 孤独/抑郁），不含自回归边",
  "稳定性：非参数 bootstrap 1000 次；case-dropping 1000 次，CS ≥ 0.25 才解释排序",
  "敏感性：lambda.1se；加入性别、年龄为不惩罚协变量；T2→T3 复现",
  paste0("敏感性（必做）：Wysocki 等人（2025）的完整流程（R/L10-2b.R）：LASSO 选边（T1→T2、T2→T3，两段都为 0 才固定为 0）",
         "→ lavaan 无惩罚重估（同波残差相关，FIML）→ 跨时间等值检验（嵌套 χ² + AIC/BIC）选最终模型 → 按 p < .01 修剪",
         "→ in-/out-prediction；逐条报告主分析的边在完整流程中是否保留，两种分析不一致的边只作探索性解释"),
  "缺失处理：本数据无缺失；若有，报告流失分析并使用多重插补")
writeLines(plan, out("L10-1_analysis_plan.md")); cat("\n", plan, sep = "\n")

# 5) 完整代码本：题目原文、取值含义、波次 + 描述统计
# 数据字典里一行对应一个题目的三波（如 "lone1_t1 / _t2 / _t3"），先取出题目名再与每一列对应。
dict$item <- sub("_t1.*$", "", dict$variable)
codebook <- data.frame(variable = item_cols,
                       item = sub("_t[0-9]+$", "", item_cols),
                       wave = as.integer(sub("^.*_t", "", item_cols)))
codebook <- merge(codebook, dict[, c("item", "label_zh", "label_en", "values")], by = "item", sort = FALSE)
codebook <- merge(codebook, cb, by = "variable", sort = FALSE)
codebook <- codebook[match(item_cols, codebook$variable),
                     c("variable", "wave", "label_zh", "label_en", "values", "mean", "sd")]
stopifnot(nrow(codebook) == length(item_cols), !anyNA(codebook$label_zh))
write.csv(codebook, out("L10-1_codebook.csv"), row.names = FALSE, fileEncoding = "UTF-8")
cat("\n代码本（R/output/L10-1_codebook.csv，", nrow(codebook), "行；这里只显示 T1 的 9 题）：\n")
print(codebook[codebook$wave == 1, c("variable", "label_zh", "label_en", "mean", "sd")], row.names = FALSE)
log_close()
