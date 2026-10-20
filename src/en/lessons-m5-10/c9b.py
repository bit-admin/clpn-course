# -*- coding: utf-8 -*-
REPORT_ITEMS = [
    "#1. Data and sample",
    "Source of the sample, recruitment, inclusion/exclusion criteria",
    "Sample size, time of measurement and interval for each wave",
    "Nodes: full wording of each item, the scale it comes from and how it is scored (reverse-scored?)",
    "Descriptive statistics: mean, SD and skewness of each item at each wave (explain any severe skew)",
    "#2. Missing data and attrition",
    "Missingness and attrition at each wave",
    "Attrition analysis: do stayers and dropouts differ at baseline?",
    "Method for handling missing data (listwise deletion / multiple imputation / other) and why",
    "#3. Estimation",
    "Estimation framework: nodewise LASSO regression of each T+1 item on all T items; state whether it is the simplified \"LASSO-only\" version (e.g., Funkhouser et al., 2021) or the full procedure of Wysocki et al. (2025) (LASSO edge selection + unpenalized re-estimation in lavaan)",
    "Whether items were z-standardized before estimation",
    "Software and function: glmnet::cv.glmnet, alpha = 1",
    "λ selection rule (lambda.min / lambda.1se / EBIC and γ) and number of cross-validation folds",
    "Random seed (set.seed)",
    "Covariates: which ones, and whether they are penalized (penalty.factor)",
    "#4. Visualization and centrality",
    "Network plot: whether autoregressive edges are shown, threshold, maximum, layout algorithm, meaning of colors",
    "Table of autoregressive edges and table of cross-lagged edges (all or the strongest)",
    "Centrality indices and how they were computed: out-EI / in-EI without autoregressive edges; community definition for bridge indices",
    "#5. Accuracy and stability",
    "Nonparametric bootstrap: number of replicates, interval type (percentile), and the limits of regularized intervals",
    "Edge-weight difference test (if used)",
    "Case-dropping bootstrap: number of replicates, CS-coefficient (cor = 0.7) and interpretation thresholds (0.25 / 0.5)",
    "Interpret rankings only for centrality indices whose CS meets the threshold",
    "#6. Sensitivity and replication",
    "Alternative analysis with another λ rule",
    "Sensitivity analyses for covariates / removing redundant items / seed, etc.",
    "Replication across waves (T2→T3) or in an independent sample (if available)",
    "#7. Open science",
    "Versions of R and all packages (sessionInfo())",
    "Links to code and (shareable) data (e.g., OSF)",
    "Preregistration or analysis plan (if any), with deviations from the plan explained",
    "#8. Interpretation and limitations",
    "Avoid causal wording; state that edges are predictive relationships over time",
    "Discuss the mixing of between-person and within-person effects",
    "Discuss limitations of measurement (single-item reliability, overlapping content), sample and interval"
]

METH_FIELDS = [
    ["N", "Sample size N", "e.g., 800"],
    ["waves", "Waves and interval", "e.g., three waves, 6 months apart"],
    ["nodes", "Description of nodes", "e.g., 4 UCLA loneliness items and 5 PHQ depression items"],
    ["miss", "Missing data handling", "e.g., no missing data in this sample / multiple imputation with 20 imputations"],
    ["rule", "λ rule", "e.g., lambda.min from 10-fold cross-validation"],
    ["seed", "Random seed", "e.g., 2026"],
    ["cov", "Covariates", "e.g., gender and age (unpenalized) / none"],
    ["nboot", "Number of bootstrap replicates", "e.g., 1000"],
    ["sens", "Sensitivity analyses", "e.g., lambda.1se; T2→T3 replication"],
    ["soft", "Software versions", "e.g., R 4.4.1, glmnet 4.1-8, bootnet 1.6"]
]

METH_TEXT = """Data analysis. We used a cross-lagged panel network (CLPN; Wysocki et al., 2025) to analyze the longitudinal relations among {{nodes}} across {{waves}} (N = {{N}}). Estimation followed the "LASSO-only" approach common in applied research (e.g., Funkhouser et al., 2021): the regularized regression coefficients were used directly as edge weights, without the unpenalized SEM re-estimation and pruning recommended by Wysocki et al. (2025). Missing data: {{miss}}. All items were z-standardized before estimation. Each T2 item was regressed on all T1 items (including its own T1 score) with LASSO (glmnet, alpha = 1); λ was chosen by {{rule}}, with random seed {{seed}}; covariates: {{cov}}. The regression coefficients form a directed weight matrix whose diagonal holds the autoregressive edges and whose off-diagonal entries are the cross-lagged edges. We computed each node's out-expected influence and in-expected influence (excluding autoregressive edges), as well as bridge out-/in-expected influence with loneliness and depression as communities. The accuracy of edge weights was assessed with {{nboot}} nonparametric bootstrap replicates; the stability of centrality was assessed with {{nboot}} case-dropping bootstrap replicates and the correlation stability coefficient (CS; Epskamp et al., 2018), and rankings were interpreted only for indices with CS ≥ 0.25. Sensitivity analyses included: {{sens}}. Analyses were run in {{soft}}; the code is in the supplementary materials."""

L["9.3"] = dict(
lead=r"""<p>However good your analysis is, if others do not know exactly what you did, they cannot check, reproduce or compare it. This lesson turns all the analysis decisions of M7–M8 into a reporting checklist and gives you a template for the Methods section that you can adapt directly.</p>""",
intuition=r"""
<h3>Why do you need """ + T("reporting standards") + r"""?</h3>
<p>Imagine reading: "We estimated a cross-lagged network with LASSO." You do not know how λ was chosen, whether the items were standardized, what the seed was, whether there were covariates, how missing data were handled, or which software versions were used. If any one of these differs, the network may differ (Lesson 9.2: just changing the seed makes about 15% of edges "sometimes there, sometimes not"). The goal of reporting standards is that readers can learn every decision that affects the results without having to ask the authors.</p>
<h3>The reporting standards of Burger et al. (2023)</h3>
<p>Burger, Isvoranu, Lunansky and colleagues proposed reporting standards for cross-sectional psychological network analysis (published in <i>Psychological Methods</i>), covering every stage from the research question and data to estimation, stability and interpretation. There is no official standard for CLPN yet, so this lesson takes the general approach of these standards as a framework, carries it over to the CLPN setting, and adds the elements specific to longitudinal data and nodewise regression: waves and interval, attrition, λ rule, autoregressive edges, out/in-EI and replication. When you write a paper, read the original as well and cite it where needed.</p>
<h3>Interactive checklist: CLPN reporting checklist</h3>
<p>The list below is the course's summary of the elements that the methods and results of a CLPN must report. Your ticks are saved automatically in the browser; click "Export as text (copy)" to copy it into your notes, or paste it after your methods outline and keep them together.</p>
""" + WJ("checklist", "CLPN reporting checklist (saved automatically)", "report93", REPORT_ITEMS) + r"""
<h3>What is missing from "we estimated it with LASSO"?</h3>
<p>At least the following: the estimation framework (nodewise regression, each T2 node on all T1 nodes), whether items were standardized, the λ rule and number of folds, the random seed, covariates and their penalty, software and versions. Only when all of these are written down can readers understand why your network looks the way it does.</p>
<h3>""" + T("Open science") + r""": sharing code and data</h3>
<ul><li><b>Code:</b> upload your R scripts (or Quarto project) to OSF (Open Science Framework) or GitHub and give the link in the paper. The course's script layout (<code>R/_setup.R</code> + one script per lesson + <code>R/output/</code>) is a good template.</li>
<li><b>Data:</b> data about service users often cannot be made public. What you can share: the correlation matrix, simulated "synthetic data", or de-identified data within what the ethics approval allows.</li>
<li><b>""" + T("Software versions", "sessionInfo()") + r""":</b> run <code>sessionInfo()</code> at the end of the script to record the versions of R and all packages (R/L9-3.R does this for you).</li></ul>
<h3>""" + T("Preregistration") + r"""</h3>
<p>Preregistration means registering your research question, hypotheses and analysis plan publicly (e.g., on OSF) before you see the data (or the results). The registration is time-stamped and cannot be changed afterwards. It is the strongest tool for limiting researcher degrees of freedom. Even if you do not preregister formally, write a one-page analysis plan before the analysis (Lesson 10.1), and in the paper explain any deviations from the plan and why.</p>
<h3>Special points for social work research</h3>
<p>Social work samples often come from a particular agency or community (for example the residents of one neighborhood, or the clients of one agency). When reporting, make the limits of the sample's representativeness clear: whom the conclusions can be generalized to and whom not. If the data come from service records or an intervention program, also state whether the measurements were taken by the service providers themselves (possible social desirability bias), and describe the ethics approval and informed consent. These are not "network methods" topics, but reviewers and practitioners will both care about them.</p>
<h3>Methods section template (fill in the blanks)</h3>
<p>Enter your project's information and a Methods paragraph (the data analysis subsection) that you can adapt is generated below. Be sure to rewrite it in your own words and check that every item matches your code.</p>
""" + WJ("tpl", "CLPN Methods (data analysis) template", "meth93", {"fields": METH_FIELDS, "text": METH_TEXT}) + r"""
<h3>Common mistakes</h3>
<ul><li><b>"The results were stable" without numbers:</b> give the actual CS-coefficient and say which index it is (out-EI or in-EI). In the course data, the CS of in-EI is between 0.44 and 0.52 (depending on the run; {{V:cs8_in}} in this run of Lesson 8.3) and out-EI's is only about {{V:cs8_out}}, so simply saying "stable" is wrong.</li>
<li><b>Reporting only the significant parts:</b> unstable results must be reported too; readers need to know which conclusions are not stable.</li>
<li><b>Methods and code disagree:</b> the paper says lambda.1se, but the code uses the default lambda.min. Check item by item before you submit.</li></ul>
""",
math=r"""
<p>The "essential math" in this lesson is which numbers must appear in a report and how to check them against each other.</p>
""" + TABLE(["Number", "Symbol", "How to check it"], [
["Sample size (per wave / analyzed)", r"\(N_1, N_2, N_3,\ N_{\text{analysis}}\)", r"With listwise deletion \(N_{\text{analysis}}\le \min(N_t)\); otherwise describe the imputation"],
["Number of nodes", r"\(p\)", r"At most \(p(p-1)\) cross-lagged edges"],
["Number of nonzero cross-lagged edges", r"\(E\)", r"Density \(=E/[p(p-1)]\)"],
["Range of autoregression", r"\(\min_k\beta_{kk},\ \max_k\beta_{kk}\)", "Usually all positive (negative values need explaining)"],
["Number of bootstrap replicates", r"\(B\)", "Usually 1,000; fewer than 500 needs explaining"],
["CS-coefficients", r"\(\mathrm{CS}_{\text{out}},\ \mathrm{CS}_{\text{in}}\)", "Compare with 0.25 / 0.5"],
["Agreement in sensitivity analysis", r"\(r\)", "Correlation of edge weights between the main and the alternative analysis"]]) + r"""
<p>Symbols: \(N_t\) is the sample size at wave \(t\); \(p\) is the number of nodes (items) per wave; \(\beta_{kk}\) is the autoregressive coefficient of node \(k\) (the diagonal of the matrix); \(E\) is the number of nonzero cross-lagged edges; \(B\) is the number of bootstrap resamples.</p>
<h4>Checking the totals of out-EI and in-EI</h4>
""" + MATH(r"\sum_k \text{out-EI}_k=\sum_j \text{in-EI}_j=\sum_{k\neq j}\hat\beta_{kj}") + r"""
<p>Each cross-lagged edge \(\hat\beta_{kj}\) is counted exactly once in an out-EI (its start, \(k\)) and once in an in-EI (its end, \(j\)), so the two columns must have the same total. If the totals of the two columns in a table are far apart, the code or the table is wrong (Lesson 7.4).</p>
<h4>Reporting precision</h4>
<p>Edge weights and centrality are usually given to 2–3 decimals, CS-coefficients to 2. In APA style (7th edition), statistics whose absolute value cannot exceed 1 (r, p, proportions, CS-coefficients) are written without a 0 before the decimal point, e.g., r = .52, p = .019, CS = .52; statistics that can exceed 1 (M, SD, unstandardized coefficients B, t, χ²) keep the 0. Standardized coefficients β usually follow the same rule and drop the 0 (β = .14); some journals (Chinese journals often) keep it (β = 0.14). Choose one according to the journal you submit to and use it consistently.</p>
""",
code=CODE(r"""
source("R/_setup.R")
log_open("L9-3_reporting_info.txt")
pk <- c("glmnet", "qgraph", "bootnet", "networktools", "lavaan", "psych", "tidyverse")
cat("== Software ==\n", R.version.string, "\n")
for (p in pk) cat(sprintf("  %s %s\n", p, utils::packageDescription(p)$Version))   # keeps the package's own format, e.g., 4.1-8
# ... (the script also prints a tick-box reporting checklist)
suppressPackageStartupMessages(for (p in pk) library(p, character.only = TRUE))   # load first, so sessionInfo() lists them
si <- capture.output(print(sessionInfo()))
writeLines(si, out("sessionInfo_full.txt"))      # full version for the archive, attach to the supplement
k <- grep("^loaded via a namespace", si)[1]       # the log stops at the directly loaded packages
cat(head(si, k - 1), sep = "\n")
log_close()
""", "Core of R/L9-3.R: generates an \"analysis information sheet\" automatically") + r"""
<p>The generated <code>R/output/L9-3_reporting_info.txt</code> can go straight into the supplementary materials (see the actual output below). <code>sessionInfo()</code> lists every loaded package, and most of them are indirectly loaded dependencies ("loaded via a namespace"). So the log stops at the directly loaded packages (R version, operating system and the analysis packages you loaded: everything the Methods section needs is there). Load the packages you use with <code>library()</code> before calling <code>sessionInfo()</code>, or they will not appear under "other attached packages". The output published in the course repository omits this computer's numerical library paths, locale and time zone; for your own study you need not omit them, but think about whether you want them public before you publish. The full content is saved separately as <code>R/output/sessionInfo_full.txt</code>. Version numbers are taken with <code>packageDescription(p)$Version</code>, which keeps the package author's format (e.g., glmnet 4.1-8); <code>as.character(packageVersion(p))</code> would write 4.1.8, which disagrees with CRAN and <code>sessionInfo()</code>. Add these lines to the end of the main script of your capstone project as well.</p>""",
quiz=[
("Why report R package versions and the random seed?",
 ["It is a journal formatting requirement",
  "Different versions and seeds can give different results (especially weak edges and the choice of λ); only when they are reported can others reproduce the results exactly",
  "To look professional",
  "There is no need: the same data always give the same results"], 1,
 ["It is not just formatting: without them, nobody can reproduce your results.",
  "Correct.",
  "The point is not to look professional but to let others reproduce the work.",
  "Plausible but wrong: Lesson 9.2 showed that with the same data, just changing the seed makes about 15% of edges come and go."]),
("If a CLPN Methods section says only \"estimated with LASSO\", what key information is missing?",
 ["Only the software name",
  "The estimation framework (nodewise regression), standardization, λ rule and folds, seed, covariates and penalty, software versions, etc.",
  "Only the sample size",
  "Nothing: LASSO is a standard procedure"], 1,
 ["The software name is only one item; without the λ rule and seed, the analysis still cannot be reproduced.",
  "Correct.",
  "The sample size is usually already given in the sample section; what is missing are the estimation settings.",
  "LASSO has many settings to choose (λ rule, folds, standardization, whether covariates are penalized), and each one changes the network."]),
("Which of these is not a common CLPN sensitivity analysis?",
 ["Switching to lambda.1se",
  "Adding covariates",
  "T2→T3 replication",
  "Raising the bootstrap replicates from 1,000 to 5,000 to steady the interval endpoints"], 3,
 ["It is one: try another reasonable λ rule and see whether the conclusions hold.",
  "It is one: it changes the choice of which variables to control for.",
  "It is one (replication): take another interval and see whether the network is similar.",
  "Correct: more replicates only reduce Monte Carlo error and change no analysis decision, so it is not a sensitivity analysis."]),
("What is the main purpose of preregistration?",
 ["To make the paper easier to publish",
  "To fix the analysis plan before seeing the results, limiting researcher degrees of freedom",
  "To replace ethics approval",
  "To increase statistical power"], 1,
 ["Some journals welcome preregistration, but that is not its purpose.",
  "Correct.",
  "Preregistration and ethics approval are two separate things; you need both.",
  "Power depends on sample size and effect size; preregistration does not change it."]),
("Data about service users cannot be made public. What can you do?",
 ["Share nothing",
  "Share the code, the correlation matrix or synthetic data, and de-identified data within what ethics approval allows",
  "Delete names and ID numbers and publish the raw data",
  "Just write \"data available from the authors on request\" in the paper"], 1,
 ["Materials that contain no personal information, such as code and the correlation matrix, can still be shared.",
  "Correct.",
  "Removing direct identifiers is often not enough: age, gender, neighborhood and so on can identify a person in combination; whether you can publish depends on the scope of the ethics approval and informed consent.",
  "You can write this, but it does not replace what you can share directly (code, correlation matrix, synthetic data)."]),
],
ex=[
("Methods outline and checklist", "Writing", r"""<p>Write a "Methods outline" for your capstone project (generate it with the template above, then rewrite it), tick through the checklist on this page item by item, and keep the exported text together with the outline. When you write the results in Lesson 10.3, check against this list again. Add two sentences at the end of the outline: where you plan to put the code (OSF or GitHub), and whether you will preregister (if not, use the analysis plan from Lesson 10.1 instead and state its date).</p>""",
 r"""<p>Checkpoints: (1) every blank is filled in, with no "[…]" placeholders left; (2) the template sentences have been rewritten in your own words; (3) everything matches the settings in the R script (λ rule, seed, number of bootstrap replicates); (4) for each unticked item on the checklist, either add it or explain in the outline why it does not apply; (5) where the code will be shared and the arrangement for preregistration (or the analysis plan) are stated.</p>"""),
("Find what is missing from a Methods paragraph", "Understanding", r"""<p>"We estimated a CLPN with the R package glmnet and checked its stability with bootnet; the results were stable." List at least 6 pieces of information that need to be added.</p>""",
 r"""<p>(1) Nodes and time interval; (2) the nodewise regression framework; (3) whether items were standardized; (4) λ rule and number of folds; (5) seed; (6) covariates; (7) bootstrap type and number of replicates; (8) the actual CS values and the standard used; (9) whether "stable" refers to edges or centrality; (10) software versions; (11) missing-data handling.</p>"""),
("Running L9-3.R", "Hands-on", r"""<p>Run R/L9-3.R, find your computer's R version and the versions of glmnet and bootnet in the output, and write them as a sentence you could put in a Methods section.</p>""",
 r"""<p>Example: "All analyses were run in R (version 4.x.x) with glmnet (version …), qgraph (version …) and bootnet (version …)." Use the version numbers in your own <code>R/output/L9-3_reporting_info.txt</code>.</p>"""),
],
summary=["Goal of reporting standards: readers learn every decision that affects the results without having to ask the authors.", "Use the cross-sectional standards of Burger et al. (2023) as a framework, carry them over and add the elements specific to CLPN.", "Must report: data and interval, missing data/attrition, standardization, nodewise LASSO, λ rule, seed, covariates, centrality definitions, bootstrap and CS, sensitivity analyses, software versions.", "Open science: share code (OSF/GitHub), sessionInfo(), preregistration or analysis plan.", "Checks: total out-EI = total in-EI; number of edges ≤ p(p−1)."],
refs=["Burger, J., Isvoranu", "Epskamp, S., Borsboom, D., & Fried", "Wysocki, A., McCarthy"],
)
