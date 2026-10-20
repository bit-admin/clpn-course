# -*- coding: utf-8 -*-
ADD("5.2", "code", r"""
<h3>Worked example: from lavaan output to a path table</h3>
<p>The output of <code>summary(fit, standardized = TRUE)</code> is long. Don't read it from top to bottom. Pull out what you need for a paper in four steps:</p>
<ol><li><b>Check that estimation ended normally.</b> The top of the output should say "lavaan ... ended normally after N iterations". If it says "did not converge", or warns about negative variances, none of the numbers below can be used. First check the scales of your variables (if they differ a lot, divide the larger ones by 10), or whether the model is written incorrectly.</li>
<li><b>Then look at fit (Model Test User Model and fitMeasures).</b> Note χ², df and p, along with CFI, TLI, RMSEA (with its 90% CI) and SRMR, for the table note.</li>
<li><b>Next, find the Regressions section.</b> Each row is one path, for example <code>dep2 ~ lone1</code>. Look at <code>Estimate</code> (unstandardized), <code>Std.all</code> (standardized β) and <code>P(&gt;|z|)</code>. Put the 4 autoregressive and 4 cross-lagged paths into one table: paths as rows; b, SE, β and p as columns.</li>
<li><b>Finally, look at Covariances.</b> <code>lone2 ~~ dep2</code> is the <b>residual</b> covariance of the two T2 variables: how much they still vary together at the same time point after the T1 predictors are taken out. It is not simply "the correlation between T2 loneliness and T2 depression".</li></ol>
<p><code>parameterEstimates(fit, standardized = TRUE)</code> turns these results into a data frame, and <code>subset(pe, op == "~")</code> keeps only the regression paths. This is far less error-prone than copying numbers off the screen.</p>
""" + WARN("Common mistakes in the code", r"""<ul>
<li><b>A misspelled variable name in the model string.</b> lavaan reports "some observed variables are not found in the data", and the name it gives is the misspelled one. Check each name against <code>names(dat)</code>.</li>
<li><b>Leaving out the covariance between the T1 variables.</b> lavaan's <code>sem()</code> estimates the covariances among exogenous (T1) variables by default. But if you write out every parameter yourself with <code>lavaan()</code>, you must add <code>lone1 ~~ dep1</code>; otherwise the model assumes they are uncorrelated and fits very badly.</li>
<li><b>Comparing two cross-lagged paths by their p-values.</b> One path with p = .001 and another with p = .20 does not show that the two paths differ significantly. You need an equality constraint and a χ² difference test, as in this lesson.</li>
<li><b>Reporting CFI and leaving out RMSEA.</b> This lesson's data are a counterexample: CFI looks acceptable, but RMSEA = .141 is poor. Report all the indices and discuss why they disagree.</li></ul>"""))

# ------------------------------------------------------------------ 7.6 (optional advanced)
ADD("7.6", "code", WARN("Common mistakes in invariance testing", r"""<ul>
<li><b>Fixing both the first loading and the factor variance in the measurement model.</b> Use one way of setting the scale, not both. This lesson fixes the wave-1 factor variance to 1, so every loading gets <code>NA*</code> to free lavaan's default "first loading = 1".</li>
<li><b>Making loadings equal but forgetting to free the factor variances at waves 2 and 3</b> (or making intercepts equal without freeing the factor means). This forces variances or means that really differ to be equal; fit gets worse, and you wrongly conclude that invariance does not hold.</li>
<li><b>Leaving out the residual correlations of the same item across waves.</b> Each item carries its own quirks every time it is answered (its wording, how each person reads that sentence), and these quirks correlate across waves. Without them, the configural model fits poorly.</li>
<li><b>Subtracting two χ² values directly under MLR.</b> The robust chi-square needs a scaling correction: use <code>lavTestLRT()</code>. For ΔCFI use <code>cfi.robust</code>; don't mix the ordinary and robust CFI.</li></ul>"""))

# ------------------------------------------------------------------ 7.7 (optional advanced)
ADD("7.7", "math", r"""
<h3>Worked example: a permutation p-value by hand from 10 shuffles</h3>
<p>Suppose M = 0.20 under the real grouping. Ten shuffles give these values of M (sorted): 0.09, 0.11, 0.12, 0.13, 0.14, 0.15, 0.17, 0.18, 0.21, 0.24.</p>
<ol><li><b>Count how many are ≥ 0.20:</b> 0.21 and 0.24, so 2.</li>
<li><b>Apply the formula:</b> p = (2 + 1) / (10 + 1) = 3/11 ≈ 0.27.</li>
<li><b>Interpret:</b> in a world where the two groups are really the same, about one random grouping in four produces a difference this large. So this M is not unusual, and there is no evidence that the groups differ.</li>
<li><b>Precision:</b> with 10 permutations the smallest possible p is 1/11 ≈ 0.09, which can never reach .05. This is why a real analysis uses 1000 permutations or more.</li></ol>
""")
ADD("7.7", "code", WARN("Common mistakes when comparing networks between groups", r"""<ul>
<li><b>Putting two plots side by side and saying, by eye, "this edge exists only in women".</b> An edge kept by LASSO in one group and shrunk to 0 in the other does not, by itself, show a significant difference. You need a test.</li>
<li><b>Using different λ rules or different preprocessing in the two groups.</b> For example, <code>lambda.min</code> in one group and EBIC in the other, or standardizing one group and not the other. Any difference may then come from the methods alone. The real grouping and every shuffle must go through exactly the same pipeline.</li>
<li><b>Testing 72 edges and reporting only the significant ones.</b> Either specify the edges in advance, or report all of them with a correction, and state the number of permutations.</li>
<li><b>Reading the size of S as a population difference when the groups differ a lot in size.</b> The smaller group's network is sparser and less stable. Because group sizes stay fixed during permutation, the null distribution already includes the effect of unequal sizes, so the test itself is still valid. But the size and direction of the observed S partly reflect the difference in group size. Report each group's N, and keep this in mind when you interpret the size of S.</li></ul>"""))

# ------------------------------------------------------------------ 6.1
ADD("6.1", "math", r"""
<h3>Worked example: reading a whole network from a matrix</h3>
<p>Here is the weighted adjacency matrix of 4 nodes A, B, C, D (symmetric, zeros on the diagonal):</p>
""" + TABLE(["", "A", "B", "C", "D"], [
["A", "0", "0.3", "0.2", "0"], ["B", "0.3", "0", "−0.1", "0"], ["C", "0.2", "−0.1", "0", "0.4"], ["D", "0", "0", "0.4", "0"]]) + r"""
<ol><li><b>How many edges?</b> Count only the nonzero cells in the upper triangle: A–B, A–C, B–C and C–D, 4 in total. Four nodes can have at most 4 × 3 / 2 = 6 edges, so the <b>density</b> is 4/6 ≈ 0.67.</li>
<li><b>Which edge is strongest?</b> C–D (0.4). Which edge is negative? B–C (−0.1), drawn in red or as a dashed line.</li>
<li><b>How many edges does each node have (its degree)?</b> A 2, B 2, C 3, D 1.</li>
<li><b>Strength (sum of absolute weights):</b> A = 0.3 + 0.2 = 0.5; B = 0.3 + 0.1 = 0.4; C = 0.2 + 0.1 + 0.4 = 0.7; D = 0.4. C has the highest strength. Lesson 6.5 develops this idea.</li>
<li><b>Are A and D related?</b> There is no direct edge between them, but they are linked indirectly through C (A–C–D). In a partial correlation network, "no edge" means that, after controlling for the other nodes, the two have no direct association (Lesson 6.2).</li></ol>
<p>For a sense of scale: an undirected network of 9 nodes has at most 9 × 8 / 2 = 36 edges. A CLPN is a directed network: each of the 9 T1 nodes points to each of the 9 T2 nodes, giving 81 coefficients, of which 9 are autoregressive (self → self) and 72 are cross-lagged. This 9 × 9 matrix is what you will see throughout the Module 7 lessons.</p>
""")
ADD("6.1", "code", WARN("Common mistakes when reading a matrix", r"""<ul>
<li><b>Counting each edge of a symmetric matrix twice.</b> In an undirected network every edge appears twice in the matrix ([A, B] and [B, A]). Count edges in the upper triangle only: <code>sum(W[upper.tri(W)] != 0)</code>.</li>
<li><b>Reading the rows and columns of a directed matrix the wrong way round.</b> In this course <code>B[k, j]</code> means "row k → column j": k at T1 predicts j at T2. Other software and papers may use the opposite convention, so check before you read someone else's results.</li>
<li><b>Forgetting the diagonal.</b> A correlation matrix has 1s on the diagonal. qgraph does not draw the diagonal by default (without <code>diag = TRUE</code> there are no self-loops), but other functions may not skip it: if you compute strength by hand with <code>colSums(abs(W))</code>, for example, the diagonal 1s are included. Get into the habit of writing <code>diag(W) &lt;- 0</code> first.</li>
<li><b>Taking "no edge" to mean "completely unrelated".</b> Two nodes without a direct edge can still be strongly correlated through other nodes (A and D in the example above).</li>
<li><b>Reading the colors without checking the legend.</b> qgraph's default (classic) theme uses green for positive and red for negative; every network plot in this course uses the colorblind theme, with blue for positive and red for negative. Other people's plots may use either, so read the caption first.</li></ul>"""))

# ------------------------------------------------------------------ 6.2
ADD("6.2", "math", r"""
<h3>Worked example: conditional independence by hand</h3>
<p>Three variables: insomnia (1), fatigue (2) and poor concentration (3). Suppose the correlations are r₁₂ = 0.6, r₁₃ = 0.6 and r₂₃ = 0.36. The correlation of 0.36 between fatigue and poor concentration is not small. But is it a direct association, or does it arise because both are affected by insomnia?</p>
<p>The partial correlation between fatigue and poor concentration, controlling for insomnia, is:</p>
""" + MATH(r"r_{23\cdot1}=\frac{r_{23}-r_{12}r_{13}}{\sqrt{(1-r_{12}^2)(1-r_{13}^2)}}=\frac{0.36-0.6\times0.6}{\sqrt{0.64\times0.64}}=\frac{0}{0.64}=0") + r"""
<p>The numerator is exactly 0: the 0.36 is fully explained by the two paths "insomnia → fatigue" and "insomnia → poor concentration" (0.6 × 0.6 = 0.36). In the partial correlation network there is <b>no edge</b> between fatigue and poor concentration. That is what "conditional independence" means.</p>
<p>Now the partial correlation between insomnia and fatigue, controlling for poor concentration: numerator = 0.6 − 0.6 × 0.36 = 0.384, denominator = √(0.64 × (1 − 0.1296)) ≈ 0.746, partial correlation ≈ 0.51. It is smaller than the original 0.6 but still clear, so the insomnia–fatigue edge stays. The final network is a chain, fatigue—insomnia—poor concentration, with insomnia in the middle.</p>
<p>Check it in R: <code>R &lt;- matrix(c(1, .6, .6, .6, 1, .36, .6, .36, 1), 3); P &lt;- -cov2cor(solve(R)); diag(P) &lt;- 1; round(P, 3)</code>. The minus sign turns the diagonal into −1, so <code>diag(P) &lt;- 1</code> sets it back to 1 (the same as <code>diag(pc) &lt;- 1</code> in this lesson's R code). The off-diagonal cells show 0.514 and 0.</p>
""")
ADD("6.2", "code", WARN("Common mistakes when computing partial correlations", r"""<ul>
<li><b>Forgetting the minus sign.</b> The partial correlation from the precision matrix is ρ = −k<sub>ij</sub>/√(k<sub>ii</sub>k<sub>jj</sub>). The off-diagonal elements of <code>cov2cor(solve(R))</code> have the wrong sign and must be multiplied by −1.</li>
<li><b>Too many variables for the sample size.</b> When p gets close to N, the correlation matrix is nearly singular: <code>solve()</code> reports "system is computationally singular" or gives very unstable results. This is one reason Lesson 6.3 uses regularization.</li>
<li><b>Putting the T1 total score into the network together with its items.</b> The total is the sum of the items, so it is perfectly linearly dependent on them and the matrix cannot be inverted. Put only variables at the same level into a network.</li></ul>"""))

# ------------------------------------------------------------------ 6.3
ADD("6.3", "math", r"""
<h3>Worked example: how LASSO shrinks small coefficients to 0</h3>
<p>Take the simplest case: the predictors are standardized and uncorrelated with each other. Then glmnet's LASSO solution has a simple formula called <b>soft-thresholding</b>:</p>
""" + MATH(r"\hat\beta_j^{\text{LASSO}}=\operatorname{sign}(\hat\beta_j^{\text{OLS}})\cdot\max\left(|\hat\beta_j^{\text{OLS}}|-\lambda,\;0\right)") + r"""
<p>Suppose ordinary regression gives four coefficients, 0.30, 0.12, −0.05 and 0.02, and λ = 0.08:</p>
""" + TABLE(["OLS coefficient", "|b| − λ", "LASSO coefficient", "What happened"], [
["0.30", "0.22", "0.22", "Kept, but shrunk toward 0 by 0.08"], ["0.12", "0.04", "0.04", "Kept, but very small after shrinking"],
["−0.05", "−0.03 → set to 0", "0", "Shrunk to 0 (removed from the network)"], ["0.02", "−0.06 → set to 0", "0", "Shrunk to 0"]]) + r"""
<p>This shows two features of LASSO: ① coefficients whose absolute value is below λ become exactly 0, which makes the network sparse; ② the coefficients that remain are all shrunk toward 0 by the same amount, so LASSO edge weights are <b>systematically too small</b>. Ridge regression is different: it shrinks every coefficient proportionally but never sets any to exactly 0, so it cannot be used to select edges.</p>
<p>In real data the predictors are correlated and the formula is no longer this simple, but the intuition is the same: the larger λ, the higher the threshold and the fewer edges remain. EBICglasso picks one λ from a sequence by EBIC (fit plus a penalty on the number of edges; the larger γ, the heavier the penalty).</p>
""")
ADD("6.3", "code", WARN("Common mistakes when using regularization", r"""<ul>
<li><b>Comparing regularized edge weights directly with ordinary regression coefficients.</b> Regularized estimates are systematically too small; don't compare them directly with unregularized coefficients from other studies.</li>
<li><b>Tuning to get the result you want.</b> Trying γ = 0, 0.25 and 0.5 and keeping the one with "the most edges" or "the nicest conclusion" misuses researcher degrees of freedom. State γ (usually 0.5) in your analysis plan in advance, and report other values only as sensitivity analyses.</li>
<li><b>Expecting the network to be "very sparse" even with a large sample.</b> The larger N, the weaker the edges that pass the threshold. The course data's cross-sectional network (N = 800) has 28 edges at γ = 0, 0.25 and 0.5 alike: in large samples γ may matter very little.</li></ul>"""))

# ------------------------------------------------------------------ 6.4
ADD("6.4", "code", r"""
<h3>Worked example: five steps for reading a network plot</h3>
<p>When you look at a qgraph network plot (your own or one in a paper), read it in this order and you will avoid most misreadings:</p>
<ol><li><b>Read the caption first:</b> what the nodes are (items or scales), what the edges are (partial correlations, regression coefficients or correlations), how they were estimated (EBICglasso, which γ), and the sample size.</li>
<li><b>Then check the color convention and maximum:</b> is blue positive and red negative? What weight does the thickest edge stand for? If the caption gives no maximum, edge widths cannot be compared between plots.</li>
<li><b>Find the strongest edges:</b> don't judge by eye. Go back to the edge-weight table (<code>getWmat(net)</code>), sort by absolute value, list the top 5, then find them on the plot.</li>
<li><b>Look at the links between communities:</b> nodes of the same color (same scale) are usually tightly connected among themselves. The informative edges are those between colors, for example which "bridges" link depression items and anxiety items.</li>
<li><b>Look at positions last:</b> in a spring layout, node positions only roughly reflect connection strength. You cannot say "this node is in the center, so it is the most important". Importance has to be quantified with centrality indices (Lesson 6.5) and checked for stability (Lesson 8.3).</li></ol>
<p>When you write it up, every sentence should map to a number in a table. For example: "Edges among depression items were generally stronger than edges between depression and anxiety items; the strongest cross-construct edge was D? – A? (partial correlation = 0.??)". Fill in the question marks from your own output.</p>
""" + WARN("Common mistakes in plotting code", r"""<ul>
<li><b>The order in groups does not match the column order.</b> The numbers in <code>groups = list(Depression = 1:9, Anxiety = 10:16)</code> are column positions. If the column order of your data changes, the colors will be wrong, and you get no error.</li>
<li><b>Using Pearson correlations on ordinal items.</b> For 4- or 5-point items with clear skew, bootnet's <code>corMethod = "cor_auto"</code> switches to polychoric correlations automatically. Polychoric correlations can be unstable when the sample is small or some categories are almost never chosen, so watch for warnings.</li>
<li><b>Drawing two networks separately when you compare them.</b> Unless <code>layout</code> and <code>maximum</code> are fixed, positions and widths in the two plots are not comparable. Use <code>averageLayout()</code> and the same <code>maximum</code>.</li>
<li><b>Exporting a low-resolution PNG, or labels turning into empty boxes.</b> Export with <code>png(..., res = 300)</code> or <code>pdf()</code>. If non-Latin characters (such as Chinese labels) show as boxes, use <code>cairo_pdf()</code> or switch to a font installed on your system.</li>
<li><b>Labels that are too long.</b> Put only short codes on the nodes (D1, A3) and the full item wording in a <code>nodeNames</code> legend or a table.</li></ul>"""))

# ------------------------------------------------------------------ 6.5
ADD("6.5", "math", r"""
<h3>Worked example: strength, expected influence and bridge strength in one go</h3>
<p>A small 4-node network: loneliness items L1 and L2, depression items D1 and D2. Edge weights: L1–L2 = 0.4, D1–D2 = 0.3, L1–D1 = 0.2, L2–D1 = 0.1, L2–D2 = −0.05.</p>
""" + TABLE(["Node", "Strength (sum of |w|)", "Expected influence EI (sum of w)", "Bridge strength (|w| across constructs only)", "Bridge EI (w across constructs only)"], [
["L1", "0.4 + 0.2 = 0.60", "0.60", "0.20", "0.20"],
["L2", "0.4 + 0.1 + 0.05 = 0.55", "0.4 + 0.1 − 0.05 = 0.45", "0.1 + 0.05 = 0.15", "0.1 − 0.05 = 0.05"],
["D1", "0.3 + 0.2 + 0.1 = 0.60", "0.60", "0.2 + 0.1 = 0.30", "0.30"],
["D2", "0.3 + 0.05 = 0.35", "0.3 − 0.05 = 0.25", "0.05", "−0.05"]]) + r"""
<p>Some observations: ① for nodes without negative edges (L1, D1), strength equals EI; ② L2 has one negative edge, so its EI is 0.1 below its strength (the negative edge's absolute value is added once in strength and subtracted once in EI); ③ by the bridge indices, D1 is the main link between the two constructs (bridge strength 0.30). If you ask "which depression symptom is most closely tied to loneliness?", the answer is D1, not L1, which ties for the highest overall strength.</p>
<p>This lesson's script has a more extreme example: a node with only two edges, +0.3 and −0.3, has strength 0.6 and EI 0. Strength says it is "well connected"; EI says its "net effect" is zero. The two answer different questions, so choose the index that fits your research question.</p>
""")
ADD("6.5", "code", WARN("Common mistakes when reporting centrality", r"""<ul>
<li><b>Reading the x-axis without checking centralityPlot's scale.</b> In qgraph 1.9 and later (the course uses 1.9.8), <code>centralityPlot()</code> defaults to <code>scale = "raw0"</code>, raw values with the axis starting at 0; older versions, and many tutorials and papers, show z-scores. This lesson's <code>R/L6-5.R</code> sets <code>scale = "z-scores"</code> explicitly, and R prints "z-scores are shown on x-axis". z-scores only show where nodes stand relative to each other: z = 1.5 does not mean "strength 1.5". Set <code>scale</code> explicitly when you plot and say so in the caption; use <code>centralityTable()</code> when you need the actual values.</li>
<li><b>Looking only at the top-ranked node.</b> The first and second nodes may differ in strength by only 0.01, well within sampling error. Draw conclusions only together with the bootstrap difference test (Lesson 8.2) and the CS-coefficient (Lesson 8.3).</li>
<li><b>Reporting only strength in a network with negative edges.</b> When there are many negative edges, report EI as well and explain how the two differ.</li>
<li><b>Getting the communities wrong when grouping by scale.</b> The order of the <code>communities</code> argument of <code>bridge()</code> must match the node order; otherwise every bridge index is wrong.</li>
<li><b>Calling the most central node of a cross-sectional network the "cause".</b> An undirected cross-sectional network has no direction and cannot show what influences what.</li></ul>"""))

# ------------------------------------------------------------------ 7.1
ADD("7.1", "math", r"""
<h3>Worked example: reading a 3-node CLPN coefficient matrix</h3>
<p>Suppose there are only 3 nodes: loneliness (L), depressed mood (D1) and fatigue (D2). Nodewise regression gives the matrix B (rows = T1 predictors, columns = T2 outcomes):</p>
""" + TABLE(["T1 ↓ / T2 →", "L", "D1", "D2"], [
["L", "<b>0.40</b>", "0.15", "0"], ["D1", "0", "<b>0.35</b>", "0.10"], ["D2", "−0.05", "0", "<b>0.30</b>"]]) + r"""
<ol><li><b>Each column is one regression equation.</b> Column 2 says: D1<sub>T2</sub> = 0.15·L<sub>T1</sub> + 0.35·D1<sub>T1</sub> + 0·D2<sub>T1</sub> + error.</li>
<li><b>The diagonal holds the autoregressive edges</b> (0.40, 0.35, 0.30 in bold): each node's "inertia", how far a high or low level at T1 carries over to T2.</li>
<li><b>The off-diagonal cells are cross-lagged edges:</b> L → D1 (0.15), D1 → D2 (0.10), D2 → L (−0.05). L → D1 and D2 → L cross constructs; D1 → D2 stays inside the depression construct.</li>
<li><b>Direction is not symmetric:</b> B[L, D1] = 0.15, but B[D1, L] = 0. Unlike an undirected network, A → B and B → A in a CLPN are two separately estimated edges.</li>
<li><b>How do you read 0.15?</b> All variables are standardized, so: among people with the same T1 depressed mood and fatigue, those 1 SD higher on T1 loneliness are on average 0.15 SD higher on T2 depressed mood. This is the "extra prediction" after controlling for all T1 nodes, including D1's own baseline.</li></ol>
<p>With 9 nodes the matrix has 9 × 9 = 81 cells, and the logic is the same. The file <code>L7-2_B_lambda_min.csv</code> written by <code>R/L7-2.R</code> is exactly this kind of table; open it in Excel and you can check it cell by cell.</p>
""")
ADD("7.1", "code", WARN("Common mistakes in understanding the CLPN", r"""<ul>
<li><b>Thinking a CLPN edge is "the correlation between T1 and T2".</b> It is a regression coefficient after controlling for all T1 nodes, usually much smaller than the simple correlation across time.</li>
<li><b>Forgetting what the autoregressive edge does.</b> Without controlling for D1's own baseline, the L → D1 coefficient also picks up the fact that loneliness and depression are already correlated at T1, and is badly overestimated (the Lesson 5.1 exercise shows this).</li>
<li><b>Adding other T2 nodes as predictors.</b> A standard CLPN predicts T2 from T1 only. Adding nodes from the same time point estimates a different (contemporaneous) relationship with an entirely different meaning.</li>
<li><b>Reading rows and columns the wrong way round.</b> Some papers write B as "row → column", others as "column → row". Check the convention every time you read a table; this course always uses "row → column".</li></ul>"""))

# ------------------------------------------------------------------ 7.2
ADD("7.2", "math", r"""
<h3>Worked example: choosing λ by hand from cross-validation results</h3>
<p>Suppose <code>cv.glmnet</code> gives the following cross-validation results for one T2 node (cvm is the mean prediction error, cvsd its standard error):</p>
""" + TABLE(["λ", "cvm (prediction error)", "cvsd", "Number of nonzero coefficients"], [
["0.20", "0.950", "0.020", "1"], ["0.10", "0.880", "0.020", "3"], ["0.05", "0.851", "0.020", "5"], ["0.02", "0.850", "0.020", "7"], ["0.01", "0.852", "0.020", "9"]]) + r"""
<ol><li><b><code>lambda.min</code></b>: the λ with the smallest cvm, 0.02 (0.850), which keeps 7 coefficients.</li>
<li><b><code>lambda.1se</code></b>: first compute the threshold = smallest cvm + its cvsd = 0.850 + 0.020 = 0.870. Among the λ values with cvm ≤ 0.870, choose the <b>largest</b>: 0.05 (0.851) qualifies, 0.10 (0.880) is above the threshold, so <code>lambda.1se</code> = 0.05, which keeps 5 coefficients.</li>
<li><b>How to think about it:</b> the prediction errors at λ = 0.05 and 0.02 differ by only 0.001, far less than the standard error of 0.02, so statistically you cannot tell them apart. The logic of <code>lambda.1se</code> is: if you can't tell them apart, pick the simpler one (fewer edges).</li></ol>
<p>This is done once for each of the 9 T2 nodes, so the <code>lambda.1se</code> network as a whole is sparser than the <code>lambda.min</code> network. Because the folds are split at random, results change slightly from run to run unless you set a seed. In Lesson 9.2 you will see that across 20 seeds, 11 edges in the course data come and go.</p>
""")
ADD("7.2", "code", WARN("Common mistakes when estimating a CLPN with glmnet", r"""<ul>
<li><b>Not standardizing.</b> glmnet standardizes internally by default, but it returns the coefficients in the original units. With loneliness items scored 1–4 and depression items 0–3, those coefficients are not comparable. The course function <code>clpn_estimate()</code> first standardizes both X and Y with <code>scale()</code>, so the edge weights can be compared directly.</li>
<li><b>Not setting a seed.</b> Cross-validation folds are split at random, so results change. Put <code>set.seed()</code> at the top of your script, and report the seed and number of folds in your paper.</li>
<li><b>Putting coefficients in the wrong place.</b> The coefficients of the j-th regression go into <b>column</b> j of B (all T1 nodes → T2 node j). Put them in a row and the direction of the whole network is reversed.</li>
<li><b>T1 and T2 rows are not the same people.</b> X and Y must be matched by id, keeping only people with data at both waves (Lessons 4.2 and 4.3).</li>
<li><b>Treating the intercept as an edge.</b> The first value returned by <code>coef(cvfit)</code> is the intercept; drop it (<code>[-1]</code>).</li>
<li><b>Adding covariates but penalizing them too.</b> Covariates should get <code>penalty.factor = 0</code>; otherwise LASSO may drop them, and you have not actually controlled for them (Lesson 7.5).</li></ul>"""))

# ------------------------------------------------------------------ 7.3
ADD("7.3", "code", r"""
<h3>Worked example: from one row of the edge table to a careful sentence</h3>
<p>Take one row from the course data: <code>from = lone3, to = dep1, weight = 0.073</code> (standardized regression coefficient, <code>lambda.min</code>, set.seed(2026); see <code>R/output/L7-2_edgelist.csv</code>, the same estimate as in Lesson 7.2). It is not among the "top 5" on this page, but in both reference matrices it is the strongest loneliness → depression edge (population target {{V:pop_lone3>dep1}}, within-person truth {{V:win_lone3>dep1}}), so it is good for practice. From number to words in four steps:</p>
<ol><li><b>Translate the variables:</b> lone3 = T1 "Feeling isolated", dep1 = T2 "Depressed mood".</li>
<li><b>State what was controlled:</b> "after controlling for all 9 T1 nodes (including T1 depressed mood)".</li>
<li><b>State size and units:</b> "among people with the same scores on the other T1 items, those 1 SD higher on T1 feeling isolated are on average about 0.07 SD higher on T2 depressed mood". The coefficient is small, so avoid words like "marked" or "strong". It has also been shrunk by LASSO, and the population target {{V:pop_lone3>dep1}} is larger (Lesson 7.2), so don't treat 0.07 as an exact effect size either.</li>
<li><b>Add the caveat:</b> "this is a temporal predictive relationship that may include stable individual differences and cannot be read directly as causal". If you have run the bootstrap, add the interval as well (Lesson 8.2).</li></ol>
<p>Put together: "Controlling for all T1 symptoms, T1 'Feeling isolated' positively predicted T2 'Depressed mood' (β = 0.07), a small effect; this suggests that the experience of being isolated, one part of loneliness, may come before a worsening of depressed mood. The relationship is a temporal prediction and may partly reflect stable individual differences." Compare "feeling isolated causes depression", which makes two mistakes at once: it turns a single item into a construct, and a prediction into a cause.</p>
""" + WARN("Common mistakes when plotting a CLPN", r"""<ul>
<li><b>Forgetting to transpose the matrix.</b> qgraph reads its input matrix as "row → column". This course's B is also "row → column" and can be used directly; if your matrix follows the opposite convention, use <code>t(B)</code> first.</li>
<li><b>Not using the same maximum for different intervals.</b> When you compare the T1 → T2 and T2 → T3 plots, fix both <code>maximum</code> and <code>layout</code>.</li></ul>"""))

# ------------------------------------------------------------------ 7.4
ADD("7.4", "math", r"""
<h3>Worked example: out-EI, in-EI and bridge indices by hand</h3>
<p>Three nodes: loneliness L (loneliness construct), depressed mood D1 and fatigue D2 (depression construct). The cross-lagged edges (autoregressive edges not counted) are: L → D1 = 0.20, L → D2 = 0.10, D1 → L = −0.05, D2 → D1 = 0.15, D1 → D2 = 0, D2 → L = 0.</p>
""" + TABLE(["Node", "Out-EI (sum of its outgoing edges)", "In-EI (sum of its incoming edges)", "Bridge out-EI (only edges to the other construct)", "Bridge in-EI (only edges from the other construct)"], [
["L", "0.20 + 0.10 = 0.30", "−0.05 + 0 = −0.05", "0.30", "−0.05"],
["D1", "−0.05 + 0 = −0.05", "0.20 + 0.15 = 0.35", "−0.05", "0.20"],
["D2", "0 + 0.15 = 0.15", "0.10 + 0 = 0.10", "0", "0.10"]]) + r"""
<ul><li><b>Check:</b> the out-EI values add up to 0.30 − 0.05 + 0.15 = 0.40, and the in-EI values to −0.05 + 0.35 + 0.10 = 0.40. The two totals must be equal, because every edge is the "out" of one node and the "in" of another. This is a good way to catch calculation errors.</li>
<li><b>D2 has out-EI 0.15 but bridge out-EI 0:</b> its only outgoing edge, D2 → D1, stays inside the depression construct. If the question is "which depression symptom predicts loneliness?", D2 is not the answer.</li>
<li><b>D1 has the highest in-EI (0.35):</b> it is the most "predictable" node. But only 0.20 of that comes from loneliness (bridge in-EI); the other 0.15 comes from within depression.</li></ul>
<p>Actual results on the course data (<code>R/L7-4.R</code>, <code>lambda.min</code>): the highest out-EI belongs to lone4 "No one understands me" (0.608), which also has the highest bridge out-EI (0.347). At the construct level, the loneliness → depression edges sum to 0.557 and the depression → loneliness edges to only 0.079. This asymmetry in direction matches the data-generating model, which has more loneliness → depression edges.</p>
""")
ADD("7.4", "code", WARN("Common mistakes in computing and interpreting EI", r"""<ul>
<li><b>Mixing up row sums and column sums.</b> With B stored as "row → column", out-EI = row sums (<code>rowSums(B)</code>) and in-EI = column sums (<code>colSums(B)</code>). Swap them and out and in are swapped too.</li>
<li><b>Ignoring how negative edges cancel.</b> EI is a signed sum: a node with one +0.2 edge and one −0.2 edge has EI 0. Look at the edge table as well to see what lies behind an EI value.</li>
</ul>"""))

# ------------------------------------------------------------------ 7.5
ADD("7.5", "code", r"""
<h3>Worked example: judging how well a result replicates</h3>
<p>The course script estimates two networks, T1 → T2 and T2 → T3. To judge replication, look at four things, from coarse to fine:</p>
<ol><li><b>Overall similarity:</b> the correlation between the two sets of cross-lagged edge weights is 0.64. The overall pattern is similar, but far from identical.</li>
<li><b>Overlap of edges:</b> 40 cross-lagged edges are nonzero in both networks, and 27 appear in only one. Most edges that appear only once are very weak (the median of the larger of the two values is about 0.02), but there are exceptions: lone4 → dep4, the third-strongest edge in T1 → T2 (0.108), is shrunk to 0 in T2 → T3.</li>
<li><b>Strongest edges:</b> the two strongest, dep3 → dep4 (0.135 and 0.139) and lone2 → lone4 (0.127 and 0.138), are almost the same size in both intervals. These are the most credible findings.</li>
<li><b>Autoregressive edges:</b> for example, dep1 goes from 0.315 to 0.398 and dep2 from 0.310 to 0.238. The nodes' autoregressive edges are similar in size, but not the same.</li></ol>
<p>Example write-up: "The cross-lagged edge weights of the T1 → T2 and T2 → T3 networks correlated .64; 40 cross-lagged edges were nonzero in both intervals; the two strongest edges (dep3 → dep4, lone2 → lone4) were of similar size in both, whereas lone4 → dep4 appeared only in T1 → T2. We therefore interpret only edges present in both intervals." Interpreting only edges that appear in both intervals is a practical, conservative strategy when you have no independent sample.</p>
""")


# ------------------------------------------------------------------ M6–M7 additions
ADD("6.1", "code", r"""
<h3>Mini-exercise: from a description to a matrix</h3>
<p>A study reports: "There is a positive edge of 0.25 between loneliness and depression, a negative edge of −0.30 between depression and social support, and no edge between loneliness and social support." Write the 3 × 3 adjacency matrix (order: loneliness, depression, social support). Answer: row 1: 0, 0.25, 0; row 2: 0.25, 0, −0.30; row 3: 0, −0.30, 0. Now think: does the missing edge between loneliness and social support mean their correlation is 0? (No. They can be correlated indirectly through depression, in the direction of 0.25 × (−0.30), that is, negatively.) Once you can move back and forth between words, matrix and plot, network plots in papers will no longer intimidate you.</p>
""")
ADD("6.2", "code", r"""
<p><b>A reminder:</b> the edges in a partial correlation network depend on which nodes you put in. Add a new variable (say, "chronic pain") and some existing edges may weaken or disappear, because part of their association is now explained by the new variable. So a network's structure is always "relative to this set of variables". The methods section of a paper should say why these nodes were chosen, and the discussion should say which important variables were left out.</p>
""")
ADD("6.5", "code", r"""
<h3>Mini-exercise: matching research questions to centrality indices</h3>
<p>Match each research question to an index: ① "Which symptom has the most connections to other symptoms overall?" ② "Activating which symptom is most likely to raise the overall level of the other symptoms?" ③ "Which depression symptom is most closely tied to anxiety symptoms?" Answers: ① strength; ② expected influence (EI), because it takes the sign into account; ③ bridge strength or bridge EI. If your research question is about comorbidity, bridge indices are often more to the point than overall centrality.</p>
""")
ADD("7.1", "code", r"""
<p><b>How this maps onto the CLPM:</b> if you first add the 9 items into two total scores, loneliness and depression, and run the same regressions, the resulting 2 × 2 matrix is the CLPM of Lesson 5.1: two autoregressive and two cross-lagged paths. The CLPN just splits the "totals" back into "items". This also means the CLPN escapes none of the CLPM's limitations (stable traits, choice of lag, unmeasured confounders).</p>
""")
ADD("7.2", "code", r"""
<h3>Check your analysis settings</h3>
<p>After running <code>R/L7-2.R</code>, answer three questions and write the answers in your analysis decision log: ① Did you use <code>lambda.min</code> or <code>lambda.1se</code>, and why? ② How many folds did cross-validation use, and what was the seed? ③ How many nonzero cross-lagged edges does each rule give, and are the top 5 edges the same? If the strongest edges appear under both rules, the conclusion is fairly robust; if one appears only under <code>lambda.min</code>, interpret it more cautiously.</p>
""")
ADD("7.3", "code", r"""
<p><b>Tables before plots.</b> Reviewers and readers check results in tables, not plots. The full 9 × 9 coefficient matrix can go in the supplementary material; in the main text, give a table of the "nonzero cross-lagged edges", sorted by absolute value, marking each edge as cross-construct or within-construct.</p>
""")
ADD("7.4", "code", r"""
<h3>Mini-exercise: how one edge changes out-EI and in-EI</h3>
<p>In the worked example above, suppose you add an edge D2 → L = 0.10. Which numbers change? Answer: D2's out-EI goes from 0.15 to 0.25, and its bridge out-EI from 0 to 0.10; L's in-EI goes from −0.05 to 0.05, and its bridge in-EI also becomes 0.05; the out-EI and in-EI totals both become 0.50. An edge always changes the indices of two nodes at once, one "out" and one "in".</p>
""")

# ------------------------------------------------------------------ 8.1
