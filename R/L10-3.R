# =====================================================================
# L10-3.R  毕业项目③：从输出自动生成“结果部分”草稿  (Auto-filled results draft)
# 原则：结果部分的每个数字都必须能在代码输出中找到 —— 所以让代码来填数字。
# =====================================================================
source("R/_setup.R")
CHAIN <- "R/L4-3.R → R/L10-1.R → R/L10-2.R → R/L10-2b.R → R/L10-3.R"
need_output("L10-2_results.rds", "R/L10-2.R", chain = CHAIN)   # 前置结果检查
need_output("L10-2b_results.rds", "R/L10-2b.R", chain = CHAIN)  # 必做的完整流程敏感性分析
res <- readRDS(out("L10-2_results.rds"))            # 需先运行 L10-2.R
B <- res$B; CL <- cl_only(B); cen <- res$cen; cs <- res$cs
el <- edge_list(CL)[1:3, ]
f <- function(x) sprintf("%.2f", x)
fr <- function(r) ifelse(abs(r) < 1 & abs(round(r, 2)) >= 1, sprintf("%.3f", r), sprintf("%.2f", r))  # 0.997 不写成 1.00
# 必做的敏感性分析：Wysocki 等人（2025）的完整流程（R/L10-2b.R）。与主分析并列报告，数字同样由代码填入。
fp <- readRDS(out("L10-2b_results.rds")); s <- fp$summary
f3p <- function(p) ifelse(p < .001, "< 0.001", sprintf("= %.3f", p))
ic_txt <- if (s["aic_equal"] <= s["aic_free"] && s["bic_equal"] <= s["bic_free"]) "AIC 与 BIC 均偏向约束模型" else
  if (s["aic_equal"] > s["aic_free"] && s["bic_equal"] > s["bic_free"]) "AIC 与 BIC 均偏向不约束模型" else
  sprintf("AIC 偏向%s模型，BIC 偏向%s模型", ifelse(s["aic_equal"] <= s["aic_free"], "约束", "不约束"),
          ifelse(s["bic_equal"] <= s["bic_free"], "约束", "不约束"))
top <- head(fp$edges[fp$edges$lasso != 0, ], s["top_n"])
drop <- top[!top$kept_p01, ]
drop_txt <- if (nrow(drop) == 0) "这些边全部保留" else
  paste0("未保留的是：", paste(sprintf("T1“%s”→ T2“%s”（主分析 β = %s；完整流程 β = %s，p %s）",
                                    drop$from_zh, drop$to_zh, f(drop$lasso), f(drop$sem_est), f3p(drop$sem_p)), collapse = "、"))
fp_par <- paste0(
  sprintf("完整流程敏感性分析。按照 Wysocki 等人（2025）推荐的完整流程，先在 T1→T2 与 T2→T3 两段分别做逐节点 LASSO，任一段非零的 %d 条交叉滞后路径进入路径模型（其余固定为 0），再在 lavaan 中无惩罚地重新估计（同一波内残差两两相关，FIML）。",
          s["n_keep"]),
  sprintf("跨时间等值约束的嵌套检验为 Δχ²(%d) = %.2f，p %s，%s，因此最终采用%s（χ²(%d) = %.2f，CFI = %.3f，TLI = %.3f，RMSEA = %.3f，SRMR = %.3f）。",
          s["eq_ddf"], s["eq_dchisq"], f3p(s["eq_p"]), ic_txt,
          ifelse(fp$use_equal, "两段路径相等的约束模型", "两段路径各自估计的不约束模型（下文报告 T1→T2 段）"),
          s["fin_df"], s["fin_chisq"], s["fin_cfi"], s["fin_tli"], s["fin_rmsea"], s["fin_srmr"]),
  sprintf("按 p < .01 修剪后保留 %d 条交叉滞后边（孤独→抑郁 %d 条，抑郁→孤独 %d 条，构念内 %d 条）。",
          s["n_sig01"], s["n_sig01_ld"], s["n_sig01_dl"], s["n_sig01_within"]),
  sprintf("主分析的 %d 条非零交叉滞后边中有 %d 条在完整流程中保留；主分析最强的 %d 条边中有 %d 条保留，%s。",
          s["n_lasso_main"], s["n_both"], s["top_n"], s["top_kept"], drop_txt),
  sprintf("修剪后，从孤独到抑郁方向的边权重之和为 %s，从抑郁到孤独方向为 %s（主分析分别为 %s 和 %s）。",
          f(s["ld_full"]), f(s["dl_full"]), f(s["ld_lasso"]), f(s["dl_lasso"])))
txt <- c(
  "## 结果（草稿，自动填数）", "",
  sprintf("交叉滞后面板网络包含 9 个节点，共估计出 %d 条非零交叉滞后边（共 72 条可能的边）。自回归边介于 %s 至 %s 之间。",
          sum(CL != 0), f(min(diag(B))), f(max(diag(B)))),
  sprintf("最强的三条交叉滞后边依次为：T1“%s”→ T2“%s”（β = %s）、T1“%s”→ T2“%s”（β = %s）和 T1“%s”→ T2“%s”（β = %s）。",
          item_zh[el$from[1]], item_zh[el$to[1]], f(el$weight[1]), item_zh[el$from[2]], item_zh[el$to[2]], f(el$weight[2]),
          item_zh[el$from[3]], item_zh[el$to[3]], f(el$weight[3])),
  sprintf("从孤独到抑郁方向的边权重之和为 %s，从抑郁到孤独方向为 %s。",
          f(sum(CL[1:4, 5:9])), f(sum(CL[5:9, 1:4]))),
  sprintf("出期望影响最高的节点为“%s”（out-EI = %s），入期望影响最高的节点为“%s”（in-EI = %s）。",
          cen$zh[which.max(cen$outEI)], f(max(cen$outEI)), cen$zh[which.max(cen$inEI)], f(max(cen$inEI))),
  sprintf("case-dropping bootstrap 显示，out-EI 的 CS 系数为 %s，in-EI 为 %s；%s",
          f(cs["outExpectedInfluence"]), f(cs["inExpectedInfluence"]),
          paste0(ifelse(min(cs) < .25, "其中 CS < 0.25 的指标排序不予解释。", "两者均达到可接受水平。"),
                 paste0(sapply(names(cs)[abs(cs - .5) < diff(seq(0.05, 0.75, length.out = 10))[1]], function(k)   # 与 0.5 相差不到一个删除比例网格档
                   sprintf("%s 的 CS 接近 0.5 的界值（边缘稳定；换随机种子可能落到相邻一档），其排序仅作谨慎解释。",
                           ifelse(k == "inExpectedInfluence", "in-EI", "out-EI"))), collapse = ""))),
  sprintf("敏感性分析中，lambda.1se、加入协变量以及 T2→T3 网络与主分析边权重的相关分别为 %s。",
          paste(fr(res$sens$r_with_main), collapse = "、")),
  "", fp_par,
  "", "（局限性提示：观测得分 CLPN 混合了被试间与被试内效应；结果为预测关系，不能作因果解释。）")
writeLines(txt, out("L10-3_results_draft.md"))
cat(txt, sep = "\n")
