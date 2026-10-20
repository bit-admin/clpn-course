# -*- coding: utf-8 -*-
# M9 module quiz: reading, critique and reporting standards (Week 15, after Lesson 9.3)
LEAD = "<p>Take this after Lessons 9.1–9.3 (Week 15 of the standard pace). 6 auto-graded questions + 1 short-answer question, about 20 minutes.</p>"
ITEMS = [
dict(obj="9.1-1", q="""Q: When you read a CLPN paper with a structured checklist, which of the following is <b>not</b> among the information to extract first?
- The sample size and the interval between waves || Must be extracted.
- The λ selection rule (e.g. <code>lambda.min</code>, EBIC) || Must be extracted.
- The stability results (CS-coefficients, bootstrap intervals) || Must be extracted.
+ The population of the authors' city || Correct. It has nothing to do with judging the study's methods.
E: For the structured checklist for reading CLPN papers, see <a href="../lessons/L9-1.html">9.1</a>."""),
dict(obj="9.1-3", q="""Q: A paper's results show that the edge "T1 loneliness → T2 fatigue" is the strongest, and the Discussion says: "This shows that loneliness causes fatigue by draining psychological energy." What is this sentence?
- The authors' finding || The finding is that "this edge is the strongest."
+ The authors' interpretation (a guess at a mechanism); the data never tested the "draining psychological energy" mechanism || Correct.
- A stability result || No.
- Descriptive statistics || No.
E: For telling findings, interpretations and over-reaching inferences apart, see <a href="../lessons/L9-1.html">9.1</a>."""),
dict(obj="9.2-1", q="""Q: Which sentence is the most typical example of "over-reading centrality" in a CLPN paper?
- "The CS-coefficient of out-EI was 0.52." || This is a factual report.
+ "'Worthlessness' had the highest out-EI and is therefore the core treatment target; intervening on it can break up the whole symptom network." || Correct. It turns predictive centrality into an intervention effect.
- "This study did not test measurement invariance." || This is an honest statement of a limitation.
- "The edges of the T1→T2 and T2→T3 networks correlated at .61." || This is a factual report.
E: For common over-readings, see <a href="../lessons/L9-2.html">9.2</a>."""),
dict(obj="9.2-2", q="""Q: A network includes both "I feel sad" and "I feel down" as nodes, with a very strong edge between them. What should you be most wary of?
- The sample being too large || It has nothing to do with sample size.
+ The two items overlap almost completely in content (they measure the same thing); the strong edge may just say the same thing twice and inflates the centrality of the nodes involved || Correct.
- The two items should be drawn in different colors || Colors cannot fix overlapping content.
- This edge proves that sadness causes feeling down || No.
E: For choosing nodes and overlapping item content, see <a href="../lessons/L9-2.html">9.2</a>."""),
dict(obj="9.3-1", q="""Q: The course recommends a set of reporting standards for psychological network analysis (for cross-sectional networks, published in Psychological Methods in 2023). What is the first author's surname?
T: Burger||burger
H: The main reference of Lesson 9.3: B______ et al. (2023).
E: The reporting standards of Burger et al. (2023) are written for cross-sectional networks; Lesson 9.3 shows how to carry them over to a CLPN. See <a href="../lessons/L9-3.html">9.3</a>."""),
dict(obj="9.3-3", q="""Q: What is the core purpose of preregistration?
- To guarantee significant results || Preregistration guarantees no result.
+ To write down your research questions and analysis plan publicly before you see the results, so readers can tell planned analyses from after-the-fact exploration || Correct.
- To get published by a journal for free || Irrelevant.
- To replace ethics approval || It cannot.
E: For the basics of preregistration and sharing code and data, see <a href="../lessons/L9-3.html">9.3</a>. The analysis plan of the capstone project (10.1) is a simple preregistration."""),
]
SHORT = [
dict(obj="9.2-3", q="<p>Read this made-up abstract and point out at least three things to question, explaining each in one sentence:</p><blockquote>\"We surveyed 120 college students in March 2023 and April 2023 (1-month interval) and estimated a CLPN with 20 nodes using lambda.min. 'Helplessness' had the highest out-EI and is the root cause of depression. All cases with missing data were deleted.\"</blockquote>",
     answer="<p>Things to question (any three are enough): (1) <b>Sample size</b>: 20 nodes give 380 cross-lagged edges, and 120 people are far too few; the estimates will be very unstable. (2) <b>No stability checks</b>: the out-EI ranking is interpreted without reporting bootstrap intervals or CS-coefficients. (3) <b>Causal language</b>: \"root cause\" is a causal conclusion, while a CLPN only gives prediction over time. (4) <b>Missing data</b>: cases with missing data were simply deleted, without reporting the missing proportion or an attrition analysis, which may cause bias. (5) <b>Interval</b>: whether a 1-month interval fits the process being studied needs a justification. (6) <b>λ rule</b>: <code>lambda.min</code> is lenient and gives more false positives, so a sensitivity analysis should be reported. (7) There is no mention that between-person and within-person effects are mixed together.</p>",
     rubric=[(3, "Points out at least three problems, each with a correct reason (sample size / stability / causal language / missing data / interval / λ rule / within- vs between-person)"),
             (2, "Points out three problems, but one reason is inaccurate; or only two, with sound reasons"),
             (1, "Points out only one problem"),
             (0, "No answer, or none of the reasons hold")]),
]
