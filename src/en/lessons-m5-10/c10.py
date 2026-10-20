# -*- coding: utf-8 -*-
PLAN_FIELDS = [["rq", "Research question (no \"causes\")", "e.g., To what extent do T1 loneliness items uniquely predict T2 depression items, and vice versa?"],
["data", "Data source and sample", "e.g., course simulated data clpn_sim_wide.csv, N = 800, three waves"],
["nodes", "Nodes", "e.g., lone1–lone4, dep1–dep5 (9 nodes)"],
["span", "Intervals", "e.g., T1→T2 main analysis, T2→T3 replication"],
["est", "Estimation method", "e.g., nodewise LASSO (glmnet), 10-fold CV, items z-standardized"],
["rule", "λ rule", "e.g., lambda.min"], ["seed", "Seed", "e.g., set.seed(2026)"],
["cent", "Centrality", "e.g., out-EI, in-EI, bridge out/in-EI (excluding autoregression)"],
["stab", "Stability", "e.g., nonparametric bootstrap 1,000 replicates; case-dropping 1,000 replicates; rankings interpreted only if CS ≥ 0.25"],
["sens", "Other sensitivity analyses", "e.g., lambda.1se; gender and age as unpenalized covariates; T2→T3 replication"],
["full", "Required sensitivity analysis: full procedure", "e.g., the full procedure of Wysocki et al. (2025) (R/L10-2b.R): LASSO edge selection on both intervals, conservative rule → unpenalized re-estimation in lavaan (same-wave residual covariances, FIML) → equality test across time (nested χ² + AIC/BIC) → pruning at p < .01 → in/out-prediction"],
["agree", "When the two analyses disagree", "e.g., edges kept in both analyses are the main findings; edges found only in the main analysis are described as \"sensitive to the estimation method\" and interpreted only as exploratory; construct-level conclusions are reported only if their direction agrees in both analyses"],
["miss", "Missing data handling", "e.g., no missing data in these data; if there were, report an attrition analysis and use multiple imputation"],
["hyp", "Expectations (optional)", "e.g., the sum of edges in the loneliness → depression direction is expected to exceed the reverse direction"]]
PLAN_TEXT = """# Analysis plan (simple preregistration)
Date written: [today's date] (before seeing any CLPN results)
1. Research question: {{rq}}
2. Data: {{data}}
3. Nodes: {{nodes}}; intervals: {{span}}
4. Estimation: {{est}}; λ selection rule: {{rule}}; {{seed}}
5. Centrality: {{cent}}
6. Accuracy and stability: {{stab}}
7. Sensitivity analyses: {{sens}}
8. Required sensitivity analysis: {{full}}
9. When the two analyses disagree: {{agree}}
10. Missing data and attrition: {{miss}}
11. Expectations: {{hyp}}
12. Deviations from the plan: any deviation will be reported in the write-up, with what changed and why."""
PREP_ITEMS = ["#Data cleaning",
"Read in the data and check that the numbers of rows and columns are as expected",
"Check value by value that every item takes only allowed values (loneliness 1, 2, 3, 4; depression 0, 1, 2, 3): catch out-of-range values and non-integers such as 2.5; looking only at the minimum and maximum is not enough",
"Check for duplicate IDs",
"Count missing values for each variable at each wave",
"Reverse scoring (if needed): new variable = (maximum + minimum) − original value",
"#Codebook",
"For each variable: name, item wording, scale, values and their meaning, wave (R/output/L10-1_codebook.csv; item wording taken from data/data_dictionary.csv)",
"Mean and SD of each item at each wave (same file; a statistics-only version is R/output/L10-1_codebook_stats.csv)",
"Flag item pairs with heavily overlapping content (goldbricker, Lesson 9.2)",
"#Attrition",
"Compute the retention rate at each wave",
"Compare baseline scores of stayers and dropouts",
"Decide how to handle missing data and write it into the analysis plan",
"#Analysis plan",
"Write and save it (with the date) before running any CLPN",
"Write down all settings of the required full-procedure sensitivity analysis (R/L10-2b.R), and how you will interpret disagreements between the two analyses",
"Once finalized, do not change it in response to results; if a change is truly needed, list in the report what was changed and why"]
L["10.1"] = dict(
lead=r"""<p>From this lesson on, you carry out a complete small CLPN study on your own. The first step is not running a model but working out what to ask, what the data look like and how you plan to analyze them, and writing this down before you see any results.</p>""",
intuition=r"""
<h3>The three stages of the capstone project</h3>
""" + TABLE(["Stage", "Lesson", "Main output", "Script"], [
["① Design and preparation", "10.1", "Research question, codebook, cleaning script, one-page analysis plan", "R/L10-1.R"],
["② Full analysis", "10.2", "An analysis project that runs in one step + 5 kinds of figures and tables; the required full-procedure sensitivity analysis and an edge-by-edge comparison table", "R/L10-2.R, R/L10-2b.R"],
["③ Writing and presenting", "10.3", "800–1,200 words of methods + results, limitations, a 10-minute talk", "R/L10-3.R"]]) + r"""
<p>The default data are the course's simulated data <code>data/clpn_sim_wide.csv</code>: three waves, each with 4 loneliness items (scored 1–4) and 5 depression items (scored 0–3), N = 800, plus covariates such as gender and age. Their advantage is that the true structure is known (population target <code>data/true_B_population.csv</code> and within-person truth <code>data/true_B_within.csv</code>, Lesson 7.2), so you can check how accurately the method estimates. If you can, you may instead use public longitudinal data; before using them, read their license, citation requirements and ethical restrictions carefully.</p>
<h3>Step 1: ask a good """ + T("research question") + r"""</h3>
<p>A good CLPN research question has three features:</p>
<ol><li><b>Not causal:</b> a CLPN estimates "predictive relationships over time, controlling for all T1 items", not causal effects. So do not write "loneliness causes depression"; write "to what extent do T1 loneliness items uniquely predict T2 depression items".</li>
<li><b>At the item level:</b> the value of network analysis is that you can see <i>which</i> item matters. A good question gets down to specific symptoms, for example "is 'No one understands me' the main bridge from loneliness to depression?"</li>
<li><b>Two-directional:</b> a cross-lagged design can test both directions as a matter of course, so the research question should include "and vice versa".</li></ol>
""" + TABLE(["Wording", "Assessment"], [
["Does loneliness cause depression?", "Causal wording; variable level"],
["Are loneliness and depression related?", "Too broad; cross-sectional data could answer it"],
["To what extent do T1 loneliness items uniquely predict T2 depression items, and vice versa? Which items are the main bridges?", "Not causal, item level, two-directional"]]) + r"""
<h3>Step 2: """ + T("data cleaning") + r""" and the """ + T("codebook") + r"""</h3>
<p>Data cleaning is not optional. A single out-of-range value (say, missing coded as 99) is enough to create a strong spurious edge. The codebook is a "manual" for the variables: which item each variable is, how it is scored, at which wave it was measured. It lets readers, reviewers and you yourself a few months from now understand the data. The checklist below follows the steps of <code>R/L10-1.R</code>; tick items off as you go.</p>
""" + WJ("checklist", "Data preparation checklist (saved automatically)", "prep101", PREP_ITEMS) + r"""
<h3>Step 3: """ + T("attrition analysis") + r"""</h3>
<p>Almost every longitudinal study loses people along the way. The key question is: are the people who leave like the people who stay? In the attrition example data in L10-1.R, the retention rate is 0.80, but the mean T1 depression total of the dropouts (8.78) is far higher than that of the stayers (2.60). If you analyze only those who stayed, the sample is systematically "healthier": the T2 means are underestimated, item variances shrink (range restriction, Lesson 1.4), and the standardized edge weights, the edges LASSO selects and the stability are all affected. In this example, dropping out depends only on T1 depression, and T1 depression is itself among the predictors of every regression, so the unstandardized regression slopes are in theory still unbiased; if dropping out depended on the unobserved T2 state (MNAR), the bias would be larger (Lesson 4.3). Report the difference, and consider methods such as multiple imputation (Module 4).</p>
<h3>Step 4: a one-page """ + T("analysis plan") + r"""</h3>
<p>Why write it before seeing results? Because a CLPN involves many "reasonable choices": the λ rule, the seed, whether to add covariates, whether to drop redundant items … If you choose after seeing the results, it is hard not to be swayed by which result looks better ("researcher degrees of freedom", Lesson 9.2). Writing the choices down in advance, with a date, is a simple form of """ + T("preregistration") + r""".</p>
<h3>Step 5: make the full procedure a required sensitivity analysis</h3>
<p>The main analysis in this course is the "LASSO-only" CLPN most common in the applied literature: the coefficients selected and already shrunk by LASSO are used directly as edge weights (Lessons 7.2–7.4). The methods paper that proposed the CLPN (Wysocki et al., 2025) does not recommend stopping there. Its recommended full procedure (""" + LINK("7.5") + r""") uses LASSO only to decide which paths are fixed to 0, then re-estimates the remaining paths without a penalty in a structural equation model, tests whether the paths are equal across intervals, and finally prunes at p &lt; .01. LASSO alone has three problems:</p>
<ol><li><b>Many false positives.</b> The λ chosen by cross-validation is on the small side and keeps quite a few edges that are close to 0 in the population, and this false-positive rate does not fall as the sample grows. In the course data, lambda.min keeps {{V:fp10_fp_lasso}} cross-lagged edges at T1→T2 with |B| &lt; 0.05 in the population (the same definition as the recovery table in Lesson 7.2).</li>
<li><b>Coefficients are pulled toward 0.</b> The LASSO penalty also shrinks the coefficients it keeps, so LASSO coefficients cannot be taken directly as effect sizes.</li>
<li><b>No standard errors, tests or fit indices.</b> LASSO gives only a set of point estimates. Only after re-estimation in SEM do you get a standard error and p-value for each path, overall fit indices (χ², CFI, TLI, RMSEA, SRMR), and a test of whether the paths are equal in the two intervals.</li></ol>
<p>Then why not make the full procedure the main analysis? First, most of the published studies you will read and compare with use LASSO only; a main analysis that matches them can be compared with them directly. Second, the edge-weight bootstrap and centrality stability (CS-coefficient) of M8 are built on the LASSO estimate, and the full procedure has no ready-made counterpart. Third, the two answer slightly different questions: LASSO selects "edges that help prediction" (judged by cross-validation error), while the full procedure keeps "paths whose unpenalized estimate differs significantly from 0 at α = .01". Their biases also run in opposite directions: LASSO tends to report too many edges (high sensitivity, many false positives); the full procedure tends to report too few (few false positives, but it misses quite a few weak edges). Only with both side by side can readers see which conclusions do not depend on the estimation method.</p>
<p>So the capstone project in this course requires: keep LASSO for the main analysis; run the full procedure as a required sensitivity analysis (<code>R/L10-2b.R</code>), write it into the analysis plan in advance, and report it next to the main analysis in the results (Lesson 10.3). "Required" means you report it whether or not the results agree; you cannot mention it only when the two agree.</p>
<h4>Full-procedure settings to fix in the plan</h4>
""" + TABLE(["Setting", "This course's choice", "Why fix it in advance"], [
["λ rule and seed for edge selection", "Same as the main analysis (lambda.min, set.seed(2026))", "A different rule changes which paths enter the SEM, which amounts to a different model"],
["Rule for combining the intervals", "Conservative rule: a path is fixed to 0 only if it is 0 in both T1→T2 and T2→T3", "The alternative (fix it if it is 0 in either interval) is sparser; the two give different results"],
["Same-wave part", "All residuals within a wave correlated pairwise", "Absorbs same-period effects and common causes within an interval; leaving them out assumes the residuals of items in the same wave are uncorrelated, which is almost certainly false, so the model fits very badly and the standard errors and tests are wrong"],
["Missing data", 'FIML (lavaan\'s missing = "ml")', "LASSO cannot handle missing data (you must first drop incomplete cases or impute, Lesson 4.3), FIML can; the two analyses may use different cases, so state this in the Methods"],
["Choice of final model", "Use the constrained model if the nested χ² test for equality constraints gives p ≥ .05 and neither AIC nor BIC argues against it; otherwise use the unconstrained model", "Picking the model after seeing the path coefficients is a researcher degree of freedom"],
["Pruning criterion", "p &lt; .01 (the criterion in the original paper's example)", "With .05 a few more edges are kept; a different criterion gives a different number of edges"],
["Node-level summary", "In-/out-prediction (proportion of variance explained)", "Its unit differs from expected influence, so the two cannot be ranked together"]]) + r"""
<h4>Decide in advance what to do when the two analyses disagree</h4>
<p>The two analyses will almost certainly disagree on some edges. Deciding which to believe after seeing the results brings back researcher degrees of freedom. So the plan needs an interpretation rule. This course's rule:</p>
<ul><li>Edges kept by both analyses with the same sign are reported as main findings;</li>
<li>Edges that are nonzero only in the main analysis and not kept by the full procedure are described as "sensitive to the estimation method", interpreted only as exploratory, and not used as a basis for practice recommendations;</li>
<li>Edges kept by the full procedure but 0 in the main analysis are likewise reported only as exploratory. This can happen because the paths entering the SEM are the union of the two LASSO results, and the equality model also pools the information of the two intervals;</li>
<li>Construct-level conclusions (e.g., "the sum of edge weights in the loneliness → depression direction is larger than in the reverse direction") go into the abstract and practical implications only if their direction agrees in both analyses.</li></ul>
<p>The rule can be set differently, for example by relaxing the pruning criterion to .05. What matters is that it is fixed before you see the results and followed in the report; if a change is truly needed, list what was changed and why.</p>
<p>Put all of this into the template below to generate your analysis plan.</p>
""" + WJ("tpl", "One-page analysis plan generator", "plan101", {"fields": PLAN_FIELDS, "text": PLAN_TEXT}) + r"""
""" + TIP("A social work perspective", "<p>The best research questions come from puzzles in practice. Say you notice while meeting residents at a community service center that some say \"no one understands me\" and others say \"I have no one to keep me company\". Which deserves attention first? This can be turned into a predictive question: \"Which loneliness item most strongly and uniquely predicts later depression (highest bridge out-expected influence)?\" On its own it cannot answer \"which one should be the first target of intervention\" (centrality is not an intervention target, Lesson 9.2), but it can generate hypotheses for later intervention research. You can also open your talk with this practice question.</p>") + r"""
<h3>Common mistakes</h3>
<ul><li><b>Running first, writing the plan afterwards:</b> such a plan is no plan.</li>
<li><b>Too many nodes:</b> the more nodes, the larger the sample needed, and it grows fast (the number of coefficients is p²). There is no accepted standard for "so many people per node"; the course data have N = 800 and use only 9 nodes. If you want more nodes, first check N/p with formula 3 in the Essential Math section, then use the simulation of Lesson 7.6 to check whether the key edges can be recovered.</li>
<li><b>Ignoring overlapping content:</b> "feeling low" and "feeling down" are practically the same item; merge them or keep one (Lesson 9.2). This is also step 1 of the full procedure.</li>
<li><b>Treating the full procedure as a "fallback when the results look bad":</b> if you look at the LASSO results before deciding whether to run the full procedure, or pick the nicer of the two results as the main analysis, the sensitivity analysis loses its meaning. Fix in the plan which one is the main analysis and which is the sensitivity analysis.</li></ul>
""",
math=r"""
<p>This lesson has only a few small formulas, all about data preparation and checking the design.</p>
<h4>1. Reverse scoring</h4>
""" + MATH(r"x^{\text{rev}} = (x_{\max}+x_{\min}) - x") + SYM([
["\\(x\\)", "Original score"], ["\\(x_{\\max}, x_{\\min}\\)", "Highest and lowest possible scores of the scale (e.g., 4 and 1 for a 1–4 scale)"], ["\\(x^{\\text{rev}}\\)", "Reverse-scored value: 1↔4, 2↔3"]]) + r"""
<p>Example: on a 1–4 scale, an original 1 → (4+1)−1 = 4. The course data have no reverse-scored items, but real scales (such as some versions of the UCLA Loneliness Scale) often do.</p>
<h4>2. Retention rate</h4>
""" + MATH(r"\text{retention rate} = \frac{N_{t}}{N_{1}}") + SYM([
["\\(N_1\\)", "Sample size at wave 1"], ["\\(N_t\\)", "Number of people still with data at wave \\(t\\)"]]) + r"""
<p>Example: 640 / 800 = 0.80. Then compare the T1 means of stayers and dropouts (or run a t-test) to show whether attrition is related to the study variables.</p>
<h4>3. A rough check of parameters against sample size</h4>
<p>Each T2 node's LASSO regression has \(p\) predictors (\(p\) is the number of nodes). The whole network has at most \(p^2\) coefficients, \(p\) of them autoregressive and \(p(p-1)\) cross-lagged. In this course \(p = 9\), 81 coefficients in all; N = 800, N/p ≈ 89, so in each regression the sample is nearly 90 times the number of predictors. N/p has no accepted hard minimum; it is only a rough quick check (Lesson 9.1). If you have only N = 150 but want 20 nodes (N/p = 7.5), each regression has very little information, and the network will be very sparse and very unstable. When planning your own study, how large a sample you need has to be settled by simulation: assume a plausible true network (from pilot data or published estimates, including the weak edges), then see whether the key edges can be recovered at different N. Constantin, Schuurman and Vermunt (2026) give the general form of this Monte Carlo method; Lesson 7.6 does a simplified version.</p>
<h4>4. Number of parameters in the full procedure and the degrees of freedom of the equality test</h4>
<p>In the path model of the full procedure, each interval (T1→T2 or T2→T3) has \(p\) autoregressive paths and \(K\) cross-lagged paths that enter the SEM. The unconstrained model estimates the two intervals separately, \(2(p+K)\) path parameters in all; the equality constraints make each path share one parameter across the two intervals, leaving \(p+K\). The other parameters (variances and covariances at T1, residual variances and same-wave residual covariances at each wave, intercepts) are the same in both models. So the degrees of freedom of the nested χ² test are:</p>
""" + MATH(r"\Delta df = 2(p+K) - (p+K) = p + K,\qquad \Delta\chi^2 = \chi^2_{\text{constrained}} - \chi^2_{\text{unconstrained}}") + SYM([
["\\(p\\)", "Number of nodes (9 in the course data)"], ["\\(K\\)", "Number of cross-lagged paths (per interval) entering the SEM under the conservative rule"],
["\\(\\Delta\\chi^2\\)", "The extra misfit of the constrained model over the unconstrained model; if the paths are equal, it approximately follows a χ² distribution with \\(\\Delta df\\) degrees of freedom"]]) + r"""
<p>In the course data \(K\) = {{V:fp10_n_keep}}, so \(\Delta df\) = 9 + {{V:fp10_n_keep}} = {{V:fp10_eq_ddf}} (the log of R/L10-2b.R prints this number, so you can use it to check that the model is written correctly). AIC and BIC are both "misfit + a penalty for the number of parameters":</p>
""" + MATH(r"\mathrm{AIC} = -2\log L + 2q,\qquad \mathrm{BIC} = -2\log L + q\ln N") + SYM([
["\\(\\log L\\)", "Log-likelihood of the model"], ["\\(q\\)", "Number of free parameters in the model"], ["\\(N\\)", "Sample size"]]) + r"""
<p>Smaller is better. The constrained model has \(p+K\) fewer parameters, so as long as its extra misfit is not too large, AIC and BIC will favor it; BIC's penalty grows with \(\ln N\), so it favors the simpler model more than AIC does. Use the constrained model only when none of the three criteria (χ² test, AIC, BIC) argues against equality, and write this rule into the plan in advance.</p>
""",
code=CODE(r"""
source("R/_setup.R"); library(tidyverse)
raw <- read_csv("data/clpn_sim_wide.csv", show_col_types = FALSE)
item_cols <- c(vars_t(1), vars_t(2), vars_t(3))
sapply(raw[item_cols], range)                      # range of values
allowed <- function(v) if (startsWith(v, "lone")) 1:4 else 0:3
n_bad <- sapply(item_cols, function(v) sum(!is.na(raw[[v]]) & !(raw[[v]] %in% allowed(v))))
sum(n_bad)                                         # number of values outside the allowed set (out of range, non-integer)
sum(duplicated(raw$id)); sum(is.na(raw))           # duplicate IDs, missing values
# reverse-scoring example: raw <- raw |> mutate(item_r = 5 - item)
cb <- data.frame(variable = item_cols,
                 mean = round(colMeans(raw[item_cols]), 2),
                 sd   = round(sapply(raw[item_cols], sd), 2))
write.csv(cb, out("L10-1_codebook_stats.csv"), row.names = FALSE)
writeLines(plan, out("L10-1_analysis_plan.md"))   # write it before seeing the results!
# full codebook: merge in item wording and value meanings from the data dictionary (part 5 of the script)
dict <- read.csv("data/data_dictionary.csv", fileEncoding = "UTF-8")
dict$item <- sub("_t1.*$", "", dict$variable)      # "lone1_t1 / _t2 / _t3" → "lone1"
codebook <- data.frame(variable = item_cols, item = sub("_t[0-9]+$", "", item_cols),
                       wave = as.integer(sub("^.*_t", "", item_cols)))
codebook <- merge(codebook, dict[, c("item", "label", "values")], by = "item")
codebook <- merge(codebook, cb, by = "variable")
write.csv(codebook, out("L10-1_codebook.csv"), row.names = FALSE, fileEncoding = "UTF-8")
""", "Main steps of R/L10-1.R (excerpt)"),
quiz=[
("Which research question best suits a CLPN?", ["Does loneliness cause depression?", "Are loneliness and depression correlated?", "To what extent do T1 loneliness items uniquely predict T2 depression items, and vice versa?", "Does the T1 loneliness total predict the T2 depression total?"], 2,
 ["It uses causal wording.", "Too broad; cross-sectional data could answer it.", "Correct: not causal, item level, two-directional.", "Plausible but wrong: no causal wording, but it stays at the level of total scores and asks only one direction, so it does not use what a CLPN is good at; a CLPM could answer it."]),
("Why write the analysis plan before seeing the results?", ["It is a formal course requirement", "To limit researcher degrees of freedom and avoid choosing the analysis according to the results", "To make sure the results match the expectations", "To make the results more significant"], 1,
 ["The formality is only the surface; the real purpose is to stop you from choosing the analysis after seeing the results.", "Correct.", "A plan does not guarantee results; it only guarantees that the analysis does not change with the results. If the results do not match expectations, you still report them.", "Quite the opposite: the plan prevents choosing analyses in order to get significance."]),
("On a 1–4 scale, what does an original 2 become after reverse scoring?", ["2", "3", "4", "1"], 1,
 ["(4+1)−2 = 3.", "Correct.", "That is the result for an original 1.", "That is the result for an original 4."]),
("Dropouts have significantly higher baseline depression than stayers. What does this mean?", ["No effect: the dropouts are no longer in the sample", "Analyzing only stayers makes the sample \"healthier\" and may bias the results; report it and consider imputation", "Fill in the dropouts' missing values with the sample mean", "As long as retention reaches 80%, it can be ignored"], 1,
 ["It is precisely because the dropouts are not in the sample that the people left are systematically \"healthier\".", "Correct.", "Mean imputation underestimates variance, distorts correlations, and ignores the information that dropping out is related to baseline depression; consider multiple imputation or FIML (Lesson 4.3).", "Plausible but wrong: the retention rate in this lesson's example is exactly 0.80, and the dropouts' baseline depression is still far higher than the stayers'; bias depends on how attrition relates to the variables, not only on the proportion."]),
("Why does this course make the full procedure of Wysocki et al. (2025) a required sensitivity analysis?", ["Because LASSO-only results are always wrong", "LASSO alone gives many false positives and pulls coefficients toward 0, and the methods paper recommends the full procedure; only with both side by side can you see which conclusions do not depend on the estimation method", "Because the full procedure separates between-person and within-person effects", "Because the full procedure keeps more edges, so the results are more significant"], 1,
 ["Not \"wrong\": LASSO tends to report too many edges, but the main analysis still uses it so the results can be compared with the existing literature.", "Correct.", "A common misunderstanding. The full procedure is also based on observed scores and also mixes between-person and within-person effects (Lesson 7.5).", "Quite the opposite: after pruning at p < .01, the full procedure usually keeps far fewer edges than lambda.min."]),
("When should the rule for \"how to interpret disagreement between the two analyses\" be set?", ["After seeing both results, pick the more reasonable one", "Before seeing any results, in the dated analysis plan", "When a reviewer asks", "No need: when they disagree, always go with the main analysis"], 1,
 ["Choosing after seeing the results is a researcher degree of freedom.", "Correct.", "By then you have already seen the results.", "That is a rule too, but its reasons must be written down in advance; and edges found only in the main analysis should be labeled \"sensitive to the estimation method\"."]),
("In the course data, each interval of the full procedure has 9 autoregressive paths and K cross-lagged paths entering the SEM. How many degrees of freedom does the nested χ² test of equality across time have?", ["K", "9 + K", "2(9 + K)", "72"], 1,
 ["The autoregressive paths count too: they are also constrained to be equal in the two intervals.", "Correct: the unconstrained model has 2(9 + K) path parameters and the constrained model 9 + K; the difference is 9 + K.", "That is the number of path parameters in the unconstrained model, not the difference between the two models.", "72 is the number of possible cross-lagged positions."]),
("At a minimum, a codebook should contain…", ["Just the variable names", "Variable name, item wording, scale, values and their meaning, wave", "The mean and SD of each variable", "Variable names and ranges are enough; the item wording goes in the paper"], 1,
 ["With only variable names, nobody knows what lone4 asks.", "Correct.", "These are descriptive statistics and part of the codebook; without item wording and scoring, the variables still cannot be understood.", "Plausible but wrong: a codebook should stand on its own; if the item wording is not in it, a few months later even you will have to dig through the paper."]),
],
ex=[
("State your research question", "Writing", r"""<p>Write 2 candidate research questions, rate them against this lesson's three criteria (not causal, item level, two-directional), and choose one.</p>""",
 r"""<p>Example: "In three waves of data from adult community residents, which T1 loneliness items most uniquely predict T2 depressive symptoms, and do depressive symptoms also predict loneliness in return?" Self-rating: not causal (uses "predict"); item level ("which items"); two-directional ("also … in return").</p>"""),
("Run L10-1.R and check the output", "Hands-on", r"""<p>Run R/L10-1.R and answer: (1) Are there any out-of-range values? (2) How many duplicate IDs and missing values are there? (3) In the attrition example, how far apart are the T1 loneliness totals of stayers and dropouts? (4) If lone2 were a reverse-scored item (1–4), write the R code to reverse-score it; if the reverse-scored item were a 0–3 depression item, what would the formula be?</p>""",
 r"""<p>(1) None: all values are allowed (loneliness 1–4, depression 0–3, no non-integers), and the total of "values not in the allowed set" in the log is 0; (2) duplicate IDs = 0, missing = 0; (3) the dropouts' mean T1 loneliness is 10.4 and the stayers' 8.42, about 2 points apart (go by your own output); (4) <code>raw$lone2_t1_r &lt;- 5 - raw$lone2_t1</code> ((4 + 1) − x); for a 0–3 item it is (3 + 0) − x, i.e., <code>3 - x</code>. Do not apply <code>5 - x</code> to every scale.</p>"""),
("Complete a one-page analysis plan", "Writing", r"""<p>Write your analysis plan with the generator on this page, copy it, save it as <code>analysis_plan.md</code>, and put the date at the top. From then on, every setting in the formal analysis follows it.</p>""",
 r"""<p>You can compare it with <code>R/output/L10-1_analysis_plan.md</code>. The key point: the λ rule, seed, CS criterion and sensitivity analyses are all fixed in advance, including the required full procedure (item 8) and what to do when the two analyses disagree (item 9).</p>"""),
("Plan entries for the full procedure", "Writing", r"""<p>Write items 8 and 9 of the analysis plan for your project. Item 8 states each full-procedure setting (λ rule and seed for edge selection, rule for combining intervals, same-wave part, missing data handling, rule for choosing the final model, pruning criterion, node-level summary); item 9 states how each of at least three kinds of disagreement will be reported. Then think: if your data had only two waves, which entries in item 8 would change?</p>""",
 r"""<p>For item 8, follow the table "Full-procedure settings to fix in the plan" on this page; every entry needs a concrete value, not "default". Item 9 should at least distinguish: edges kept in both analyses; edges found only in the main analysis; edges found only in the full procedure; whether construct-level conclusions have the same direction in both analyses.</p><p>With only two waves: there is no second interval, so there is no rule for combining intervals (paths that are 0 in LASSO are simply fixed to 0), and no equality test across time is possible; the final model is the one and only path model, and the other settings stay the same. You then cannot check with T2→T3 whether the results replicate, and the limitations should say so.</p>"""),
],
summary=["Research question: not causal, item level, two-directional.", "Data cleaning: ranges of values, duplicate IDs, missing values, reverse scoring; the codebook records every variable.", "Attrition analysis: compare stayers and dropouts and decide how to handle missing data.", "Write a dated one-page analysis plan before seeing the results (simple preregistration).", "The main analysis is the LASSO-only CLPN; the full procedure of Wysocki et al. (2025) is a required sensitivity analysis, and both its settings and \"what to do when the two analyses disagree\" are written into the plan in advance."],
refs=["Wysocki, A., McCarthy", "Burger, J., Isvoranu", "Constantin, M. A."],
)
