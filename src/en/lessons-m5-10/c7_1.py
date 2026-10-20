# -*- coding: utf-8 -*-
L["7.1"] = dict(
lead=r"""<p>The earlier modules have prepared everything a CLPN needs: multiple regression (M3), LASSO (Lessons 3.5 and 6.3), the autoregressive and cross-lagged logic of the CLPM (M5), and networks and weight matrices (M6). This lesson puts them together into the cross-lagged panel network (CLPN).</p>
<p>First, which CLPN does this module teach? The CLPN was proposed by Wysocki, van Bork, Cramer, and Rhemtulla (2022 preprint; published in 2025 in <i>advances.in/psychology</i> as “Cross-lagged panel networks,” with McCarthy as an added coauthor). The main track of this course (Lessons 7.1–7.4, plus M8 and M10) teaches the <b>“LASSO-only” simplified version</b> that is most common in applied research (e.g., Funkhouser et al., 2021): run one LASSO regression per T2 node, take the shrunken coefficients directly as the network's edges, and then compute expected influence. This is not the full procedure that Wysocki et al. (2025) recommend. The full procedure uses LASSO only as a first step to select edges; it then re-estimates the model without a penalty as an SEM in lavaan, tests equality across time, and summarizes nodes with in-/out-prediction (explained variance). <a href="L7-5.html#full-clpn">Lesson 7.5</a> introduces the full procedure with a runnable R example. You learn the simplified version first for two reasons: it is the version you will meet most often in the literature, and it is step 1 of the full procedure.</p>""",
intuition=r"""
<h3>Three models in one table</h3>
""" + TABLE(["", "CLPM (M5)", "Cross-sectional network, GGM (M6)", "CLPN (this module)"], [
["Level of the variables", "Construct total scores (2)", "Items / symptoms (p)", "Items / symptoms (p)"],
["Time", "Yes (T1 → T2)", "No (one time point)", "Yes (T1 → T2)"],
["What an edge means", "Regression coefficient", "Partial correlation", "Regression coefficient (controlling for all T1 nodes)"],
["Direction", "Directed", "Undirected", "Directed"],
["Estimation", "SEM (lavaan)", "EBICglasso", "Nodewise LASSO regression (glmnet); the full procedure adds SEM re-estimation (Lesson 7.5)"]]) + r"""
<p>In other words, CLPN = the time direction of the CLPM + the item level of a network. The question it asks is: <b>which specific problems at T1 best (and uniquely) predict which specific problems at T2?</b></p>
<h3>Each T2 node = one regression equation</h3>
<p>Estimating a CLPN means running a multiple regression p times. With the 9 items of the course data:</p>
<ol><li>Take “Depressed mood” at T2 (dep1_t2) as the outcome and regress it on all 9 items at T1 (including dep1 at T1 itself). This gives 9 coefficients.</li>
<li>Repeat for the other 8 items at T2: 9 regressions, 81 coefficients in all.</li>
<li>Put the 9 coefficients from regression j into <b>column j</b> of a matrix. Row k, column j of the matrix B is then the coefficient for “k at T1 → j at T2.” The result is a 9 × 9 directed weight matrix.</li></ol>
<p>Running a separate regression for each node is called """ + T("nodewise regression") + r""". The matrix below is the """ + T("population target") + r""" for the course data (<code>data/true_B_population.csv</code>: the coefficients you get by applying this lesson's method to the observed scores of a very large simulated sample of 200,000 people, i.e., the answer a standard CLPN would give with an infinitely large sample). Note that this is not yet the “within-person truth”; the warning box further down this page and Lesson 7.2 explain the difference. Hover over any cell to read what it means.</p>
""" + W("bmat") + r"""
<h3>Two kinds of edges</h3>
<ul><li><b>""" + T("Autoregressive edge", "AR edge") + r""":</b> the diagonal of the matrix, B[k, k], k at T1 → k at T2. As in the CLPM, it represents the stability of that item (after controlling for the other items). In the course data these are about 0.3–0.4.</li>
<li><b>""" + T("Cross-lagged edge", "CL edge") + r""":</b> the off-diagonal cells, B[k, j] (k ≠ j), k at T1 → j at T2. Those that connect different constructs (e.g., a loneliness item → a depression item) are called """ + T("cross-construct edges") + r"""; they answer the question “how do loneliness and depression predict each other?” at the item level.</li></ul>
<p>Below is the same matrix drawn as a network. Autoregressive loops are shown by default (click a node to see its outgoing and incoming edges); uncheck the box to keep only the cross-lagged edges, which is how most papers draw it.</p>
""" + W("clpn", mode="view1") + r"""
<h3>What does a CLPN edge mean?</h3>
<p>B["lone3", "dep1"] = 0.118 reads: <i>among people with the same scores on all 9 items at T1 (including Depressed mood at T1 itself), those who are 1 standard deviation higher on “Feeling isolated” at T1 have a predicted T2 “Depressed mood” about 0.12 standard deviations higher.</i> Three points:</p>
<ol><li><b>Unique</b> prediction: it controls for all other T1 nodes, including the outcome node's own past (this is the job of the autoregressive term in a CLPN, for the same reason as in the CLPM).</li>
<li><b>Directed</b>: T1 comes before T2, so the arrow points from T1 to T2. But this is a direction in time, not a causal direction.</li>
<li><b>Standardized</b>: all variables are standardized first, so you can compare the size of coefficients across edges.</li></ol>
""" + WARN("Between-person vs. within-person:", "Look closely at the matrix above: almost every pair of items within the same construct has a small positive edge of about 0.06 (e.g., lone1 → lone2 = 0.07). Yet the within-person truth used to generate the data (<code>true_B_within.csv</code>) contains none of these edges. They come from stable traits: people who are lonely in the long run score high on every loneliness item, so any loneliness item at T1 helps predict the other loneliness items at T2. Like the CLPM, the standard CLPN does not separate between-person from within-person effects (see Lesson 5.3); Lesson 7.5 discusses this in detail.") + r"""
<h3>Why LASSO?</h3>
<p>With 9 nodes there are 81 coefficients, but only 800 people. With ordinary least squares (OLS), every coefficient carries sampling noise and almost none is exactly 0 (in the 4-node OLS example in R/L7-1.R, every cell is nonzero). Once p grows, you get the same “screen full of small edges” problem as in Lesson 6.3. So the CLPN runs LASSO in each regression, chooses λ by cross-validation, and shrinks unimportant coefficients to 0. That is the topic of the next lesson. The main track of this course (the “LASSO-only” simplified version) uses these LASSO coefficients directly; the full procedure of Wysocki et al. (2025) uses LASSO only to select edges and then re-estimates them without a penalty in an SEM (Lesson 7.5).</p>
""",
math=r"""
<p>For each T2 node \(j = 1,\dots,p\):</p>
""" + MATH(r"X_{j,t+1}=\sum_{k=1}^{p}\beta_{kj}\,X_{k,t}+\varepsilon_{j}") + SYM([
(r"\(X_{j,t+1}\)", "Standardized score on item j at time t+1 (e.g., T2)"),
(r"\(X_{k,t}\)", "Standardized score on item k at time t (e.g., T1), k from 1 to p, <b>including k = j</b>"),
(r"\(\beta_{kj}\)", "Coefficient from k at T1 to j at T2; stored in row k, column j of B"),
(r"\(\beta_{jj}\)", "Diagonal: autoregressive edge"),
(r"\(\beta_{kj},\ k\neq j\)", "Off-diagonal: cross-lagged edge"),
(r"\(\varepsilon_j\)", "Residual of equation j"),
(r"\(p\)", "Number of nodes (p = 9 in the course data)"),
]) + r"""
<h4>Matrix form (for reference)</h4>
<p>Stack the T1 scores of N people into an \(N\times p\) matrix \(\mathbf{X}_t\) and the T2 scores into \(\mathbf{X}_{t+1}\). All the equations together are then</p>
""" + MATH(r"\mathbf{X}_{t+1}=\mathbf{X}_{t}\,B+\mathbf{E}") + r"""
<p>Column j of B is exactly the coefficient vector of equation j. That is why we use the convention “row = origin (T1), column = destination (T2)”: it matches matrix multiplication and also matches qgraph's convention for directed matrices.</p>
<h4>Counting</h4>
<ul><li>p nodes → p regression equations, each with p coefficients → \(p^2\) coefficients;</li>
<li>of these, p are autoregressive and \(p(p-1)\) are cross-lagged;</li>
<li>if the nodes fall into two constructs (\(p_1\) loneliness items, \(p_2\) depression items), there are at most \(2p_1p_2\) cross-construct edges: \(2\times4\times5=40\) in the course data.</li></ul>
""",
code=r"""<p>R/L7-1.R uses 4 nodes (lone1, lone3, dep1, dep2) and plain <code>lm()</code> to show the “one equation per T2 node” logic, without regularization for now.</p>""" + CODE(r"""
source("R/_setup.R"); library(qgraph)
dat  <- read_course_data()
four <- c("lone1", "lone3", "dep1", "dep2")
X <- scale(dat[, paste0(four, "_t1")])          # T1 predictors (standardized)
Y <- scale(dat[, paste0(four, "_t2")])          # T2 outcomes (same order)
B <- matrix(0, 4, 4, dimnames = list(four, four))   # row = from (T1), col = to (T2)
for (j in 1:4) {
  fit <- lm(Y[, j] ~ X)                         # equation j: node j at T2 ~ all T1 nodes
  B[, j] <- coef(fit)[-1]                       # drop the intercept, store in column j
}
round(B, 2)
CL <- B; diag(CL) <- 0                          # keep cross-lagged edges only
qgraph(CL, directed = TRUE, edge.labels = TRUE, layout = "circle",
       groups = list(Loneliness = 1:2, Depression = 3:4), theme = "colorblind")
""", "Core of R/L7-1.R") + OUT(RLOG("L7-1_log.txt", "lone1_T2 =", 4), "Actual output excerpt: R/output/L7-1_log.txt") + r"""
<p><b>Matching the output to the matrix:</b> the third line, “dep1_T2 = … +0.11*lone3_T1 …,” is B["lone3", "dep1"] = 0.11 in the matrix (Feeling isolated → Depressed mood). In the first line, the coefficient of dep2_T1, −0.01, is noise-sized. This is OLS's “screen full of small edges,” which the next lesson handles with LASSO.</p>
<h3>Worked example: checking the 12 cross-lagged edges of the 4-node matrix against the within-person truth</h3>
<p>The course data are simulated, so the within-person lagged coefficients used to generate them (<code>data/true_B_within.csv</code>) are known. Sort the 12 cross-lagged edges of the OLS matrix above into three groups according to the within-person truth:</p>
""" + TABLE(["Group", "Edge (T1 → T2)", "4-node OLS", "Within-person truth"], [
["① Edges that exist in the within-person truth", "lone1 → dep2", "0.13", "{{V:win_lone1>dep2}}"],
["", "lone3 → dep1", "0.11", "{{V:win_lone3>dep1}}"],
["", "dep2 → lone3", "0.11", "{{V:win_dep2>lone3}}"],
["② Within-construct edges (within-person truth = 0)", "lone1 → lone3 / lone3 → lone1", "0.09 / 0.06", "0 / 0"],
["", "dep1 → dep2 / dep2 → dep1", "0.13 / 0.11", "0 / 0"],
["③ Other cross-construct edges (within-person truth = 0)", "lone1 → dep1, lone3 → dep2, dep1 → lone1, dep1 → lone3, dep2 → lone1", "0.06, −0.04, 0.04, −0.02, −0.01", "All 0"]]) + r"""
<ol><li><b>Group ①</b>: all 3 real within-person edges are estimated as positive, 0.11–0.13. But the estimate for lone3 → dep1 (0.11) is clearly smaller than the within-person truth ({{V:win_lone3>dep1}}); Lesson 7.2 explains where this gap comes from.</li>
<li><b>Group ②</b>: all 4 within-construct edges are positive, and just as large as those in group ①: dep1 → dep2 (0.13) equals the real lone1 → dep2 (0.13). The generating model contains no such within-person effects. They come from stable traits: people high on the depression trait score high on every depression item at both T1 and T2, so dep1 at T1 helps predict dep2 at T2 (derivation in Part 3 of Essential Math in Lesson 7.5).</li>
<li><b>Group ③</b>: between −0.04 and 0.06, some positive and some negative. This is sampling noise, and OLS does not set it to 0.</li></ol>
<p>This example shows two things. First, you cannot tell group ① from group ② by the size of the coefficients: a 0.13 within-person edge and a 0.13 trait edge look exactly the same in the matrix. LASSO can deal with group ③ (noise) but not with group ② (Lesson 7.2). Second, the value of an edge depends on which nodes the regression controls for: the same lone3 → dep1 edge is 0.11 in the 4-node OLS and {{V:pop_lone3>dep1}} in the population target of the 9-node model. So you can compare edge weights across studies directly only when the studies use the same nodes.</p>""",
quiz=[
("How many regressions does an 8-node CLPN need, and what is the maximum number of cross-lagged edges?", ["8; 56", "8; 64", "64; 56", "1; 28"], 0,
 ["Correct: one regression per T2 node; 8 × 7 = 56.", "64 = 8 × 8 also counts the 8 autoregressive edges.", "The number of regressions equals the number of T2 nodes, 8; 64 is the number of coefficients.", "A regression has only one outcome, so one regression cannot predict 8 T2 nodes at once; 28 = 8 × 7 / 2 is the maximum number of edges in an undirected network."]),
("What does B[\"lone3\", \"dep1\"] represent?", ["T1 Depressed mood → T2 Feeling isolated", "T1 Feeling isolated → T2 Depressed mood", "The partial correlation between the two", "The autoregression of Feeling isolated"], 1,
 ["Reversed: row = origin (T1), column = destination (T2).", "Correct.", "CLPN edges are directed regression coefficients, not symmetric partial correlations.", "The autoregression is on the diagonal: B[\"lone3\", \"lone3\"]."]),
("What are the predictors in each regression equation of a CLPN?", ["All T1 nodes except the outcome node", "All T1 nodes (including the outcome node's own T1 score)", "All T2 nodes", "Only the T1 nodes of the other construct"], 1,
 ["The outcome's own past must be included; otherwise the cross-lagged edges absorb the outcome node's stability and are overestimated.", "Correct.", "The T2 nodes are the outcomes; putting nodes from the same time point among the predictors estimates contemporaneous relations, not cross-lagged ones.", "All T1 nodes go in, including items of the same construct and the outcome node's own T1 score."]),
("Why are CLPN edges directed while GGM edges are undirected?", ["It is a software setting", "CLPN edges are T1 → T2 regression coefficients with an order in time; GGM edges are symmetric partial correlations at the same time point", "Because the CLPN uses LASSO", "Because a GGM cannot draw arrows"], 1,
 ["It is not a software setting: the direction comes from the order in time; T1 can only predict T2.", "Correct.", "GGMs often use LASSO too (EBICglasso); direction has nothing to do with regularization.", "It could draw arrows, but partial correlations at the same time point are symmetric, so an arrow would have no basis."]),
("Can a single CLPN edge tell between-person effects apart from within-person effects?", ["Yes", "No: the standard CLPN is based on observed scores and mixes the two", "Only autoregressive edges can", "Yes, as long as N is large enough"], 1,
 ["This is a common misconception: the standard CLPN regresses observed scores, so stable traits and within-person states both end up in the coefficients.", "Correct: you must say this when you write up limitations.", "Autoregression mixes in stable traits too (a trait keeps the same item high at every wave), so it cannot stand alone for within-person inertia.", "Sample size only reduces sampling error; the population target itself contains the effect of traits (Lesson 7.2)."]),
],
ex=[
("Write four regression equations by hand", "Foundational", r"""<p>Using 4 nodes (insomnia S, fatigue F, loneliness L, depressed mood D), write the 4 regression equations of a CLPN. Mark which coefficients are autoregressive, which are cross-lagged, and which are cross-construct edges (take S and F as the “somatic” construct and L and D as the “emotional” construct), and draw the corresponding directed network.</p>""",
 r"""<p>\(S_2=\beta_{SS}S_1+\beta_{FS}F_1+\beta_{LS}L_1+\beta_{DS}D_1+\varepsilon\), and the other three in the same way (with F₂, L₂, D₂ as the outcome). Autoregressive: β<sub>SS</sub>, β<sub>FF</sub>, β<sub>LL</sub>, β<sub>DD</sub> (4); cross-lagged: the other 12; cross-construct: the 8 between S, F and L, D (β<sub>SL</sub>, β<sub>SD</sub>, β<sub>FL</sub>, β<sub>FD</sub>, β<sub>LS</sub>, β<sub>LF</sub>, β<sub>DS</sub>, β<sub>DF</sub>). Note the order of the subscripts: β<sub>kj</sub> = from k to j.</p>"""),
("Read the matrix", "Conceptual", r"""<p>In the matrix widget on this page, find (1) the largest cross-lagged edge; (2) the only clearly negative edge; (3) the sum of the lone1 row (excluding the diagonal). Explain each in one sentence.</p>""",
 r"""<p>(1) B["dep3", "dep4"] = 0.169: T1 Sleep problems → T2 Fatigue. (2) B["dep4", "lone2"] = −0.083: T1 Fatigue → T2 Feeling left out (negative). (3) Row sum of lone1 ≈ 0.07 + 0.072 + 0.062 + 0.005 + 0.102 + 0.015 + 0.013 + 0.002 ≈ 0.34: the total amount by which T1 “Lack of companionship” predicts the other T2 items. This is the out-EI of Lesson 7.4.</p>"""),
("Translating between CLPM and CLPN", "Writing", r"""<p>In Lesson 5.1, the CLPM cross-lagged path “loneliness → depression” was d ≈ 0.13. In a CLPN, which edges carry the corresponding information?</p>""",
 r"""<p>It is spread over the 4 × 5 = 20 cross-construct edges “loneliness item → depression item” (the submatrix of loneliness rows × depression columns, top right). The CLPN shows which loneliness items (e.g., lone3 Feeling isolated, lone1 Lack of companionship, lone4 No one understands me) predict which depression items, whereas the CLPM gives only one overall, average coefficient. The two are not related by simple addition (the regressions control for different variables), but they should broadly agree in direction.</p>"""),
],
summary=[
    "CLPN = for each T2 node, a regression on all T1 nodes; the coefficients form a p × p directed matrix B.",
    "B[k, j] = from k at T1 to j at T2; diagonal = autoregressive, off-diagonal = cross-lagged.",
    "An edge = unique prediction after controlling for all T1 nodes (including the outcome's own past).",
    "When p is large, OLS gives a screen full of small edges → use LASSO (Lesson 7.2).",
    "The standard CLPN does not separate between-person from within-person effects (Lesson 7.5).",
    "This course's main track = the “LASSO-only” simplified version common in applied work; the full procedure of Wysocki et al. (2025) (LASSO edge selection → SEM re-estimation → in-/out-prediction) is in Lesson 7.5."
],
refs=["Wysocki, A., McCarthy", "Wysocki, A., van Bork", "Hamaker, E. L., Kuiper"],
)

L["7.2"] = dict(
lead=r"""<p>This lesson walks through the CLPN estimation code line by line and runs it with <code>glmnet</code>. On simulated data whose true structure is known, it compares how different λ rules perform, and it separates two different “answer keys”: the population target of the standard CLPN and the within-person truth that generated the data.</p>""",
intuition=r"""
<h3>Estimation in five steps</h3>
""" + TABLE(["Step", "What to do", "Common mistake"], [
["① Align the data", "T1 matrix X and T2 matrix Y: <b>same people, same row order, same item order</b>", "T2 columns in a different order from T1 → the matrix's row and column names don't match"],
["② Standardize", "<code>scale()</code> turns each item into z-scores", "No standardization → coefficients stay in each item's own units, so you can't compare the size of edges"],
["③ Set a seed", "<code>set.seed(2026)</code>", "No seed → cross-validation assigns folds at random, so results differ slightly every run"],
["④ Loop over regressions", "For j = 1…p: <code>cv.glmnet(X, Y[, j])</code>, put the coefficients into column j of B", "Putting the coefficients into a row instead of a column → every direction is reversed"],
["⑤ Check", "Look at the row/column names, whether the diagonal is around 0.3, and whether the signs agree with OLS", "Plotting without checking"]]) + r"""
<p><b>Why not use <code>cor_auto</code> from Lessons 6.3–6.5 here?</b> A cross-sectional network (EBICglasso) needs only a correlation matrix as input, so you can swap in polychoric correlations: they estimate the correlations between the continuous latent variables behind the items, which suits 4-point items better. A CLPN, by contrast, runs one glmnet regression per T2 node and needs each person's actual score on each item (a person-level data matrix). Polychoric correlations give only a correlation matrix, not each person's latent scores, so they cannot be fed into glmnet. The usual practice for a CLPN is therefore to z-standardize the observed scores and run the regressions; the edges are then standardized regression coefficients based on Pearson correlations. The cost: for items with few categories or strong skew, these coefficients are somewhat smaller than the associations on the latent scale. Keep this difference in mind when you compare the cross-sectional networks of Lesson 6.4 with the CLPN of this lesson.</p>
<h3>What does LASSO do in each regression?</h3>
<p>For T2 “Depressed mood,” the autoregressive predictor (T1 Depressed mood) is usually the strongest of the 9 T1 predictors, followed by a few items with unique predictive value; the remaining coefficients are small. LASSO starts with a λ so large that every coefficient is 0; as λ decreases, the variables enter the model in order of importance. Below is a schematic """ + T("coefficient path") + r""" for one T2 node.</p>
""" + W("path") + r"""
<h3>Choosing λ: <code>lambda.min</code> vs. <code>lambda.1se</code></h3>
<p><code>cv.glmnet</code> uses 10-fold cross-validation: it splits the 800 people at random into 10 parts, fits on 9 parts and predicts the remaining part, and computes the prediction error. Doing this for 100 candidate values of λ gives a curve of prediction error against λ (review the cvplot in Lesson 3.5).</p>
<ul><li><b><code>lambda.min</code></b>: the λ with the smallest cross-validation error. It predicts best but tends to keep more small edges (more false positives). The reason is that cross-validation looks only at prediction error: a very small coefficient, whether or not it exists in the population, makes almost no difference to the prediction error if it stays in the model (in the example after Essential Math on this page, the errors at two neighboring values of λ differ by only 0.001), so cross-validation has no reason to remove it. Step 1 (edge selection) of the full procedure of Wysocki et al. (2025) also uses <code>lambda.min</code> from 10-fold CV. Because CV-based edge selection has a high false-positive rate that does not fall as the sample grows, they added unpenalized SEM re-estimation and pruning afterward (see <a href="L7-5.html#full-clpn">Lesson 7.5: the full procedure</a>). The “LASSO-only” simplified version stops at this step and draws these false positives into the network plot along with everything else.</li>
<li><b><code>lambda.1se</code></b>: the largest λ whose error is within the minimum error + 1 standard error. The idea is “almost as accurate, but simpler”: the network is sparser and more conservative.</li></ul>
""" + KEY("Decide in advance:", "Which rule you use is an important “researcher degree of freedom.” Write it into your analysis plan before you see the results (Lesson 10.1), and you can report the other rule as a sensitivity analysis.") + r"""
<h3>How it works on the course data: first, which answer key?</h3>
<p>The advantage of simulated data is that we know the answer. But the course data have two answer keys, and they are not the same matrix:</p>
<ul><li><b>""" + T("Within-person truth") + r"""</b> (<code>data/true_B_within.csv</code>): the within-person lagged coefficients that <code>data/simulate_data.R</code> used to generate the data. It describes how a person changes at T2 after deviating from their own average at T1. Its cross-lagged part has only {{V:rec72_n_win}} nonzero edges.</li>
<li><b>""" + T("Population target") + r"""</b> (<code>data/true_B_population.csv</code>): the coefficients obtained with this lesson's method (standardize the observed scores, run the regressions without a penalty) on a simulated sample of 200,000 people. With an infinitely large sample and no sampling error, the standard CLPN converges to this matrix. Observed scores include each person's stable trait level, so this matrix also includes the effect of traits.</li></ul>
<p>Here are the two matrices side by side (rows = T1 predictors, columns = T2 outcomes, autoregressive cells in gray):</p>
""" + TWO_TRUTHS() + r"""
""" + KEY("The CLPN's population target ≠ the within-person process", "<p>Even with an infinite sample and a LASSO without any bias, the standard CLPN estimates the population target in the first table, not the within-person truth in the second. The difference between them is not sampling error, and a larger sample will not make it smaller. The reason was covered in Lesson 5.3: observed score = stable trait + within-person state, and because the standard CLPN regresses observed scores, both parts enter the coefficients (Lesson 7.5 discusses this in depth).</p>") + r"""
<p>Comparing the two cell by cell shows three kinds of difference:</p>
<ol><li><b>Extra edges.</b> The population target has {{V:rec72_n_pop}} cross-lagged edges with |β| ≥ 0.05. {{V:rec72_n_both}} of them are also in the within-person truth; the other {{V:rec72_n_trait}} are 0 in the within-person truth, and all of them are within-construct edges (loneliness item → loneliness item, depression item → depression item), ranging from {{V:rec72_trait_lo}} to {{V:rec72_trait_hi}}. They come from stable traits: people who are lonely in the long run score high on every loneliness item, so any loneliness item at T1 carries information about how high the person's trait is, which helps predict the other loneliness items at T2.</li>
<li><b>Weakened edges.</b> The within-person truth for lone3 → dep1 is {{V:win_lone3>dep1}}, but the population target is only {{V:pop_lone3>dep1}}; the negative edge dep4 → lone2 goes from {{V:win_dep4>lone2}} to {{V:pop_dep4>lone2}}.</li>
<li><b>Strengthened edges.</b> Within-person edges inside one construct, such as lone2 → lone4 (within-person {{V:win_lone2>lone4}}, population {{V:pop_lone2>lone4}}), get the trait part added on top.</li></ol>
<p>Note also that no cell of the population target is exactly 0: among the edges below 0.05, the largest in absolute value is {{V:rec72_pop_maxsmall}}. So “an edge in the population target” needs a cutoff, and R/L7-2.R uses |β| ≥ 0.05. The cutoff is a convention: with 0.04 or 0.08, the counts of hits and false positives below would change. The within-person truth has no such problem: nonzero means an edge.</p>
<h4>The {{V:rec72_n_win}} cross-lagged edges of the within-person truth</h4>
""" + TABLE(["Edge (T1 → T2)", "Within-person truth", "Population target", "<code>lambda.min</code> estimate", "<code>lambda.1se</code> estimate"],
 [[f"{ZH[k]} → {ZH[j]} ({k} → {j})", "{{V:win_" + f"{k}>{j}" + "}}", "{{V:pop_" + f"{k}>{j}" + "}}", "{{V:est72_min_" + f"{k}>{j}" + "}}", "{{V:est72_1se_" + f"{k}>{j}" + "}}"]
  for k, j in [("lone1", "dep2"), ("lone2", "lone4"), ("lone3", "dep1"), ("lone4", "dep5"), ("dep1", "dep5"), ("dep2", "lone3"), ("dep3", "dep4"), ("dep4", "lone2")]]) + r"""
<p class="muted" style="font-size:.88rem">Estimates from R/output/L7-2_B_lambda_min.csv and L7-2_B_lambda_1se.csv (set.seed(2026)); both answer keys from the two CSV files in data/.</p>
<p>Take lone3 → dep1. The drop from {{V:win_lone3>dep1}} to {{V:est72_min_lone3>dep1}} has two parts with different causes. From the within-person truth {{V:win_lone3>dep1}} to the population target {{V:pop_lone3>dep1}}: the model targets a different quantity (trait confounding), and this gap does not go away however large the sample. From the population target {{V:pop_lone3>dep1}} to the <code>lambda.min</code> estimate {{V:est72_min_lone3>dep1}}: LASSO """ + T("shrinkage bias") + r""" plus the sampling error of this particular sample; this gap shrinks as the sample grows and the penalty becomes lighter.</p>
<h4>Recovery: one estimate, checked against two answer keys</h4>
<p>R/L7-2.R checks the estimates from three λ rules against both answer keys (cross-lagged edges only). Against the population target, the “edges to recover” are the {{V:rec72_n_pop}} edges with |β| ≥ 0.05; against the within-person truth, they are the {{V:rec72_n_win}} nonzero edges. The column “of which trait edges” counts edges that are estimated as nonzero but exist only in the population target (within-person truth = 0).</p>
""" + TABLE(["λ rule", "Estimated CL edges", "Population target: hits", "Misses", "False positives", "r with population target", "Within-person truth: hits", "Misses", "False positives", "Of which trait edges", "r with within-person truth"],
 [[name, "{{V:rec72_" + r + "_pop_n_est}}"] + ["{{V:rec72_" + r + "_pop_" + c + "}}" for c in ["hit", "miss", "fp", "r"]] + ["{{V:rec72_" + r + "_win_" + c + "}}" for c in ["hit", "miss", "fp", "trait_hit", "r"]]
  for r, name in [("min", "<code>lambda.min</code>"), ("1se", "<code>lambda.1se</code>"), ("ebic", "EBIC (γ = 0.5)")]]) + r"""
<p class="muted" style="font-size:.88rem">Source: “Edge recovery under two truths” at the end of R/output/L7-2_log.txt, and R/output/L7-2_recovery_two_truths.csv; “r” is the Pearson correlation between the estimates and the answer key over all 72 cross-lagged positions.</p>
<p>Start with the comparison against the population target. It shows a typical trade-off: <code>lambda.min</code> recovers {{V:rec72_min_pop_hit}} edges and brings {{V:rec72_min_pop_fp}} false positives along; <code>lambda.1se</code> has only {{V:rec72_1se_pop_fp}} false positives but misses {{V:rec72_1se_pop_miss}} edges. EBIC lies in between. The more conservative the rule, the fewer false positives and the more misses; no rule wins on both.</p>
<p>Now the comparison against the within-person truth. Of the {{V:rec72_n_win}} within-person edges, <code>lambda.min</code> recovers {{V:rec72_min_win_hit}}; but of the {{V:rec72_min_pop_n_est}} cross-lagged edges it estimates, {{V:rec72_min_win_fp}} are 0 in the within-person truth. {{V:rec72_min_win_trait_hit}} of these are trait edges, and the remaining {{V:rec72_min_pop_fp}} are the false positives from the comparison against the population target. These {{V:rec72_min_win_trait_hit}} edges count as “hits” in the population-target part of the table and as “false positives” in the within-person part. Whether the same edge is right or wrong depends on your research question:</p>
<ul><li>If the question is “in the population, controlling for all T1 items, which T1 item predicts which T2 item?” (prediction, description), these edges are right, because these predictive relations really exist in the population.</li>
<li>If the question is “when one of a person's items goes up, does that push another of their own items up at the next wave?” (a within-person process), these edges are wrong: they reflect stable differences between people.</li></ul>
<p>A more conservative rule does not solve the second problem: of the {{V:rec72_1se_pop_n_est}} edges kept by <code>lambda.1se</code>, {{V:rec72_1se_win_trait_hit}} are still trait edges, and it also misses {{V:rec72_1se_win_miss}} within-person edges. λ rules deal with sampling noise; trait edges are not noise, and the larger the sample, the more reliably they appear. The correlation of the estimates with the within-person truth ({{V:rec72_min_win_r}} for <code>lambda.min</code>) is also lower than with the population target ({{V:rec72_min_pop_r}}).</p>
""" + WARN("What do the {{V:rec72_min_pop_fp}} false positives against the population target mean?", "The simulation study by Wysocki et al. (2025) points to the same problem: with LASSO alone (called the ℓ1 GLM in the paper), sensitivity is nearly perfect but there are many false positives; under nonstationary conditions, specificity fell below the 0.80 benchmark in every scenario. So they do not treat the LASSO coefficients as the final answer but as a list of candidate edges, which they then re-estimate without a penalty in an SEM and prune at p &lt; .01. On the same course data, <code>R/L7-5b.R</code> applies this full procedure (a constrained model with equality across time) and cuts the false positives against the population target from {{V:sem75_lasso_fp}} to {{V:sem75_p01_fp}}, at the cost of fewer hits, from {{V:sem75_lasso_hit}} to {{V:sem75_p01_hit}} (details in <a href=\"L7-5.html#full-clpn\">Lesson 7.5</a>). The nonparametric bootstrap (M8) and the CS-coefficient later in the course are the simplified version's other answer to this problem: keep the edges, but report how uncertain each one is. Both approaches target sampling noise, and neither removes trait edges from the network: to estimate a within-person process you need a model that separates out the traits (Lesson 7.5).") + r"""
<h3>Should you add covariates?</h3>
<p>""" + T("Covariates") + r""" (e.g., gender, age) can be added to each regression as extra predictors. They should usually not be penalized (penalty.factor = 0), because you add them to control for them, not to select them. Lesson 7.5 discusses this in detail; the course function <code>clpn_estimate(…, covariates = …)</code> already supports it.</p>
<h3>Record your decisions: the analysis log</h3>
<p>For every estimation, write down in an """ + T("analysis log") + r""": the items used and their order, whether you standardized, how you handled missing data (the course data have none; for real data see Lesson 4.3), alpha (1 = LASSO), the number of folds, the λ rule, the random seed, covariates, and the versions of R and glmnet (<code>sessionInfo()</code>). The reporting standards in Lesson 9.3 ask for all of these.</p>
""",
math=r"""
<p>For each T2 node j, LASSO solves:</p>
""" + MATH(r"\hat{\boldsymbol\beta}_{j}=\arg\min_{\boldsymbol\beta}\ \frac{1}{2N}\sum_{i=1}^{N}\Big(y_{ij}-\sum_{k=1}^{p}\beta_{kj}x_{ik}\Big)^2+\lambda_j\sum_{k=1}^{p}|\beta_{kj}|") + SYM([
(r"\(i=1,\dots,N\)", "Case (participant) index"),
(r"\(y_{ij}\)", "Standardized score of person i on item j at T2"),
(r"\(x_{ik}\)", "Standardized score of person i on item k at T1"),
(r"\(\frac{1}{2N}\sum(\cdots)^2\)", "Mean squared error (how well the model fits). This is how glmnet writes it"),
(r"\(\lambda_j\)", "Penalty strength of regression j; each T2 node gets its own λ from cross-validation"),
(r"\(\sum_k|\beta_{kj}|\)", "L1 penalty: the sum of the absolute values of all coefficients"),
]) + r"""
<h4>Cross-validation error</h4>
""" + MATH(r"\mathrm{CV}(\lambda)=\frac{1}{K}\sum_{f=1}^{K}\mathrm{MSE}_f(\lambda),\qquad \lambda_{\min}=\arg\min_\lambda \mathrm{CV}(\lambda)") + r"""
<p>K = 10 folds; \(\mathrm{MSE}_f\) is the mean squared error on fold f after fitting on the other 9 folds. <code>lambda.1se</code> is the largest λ with \(\mathrm{CV}(\lambda)\le \mathrm{CV}(\lambda_{\min})+\mathrm{SE}(\lambda_{\min})\) (SE is the standard error of the 10 fold errors).</p>
<p>An easily overlooked consequence: λ is chosen separately for each column (each T2 node). If one column has many nonzero edges, that may only mean a smaller λ was chosen for that column, not that this T2 node is “predicted by more items.” When you compare nodes, look at the size of the coefficients (the in-EI of Lesson 7.4), not just the number of nonzero edges.</p>
<h4>Why standardize?</h4>
<p>The penalty \(\lambda\sum|\beta_k|\) treats all coefficients the same, so the coefficients have to be measured on the same scale. The items do not have the same standard deviation (in the course data the loneliness items are scored 1–4, the depression items 0–3 and right-skewed): for an equally strong association, a predictor with a smaller standard deviation has a numerically larger coefficient and so is penalized relatively less. glmnet's default <code>standardize = TRUE</code> already takes care of this: it standardizes each predictor internally before applying the penalty and converts the coefficients back to the original units at the end. We still <code>scale()</code> X and Y by hand beforehand so that the returned coefficients are already standardized coefficients, with all edges on the same scale and comparable in size. Note that what matters is the standard deviation: moving only the starting point of the scale from 0 to 1 (0–3 becomes 1–4) does not change the slope.</p>
""",
code=CODE(r"""
source("R/_setup.R")
library(glmnet)
dat <- read_course_data()
d1 <- dat[, vars_t(1)]                 # T1 items: lone1_t1 ... dep5_t1
d2 <- dat[, vars_t(2)]                 # T2 items (same order!)
X <- scale(as.matrix(d1))              # standardize
Y <- scale(as.matrix(d2))
p <- ncol(X); labs <- sub("_t1", "", colnames(X))
B <- matrix(0, p, p, dimnames = list(labs, labs))  # row = T1 predictor, col = T2 outcome
set.seed(2026)                         # CV assigns folds at random -> set a seed
for (j in seq_len(p)) {                # for each T2 node j
  cvfit <- cv.glmnet(X, Y[, j], alpha = 1, nfolds = 10)
  B[, j] <- as.numeric(coef(cvfit, s = "lambda.min"))[-1]  # drop the intercept, store in column j
}
AR <- diag(B)                          # autoregressive edges
CL <- B; diag(CL) <- 0                 # cross-lagged edges
round(B, 2)
# the same thing in one line with the course function (defined in _setup.R):
set.seed(2026); B_1se <- clpn_estimate(d1, d2, rule = "lambda.1se")
""", "Core of R/L7-2.R") + r"""
<p><b>Line by line:</b> <code>vars_t(1)</code> returns <code>"lone1_t1" ... "dep5_t1"</code>, which keeps the T1 and T2 columns in the same order; <code>alpha = 1</code> means LASSO (alpha = 0 is ridge regression); <code>coef(cvfit, s = "lambda.min")</code> returns 10 numbers (intercept + 9 coefficients), and <code>[-1]</code> drops the intercept; <code>B[, j] &lt;-</code> stores the coefficients in column j.</p>
""" + TIP("Self-check:", "① <code>all(sub('_t1','',colnames(d1)) == sub('_t2','',colnames(d2)))</code> should be TRUE; ② <code>diag(B)</code> should be all positive, about 0.3–0.45; ③ pick any column and compare it with <code>coef(lm(Y[, j] ~ X))</code>: the signs should mostly agree and the LASSO values should be a little smaller (shrinkage)."),
quiz=[
("Why call set.seed() before each run?", ["It makes the LASSO estimates more accurate", "cv.glmnet assigns folds at random; a seed makes the results reproducible", "It lets cross-validation pick the truly optimal λ and so recover the true network", "glmnet throws an error without a seed"], 1,
 ["A seed does not change how accurate the method is; it only fixes this particular random split.", "Correct.", "A seed only makes the result reproducible; another seed may pick a different λ, and neither one guarantees the “true network.”", "No error without a seed; the results just differ slightly from run to run, which is exactly why you should set one."]),
("Which direction does B[\"sleep\", \"fatigue\"] represent?", ["T1 fatigue → T2 sleep", "T1 sleep → T2 fatigue", "The correlation between sleep and fatigue", "The autoregression of sleep"], 1,
 ["Reversed: rows are the T1 origin, columns the T2 destination.", "Correct: row = origin (T1), column = destination (T2).", "CLPN edges are regression coefficients, not symmetric correlations: B[\"sleep\", \"fatigue\"] and B[\"fatigue\", \"sleep\"] can differ.", "The autoregression is on the diagonal: B[\"sleep\", \"sleep\"]."]),
("After switching to <code>lambda.1se</code>, the network is usually:", ["Denser, because λ is smaller", "Sparser, because λ is larger (stronger penalty)", "Exactly the same", "Same number of edges, but each edge closer to the population target"], 1,
 ["Reversed: <code>lambda.1se</code> ≥ <code>lambda.min</code>; it picks the largest λ among those with similar error.", "Correct. In the course data the CL edges drop from {{V:rec72_min_pop_n_est}} to {{V:rec72_1se_pop_n_est}}.", "The two rules pick different λ values, so the network usually changes; in the course data the edge counts differ a lot.", "A larger λ means more shrinkage: fewer edges, and the edges that remain are usually further from the population target."]),
("What happens if you put the coefficients into rows instead of columns (B[j, ] <- …)?", ["Nothing", "The whole network is reversed: outgoing edges become incoming edges", "Only the autoregressive edges are affected", "R throws an error"], 1,
 ["It matters a lot: every cross-lagged edge points the wrong way.", "Correct; the autoregressive edges (the diagonal) are unaffected, which makes this error easy to miss.", "The opposite: only the diagonal (autoregression) is unaffected; every cross-lagged edge is reversed.", "No error: the dimensions are the same, so R assigns the values anyway. That is what makes it dangerous."]),
("Why standardize the T1 and T2 items first?", ["To make the data normally distributed", "So that the returned coefficients are standardized coefficients you can compare with each other", "To remove missing values", "Without it, glmnet cannot apply the penalty fairly"], 1,
 ["Standardizing changes only the mean and standard deviation, not the shape of the distribution; skewed items stay skewed.", "Correct: after standardizing X and Y by hand, every edge is a standardized coefficient, so you can compare their sizes.", "scale() neither deletes nor imputes missing values; missing data must be handled separately before estimation (Lesson 4.3).", "glmnet's default standardize = TRUE already applies the penalty on a standardized scale internally; standardizing by hand is about making the returned coefficients comparable."]),
("In the course data, lone1 → lone2 is about 0.07 in the population target and 0 in the within-person truth. <code>lambda.min</code> estimates it as nonzero. Which statement is correct?", ["It is a false positive caused by sampling and will disappear in a larger sample", "It is right for “predictive relations in the population” and wrong for “within-person processes”; it will not disappear however large the sample", "Switching to <code>lambda.1se</code> reliably removes all such edges", "It shows that data/true_B_within.csv is wrong"], 1,
 ["No: it exists in the population target, and the larger the sample, the more reliably it appears.", "Correct: this edge is produced by stable traits, and the population target of the standard CLPN includes it.", "No: <code>lambda.1se</code> is only more conservative; on the course data it still keeps several trait edges.", "No: the two matrices answer different questions."]),
],
ex=[
("Recovering the network: checking against two answer keys", "Hands-On", r"""<p>Run R/L7-2.R and open R/output/L7-2_est_vs_true.png (the x-axis of the left panel is the population target, of the right panel the within-person truth). Answer: (1) Which of the stronger edges were recovered? Give each one's estimate, population target, and within-person truth. (2) How large are most of the false positives against the population target? (3) In the right panel, how many blue points lie on x = 0 (within-person truth = 0) but have nonzero estimates? What type of edge are most of them? (4) What changes with <code>lambda.1se</code>? Which changes hold for both answer keys?</p>""",
 r"""<p>(1) dep3 → dep4 (estimate {{V:est72_min_dep3>dep4}}, population target {{V:pop_dep3>dep4}}, within-person truth {{V:win_dep3>dep4}}), lone2 → lone4 ({{V:est72_min_lone2>lone4}} / {{V:pop_lone2>lone4}} / {{V:win_lone2>lone4}}), dep4 → lone2 ({{V:est72_min_dep4>lone2}} / {{V:pop_dep4>lone2}} / {{V:win_dep4>lone2}}), dep1 → dep5 ({{V:est72_min_dep1>dep5}} / {{V:pop_dep1>dep5}} / {{V:win_dep1>dep5}}) and others were recovered; lone3 → dep1 was recovered but is fairly far from both answer keys ({{V:est72_min_lone3>dep1}} / {{V:pop_lone3>dep1}} / {{V:win_lone3>dep1}}). Notice that the estimates are generally closer to the population target, because the population target is what the standard CLPN estimates. (2) Most of the {{V:rec72_min_pop_fp}} false positives against the population target are small edges with |β| &lt; 0.05 (the blue points near x = 0 in the left panel). (3) {{V:rec72_min_win_fp}}, of which {{V:rec72_min_win_trait_hit}} are within-construct trait edges: in the population target they are about {{V:rec72_trait_lo}}–{{V:rec72_trait_hi}}, so they count as “hits” in the left panel and as “false positives” in the right panel. (4) With <code>lambda.1se</code> the CL edges drop from {{V:rec72_min_pop_n_est}} to {{V:rec72_1se_pop_n_est}}. Against the population target, false positives fall from {{V:rec72_min_pop_fp}} to {{V:rec72_1se_pop_fp}} and hits from {{V:rec72_min_pop_hit}} to {{V:rec72_1se_pop_hit}}; against the within-person truth, false positives fall from {{V:rec72_min_win_fp}} to {{V:rec72_1se_win_fp}} and hits from {{V:rec72_min_win_hit}} to {{V:rec72_1se_win_hit}}. Under both answer keys, sparser means fewer false positives and more misses, but <code>lambda.1se</code> still keeps {{V:rec72_1se_win_trait_hit}} trait edges.</p>"""),
("Check the direction", "Foundational", r"""<p>Write two lines of R code to check that your B matrix points the right way: estimate the OLS regression for dep4 at T2. Which column (or row) of B do you compare it with?</p>""",
 r"""<p><code>ols &lt;- coef(lm(Y[, "dep4_t2"] ~ X))[-1]; cbind(ols, B[, "dep4"])</code>. Compare it with <b>column dep4</b> of B: the signs of the two columns should mostly agree, and the LASSO values should be smaller in absolute value or 0. If it looks more like row dep4, you have the direction reversed.</p>"""),
("Analysis log", "Writing", r"""<p>Write a 6–8 item decision log for the estimation you just ran.</p>""",
 r"""<p>Example: ① Data: data/clpn_sim_wide.csv, N = 800, no missing data; ② Nodes: lone1–lone4, dep1–dep5, T1 → T2; ③ Preprocessing: each item z-standardized (scale); ④ Estimation: glmnet 4.x, alpha = 1 (LASSO), nodewise regression; ⑤ λ: 10-fold cross-validation, <code>lambda.min</code>; ⑥ Random seed 2026; ⑦ Covariates: none (gender and age added, unpenalized, in a sensitivity analysis); ⑧ Sensitivity analyses: <code>lambda.1se</code> and EBIC (γ = 0.5); ⑨ Software: R and package versions from sessionInfo().</p>"""),
],
summary=[
    "Workflow: align → standardize → set.seed → cv.glmnet for each T2 node → coefficients into column j → check.",
    "<code>lambda.min</code> is denser (more hits, more false positives); <code>lambda.1se</code> is sparser (conservative, more misses).",
    "The course data have two answer keys: the population target (true_B_population.csv, what the standard CLPN converges to with an infinite sample, traits included) and the within-person truth (true_B_within.csv). The CLPN's population target ≠ the within-person process.",
    "Against the population target, {{V:rec72_n_trait}} of the {{V:rec72_n_pop}} “edges” are within-construct trait edges; against the within-person truth they are all false positives, and neither another λ rule nor a larger sample removes them.",
    "lone3 → dep1: within-person truth {{V:win_lone3>dep1}} → population target {{V:pop_lone3>dep1}} (trait confounding) → <code>lambda.min</code> estimate {{V:est72_min_lone3>dep1}} (shrinkage bias + sampling error).",
    "Decide the λ rule, seed, number of folds, and covariates in advance, and record them.",
    "The course function clpn_estimate() wraps all the steps and supports <code>lambda.min</code>, <code>lambda.1se</code>, and ebic.",
    "The {{V:rec72_min_pop_fp}} false positives of <code>lambda.min</code> against the population target are a weakness of the “LASSO-only” simplified version; the full procedure of Wysocki et al. (2025) handles them with SEM re-estimation + pruning (Lesson 7.5)."
],
refs=["Wysocki, A., McCarthy", "Friedman, J., Hastie", "Tibshirani, R. (1996)"],
)
