# -*- coding: utf-8 -*-
# Module 8: Accuracy and stability checks
L["8.1"] = dict(
lead=r"""<p>So far, every conclusion has rested on a single estimate from the one sample you have. If you recruited another 800 similar people and ran the study again, how much would the results change? In practice you cannot rerun a survey a thousand times, but the bootstrap lets you "rerun" it on the computer using the sample you already have. This lesson explains the idea on a correlation coefficient and lays the groundwork for Lessons 8.2–8.3.</p>""",
intuition=r"""
<h3>The question: how reliable is one number?</h3>
<p>In the course data, the correlation between the T1 loneliness total and the T2 depression total is r = 0.296. With a different group of people it might be 0.25, or 0.34. How much an estimate changes when you swap in a different sample is called """ + T("sampling variability") + r""". In M1 we described it with standard errors and confidence intervals (review """ + LINK("1.5") + r"""), but those need a formula, and network edges and centrality indices have no simple ready-made formula.</p>
<h3>The bootstrap idea: treat the sample as the population</h3>
<p>The idea behind the """ + T("bootstrap") + r""" (named after "pulling yourself up by your own bootstraps") is:</p>
<ol><li>Your sample of 800 people is the best miniature of the population you have.</li>
<li>Draw 800 times at random <b>with replacement</b> from these 800 people to get a "new sample" (""" + T("resampling with replacement") + r"""). Some people are drawn two or three times, others not at all (on average about 37% of people are not drawn).</li>
<li>Recompute the statistic you care about (a correlation, an edge weight, a centrality index …) on the new sample.</li>
<li>Repeat 1,000 times to get 1,000 values. Their distribution approximates what you would see if you really reran the study 1,000 times.</li></ol>
<p>The 2.5th and 97.5th percentiles of these 1,000 values form the 95% """ + T("percentile interval") + r"""; their standard deviation is the bootstrap standard error. Because no assumption about the shape of the data's distribution is needed, this is called the """ + T("nonparametric bootstrap") + r""".</p>
<p>Try it: click "Draw 1 bootstrap sample" to see what resampling with replacement looks like, then "Run 1,000 times". Then set N to 20 or 400, generate a new sample, and compare the interval widths.</p>
""" + W("boot") + r"""
<h3>Why "with replacement"?</h3>
<p>If you drew 800 times without replacement, you would just get the original 800 people in a different order. The statistic would be exactly the same, with no variation at all. Drawing with replacement makes each new sample differ in who is repeated and who is left out, which mimics "a different group of people".</p>
<h3>What does a wide bootstrap interval tell you?</h3>
<p>A wide interval means the statistic is sensitive to the sample, so the estimate is imprecise. The cause may be a small sample, a weak effect, or a statistic that is unstable by nature (such as betweenness centrality). A narrow interval does not mean "correct", only "precise" (repeating the study would give similar numbers).</p>
<h3>What can't the bootstrap do?</h3>
""" + WARN("The bootstrap cannot fix a biased sample.", "If your whole sample comes from the clients of one community service center, the bootstrap only resamples within that group. It tells you how precise the estimate is among people like these, not whether it holds for all residents of the district. Nor can it fix measurement error, confounding, or a misspecified model.") + r"""
<h3>Why does network analysis especially need accuracy checks?</h3>
<p>Start by counting the parameters. A 9-node CLPN has 9 × 9 = 81 lagged coefficients (9 autoregressive edges plus 72 cross-lagged edges); a 16-node GGM has 16 × 15 / 2 = 120 possible edges; and samples usually number only a few hundred. Epskamp, Borsboom and Fried (2018) wrote about cross-sectional networks (GGMs). Their argument: with this many parameters and this few people, every parameter has sizable sampling variability, and the network plot does not show that uncertainty. A CLPN has even more parameters, so the argument applies here too. Every parameter carries sampling variability, and LASSO adds an "in or out" decision on top, so a network plot can look highly structured while many of its details are chance. Readers naturally look at the thickest edges and the "most central" node; if those change with a different sample, the conclusions do not hold. That is why network papers now almost always report bootstrap intervals for edge weights (Lesson 8.2) and the stability of centrality (Lesson 8.3).</p>
""",
math=r"""
<p>Let the original sample be \(\{z_1,\dots,z_N\}\) (each \(z_i\) is all of one person's data) and the statistic \(\hat\theta = s(z_1,\dots,z_N)\).</p>
""" + MATH(r"\text{Replicate } b:\ z^{*(b)}_1,\dots,z^{*(b)}_N \overset{\text{with replacement}}{\sim} \{z_1,\dots,z_N\},\qquad \hat\theta^{*(b)}=s\big(z^{*(b)}_1,\dots,z^{*(b)}_N\big)") + MATH(r"\widehat{\mathrm{SE}}_{\text{boot}}=\sqrt{\frac{1}{B-1}\sum_{b=1}^{B}\big(\hat\theta^{*(b)}-\bar\theta^{*}\big)^2},\qquad \mathrm{CI}_{95\%}=\big[\hat\theta^{*}_{(2.5\%)},\ \hat\theta^{*}_{(97.5\%)}\big]") + SYM([
(r"\(\hat\theta\)", "The statistic computed on the original sample (e.g., r = 0.296)"),
(r"\(z^{*(b)}_i\)", "The i-th person in the b-th bootstrap sample (the asterisk * means \"resampled\")"),
(r"\(B\)", "Number of bootstrap replicates (usually 1,000; not to be confused with the CLPN matrix B)"),
(r"\(\bar\theta^{*}\)", "Mean of the B bootstrap statistics"),
(r"\(\hat\theta^{*}_{(2.5\%)}\)", "2.5th percentile of the B bootstrap statistics"),
]) + r"""
<h4>Where does "about 37% are not drawn" come from?</h4>
<p>The probability that a given person is not picked in one draw is \(1-1/N\); the probability of not being picked in any of the N draws is \((1-1/N)^N\). As N grows, this approaches \(e^{-1}\approx 0.368\), the calculus limit \(\lim_{N\to\infty}(1-1/N)^N=1/e\).</p>
<h4>Comparison with the formula</h4>
<p>The correlation has a classic formula-based interval (Fisher z transformation): \(z=\tanh^{-1}(r)\), \(\mathrm{SE}=1/\sqrt{N-3}\), interval \(\tanh(z\pm1.96\,\mathrm{SE})\). Course data (R/L8-1.R): bootstrap interval [0.234, 0.360], <code>cor.test()</code> interval [0.232, 0.358], nearly identical; bootstrap standard error 0.033. When a formula exists, the two usually agree; the bootstrap earns its keep where there is no formula (such as the edges and centrality of a LASSO network).</p>
""",
code=CODE(r"""
source("R/_setup.R")
dat <- read_course_data()
x <- rowSums(dat[, paste0(lone_items, "_t1")])     # T1 loneliness total
y <- rowSums(dat[, paste0(dep_items,  "_t2")])     # T2 depression total
n <- length(x)
set.seed(81)
B <- 1000
r_boot <- numeric(B)                       # empty vector to hold the 1,000 results
for (b in 1:B) {
  idx <- sample(1:n, n, replace = TRUE)    # draw n case numbers with replacement
  r_boot[b] <- cor(x[idx], y[idx])         # recompute the correlation on the "new sample"
}
quantile(r_boot, c(.025, .975))            # percentile interval
sd(r_boot)                                 # bootstrap standard error
cor.test(x, y)$conf.int                    # compare with the formula
hist(r_boot, breaks = 40); abline(v = cor(x, y), lwd = 3)
""", "Core of R/L8-1.R (no packages needed, about 15 lines)") + r"""
<p><b>Key point:</b> <code>sample(1:n, n, replace = TRUE)</code> draws n case numbers with replacement. <code>x[idx]</code> and <code>y[idx]</code> use the same set of numbers, so each person's x and y are drawn together (you resample people, not single numbers).</p>
""" + OUT(RLOG("L8-1_log.txt", "Sample correlation", 4), "Actual output: R/output/L8-1_log.txt"),
quiz=[
("Why does the bootstrap sample with replacement?",
 ["To make the bootstrap sample larger than the original and improve precision",
  "Without replacement you only get the original sample reordered, so the statistic does not change; with replacement you can mimic \"a different group of people\"",
  "To make sure everyone is drawn at least once",
  "To make the bootstrap distribution normal"],
 1,
 ["Each bootstrap sample still has N people; the bootstrap does not make an estimate more precise, it only describes how precise it is.",
  "Correct.",
  "The opposite: with replacement, on average about 37% of people are never drawn, and that is exactly where the differences between samples come from.",
  "The bootstrap neither assumes nor imposes a distribution shape; the percentile interval takes quantiles directly and works even when the distribution is skewed."]),
("What does a very wide bootstrap interval tell you?",
 ["The estimate is more reliable: the interval covers more ground, so it is more likely to contain the population value",
  "The estimate is sensitive to the sample and imprecise",
  "The effect must be 0",
  "Too few bootstrap replicates; raise it to 5,000 and the interval will narrow noticeably"],
 1,
 ["This mixes up \"coverage\" and \"precision\": a wide interval means the estimate would change a lot with a different sample, so precision is low.",
  "Correct.",
  "A wide interval only means imprecision; even if it contains 0, you just cannot rule out 0, which is not the same as the effect being 0.",
  "Plausible but wrong: more replicates only reduce Monte Carlo error and steady the endpoints; the width is set by the sample size and the variability of the statistic itself, so it will not shrink."]),
("Can the bootstrap fix a sample that is itself biased?",
 ["Yes: the bootstrap makes no distributional assumptions",
  "No: it only resamples within the sample you already have",
  "Yes, as long as there are enough bootstrap replicates",
  "Yes, as long as the sample is large enough"],
 1,
 ["\"No distributional assumptions\" refers to the shape of the sampling distribution; it has nothing to do with whether the sample represents the population.",
  "Correct.",
  "More replicates only reduce Monte Carlo error; you are still resampling the same biased people.",
  "A larger sample only narrows the interval; the interval is still centered on the biased sample's estimate, and this bias does not go away as N grows."]),
("In the bootstrap, x[idx] and y[idx] must use the same idx because…",
 ["It saves memory: only one set of random numbers is needed",
  "You are resampling people, so each person's x and y must stay paired",
  "It gives a narrower interval",
  "cor() requires both vectors to have the same indices"],
 1,
 ["Memory is not the reason; a second set of numbers is just one more vector. The real problem is that the pairs get split.",
  "Correct: drawing them separately destroys the relationship, and the correlation drifts toward 0.",
  "Interval width is not the goal; drawing separately gives a distribution around 0, which answers a different question.",
  "cor() only requires the two vectors to have the same length; it runs with different indices, but the result is meaningless."]),
("For large N, roughly what is the probability that a given person is never drawn in a bootstrap sample?",
 ["0", "0.368", "0.5", "0.632"], 1,
 ["Only drawing N times without replacement includes everyone; with replacement some people are always missing.",
  "Correct: (1 − 1/N)^N → 1/e.",
  "No basis for this: each draw picks a given person with probability 1/N, so the probability of missing them in all N draws is (1 − 1/N)^N, not one half.",
  "0.632 is the probability of being drawn at least once, i.e., 1 − 0.368."]),
],
ex=[
("A 15-line bootstrap", "Hands-on",
 r"""<p>Without looking at the code above, write R code that bootstraps a correlation 1,000 times, plot the distribution, compute the 95% interval, and compare it with <code>cor.test()</code>.</p>""",
 r"""<p>Four core steps: <code>r_boot &lt;- numeric(1000)</code> → in a <code>for</code> loop, <code>idx &lt;- sample(n, n, replace = TRUE)</code> → <code>r_boot[b] &lt;- cor(x[idx], y[idx])</code> → <code>quantile(r_boot, c(.025, .975))</code>. With the seed in <code>R/L8-1.R</code>, the course data give [0.234, 0.360]; the reference solution <code>R/solutions/L8-1_solution.R</code> uses seed 2024 and gets [0.232, 0.359], nearly the same as cor.test's [0.232, 0.358]. A different seed changes the result slightly in the third decimal. This seed-to-seed difference is called Monte Carlo error: it comes from doing only a finite number (B) of resamples and shrinks as B grows. It is a different thing from the sampling variability set by the sample size.</p>"""),
("A wrong version", "Understanding",
 r"""<p>If you wrote <code>cor(sample(x, replace = TRUE), sample(y, replace = TRUE))</code>, what would the bootstrap distribution look like, and why?</p>""",
 r"""<p>x and y are shuffled separately, so the pairing is destroyed and the bootstrap correlations cluster around 0 (roughly within ±0.07). This is close to the null distribution of a permutation test (a proper permutation test shuffles one of the columns without replacement), not an estimate of the sampling distribution of r.</p>"""),
("Sample size and interval width", "Understanding",
 r"""<p>In the demo on this page, fix ρ = 0.3 and run 1,000 bootstrap replicates with N = 50, 200 and 400, recording the interval width each time. Roughly how does the width depend on N? In a sentence or two, how does this relate to "network analysis especially needs accuracy checks"?</p>""",
 r"""<p>The width is roughly proportional to \(1/\sqrt{N}\): going from N = 50 to 200 (4 times as many) about halves it. The reference solution <code>R/solutions/L8-1_solution.R</code> (averaging 20 samples per N) gets 0.466 at N = 50, 0.248 at N = 200 and 0.171 at N = 400; width × √N stays around 3.3–3.5 throughout (exact values depend on the random samples). This is why network studies need fairly large samples. The link to networks: a 9-node CLPN estimates 81 coefficients at once, and each one's interval width follows the same 1/√N rule, while cross-lagged edges are often only 0.05–0.15, so a slightly wider interval already crosses 0. On top of that, LASSO may select or drop an edge in each resample, so a single estimated network easily looks more certain than it is. That is why you check it with the intervals of Lesson 8.2 and the CS-coefficient of Lesson 8.3.</p>"""),
],
summary=["Bootstrap = draw N people from the sample with replacement, recompute the statistic, repeat, and use the distribution to describe sampling variability.", "Percentile interval = the 2.5th and 97.5th percentiles; bootstrap SE = the standard deviation of the distribution.", "About 37% (1/e) of people are missing from each bootstrap sample.", "The bootstrap cannot fix sample bias, measurement error or confounding.", "Many network parameters, limited samples → accuracy and stability checks are a must."],
refs=["Epskamp, S., Borsboom, D., & Fried"],
)
