# -*- coding: utf-8 -*-
# M1 module quiz: statistical foundations (Week 5, together with M2)
LEAD = "<p>Take this after Lessons 1.1–1.6 (Week 5 of the standard pace, together with the M2 module quiz). 10 auto-graded questions + 1 short-answer question, about 20 minutes. You may use a calculator.</p>"
ITEMS = [
dict(obj="1.1-2", q="""Q: Each item on a loneliness scale is answered "1 never, 2 rarely, 3 sometimes, 4 often." Researchers often treat these answers as continuous numbers and compute means and correlations. Which view is most accurate?
- This is simply wrong; Likert items can only be counted || It is very common in published research, so not "simply wrong."
+ Strictly, the data are ordinal; treating them as continuous is a common approximation that is debated, and the fewer the response options, the stronger the objection || Correct.
- Likert items are ratio data to begin with || Ratio data need a true zero and equal intervals.
- With a large enough sample, ordinal data automatically become interval data || Sample size does not change the level of measurement.
E: For how to handle Likert items and the debate around it, see <a href="../lessons/L1-1.html">1.1</a>."""),
dict(obj="1.1-3", q="""Q: Item 3 of the UCLA Loneliness Scale, the total score on that scale, and "loneliness" itself are, in that order:
+ Item, scale score, construct || Correct. CLPN nodes are usually items, not total scores.
- Construct, item, scale score || Wrong order.
- Different names for the same thing || The three sit at different levels.
- Scale score, construct, item || Wrong order.
E: For the difference between items, scale scores and constructs, see <a href="../lessons/L1-1.html">1.1</a>."""),
dict(obj="1.2-1", q="""Q: Seven clients asked for help this many times in one week: 0, 1, 1, 2, 3, 3, 11. What is the median?
N: 2 | 0
H: Sort the values from smallest to largest, then find the one in the middle.
E: After sorting, the 4th value is the median: 2. The mean is 3, pulled up by the extreme value 11; see <a href="../lessons/L1-2.html">1.2</a>."""),
dict(obj="1.2-2", q="""Q: On a depression screening scale in a community sample, most people score 0–3 and a few score very high. This distribution is most likely:
- Left-skewed, with the mean below the median || The tail is on the right (high-score end), so it is not left-skewed.
+ Right-skewed (positively skewed), with the mean above the median || Correct. The few high scores pull the mean to the right.
- Normal || A normal distribution is symmetric.
- Uniform || In a uniform distribution, every score has about the same number of people.
E: Symptom scales in community samples are often right-skewed and may show a floor effect; see <a href="../lessons/L1-2.html">1.2</a>."""),
dict(obj="1.2-3", q="""Q: A life satisfaction scale is roughly normally distributed with mean 50 and standard deviation 10. About what percentage of people score between 30 and 70? (Enter a number only)
N: 95 | 1
H: How many standard deviations from the mean are 30 and 70?
E: 30 and 70 are each 2 standard deviations from the mean; by the 68–95–99.7 rule that is about 95%. See <a href="../lessons/L1-2.html">1.2</a>."""),
dict(obj="1.3-1", q="""Q: Xiao Wang's social support score is 65. The sample mean is 50 and the standard deviation is 6. What is his z-score?
N: 2.5 | 0.01
H: z = (raw score − mean) ÷ standard deviation.
E: (65 − 50) ÷ 6 = 2.5, i.e. 2.5 standard deviations above the mean; see <a href="../lessons/L1-3.html">1.3</a>."""),
dict(obj="1.4-2", q="""Q: A study reports that "the correlation between weekly volunteer hours and depression score is r = −0.30." What is the best interpretation?
- Each additional hour of volunteering lowers depression by 0.30 points || r has no units; it is not "points per extra hour."
+ A weak-to-moderate negative correlation: people who volunteer more hours tend to have lower depression scores || Correct.
- 30% of people became less depressed || r is not a percentage.
- The two are unrelated, because r is negative || The minus sign gives the direction; it does not mean "no relationship."
E: The sign of r gives the direction and its absolute value gives the strength; see <a href="../lessons/L1-4.html">1.4</a>."""),
dict(obj="1.5-3", q="""Q: A study estimates college students' mean loneliness score at 2.4, with a 95% confidence interval of [2.3, 2.5]. Which interpretation is correct?
- 95% of college students have loneliness scores between 2.3 and 2.5 || A confidence interval describes uncertainty about the mean, not the range of individual scores.
- The true mean has a 95% probability of falling in this interval || A common misreading: for an interval that has already been computed, the true value is either in it or not.
+ If you repeated the sampling many times with the same method and computed an interval each time, about 95% of those intervals would contain the true mean || Correct.
- The mean in the next survey will certainly be between 2.3 and 2.5 || Nothing here is certain.
E: For the correct interpretation of confidence intervals and common misreadings, see <a href="../lessons/L1-5.html">1.5</a>."""),
dict(obj="1.6-2", q="""Q: An intervention study reports p = 0.03. Which statement is correct?
- The probability that the intervention works is 97% || A p-value is not the probability that a hypothesis is true.
- There is a 3% chance that the result is wrong || This is another common misreading.
+ If the intervention actually had no effect (the null hypothesis is true), the probability of a difference this large or larger would be about 3% || Correct.
- The effect is large || A small p-value does not mean a large effect.
E: For what a p-value means and common misreadings, see <a href="../lessons/L1-6.html">1.6</a>."""),
dict(obj="1.6-4", q="""Q: A researcher tests the correlation of 40 pairs of variables one by one, each at α = 0.05. Even if none of the variables are actually related, how many pairs will be "significant" on average?
N: 2 | 0
H: Each test has a 5% chance of a false positive.
E: 40 × 0.05 = 2. The more tests, the more false positives: this is the multiple comparisons problem. A network analysis estimates dozens of edges at once, which is why it uses regularization; see <a href="../lessons/L1-6.html">1.6</a>."""),
]
SHORT = [
dict(obj="1.6-3", q="<p>Two studies both found that \"people who join a support group are less depressed.\" Study A: N = 5000, p &lt; .001, Cohen's d = 0.08. Study B: N = 60, p = .04, d = 0.55. In 3–4 sentences, explain to an agency director which study's effect deserves more attention, and how \"significant\" differs from \"important.\"</p>",
     answer="<p>Study A is highly significant mainly because its sample is very large; but d = 0.08 means the difference between the groups is tiny, so its practical meaning is limited. Study B's effect size, d = 0.55, is a medium-sized difference with more practical meaning, but its sample is small, so the estimate is imprecise (wide confidence interval) and needs to be replicated. \"Significant\" only says the difference is unlikely to come entirely from sampling error; \"important\" depends on how large the effect is and what it means for clients.</p>",
     rubric=[(3, "Points out that A's significance comes mainly from its large sample and its effect is tiny; that B's effect is medium but its sample is small and needs replication; and explains clearly that significant ≠ important"),
             (2, "Compares the two effect sizes but does not mention the role of sample size or B's uncertainty"),
             (1, "Looks only at p-values and calls A more important; or only says significant ≠ important without using the numbers"),
             (0, "No answer, or wrong conclusion")]),
]
