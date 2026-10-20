# -*- coding: utf-8 -*-
PACING = [
 (1, "0.1 · 0.2 · 1.1", "Getting started: course map, why learn CLPN, variables and measurement"),
 (2, "1.2 · 1.3 · 2.1 · 0.2 Quick Run", "Descriptive statistics, z-scores; install R (in Weeks 2–5, M1 Statistics and M2 R are studied side by side); once R is installed, do the 'Quick Run' in Lesson 0.2 (about 30 min): copy the ready-made code and produce your first CLPN plot"),
 (3, "2.2 · 1.4 · 2.3", "R syntax; covariance and correlation; data frames"),
 (4, "1.5 · 1.6 · 2.4", "Standard errors, confidence intervals, p-values; packages and importing data"),
 (5, "2.5 · 2.6 · Module Quizzes", "Redoing the statistics basics in R; plots and reports; M1 and M2 module quizzes"),
 (6, "3.1 · 3.2 · 3.3", "After M1 and M2, on to M3 Regression: simple regression, multiple regression, standardized coefficients"),
 (7, "3.4 · 3.5 · 4.1", "Logistic regression, regularization and LASSO; longitudinal designs"),
 (8, "4.2 · 4.3 · Module Quizzes", "Reshaping data, missing data and attrition; M3 and M4 module quizzes (midterm)"),
 (9, "5.1 · 5.2 · 5.3", "CLPM intuition, lavaan in practice, RI-CLPM"),
 (10, "5.4 · 6.1 · 6.2", "The limits of causal inference; the language of networks; partial correlation and GGMs"),
 (11, "6.3 · 6.4 · 6.5", "Regularized networks, qgraph / bootnet, centrality"),
 (12, "7.1 · 7.2 (2 sessions)", "CLPN model logic; nodewise estimation with glmnet"),
 (13, "7.3 · 7.4 · 7.5", "CLPN visualization, out/in-EI, multi-wave data and design choices; the optional advanced lessons {{C:optlist}} are not part of the standard hours and can be studied after this week"),
 (14, "8.1 · 8.2 (2 sessions) · 8.3", "Bootstrap, edge accuracy, CS-coefficient (4 sessions this week)"),
 (15, "9.1 · 9.2 · 9.3 · 10.1", "Reading papers, critique, reporting standards; project design (4 sessions this week)"),
 (16, "10.2 (2 sessions) · 10.3", "Capstone project: analysis, write-up and presentation"),
]
REFS = [
 ("Core: CLPN Methodology and Applications", [
  dict(c="Wysocki, A., van Bork, R., Cramer, A. O. J., & Rhemtulla, M. (2022). <i>Cross-lagged network models</i> [Preprint]. PsyArXiv.", url="https://osf.io/preprints/psyarxiv/vjr8z_v1", v=True, note="The original preprint of the CLPN method (October 1, 2022); this is the paper usually cited as 'Wysocki et al. (2022)'."),
  dict(c="Wysocki, A., McCarthy, I., van Bork, R., Cramer, A. O. J., & Rhemtulla, M. (2025). Cross-lagged panel networks. <i>advances.in/psychology, 2</i>, e739621.", url="https://doi.org/10.56296/aip00037", v=True, note="The published version of the CLPN method paper (June 2025), revised from the 2022 PsyArXiv preprint 'Cross-lagged network models', with McCarthy added as a co-author. The main reference for Module 7; cite this version where you can."),
  dict(c="Funkhouser, C. J., et al. (2021). Unique longitudinal relationships between symptoms of psychopathology in youth: A cross-lagged panel network analysis in the ABCD study. <i>Journal of Child Psychology and Psychiatry, 62</i>(2), 184–194.", url="https://doi.org/10.1111/jcpp.13256", v=True, note="An example empirical application of CLPN (4,093 adolescents, including a T2→T3 replication); read closely in Lesson 9.1."),
 ]),
 ("Network Psychometrics", [
  dict(c="Borsboom, D., & Cramer, A. O. J. (2013). Network analysis: An integrative approach to the structure of psychopathology. <i>Annual Review of Clinical Psychology, 9</i>, 91–121.", url="https://doi.org/10.1146/annurev-clinpsy-050212-185608", v=True, note="The founding review of the network view; reading for Lesson 0.2."),
  dict(c="Epskamp, S., Borsboom, D., & Fried, E. I. (2018). Estimating psychological networks and their accuracy: A tutorial paper. <i>Behavior Research Methods, 50</i>(1), 195–212.", url="https://doi.org/10.3758/s13428-017-0862-1", v=True, note="The standard tutorial on bootnet and stability checks (CS-coefficient); Modules 6 and 8."),
  dict(c="Epskamp, S., & Fried, E. I. (2018). A tutorial on regularized partial correlation networks. <i>Psychological Methods, 23</i>(4), 617–634.", url="https://doi.org/10.1037/met0000167", v=True, note="Tutorial on regularized partial correlation networks (EBICglasso); Lesson 6.3."),
  dict(c="Foygel, R., & Drton, M. (2010). Extended Bayesian information criteria for Gaussian graphical models. <i>Advances in Neural Information Processing Systems, 23</i>, 604–612.", url="https://proceedings.neurips.cc/paper/2010/hash/072b030ba126b2f4b2374f342be9ed44-Abstract.html", v=True, note="The original paper on EBIC for Gaussian graphical models, where the 4γ|E| log p penalty comes from; Lesson 6.3."),
  dict(c="Epskamp, S., Cramer, A. O. J., Waldorp, L. J., Schmittmann, V. D., & Borsboom, D. (2012). qgraph: Network visualizations of relationships in psychometric data. <i>Journal of Statistical Software, 48</i>(4), 1–18.", url="https://doi.org/10.18637/jss.v048.i04", v=True, note="Paper introducing the qgraph package."),
  dict(c="Robinaugh, D. J., Millner, A. J., & McNally, R. J. (2016). Identifying highly influential nodes in the complicated grief network. <i>Journal of Abnormal Psychology, 125</i>(6), 747–757.", url="https://doi.org/10.1037/abn0000181", v=True, note="Introduced the expected influence (EI) index; Lesson 6.5."),
  dict(c="Jones, P. J., Ma, R., & McNally, R. J. (2021). Bridge centrality: A network approach to understanding comorbidity. <i>Multivariate Behavioral Research, 56</i>(2), 353–367.", url="https://doi.org/10.1080/00273171.2019.1614898", v=True, note="Bridge centrality and the networktools package; Lessons 6.5 and 7.4."),
  dict(c="Fried, E. I., & Cramer, A. O. J. (2017). Moving forward: Challenges and directions for psychopathological network theory and methodology. <i>Perspectives on Psychological Science, 12</i>(6), 999–1020.", url="https://doi.org/10.1177/1745691617705892", v=True, note="Challenges to and criticisms of network methodology; Lesson 9.2."),
  dict(c="Robinaugh, D. J., Hoekstra, R. H. A., Toner, E. R., & Borsboom, D. (2020). The network approach to psychopathology: A review of the literature 2008–2018 and an agenda for future research. <i>Psychological Medicine, 50</i>(3), 353–366.", url="https://doi.org/10.1017/S0033291719003404", v=True, note="A review of ten years of literature; further reading."),
  dict(c="Grygiel, P., Opozda-Suder, S., & Dolata, R. (2026). The longitudinal interplay between loneliness and depressive symptoms during late childhood: Cross-lagged panel network analyses. <i>European Journal of Investigation in Health, Psychology and Education, 16</i>(6), 78.", url="https://doi.org/10.3390/ejihpe16060078", v=True, note="An empirical CLPN study of loneliness and depressive symptoms (open access): the NLSY79 Child and Young Adult sample (NLSY79-CY), N = 4,333 children aged 10–12, two time points. In the Paper Reading Pack."),
  dict(c="Fried, E. I., Papanikolaou, F., & Epskamp, S. (2022). Mental health and social contact during the COVID-19 pandemic: An ecological momentary assessment study. <i>Clinical Psychological Science, 10</i>(2), 340–354.", url="https://doi.org/10.1177/21677026211017839", v=True, note="Social contact and mental health in intensive longitudinal data (open access); in the Paper Reading Pack."),
  dict(c="Burger, J., Isvoranu, A.-M., Lunansky, G., Haslbeck, J. M. B., Epskamp, S., Hoekstra, R. H. A., Fried, E. I., Borsboom, D., & Blanken, T. F. (2023). Reporting standards for psychological network analyses in cross-sectional data. <i>Psychological Methods, 28</i>(4), 806–824.", url="https://doi.org/10.1037/met0000471", v=True, note="Reporting standards for network analysis; Lesson 9.3."),
  dict(c="Isvoranu, A.-M., Epskamp, S., Waldorp, L. J., & Borsboom, D. (Eds.). (2022). <i>Network psychometrics with R: A guide for behavioral and social scientists</i>. Routledge.", url="https://doi.org/10.4324/9781003111238", v=True, note="A full textbook; reference for Modules 6–8 (its companion website has exercises and answers)."),
 ]),
 ("Cross-Lagged Panel Models (CLPM / RI-CLPM)", [
  dict(c="Hamaker, E. L., Kuiper, R. M., & Grasman, R. P. P. P. (2015). A critique of the cross-lagged panel model. <i>Psychological Methods, 20</i>(1), 102–116.", url="https://doi.org/10.1037/a0038889", v=True, note="Introduced the RI-CLPM; required reading for Lesson 5.3."),
  dict(c="Mulder, J. D., & Hamaker, E. L. (2021). Three extensions of the random intercept cross-lagged panel model. <i>Structural Equation Modeling: A Multidisciplinary Journal, 28</i>(4), 638–648.", url="https://doi.org/10.1080/10705511.2020.1784738", v=True, note="Website with lavaan / Mplus example code: jeroendmulder.github.io/RI-CLPM"),
  dict(c="Lucas, R. E. (2023). Why the cross-lagged panel model is almost never the right choice. <i>Advances in Methods and Practices in Psychological Science</i>.", url="https://doi.org/10.1177/25152459231158378", v=True, note="Further critique of the CLPM; Lesson 5.4."),
  dict(c="Rosseel, Y. (2012). lavaan: An R package for structural equation modeling. <i>Journal of Statistical Software, 48</i>(2), 1–36.", url="https://doi.org/10.18637/jss.v048.i02", v=True, note="Paper introducing the lavaan package; Lesson 5.2."),
 ]),
 ("Regularization and R", [
  dict(c="Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. <i>Journal of the Royal Statistical Society: Series B (Methodological), 58</i>(1), 267–288.", url="https://doi.org/10.1111/j.2517-6161.1996.tb02080.x", v=True, note="The original LASSO paper (background only; the math is demanding)."),
  dict(c="Friedman, J., Hastie, T., & Tibshirani, R. (2010). Regularization paths for generalized linear models via coordinate descent. <i>Journal of Statistical Software, 33</i>(1), 1–22.", url="https://doi.org/10.18637/jss.v033.i01", v=True, note="Paper introducing the glmnet package; Lessons 3.5 and 7.2."),
  dict(c="Wickham, H., Çetinkaya-Rundel, M., & Grolemund, G. (2023). <i>R for data science</i> (2nd ed.). O'Reilly. (Free online edition)", url="https://r4ds.hadley.nz/", v=True, note="The main self-study textbook for Module 2."),
 ]),
 ("Foundational Statistics and Missing Data", [
  dict(c="Field, A., Miles, J., & Field, Z. (2012). <i>Discovering statistics using R</i>. SAGE.", url="https://www.sagepub.com/en-us/nam/discovering-statistics-using-r/book236067", v=True, note="An introductory textbook on statistics and R, to go with Modules 1–3. Published by SAGE in 2012; authors Andy Field, Jeremy Miles and Zoë Field. The book has no DOI; the publisher's catalog page is the reference."),
  dict(c="Enders, C. K. (2022). <i>Applied missing data analysis</i> (2nd ed.). The Guilford Press.", url="https://www.guilford.com/books/Applied-Missing-Data-Analysis/Craig-Enders/9781462549863", v=True, note="A missing data textbook; further reading for Lesson 4.3. The current edition is the 2nd (2022, hardcover ISBN 978-1-4625-4986-3, 546 pp.); the 1st edition appeared in 2010."),
 ]),
 ("Measurement Invariance, Sample Size Planning, and Group Comparisons (Optional Advanced)", [
  dict(c="Putnick, D. L., & Bornstein, M. H. (2016). Measurement invariance conventions and reporting: The state of the art and future directions for psychological research. <i>Developmental Review, 41</i>, 71–90.", url="https://doi.org/10.1016/j.dr.2016.06.004", note="A review of measurement invariance: what the configural, metric and scalar levels mean, and which numbers to report. Lesson 7.6."),
  dict(c="Cheung, G. W., & Rensvold, R. B. (2002). Evaluating goodness-of-fit indexes for testing measurement invariance. <i>Structural Equation Modeling, 9</i>(2), 233–255.", url="https://doi.org/10.1207/S15328007SEM0902_5", note="The source of the rule of thumb ΔCFI ≥ −0.01. Lesson 7.6."),
  dict(c="Chen, F. F. (2007). Sensitivity of goodness of fit indexes to lack of measurement invariance. <i>Structural Equation Modeling, 14</i>(3), 464–504.", url="https://doi.org/10.1080/10705510701301834", note="A simulation study comparing fit indices, which proposes looking at ΔCFI together with ΔRMSEA ≤ 0.015. Lesson 7.6."),
  dict(c="Constantin, M. A., Schuurman, N. K., & Vermunt, J. K. (2026). A general Monte Carlo method for sample size analysis in the context of network models. <i>Psychological Methods, 31</i>(3), 385–405.", url="https://doi.org/10.1037/met0000555", note="A general method for sample size planning in network models: assume a true network, then simulate to find the N needed. The simulation in Lesson 7.6 is a simplified version."),
  dict(c="van Borkulo, C. D., van Bork, R., Boschloo, L., Kossakowski, J. J., Tio, P., Schoevers, R. A., Borsboom, D., & Waldorp, L. J. (2023). Comparing network structures on three aspects: A permutation test. <i>Psychological Methods, 28</i>(6), 1273–1285.", url="https://doi.org/10.1037/met0000476", note="The Network Comparison Test (NCT): three tests, M (network structure), S (global strength) and single edges. The hand-written permutation test in Lesson 7.7 follows its approach."),
  dict(c="Ackeret, N., Röthlin, P., Horvath, S., & Allemand, M. (2023). <i>Positive mental health among sports coaches: A six-month longitudinal study</i> [Data set, version 3]. Dryad.", url="https://doi.org/10.5061/dryad.8931zcrws", note="The real data (CC0) used in the Lesson 7.6 exercises, included as data/coaches_mhc_raw.csv; known issues are listed in the data dictionary."),
 ]),
]

# ---- Course Size: Single Source of Truth ----
# All lesson counts and week numbers across pages are generated from here: source files use {{C:size}}, {{C:weeks}}, etc.,
# which fillC() replaces at build time; missing keys raise KeyError.
# Optional advanced lessons have opt=True in their lesson dict in data*.py: they are excluded from the core count, standard pacing sessions, and hours.
# Hand-written documents (README.md, src/README.md, and the local CLAUDE.md if present) cannot use macros; build.py checks that they mention the current COURSE_SIZE.
_LS = [l for _m in MODULES for l in _m["lessons"]]
N_LESSONS = len(_LS)
N_OPT = sum(1 for l in _LS if l.get("opt"))
N_CORE = N_LESSONS - N_OPT
N_WEEKS = len(PACING)
COURSE_SIZE = f"{N_CORE} core lessons + {N_OPT} optional lessons" if N_OPT else f"{N_CORE} lessons"
OPT_IDS = [l["id"] for l in _LS if l.get("opt")]
COUNTS = {"optlist": ", ".join(OPT_IDS) or "(none)", "size": COURSE_SIZE, "core": str(N_CORE), "opt": str(N_OPT), "all": str(N_LESSONS),
          "weeks": str(N_WEEKS), "mods": str(len(MODULES))}
def fillC(s):
    import re as _re
    def _rep(m):
        if m.group(1) not in COUNTS: raise KeyError("Unknown course size key: " + m.group(1))
        return COUNTS[m.group(1)]
    return _re.sub(r"\{\{C:([a-z]+)\}\}", _rep, s)
