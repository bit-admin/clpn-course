# -*- coding: utf-8 -*-
_E82 = ["dep3 → dep4", "lone2 → lone4", "lone4 → dep4", "lone4 → lone2", "lone4 → lone3", "dep4 → lone2"]   # edges in the Lesson 8.2 table
L["8.2"] = dict(
lead=r"""<p>In this lesson you wrap the CLPN estimation code from Lesson 7.2 in a function and hand it to bootnet, which runs it 1,000 times. You learn to read the bootstrap interval plot and the difference test for edge weights, and you see the limits of these intervals under regularized estimation.</p>""",
intuition=r"""
<h3>The idea: put the whole estimation procedure inside the bootstrap loop</h3>
<p>In Lesson 8.1, each bootstrap replicate recomputed one correlation. Now each replicate must redo the entire CLPN estimation: 9 calls to cv.glmnet, each with its own cross-validation to choose λ. So you need a """ + T("custom estimator") + r""": a function that takes a data set and returns a 9 × 9 matrix. bootnet does the resampling, calls the function 1,000 times and collects the results.</p>
<h3>Three rules for writing the function</h3>
<ol><li><b>The function depends only on its arguments.</b> Do not use variables defined outside it (such as <code>t1_vars</code>). With """ + T("parallel computing", "nCores") + r""" &gt; 1, each worker process receives only the function itself and cannot see global variables. The course scripts handle this by putting T1 in the first p columns of the data and T2 in the last p columns; inside the function, p is computed as <code>ncol(data)/2</code>.</li>
<li><b>Write package functions with their full name</b>: <code>glmnet::cv.glmnet</code>, because <code>library(glmnet)</code> may not have been run in a worker process.</li>
<li><b>Tell bootnet what to save</b>: <code>statistics = c("edge", "outExpectedInfluence", "inExpectedInfluence")</code>; for a directed network, set <code>directed = TRUE</code>.</li></ol>
<h3>Reading the edge-weight interval plot</h3>
<p><code>plot(boot, order = "sample")</code> draws every edge, sorted by its sample estimate from largest to smallest. The plot shows three things: red line (points) = estimate in the original sample; black line (points) = mean of the 1,000 bootstrap estimates; gray band = bootstrap interval (here <code>CIstyle = "quantiles"</code>, i.e., the 2.5th and 97.5th percentiles). The red and black lines do not coincide because LASSO shrinks the estimates again in each resample and sometimes sets an edge to 0; see "Why does regularization bias the intervals?" below. Below is a simulated version. The green circles are the population target of the course data (<code>true_B_population.csv</code>, what a standard CLPN estimates as the sample grows without bound). Only a simulation study knows these values. They are also not the within-person truth (Lesson 7.2): the bootstrap can tell you how uncertain the estimate is relative to the population target, not how far it is from the within-person process. Adjust the sample size and λ and watch how the intervals change.</p>
""" + W("edgeci") + r"""
<h3>Three points for interpretation</h3>
<ol><li><b>Look at overlap, not at "significance".</b> If the intervals of the strongest edges overlap heavily, you cannot say "A→B is stronger than C→D".</li>
<li><b>Edges whose interval contains 0:</b> in at least some of the bootstrap samples (no less than 2.5%), LASSO set the edge to 0 or it changed sign. The estimate is unstable and should not be a focus of interpretation. The course script also reports <code>prop0</code>: the proportion of bootstrap samples in which the edge is 0.</li>
<li><b>The interval is not a strict 95% confidence interval.</b> LASSO pulls coefficients toward 0, so the bootstrap distribution is shifted toward 0 and piles up at 0, and 95% coverage is not guaranteed. Epskamp et al. (2018) recommend reading it as a description of estimation precision, not as a hypothesis test.</li></ol>
<h3>Results for the course data</h3>
""" + TABLE(["Edge", "Sample estimate", "Bootstrap mean", "2.5%", "97.5%", "prop0", "Population target", "Within-person truth"],
  [r + ["{{V:pop_" + e.replace(" → ", ">") + "}}", "{{V:win_" + e.replace(" → ", ">") + "}}"] for e, r in zip(_E82, boot_table_rows(_E82))]) + r"""
<p class="muted" style="font-size:.88rem">Source: R/output/L8-2_cl_edge_boot.csv (1,000 nonparametric bootstrap replicates). The last two columns are the answers, from data/true_B_population.csv and data/true_B_within.csv; a real study does not have them. The course script runs on a single core by default (<code>nCores = 1</code>), so with <code>set.seed(2026)</code> your own run should reproduce this table exactly. With parallel processing, <code>set.seed()</code> does not reach the worker processes and the second or third decimal will differ slightly; the sample estimates (column 2) are still identical every time.</p>
<p>The intervals of the 5 strongest cross-lagged edges are all about 0.15 wide and overlap heavily, and the difference test finds no pair among them that is "significantly different". So in a paper you cannot write "Sleep problems → Fatigue is the strongest edge"; you can only write "the strongest edges include …; the differences between them did not reach significance in the bootstrapped difference test".</p>
<h4>How prop0 relates to the interval endpoints</h4>
<p>The prop0 and 2.5% columns are two sides of the same thing. For an edge with a positive sample estimate, each bootstrap value is either 0 (removed by LASSO) or, mostly, positive. Sort the 1,000 values from smallest to largest and the zeros come first. The 2.5th percentile is roughly the 25th value: if more than 25 values are 0 (prop0 &gt; 0.025), the 25th value is 0 and the lower bound is exactly 0. Only when prop0 is below 0.025 is the lower bound a positive number, and then often only just above 0. lone4 → dep4 has prop0 {{V:b8_lone4>dep4_prop0}} and lower bound {{V:b8_lone4>dep4_q2.5}}; dep5 → dep4 has prop0 {{V:b8_dep5>dep4_prop0}} and lower bound {{V:b8_dep5>dep4_q2.5}}. These two intervals "just exclude 0" only because fewer than 2.5% of the resamples set them to 0; a few more and the intervals would contain 0. So when you read the table, treat an edge whose lower bound is very close to 0 with the same caution as one whose lower bound is 0, and do not draw a hard line at "contains 0 or not". For a negative edge, look at the upper bound instead: dep4 → lone2 has upper bound {{V:b8_dep4>lone2_q97.5}}, very small in absolute value, the same situation.</p>
<p>Now look at the last two columns. lone4 → lone2 (interval [{{V:b8_lone4>lone2_q2.5}}, {{V:b8_lone4>lone2_q97.5}}]) and lone4 → lone3 ([{{V:b8_lone4>lone3_q2.5}}, {{V:b8_lone4>lone3_q97.5}}]) are among the strongest edges in the sample. Their population targets are {{V:pop_lone4>lone2}} and {{V:pop_lone4>lone3}}, but their within-person truth is 0 for both: they are within-construct edges produced by the stable trait (Lesson 7.2). The bootstrap interval answers "if you drew another sample like this one, how much would the estimate change?"; it measures sampling uncertainty relative to the population target. A trait edge really exists in the population, so the larger the sample, the narrower its interval and the more reliably it stays away from 0, yet it is never an edge of the within-person process. So "the interval excludes 0" says at most that the predictive relationship in the population is probably not 0, not that the edge reflects a within-person dynamic effect.</p>
<h3>The """ + T("bootstrapped difference test") + r""" for edge weights</h3>
<p>For each pair of edges, compute "edge A − edge B" in every bootstrap sample. If the 95% interval of the difference does not contain 0, the two edges are considered "significantly different". <code>plot(boot, "edge", plot = "difference")</code> draws a square grid: black cells = significantly different, gray cells = not significant. Note: with many edge pairs this is a large number of multiple comparisons, and it is also affected by regularization, so be conservative with conclusions.</p>
<h3>Worked example: two overlapping intervals—what does the difference test say?</h3>
<p>Take dep3 → dep4 (interval [{{V:b8_dep3>dep4_q2.5}}, {{V:b8_dep3>dep4_q97.5}}]) and lone4 → dep4 ([{{V:b8_lone4>dep4_q2.5}}, {{V:b8_lone4>dep4_q97.5}}]). Neither interval contains 0, and they largely overlap. From the two intervals alone you can say neither that the edges are equally strong nor that dep3 → dep4 is stronger. The difference test subtracts the two edges estimated from the same resample in each bootstrap sample, giving 1,000 differences \(d^{*(b)}\), and checks whether the 95% interval of the differences contains 0. This is the beginning of that part of the R/L8-2.R log:</p>
""" + OUT(RLOG("L8-2_log.txt", "Difference tests between the top 5 CL edges", 4), "Actual output: R/output/L8-2_log.txt (excerpt)") + r"""
<p>The second line is this pair (<code>lower</code> and <code>upper</code> are the ends of the interval for the difference): the interval contains 0, so no difference is detected. The 5 strongest edges give {{V:b8_diff_total}} comparisons in total: {{V:b8_diff_text}}. The interval for a difference is wider than that of a single edge, because the difference carries the fluctuation of both edges.</p>
<p>Why can't you replace the difference test with "do the intervals overlap"? The variance of the difference is</p>
""" + MATH(r"\mathrm{Var}(d^*)=\mathrm{Var}(\hat\beta^*_A)+\mathrm{Var}(\hat\beta^*_B)-2\,\mathrm{Cov}(\hat\beta^*_A,\hat\beta^*_B)") + r"""
<p>Each interval reflects only its own term among the first two; neither shows the third. Within one bootstrap sample, the two estimates may rise and fall together (positive covariance), making the difference more stable than the two intervals suggest, or one may rise as the other falls (negative covariance), making it less stable. dep3 → dep4 and lone4 → dep4 both come from the same LASSO regression predicting dep4; when dep3 and lone4 are correlated at T1, they split the same share of variance in that regression, and when one edge gets more, the other gets less. Even if the two estimates were independent (covariance 0), the difference can be significant while the two intervals still overlap slightly; only when they do not overlap at all can you roughly conclude that the difference is significant. So to compare two edges, run the difference test instead of eyeballing the intervals.</p>
<h3>λ is chosen again in every resample</h3>
<p><code>clpn_fun</code> reruns 10-fold cross-validation and chooses λ anew on every bootstrap sample. So the intervals reflect not only how the coefficients vary for a fixed λ but also how λ itself varies: if a resample happens to choose a larger λ, a set of weak edges drops to 0 together; if it chooses a smaller λ, they come back together. If you fixed λ inside the function at the value chosen on the full sample, the intervals would be somewhat narrower, but that amounts to assuming λ is known in advance and underestimates the uncertainty. bootnet does the same for its built-in estimators: each resample reruns the whole estimation function, including the choice of tuning parameter. The principle: the bootstrap repeats the entire estimation procedure, so the randomness of every step is included. That is also how the variation from the random fold assignment in cross-validation (Lesson 9.2: changing the seed changes weak edges) enters the bootstrap intervals, while a single estimate never shows it.</p>
<h3>Common misreadings and corrections</h3>
<ul><li><b>Misreading: a low prop0 and an interval that excludes 0 mean the edge really is this strong in the population.</b> The bootstrap only resamples within your sample; it cannot see how the sample itself departs from the population. lone4 → dep4 has prop0 of only {{V:b8_lone4>dep4_prop0}} and an interval that excludes 0, yet its population target is only {{V:pop_lone4>dep4}} and its within-person truth is {{V:win_lone4>dep4}}. The interval describes how much the estimate would vary with another group of people from the same source, not how far the estimate is from the population value. The full procedure in Lesson 10.2 (unpenalized re-estimation, with two spans of data checked against each other) classifies this edge as "{{V:fp10_lone4>dep4_kept}}".</li>
<li><b>Misreading: the bootstrap mean is smaller than the sample estimate, so the sample estimate is too high and you can "correct" it with the mean.</b> The mean departs from the sample estimate mainly because LASSO shrinks again in each resample and sometimes sets the edge to 0. That is how the method behaves under resampling, not an estimate of bias relative to the population; "correcting" with it counts the shrinkage twice. In a paper, report the sample estimate and its interval.</li>
<li><b>Misreading: a wide interval means the edge is unimportant.</b> A wide interval only means the estimate is imprecise. An edge of moderate strength in the population will also have a wide interval when the sample is fairly small. The conclusion is "these data are not enough to estimate it precisely", not "it is unimportant".</li></ul>
<h3>The nonparametric bootstrap can also look at centrality</h3>
<p>Because you saved outExpectedInfluence and inExpectedInfluence, <code>plot(boot, statistics = "outExpectedInfluence", plot = "difference")</code> tests differences in out-EI between nodes. But the more standard tool for whether a centrality ranking is stable is the case-dropping bootstrap and CS-coefficient of the next lesson.</p>
""",
math=r"""
<p>For the b-th bootstrap sample, re-estimate the whole matrix:</p>
""" + MATH(r"\hat B^{*(b)}=\mathrm{CLPN}\big(\text{resample } b\big),\qquad b=1,\dots,1000") + MATH(r"\mathrm{CI}_{kj}=\Big[\ q_{0.025}\big(\{\hat\beta^{*(b)}_{kj}\}_b\big),\ \ q_{0.975}\big(\{\hat\beta^{*(b)}_{kj}\}_b\big)\ \Big],\qquad \mathrm{prop0}_{kj}=\frac{1}{1000}\sum_b \mathbb{1}\big[\hat\beta^{*(b)}_{kj}=0\big]") + MATH(r"\text{Difference test:}\ d^{*(b)}=\hat\beta^{*(b)}_{A}-\hat\beta^{*(b)}_{B},\quad \text{if } 0\notin[q_{0.025}(d^*),q_{0.975}(d^*)]\ \Rightarrow\ \text{“significantly different”}") + SYM([
(r"\(\hat B^{*(b)}\)", "The 9 × 9 matrix estimated on the b-th bootstrap sample"),
(r"\(q_{0.025}(\cdot)\)", "2.5th percentile"),
(r"\(\mathbb{1}[\cdot]\)", "Indicator function: 1 if the condition holds, 0 otherwise"),
(r"\(\mathrm{prop0}_{kj}\)", "Proportion of bootstrap samples in which this edge is set to 0"),
(r"\(d^{*(b)}\)", "Difference between two edges in sample b"),
]) + r"""
<h4>Why does regularization bias the intervals?</h4>
<p>Recall soft thresholding: \(\hat\beta=\mathrm{sign}(z)\max(|z|-\lambda,0)\). If an edge's population target is 0.06 and λ ≈ 0.04, then in a fair share of bootstrap samples |z| &lt; λ and the estimate is exactly 0; in the rest, λ is subtracted from the estimate. So the bootstrap distribution has a spike at 0, and the rest of it is shifted toward 0. The lower bound of the percentile interval is often exactly 0 (in this run: {{V:b8_zero_lower_text}}; nearly all weaker edges further down the list are the same). Such intervals do not have the coverage property of an ordinary confidence interval.</p>
<h4>Computational cost</h4>
<p>Each <code>cv.glmnet(nfolds = 10)</code> fits 11 glmnet paths: one per fold, plus a final one on all the data. Each path is solved along up to 100 λ values (glmnet uses "warm starts", solving from large λ to small λ in turn, which is much faster than 100 separate fits). So 1,000 bootstrap replicates × 9 nodes × 11 paths ≈ 100,000 glmnet paths, and the 200-replicate hand-written bootstrap at the end of the script adds about 20,000 more. On a single core, the course script takes about 7–15 minutes for 1,000 replicates (the measured range of R/L8-2.R on different computers, including the difference test and the hand-written bootstrap). Parallel processing (<code>nCores</code> &gt; 1) can be several times faster, but bootnet's parallel resampling is not controlled by <code>set.seed()</code>, so results are no longer reproducible. That is why the course defaults to a single core; for a first try you can use 200 replicates.</p>
""",
code=CODE(r"""
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(glmnet); library(qgraph) })
dat <- read_course_data()
wide_items <- dat[, c(vars_t(1), vars_t(2))]   # 18 columns: first 9 are T1, last 9 are T2
clpn_fun <- function(data) {                   # custom estimator: depends only on its argument data
  p <- ncol(data) / 2
  X <- scale(as.matrix(data[, 1:p]))           # T1
  Y <- scale(as.matrix(data[, (p + 1):(2 * p)]))   # T2
  B <- matrix(0, p, p)
  for (j in seq_len(p)) {
    cvfit <- glmnet::cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
    B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]
  }
  B                                            # rows = T1 (from), columns = T2 (to)
}
set.seed(2026)
net <- estimateNetwork(wide_items, default = "none", fun = clpn_fun,
                       directed = TRUE, labels = items)
set.seed(2026)
boot <- bootnet(net, nBoots = 1000, type = "nonparametric",
                nCores = 1,   # single core: reproducible after set.seed; parallel is faster but not reproducible
                statistics = c("edge", "outExpectedInfluence", "inExpectedInfluence"))
plot(boot, statistics = "edge", order = "sample", labels = TRUE, CIstyle = "quantiles")
s <- as.data.frame(summary(boot, statistics = "edge"))
s_cl <- s[s$node1 != s$node2, c("node1", "node2", "sample", "mean", "q2.5", "q97.5", "prop0")]
head(s_cl[order(-abs(s_cl$sample)), ], 10)     # 10 strongest cross-lagged edges
plot(boot, "edge", plot = "difference", onlyNonZero = TRUE, order = "sample")
""", "Core of R/L8-2.R (for a first try, use nBoots = 200; 1,000 replicates on one core take about 7–15 minutes)") + r"""
<p><b>Notes:</b> <code>default = "none", fun = clpn_fun</code> tells bootnet to use your own function; <code>CIstyle = "quantiles"</code> draws percentile intervals; <code>summary()</code> returns each edge's sample value, bootstrap mean, quantiles and prop0. The end of the script also has a "hand-written" bootstrap (200 replicates) that does not use bootnet, to help you see how it works.</p>""",
quiz=[
("Why write the estimation procedure as a function?",
 ["To make the code shorter and neater",
  "The bootstrap must repeat the entire estimation procedure on each resample, and a function lets bootnet call it over and over",
  "bootnet accepts only custom functions and has no built-in estimators",
  "Once it is a function, cv.glmnet runs in parallel automatically and is faster"],
 1,
 ["Readability is a side benefit; the point is that bootnet has to rerun the same estimation on every resample.",
  "Correct.",
  "bootnet has built-in methods such as EBICglasso, but no nodewise LASSO for a CLPN, so you write it yourself.",
  "Making it a function does not change the speed of cv.glmnet; parallelism is set by bootnet's nCores, and it breaks reproducibility."]),
("A custom estimator uses the outside variable t1_vars, and you set nCores = 4. What is likely to happen?",
 ["It runs faster, with results identical to a single core",
  "The worker processes cannot find t1_vars and throw an error",
  "It runs, but every replicate estimates on the original data, so the intervals have width close to 0",
  "bootnet switches to a single core automatically"],
 1,
 ["Worker processes cannot see global variables, so it never finishes; and even if it ran, parallel results are not controlled by set.seed().",
  "Correct: the function should depend only on its arguments.",
  "That is the result of a different mistake (reading the outside data frame dat directly inside the function). Here only column names are referenced: it runs on one core and fails outright on several.",
  "bootnet does not check for you whether the function depends on global variables."]),
("How should you read an edge whose bootstrap interval contains 0?",
 ["The edge is 0 in the population and should be deleted from the network",
  "The estimate of this edge is unstable (often set to 0, or its sign is unstable); it should not be a focus of interpretation",
  "The edge has p > .05 and is not significant",
  "You should re-estimate with a larger λ"],
 1,
 ["Containing 0 only shows instability; it does not prove the edge is 0. LASSO's bootstrap distribution piles up at 0 by design.",
  "Correct.",
  "Plausible but wrong: bootstrap intervals from a regularized estimate are not strict confidence intervals and cannot be turned into p-values (point 3 of \"Three points for interpretation\" in this lesson).",
  "Changing λ after seeing the bootstrap results is post hoc tuning; and a larger λ sets even more edges to 0."]),
("Why can't a bootstrap interval from a regularized estimate be treated as an ordinary 95% CI?",
 ["Because 1,000 bootstrap replicates are not enough",
  "LASSO's shrinkage and zeroing shift the bootstrap distribution toward 0 and make it pile up at 0, so coverage is not guaranteed",
  "Because the percentile method cannot give a confidence interval at all",
  "Because the course data are simulated"],
 1,
 ["The number of replicates only affects the Monte Carlo error of the endpoints; with 10,000 the distribution is still shifted toward 0.",
  "Correct.",
  "For an unpenalized estimate, the percentile interval is a commonly used confidence interval; the problem is LASSO's shrinkage, not the percentile method.",
  "Real data behave the same way; simulated data just let you see how the interval sits relative to the population target."]),
("In the course data, none of the pairwise difference tests among the 5 strongest cross-lagged edges is significant. What is the correct way to write this?",
 ["dep3 → dep4 is the strongest edge, because its sample estimate is largest",
  "The strongest edges include …; the differences between them did not reach significance in the bootstrapped difference test",
  "These 5 edges are equally strong",
  "The difference test failed, so the results are invalid"],
 1,
 ["The largest sample estimate is not necessarily the largest edge; the difference test shows that its gap to the other 4 does not exceed sampling fluctuation.",
  "Correct.",
  "Plausible but wrong: not detecting a difference is not the same as being equal; it only means these data are not enough to rank them.",
  "Non-significance is a result, not a failure; it tells you that you cannot rank these edges."]),
],
ex=[
("Intervals of the 5 strongest edges", "Hands-on", r"""<p>Run R/L8-2.R (200 replicates first is fine), report the sample values and bootstrap intervals of the 5 strongest cross-lagged edges, and use the difference test to decide which edges are "clearly different" from the others.</p>""",
 r"""<p>Reference (1,000 replicates, current output): dep3→dep4 {{V:b8_dep3>dep4_sample}} [{{V:b8_dep3>dep4_q2.5}}, {{V:b8_dep3>dep4_q97.5}}]; lone2→lone4 {{V:b8_lone2>lone4_sample}} [{{V:b8_lone2>lone4_q2.5}}, {{V:b8_lone2>lone4_q97.5}}]; lone4→dep4 {{V:b8_lone4>dep4_sample}} [{{V:b8_lone4>dep4_q2.5}}, {{V:b8_lone4>dep4_q97.5}}]; lone4→lone2 {{V:b8_lone4>lone2_sample}} [{{V:b8_lone4>lone2_q2.5}}, {{V:b8_lone4>lone2_q97.5}}]; lone4→lone3 {{V:b8_lone4>lone3_sample}} [{{V:b8_lone4>lone3_q2.5}}, {{V:b8_lone4>lone3_q97.5}}]. Difference test: {{V:b8_diff_total}} comparisons, {{V:b8_diff_text}}. The course script uses a single core and a fixed seed, so the full 1,000 replicates should give exactly the same results; with 200 replicates first, or with parallel processing, the endpoints will differ slightly in the second or third decimal. Conclusion: the ranking of these 5 edges is not reliable; you can only say they are "a group of relatively strong edges".</p>"""),
("Hand-written bootstrap of one edge", "Hands-on", r"""<p>Following Lesson 8.1, write a 200-replicate loop with <code>clpn_fun</code> that records only B["lone3", "dep1"]. Compute the interval and prop0, then compare them with the two answers: the population target ({{V:pop_lone3>dep1}} in <code>data/true_B_population.csv</code>) and the within-person truth ({{V:win_lone3>dep1}} in <code>data/true_B_within.csv</code>).</p>""",
 r"""<p><code>v &lt;- replicate(200, { idx &lt;- sample(n, n, TRUE); clpn_fun(wide_items[idx, ])[3, 5] })</code> (row 3 is lone3, column 5 is dep1); <code>quantile(v, c(.025, .975)); mean(v == 0)</code>. The hand-written part of the script (seed 82, {{V:hand_n}} replicates) gives the interval [{{V:hand_lo}}, {{V:hand_hi}}], with proportion {{V:hand_p0}} set to 0. You will see the interval as a whole shifted toward 0 (sample estimate {{V:b8_lone3>dep1_sample}}, below the population target {{V:pop_lone3>dep1}}), possibly with some share of zeros: this is shrinkage bias showing up in the bootstrap. The within-person truth {{V:win_lone3>dep1}} is higher and further from the interval; that gap comes from trait confounding, which the bootstrap was never meant to address.</p>"""),
("Seeing what λ does in the demo", "Understanding", r"""<p>In the edge-weight bootstrap interval demo on this page, set λ = 0, then λ = 0.05. Describe how the shape of the intervals and the "share of zeros" change.</p>""",
 r"""<p>λ = 0 (equivalent to OLS): the intervals are roughly centered on the estimates and symmetric, almost no edge is exactly 0, and the green circles (population target) mostly fall inside the intervals. λ = 0.05: the share of zeros rises sharply for weak edges and one end of their intervals sticks at 0; the intervals of strong edges shift toward 0 as a whole, and the green circles (population target) often sit at the upper end of the interval or even outside it. This shows that regularized intervals are not ordinary confidence intervals.</p>"""),
],
summary=["Write the CLPN estimation as a function that depends only on its arguments and pass it to bootnet(default = \"none\", fun = …, directed = TRUE).", "Always set statistics = c(\"edge\", \"outExpectedInfluence\", \"inExpectedInfluence\").", "Reading intervals: look at overlap and whether 0 is included; prop0 = share set to 0.", "Regularized bootstrap intervals are shifted toward 0 and pile up at 0; they are not strict 95% CIs.", "Course data: no pairwise difference among the 5 strongest edges is significant → you cannot rank them."],
refs=["Epskamp, S., Borsboom, D., & Fried", "Wysocki, A., McCarthy"],
)

L["8.3"] = dict(
lead=r"""<p>Lesson 8.2 answered "how precise is each edge?". This lesson answers a different question: can you trust the centrality ranking? If a paper says "lone4 has the highest out-EI", readers need to know whether it would still be highest with a different group of people. The case-dropping bootstrap and the CS-coefficient were designed for exactly this.</p>""",
intuition=r"""
<h3>The idea: drop more and more people</h3>
<p>The """ + T("case-dropping bootstrap") + r""" works like this:</p>
<ol><li>Drop 5% of the people at random, re-estimate the network on the remaining 95%, compute centrality (for example out-EI), and correlate it with the centrality from the <b>full sample</b>.</li>
<li>Repeat many times, and do the same for dropping 10%, 20% … up to 75% (bootnet's default maximum); bootnet divides the total number of replicates among the drop proportions.</li>
<li>If the centrality pattern still agrees closely with the full sample after more than half the people are dropped, the ranking is stable; if dropping just a few people scrambles it, the ranking is unstable.</li></ol>
<h3>The CS-coefficient in one sentence</h3>
<p>""" + T("CS-coefficient", "correlation stability coefficient") + r""": <b>the largest proportion of cases you can drop while, in 95% of the subsamples, the correlation between subsample centrality and original-sample centrality stays ≥ 0.7.</b></p>
<p>Epskamp, Borsboom and Fried (2018) suggest that CS should not fall below 0.25 and preferably be above 0.5. CS = 0.6 means: even after dropping 60% of the people, you can be 95% sure that the correlation of centrality with the original sample is at least 0.7.</p>
""" + NOTE("Can these two thresholds be used directly for a CLPN?", "<p>0.25 and 0.5 come from the simulation study of Epskamp, Borsboom and Fried (2018). They simulated cross-sectional undirected networks (partial correlation networks) and looked at undirected centrality indices such as strength, closeness and betweenness. A CLPN is a directed network; this course uses out-EI and in-EI for 9 nodes, and each node's coefficients come from a separate LASSO regression. As far as the course author knows, no study has checked whether these two thresholds are equally suitable for a directed CLPN with this few nodes.</p><p>So the course uses them as reference lines that are common in the literature, not as cutoffs with theoretical guarantees. In practice: (1) report the actual CS value, not just \"passed\" or \"failed\"; (2) in the Methods, cite where the thresholds come from and state that they come from simulations of undirected networks; (3) when CS is near a threshold (like in-EI in this lesson, between the 0.44 and 0.52 steps), treat it as a borderline case and interpret it cautiously; (4) with only 9 nodes, the correlation itself is unstable (a correlation computed from 9 points has large sampling fluctuation), which is one reason the CS result easily jumps between two steps.</p>") + r"""
<p>The simulation below shows how the CS-coefficient is read from the curves, and how the sample size and the true differences between nodes affect it. Try to find out: at N = 300, how large must the true EI difference be for CS to reach ≥ 0.5?</p>
""" + W("cs") + r"""
<h3>Why do the true differences between nodes matter?</h3>
<p>Whether a centrality ranking is stable depends on the size of the true differences between nodes relative to the estimation noise. If the true out-EI of all 9 nodes is about the same (all around 0.2), even a very large sample can hardly produce a stable order, because there is no real order. So a low CS does not necessarily mean the study was done badly; the nodes may simply be about equally important. Either way the conclusion is the same: do not interpret the ranking.</p>
<h3>Case-dropping versus the ordinary bootstrap</h3>
""" + TABLE(["", "Nonparametric bootstrap (8.2)", "Case-dropping bootstrap (8.3)"], [
["How it samples", "Draws N people with replacement", "Draws (1 − drop proportion) × N people without replacement"],
["Question answered", "How precise is each edge (or centrality value)?", "Does the centrality ranking / pattern hold as the sample gets smaller?"],
["Main output", "Intervals, prop0, difference test", "Stability curve, CS-coefficient"],
["Mainly used for", "Edge weights", "Centrality indices (out-EI, in-EI, etc.)"]]) + r"""
<h3>How to write it up when CS falls short</h3>
""" + TABLE(["CS value", "You can say", "Do not say"], [
["≥ 0.5", "\"lone4 had the highest out-EI (CS = …); the ranking was fairly stable.\" (still prediction, not causation)", "\"lone4 is the core symptom driving depression.\""],
["0.25–0.5", "\"The stability of the out-EI ranking was moderate (CS = …); the following ranking is for reference only: …\"", "Treating the top-ranked node as the main finding"],
["< 0.25", "\"The stability of out-EI was insufficient (CS = 0.13), so we do not interpret the out-EI ranking of the nodes and report it only in the supplementary material.\"", "\"lone4 is the most influential.\""]]) + r"""
""" + KEY("The principle for scaling back claims:", "When CS is insufficient, the conclusion falls back from \"a ranking of nodes\" to \"a description of edges\" (e.g., \"several loneliness items have positive predictive edges to later depression items\") or to \"construct-level sums\" (e.g., \"the sum of edge weights loneliness → depression is larger than in the reverse direction\", tested with the bootstrap).") + r"""
<h3>Results for the course data</h3>
<p>The companion script R/L8-3.R runs 1,000 case-dropping bootstrap replicates for out-EI and in-EI (see the actual output in the "R Code" section):</p>
""" + TABLE(["Index", "CS-coefficient (this run of R/L8-3.R)", "Verdict", "Separate run in the Lesson 10.2 main script"], [["in-EI (in-expected influence)", "{{V:cs8_in}}", "{{V:cs8_in_judge}}", "{{V:cs10_in}} ({{V:cs10_in_short}})"], ["out-EI (out-expected influence)", "{{V:cs8_out}}", "{{V:cs8_out_judge}}", "{{V:cs10_out}} ({{V:cs10_out_short}})"]]) + r"""
<p><b>Why does the CS of in-EI "change from run to run"?</b> CS is not computed on a continuous scale. It is checked at a fixed set of drop proportions (5%, 12.7%, 20.5%, 28.4%, 36.1%, 43.9%, 51.6% …), and the largest step that still meets the 95% condition is taken. In the course data, in-EI sits right between the 43.9% and 51.6% steps: depending on which subsamples are drawn (a different random seed, or parallel processing), the 51.6% step sometimes just reaches 95% (CS = 0.52) and sometimes just misses (CS = 0.44). The course script fixes the seed and runs on one core, so it gets the same value every time (currently {{V:cs8_in}}, the same as {{V:cs10_in}} in Lesson 10.2); but reproducible is not the same as stable, and the value itself is still borderline. So report the actual numbers: the stability of in-EI is at the edge of 0.5, so its ranking can only be interpreted cautiously; out-EI is around 0.20 every time, consistently below the bar. For a more precise CS, follow bootnet's hint: set <code>caseMin</code>/<code>caseMax</code> to put more steps in the critical range and increase <code>nBoots</code>.</p>
<p>This result means the eye-catching finding from Lesson 7.4, "lone4 (No one understands me) has the highest out-EI", cannot go into the conclusions, while the in-EI ranking, "depression items such as dep4 (Fatigue) and dep1 (Depressed mood) are easier to predict", can be reported (cautiously). Recall from Lesson 7.4 that lone4's outgoing edges do not stand out whether computed from the population target or from the within-person truth. But keep these two things apart: CS only says that the out-EI ranking is unstable when some participants are removed. It measures how stable the estimate is relative to this sample, not how far the estimate is from the population target or the within-person truth. A biased estimate can be very stable (Lesson 10.2 compares each estimate with the population target and the within-person truth, and there are such edges there); "does not match the answer" can only be seen in simulated data where the answer is known. Even if CS is high and the ranking agrees with the population target, it may still not be the ranking of the within-person process, because EI also adds in the within-construct edges produced by the trait.</p>
""",
math=r"""
""" + MATH(r"\mathrm{CS}(\mathrm{cor}=0.7)=\max\Big\{\,d\ :\ P\big(\ \mathrm{cor}(\hat c^{\,(d)},\hat c\,)\ \ge 0.7\ \big)\ \ge 0.95\Big\}") + SYM([
(r"\(d\)", "Proportion of cases dropped; by default bootnet uses 10 equally spaced steps between 0.05 and 0.75: 0.05, 0.127, 0.205, …, 0.75"),
(r"\(\hat c\)", "Centrality vector on the full sample (e.g., the out-EI of the 9 nodes)"),
(r"\(\hat c^{\,(d)}\)", "Centrality vector re-estimated on a subsample with drop proportion d"),
(r"\(\mathrm{cor}(\cdot,\cdot)\)", "(Pearson) correlation between two centrality vectors, measuring agreement in pattern/ranking"),
(r"\(P(\cdots)\ge0.95\)", "Among all subsamples at this drop proportion, at least 95% have correlation ≥ 0.7"),
(r"\(\max\{\cdots\}\)", "The largest drop proportion that meets the condition"),
]) + r"""
<h4>Why are smaller samples less stable? (intuition)</h4>
<p>With a subsample of size \(n=(1-d)N\), the noise in each centrality estimate is roughly proportional to \(1/\sqrt{n}\). The correlation between the centrality vector and the full-sample vector depends on the ratio of the variance of the true differences between nodes to the noise variance:</p>
""" + MATH(r"\mathrm{cor}\approx\sqrt{\frac{\sigma^2_{\text{true diff.}}}{\sigma^2_{\text{true diff.}}+\sigma^2_{\text{noise}}(n)}},\qquad \sigma^2_{\text{noise}}(n)\propto\frac1n") + r"""
<p>(This is a simplified formula for intuition; the interactive demo on this page simulates along exactly these lines.) The larger the true differences and the larger n, the closer the correlation is to 1.</p>
<h4>The argument in bootnet</h4>
<p>In <code>corStability(cd, cor = 0.7)</code>, <code>cor</code> is the 0.7 in the formula; you can make it stricter, e.g., 0.8. When reporting, use the default so results can be compared with the literature, and explain any change.</p>
""",
code=CODE(r"""
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(glmnet) })
dat <- read_course_data()
wide_items <- dat[, c(vars_t(1), vars_t(2))]
# clpn_fun is the same as in L8-2 (first 9 columns T1, last 9 columns T2)
set.seed(2026)
net <- estimateNetwork(wide_items, default = "none", fun = clpn_fun,
                       directed = TRUE, labels = items)
set.seed(2026)
cd <- bootnet(net, nBoots = 1000, type = "case",
              nCores = 1,   # single core: reproducible after set.seed; parallel is faster but not reproducible
              statistics = c("outExpectedInfluence", "inExpectedInfluence"))
cs <- corStability(cd)        # prints the CS-coefficient for each index
cs
plot(cd, statistics = c("outExpectedInfluence", "inExpectedInfluence"))
""", "Core of R/L8-3.R") + r"""
<p><b>Reading plot(cd):</b> the x-axis is the proportion of the sample kept (by default bootnet decreases it from left to right), the y-axis is the mean correlation with the original-sample centrality, and the shading is the 2.5%–97.5% quantile range. The more slowly the curve falls, the more stable the index. The script also prints a verdict against the 0.25 / 0.5 thresholds automatically.</p>""",
quiz=[
("What does CS = 0.6 mean?",
 ["60% of the edges are stable",
  "After dropping 60% of the cases, you can still be 95% sure that the correlation of centrality with the original sample is ≥ 0.7",
  "The mean correlation between subsample centrality and original centrality is 0.6",
  "After dropping 60% of the cases, the centrality ranking is exactly the same as in the original sample"],
 1,
 ["CS is about centrality indices, not edges; for the precision of edges, see the intervals of Lesson 8.2.",
  "Correct.",
  "Plausible but wrong: 0.6 is the drop proportion, not a correlation; the correlation threshold is the 0.7 in the formula.",
  "The requirement is that at least 95% of subsamples have correlation ≥ 0.7, not an identical ranking."]),
("If the CS of out-EI is only 0.13, can a paper still call some node \"the most influential\"?",
 ["Yes, as long as that node's out-EI is clearly higher than the others in the sample",
  "No: report that stability is insufficient, do not interpret the ranking, and switch to an edge-level or construct-level description",
  "Yes, as long as p < .05",
  "Yes, a sample of 800 is enough"],
 1,
 ["\"Clearly higher in the sample\" is exactly what needs to be checked; CS = 0.13 means the ranking may change after dropping only a few cases.",
  "Correct.",
  "A centrality ranking has no corresponding p-value; significance and the stability of a ranking are two different things.",
  "A large sample does not guarantee a stable ranking: the course data have N = 800, and the CS of out-EI is still below 0.25."]),
("How do the questions answered by the case-dropping and the ordinary bootstrap differ?",
 ["They are the same; only the names differ",
  "The ordinary bootstrap assesses the precision of estimates (intervals); case-dropping assesses whether the centrality ranking holds as the sample shrinks",
  "Case-dropping is for edges, the ordinary bootstrap is for centrality",
  "Case-dropping also samples with replacement, just with a smaller sample"],
 1,
 ["Both the sampling and the question differ (see the comparison table in this lesson).",
  "Correct.",
  "Roughly the reverse: the precision of edges comes from the ordinary bootstrap, the stability of the centrality ranking from case-dropping.",
  "Case-dropping draws a subset of cases without replacement."]),
("What is the usual reference standard for CS?",
 ["≥ 0.05 is enough", "No lower than 0.25, preferably above 0.5", "It must reach 0.95", "≥ 0.7"], 1,
 ["0.05 is the first step of bootnet's grid of drop proportions, not a standard.",
  "Correct (Epskamp et al., 2018); for a directed CLPN it is only a reference.",
  "0.95 is the \"at least 95% of subsamples\" requirement, not the CS standard.",
  "0.7 is the correlation threshold used in the computation, not the CS standard."]),
("Which situation is most likely to give a very low CS even with a large sample?",
 ["The nodes' true centralities are nearly the same",
  "Only 1,000 case-dropping replicates were run",
  "The larger the sample, the more people are dropped, so the ranking is more easily scrambled",
  "The items were not z-standardized"],
 0,
 ["Correct: with no true differences, there is no stable order to find.",
  "The number of replicates affects how precise CS is (it may jump between two adjacent steps); it does not make a stable index look very unstable.",
  "What is dropped is a proportion; with a larger sample, more people remain at the same proportion, so the ranking can only be more stable.",
  "Standardization changes the scale of the coefficients, not the size of the true differences between nodes; the items are already standardized, and when node differences are small CS is low all the same."]),
],
ex=[
("CS-coefficients and scaled-back wording", "Hands-on + writing", r"""<p>Run R/L8-3.R and report the CS-coefficients of out-EI and in-EI. If CS &lt; 0.25, write a paragraph on how the conclusions should be scaled back; if ≥ 0.25, write how the ranking can be reported.</p>""",
 r"""<p>Course data (current output): CS of in-EI = {{V:cs8_in}}, CS of out-EI = {{V:cs8_out}}, so out-EI must be scaled back; in-EI is near 0.5 ({{V:cs8_in}} with the fixed seed; with other random seeds it varies between the 0.44 and 0.52 steps), which is borderline stable, so its ranking can only be reported cautiously. If CS &lt; 0.25: "The case-dropping bootstrap showed that the stability of out-EI was insufficient (CS = …), so we do not interpret the out-EI ranking of the nodes. At the edge level, several loneliness items (such as 'No one understands me') have positive cross-lagged edges to T2 depression items, but their bootstrap intervals are fairly wide." If you also want a construct-level comparison ("the sum of edge weights loneliness → depression is larger than in the reverse direction"), test this difference first; do not just see which of the two sums is bigger. How: read in <code>R/output/L8-2_boot.rds</code>, saved in Lesson 8.2, compute Σ B[loneliness, depression] − Σ B[depression, loneliness] in each bootstrap network, and take the 2.5% and 97.5% quantiles of the difference (code in part 2 of <code>R/solutions/L8-3_solution.R</code>, results written to <code>R/output/sol_L8-3_log.txt</code>). Only if the interval excludes 0 can you write "the sum of edge weights in the loneliness → depression direction is larger than in the reverse direction"; if it contains 0, write "no difference was detected between the sums of edge weights in the two directions". Course data: the loneliness → depression sum is {{V:sol83_sum_ld}}, depression → loneliness is {{V:sol83_sum_dl}}, and the difference {{V:sol83_diff}} has a 95% bootstrap interval of [{{V:sol83_q025}}, {{V:sol83_q975}}], which excludes 0, so the sentence can be written for these data; it is still a predictive relationship, and the interval is wide. Also remember that with signed sums, positive and negative edges cancel out, so a small sum does not mean weak connections. If 0.25–0.5: report the ranking with a "for reference only" qualifier; if ≥ 0.5: you can report the ranking, still without causal words.</p>"""),
("Finding the conditions in the demo", "Understanding", r"""<p>In the CS simulation on this page, find the smallest "true EI difference" (the "True EI spread across nodes" slider) that gives CS ≥ 0.5 at N = 150, 500 and 3000. Summarize the pattern.</p>""",
 r"""<p>The larger N, the smaller the true difference needed (roughly proportional to 1/√N). At N = 150 you need a large difference; at N = 3000 a fairly small difference can also be ranked stably. The pattern: stability = signal (true difference) / noise (∝ 1/√N). Exact values vary slightly with the simulation seed.</p>"""),
("Computing CS", "Basics", r"""<p>A case-dropping result: dropping 30%, 96% of subsamples have correlation ≥ 0.7; dropping 40%, 95.5%; dropping 50%, 93%. What is CS? How would you judge it?</p>""",
 r"""<p>CS = 0.4 (the largest drop proportion that meets ≥ 95%). It lies between 0.25 and 0.5: just acceptable, and the ranking must be interpreted with caution.</p>"""),
],
summary=["Case-dropping: drop more and more cases, re-estimate centrality, compare with the full sample.", "CS = the largest proportion that can be dropped while 95% of subsamples keep correlation ≥ 0.7.", "Reference: < 0.25 do not interpret the ranking; 0.25–0.5 with caution; ≥ 0.5 fairly stable.", "A low CS may come from a small sample or from small true differences between nodes.", "CS insufficient → fall back to edge-level or construct-level description."],
refs=["Epskamp, S., Borsboom, D., & Fried", "Isvoranu, A.-M., Epskamp"],
)
