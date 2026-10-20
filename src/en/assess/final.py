# -*- coding: utf-8 -*-
# Final exam: Part A 25 auto-graded questions (8 of them parallel to the pre-test, marked [Parallel]);
# Part B 4 interpretation questions (numbers from R/output via {{V:key}});
# Part C 5 small R tasks (answers from R/output/assess_answers.csv, written by R/assess_answers.R; ANS is provided by the builder).

LEAD = "<p>Take this after Lesson 10.3; about 90 minutes. Part A has 25 auto-graded questions; Part B has 4 interpretation questions (write your answer first, then score it point by point against the reference answer and rubric; you may revise and score again); Part C has 5 questions you work out in R.</p>"

INTRO = """<section class="sec" id="rules"><h2>Before you start</h2>
<ul><li><b>Parts A and C are scored on first-try answers</b>: only your first answer to each question counts. The "(y correct on first try)" count at the top of the page is your score. Each Part A question is worth 2 points (50 in total) and each Part C question 2 points (10 in total).</li>
<li>Each Part B question is worth 10 points, scored on four dimensions: conclusion 4 · numbers and intervals 3 · direction 2 · no over-interpretation 1. Finish writing before you open the reference answer.</li>
<li>Part A can be done closed-book; for Part B you may open the course's figures and tables; Part C needs RStudio and the course data <code>data/clpn_sim_wide.csv</code>.</li>
<li>Eight Part A questions test the same points as the <a href="assess_pre.html">pre-test</a> (with different numbers and settings). When you finish, compare your score with the pre-test score in your study log to see how far you have come.</li></ul></section>"""

OUTRO = ""

PARTS = [
    ("A", "Part A: Auto-graded questions (25)", "<p>Covers M1–M9. The 8 questions marked [Parallel] test the same points as the pre-test.</p>"),
    ("short", "Part B: Interpretation questions (4)", "<p>Each question gives real output from the course scripts (the course site reads the numbers from <code>R/output/</code> automatically). Write a paragraph in answer, then open the reference answer and score yourself on the four dimensions.</p>"),
    ("C", "Part C: Small R tasks (5)", """<p>Open <code>clpn-course.Rproj</code> in RStudio, run the two lines below, then do each question. Give answers to 3 decimal places (or as whole numbers); tolerance ±0.01.</p>
<pre><code>source("R/_setup.R")
dat &lt;- read_course_data()</code></pre>"""),
]

L = lambda i: f'<a href="../lessons/L{i.replace(".", "-")}.html">{i}</a>'

ITEMS = [
    # ---------------- Part A ----------------
    dict(part="A", obj="1.2-1", q=f"""Q: [Parallel] A domestic violence helpline received 50 calls in one week, 18 of them from older adults. What percentage of the calls came from older adults? (Enter a number only)
N: 36 | 0.5
H: Part ÷ whole × 100.
E: 18 ÷ 50 = 0.36, i.e. 36%. See {L("1.2")}."""),

    dict(part="A", obj="1.2-1", q=f"""Q: [Parallel] Last week four social workers made 3, 5, 6 and 10 home visits. How many home visits did each make on average?
N: 6 | 0.01
H: Add them up, then divide by the number of people.
E: (3 + 5 + 6 + 10) ÷ 4 = 24 ÷ 4 = 6. See {L("1.2")}."""),

    dict(part="A", obj="1.2-1", q=f"""Q: [Parallel] The loneliness scale in the course data has 4 items, each scored 1–4. What is the <b>lowest</b> possible total of the 4 items?
N: 4 | 0
H: Each item scores at least 1.
E: 4 × 1 = 4 (the highest is 16). See {L("1.1")} and {L("1.2")}."""),

    dict(part="A", obj="1.2-1", q=f"""Q: [Parallel] Among the monthly incomes of 7 households in a community, one belongs to a business owner with a very high income. Which number better describes "the income of a typical household in this community"?
- The mean, because it uses all the data || The mean is pulled up by that one extreme household.
+ The median, because it is not affected by a few extreme values || Correct.
- The maximum || The maximum only describes that one household.
- The variance || The variance describes spread, not the "typical level."
E: For choosing between the mean and the median, see {L("1.2")}."""),

    dict(part="A", obj="1.4-4", q=f"""Q: [Parallel] A survey finds that adolescents who exercise more times a week have lower depression scores. Which statement is the most cautious?
- Exercise can treat depression || This is a causal conclusion.
- Depressed adolescents never like exercise || This applies a group trend to every individual.
+ The two are associated, but the relationship may run both ways, or a third factor (such as family support) may affect both || Correct.
- The two are unrelated || The question says they are associated.
E: For "correlation is not causation" and confounders, see {L("1.4")}."""),

    dict(part="A", obj="1.5-1", q=f"""Q: [Parallel] Suppose you really did survey <b>every</b> social worker in the province and found an average of 6.2 years in the job. What is this 6.2 called in statistics?
+ A parameter, because it describes the population || Correct.
- A statistic, because it was calculated || A statistic is calculated from a sample; here the whole population was surveyed.
- A standard error || No.
- An effect size || No.
E: For population vs sample and parameter vs statistic, see {L("1.5")}. Real studies can rarely survey everyone, so we usually estimate population parameters with sample statistics."""),

    dict(part="A", obj="3.1-1", q=f"""Q: [Parallel] What is the statistical method called that predicts an outcome from one or more predictors (as in "linear ____")? (One word)
T: regression||linear regression||regression analysis
H: The topic of Module 3: "____ coefficient," "____ equation."
E: Regression (e.g. linear regression) describes how predictors relate to an outcome. See {L("3.1")}."""),

    dict(part="A", obj="2.4-3", q=f"""Q: [Parallel] You run <code>read.csv("data/clpn_sim_wide.csv")</code> in RStudio and get the error "cannot open file … No such file or directory." What is the most likely cause, and the best fix?
- The computer has a virus; reinstall R || It has nothing to do with viruses.
+ The working directory is not the course folder: open the project by double-clicking <code>clpn-course.Rproj</code>, then read the file with the relative path || Correct.
- The CSV file is damaged; convert it to Excel || Check the path first.
- Change the path to an absolute path on your computer, and edit it again on every new computer || It works, but it is not reproducible; use a Project and relative paths.
E: For RStudio Projects and relative paths, see {L("2.4")}."""),

    dict(part="A", obj="1.3-1", q=f"""Q: Someone scores 35 on a scale with mean 50 and standard deviation 10. What is their z-score?
N: -1.5 | 0.01
H: z = (raw score − mean) ÷ standard deviation.
E: (35 − 50) ÷ 10 = −1.5, i.e. 1.5 standard deviations below the mean. See {L("1.3")}."""),

    dict(part="A", obj="1.5-3", q=f"""Q: A study reports a 95% confidence interval of [2.10, 2.30] for mean loneliness. Which interpretation is correct?
- 95% of participants have loneliness scores between 2.10 and 2.30 || A confidence interval describes uncertainty about the mean, not the range of individual scores.
+ If you sampled again and again with the same method and computed an interval each time, about 95% of the intervals would contain the population mean || Correct.
- The population mean has a 95% probability of being 2.20 || No.
- The sample mean must lie outside the interval || The sample mean sits in the middle of the interval.
E: For the correct interpretation of confidence intervals and common misreadings, see {L("1.5")}."""),

    dict(part="A", obj="1.6-2", q=f"""Q: A test gives p = .03. Which statement is correct?
- The probability that the null hypothesis is true is 3% || This is the most common misreading.
+ If the null hypothesis were true, the probability of a result this extreme (or more extreme) would be about 3% || Correct.
- The finding has a 97% probability of being true || No.
- The effect is very large || A p-value is not an effect size.
E: For the correct interpretation of p-values, see {L("1.6")}."""),

    dict(part="A", obj="1.6-3", q=f"""Q: A survey with N = 20000 finds that men's and women's mean loneliness differ by 0.02 points (on a 4-point scale), p &lt; .001. What is the most appropriate conclusion?
- The gender difference is very important || With a very large sample, even tiny differences become significant.
+ The difference is statistically significant, but the effect size is tiny and probably has little practical meaning || Correct.
- The result was miscalculated || This is common with large samples.
- The sample should be made smaller || No.
E: For statistical significance vs practical meaning (effect size), see {L("1.6")}."""),

    dict(part="A", obj="3.2-1", q=f"""Q: Regression model: depression = 0.5 + 0.30 × loneliness + 0.10 × age. How should the loneliness coefficient 0.30 be interpreted?
+ Among people of the same age, each extra point of loneliness goes with depression 0.30 points higher on average || Correct.
- Loneliness causes depression to rise by 30% || It is neither causal nor a percentage.
- 30% of depression is explained by loneliness || That is the kind of thing you say about R².
- The correlation between loneliness and depression is 0.30 || A partial regression coefficient is not a correlation.
E: For "with the other variables held constant" as the meaning of a partial regression coefficient, see {L("3.2")}."""),

    dict(part="A", obj="3.4-2", q=f"""Q: A logistic regression of "whether someone seeks professional help" gives an odds ratio of OR = 1.5 for social support. What is the most appropriate interpretation?
- People with high social support have a 1.5% probability of seeking help || An OR is not a probability.
+ Each 1-unit increase in social support multiplies the odds of seeking help by 1.5 || Correct.
- Social support causes 50% of people to seek help || No.
- An OR above 1 means a negative relationship || OR &gt; 1 means a positive relationship.
E: For odds and odds ratios, see {L("3.4")}."""),

    dict(part="A", obj="3.5-3", q=f"""Q: What is the purpose of choosing LASSO's λ with k-fold cross-validation?
- To make the model fit the training data as well as possible || That leads to overfitting.
+ To choose the penalty strength with the smallest (or close to the smallest) prediction error on data that were not used for training || Correct.
- To remove missing values || Irrelevant.
- To make all coefficients 0 || No.
E: For λ and k-fold cross-validation, see {L("3.5")}."""),

    dict(part="A", obj="2.2-3", q=f"""Q: For the vector <code>x &lt;- c(2, NA, 4)</code>, what does <code>mean(x)</code> return?
- 3 || By default, missing values are not skipped.
+ NA || Correct. To get 3, write <code>mean(x, na.rm = TRUE)</code>.
- 2 || No.
- An error, and the code stops || There is no error; it returns NA.
E: For NA and <code>na.rm = TRUE</code>, see {L("2.2")}."""),

    dict(part="A", obj="4.2-1", q=f"""Q: A dataset with 300 people and 4 waves is converted from wide format (one row per person) to long format (one row per person per wave). How many rows are there?
N: 1200 | 0
H: One row per person per wave.
E: 300 × 4 = 1200. See {L("4.2")}."""),

    dict(part="A", obj="4.3-1", q=f"""Q: In a panel study, whether participants drop out at Wave 2 depends on how depressed they <b>actually</b> were at Wave 2 (the more depressed, the less willing to respond), even after controlling for the Wave 1 information. What kind of missingness is this?
- MCAR || It is not completely random.
- MAR || Under MAR, missingness depends only on observed variables.
+ MNAR (missing not at random) || Correct. Missingness depends on the unobserved values themselves; FIML and multiple imputation cannot fully solve this, so a sensitivity analysis is needed.
- No missing data || There are missing data.
E: For the three missingness mechanisms, see {L("4.3")}."""),

    dict(part="A", obj="5.3-1", q=f"""Q: What is the core criticism of the traditional CLPM by Hamaker et al. (2015)?
- A CLPM needs too many waves || No.
+ A CLPM mixes stable differences between people (between-person) with change within people (within-person), so the cross-lagged coefficients can mislead conclusions about "processes within individuals" || Correct.
- A CLPM cannot estimate autoregression || A CLPM does estimate autoregression.
- A CLPM can only be used with two variables || That is not the core criticism.
E: See {L("5.3")}. The RI-CLPM uses random intercepts to separate the two."""),

    dict(part="A", obj="6.2-3", q=f"""Q: From which matrix can the partial correlations of a GGM be computed directly?
- The raw data matrix || You first need the covariance matrix.
+ The inverse of the covariance matrix (the precision matrix) || Correct.
- The identity matrix || No.
- The vector of means || No.
E: For how the precision matrix relates to partial correlations, see {L("6.2")} (for background only)."""),

    dict(part="A", obj="6.5-3", q=f"""Q: When you study the "comorbidity" of loneliness and depression, which edges does bridge expected influence (bridge EI) count?
- All edges || That is ordinary EI.
+ Edges that connect different constructs (loneliness ↔ depression) || Correct.
- Edges within the same construct || Exactly the opposite.
- Autoregressive edges || No.
E: For bridge centrality, see {L("6.5")} (Jones et al., 2021)."""),

    dict(part="A", obj="7.1-4", q=f"""Q: A CLPN weights matrix is stored as <code>B[k, j]</code> = "k at T1 → j at T2." <code>B["dep4", "lone2"]</code> is negative. What does this mean?
- Feeling left out at T1 predicts lower fatigue at T2 || The direction is read backwards.
+ Controlling for all T1 nodes, people with higher fatigue (dep4) at T1 tend to score <b>lower</b> on "Feeling left out" (lone2) at T2 || Correct. A negative edge is a predictive relationship in the opposite direction.
- The two are unrelated || The coefficient is not 0.
- Fatigue causes feeling left out to decrease || It is not causal.
E: For reading CLPN edges, see {L("7.1")} and {L("7.3")}."""),

    dict(part="A", obj="7.5-1", q=f"""Q: You estimate separate CLPNs for T1→T2 and T2→T3 and find that the edges of the two networks correlate at .64. What does this mainly tell you?
- The two networks are identical || .64 means similar, but not identical.
+ The network structure replicates to some extent, but a given edge (especially a weak one) does not necessarily appear in both intervals, so interpret single edges with caution || Correct.
- 64% of the edges are causal relationships || No.
- The data of the second interval are faulty || Not necessarily.
E: For multi-wave data and how well the structure replicates, see {L("7.5")}."""),

    dict(part="A", obj="8.3-2", q=f"""Q: A study reports a CS-coefficient of 0.36 for in-EI. By the usual standards, how should the in-EI ranking be treated?
- Very stable; you can safely make it a main conclusion || It should preferably be above 0.5.
+ Just acceptable (0.25–0.5): report it, but interpret the ranking only cautiously and as a pointer || Correct.
- It must not be reported at all || Report it honestly; only the interpretation needs to be cautious.
- The CS-coefficient has nothing to do with the ranking || The CS-coefficient describes exactly how stable the ranking is.
E: For the reference values of the CS-coefficient, see {L("8.3")}."""),

    dict(part="A", obj="9.2-1", q=f"""Q: Which sentence does <b>not</b> over-interpret?
- "'No one understands me' has the highest out-EI, so it is the root through which loneliness triggers depression." || Causal.
- "With every client, 'No one understands me' should be dealt with first." || Applies a group result to individuals.
+ "'No one understands me' has the highest out-EI (but its stability is insufficient), which suggests it predicts more of the other symptoms over time and is worth testing in future studies." || Correct.
- "Intervening on 'No one understands me' will lower symptoms across the whole network." || Observational data cannot support an intervention conclusion.
E: For common over-interpretations, see {L("9.2")}."""),

    # ---------------- Part C (answers from R/output/assess_answers.csv) ----------------
    dict(part="C", obj="2.5-1", q=f"""Q: C1: What is the mean of <code>lone1_t1</code> (Lack of companionship) at Wave 1? (3 decimal places)
N: {ANS["C1"]} | 0.01
H: <code>mean(dat$lone1_t1)</code>
E: The reference answer is computed by <code>R/assess_answers.R</code>. For the mean, see {L("1.2")} and {L("2.5")}."""),

    dict(part="C", obj="2.5-2", q=f"""Q: C2: What is the Pearson correlation between <code>lone3_t1</code> (Feeling isolated) at T1 and <code>dep1_t2</code> (Depressed mood) at T2? (3 decimal places)
N: {ANS["C2"]} | 0.01
H: <code>cor(dat$lone3_t1, dat$dep1_t2)</code>
E: The reference answer is computed by <code>R/assess_answers.R</code>. For correlation, see {L("1.4")} and {L("2.5")}. Note that this is a simple correlation, not a CLPN edge: a CLPN edge controls for all T1 nodes."""),

    dict(part="C", obj="2.3-2", q=f"""Q: C3: How many women (<code>gender == 1</code>) are in the data?
N: {ANS["C3"]} | 0
H: <code>sum(dat$gender == 1)</code> or <code>table(dat$gender)</code>
E: The reference answer is computed by <code>R/assess_answers.R</code>. For logical conditions and counting, see {L("2.2")} and {L("2.3")}."""),

    dict(part="C", obj="1.2-1", q=f"""Q: C4: What is the standard deviation of <code>dep1_t1</code> at Wave 1? (3 decimal places)
N: {ANS["C4"]} | 0.01
H: <code>sd(dat$dep1_t1)</code>
E: The reference answer is computed by <code>R/assess_answers.R</code>. For the standard deviation, see {L("1.2")}."""),

    dict(part="C", obj="7.2-4", q=f"""Q: C5: Estimate the T1 → T2 CLPN with the course function, using the EBIC rule for λ (no cross-validation, so the result is fixed): <code>B &lt;- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], rule = "ebic")</code>. Leaving out the autoregressive edges, how many cross-lagged edges are nonzero?
N: {ANS["C5"]} | 0
H: <code>sum(cl_only(B) != 0)</code>: <code>cl_only()</code> sets the diagonal to 0.
E: The reference answer is computed by <code>R/assess_answers.R</code>. For nodewise estimation and the weights matrix, see {L("7.2")}; the EBIC rule gives a sparser network than <code>lambda.min</code>."""),
]

_DIMS = lambda k1, k2, k3, k4: [
    ("Correct conclusion", 4, k1),
    ("Cites the correct numbers and intervals", 3, k2),
    ("Reads the direction and B[k, j] correctly", 2, k3),
    ("No causal or individual-level over-interpretation", 1, k4),
]

_IMG = lambda f, alt: f'<p><img src="../R/output/{f}" alt="{alt}" style="max-width:100%"></p><p class="muted">Figure: <a href="../R/output/{f}">R/output/{f}</a></p>'

SHORT = [
    dict(
        obj="7.3-4",
        q="<p><b>B1 (Reading edges)</b> In the T1 → T2 CLPN of the course data (<code>R/L7-2.R</code>, <code>lambda.min</code>, {{V:fx_n_cl}} nonzero cross-lagged edges in total), the loneliness → depression edge with the largest absolute value is <code>B[\"{{V:fx_ld_from}}\", \"{{V:fx_ld_to}}\"]</code> = {{V:fx_ld_b}} ({{V:fx_ld_from_zh}} → {{V:fx_ld_to_zh}}), and the depression → loneliness edge with the largest absolute value is <code>B[\"{{V:fx_dl_from}}\", \"{{V:fx_dl_to}}\"]</code> = {{V:fx_dl_b}} ({{V:fx_dl_from_zh}} → {{V:fx_dl_to_zh}}). In 3–4 sentences, write an interpretation of these two edges for a paper.</p>"
        + _IMG("L7-3_clpn.png", "CLPN network plot of the course data from T1 to T2: 9 nodes (4 loneliness items, 5 depression items); arrows are cross-lagged edges, with positive and negative edges in different colors and thicker lines for stronger edges; autoregressive edges are not drawn"),
        answer="<p>Example: \"Controlling for all 9 items at T1, participants who scored higher on '{{V:fx_ld_from_zh}}' at T1 tended to score higher on '{{V:fx_ld_to_zh}}' at T2 (B = {{V:fx_ld_b}}); this is the strongest edge in the loneliness → depression direction. In the opposite direction, participants who scored higher on '{{V:fx_dl_from_zh}}' at T1 tended to score slightly lower on '{{V:fx_dl_to_zh}}' at T2 (B = {{V:fx_dl_b}}), a negative edge. Both are small predictive relationships over time; they cannot be interpreted as causal effects, nor do they represent a change process within each individual. Their stability has to be judged together with the bootstrap results (Lesson 8.2).\"</p>",
        dims=_DIMS(
            "Gets the meaning and the sign of both edges right",
            "Gives both B values",
            "Reads both edges as row node at T1 → column node at T2",
            "No wording such as \"causes\" or \"everyone will\"",
        ),
    ),
    dict(
        obj="8.2-2",
        q="<p><b>B2 (Edge accuracy)</b> Results of the 1000 bootstrap samples in <code>R/L8-2.R</code>: lone4 → dep4 has an estimate of {{V:b8_lone4>dep4_sample}}, a bootstrap interval of [{{V:b8_lone4>dep4_q2.5}}, {{V:b8_lone4>dep4_q97.5}}], and is 0 in a proportion {{V:b8_lone4>dep4_prop0}} of the resamples; lone3 → dep1 has an estimate of {{V:b8_lone3>dep1_sample}}, an interval of [{{V:b8_lone3>dep1_q2.5}}, {{V:b8_lone3>dep1_q97.5}}], and is 0 in a proportion {{V:b8_lone3>dep1_prop0}} of the resamples. In addition, the difference tests comparing the 10 strongest cross-lagged edges pair by pair were {{V:b8_diff_text}}. The course data are simulated, so the population targets of both edges are known: lone4 → dep4 = {{V:pop_lone4>dep4}}, lone3 → dep1 = {{V:pop_lone3>dep1}}. Write 3–5 sentences: From the bootstrap alone, can you tell which edge is more reliable? Can you say that \"lone4 → dep4 is stronger than all the other strong edges\"? Compared with the population targets, what does the bootstrap tell you, and what does it not tell you?</p>"
        + _IMG("L8-2_edge_ci.png", "Bootstrap intervals of the cross-lagged edges: each row is one edge, the dot is the original-sample estimate, the horizontal line is the bootstrap interval, and the vertical dashed line is 0"),
        answer="<p>Example: \"The two edges are about equally stable under resampling: the proportions of resamples in which they were shrunk to 0 are {{V:b8_lone4>dep4_prop0}} and {{V:b8_lone3>dep1_prop0}}, and their lower interval limits are {{V:b8_lone4>dep4_q2.5}} and {{V:b8_lone3>dep1_q2.5}}, both close to 0. From the bootstrap alone, you cannot tell which is more reliable. The difference tests between the strongest edges were {{V:b8_diff_text}}, so you also cannot say that lone4 → dep4 is 'stronger' than the other strong edges. Compared with the population targets, the picture is actually reversed: lone4 → dep4 is almost 0 in the population ({{V:pop_lone4>dep4}}), while lone3 → dep1 is the strongest loneliness → depression edge in the population target ({{V:pop_lone3>dep1}}). The bootstrap only reflects sampling variation around the estimate from this sample; it cannot show whether an edge exists in the population. Because LASSO shrinks estimates toward 0, these intervals also cannot be treated as strict 95% confidence intervals.\"</p>",
        dims=_DIMS(
            "The two edges are about equally stable under the bootstrap and cannot be ranked; lone4 → dep4 cannot be called stronger than the other strong edges; being stable in the bootstrap does not mean an edge exists in the population",
            "Cites both edges' proportions of zeros or intervals, the difference test result, and both population targets",
            "Gets the direction of both edges right",
            "Does not treat the intervals as strict confidence intervals; no causal claims",
        ),
    ),
    dict(
        obj="8.3-3",
        q="<p><b>B3 (Centrality and stability)</b> In <code>R/L7-4.R</code>, the node with the highest out-EI is {{V:fx_out_top}} ({{V:fx_out_top_zh}}, {{V:fx_out_top_v}}) and the node with the highest in-EI is {{V:fx_in_top}} ({{V:fx_in_top_zh}}, {{V:fx_in_top_v}}). The CS-coefficients from <code>R/L8-3.R</code> are: out-EI = {{V:cs8_out}}, in-EI = {{V:cs8_in}}. Write a paragraph (3–5 sentences) reporting the centrality results for a paper, including how to interpret the two rankings.</p>"
        + _IMG("L8-3_casedrop.png", "Case-dropping bootstrap plot: the horizontal axis is the proportion of the sample dropped, the vertical axis is the correlation of the centrality ranking with the original sample's; the out-EI line falls faster than the in-EI line"),
        answer="<p>Example: \"'{{V:fx_in_top_zh}}' had the highest in-EI ({{V:fx_in_top_v}}), i.e. it was the item most easily predicted by the other items at T1; the stability of in-EI just reached an acceptable level (CS = {{V:cs8_in}}), so its ranking can be interpreted with caution. '{{V:fx_out_top_zh}}' had the highest out-EI ({{V:fx_out_top_v}}), but the CS of out-EI was only {{V:cs8_out}}, below 0.25, so the ranking is unstable, and this study does not interpret the out-EI ranking. High centrality only reflects predictive relationships over time; it does not establish a node as a 'core symptom' or the best intervention target.\"</p>",
        dims=_DIMS(
            "in-EI can be interpreted with caution; the out-EI ranking is not interpreted",
            "Gives both nodes' values and both CS-coefficients, and compares them with 0.25 / 0.5",
            "out-EI = predicting others, in-EI = being predicted by others, not reversed",
            "No \"core symptom\" or \"intervening on it will ...\" wording",
        ),
    ),
    dict(
        obj="9.3-2",
        q="<p><b>B4 (Sensitivity analysis)</b> In the capstone example (<code>R/L10-2.R</code>), the main analysis (<code>lambda.min</code>) has {{V:fx_sens_main_n}} nonzero cross-lagged edges. Sensitivity analyses: with <code>lambda.1se</code> only {{V:fx_sens_1se_n}} remain, and their edges correlate with the main analysis at r = {{V:fx_sens_1se_r}}; with gender and age added as covariates, r = {{V:fx_sens_cov_r}}; re-estimated with the T2 → T3 data, there are {{V:fx_sens_rep_n}} nonzero edges, correlating with the main analysis at r = {{V:fx_sens_rep_r}}. Write a 4–5 sentence paragraph reporting the sensitivity analysis results.</p>",
        answer="<p>Example: \"With gender and age added as covariates, the network hardly changed (edge correlation with the main analysis r = {{V:fx_sens_cov_r}}). With the more conservative <code>lambda.1se</code>, the number of nonzero cross-lagged edges fell from {{V:fx_sens_main_n}} to {{V:fx_sens_1se_n}} (r = {{V:fx_sens_1se_r}}), showing that many weak edges depend on the λ rule and only the stronger edges are kept under both rules. Re-estimated with the T2 → T3 data, the edge correlation was r = {{V:fx_sens_rep_r}}: the overall structure replicates to some extent, but individual weak edges do not necessarily reappear. We therefore focus the interpretation on edges kept under both rules whose bootstrap intervals exclude 0; these sensitivity analyses cannot remove design limitations such as the mixing of between-person and within-person effects.\"</p>",
        dims=_DIMS(
            "Covariates make little difference; weak edges depend on the λ rule; the structure partly replicates",
            "Gives the 3 r values and the edge counts",
            "Makes clear that the comparison is of cross-lagged edges (T1 → T2 / T2 → T3) and does not call T2 → T3 \"another sample\"",
            "Does not treat replication as evidence of causation",
        ),
    ),
]
