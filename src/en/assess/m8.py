# -*- coding: utf-8 -*-
# M8 module quiz: stability and accuracy (Week 14, after Lesson 8.3)
LEAD = "<p>Take this after Lessons 8.1–8.3 (Week 14 of the standard pace). 8 auto-graded questions + 1 short-answer question, about 20 minutes. You don't need to open R.</p>"
ITEMS = [
dict(obj="8.1-1", q="""Q: You run a nonparametric bootstrap on a sample of N = 200. How is each bootstrap sample drawn?
- 100 people drawn without replacement || The sample must be the same size as the original, and drawn with replacement.
+ 200 people drawn with replacement: some people are drawn several times, and some not at all || Correct.
- 200 new participants recruited || A bootstrap collects no new data.
- The 200 people's scores shuffled into a new order || That is closer to a permutation (7.7) than to a bootstrap.
E: For how the nonparametric bootstrap works, see <a href="../lessons/L8-1.html">8.1</a>."""),
dict(obj="8.1-2", q="""Q: You ran 1000 bootstrap samples and sorted the 1000 correlation coefficients from smallest to largest. Which value in the sorted list is the lower limit of the 95% percentile interval?
N: 25 | 0
H: 2.5% is cut off at each end. What is 2.5% of 1000?
E: 1000 × 2.5% = 25, so the lower limit is the 25th value and the upper limit the 975th. See <a href="../lessons/L8-1.html">8.1</a>."""),
dict(obj="8.1-3", q="""Q: Why does network analysis particularly need accuracy (stability) checks?
- Because network analysis cannot compute p-values || That is not the main reason.
+ A network estimates dozens of edges at once; with a limited sample, each edge and the centrality ranking can vary a lot from sample to sample, so it is easy to over-read a single plot || Correct.
- Because network plots look bad || Looks have nothing to do with it.
- Only when the sample exceeds 10000 || Quite the opposite: it is most needed when the sample is limited.
E: For why network analysis needs accuracy checks, see <a href="../lessons/L8-1.html">8.1</a> (Epskamp et al., 2018)."""),
dict(obj="8.2-2", q="""Q: A cross-lagged edge has an estimate of 0.08 and a bootstrap interval of [0.00, 0.17]. Which interpretation is most appropriate?
- This edge is very stable and can be a main finding || The lower limit is 0, so at least 2.5% of the bootstrap samples set it to 0; it is hardly "very stable."
+ The estimate of this edge is not very stable: at least 2.5% of the resamples set it to 0, so interpret it with caution || Correct. A lower limit of 0 only tells you that at least 2.5% of the samples were 0; for the actual proportion, look at the proportion of zeros (prop0).
- The interval contains 0, so this edge certainly does not exist in the population || "Unstable" does not mean "certainly absent."
- The wider the interval, the better || A wider interval means a less precise estimate.
E: For how to read edge-weight bootstrap intervals, see <a href="../lessons/L8-2.html">8.2</a>."""),
dict(obj="8.2-4", q="""Q: Why does the course say the bootstrap intervals of LASSO-estimated CLPN edges "cannot be treated as strict confidence intervals"?
+ LASSO shrinks estimates toward 0, so the bootstrap distribution often piles up many values at 0; the interval is pulled toward 0, and its coverage is not guaranteed to be 95% || Correct.
- Because there were too few bootstrap samples || No number of samples fixes the bias that shrinkage causes.
- Because confidence intervals can only be used for means || Confidence intervals can be used for many statistics.
- Because CLPN edges have no direction || CLPN edges do have a direction, and that has nothing to do with the question.
E: For what to keep in mind about bootstrap intervals under regularized estimation, see <a href="../lessons/L8-2.html">8.2</a>."""),
dict(obj="8.2-3", q="""Q: The bootstrap intervals of two edges partly overlap. You want to know whether "edge A is significantly stronger than edge B." What should you do?
- Check whether the two intervals overlap: overlap means no difference || Overlapping intervals do not by themselves show that the difference is not significant.
+ Use the edge-weight difference test: check whether the bootstrap interval of "A − B" contains 0 || Correct.
- Compare the two edges' p-values || Separate p-values cannot compare two edges.
- Add the two edges together || Irrelevant.
E: For the edge-weight difference test, see <a href="../lessons/L8-2.html">8.2</a>."""),
dict(obj="8.3-2", q="""Q: By the rule of thumb of Epskamp et al. (2018), the CS-coefficient of a centrality index <b>should not be below</b> what value?
N: 0.25 | 0.001
H: There is also a "preferably above" value of 0.5.
E: CS should not be below 0.25 and preferably above 0.5. This is a rule of thumb based on simulation studies, not a mathematical theorem. See <a href="../lessons/L8-3.html">8.3</a>."""),
dict(obj="8.3-1", q="""Q: What does the case-dropping bootstrap do?
- Drops the cases with the most missing values || The dropping is random, not chosen by missingness.
+ Randomly drops a growing share of the sample (e.g. 10%, 20%, ...), re-estimates each time, and checks how highly the centrality ranking still correlates with the original sample's || Correct.
- Drops the strongest edges || It drops people, not edges.
- Drops nonsignificant nodes || No.
E: For the case-dropping bootstrap and the CS-coefficient, see <a href="../lessons/L8-3.html">8.3</a>."""),
]
SHORT = [
dict(obj="8.3-3", q="<p>A CLPN study reports: CS-coefficient of in-EI = 0.44, CS-coefficient of out-EI = 0.13. In the Discussion the authors write: \"'No one understands me,' which has the highest out-EI, is the most important intervention target.\" In 3–4 sentences, evaluate this sentence and give the wording you would recommend.</p>",
     answer="<p>The CS of out-EI is 0.13, below the minimum of 0.25, so the out-EI ranking is very unstable: drop a small random part of the sample and the top-ranked node may change. You therefore cannot pick out the \"most important\" node from the out-EI ranking. Even if it were stable, a high out-EI only means the node predicts many other nodes over time; it does not mean that intervening on it would improve the other symptoms (causal and intervention claims need experiments or intervention studies). The CS of in-EI is 0.44, so its ranking can be interpreted with caution (it lies between 0.25 and 0.5). Recommended wording: \"The stability of out-EI was insufficient (CS = 0.13), and we do not interpret its ranking; the stability of in-EI was acceptable (CS = 0.44), ... and may serve as a reference for future research and follow-up monitoring.\"</p>",
     rubric=[(3, "Points out that the out-EI CS is below 0.25 so the ranking cannot be interpreted, points out that \"intervention target\" over-reads the result in causal / intervention terms, and gives a reasonable rewrite"),
             (2, "Points out the low CS but not the problem with the intervention language (or vice versa); the rewrite is mostly reasonable"),
             (1, "Only says \"the CS is a bit low,\" without explaining what follows or giving a rewrite"),
             (0, "No answer, or says the original has no problem")]),
]
