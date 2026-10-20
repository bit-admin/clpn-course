# -*- coding: utf-8 -*-
L["7.7"] = dict(
lead=r"""<p>Social work research often asks whether two groups are the same: do men and women, urban and rural residents, people who received a service and people who did not, have the same loneliness–depression network? This lesson answers that question with a permutation test (shuffle the group labels and re-estimate the networks).</p>""",
h_intuition="Shuffling: if the grouping doesn't matter, shuffling the labels changes nothing",
intuition=r"""
<h3>1. First, state the question clearly</h3>
<p>“Are the networks of men and women the same?” is too vague. When you compare two CLPNs (the coefficient matrix \(B^{(1)}\) of group 1 and \(B^{(2)}\) of group 2), you usually ask three more specific questions (van Borkulo et al., 2023):</p>
""" + TABLE(["Question", "Statistic", "What it answers"], [
["① Is there any edge that differs a lot?", T("network structure invariance test") + "; statistic <b>M</b> = the largest absolute difference among the 72 cross-lagged edges", "Whether the overall “shape” of the two networks differs"],
["② Are the networks equally tightly connected overall?", T("global strength invariance test") + "; statistic <b>S</b> = the difference between the two groups' sums of absolute cross-lagged edge weights", "Whether the symptoms are, overall, equally interconnected in the two groups"],
["③ Is one particular edge the same?", T("edge invariance test") + "; the difference for each edge", "For example, “does the loneliness item Feeling isolated predict later Depressed mood differently in men and women?”"]]) + r"""
<p>The three questions share one null hypothesis: the data of both groups come from the same population (so their population networks are also the same), and the differences between the samples are due only to sampling. Strictly speaking, the permutation test tests “the two groups' data have the same distribution,” which is stronger than “the networks are the same”: differences in means, variances, or skewness between the groups can also make M or S significant.</p>

<h3>2. Why you can't just compare the plots by eye</h3>
<p>If you estimate a separate CLPN for men and for women, the two plots will certainly differ. When the course data were generated, both genders used the same lagged coefficients; only women's continuous depression scores were raised by 0.2 before being cut into 0–3 categories. Because the shift happened before the cutting, the networks on the observed scale may differ very slightly; below we treat the two groups as having “the same generating network.” Estimated separately, the edge that differs most is {{V:pg1_M_from}} → {{V:pg1_M_to}}: men {{V:pg1_M_b1}}, women {{V:pg1_M_b2}}. Someone looking at the plots might well say “this edge exists only in men,” but with only about 400 people per group, it is quite ordinary for a weak edge to be kept in one group and shrunk to 0 in the other. So the question to ask is: is the observed difference larger than the differences you would usually see if the two groups were really the same and people had just been split at random?</p>

<h3>3. Shuffling: building a world where the two groups are the same</h3>
""" + KEY("The logic of a permutation test", r"""<ol><li>Compute the statistic for the real grouping, e.g., M.</li>
<li>If gender really has nothing to do with the network, the """ + T("group label") + r""" (“who is a man, who is a woman”) can be swapped freely. Shuffle the labels of the 800 people (keeping the group sizes), split them into two groups again, estimate a CLPN for each, and compute M again.</li>
<li>Repeat 1000 times to get 1000 values of M for a world where the two groups are the same: the """ + T("null distribution") + r""".</li>
<li>The proportion of shuffled M values that are ≥ the real M is the permutation p-value.</li></ol>""") + r"""
<p>Compare this with the bootstrap of Lesson 8.1: the bootstrap resamples cases with replacement and answers “how unstable is this estimate?”, giving an interval; a permutation shuffles labels and answers “would we see a difference this large if the two groups were the same?”, giving a p-value. Both replace formulas with repeated computation, so the """ + T("permutation test") + r""" needs almost no distributional assumptions and works for statistics like those of a CLPN, for which formulas are hard to derive. The figure in the R Code section draws the null distributions of the three data sets as histograms, with a red line at the observed M: if the red line falls within the bulk of the histogram, such a difference is common under the null hypothesis; if it falls beyond the right tail, it is rare.</p>

<h3>4. Results for three data sets</h3>
""" + TABLE(["Data", "People per group", "M (permutation p)", "S (permutation p)", "lone3 → dep1 single-edge p", "Of 72 edges, unadjusted p &lt; .05", "After Holm correction"], [
["① Course data: men vs. women (no real difference)", "{{V:pg1_n1}} / {{V:pg1_n2}}", "{{V:pg1_M}} ({{V:pg1_p_M}})", "{{V:pg1_S}} ({{V:pg1_p_S}})", "{{V:pg1_p_lone3_dep1}}", "{{V:pg1_edges_p05}} edges", "{{V:pg1_edges_holm05}} edges"],
["② Simulation: group 2 lone3 → dep1 +0.20", "{{V:pg2_n1}} / {{V:pg2_n2}}", "{{V:pg2_M}} ({{V:pg2_p_M}})", "{{V:pg2_S}} ({{V:pg2_p_S}})", "{{V:pg2_p_lone3_dep1}}", "{{V:pg2_edges_p05}} edges", "{{V:pg2_edges_holm05}} edges"],
["③ Simulation: same difference, half the people", "{{V:pg3_n1}} / {{V:pg3_n2}}", "{{V:pg3_M}} ({{V:pg3_p_M}})", "{{V:pg3_S}} ({{V:pg3_p_S}})", "{{V:pg3_p_lone3_dep1}}", "{{V:pg3_edges_p05}} edges", "{{V:pg3_edges_holm05}} edges"]]) + r"""
<p class="muted" style="font-size:.88rem">Source: R/output/L7-7_perm_summary.csv ({{V:pg1_nperm}} permutations per data set).</p>
<ul><li><b>① No real difference:</b> neither M nor S is significant, which matches the truth. The 95th percentile of the null distribution of M is {{V:pg1_M_q95}}, and the observed {{V:pg1_M}} is still below it. The edge that “exists only in men” in the previous section is a random difference of exactly this size.</li>
<li><b>② A real difference, enough people:</b> M is significant (p = {{V:pg2_p_M}}), and the edge that differs most is the one that was changed, {{V:pg2_M_from}} → {{V:pg2_M_to}} (group 1 {{V:pg2_M_b1}}, group 2 {{V:pg2_M_b2}}). S, however, is not significant: only one edge changed, so the total strength is hardly affected. M and S answer different questions and cannot stand in for each other.</li>
<li><b>③ The same difference, half the people:</b> M is no longer significant (p = {{V:pg3_p_M}}), and the edge that differs most is now {{V:pg3_M_from}} → {{V:pg3_M_to}}, an edge that is the same in both groups. The real difference is drowned out by noise.</li></ul>
<p>The 600 and 300 people per group were picked for the demonstration, not as recommended sample sizes; ② and ③ are each a single generated data set (seeds 2027 and 2028), and with another seed the results could be reversed. """ + T("Statistical power") + r""" has to be estimated with repeated simulations as in Lesson 7.6 (hundreds of data sets × thousands of permutations each, not done in this lesson). From ② and ③ you can only draw a qualitative conclusion: the same difference is more easily drowned out by noise when there are fewer people.</p>
""" + WARN("Not significant ≠ the same", "The two groups in ③ really are different, yet the test did not find it. A nonsignificant network comparison can only be reported as “we found no evidence that the two networks differ.” Group comparisons usually have low power: each group is only part of the total sample, yet the network has dozens of edges to estimate.") + r"""

<h3>5. Single-edge tests and multiple comparisons</h3>
<p>If you compare all 72 edges one by one, each at p &lt; .05, then even if the two groups are exactly the same, on average 72 × 0.05 ≈ 3.6 edges will be “significant.” Course data ① has exactly {{V:pg1_edges_p05}}, among them lone3 → dep1 (men {{V:pg1_l3d1_b1}}, women {{V:pg1_l3d1_b2}}) with p of only {{V:pg1_p_lone3_dep1}}. Both genders were generated with the same coefficient for this edge, so it is very likely just the smallest of 72 tests (in Exercise 2, with the T2 → T3 data, it is no longer significant). This is the """ + T("multiple comparisons") + r""" problem from Lesson 1.6. Two remedies:</p>
<ol><li><b>Correct:</b> for example with the """ + T("Holm correction") + r""". The smallest possible permutation p-value is 1 / (B + 1) (B = number of permutations), which is {{V:pg_pmin}} with 1000 permutations; multiplied by 72 it is at least {{V:pg_holm_min}}, which is why the “after Holm correction” column shows 0 everywhere. For a corrected p to have any chance of falling below .05, you need B + 1 &gt; 72 / .05 = 1440, and in practice far more, e.g., 10000 (derivation in Essential Math); the run time of each part then goes from about 1 minute to about 7–10 minutes.</li>
<li><b>Specify in advance:</b> before looking at the data, write 1–2 theoretically motivated edges into your analysis plan (Lesson 10.1) and test only those. A """ + T("pre-specified hypothesis") + r""" pays no price for the edges you don't test: in ③, for example, M is not significant, but the pre-specified single-edge test of lone3 → dep1 gives p = {{V:pg3_p_lone3_dep1}}. Only what you wrote down beforehand counts: “specifying” the most significant edge after seeing the results takes you right back into the multiple-comparisons trap.</li></ol>

<h3>6. Why λ is chosen by EBIC here</h3>
<p>Each permutation needs a CLPN for each of the two groups (18 LASSO regressions), so 1000 permutations mean 18,000 regressions. The course default, <code>lambda.min</code>, needs 10-fold cross-validation, which would take about 12 minutes per part, and the random fold splits would add another layer of noise to every estimate. So this lesson uses <code>clpn_estimate(rule = "ebic")</code> (introduced in Lesson 7.2): no cross-validation, exactly the same result every time for the same data, about 45 seconds per part. What matters is that the real grouping and every shuffle use the same rule; the rule affects the power and the conclusions of the test, so state it in the paper.</p>

<h3>7. NCT: a ready-made tool for cross-sectional networks</h3>
<p>The R package """ + T("NetworkComparisonTest", "NCT; R package, for awareness") + r""" (van Borkulo et al., 2023) wraps the M, S, and single-edge tests above into one function and is often used to compare the cross-sectional networks of two groups (the GGM of Lesson 6.2). The course does not install it; the code below is for illustration only:</p>
""" + CODE(r"""
# install.packages("NetworkComparisonTest")    # not installed by the course; illustration only
library(NetworkComparisonTest)
dat <- read_course_data()
men   <- dat[dat$gender == 0, vars_t(1)]       # the 9 items at wave 1: a cross-sectional network
women <- dat[dat$gender == 1, vars_t(1)]
nct <- NCT(men, women, it = 1000, test.edges = TRUE, edges = "all",
           p.adjust.methods = "holm")
nct$nwinv.pval      # permutation p for M (network structure)
nct$glstrinv.pval   # permutation p for S (global strength)
nct$einv.pvals      # p for each edge (Holm-corrected)
""", "Illustration only: comparing men's and women's T1 cross-sectional networks with NCT (not run by the course scripts)") + r"""
<p>By default NCT estimates an undirected network (partial correlations) within one time point, whereas a CLPN is a directed T1 → T2 regression network; conclusions from one cannot be carried over to the other. Newer versions of NCT accept a custom estimation function, but directed edges and whether to include the autoregressions need careful setup; the hand-written permutation test of this lesson is easier to check step by step. Also, shuffling assumes the two groups are different people; you cannot shuffle like this to compare the T1 → T2 and T2 → T3 networks of the same people (NCT has a paired option, <code>paired = TRUE</code>; paired comparisons of CLPNs are beyond this lesson).</p>
""" + NOTE("Social work perspective: the ethics of group comparisons", "When you compare groups defined by gender, ethnicity, household registration status (hukou, China's residence registration), and the like, any difference is at the level of group averages and does not apply to any one person; not finding a difference does not mean there is none. When you report, avoid presenting a statistical difference as a “characteristic” of a group, so as not to reinforce stereotypes.") + r"""
""",
h_math="The three statistics and the permutation p-value",
math=r"""
""" + MATH(r"M=\max_{k\neq j}\big|\hat\beta^{(1)}_{kj}-\hat\beta^{(2)}_{kj}\big|,\qquad S=\Big|\sum_{k\neq j}\big|\hat\beta^{(1)}_{kj}\big|-\sum_{k\neq j}\big|\hat\beta^{(2)}_{kj}\big|\Big|,\qquad D_{kj}=\hat\beta^{(1)}_{kj}-\hat\beta^{(2)}_{kj}") + SYM([
(r"\(\hat\beta^{(1)}_{kj}\)", "Estimated CLPN coefficient of group 1: k at T1 → j at T2"),
(r"\(\max_{k\neq j}\)", "The maximum over all 72 cross-lagged edges (autoregressions excluded)"),
(r"\(\sum_{k\neq j}|\cdot|\)", "The sum of the absolute values of the 72 cross-lagged edges: the overall connection strength of the network"),
(r"\(D_{kj}\)", "The difference for a single edge; the test uses its absolute value"),
]) + r"""
<h4>The permutation p-value</h4>
""" + MATH(r"p=\frac{\#\{b:\ M^{*}_b\ \ge\ M_{\text{obs}}\}+1}{B+1}") + SYM([
(r"\(M^{*}_b\)", "M computed after the b-th shuffle of the labels"),
(r"\(M_{\text{obs}}\)", "M observed with the real grouping"),
(r"\(B\)", "Number of permutations ({{V:pg1_nperm}} in this lesson)"),
(r"\(+1\)", "Counts the observed data as one possible grouping; this way p is never 0, and its minimum is 1/(B+1)"),
]) + r"""
<p>S and the p-value of each edge are computed the same way (a single edge compares \(|D^{*}_{kj}|\) with \(|D_{kj}|\)).</p>
<h4>Holm correction</h4>
<p>Sort the m p-values from smallest to largest, \(p_{(1)}\le p_{(2)}\le\dots\le p_{(m)}\), and multiply the i-th by \(m-i+1\) (making sure the corrected values do not decrease with i and do not exceed 1). The smallest p is multiplied by m = 72. That is why, with 1000 permutations, the Holm-corrected p is at least 72 / 1001 ≈ {{V:pg_holm_min}}. In R: <code>p.adjust(p, "holm")</code>.</p>
<p>This gives a lower bound on the number of permutations: the smallest possible p is \(1/(B+1)\); for it to stay below α after multiplying by m, you need \(B + 1 > m/\alpha\). With m = 72 and α = .05, m/α = 1440. Just exceeding it is not enough, because the p-values need enough resolution, so in practice B should be far larger, e.g., B ≥ 10000.</p>
<h4>Why shuffling represents the null hypothesis</h4>
<p>If the data of the two groups come from the same population (so the networks are also the same) and each person's data are drawn independently, then which group a person belongs to carries no information about the network. Any shuffling of the labels gives data that are “just as likely” as the real data (the statistical term is exchangeability). So the distribution of the statistic over shuffles is the distribution of the statistic under the null hypothesis.</p>
""",
code=CODE(r"""
source("R/_setup.R"); library(glmnet)
dat <- read_course_data()
est <- function(d) clpn_estimate(d[, vars_t(1)], d[, vars_t(2)], rule = "ebic")
off <- matrix(TRUE, 9, 9); diag(off) <- FALSE            # positions of the cross-lagged edges
stats <- function(B1, B2) {
  D <- B1 - B2
  list(M = max(abs(D[off])), S = abs(sum(abs(B1[off])) - sum(abs(B2[off]))), D = D)
}
perm_test <- function(d, grp, nperm = 1000) {
  obs <- stats(est(d[grp == 0, ]), est(d[grp == 1, ]))   # the real grouping
  nullM <- nullS <- numeric(nperm); exceedD <- matrix(0, 9, 9)
  for (b in seq_len(nperm)) {
    g <- sample(grp)                                     # shuffle: permute the group labels, group sizes unchanged
    s <- stats(est(d[g == 0, ]), est(d[g == 1, ]))
    nullM[b] <- s$M; nullS[b] <- s$S
    exceedD <- exceedD + (abs(s$D) >= abs(obs$D))
  }
  list(pM = (sum(nullM >= obs$M) + 1) / (nperm + 1),     # permutation p-value
       pS = (sum(nullS >= obs$S) + 1) / (nperm + 1),
       pD = (exceedD + 1) / (nperm + 1))                 # permutation p for each edge
}
set.seed(2026)
rA <- perm_test(dat, dat$gender)
p.adjust(rA$pD[off], "holm")                             # Holm correction over all 72 edges
""", "Core of R/L7-7.R (simplified)") + r"""
<p><b>Notes:</b> <code>sample(grp)</code> randomly reorders the group vector: the numbers of men and women stay the same, only who is a man and who is a woman is shuffled. <code>exceedD</code> is a 9 × 9 count matrix that records, for each edge, how often a shuffle produced a difference as large or larger. The full script also prints the 6 edges that differ most and applies the correction with <code>p.adjust(…, "holm")</code>; its comparisons use a small tolerance, <code>- 1e-12</code>, so that floating-point error doesn't turn “equal” into “less than.”</p>
""" + OUT(RLOG("L7-7_log.txt", "===== Part 1", end="Elapsed time"), "Actual output excerpt from R/output/L7-7_log.txt (Part 1)") + r"""
<p>Columns: <code>B_g1</code> and <code>B_g2</code> are the two groups' coefficients, <code>diff</code> = group 1 − group 2, <code>p</code> is the single-edge permutation p, and <code>p_holm</code> is the p after Holm correction over all 72 edges.</p>
""" + OUT(RLOG("L7-7_log.txt", "===== Part 2", end="Elapsed time"), "Actual output excerpt from R/output/L7-7_log.txt (Part 2)") + OUT(RLOG("L7-7_log.txt", "Note: With 1000 permutations", 2), "Actual output excerpt from R/output/L7-7_log.txt (Note)") + r"""
<p><b>Run time:</b> about 2–4 minutes on one core (3 parts × {{V:pg1_nperm}} permutations, about 45 seconds to 1 minute per part). With <code>set.seed()</code> fixed and no cross-validation in EBIC, the results are reproducible to the last digit. For a quicker run, set <code>NPERM</code> to 200; the p-values become coarser (the minimum is then 1/201).</p>""",
quiz=[
("Why does a permutation test shuffle the group labels?", ["To make the two groups the same size", "To build the distribution of the statistic for a world where grouping has nothing to do with the network (the null distribution), and see whether the observed value is rare", "To estimate a confidence interval for each edge, like the bootstrap", "To check whether the estimates depend on the random seed"], 1,
 ["Shuffling keeps the group sizes unchanged; size is not the point.", "Correct.", "That is what the bootstrap is for (resampling cases with replacement); a permutation shuffles labels and gives a p-value.", "The seed only affects whether results can be reproduced; shuffling is about getting the distribution under the null hypothesis."]),
("In 1000 permutations, 81 give an M ≥ the observed M. What is the permutation p-value?", ["81 / 1000", "(81 + 1) / (1000 + 1)", "(1000 − 81) / 1000", "1 / 1001"], 1,
 ["You also have to count the observed data itself: (81 + 1) / (1000 + 1).", "Correct: (81 + 1) / 1001, about 0.08.", "That is the proportion “smaller than the observed value”: the wrong direction.", "That is the smallest possible p with 1000 permutations, which you get only if no shuffle is ≥ the observed value."]),
("In simulation ②, M is significant and S is not. What does that tell you?", ["The test was done wrong", "The edge that differs most stands out, but S finds no difference: one edge's change is a small share of the total strength, so the S test is not sensitive to it; M and S answer different questions", "S is more reliable than M", "The two groups are exactly the same"], 1,
 ["This is exactly what the simulation was designed to show: change only one edge, and M detects it while S is insensitive.", "Correct.", "Neither is more reliable; they answer different questions.", "A significant M says the groups differ in at least one edge."]),
("A comparison of two groups' networks is not significant. What is the most appropriate way to write it?", ["The two groups' networks are the same", "We found no evidence that the two groups' networks differ; the comparison may lack power", "Gender has no effect on the network", "The result is not worth reporting"], 1,
 ["Not significant ≠ the same: the two groups in simulation ③ really differ, yet the test did not find it.", "Correct.", "This treats “not found” as “not there,” and also stretches a network comparison into “the effect of gender.”", "Negative results should be reported too, along with the limits of the power."]),
("Testing the 72 edges one by one, the course data (both groups generated with the same lagged coefficients) have {{V:pg1_edges_p05}} edges with unadjusted p &lt; .05. What is the most reasonable explanation?", ["Gender really affects these edges", "Multiple comparisons: of 72 tests, about 3.6 on average reach p &lt; .05 by chance", "The EBIC rule went wrong", "You should try another random seed"], 1,
 ["Both genders were generated with the same lagged coefficients; only the means of the depression items differ.", "Correct.", "The real grouping and every shuffle use the same EBIC rule; chance “significance” comes from the number of tests, not from the rule.", "Changing the seed to pick results is p-hacking, and it does not solve the multiple-comparisons problem either."]),
("Why not just use NCT to compare two groups' CLPNs?", ["NCT is commercial software", "By default NCT compares undirected networks within one time point (GGMs), whereas a CLPN is a directed T1 → T2 regression network; also, paired data cannot be shuffled freely", "NCT cannot do permutation tests", "NCT works only with binary variables"], 1,
 ["It is an open-source R package, available from CRAN.", "Correct.", "Permutation tests (M, S, and single edges) are exactly what it does.", "It handles continuous variables by default (binary data have their own option); it is the grouping that is binary, not the variables."]),
],
ex=[
("Read the plot", "Foundational", r"""<p>Open <code>R/output/L7-7_null_M.png</code> (the figure under “Companion Script &amp; Output” on this page). For each panel: where does the red line fall relative to the null distribution, and what do you conclude? Then explain in one sentence why the same difference (lone3 → dep1 +0.20) is significant in the middle panel but not in the right panel.</p>""",
 r"""<p>Left panel (course data): the red line, M = {{V:pg1_M}}, is on the right side of the histogram but still within the bulk (95th percentile of the null distribution {{V:pg1_M_q95}}), p = {{V:pg1_p_M}}: no evidence of a difference, which matches the truth. Middle panel ({{V:pg2_n1}} per group): the red line lies to the right of the whole null distribution, p = {{V:pg2_p_M}}: a difference. Right panel ({{V:pg3_n1}} per group): the red line falls in the middle of the bulk, p = {{V:pg3_p_M}}. The difference is just as large, but with fewer people each group's estimates are less stable and the null distribution is wider (the 95th percentile goes from {{V:pg2_M_q95}} to {{V:pg3_M_q95}}), so the real difference is drowned out by noise.</p>"""),
("Hands-on: compare men's and women's T2 → T3 networks", "Hands-On", r"""<p>In R/L7-7.R, replace <code>vars_t(1)</code> and <code>vars_t(2)</code> in <code>est()</code> with <code>vars_t(2)</code> and <code>vars_t(3)</code>, and compare men's and women's T2 → T3 networks (200 permutations are enough). Report M and S with their permutation p-values, and look at the single-edge p of lone3 → dep1. Compared with p = {{V:pg1_p_lone3_dep1}} in Part 1 (T1 → T2), what do you learn?</p>""",
 r"""<p>Reference solution <code>R/solutions/L7-7_solution.R</code> (log <code>R/output/sol_L7-7_log.txt</code>): M = {{V:sol77_M}} ({{V:sol77_M_from}} → {{V:sol77_M_to}}: men {{V:sol77_M_m}}, women {{V:sol77_M_f}}), permutation p = {{V:sol77_pM}}; S = {{V:sol77_S}} (men {{V:sol77_S_m}}, women {{V:sol77_S_f}}), p = {{V:sol77_pS}}. Of the 72 edges, {{V:sol77_n05}} have unadjusted p &lt; .05. lone3 → dep1: men {{V:sol77_l3d1_m}}, women {{V:sol77_l3d1_f}}, p = {{V:sol77_l3d1_p}}.</p>
<p>In T1 → T2 this edge had p = {{V:pg1_p_lone3_dep1}}; in T2 → T3 it is not significant at all: the first was very likely just the smallest of 72 tests by chance. Had you looked only at T1 → T2 and written “the prediction of depressed mood by loneliness differs by gender,” it would most likely have been a false positive: the two groups were generated with the same lagged coefficients, and the result did not replicate in another time interval (“most likely” because the shift before the cutting into categories may create a very small difference on the observed scale). Also, with 200 permutations the smallest possible p is {{V:sol77_pmin}}, so the p-values are coarser than with 1000.</p>"""),
("Writing: report a network comparison", "Writing", r"""<p>Take simulation ② (pretend it is real data: group 1 are clients before receiving a service, group 2 another set of clients after receiving it) and write a 120–150 word results paragraph that covers the method (estimation rule, number of permutations), the results for M and S, the edge that differs most, and one careful sentence of interpretation.</p>""",
 r"""<p>Sample: “We compared the two groups' cross-lagged networks with a permutation test ({{V:pg2_nperm}} permutations, λ chosen by EBIC in both groups). The network structure invariance test was significant (M = {{V:pg2_M}}, p = {{V:pg2_p_M}}); the edge with the largest difference was {{V:pg2_M_from}} → {{V:pg2_M_to}} (group 1 {{V:pg2_M_b1}}, group 2 {{V:pg2_M_b2}}). The global strength invariance test was not significant (S = {{V:pg2_S}}, p = {{V:pg2_p_S}}). The S test found no difference in overall strength, but its null distribution is wide and insensitive to changes in single edges, so this does not show that the overall connectivity of the groups is the same. The difference lies mainly in individual edges. Because none of the 72 edges remained significant after correction in the edge-by-edge tests, single-edge differences should be treated as exploratory findings to be tested in independent samples; and since the two groups are different people, the difference cannot be read as a causal effect of the service on individuals.”</p>"""),
("Analysis plan: pre-specification + sample size", "Conceptual", r"""<p>You plan to compare the CLPNs of urban and rural community residents, and theoretically you care most about the edge “Feeling isolated (lone3) → later Depressed mood (dep1).” (1) Write a pre-specified hypothesis for your analysis plan (Lesson 10.1). (2) Based on simulation ③, if you can only recruit 300 people per group, what should the plan say?</p>""",
 r"""<p>(1) Example: “Primary hypothesis: the cross-lagged coefficient lone3 → dep1 differs between urban and rural residents; this one edge's group difference is tested with a permutation test (1000 permutations, λ chosen by EBIC in both groups), α = .05, without multiple-comparison correction. The other comparisons (M, S, and edge-by-edge) are exploratory, and the edge-by-edge comparisons use the Holm correction.”</p>
<p>(2) Simulation ③ shows that for the same difference of 0.20, with 300 people per group the M test did not find it (p = {{V:pg3_p_M}}), and the pre-specified single-edge p = {{V:pg3_p_lone3_dep1}}, right around .05. That is one sample, not power. The plan should state that power is limited with 300 people per group and that a nonsignificant result cannot be read as “no difference”; if possible, estimate the needed sample size with the simulation method of Lesson 7.6 (adapted to two groups), or aim for a larger sample.</p>"""),
],
summary=[
"Before comparing groups, be clear about the question: the edge that differs most (M), overall strength (S), or one particular edge. Null hypothesis: the two groups' data come from the same population (so their networks are also the same).",
"Permutation test: shuffle the group labels and re-estimate to get the null distribution; p = (number of shuffles ≥ the observed value + 1) / (number of permutations + 1).",
"Course data (no real difference): neither M nor S significant; simulation ②: M found the changed edge, S was not significant; simulation ③: with half the people the difference is no longer found.",
"Not significant ≠ the same; group comparisons need large samples. ② and ③ are single samples; power has to be estimated with repeated simulations (Lesson 7.6).",
"Testing 72 edges one by one produces chance “significance”; the smallest possible p is 1/(B+1), so correcting all edges together needs B far larger than m/α (1440 here; ≥ 10000 recommended). Better: test only a few edges specified in advance.",
"NCT is for cross-sectional networks and cannot directly replace a CLPN comparison; paired comparisons (the same people) cannot be shuffled this way."
],
refs=["van Borkulo, C. D.", "Wysocki, A., McCarthy", "Epskamp, S., Borsboom, D., & Fried"],
)
