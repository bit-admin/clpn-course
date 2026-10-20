# -*- coding: utf-8 -*-
# M5 module quiz: the traditional cross-lagged panel model (Week 10, after Lesson 5.4)
LEAD = "<p>Take this after Lessons 5.1–5.4 (Week 10 of the standard pace). 10 auto-graded questions + 1 short-answer question, about 20 minutes. You don't need to open R.</p>"
ITEMS = [
dict(obj="5.1-1", q="""Q: A two-variable (loneliness L, depression D), three-wave CLPM is drawn with only the one-way arrows between adjacent waves (no same-wave correlations). How many directed regression paths are there in total?
N: 8 | 0
H: Count separately: L to itself and D to itself (autoregressive), and L to D and D to L (cross-lagged). How many are there between each pair of adjacent waves, and how many pairs of adjacent waves are there?
E: Each pair of adjacent waves (T1→T2, T2→T3) has 2 autoregressive + 2 cross-lagged paths = 4 paths; the two pairs give 8 in total. For the path diagram, see <a href="../lessons/L5-1.html">5.1</a>."""),
dict(obj="5.1-2", q="""Q: In a CLPM, the coefficient for "T1 loneliness → T2 loneliness" is 0.65. What does it mainly tell you?
- Loneliness causes depression || This is a path from loneliness to loneliness; it has nothing to do with depression.
+ Loneliness is fairly stable over six months: people who were lonelier at T1 tend to still be lonelier at T2 || Correct. This is an autoregressive path, and it shows stability.
- 65% of people are lonely || A coefficient is not a percentage.
- 65% of T2 loneliness comes from depression || Both the direction and the meaning are wrong.
E: An autoregressive (AR) path shows how stable the same variable is over time; it is the cross-lagged (CL) paths that capture "one variable predicting another." See <a href="../lessons/L5-1.html">5.1</a>."""),
dict(obj="5.1-3", q="""Q: In a CLPM, what does the two-headed arrow (residual covariance) between T2 loneliness and T2 depression represent?
- T2 loneliness causes T2 depression || A two-headed arrow has no direction and is not causal.
- The correlation between T1 loneliness and T1 depression || That is the covariance between the two T1 variables.
+ The co-variation the two still share at the same time point after the T1 predictions are taken out || Correct. It often reflects influences that happen at the same time, or shared outside events.
- A sign that the model failed to estimate || It is a normal part of the model.
E: For what same-wave residual correlations mean, see <a href="../lessons/L5-1.html">5.1</a>."""),
dict(obj="5.1-4", q="""Q: In a path diagram (SEM diagram), what statistic does a curved line with arrowheads at both ends represent? (One or two words)
T: covariance||correlation||covariance or correlation||correlation or covariance||covariation||co-variation
H: A one-headed arrow is a regression (prediction); a two-headed arrow has no direction and means the two "vary together."
E: One-headed arrow = regression path; two-headed arrow = covariance (a correlation once standardized). For the diagram conventions, see <a href="../lessons/L5-1.html">5.1</a>."""),
dict(obj="5.2-1", q="""Q: In lavaan model syntax, how do you write "T2 depression is predicted by T1 loneliness and T1 depression"?
+ <code>dep2 ~ lone1 + dep1</code> || Correct. <code>~</code> means regression, with the outcome on the left.
- <code>dep2 ~~ lone1 + dep1</code> || <code>~~</code> means (residual) covariance.
- <code>dep2 =~ lone1 + dep1</code> || <code>=~</code> defines which items measure a latent variable (factor).
- <code>lone1 + dep1 ~ dep2</code> || The outcome goes on the left.
E: The three basic lavaan operators: <code>~</code> regression, <code>~~</code> covariance, <code>=~</code> measurement. See <a href="../lessons/L5-2.html">5.2</a>."""),
dict(obj="5.2-2", q="""Q: A CLPM's fit: CFI = .97, RMSEA = .12 (90% CI .09–.15), SRMR = .04. Which write-up is most appropriate?
- The model fits well because CFI is above .95 || Picking only the indices that look good is a common reporting error.
- The model is completely unusable because RMSEA is above .08 || One poor index does not make the whole model "completely unusable," but it needs careful discussion.
+ The indices disagree: CFI and SRMR are acceptable, RMSEA is poor. Report all the indices and discuss possible reasons (e.g. very few degrees of freedom, or omitted paths) || Correct.
- Reporting SRMR alone is enough || Report them all.
E: For what the fit indices mean and the usual reference values, see <a href="../lessons/L5-2.html">5.2</a>. The reference values are only rules of thumb; when indices conflict, report them honestly and discuss them."""),
dict(obj="5.2-3", q="""Q: A researcher compares two nested models: with all paths freely estimated, χ² = 52.1, df = 8; with the cross-lagged paths set equal across the two intervals, χ² = 60.4, df = 10. What are the degrees of freedom of the chi-square difference test?
N: 2 | 0
H: The df of the difference test = the difference between the two models' df.
E: Δdf = 10 − 8 = 2 (Δχ² = 8.3). For equality constraints and the chi-square difference test, see <a href="../lessons/L5-2.html">5.2</a>. With a robust estimator (such as MLR), Δχ² needs a scaling correction with <code>lavTestLRT()</code>; you cannot simply subtract."""),
dict(obj="5.3-2", q="""Q: What does the "random intercept" in an RI-CLPM represent?
- The measurement error at each wave || Measurement error is not the random intercept.
+ Trait-like differences between people that stay stable across all waves || Correct. Once it is separated out, what remains is within-person fluctuation around each person's own average.
- The effect of depression on loneliness || That is a cross-lagged path.
- The sample mean || The mean is the overall average, not each person's random intercept.
E: For the random intercept and the within-person part, see <a href="../lessons/L5-3.html">5.3</a> (Hamaker et al., 2015)."""),
dict(obj="5.3-4", q="""Q: To separate out the random intercept (stable personal traits), how many waves of data does an RI-CLPM need at minimum?
N: 3 | 0
H: With two waves, stable traits and change between waves cannot be estimated separately.
E: An RI-CLPM needs at least 3 waves; see <a href="../lessons/L5-3.html">5.3</a>."""),
dict(obj="5.4-1", q="""Q: A CLPM shows that "T1 loneliness significantly predicts T2 depression (β = .15)." Which statement is most accurate?
- Loneliness causes depression, so reducing loneliness will lower depression || This is a causal, interventional conclusion that a CLPM cannot support on its own.
- Each person's loneliness makes that same person more depressed six months later || This is an individual-level, within-person conclusion, but a CLPM mixes in between-person information.
+ Controlling for T1 depression, people with higher T1 loneliness tend to have higher T2 depression; this is a predictive relationship over time and may be affected by unmeasured confounding and other factors || Correct.
- Depression does not affect loneliness || You looked at only one path; you cannot conclude the other direction is absent.
E: For the difference between Granger-style "prediction over time" and a causal effect, and the main threats (confounding, the length of the interval, measurement error), see <a href="../lessons/L5-4.html">5.4</a>."""),
]
SHORT = [
dict(obj="5.4-3", q="<p>Here is a passage from a student's results: \"The CLPM results prove that loneliness is a cause of depression: for every one-unit increase in loneliness, depression six months later increases by 0.15 units. Therefore, social work agencies should prioritize interventions on loneliness.\" Point out two problems in it and rewrite it as a cautious, accurate statement (3–4 sentences).</p>",
     answer="<p>Problems: (1) \"Prove ... a cause\" is causal language. A CLPM can only show a predictive relationship over time, which may be affected by unmeasured confounding (e.g. family hardship affecting both), the choice of interval, and measurement error. (2) \"For every one-unit increase in loneliness ... increases\" turns a group-level regression coefficient into a change within each person, and a CLPM also mixes between-person and within-person information. (3) \"Should prioritize interventions on loneliness\" is an intervention recommendation that goes beyond what observational data can support.</p><p>Sample rewrite: \"Controlling for T1 depression, T1 loneliness significantly predicted T2 depression (β = .15): people who were lonelier at Wave 1 tended to be more depressed six months later. This is a predictive relationship over time and cannot be read directly as a causal effect; because the CLPM does not separate out stable personal traits, it also does not describe a change process within individuals. Whether loneliness deserves to be a priority for intervention needs further testing with intervention studies or methods such as the RI-CLPM.\"</p>",
     rubric=[(3, "Points out at least two problems among the causal language, the individual-level reading and the intervention recommendation; the rewrite removes the causal and individual-level wording, keeps the number, and states the limitations"),
             (2, "Points out two problems, but the rewrite still overstates once or lacks the limitations"),
             (1, "Points out only one problem, or the rewrite is still causal"),
             (0, "No answer, or says the original has no problem")]),
]
