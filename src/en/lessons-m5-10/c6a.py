# -*- coding: utf-8 -*-
# Module 6: Foundations of network psychometrics
L["6.1"] = dict(
lead=r"""<p>From this lesson on, you look at a scale in a different way: instead of adding the 9 items up into two totals, you treat each item as a node that "pulls on" the other items. This lesson introduces the basic vocabulary of networks and how a network is written as a matrix.</p>""",
intuition=r"""
<h3>Why look at psychological problems as networks?</h3>
<p>The traditional view (the common cause model) says that "depressed mood, loss of interest, sleep problems … are all expressions of one underlying 'depression'," just as fever and cough are expressions of the flu. The <b>network perspective</b> says instead that symptoms may act on each other directly: poor sleep makes you tired, tiredness takes away your interest, losing interest makes you feel worthless … and "depression" is such a self-reinforcing system (see Borsboom & Cramer, 2013). Network analysis gives us a language for describing systems like this.</p>
<h3>Five basic terms</h3>
""" + TABLE(["Term", "Meaning in a psychological network", "In a plot"], [
[T("node"), "A variable: an item, a symptom, or a construct", "Circle"],
[T("edge"), "A statistical association between two nodes (not necessarily causal)", "Line"],
[T("edge weight"), "The size and direction (positive / negative) of the association", "Line thickness and color"],
[T("directed / undirected"), "Undirected: only says \"related\"; directed: says \"from which to which\" (e.g., prediction over time)", "Arrowhead or not"],
[T("density"), "Edges present ÷ edges possible", "How \"full\" the plot looks"]]) + r"""
<h3>A network is a matrix</h3>
<p>A computer can't read a picture; it reads tables. A network with \(p\) nodes can be written completely as a \(p\times p\) """ + T("weights matrix") + r""": the number in row i, column j is the weight of the edge between node i and node j, and 0 means no edge. If the matrix only records whether there is an edge (1/0), it is called an """ + T("adjacency matrix") + r""".</p>
<ul><li>The matrix of an undirected network is symmetric: [i, j] = [j, i], because A—B and B—A are the same edge.</li>
<li>The matrix of a directed network is usually not symmetric. In qgraph, [i, j] means <b>from i (row) to j (column)</b>. The CLPN coefficient matrix B follows this convention: B["lone3", "dep1"] = Feeling isolated (T1) → Depressed mood (T2).</li>
<li>In a cross-sectional network the diagonal [i, i] is usually 0 (a node's association with itself means nothing); in a CLPN the diagonal holds the autoregressive paths (yourself at T1 → yourself at T2), an important part of the model.</li></ul>
<p>Try it: change the numbers in the matrix below and watch the plot on the right change; tick "directed network" and [A, B] and [B, A] can differ.</p>
""" + W("adj") + r"""
<h3>Positive and negative edges: color conventions</h3>
<p>A positive edge means "when one is high, the other tends to be high"; a negative edge means "when one is high, the other tends to be low" (e.g., social support and loneliness). qgraph's classic (default) theme draws positive edges green and negative edges red. All network plots in this course use <code>theme = "colorblind"</code> (the colorblind-friendly theme, which is also the default of bootnet's <code>plot()</code>): <b style="color:var(--pos)">blue = positive</b>, <b style="color:var(--neg)">red = negative</b>. The thicker and darker the line, the larger |weight|. When you read someone else's plot, first check the caption to see which colors they used.</p>
<h3>Communities</h3>
<p>A """ + T("community / cluster") + r""" is a group of nodes that are especially tightly connected to each other; for example, the "4 loneliness items" and the "5 depression items" may each form a community. In this course the communities are set in advance by scale (loneliness vs. depression) and are used for coloring and for the bridge centrality of Lesson 6.5. There are also algorithms that find communities in the data (such as EGA or the walktrap algorithm); they are beyond the scope of this course.</p>
""" + KEY("Rule for checking:", "A plot is just one way to draw a matrix. Every conclusion should be traceable to specific numbers in the matrix."),
math=r"""
<p>Let the network have \(p\) nodes and weights matrix \(W\):</p>
""" + MATH(r"W = \begin{pmatrix} 0 & w_{12} & \cdots & w_{1p}\\ w_{21} & 0 & \cdots & w_{2p}\\ \vdots & & \ddots & \vdots\\ w_{p1} & w_{p2} & \cdots & 0 \end{pmatrix},\qquad \text{undirected: } w_{ij}=w_{ji}") + SYM([
(r"\(p\)", "Number of nodes. In the course data p = 9 (4 loneliness items + 5 depression items)"),
(r"\(w_{ij}\)", "Row i, column j: the weight of the edge between nodes i and j (directed: from i to j)"),
(r"\(w_{ij}=w_{ji}\)", "Symmetry: the mark of an undirected network; the matrix is a \"mirror image\" across the diagonal"),
]) + r"""
<h4>How many edges can there be?</h4>
<p>Undirected network: at most one edge per pair of nodes, so \(\binom{p}{2} = \frac{p(p-1)}{2}\) edges; 36 when p = 9.<br>Directed network: each pair has two directions, so \(p(p-1)\) edges (not counting self-loops); 72 when p = 9. That is the maximum number of cross-lagged edges in a CLPN; add the 9 autoregressive paths and you get 81 coefficients.</p>
<h4>Density</h4>
""" + MATH(r"\text{density} = \frac{\text{number of nonzero edges}}{\text{number of possible edges}}") + r"""
<p>The 5-node example in R/L6-1.R: 6 nonzero edges ÷ \(\binom{5}{2}=10\) = 0.6.</p>
""" + TIP("Tip:", "In R, <code>W[upper.tri(W)]</code> takes all elements of the upper triangle (without the diagonal), which is exactly each edge of an undirected network once. <code>sum(W[upper.tri(W)] != 0)</code> is the number of edges."),
code=CODE(r"""
source("R/_setup.R")
library(qgraph)
labs5 <- c("Lonely", "Insomnia", "Fatigue", "Depressed", "Support")
W <- matrix(c( 0, .3,  0, .4, -.3,
              .3,  0, .5,  0,   0,
               0, .5,  0, .2,   0,
              .4,  0, .2,  0, -.2,
             -.3,  0,  0, -.2,  0), 5, 5, byrow = TRUE,
            dimnames = list(labs5, labs5))   # Row and column names
isSymmetric(W)                                # TRUE -> undirected
sum(W[upper.tri(W)] != 0) / choose(5, 2)      # Density = 0.6
qgraph(W, labels = labs5, edge.labels = TRUE, theme = "colorblind")

# Directed network: D[i, j] = from i to j
D <- matrix(0, 3, 3, dimnames = list(labs5[1:3], labs5[1:3]))
D["Lonely", "Insomnia"] <- .4;  D["Insomnia", "Fatigue"] <- .5
qgraph(D, directed = TRUE, edge.labels = TRUE, asize = 6, theme = "colorblind")
""", "Core of R/L6-1.R") + r"""
<p><b>Line by line:</b> <code>matrix(…, 5, 5, byrow = TRUE)</code> fills in 25 numbers row by row; <code>dimnames</code> names the rows and columns, so you can then pick values by name, e.g., <code>W["Lonely", "Insomnia"]</code>; the first argument of <code>qgraph()</code> is the weights matrix, and <code>edge.labels = TRUE</code> prints the values on the edges; <code>directed = TRUE</code> draws arrows, and <code>asize</code> sets the arrow size.</p>""",
quiz=[
("What is special about the weights matrix of an undirected network?", ["The diagonal is all 1s", "It is symmetric about the diagonal", "All elements are positive", "Each row sums to 0"], 1,
 ["A matrix with 1s on the diagonal is a correlation matrix; a network's weights matrix usually has 0 on the diagonal, because an edge from a node to itself means nothing.", "Correct: [i, j] = [j, i]; A—B and B—A are the same edge.", "Negative edges (e.g., social support—loneliness) exist too, so elements can be negative.", "A row sum is that node's expected influence (6.5); it doesn't have to be 0."]),
("In a directed weights matrix in qgraph, what does [i, j] mean?", ["From j to i", "From i to j", "The correlation of i and j", "The autoregressive path of i"], 1,
 ["The wrong way round: in qgraph the row is the starting point and the column the end point.", "Correct: row = starting point, column = end point.", "A correlation is symmetric and cannot express direction; in a directed matrix [i, j] and [j, i] can differ.", "The autoregressive path is on the diagonal [i, i], not at [i, j]."]),
("What is the maximum number of edges in a directed network with 9 nodes (no self-loops)?", ["36", "72", "81", "45"], 1,
 ["36 = 9 × 8 / 2 is the maximum for an undirected network; in a directed network each pair has two directions.", "Correct: 9 × 8 = 72.", "81 = 9 × 9 also counts the 9 diagonal elements (self-loops).", "45 = 9 × 10 / 2 is the number of undirected edges with self-loops counted; it gets both the direction and the self-loops wrong."]),
("In a qgraph plot with the colorblind theme, what does a thick red line mean?", ["A strong positive edge", "A strong negative edge", "A weak positive edge", "An autoregressive path"], 1,
 ["In the colorblind theme positive edges are blue (green in the classic theme); red means negative in both themes.", "Correct.", "The thicker the line, the larger |weight|, so a thick line is a strong edge.", "Color only shows the sign; autoregressive paths are usually not drawn in a cross-sectional network plot."]),
("An undirected network with 5 nodes has 4 nonzero edges. What is its density?", ["0.4", "0.8", "0.2", "0.5"], 0,
 ["Correct: 4 / C(5,2) = 4 / 10 = 0.4.", "0.8 = 4 / 5 divides by the number of nodes; divide by the number of possible edges, C(5,2) = 10.", "0.2 = 4 / 20 divides by the number of edges of a directed network, 5 × 4; an undirected network divides by 10.", "0.5 = 4 / 8 has the wrong denominator: an undirected network with 5 nodes has at most 10 edges."]),
],
ex=[
("Draw it and write the matrix", "Basic", r"""<p>Draw a 5-node network: Lonely—Depressed (+0.4), Lonely—Support (−0.3), Insomnia—Fatigue (+0.5), Fatigue—Depressed (+0.2). Write out the 5×5 weights matrix and compute the density.</p>""",
 r"""<p>In the order "Lonely, Insomnia, Fatigue, Depressed, Support": row 1 = (0, 0, 0, .4, −.3); row 2 = (0, 0, .5, 0, 0); row 3 = (0, .5, 0, .2, 0); row 4 = (.4, 0, .2, 0, 0); row 5 = (−.3, 0, 0, 0, 0). The matrix is symmetric. Density = 4/10 = 0.4.</p>"""),
("Plot your own matrix with qgraph", "Hands-on", r"""<p>Enter the matrix from Exercise 1 in R and plot it with <code>qgraph(W, theme = "colorblind", edge.labels = TRUE)</code>. Then remove <code>theme</code> and look at the default colors.</p>""",
 r"""<p>Reference code: <code>W &lt;- matrix(0, 5, 5, dimnames = list(labs5, labs5)); W["Lonely", "Depressed"] &lt;- W["Depressed", "Lonely"] &lt;- .4</code> … (assign each edge twice to keep the matrix symmetric). In the default (classic) theme positive edges are green and negative edges red. Use <code>isSymmetric(W)</code> to check that you haven't missed a mirror position.</p>"""),
("Reading a directed matrix", "Understanding", r"""<p>In the "population CLPN target matrix" of the course data, <code>B["dep4", "lone2"] = -0.083</code> and <code>B["lone2", "dep4"] = 0.017</code>. Say in words what the direction and meaning of each edge are.</p>""",
 r"""<p><code>B["dep4", "lone2"]</code>: from T1 Fatigue → T2 Feeling left out, a negative edge: people who are more fatigued at T1 feel slightly less left out at T2, controlling for the other T1 items. <code>B["lone2", "dep4"]</code>: from T1 Feeling left out → T2 Fatigue, almost 0. A directed matrix is not symmetric; the two directions carry completely different information.</p>"""),
],
summary=["Node = item/symptom; edge = statistical association; weight = size and direction.", "Network = p × p weights matrix; undirected is symmetric, directed [i, j] = from i to j.", "Undirected: at most p(p−1)/2 edges; directed: at most p(p−1); density = nonzero edges / possible edges.", "The course's network plots all use the colorblind theme: blue positive, red negative (the default classic theme is green positive, red negative).", "The diagonal of a CLPN holds the autoregressive paths; it is not 0."],
refs=["Borsboom, D., & Cramer", "Epskamp, S., Cramer, A. O. J., Waldorp"],
)

L["6.2"] = dict(
lead=r"""<p>The edges in the previous lesson were "numbers we made up." This lesson asks: with real data, what statistic should an edge be? The answer is the partial correlation. In a CLPN, "the unique prediction after controlling for all T1 nodes" rests on the same idea.</p>""",
intuition=r"""
<h3>Correlation is "contagious"</h3>
<p>Picture a chain: insomnia → fatigue → poor concentration. Insomnia affects only fatigue, and fatigue affects only concentration. Is insomnia correlated with poor concentration? Yes: people with insomnia are more tired, and tired people concentrate worse, so on average people with insomnia also concentrate worse. In the simulation in the course script R/L6-2.R, the correlation of insomnia with poor concentration is r = 0.39.</p>
<p>But this correlation travels "by way of" fatigue. If you compare only people with the same level of fatigue, is there still a relationship between insomnia and poor concentration? No. This "association left over after controlling for the other variables" is the """ + T("partial correlation") + r""". In the same simulated data, the partial correlation of insomnia with poor concentration is ≈ 0.00.</p>
<p>In the demonstration below you can change the strength of the three "true effects." First keep "direct effect c = 0" and compare the two plots; then increase c and watch the insomnia—poor concentration edge appear in the partial correlation network.</p>
""" + W("pcor") + r"""
<h3>Conditional independence and the GGM</h3>
<p>When the partial correlation of two variables is 0, we say they are """ + T("conditionally independent") + r""" given all the other variables. A """ + T("Gaussian graphical model", "GGM") + r""" is this: for a set of (approximately) normal variables, draw an edge between two nodes if and only if their partial correlation is not 0, and use the partial correlation as the edge weight. The GGM is a special case of a """ + T("Markov random field") + r""" (an undirected graphical model): "no edge" means "independent, given all other nodes."</p>
""" + KEY("No edge in a GGM means:", "after controlling for all other nodes in the network, there is no linear association left between the two nodes. It does not say that they are \"unrelated\" (their correlation may be large); it says that their relationship can be \"explained away\" by the other nodes.") + r"""
<h3>Why is a partial correlation network "cleaner" than a correlation network?</h3>
<p>In a correlation network almost every pair of items has an edge, because psychological variables are almost always positively correlated (when someone is doing badly, they tend to do badly on everything). The plot looks like a ball of yarn and shows no structure. Partial correlations remove """ + T("indirect associations") + r""" passed along through other nodes (e.g., A and C are correlated only because A → B → C), and they also remove associations created by a common cause (A ← B → C). What is left are the "direct" connections, and the structure becomes clearer. The first kind of association, passed along through the mediator B, really exists; it is just not direct, which is why it is called indirect. The second comes from a common cause and is usually called a spurious association. In a network both cases show up as no A—C edge once B is controlled, and the partial correlation alone can't tell you which one it is. The course script's figure L6-2_cor_vs_pcor.png compares the two networks (see the R code section).</p>
<h3>Two "traps" of partial correlation</h3>
<ol><li><b>What you control for depends on what you put in.</b> A partial correlation only controls for nodes that are in the network. If "chronic illness" was not measured, the loneliness–depression association it creates stays in the edge.</li>
<li><b>Colliders.</b> If A and B are unrelated but both affect C, then controlling for C creates a partial correlation (usually negative) between A and B. This is one reason negative edges sometimes appear "out of nowhere."</li></ol>
""" + NOTE("Connection to CLPN:", "A GGM edge is an undirected association \"at the same time point, after controlling for all other nodes\"; a CLPN edge is \"the prediction of a T2 node by a T1 node after controlling for all T1 nodes,\" a directed regression coefficient. Both rest on the idea of \"controlling for all the other nodes.\""),
math=r"""
<h4>Partial correlation with three variables</h4>
""" + MATH(r"r_{XZ\cdot Y}=\frac{r_{XZ}-r_{XY}\,r_{YZ}}{\sqrt{(1-r_{XY}^2)(1-r_{YZ}^2)}}") + SYM([
(r"\(r_{XZ}\)", "The ordinary (zero-order) correlation of X and Z"),
(r"\(r_{XZ\cdot Y}\)", "Read \"the partial correlation of X and Z controlling for Y\"; the variable after the dot is the one controlled for"),
(r"\(r_{XY}\,r_{YZ}\)", "The part of the correlation passed along through Y; subtract it and you have the \"direct\" part"),
]) + r"""
<p>With the R/L6-2 output, \(r_{XZ}=0.39,\ r_{XY}=0.62,\ r_{YZ}=0.63\), the numerator is \(0.39 - 0.62\times0.63 = 0.39-0.39 \approx 0\). So the partial correlation ≈ 0.</p>
<h4>Many variables: the precision matrix (for reference)</h4>
<p>With many variables, the inverse of the covariance matrix \(\Sigma\), the """ + T("precision matrix") + r""" \(K=\Sigma^{-1}\), gives all partial correlations at once:</p>
""" + MATH(r"\rho_{ij\cdot\text{rest}} = -\frac{k_{ij}}{\sqrt{k_{ii}\,k_{jj}}}") + SYM([
(r"\(\Sigma\)", "The covariance (or correlation) matrix"),
(r"\(K=\Sigma^{-1}\)", "Precision matrix: the inverse of Σ; in R, solve(Σ)"),
(r"\(k_{ij}\)", "The element in row i, column j of the precision matrix"),
(r"\(\rho_{ij\cdot\text{rest}}\)", "The partial correlation of nodes i and j controlling for all other nodes; note the minus sign"),
]) + r"""
<p>So "no edge in the GGM" ⇔ \(k_{ij}=0\) ⇔ that entry of the precision matrix is 0. The graphical lasso in the next lesson penalizes K directly, turning many \(k_{ij}\) into 0.</p>
<h4>Partial correlation and multiple regression</h4>
<p>When you predict \(X_i\) from all the other variables, the regression coefficient \(\beta_{ij}\) of \(X_j\) has the same sign as the partial correlation, and \(\beta_{ij}=0 \iff \rho_{ij\cdot\text{rest}}=0\). In R/L6-2, the insomnia coefficient in <code>lm(poor_conc ~ insomnia + fatigue)</code> is −0.004 ≈ 0, matching the partial correlation. This is the idea behind nodewise regression: regress each node on the others, and you also recover the network structure. CLPN works this way, except that the predictors are all the nodes at the previous time point.</p>
""",
code=CODE(r"""
source("R/_setup.R"); library(qgraph)
set.seed(62); n <- 1000
insomnia <- rnorm(n)
fatigue <- 0.6 * insomnia + rnorm(n, 0, .8)
poor_conc <- 0.6 * fatigue + rnorm(n, 0, .8)       # Affected only by fatigue
d <- data.frame(insomnia, fatigue, poor_conc)
round(cor(d), 2)                                # Ordinary correlations
P  <- solve(cor(d))                             # Precision matrix = inverse of the correlation matrix
pc <- -cov2cor(P); diag(pc) <- 1                # Partial correlations
round(pc, 2)
coef(lm(poor_conc ~ insomnia + fatigue))        # Regression coefficients agree with the partial correlations (insomnia ≈ 0)
par(mfrow = c(1, 2))
qgraph(cor(d), graph = "cor",  labels = names(d), edge.labels = TRUE, theme = "colorblind", title = "Correlation Network")
qgraph(cor(d), graph = "pcor", labels = names(d), edge.labels = TRUE, theme = "colorblind", title = "Partial Correlation Network")
""", "Core of R/L6-2.R") + r"""
<p><b>Key functions:</b> <code>solve(A)</code> inverts a matrix; <code>cov2cor()</code> rescales a matrix into "correlation" form (dividing by the square roots of the diagonal), and adding a minus sign gives the partial correlations; <code>qgraph(…, graph = "pcor")</code> makes qgraph turn a correlation matrix into a partial correlation network for you.</p>""",
quiz=[
("What does the partial correlation r<sub>XZ·Y</sub> mean?", ["The ordinary (zero-order) correlation of X and Z", "The association between X and Z left after controlling for Y", "The causal effect of X on Z: Y has been controlled, so what is left is causal", "The part of the X–Z association passed along through Y"], 1,
 ["A zero-order correlation controls for nothing; a partial correlation is computed after controlling for Y.", "Correct.", "Controlling for one measured variable can't remove unmeasured confounding; a partial correlation is still an association, not causation.", "The part passed along through Y (r<sub>XY</sub>r<sub>YZ</sub>) is exactly what gets subtracted; the partial correlation is what remains."]),
("What does it mean when two nodes in a GGM have no edge?", ["Their correlation is 0", "Given all other nodes, they are conditionally independent (partial correlation 0)", "One node has no effect at all on the other, not even an indirect one", "The sample is too small"], 1,
 ["Their correlation can be large; it just can be explained by other nodes (this lesson's insomnia—poor concentration: r = 0.39, partial correlation ≈ 0).", "Correct.", "Indirect effects can still exist: in the chain A → B → C, A and C have no edge, but A affects C through B.", "In a regularized network a zero edge can have to do with sample size, but the definition of the GGM is about conditional independence and has nothing to do with sample size."]),
("How are partial correlations related to multiple regression coefficients?", ["Regression coefficients measure prediction and partial correlations association, so they can have opposite signs", "A regression coefficient is 0 if and only if the partial correlation is 0, and the two have the same sign", "The regression coefficient always equals the partial correlation", "The partial correlation is the square of the regression coefficient"], 1,
 ["They always have the same sign and are 0 together; that is exactly why nodewise regression can recover the network structure.", "Correct.", "Same sign and zero together, but the values usually differ: the regression coefficient also depends on the (residual) variances of the two variables.", "A partial correlation can be negative; a square can't."]),
("What does k<sub>ij</sub> = 0 in the precision matrix K tell you?", ["The correlation of i and j is 0", "The partial correlation of i and j is 0", "The variance of i is 0", "The matrix cannot be inverted"], 1,
 ["The elements of the precision matrix correspond to partial correlations; the ordinary correlation may not be 0.", "Correct: ρ = −k<sub>ij</sub>/√(k<sub>ii</sub>k<sub>jj</sub>).", "Variance information is on the diagonal; an off-diagonal k<sub>ij</sub> of 0 has nothing to do with the variance of i.", "K is itself the inverse of Σ; one off-diagonal zero doesn't affect whether it can be inverted."]),
("A and B both affect C but are unrelated to each other. After controlling for C, the partial correlation of A and B may be:", ["Still 0, because A and B were unrelated to begin with", "Nonzero (often negative)", "Nonzero, showing a direct effect between A and B", "Always positive"], 1,
 ["That is exactly the collider trap: A and B were unrelated, and controlling for C creates an association.", "Correct: controlling for a collider creates a spurious association.", "This partial correlation is created by controlling for C; it does not show a direct effect between A and B.", "When both causes affect C positively, the partial correlation after controlling for C is usually negative."]),
],
ex=[
("Partial correlation by hand", "Basic", r"""<p>Given r(loneliness, depression) = 0.50, r(loneliness, social support) = −0.40 and r(depression, social support) = −0.30, compute the partial correlation of loneliness and depression controlling for social support.</p>""",
 r"""<p>\(\frac{0.50-(-0.40)(-0.30)}{\sqrt{(1-0.16)(1-0.09)}}=\frac{0.50-0.12}{\sqrt{0.84\times0.91}}=\frac{0.38}{0.874}\approx0.43\). After controlling for social support, the loneliness–depression association drops a little but is still clear.</p>"""),
("cor() vs. pcor", "Hands-on", r"""<p>Run R/L6-2.R, then change <code>poor_conc &lt;- 0.6 * fatigue + rnorm(n, 0, .8)</code> to <code>poor_conc &lt;- 0.6 * fatigue + 0.3 * insomnia + rnorm(n, 0, .8)</code> and recompute the partial correlations. What is the partial correlation of insomnia with poor concentration now?</p>""",
 r"""<p>With the direct effect added, the insomnia—poor concentration partial correlation is clearly above 0 (solution script <code>R/solutions/L6-2_solution.R</code>, seed 62: 0.28; fatigue—poor concentration 0.53, insomnia—fatigue 0.36), and the edge appears in the partial correlation network. Partial correlations can tell "direct" from "indirect" associations, provided the variable in between was measured.</p>"""),
("Comparing the two networks on the course data", "Extension", r"""<p>Read the course data, take the 9 items at T1, draw the two plots with <code>qgraph(cor(x), graph = "cor")</code> and <code>graph = "pcor"</code>, and count the edges with |weight| &gt; 0.1 in each.</p>""",
 r"""<p>Reference code: <code>x &lt;- read_course_data()[, vars_t(1)]; R &lt;- cor(x); P &lt;- -cov2cor(solve(R)); diag(P) &lt;- 0; sum(abs(R[upper.tri(R)]) &gt; .1); sum(abs(P[upper.tri(P)]) &gt; .1)</code>. Results from the solution script: in the correlation network all 36 pairs are &gt; 0.1 (the items are generally positively correlated and share stable traits); the partial correlation network has only 16, and all 16 are within one scale (between loneliness items or between depression items). The associations across scales all drop below 0.1 once the other items are controlled.</p>"""),
],
summary=["Correlation is \"passed along\" chains; partial correlation = the association left after controlling for the other variables.", "GGM: edge = partial correlation; no edge = conditional independence.", "Partial correlations can be computed from the precision matrix K = Σ⁻¹: ρ = −k<sub>ij</sub>/√(k<sub>ii</sub>k<sub>jj</sub>).", "Regression coefficient 0 ⇔ partial correlation 0: the basis of nodewise regression and of CLPN.", "Traps: only measured variables are controlled; controlling for a collider creates spurious edges."],
refs=["Epskamp, S., & Fried, E. I. (2018)", "Borsboom, D., & Cramer"],
)

L["6.3"] = dict(
lead=r"""<p>The partial correlation network of the previous lesson has a practical problem: with a finite sample, almost no partial correlation is exactly 0, so every pair of nodes gets a small edge (in the course data the unregularized partial correlation network has 36 of 36 edges nonzero). This lesson shows how regularization removes the small edges that noise creates. It is the same idea as the LASSO regression in CLPN.</p>""",
intuition=r"""
<h3>Where do all the small edges come from?</h3>
<p>Even if two items really are conditionally independent in the population (partial correlation = 0), the sample estimate will be a small number like 0.03 or −0.05 because of """ + T("sampling variability") + r""". With 9 nodes there are 36 partial correlations to estimate, with 16 nodes 120; each carries a little noise, so the plot becomes a "ball of yarn," and many of the edges are """ + T("false positive edges") + r""".</p>
<h3>The intuition of LASSO: charge for "complexity"</h3>
<p>Review """ + LINK("3.5") + r""": LASSO adds a "fine" to the goal of "fitting the data": the sum of the absolute values of all coefficients times λ. To pay less, the model pushes coefficients that don't do much all the way to 0 and keeps only those "worth paying for." The larger λ, the heavier the fine and the fewer edges remain. Applied to a network, this gives a """ + T("sparse network") + r""".</p>
<p>In the demonstration below, the "true network" has 10 edges (tick "show true structure" to see them as green dashed lines). We draw a sample from the true network, estimate the partial correlations, and then use λ to remove the small edges. Try to answer: how many false positives are there at λ = 0? At what λ do the false positives drop to 0? How many true edges are missed at that point? Then set the sample size to 100 and try again.</p>
""" + W("lasso") + r"""
<h3>Graphical lasso and EBIC</h3>
<p>The """ + T("graphical lasso", "glasso") + r""" puts the LASSO penalty directly on the precision matrix K: while making K fit the sample covariance as well as possible, it penalizes the sum of the absolute values of all off-diagonal elements of K. As a result, many \(k_{ij}\) are exactly 0, which means no edge in the GGM.</p>
<p>How do you choose λ? glasso tries a sequence of λ values (usually 100, from "empty network" to "almost fully connected"), and each λ gives a candidate network. Each candidate is then scored with the """ + T("extended Bayesian information criterion", "EBIC") + r""", and the one with the lowest score is chosen. EBIC adds to the ordinary BIC an extra penalty for "networks with many edges," and how heavy it is depends on the """ + T("hyperparameter gamma", "γ") + r""": γ = 0 is the ordinary BIC, and the larger γ, the more EBIC prefers sparse networks. bootnet's default is γ = 0.5 (the conservative choice recommended by Epskamp & Fried, 2018); 0.25 is also common.</p>
""" + KEY("Key point:", "EBICglasso = graphical lasso (produces a sequence of candidate networks) + EBIC (picks one of them). Larger γ → sparser → fewer false positives, but more likely to miss real weak edges.") + r"""
<h3>Actual results from the course script</h3>
<p>R/L6-3.R makes two comparisons:</p>
<ol><li><b>Course data (N = 800, 9 items):</b> γ = 0, 0.25 and 0.5 all select a network with 28 edges, the very same network. In other words, EBIC picks the same λ under all three γ. With a large sample and strong associations among items, the extra penalty from γ is small compared with the differences in log-likelihood, not enough to change the choice. This is not caused by the end of the λ sequence: R/L6-3.R prints the λ chosen for each γ at the end of the log, and all three choose the 81st of the 100 candidate λ values counted from the largest (λ = 0.01375), not the smallest end of the sequence. If the smallest value of the sequence were chosen, that would mean EBIC wants a denser network than the sequence can offer, and you should extend the sequence downward and look again. bootnet may also say "A dense regularized network was selected": this reminds you that the chosen network is fairly dense; it is not an error.</li>
<li><b>Small-sample simulation with a known true network (12 true edges, n = 150):</b></li></ol>
""" + TABLE(["γ", "Estimated edges", "Of which false positives"], [["0", "22", "10"], ["0.25", "15", "3"], ["0.5", "13", "1"]]) + r"""
<p>Note that "estimated edges − false positives" is 12 in all three rows: in this simulation, all three γ values found all 12 true edges, and they differ only in the extra false positives (10, 3, 1). At γ = 0.5, 12 of the 13 estimated edges are true: no true edge is missed and there is only 1 extra. That is because the true edges in this simulation are not very weak; with weaker true edges and smaller samples, a larger γ is more likely to remove weak true edges too. γ matters a lot in small samples; in large samples its effect is often small.</p>
<h3>Three limitations of regularization</h3>
<ol><li><b>Edge = 0 ≠ no relationship.</b> When regularization pushes an edge to 0, that only says "at this sample size and penalty, the evidence is not enough to keep it." Weak true edges are often removed.</li>
<li><b>The edges that remain are "shrunk."</b> LASSO estimates are systematically biased toward 0, so you can't treat regularized edge weights as unbiased estimates.</li>
<li><b>With large samples and dense true networks, EBICglasso may not work well.</b> Later work by Epskamp and colleagues proposed """ + T("unregularized estimation, e.g. ggmModSelect") + r""", which can be used as an alternative or a sensitivity analysis with large samples. In bootnet it only takes <code>default = "ggmModSelect"</code>.</li></ol>
<h3>The difference in CLPN: EBIC vs. cross-validation</h3>
<p>CLPN runs a LASSO regression (glmnet) for each T2 node and chooses λ by """ + T("cross-validation", "CV") + r""" (<code>cv.glmnet</code>): the sample is split into 10 parts; in turn, 9 are used for estimation and 1 to test the prediction error, and the λ with the smallest prediction error is chosen (<code>lambda.min</code>), or the more conservative <code>lambda.1se</code>. The simplified "LASSO-only" version that is the course's main approach stops here; the full procedure of Wysocki et al. (2025) treats this step as "edge selection" and follows it with an SEM refit (Lesson 7.5). EBIC is an "information criterion" geared toward finding the true structure; CV is geared toward "predicting accurately" and usually selects a denser network than EBIC(γ = 0.5). The course's <code>clpn_estimate()</code> supports both (<code>rule = "lambda.min" / "lambda.1se" / "ebic"</code>), and Lesson 7.2 compares them.</p>
""",
math=r"""
<h4>The objective of the graphical lasso</h4>
""" + MATH(r"\hat K=\arg\max_{K\succ0}\ \Big[\ \log\det K-\mathrm{tr}(SK)\ -\ \lambda\sum_{i\neq j}|k_{ij}|\ \Big]") + SYM([
(r"\(K\succ0\)", "K must be positive definite (so it is a valid precision matrix); for reference only"),
(r"\(\log\det K-\mathrm{tr}(SK)\)", "Gaussian log-likelihood (without constants): how well K agrees with the sample covariance S; larger is better"),
(r"\(\det,\ \mathrm{tr}\)", "Determinant and trace (sum of the diagonal); all you need to know is that they are \"summary numbers\" of a matrix"),
(r"\(\lambda\)", "Penalty strength. λ = 0 → no penalty; the larger λ, the more k<sub>ij</sub> are pushed to 0"),
(r"\(\sum_{i\neq j}|k_{ij}|\)", "The sum of the absolute values of all off-diagonal elements: the L1 penalty (the mark of LASSO)"),
]) + r"""
<h4>EBIC</h4>
""" + MATH(r"\mathrm{EBIC}=-2L+E\log N+4\gamma E\log p") + SYM([
(r"\(L\)", "The log-likelihood of the candidate network (goodness of fit; larger is better)"),
(r"\(E\)", "The number of edges in the network (number of parameters)"),
(r"\(N,\ p\)", "Sample size, number of nodes"),
(r"\(\gamma\)", "The EBIC hyperparameter, usually 0, 0.25 or 0.5"),
]) + r"""
<p>The first two terms are the ordinary BIC: the better the fit, the lower; the more edges, the higher. The third term is the "extra fine for edges," heavier the larger γ is. Note that the coefficient of the third term is 4γ (from Foygel & Drton, 2010: p nodes have about p²/2 possible edges, whose log is about 2 log p; multiplied by the 2γ in the definition of EBIC this gives 4γ log p; Epskamp & Fried, 2018, use this form).</p>
<h4>Why does the L1 penalty give "exactly 0"?</h4>
<p>Take a single coefficient: minimizing \((z-\beta)^2/2+\lambda|\beta|\) gives """ + r"""\(\hat\beta=\mathrm{sign}(z)\max(|z|-\lambda,0)\), called "soft thresholding": if |z| is not larger than λ the result is 0, and otherwise λ is subtracted. The interactive demonstration above uses exactly this formula. |β| has a "corner" at 0, which makes 0 an "attractor"; ridge regression uses a β² penalty, which has no corner, so its coefficients get smaller but never exactly 0.</p>
""",
code=CODE(r"""
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(qgraph) })
dat <- read_course_data()
items_t1 <- dat[, vars_t(1)]; names(items_t1) <- items     # Only the 9 items at T1
for (g in c(0, 0.25, 0.5)) {
  net <- estimateNetwork(items_t1, default = "EBICglasso", tuning = g,
                         corMethod = "cor_auto", verbose = FALSE)
  cat("gamma =", g, " edges =", sum(net$graph[upper.tri(net$graph)] != 0), "\n")
}
# For comparison: the unregularized partial correlation network (all 36 edges nonzero)
pc <- getWmat(qgraph(cor_auto(items_t1, verbose = FALSE), graph = "pcor", DoNotPlot = TRUE))
sum(pc[upper.tri(pc)] != 0)
""", "Core of R/L6-3.R") + r"""
<p><b>Arguments:</b> <code>default = "EBICglasso"</code> chooses the estimation method; <code>tuning</code> is γ; <code>corMethod = "cor_auto"</code> detects ordinal variables and uses polychoric correlations (see the next lesson); <code>net$graph</code> is the estimated weights (partial correlation) matrix. The second half of the script uses <code>genGGM()</code> and <code>ggmGenerator()</code> to generate data from a known true network and count false positives.</p>""",
quiz=[
("As γ gets larger, the EBICglasso network becomes:", ["Denser", "Sparser", "Unchanged", "Same number of edges, but smaller weights"], 1,
 ["The wrong way round: γ increases the penalty on the number of edges, so the network gets sparser.", "Correct: γ increases the penalty on the number of edges.", "With a large sample it may happen not to change (in the course data all three γ give 28 edges), but the direction is: larger γ, sparser network.", "γ changes which λ EBIC picks, and with it the number of edges; it does not shrink the weights while keeping the edges fixed."]),
("If regularization pushes an edge to 0, does that prove the two variables are unrelated?", ["Yes", "No: it only means that at this sample size and penalty the evidence is not enough to keep it", "Only when γ = 0.5", "Yes, as long as N > 500"], 1,
 ["This is the most common misreading: being pushed to 0 only means the evidence is not enough to keep the edge.", "Correct.", "γ only changes how heavy the penalty is; at any γ, being pushed to 0 does not prove the relationship is 0.", "With large samples weak edges are kept more easily, but an edge pushed to 0 still only means there isn't enough evidence."]),
("How does EBICglasso choose λ differently from cv.glmnet in CLPN?", ["Both use cross-validation; only the number of folds differs", "EBICglasso uses an information criterion (EBIC); cv.glmnet uses cross-validated prediction error", "The other way round: EBICglasso uses cross-validation and cv.glmnet uses EBIC", "EBICglasso doesn't use λ"], 1,
 ["EBICglasso does no cross-validation: it computes EBIC for the network at each candidate λ and picks the lowest.", "Correct.", "The wrong way round: the cv in cv.glmnet stands for cross-validation; EBICglasso uses EBIC.", "It first produces candidate networks for a sequence of λ values (usually 100) and then picks one with EBIC."]),
("In the course data (N = 800), all three γ values select a network with 28 edges. What does this tell you?", ["λ was chosen at the end of the candidate sequence, so the result can't be trusted", "With a large sample and strong associations, γ may have little effect", "γ has no effect at all", "You should switch to γ = 1"], 1,
 ["The script prints the chosen λ: all three γ choose the 81st of the 100 candidates (λ = 0.01375), not the smallest end of the sequence.", "Correct; in the small-sample simulation γ has a clear effect.", "In the small-sample simulation, going from γ = 0 to 0.5 cut the false positives from 10 to 1, a clear effect.", "γ should be fixed in advance; switching to γ = 1 after seeing the results only makes the network sparser, and it is trading tuning for results."]),
("The nonzero edge weights kept by LASSO estimation are usually:", ["Unbiased", "Systematically shrunk toward 0", "Larger than the true values", "Equal to the unpenalized partial correlations"], 1,
 ["The L1 penalty brings shrinkage bias: even the coefficients that are kept have had part of their size taken away.", "Correct.", "The wrong direction: LASSO shrinks coefficients toward 0; it never inflates them.", "They equal the unpenalized partial correlations only when λ = 0; when λ > 0 they are shrunk."]),
],
ex=[
("Comparing γ", "Hands-on", r"""<p>Run R/L6-3.R, record the number of edges and false positives under γ = 0, 0.25 and 0.5 for the course data and the simulated data, and write three observations.</p>""",
 r"""<p>Suggested observations: ① In the course data all three γ give 28 edges, the same network. ② In the small-sample simulation, going from γ = 0 to 0.5 reduces the edges from 22 to 13 and the false positives from 10 to 1. ③ The true network has 12 edges, and at γ = 0.5, 12 of the 13 estimated edges are true, so all true edges were found (γ = 0 and 0.25 also find all 12; the extras are false positives). But this is a single simulation; with another seed the numbers will vary, and with weaker true edges a large γ may also miss edges. Conclusion: in small samples γ is an important researcher degree of freedom; fix it in advance in the analysis plan, and you can add a sensitivity analysis.</p>"""),
("Soft thresholding by hand", "Basic", r"""<p>With λ = 0.1 and sample partial correlations of 0.35, 0.08, −0.15 and −0.04, what is each after soft thresholding?</p>""",
 r"""<p>0.35 → 0.25; 0.08 → 0; −0.15 → −0.05; −0.04 → 0. Rule: subtract λ from the absolute value; if that would go below 0, the result is 0; keep the original sign.</p>"""),
("Finding the \"best λ\" in the demonstration", "Understanding", r"""<p>In this page's demonstration, find the λ that gives "0 false positives and the fewest missed true edges" at N = 100, 300 and 1000, and write them down. How does the best λ depend on sample size?</p>""",
 r"""<p>The larger the sample, the smaller the sampling noise (about 1/√N), so a smaller λ is enough, and more weak true edges can be kept. At N = 1000, λ ≈ 0.05–0.08 may be enough; at N = 100 you need λ ≈ 0.15 or more, and several weak edges are missed. That is why the λ chosen by EBIC/CV depends on sample size, and why networks from small samples are necessarily sparser.</p>"""),
],
summary=["Finite sample → noise in every partial correlation → a screen full of small edges, many of them false positives.", "LASSO / glasso: add an L1 penalty, which pushes small edges to 0 (soft thresholding) and shrinks the large ones.", "EBICglasso = glasso produces candidates + EBIC chooses; larger γ, sparser network (default 0.5).", "Edge = 0 ≠ unrelated; regularized weights have shrinkage bias.", "CLPN chooses λ with cv.glmnet (cross-validation), usually giving denser networks than EBIC(γ = 0.5)."],
refs=["Epskamp, S., & Fried, E. I. (2018)", "Foygel, R., & Drton", "Tibshirani, R. (1996)", "Friedman, J., Hastie"],
)
