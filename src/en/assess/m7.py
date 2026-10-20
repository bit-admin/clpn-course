# -*- coding: utf-8 -*-
# M7 module quiz: the cross-lagged panel network (Week 13, after Lesson 7.5). Plus 4 optional advanced questions (7.6 / 7.7), not counted in the 10.
LEAD = "<p>Take this after Lessons 7.1–7.5 (Week 13 of the standard pace). 10 auto-graded questions + 1 short-answer question, about 25 minutes. At the end of the page are 4 <b>optional advanced questions</b>; do them after Lessons 7.6 and 7.7. They do not count toward this module's score.</p>"
ITEMS = [
dict(obj="7.1-2", q="""Q: The course data have 9 nodes (4 loneliness items, 5 depression items). How many regression equations do you fit to estimate a T1 → T2 CLPN?
N: 9 | 0
H: A CLPN is estimated "nodewise": each T2 node gets its own regression equation.
E: 9 T2 nodes, each predicted from all 9 T1 nodes: 9 regressions in total. See <a href="../lessons/L7-1.html">7.1</a>."""),
dict(obj="7.1-3", q="""Q: In the same 9-node CLPN, how many cross-lagged edges (not counting autoregressive edges) does the weights matrix B contain?
N: 72 | 0
H: B is a 9 × 9 matrix; the autoregressive edges are on the diagonal.
E: 9 × 9 = 81 cells, minus the 9 autoregressive edges on the diagonal, leaves 72 cross-lagged edges. See <a href="../lessons/L7-1.html">7.1</a>."""),
dict(obj="7.1-4", q="""Q: The course convention is that <code>B[k, j]</code> means "k at T1 → j at T2." If <code>B["lone2", "dep3"]</code> = 0.12, which reading is correct?
+ Controlling for all 9 T1 nodes (including dep3 at T1 itself), people with higher lone2 at T1 tend to have higher dep3 at T2 || Correct.
- dep3 at T1 predicts lone2 at T2 || The direction is reversed: rows are the T1 predictors, columns are the T2 outcomes.
- The partial correlation between lone2 and dep3 at the same time point is 0.12 || A CLPN edge is a directed regression coefficient across time.
- lone2 causes dep3 to rise by 12% || It is neither causal nor a percentage.
E: For what a CLPN edge means, see <a href="../lessons/L7-1.html">7.1</a>; for wording an interpretation, see Lesson 7.3."""),
dict(obj="7.1-1", q="""Q: What is the main difference between a CLPN and a CLPM?
- A CLPN does not need longitudinal data || A CLPN needs panel data with at least two waves.
+ A CLPN breaks the constructs down to the item level: each item is a node, so you can see which loneliness item predicts which depression item || Correct.
- A CLPN can prove causation and a CLPM cannot || Both give only predictive relationships over time.
- A CLPN automatically separates within-person and between-person effects || A standard CLPN, like a CLPM, does not separate them (see 7.5).
E: For how the CLPN relates to the CLPM and to cross-sectional networks, see <a href="../lessons/L7-1.html">7.1</a>."""),
dict(obj="7.2-1", q="""Q: Why do you standardize each item (z-scores) before running nodewise LASSO?
- To make the data normally distributed || Standardizing does not change the shape of a distribution.
+ The LASSO penalty treats every coefficient the same, so variables on different scales would be penalized unfairly; standardized coefficients are also easier to compare || Correct.
- To remove missing values || Standardizing does nothing about missing data.
- After standardizing you no longer need to choose λ || You still need to choose λ.
E: For why to standardize, see <a href="../lessons/L7-2.html">7.2</a> and 3.5."""),
dict(obj="7.2-3", q="""Q: When you estimate a CLPN with <code>cv.glmnet()</code> and switch the λ rule from <code>lambda.min</code> to <code>lambda.1se</code>, what usually happens to the network?
- More edges || The opposite direction.
+ Fewer edges, a sparser network: <code>lambda.1se</code> chooses a larger penalty || Correct. It is more conservative, with fewer false positives, but may also miss weak true edges.
- Exactly the same result || The two rules choose different λ values.
- The autoregressive edges disappear || Not necessarily, and that is not the main difference between the two.
E: For the trade-off between <code>lambda.min</code> and <code>lambda.1se</code>, see <a href="../lessons/L7-2.html">7.2</a>. Whichever you use, state it in your analysis plan in advance."""),
dict(obj="7.2-3", q="""Q: The cross-validation in <code>cv.glmnet()</code> splits the data into folds at random. So that others (and your future self) can reproduce exactly the same CLPN, which R function must you call before running it? (Function name)
T: set.seed||set.seed()||set.seed(2026)
H: Its name contains "seed."
E: Write a line such as <code>set.seed(2026)</code> before running, and report the seed in your Methods. See <a href="../lessons/L7-2.html">7.2</a>."""),
dict(obj="7.4-1", q="""Q: In a CLPN weights matrix, the nonzero coefficients in row lone4 (lone4 at T1 predicting each node at T2) are: →lone4 0.40 (autoregressive), →dep1 0.10, →dep2 0.05, →dep4 −0.02; all others are 0. What is lone4's out-expected influence (out-EI, counting only cross-lagged edges)?
N: 0.13 | 0.001
H: out-EI adds the coefficients of the cross-lagged edges in that row as they are (keeping the signs), without the autoregressive edge on the diagonal.
E: 0.10 + 0.05 − 0.02 = 0.13. The autoregressive 0.40 is not counted. See <a href="../lessons/L7-4.html">7.4</a>."""),
dict(obj="7.4-2", q="""Q: "Depressed mood (dep1)" has the highest in-expected influence (in-EI) of the 9 nodes. Which statement is most appropriate?
- dep1 is the core symptom that causes the other symptoms || That would be over-reading out-EI, and it is still causal language.
+ dep1 is the node most easily predicted by the other nodes at T1; it may be a "convergence point" worth monitoring at follow-up, but this is not a causal conclusion, and its stability still has to be checked || Correct.
- Intervening on dep1 will lower all the symptoms || Observational data cannot support an intervention conclusion like this.
- A high in-EI means dep1 is measured most accurately || It has nothing to do with measurement precision.
E: For what "predictive" and "predictable" nodes mean and their limits, see <a href="../lessons/L7-4.html">7.4</a>; for stability testing, see Lesson 8.3."""),
dict(obj="7.5-2", q="""Q: How does the course recommend adding age and gender as covariates in a CLPN?
- Draw them as nodes in the network too || Covariates are usually not nodes.
+ Add them to each regression as extra predictors without a penalty (so LASSO cannot push them to 0), and state in the results which covariates were included || Correct.
- With covariates added, you no longer need to standardize || The items still need to be standardized.
- Covariates must be continuous || Binary variables such as gender work too.
E: For how to add covariates and why, see <a href="../lessons/L7-5.html">7.5</a>."""),
# ---- Optional advanced questions (7.6 / 7.7), not counted toward this module's score ----
dict(obj="7.6-3", adv=True, q="""Q: Before you use CLPNs to compare the edges of the T1→T2 and T2→T3 networks, which level of measurement invariance do you most need to establish first?
- Configural invariance is enough || Configural invariance only says "the structure is the same"; it does not guarantee that each item is related to the latent trait equally strongly.
+ Metric (loading) invariance: each item reflects the latent trait equally strongly at every wave, so the edges can be compared || Correct. Scalar (intercept) invariance is what you need to compare means.
- Scalar invariance is enough || Scalar invariance is the prerequisite for comparing means; comparing edges first requires equal loadings.
- No invariance is needed || If an item's meaning drifts, a change in the edges may just be a change in measurement.
E: For what loading invariance and intercept invariance are each a prerequisite for, see <a href="../lessons/L7-6.html">7.6</a>."""),
dict(obj="7.6-4", adv=True, q="""Q: When you use simulation to estimate "how many people are needed to detect the target edges," which of the following is <b>not</b> an assumption the estimate depends on?
- The assumed "true network" (how strong the edges are and how many there are) || This is the most important assumption.
- Which λ rule is used || <code>lambda.min</code> and <code>lambda.1se</code> give different results.
- The number of nodes || The more nodes, the more people you need.
+ The participants' names || Correct. This has nothing to do with sample size planning.
E: For sample size simulation and the assumptions it depends on, see <a href="../lessons/L7-6.html">7.6</a>."""),
dict(obj="7.7-2", adv=True, q="""Q: You ran 999 permutations, and in 24 of them the shuffled M was ≥ the observed M. Using the course formula, what is the permutation p-value?
N: 0.025 | 0.0005
H: p = (number of times ≥ the observed value + 1) / (number of permutations + 1).
E: (24 + 1) / (999 + 1) = 0.025. See <a href="../lessons/L7-7.html">7.7</a>."""),
dict(obj="7.7-4", adv=True, q="""Q: Comparing the CLPNs of 150 urban and 150 rural older adults, the M test gives p = .38. What is the most appropriate conclusion?
- Urban and rural older adults have the same loneliness–depression network || Not significant ≠ the same.
+ There is no evidence that the two groups' networks differ; with only 150 people per group, the test probably lacks power || Correct.
- There were too many permutations; use fewer || The number of permutations does not fix a lack of power.
- Try again with a different random seed || Changing the seed to pick a result is p-hacking.
E: For "not significant ≠ the same" and sample size in group comparisons, see <a href="../lessons/L7-7.html">7.7</a>."""),
]
SHORT = [
dict(obj="7.3-4", q="<p>In a CLPN (N = 600, <code>lambda.min</code>), the strongest cross-lagged edge is \"Feeling left out\" (lone2) at T1 → \"Loss of interest\" (dep2) at T2, B = 0.14. Write a 2–3 sentence interpretation for the Results section of a paper: read the direction correctly, give the number, avoid causal language, and add one limitation.</p>",
     answer="<p>Example: \"Controlling for all 9 items at T1, participants who scored higher on 'Feeling left out' at T1 tended to score higher on 'Loss of interest' at T2 (B = 0.14); this was the strongest cross-lagged edge in the network. This result reflects a predictive relationship over time and cannot be interpreted as a causal effect; a standard CLPN also does not separate within-person from between-person effects, so whether this edge represents a change process within individuals needs further study (together with a bootstrap check of its stability).\"</p>",
     rubric=[(3, "Correct direction (lone2 at T1 → dep2 at T2, controlling for the other T1 nodes), gives B = 0.14, no causal language, and adds a reasonable limitation (causality / within- vs between-person / stability)"),
             (2, "Direction and number correct, but the limitation is missing or vague, or there is one mildly causal phrase"),
             (1, "Direction reversed, or clearly causal language"),
             (0, "No answer, or wrong")]),
]
