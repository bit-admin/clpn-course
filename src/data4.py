# -*- coding: utf-8 -*-
PACING = [
 (1,"0.1 · 0.2 · 1.1","启动：课程地图、为什么学 CLPN、变量与测量"),
 (2,"1.2 · 1.3 · 2.1 · 0.2 先跑一遍","描述统计、z 分数；安装 R（第 2–5 周 M1 统计与 M2 R 并排学）；装好 R 后做 0.2 课的“先跑一遍”（约 30 分钟）：复制现成代码，跑出第一张 CLPN 图"),
 (3,"2.2 · 1.4 · 2.3","R 语法；协方差与相关；数据框"),
 (4,"1.5 · 1.6 · 2.4","标准误、置信区间、p 值；包与导入数据"),
 (5,"2.5 · 2.6 · 阶段测验","用 R 复现统计基础；绘图与报告；M1、M2 阶段测验"),
 (6,"3.1 · 3.2 · 3.3","M1、M2 之后进入 M3 回归：简单回归、多元回归、标准化系数"),
 (7,"3.4 · 3.5 · 4.1","逻辑回归、正则化与 LASSO；纵向设计"),
 (8,"4.2 · 4.3 · 阶段测验","数据整形、缺失与流失；M3、M4 阶段测验（期中）"),
 (9,"5.1 · 5.2 · 5.3","CLPM 直觉、lavaan 实操、RI-CLPM"),
 (10,"5.4 · 6.1 · 6.2","因果推断边界；网络语言；偏相关与 GGM"),
 (11,"6.3 · 6.4 · 6.5","正则化网络、qgraph / bootnet、中心性"),
 (12,"7.1 · 7.2（2 次）","CLPN 模型逻辑；glmnet 逐节点估计"),
 (13,"7.3 · 7.4 · 7.5","CLPN 可视化、出/入 EI、多波与设计选择；进阶选学 {{C:optlist}} 不占标准课时，可在本周之后自学"),
 (14,"8.1 · 8.2（2 次）· 8.3","bootstrap、边准确性、CS 系数（本周学 4 次）"),
 (15,"9.1 · 9.2 · 9.3 · 10.1","读论文、批判、报告规范；项目设计（本周学 4 次）"),
 (16,"10.2（2 次）· 10.3","毕业项目分析、写作与汇报"),
]
REFS = [
 ("核心：CLPN 方法与应用", [
  dict(c="Wysocki, A., van Bork, R., Cramer, A. O. J., & Rhemtulla, M. (2022). <i>Cross-lagged network models</i> [Preprint]. PsyArXiv.", url="https://osf.io/preprints/psyarxiv/vjr8z_v1", v=True, note="CLPN 方法的原始预印本（2022 年 10 月 1 日）。即通常所说的“Wysocki et al. (2022)”。"),
  dict(c="Wysocki, A., McCarthy, I., van Bork, R., Cramer, A. O. J., & Rhemtulla, M. (2025). Cross-lagged panel networks. <i>advances.in/psychology, 2</i>, e739621.", url="https://doi.org/10.56296/aip00037", v=True, note="CLPN 方法论文的正式发表版（2025 年 6 月），由 2022 年的 PsyArXiv 预印本《Cross-lagged network models》修订而成，增加合著者 McCarthy。模块 7 的主要参考文献，引用时优先引用此版。"),
  dict(c="Funkhouser, C. J., et al. (2021). Unique longitudinal relationships between symptoms of psychopathology in youth: A cross-lagged panel network analysis in the ABCD study. <i>Journal of Child Psychology and Psychiatry, 62</i>(2), 184–194.", url="https://doi.org/10.1111/jcpp.13256", v=True, note="CLPN 实证应用范例（4,093 名青少年，含 T2→T3 复现），第 9.1 课精读。"),
 ]),
 ("网络心理测量学", [
  dict(c="Borsboom, D., & Cramer, A. O. J. (2013). Network analysis: An integrative approach to the structure of psychopathology. <i>Annual Review of Clinical Psychology, 9</i>, 91–121.", url="https://doi.org/10.1146/annurev-clinpsy-050212-185608", v=True, note="网络视角的奠基性综述，第 0.2 课阅读。"),
  dict(c="Epskamp, S., Borsboom, D., & Fried, E. I. (2018). Estimating psychological networks and their accuracy: A tutorial paper. <i>Behavior Research Methods, 50</i>(1), 195–212.", url="https://doi.org/10.3758/s13428-017-0862-1", v=True, note="bootnet 与稳定性检验（CS 系数）的标准教程，模块 6、8。"),
  dict(c="Epskamp, S., & Fried, E. I. (2018). A tutorial on regularized partial correlation networks. <i>Psychological Methods, 23</i>(4), 617–634.", url="https://doi.org/10.1037/met0000167", v=True, note="正则化偏相关网络（EBICglasso）教程，第 6.3 课。"),
  dict(c="Foygel, R., & Drton, M. (2010). Extended Bayesian information criteria for Gaussian graphical models. <i>Advances in Neural Information Processing Systems, 23</i>, 604–612.", url="https://proceedings.neurips.cc/paper/2010/hash/072b030ba126b2f4b2374f342be9ed44-Abstract.html", v=True, note="EBIC 用于高斯图模型的原始论文：罚项 4γ|E| log p 的出处，第 6.3 课。"),
  dict(c="Epskamp, S., Cramer, A. O. J., Waldorp, L. J., Schmittmann, V. D., & Borsboom, D. (2012). qgraph: Network visualizations of relationships in psychometric data. <i>Journal of Statistical Software, 48</i>(4), 1–18.", url="https://doi.org/10.18637/jss.v048.i04", v=True, note="qgraph 包的说明论文。"),
  dict(c="Robinaugh, D. J., Millner, A. J., & McNally, R. J. (2016). Identifying highly influential nodes in the complicated grief network. <i>Journal of Abnormal Psychology, 125</i>(6), 747–757.", url="https://doi.org/10.1037/abn0000181", v=True, note="提出期望影响（EI）指标，第 6.5 课。"),
  dict(c="Jones, P. J., Ma, R., & McNally, R. J. (2021). Bridge centrality: A network approach to understanding comorbidity. <i>Multivariate Behavioral Research, 56</i>(2), 353–367.", url="https://doi.org/10.1080/00273171.2019.1614898", v=True, note="桥接中心性与 networktools 包，第 6.5 / 7.4 课。"),
  dict(c="Fried, E. I., & Cramer, A. O. J. (2017). Moving forward: Challenges and directions for psychopathological network theory and methodology. <i>Perspectives on Psychological Science, 12</i>(6), 999–1020.", url="https://doi.org/10.1177/1745691617705892", v=True, note="网络方法学的挑战与批判，第 9.2 课。"),
  dict(c="Robinaugh, D. J., Hoekstra, R. H. A., Toner, E. R., & Borsboom, D. (2020). The network approach to psychopathology: A review of the literature 2008–2018 and an agenda for future research. <i>Psychological Medicine, 50</i>(3), 353–366.", url="https://doi.org/10.1017/S0033291719003404", v=True, note="十年文献综述，拓展阅读。"),
  dict(c="Grygiel, P., Opozda-Suder, S., & Dolata, R. (2026). The longitudinal interplay between loneliness and depressive symptoms during late childhood: Cross-lagged panel network analyses. <i>European Journal of Investigation in Health, Psychology and Education, 16</i>(6), 78.", url="https://doi.org/10.3390/ejihpe16060078", v=True, note="孤独与抑郁症状的 CLPN 实证研究（开放获取）：NLSY79 儿童与青年样本（NLSY79-CY），N = 4,333 名 10–12 岁儿童，两个时间点。见论文阅读包。"),
  dict(c="Fried, E. I., Papanikolaou, F., & Epskamp, S. (2022). Mental health and social contact during the COVID-19 pandemic: An ecological momentary assessment study. <i>Clinical Psychological Science, 10</i>(2), 340–354.", url="https://doi.org/10.1177/21677026211017839", v=True, note="密集追踪数据中的社会接触与心理健康（开放获取），见论文阅读包。"),
  dict(c="Burger, J., Isvoranu, A.-M., Lunansky, G., Haslbeck, J. M. B., Epskamp, S., Hoekstra, R. H. A., Fried, E. I., Borsboom, D., & Blanken, T. F. (2023). Reporting standards for psychological network analyses in cross-sectional data. <i>Psychological Methods, 28</i>(4), 806–824.", url="https://doi.org/10.1037/met0000471", v=True, note="网络分析报告规范，第 9.3 课。"),
  dict(c="Isvoranu, A.-M., Epskamp, S., Waldorp, L. J., & Borsboom, D. (Eds.). (2022). <i>Network psychometrics with R: A guide for behavioral and social scientists</i>. Routledge.", url="https://doi.org/10.4324/9781003111238", v=True, note="系统教材，模块 6–8 的参考书（配套网站含练习与答案）。"),
 ]),
 ("交叉滞后面板模型（CLPM / RI-CLPM）", [
  dict(c="Hamaker, E. L., Kuiper, R. M., & Grasman, R. P. P. P. (2015). A critique of the cross-lagged panel model. <i>Psychological Methods, 20</i>(1), 102–116.", url="https://doi.org/10.1037/a0038889", v=True, note="提出 RI-CLPM，第 5.3 课必读。"),
  dict(c="Mulder, J. D., & Hamaker, E. L. (2021). Three extensions of the random intercept cross-lagged panel model. <i>Structural Equation Modeling: A Multidisciplinary Journal, 28</i>(4), 638–648.", url="https://doi.org/10.1080/10705511.2020.1784738", v=True, note="配套 lavaan / Mplus 示例代码网站：jeroendmulder.github.io/RI-CLPM"),
  dict(c="Lucas, R. E. (2023). Why the cross-lagged panel model is almost never the right choice. <i>Advances in Methods and Practices in Psychological Science</i>.", url="https://doi.org/10.1177/25152459231158378", v=True, note="对 CLPM 的进一步批评，第 5.4 课。"),
  dict(c="Rosseel, Y. (2012). lavaan: An R package for structural equation modeling. <i>Journal of Statistical Software, 48</i>(2), 1–36.", url="https://doi.org/10.18637/jss.v048.i02", v=True, note="lavaan 包的说明论文，第 5.2 课。"),
 ]),
 ("正则化与 R", [
  dict(c="Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. <i>Journal of the Royal Statistical Society: Series B (Methodological), 58</i>(1), 267–288.", url="https://doi.org/10.1111/j.2517-6161.1996.tb02080.x", v=True, note="LASSO 原始论文（了解即可，数学较深）。"),
  dict(c="Friedman, J., Hastie, T., & Tibshirani, R. (2010). Regularization paths for generalized linear models via coordinate descent. <i>Journal of Statistical Software, 33</i>(1), 1–22.", url="https://doi.org/10.18637/jss.v033.i01", v=True, note="glmnet 包的说明论文，第 3.5 / 7.2 课。"),
  dict(c="Wickham, H., Çetinkaya-Rundel, M., & Grolemund, G. (2023). <i>R for data science</i> (2nd ed.). O'Reilly.（免费在线版）", url="https://r4ds.hadley.nz/", v=True, note="模块 2 的主要自学教材。"),
 ]),
 ("统计基础与缺失数据", [
  dict(c="Field, A., Miles, J., & Field, Z. (2012). <i>Discovering statistics using R</i>. SAGE.", url="https://www.sagepub.com/en-us/nam/discovering-statistics-using-r/book236067", v=True, note="统计与 R 的入门教材，可配合模块 1–3。2012 年 SAGE 出版，作者为 Andy Field、Jeremy Miles、Zoë Field。这本书没有 DOI，以出版社书目页为准。"),
  dict(c="Enders, C. K. (2022). <i>Applied missing data analysis</i> (2nd ed.). The Guilford Press.", url="https://www.guilford.com/books/Applied-Missing-Data-Analysis/Craig-Enders/9781462549863", v=True, note="缺失数据教材，第 4.3 课拓展阅读。现行版本是 2022 年第 2 版（精装 ISBN 978-1-4625-4986-3，546 页）；第 1 版出版于 2010 年。"),
 ]),
 ("测量不变性、样本量规划与组间比较（进阶选学）", [
  dict(c="Putnick, D. L., & Bornstein, M. H. (2016). Measurement invariance conventions and reporting: The state of the art and future directions for psychological research. <i>Developmental Review, 41</i>, 71–90.", url="https://doi.org/10.1016/j.dr.2016.06.004", note="测量不变性的综述：构形、度量、标量三级的含义，以及报告时要写哪些数字。7.6 课。"),
  dict(c="Cheung, G. W., & Rensvold, R. B. (2002). Evaluating goodness-of-fit indexes for testing measurement invariance. <i>Structural Equation Modeling, 9</i>(2), 233–255.", url="https://doi.org/10.1207/S15328007SEM0902_5", note="ΔCFI ≥ −0.01 这条经验规则的出处。7.6 课。"),
  dict(c="Chen, F. F. (2007). Sensitivity of goodness of fit indexes to lack of measurement invariance. <i>Structural Equation Modeling, 14</i>(3), 464–504.", url="https://doi.org/10.1080/10705510701301834", note="用模拟研究比较拟合指标，提出 ΔCFI 与 ΔRMSEA ≤ 0.015 一起看。7.6 课。"),
  dict(c="Constantin, M. A., Schuurman, N. K., & Vermunt, J. K. (2026). A general Monte Carlo method for sample size analysis in the context of network models. <i>Psychological Methods, 31</i>(3), 385–405.", url="https://doi.org/10.1037/met0000555", note="网络模型样本量规划的一般方法：先假定真实网络，再用模拟找出所需的 N。7.6 课的模拟是它的简化版。"),
  dict(c="van Borkulo, C. D., van Bork, R., Boschloo, L., Kossakowski, J. J., Tio, P., Schoevers, R. A., Borsboom, D., & Waldorp, L. J. (2023). Comparing network structures on three aspects: A permutation test. <i>Psychological Methods, 28</i>(6), 1273–1285.", url="https://doi.org/10.1037/met0000476", note="网络比较检验（NCT）：M（网络结构）、S（整体强度）与单条边三种检验。7.7 课的手写置换检验沿用它的思路。"),
  dict(c="Ackeret, N., Röthlin, P., Horvath, S., & Allemand, M. (2023). <i>Positive mental health among sports coaches: A six-month longitudinal study</i> [Data set, version 3]. Dryad.", url="https://doi.org/10.5061/dryad.8931zcrws", note="7.6 课练习用的真实数据（CC0），收录为 data/coaches_mhc_raw.csv；已知问题见数据字典。"),
 ]),
]

# ---- 课程规模：唯一来源 ----
# 页面里的课数和周数都由这里生成：源文件写 {{C:size}}、{{C:weeks}} 等，构建时用 fillC() 替换；键名不存在会报错。
# 进阶选学课在 data*.py 的课程 dict 里写 opt=True：它们不计入核心课数、标准节奏的课次和课时。
# 手写文档（README.md、src/README.md，以及本地的 CLAUDE.md，若存在）不能用宏，build.py 会检查它们写的是不是当前的 COURSE_SIZE。
_LS = [l for _m in MODULES for l in _m["lessons"]]
N_LESSONS = len(_LS)
N_OPT = sum(1 for l in _LS if l.get("opt"))
N_CORE = N_LESSONS - N_OPT
N_WEEKS = len(PACING)
COURSE_SIZE = f"{N_CORE} 节核心课 + {N_OPT} 节选学" if N_OPT else f"{N_CORE} 节课"
OPT_IDS = [l["id"] for l in _LS if l.get("opt")]
COUNTS = {"optlist": "、".join(OPT_IDS) or "（无）", "size": COURSE_SIZE, "core": str(N_CORE), "opt": str(N_OPT), "all": str(N_LESSONS),
          "weeks": str(N_WEEKS), "mods": str(len(MODULES))}
def fillC(s):
    import re as _re
    def _rep(m):
        if m.group(1) not in COUNTS: raise KeyError("未知的课程规模键：" + m.group(1))
        return COUNTS[m.group(1)]
    return _re.sub(r"\{\{C:([a-z]+)\}\}", _rep, s)
