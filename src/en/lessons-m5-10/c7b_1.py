# -*- coding: utf-8 -*-
# Optional advanced lesson 7.6 (opt=True, outside the standard pacing). All numbers are read from R/output/: {{V:…}} see src/en/common/rvals.py; output boxes use RLOG() to slice the logs directly.

L["7.6"] = dict(
lead=r"""<p>After you have estimated a CLPN and before you interpret it, two questions come first. Do the items still measure the same thing at every wave (measurement invariance)? And is the sample large enough (sample size planning)? This lesson answers both with the simulated course data and a real public data set.</p>""",
h_intuition="The same ruler, and a “dry run”",
intuition=r"""
<h3>1. Why ask whether the ruler has changed</h3>
<p>Imagine a community service center tracking residents' loneliness with the same questionnaire in three surveys. For the third survey a new translator changes “I often feel left out” to “I often feel nobody pays attention to me.” The new wording is more colloquial and easier to agree with, so everyone scores half a point higher on this item, although nobody has actually become lonelier. If you compare the mean scores directly, the report will say “residents have become lonelier,” when what changed was the ruler. Lesson 4.1 mentioned this problem, called """ + T("measurement invariance") + r""": whether the same item measures the same thing, on the same scale, at different waves (or in different groups, such as men and women). This lesson shows you how to test it.</p>

<h3>2. Split an item score into three parts</h3>
<p>Suppose each person has an unobserved “true loneliness level,” called a factor (the latent variable from Lesson 0.2), and the 4 loneliness items are its “readings.” Each item score can be split into:</p>
""" + KEY("Item score = intercept + loading × true loneliness level + the item's own error", r"""<ul><li>""" + T("item intercept") + r""": the expected score on this item when true loneliness is at the reference level (e.g., the average at wave 1); like the zero point of a scale.</li>
<li>""" + T("factor loading") + r""": how much higher the item score is, on average, for each 1-unit increase in true loneliness; like the sensitivity of a scale.</li>
<li>Residual: what is specific to this item plus random error, unrelated to true loneliness.</li></ul>""") + r"""
<p>“The ruler has not changed” means using the same scale each time: same zero point, same sensitivity. In the translation example, the intercept of lone2 went up at wave 3; the loading may not have changed.</p>

<h3>3. Three steps: each extra equality allows one more kind of comparison</h3>
""" + TABLE(["Level", "What must be equal across waves (or groups)", "What you can compare once it holds", "Social work example"], [
["① " + T("configural invariance"), "Only the structure: the same items belong to the same factors (all 4 loneliness items measure only loneliness). Loadings and intercepts may differ", "Only that you are “broadly measuring the same kind of thing”; you can't compare numbers yet", "In both surveys the loneliness items measure loneliness; no item has drifted to measuring depression"],
["② " + T("metric invariance", "weak invariance"), "On top of ①, each item's loading is equal (same sensitivity)", "<b>Relations</b>: correlations, regression coefficients, CLPN edges", "Is the link between loneliness and depression as strong at wave 3 as at wave 1?"],
["③ " + T("scalar invariance", "strong invariance"), "On top of ②, each item's intercept is equal too (same zero point)", "<b>Means</b>: who is higher, whether levels rise", "After a year of services, has residents' loneliness gone down on average?"]]) + r"""
<p>A fourth level, equal residuals (strict invariance), is not required in most studies; just be aware of it.</p>

<h3>4. How to decide whether a level holds</h3>
<p>Each step up adds a set of """ + T("equality constraints") + r""" (Lesson 5.2). More constraints can only make the fit worse or leave it unchanged; the question is how much worse. Look at two things:</p>
<ol><li>The chi-square difference test (Δχ², <code>anova()</code> / <code>lavTestLRT()</code> from Lesson 5.2): p &gt; .05 means the constraints did not make the fit noticeably worse. But the larger the sample, the more sensitive it is: with hundreds or thousands of people, trivial differences become significant.</li>
<li>Changes in fit indices: a common rule of thumb is that """ + T("change in CFI", "ΔCFI") + r""" should not drop below −0.01 (Cheung &amp; Rensvold, 2002) and ΔRMSEA should not exceed 0.015 (Chen, 2007). These do not inflate with sample size, so they are more useful in large samples. Chen's (2007) cutoffs are meant for a fairly large total sample (N &gt; 300) with groups of similar size; for smaller samples (N ≤ 300) she recommends the stricter ΔCFI ≥ −0.005 and ΔRMSEA ≤ 0.010, together with ΔSRMR: at most 0.030 when testing loadings and at most 0.010 when testing intercepts (0.025 and 0.005 in small samples).</li></ol>
<p>Report both. When they disagree (typically “significant chi-square, but tiny ΔCFI”), give more weight to the fit indices and report both results in the paper.</p>

<h3>5. Results for the course data</h3>
<p>R/L7-6.R tests the three levels for the 4 loneliness items × 3 waves (N = 800, robust estimator MLR):</p>
""" + TABLE(["Model", "χ²", "df", "CFI", "RMSEA", "ΔCFI", "ΔRMSEA", "Chi-square difference p"], [
["Configural", "{{V:mi_long_conf_chisq}}", "{{V:mi_long_conf_df}}", "{{V:mi_long_conf_CFI}}", "{{V:mi_long_conf_RMSEA}}", "—", "—", "—"],
["Metric", "{{V:mi_long_metr_chisq}}", "{{V:mi_long_metr_df}}", "{{V:mi_long_metr_CFI}}", "{{V:mi_long_metr_RMSEA}}", "{{V:mi_long_metr_dCFI}}", "{{V:mi_long_metr_dRMSEA}}", "{{V:mi_long_metr_lrtp}}"],
["Scalar", "{{V:mi_long_scal_chisq}}", "{{V:mi_long_scal_df}}", "{{V:mi_long_scal_CFI}}", "{{V:mi_long_scal_RMSEA}}", "{{V:mi_long_scal_dCFI}}", "{{V:mi_long_scal_dRMSEA}}", "{{V:mi_long_scal_lrtp}}"]]) + r"""
<p class="muted" style="font-size:.88rem">Source: R/output/L7-6_log.txt, Part 1.</p>
<p>Read it in order. The configural model itself fits well (if it already fits poorly, e.g., CFI &lt; .90, even the structure differs, and you need to go back and check the factor model first). At both the metric and the scalar step, the chi-square difference is not significant, CFI barely changes, and RMSEA even drops a little (it rewards more parsimonious models). All three levels hold, so you can compare the loneliness means of the three waves: the factor means at waves 2 and 3 are {{V:mi_long_F2}} and {{V:mi_long_F3}} higher than at wave 1, neither significant (p = {{V:mi_long_F2_p}}, {{V:mi_long_F3_p}}), which fits the fact that the data were generated by a process that does not change over time. In a paper, put the χ², df, CFI, and RMSEA of the three models and the ΔCFI, ΔRMSEA, and Δχ² of each step in one table (the minimum reporting recommended by Putnick &amp; Bornstein, 2016), and state the estimator and the decision rules.</p>
<p>Comparing the 5 depression items by gender (T1, {{V:mi_n_m}} men, {{V:mi_n_f}} women) also passes all three levels (equal loadings p = {{V:mi_sex_metr_lrtp}}, equal intercepts p = {{V:mi_sex_scal_lrtp}}), so the means can be compared: the depression factor mean of women is {{V:mi_sex_diff}} higher than that of men (SE = {{V:mi_sex_diff_se}}, p = {{V:mi_sex_diff_p}}). In the simulated data, the same amount was added to every depression item for women: the difference lies in the people, not in the wording of any one item, so invariance holds.</p>

<h3>6. Breaking the ruler on purpose: what failure looks like</h3>
<p>The script adds 0.5 to everyone's lone2 (Feeling left out) score at wave 3, mimicking the translation story from the beginning:</p>
<ul><li><b>The scalar level fails</b>: χ² jumps from {{V:mi_bad_metr_chisq}} to {{V:mi_bad_scal_chisq}}, ΔCFI = {{V:mi_bad_scal_dCFI}}, far beyond −0.01. The configural and metric levels are unaffected: adding a constant does not change the sensitivity.</li>
<li><b>Finding the “broken item”</b>: a """ + T("score test") + r""" estimates, constraint by constraint, how much χ² would drop if that one equality constraint were freed. The largest is the equality of the {{V:mi_score1_a}} intercept and the {{V:mi_score1_b}} intercept (X² = {{V:mi_score1_x2}}), far above the next one ({{V:mi_score2_x2}}). It points straight at the item that was changed.</li>
<li><b>The fix</b>: """ + T("partial invariance") + r""". Free only this item's intercept at wave 3 and keep all other constraints: ΔCFI goes back to {{V:mi_bad_part_dCFI}}, and the model holds.</li></ul>
<p>The consequence shows up in the means. If you force the intercepts to be equal, the wave 3 loneliness factor mean is pushed from {{V:mi_F3_orig}} up to {{V:mi_F3_forced}}: a change in one item's wording is taken for “everyone became lonelier.” With partial invariance, the mean returns to {{V:mi_F3_part}}, close to the original data.</p>
""" + WARN("When partial invariance is acceptable", "Free as few items as possible (a common recommendation is that at least half of the items of each factor stay equal), have a reason for every item you free (e.g., its wording was changed), and state in the paper which parameters you freed. Do not free items one by one just to make the model “pass.”") + r"""

<h3>7. What this has to do with CLPN</h3>
<p>A CLPN does not use factors; it takes each observed item directly as a node. That makes item-level invariance even more important:</p>
<ul><li>A loading changes (metric invariance fails): the item's correlations with the other items change, and so do its autoregressive and cross-lagged edges. A “network change” between T1 → T2 and T2 → T3 may just be a change in the item's sensitivity.</li>
<li>An intercept changes (scalar invariance fails): if everyone simply gets the same amount added, the correlations do not change and neither do the CLPN edges, but the means across waves (the descriptive table, “did the symptoms get worse?”) will be wrong. Real changes in wording often change the sensitivity at the same time.</li></ul>
<p>The equality-across-time test in the full procedure of Lesson 7.5 constrains paths (whether the T1 → T2 edges equal the T2 → T3 edges), not item loadings and intercepts, so it cannot replace the tests in this lesson. Whichever CLPN you use, run this lesson's tests as part of your descriptive statistics, or state in the limitations that you did not.</p>

<h3>8. Worked example: how large a sample? A “dry run” by simulation</h3>
<p>There is no ready-made sample size formula for a CLPN, but you can rehearse: ① assume a “true network” (here the population target matrix <code>true_B_population</code> of the course data, so the simulation answers “what N do I need to recover the population target,” not the within-person truth; for your own study you can use estimates from a pilot study or the literature); ② generate a data set of N people from it, estimate a CLPN once, and record which edges are recovered and which are falsely reported; ③ do this for several values of N, many times each. This is called a """ + T("Monte Carlo simulation") + r""" (Constantin et al., 2026, describe the general method for network models). Record two numbers:</p>
<ul><li>""" + T("statistical power") + r""": the proportion of the {{V:ss_n_target}} “target edges” (the stronger edges of the generating model, |B| ≥ 0.08) that are recovered with the correct sign.</li>
<li>""" + T("false positive rate") + r""": the proportion of the {{V:ss_n_near0}} near-zero edges (|B| &lt; 0.02) that are estimated as nonzero.</li></ul>
""" + TABLE(["N", "<code>lambda.min</code>: power", "<code>lambda.min</code>: all 8 recovered", "<code>lambda.min</code>: false positive rate", "<code>lambda.min</code>: r with population target", "<code>lambda.1se</code>: power", "<code>lambda.1se</code>: false positive rate"], ss_table_rows()) + r"""
<p class="muted" style="font-size:.88rem">Source: R/output/L7-6_power.csv ({{V:ss_reps}} replications per N).</p>
<ol><li><b><code>lambda.min</code> (the course default):</b> power exceeds 0.80 already at N = {{V:ss_min_power80_n}}; to recover all 8 target edges in more than 80% of the simulations you need N ≈ {{V:ss_min_all8_80_n}}. But the false positive rate stays between {{V:ss_min_fpr_lo}} and {{V:ss_min_fpr_hi}} and does not fall as N grows. There are two reasons: the larger N is, the smaller the λ chosen by cross-validation, so weak edges slip in more easily; and most of these “near-zero edges” are not exactly 0 in the population, so with a larger N LASSO increasingly detects these tiny but real coefficients. Either way, under <code>lambda.min</code> you cannot treat very weak edges in the plot as meaningful findings.</li>
<li><b><code>lambda.1se</code> (more conservative):</b> the false positive rate is only {{V:ss_1se_fpr_lo}}–{{V:ss_1se_fpr_hi}}, but power is only {{V:ss_1se_1200_power_target}} even at N = 1200. This is the trade-off from Lesson 3.5: a lenient rule recovers more and also reports more false positives. A sample size plan should report both numbers and state the λ rule.</li>
<li><b>These proportions have Monte Carlo error of their own.</b> Each proportion is the average of {{V:ss_reps}} results. For a proportion near 0.5, the standard error is about \(\sqrt{0.5 \times 0.5 / {{V:ss_reps}}}\), i.e., about 0.1, and the 95% interval is roughly ±0.2. So read “N ≈ {{V:ss_min_all8_80_n}}” as “somewhere around the neighboring values of N”: with another seed, the point where it crosses 0.80 could move one step up or down. For a research proposal, raise <code>REPS</code> to several hundred before you read off this number, and report the number of replications.</li></ol>
""" + WARN("A dry run only holds under its assumptions", "A different true network (weaker edges), more nodes (more predictors per regression), more skewed items, missing data or attrition all increase the N you need. In the research plan, state clearly what network you assumed, how many nodes, which λ rule, and whether the goal is power of 0.80 or recovering every edge.") + r"""
""",
h_math="Writing the three parts as an equation",
math=r"""
<h4>1. The measurement equation</h4>
""" + MATH(r"x_{kti}=\tau_{kt}+\lambda_{kt}\,\eta_{ti}+\varepsilon_{kti}") + SYM([
(r"\(x_{kti}\)", "Score of person i on item k at wave t"),
(r"\(\eta_{ti}\)", "Greek eta: the factor (true loneliness level) of person i at wave t"),
(r"\(\lambda_{kt}\)", "Greek lambda: the loading (sensitivity) of item k at wave t"),
(r"\(\tau_{kt}\)", "Greek tau: the intercept (zero point) of item k at wave t"),
(r"\(\varepsilon_{kti}\)", "Residual: what is specific to this item plus random error"),
]) + r"""
<h4>2. The three levels of constraints</h4>
""" + MATH(r"\text{Configural: same structure at every wave};\quad \text{Metric: }\lambda_{k1}=\lambda_{k2}=\lambda_{k3};\quad \text{Scalar: also }\tau_{k1}=\tau_{k2}=\tau_{k3}") + r"""
<p>Why can you compare means only under scalar invariance? Average over people at wave t: \(\bar x_{kt}=\tau_{kt}+\lambda_{kt}\,\bar\eta_t\). The difference between the mean scores of two waves = the difference in intercepts + loading × the difference in factor means (when the loadings are equal). Only when the intercepts are equal does the change in the item mean come entirely from the change in the factor mean. Otherwise a shift of the ruler's zero point and a change in the people are mixed together and cannot be separated.</p>
<h4>3. Identification: giving the factor a scale</h4>
<p>The factor is unobserved, so its unit has to be fixed by convention. In this lesson, the wave 1 factor variance is fixed to 1 and its mean to 0. Once the loadings are equal, the variances at waves 2 and 3 can be estimated freely; once the intercepts are equal, the means at waves 2 and 3 can be estimated freely, and those are what we want to compare. In the script, <code>F1 ~~ 1*F1</code> and <code>F2 ~ NA*1</code> make these settings.</p>
<h4>4. Chi-square differences under robust estimation</h4>
<p>ΔCFI and ΔRMSEA are both “the stricter model minus the looser model.” With the robust estimator (MLR), you cannot simply subtract the two χ² values: the difference needs a scaling correction (Satorra–Bentler), which <code>lavTestLRT()</code> applies automatically. Course data, metric vs. configural: corrected Δχ² = {{V:mi_long_metr_dchisq}}, Δdf = {{V:mi_long_metr_ddf}}, p = {{V:mi_long_metr_lrtp}}.</p>
<h4>5. The two measures of the sample size simulation</h4>
""" + MATH(r"\text{Power}=\frac{1}{R}\sum_{r=1}^{R}\frac{1}{|T|}\sum_{(k,j)\in T}\mathbf 1\big[\hat\beta^{(r)}_{kj}\neq 0\ \text{and correct sign}\big],\qquad \text{FPR}=\frac{1}{R}\sum_{r=1}^{R}\frac{1}{|Z|}\sum_{(k,j)\in Z}\mathbf 1\big[\hat\beta^{(r)}_{kj}\neq 0\big]") + SYM([
(r"\(R\)", "Number of simulation replications (the script uses {{V:ss_reps}} per N)"),
(r"\(T,\ |T|\)", "The set of target edges and their number ({{V:ss_n_target}})"),
(r"\(Z,\ |Z|\)", "The set of near-zero edges and their number ({{V:ss_n_near0}})"),
(r"\(\mathbf 1[\cdot]\)", "Indicator function: 1 if the condition in brackets holds, 0 otherwise"),
]) + r"""
""",
code=CODE(r"""
source("R/_setup.R"); library(lavaan)
dat <- read_course_data()
# 1. Model syntax: same label = same parameter (equality constraint)
#    Configural: loading labels l1_1, l1_2, ... all differ; metric: l1-l4 at every wave; scalar: intercepts i1-i4 too
#    R/L7-6.R writes the three models with a small function lone_model(level); waves 1 and 2 of the metric model look like this:
#    F1 =~ NA*lone1_t1 + l1*lone1_t1 + NA*lone2_t1 + l2*lone2_t1 + ...
#    F2 =~ NA*lone1_t2 + l1*lone1_t2 + NA*lone2_t2 + l2*lone2_t2 + ...
#    lone1_t1 ~~ lone1_t2 + lone1_t3   # residual correlations of the same item across waves (what is specific to the item)
f_conf <- cfa(lone_model("configural"), data = dat, estimator = "MLR", meanstructure = TRUE)
f_metr <- cfa(lone_model("metric"),     data = dat, estimator = "MLR", meanstructure = TRUE)
f_scal <- cfa(lone_model("scalar"),     data = dat, estimator = "MLR", meanstructure = TRUE)
lavTestLRT(f_conf, f_metr, f_scal)                       # scaled chi-square difference tests
sapply(list(f_conf, f_metr, f_scal), fitMeasures, c("cfi.robust", "rmsea.robust"))

# 2. Multiple groups: group.equal adds the constraints in one line
dat$sex <- factor(dat$gender, levels = c(0, 1), labels = c("Male", "Female"))
g_scal <- cfa("Dep =~ dep1_t1 + dep2_t1 + dep3_t1 + dep4_t1 + dep5_t1", data = dat,
              group = "sex", estimator = "MLR", group.equal = c("loadings", "intercepts"))

# 3. Find the worst-fitting equality constraint: score test (computed under ML)
bad <- dat; bad$lone2_t3 <- bad$lone2_t3 + 0.5     # raise the wave 3 lone2 intercept by 0.5 on purpose
b_scal_ml <- cfa(lone_model("scalar"), data = bad, estimator = "ML", meanstructure = TRUE)
head(lavTestScore(b_scal_ml)$uni[order(-lavTestScore(b_scal_ml)$uni$X2), ], 3)
b_part <- cfa(lone_model("scalar", free_int = "lone2_t3"), data = bad, estimator = "MLR", meanstructure = TRUE)
""", "Core of R/L7-6.R (invariance)") + r"""
<p><b>Notes:</b> <code>NA*lone1_t1</code> frees the first loading too (lavaan fixes it to 1 by default), because we set the scale with “wave 1 factor variance = 1” instead. <code>lavTestScore()</code> labels parameters with internal codes (such as <code>.p5.</code>); the script uses <code>parTable()</code> to translate them into item names. In multiple-group models, <code>group.equal</code> adds the constraints for you, which is easier than writing labels; in longitudinal models the constraints span different variables, so you have to write the labels by hand.</p>
""" + OUT(RLOG("L7-6_log.txt", "===== Part 1", end="===== Part 2"), "Actual output: excerpt from R/output/L7-6_log.txt (Part 1)") + r"""
<p>Columns: <code>dCFI</code> and <code>dRMSEA</code> are the changes from the row above; <code>judge</code> applies ΔCFI ≥ −0.01 and ΔRMSEA ≤ 0.015. <code>Chisq diff</code> is the scaled chi-square difference.</p>
""" + OUT(RLOG("L7-6_log.txt", "===== Part 3", end="===== Part 4"), "Actual output: excerpt from R/output/L7-6_log.txt (Part 3: breaking the ruler on purpose)") + CODE(r"""
# 4. Sample size simulation (REPS replications per N)
B  <- true_B()                                   # the assumed true network
R1 <- cor(dat[, vars_t(1)]); R2 <- cor(dat[, vars_t(2)])
Se <- R2 - t(B) %*% R1 %*% B                     # residual covariance: keeps the simulated T2 item variances near 1
off    <- row(B) != col(B)                       # positions of the cross-lagged edges (no autoregression)
target <- off & abs(B) >= 0.08                   # target edges
near0  <- off & abs(B) < 0.02                    # near-zero edges
for (N in c(150, 300, 500, 800, 1200)) for (rep in 1:REPS) {
  X <- rmvn(N, R1); Y <- X %*% B + rmvn(N, Se)  # generate a data set from the true network
  e <- est_both(X, Y)                            # one cross-validation, taking both lambda.min and lambda.1se
  # score(): power = share of target edges nonzero with the correct sign; FPR = share of near-zero edges nonzero
}
""", "Core of R/L7-6.R (sample size simulation)") + r"""
""" + OUT(RLOG("L7-6_log.txt", "Each N repeated", end="Simulation completed"), "Actual output: excerpt from R/output/L7-6_log.txt (Part 4)") + r"""
<p><b>Run time:</b> the whole script takes about 40 seconds to 1 minute, most of it in Part 4 ({{V:ss_reps}} × 5 = 100 CLPN estimations). For smoother curves, set <code>REPS</code> to 50 (about 2–3 minutes); the numbers will then differ slightly from those on this page.</p>""",
quiz=[
("At wave 3, the wording of one item is changed so that everyone scores 0.5 higher on it, while nothing real has changed. Which level of invariance breaks first?", ["Configural invariance", "Metric invariance", "Scalar invariance", "None"], 2,
 ["The structure is unchanged; the item still measures loneliness.", "Adding the same amount to everyone does not change the sensitivity (loading).", "Correct: the intercept (zero point) changed, so scalar invariance fails; you can no longer compare the means of the waves directly.", "The intercept changed, so scalar invariance fails."]),
("Metric invariance holds but scalar invariance does not. Which comparison is still reasonable?", ["Comparing the mean loneliness score at wave 1 and wave 3", "Comparing the correlation between loneliness and depression at the two waves", "Saying “people were lonelier at wave 3”", "Nothing can be compared"], 1,
 ["Comparing means needs scalar invariance: with unequal intercepts, the change in the mean includes a shift of the zero point.", "Correct: equal loadings let you compare relations (correlations, regression coefficients, edges).", "That sentence compares means, which needs scalar invariance.", "Metric invariance holds, so relations (correlations, regression coefficients, edges) can still be compared."]),
("With N = 2000, the chi-square difference test of scalar vs. metric gives p = .004, but ΔCFI = −0.002 and ΔRMSEA = 0.001. What is the most reasonable conclusion?", ["Scalar invariance definitely fails", "With a large sample, chi-square is oversensitive; the fit indices barely change, so scalar invariance roughly holds, and you report both results", "The two results contradict each other, so the analysis is wrong", "Drop half the sample and test again"], 1,
 ["With a large sample, chi-square reacts even to tiny differences, so don't decide on it alone; ΔCFI and ΔRMSEA are both within bounds.", "Correct.", "This kind of disagreement is common in large samples and does not mean the analysis is wrong.", "Dropping cases to make a test nonsignificant is manipulating the result."]),
("What does the score test do in an invariance analysis?", ["Tests whether the whole model fits", "Estimates how much χ² would drop if one equality constraint were freed, to find the worst-fitting constraint", "Computes the factor means", "Replaces cross-validation for choosing λ"], 1,
 ["Overall fit is judged with the chi-square test and fit indices; the score test looks at single constraints.", "Correct: the course script used it to find the altered lone2_t3 intercept directly.", "Factor means are parameter estimates of the model, not output of the score test.", "The score test is a diagnostic for SEM constraints and has nothing to do with choosing λ for LASSO."]),
("A CLPN uses the observed items directly as nodes. Which of these is most likely to change the CLPN's edges?", ["Everyone scores 0.5 higher on an item at wave 3", "An item's loading gets smaller at wave 3 (its relation to loneliness weakens)", "The sample's mean age is 1 year higher at wave 3", "All items at wave 3 are linearly rescaled to 0–100"], 1,
 ["Adding a constant does not change correlations, so it does not change the edges; but it misleads mean comparisons.", "Correct: a change in loading changes the item's correlations with the other items, and so changes the edges.", "This is a small change in who is in the sample, not a measurement problem; a 1-year difference in mean age hardly changes how the items relate to each other.", "A linear rescaling does not change correlations; a CLPN standardizes first, so the edges stay the same."]),
("In the course's sample size simulation, the false positive rate of <code>lambda.min</code> does not fall as N grows. What is the most likely reason?", ["The larger N, the larger the sampling noise", "The larger N, the smaller the λ chosen by cross-validation, so very weak edges are kept more easily", "<code>lambda.min</code> never reports false positives", "glmnet stops standardizing when N is large"], 1,
 ["The opposite: the larger N, the smaller the sampling noise. The false positive rate stays because λ also shrinks with N, and most near-zero edges are not exactly 0 in the population.", "Correct: that is why a sample size plan should report both power and the false positive rate and state the λ rule. Another reason is that most of these near-zero edges are not exactly 0 in the population.", "In the course data the false positive rate of <code>lambda.min</code> is between {{V:ss_min_fpr_lo}} and {{V:ss_min_fpr_hi}}.", "glmnet always standardizes internally by default, whatever N is."]),
],
ex=[
("Read the table: invariance across gender", "Foundational", r"""<p>Results from Part 2 of R/L7-6.R: configural χ²({{V:mi_sex_conf_df}}) = {{V:mi_sex_conf_chisq}}, CFI = {{V:mi_sex_conf_CFI}}; metric ΔCFI = {{V:mi_sex_metr_dCFI}}, chi-square difference p = {{V:mi_sex_metr_lrtp}}; scalar ΔCFI = {{V:mi_sex_scal_dCFI}}, p = {{V:mi_sex_scal_lrtp}}.</p>
<p>(1) Which levels hold? (2) Can you write “women are more depressed than men”? (3) What would you do if ΔCFI at the scalar step were −0.03?</p>""",
 r"""<p>(1) All three levels hold: at neither step does ΔCFI drop below −0.01 (CFI even rises slightly), and neither chi-square difference is significant.</p>
<p>(2) You can compare the means: the depression factor mean of women is {{V:mi_sex_diff}} higher than that of men (SE = {{V:mi_sex_diff_se}}, p = {{V:mi_sex_diff_p}}). Still word it carefully: this is a difference in group averages and does not apply to any individual woman; and the data are simulated.</p>
<p>(3) Scalar invariance fails, so don't compare the means yet. Use the score test to find the item whose intercept fits worst, and check whether its content gives a reason why it might “read differently” for men and women (e.g., items about crying often show gender differences). If only one or two items are affected, you can free just their intercepts (partial invariance), then compare the means, and state in the paper which items you freed.</p>"""),
("Hands-on: longitudinal invariance of the 5 depression items", "Hands-On", r"""<p>Following Part 1 of R/L7-6.R, test configural → metric → scalar invariance for the 5 depression items × 3 waves of the course data (hint: replace <code>lone_items</code> with <code>dep_items</code> in <code>lone_model()</code>, and note that the number of items goes from 4 to 5). Report χ², df, CFI, RMSEA, ΔCFI, and the chi-square difference p for the three models, and decide whether each level holds.</p>""",
 r"""<p>Reference solution <code>R/solutions/L7-6_solution.R</code> (log <code>R/output/sol_L7-6_log.txt</code>):</p>
""" + TABLE(["Model", "χ²", "df", "CFI", "RMSEA", "ΔCFI"], [
["Configural", "{{V:sol76_dep_conf_chisq}}", "{{V:sol76_dep_conf_df}}", "{{V:sol76_dep_conf_CFI}}", "{{V:sol76_dep_conf_RMSEA}}", "—"],
["Metric", "{{V:sol76_dep_metr_chisq}}", "{{V:sol76_dep_metr_df}}", "{{V:sol76_dep_metr_CFI}}", "{{V:sol76_dep_metr_RMSEA}}", "{{V:sol76_dep_metr_dCFI}}"],
["Scalar", "{{V:sol76_dep_scal_chisq}}", "{{V:sol76_dep_scal_df}}", "{{V:sol76_dep_scal_CFI}}", "{{V:sol76_dep_scal_RMSEA}}", "{{V:sol76_dep_scal_dCFI}}"]]) + r"""
<p>Chi-square difference p: metric vs. configural = {{V:sol76_dep_p_metr}}, scalar vs. metric = {{V:sol76_dep_p_scal}}; both ΔCFI values are within −0.01. All three levels hold. The depression factor means at waves 2 and 3 (wave 1 = 0) are {{V:sol76_dep_F2}} and {{V:sol76_dep_F3}}: almost no change. The df are larger than in the loneliness model because there is one more item.</p>"""),
("Real data: social well-being of coaches", "Hands-On + Writing", r"""<p>data/coaches_mhc_raw.csv is a real public data set (422 sports coaches in Switzerland, 3 waves, CC0; read the last section of the <a href="../data/data_dictionary.html">data dictionary</a> first). The 5 social well-being items (items 4–8: having something to contribute to society, belonging to a community, society is getting better, people are basically good, the way society works makes sense) are closely related to community work.</p>
<ol><li>Read the data with <code>read.csv2("data/coaches_mhc_raw.csv", dec = ".")</code>. Start with a data check: recompute each wave's social well-being mean from the item columns and correlate it with the file's own <code>t1socwb</code>, <code>t2socwb</code>, <code>t3socwb</code>. What do you find?</li>
<li>Test three levels of longitudinal invariance for <code>t1w4</code>–<code>t1w8</code>, <code>t2w4</code>–<code>t2w8</code>, <code>t3w4</code>–<code>t3w8</code>. Waves 2 and 3 have attrition; use <code>missing = "ml"</code> (FIML, Lesson 4.3) so that all 422 people enter the model.</li>
<li>Write a report of about 150 words: which levels hold, what you can and cannot compare, and the limitations of these data.</li></ol>""",
 r"""<p>Reference solution <code>R/solutions/L7-6_solution.R</code>:</p>
<p>(1) The file's own subscale mean columns do not match the item columns: for social well-being the correlations at the three waves are only {{V:sol76_chk_soc_T1}}, {{V:sol76_chk_soc_T2}}, {{V:sol76_chk_soc_T3}} (they should be close to 1). So compute the scores yourself from the item columns only. This is a step you must take whenever you work with someone else's data.</p>
<p>(2) Results (FIML, N = 422; only {{V:sol76_coach_ncomplete}} people have all three waves):</p>
""" + TABLE(["Model", "χ²", "df", "CFI", "RMSEA", "ΔCFI"], [
["Configural", "{{V:sol76_coach_conf_chisq}}", "{{V:sol76_coach_conf_df}}", "{{V:sol76_coach_conf_CFI}}", "{{V:sol76_coach_conf_RMSEA}}", "—"],
["Metric", "{{V:sol76_coach_metr_chisq}}", "{{V:sol76_coach_metr_df}}", "{{V:sol76_coach_metr_CFI}}", "{{V:sol76_coach_metr_RMSEA}}", "{{V:sol76_coach_metr_dCFI}}"],
["Scalar", "{{V:sol76_coach_scal_chisq}}", "{{V:sol76_coach_scal_df}}", "{{V:sol76_coach_scal_CFI}}", "{{V:sol76_coach_scal_RMSEA}}", "{{V:sol76_coach_scal_dCFI}}"]]) + r"""
<p>At the metric step both kinds of evidence say it holds (p = {{V:sol76_coach_p_metr}}, ΔCFI = {{V:sol76_coach_metr_dCFI}}). The scalar step is borderline: the chi-square difference is significant (p = {{V:sol76_coach_p_scal}}), and ΔCFI = {{V:sol76_coach_scal_dCFI}} is still within the common −0.01 rule; but only {{V:sol76_coach_ncomplete}} people have all three waves, and by Chen's (2007) stricter −0.005 rule for small samples it fails. The score test shows that the worst-fitting constraint is the equality of the {{V:sol76_worst_a}} and {{V:sol76_worst_b}} intercepts (X² = {{V:sol76_worst_x2}}, “having something to contribute to society”). Freeing only the intercept of {{V:sol76_part_item}} gives ΔCFI = {{V:sol76_part_dCFI}} compared with the metric model. The conclusion about the means hardly changes: the factor means at waves 2 and 3 are {{V:sol76_coach_F2_full}} and {{V:sol76_coach_F3_full}} under full scalar invariance and {{V:sol76_coach_F2_part}} and {{V:sol76_coach_F3_part}} under partial scalar invariance (SE about {{V:sol76_coach_F_se}} each), all close to 0. Note also that the configural model itself fits only acceptably (CFI = {{V:sol76_coach_conf_CFI}}, RMSEA = {{V:sol76_coach_conf_RMSEA}}).</p>
<p>(3) Sample report: “Tests of longitudinal measurement invariance of the 5 social well-being items across three waves (MLR, FIML, N = 422) supported metric invariance (ΔCFI = {{V:sol76_coach_metr_dCFI}}). The scalar model had a significant chi-square difference and ΔCFI = {{V:sol76_coach_scal_dCFI}}, which fails the small-sample criterion (only {{V:sol76_coach_ncomplete}} participants completed all three waves). After freeing the intercept of {{V:sol76_part_item}} (wave 2, ‘having something to contribute to society’), partial scalar invariance held, and the factor means of the later waves did not differ noticeably from wave 1. Relations can therefore be compared across waves; mean comparisons should rely on the partial invariance model. Limitations: the documentation describes the intervals between waves inconsistently (3 / 6 months or 6 / 12 months), so we do not interpret the rate of change; retention at wave 3 was about 61%; and there are no demographic variables, so group comparisons are not possible.”</p>"""),
("Sample size: one sentence for a research plan", "Conceptual", r"""<p>You plan a two-wave CLPN with 9 items (4 loneliness, 5 depression) and expect N = 300. Using this lesson's sample size table, answer: (1) What can you expect with <code>lambda.min</code> and with <code>lambda.1se</code>? (2) How would the conclusion change if your network had 15 nodes and weaker true edges than the course data? (3) Write a one-sentence sample size statement for the research plan.</p>""",
 r"""<p>(1) At N = 300, <code>lambda.min</code> has power of about {{V:ss_min_300_power_target}} but a false positive rate of about {{V:ss_min_300_fpr_near0}}, and the probability of recovering all 8 target edges is only {{V:ss_min_300_p_all8}}; <code>lambda.1se</code> has a false positive rate of only {{V:ss_1se_300_fpr_near0}} but power of only {{V:ss_1se_300_power_target}}. You will see most of the stronger edges, but quite a few very weak false edges will slip in, so whether a single edge is there has to be checked with the bootstrap of M8.</p>
<p>(2) More nodes mean more predictors in each regression; weaker edges are harder to tell from 0. Both raise the N you need. You cannot apply this lesson's table directly; rerun the simulation with your own assumed network (change <code>B</code> and <code>N_GRID</code>).</p>
<p>(3) Example: “Taking the population coefficients of the simulated course data as the assumed true network (9 nodes), a simulation with {{V:ss_reps}} replications per sample size showed that at N = 300 with the <code>lambda.min</code> rule, about {{V:ss_min_300_power_target}} of the stronger edges (|B| ≥ 0.08) were recovered, but the false positive rate for near-zero edges was about {{V:ss_min_300_fpr_near0}}; we therefore treat the presence or absence of edges as exploratory and assess their stability with the bootstrap.” (Replace the numbers with those from your own simulation.)</p>"""),
],
summary=[
    "Measurement invariance = different waves / groups use the same ruler: configural (same structure) → metric (equal loadings; relations comparable) → scalar (equal intercepts too; means comparable).",
    "Decision: Δχ² plus ΔCFI ≥ −0.01 and ΔRMSEA ≤ 0.015; with large samples chi-square is oversensitive, so rely mainly on the fit indices and report both.",
    "All three levels hold in the course data; after one item's intercept is changed on purpose, scalar invariance fails, the score test finds the item, and partial invariance fixes it; otherwise the means would be misjudged.",
    "A CLPN uses observed items as nodes: changed loadings change the edges; changed intercepts mislead mean comparisons.",
    "Plan the sample size with a simulated dry run: <code>lambda.min</code> has high power but a false positive rate of {{V:ss_min_fpr_lo}}–{{V:ss_min_fpr_hi}}; <code>lambda.1se</code> has few false positives but low power. The conclusions hold only for the assumed network, number of nodes, and λ rule.",
    "Check real data first: the coaches data's own subscale columns do not match the item columns, so use the item columns only."
],
refs=["Putnick, D. L.", "Cheung, G. W.", "Chen, F. F.", "Constantin, M. A.", "Ackeret, N.", "Wysocki, A., McCarthy"],
)
