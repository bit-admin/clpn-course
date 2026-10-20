# -*- coding: utf-8 -*-
L["6.4"] = dict(
lead=r"""<p>This lesson shows you how to estimate a network with bootnet and draw a publication-ready network plot with qgraph. The CLPN lessons use these plotting arguments again and again.</p>""",
intuition=r"""
<h3>Two packages, two jobs</h3>
<ul><li><b>bootnet</b>: estimation (<code>estimateNetwork()</code>) and, later in Module 8, stability checks (<code>bootnet()</code>). It wraps methods such as EBICglasso and ggmModSelect in one interface.</li>
<li><b>qgraph</b>: plotting and centrality. <code>plot(net)</code> actually calls qgraph.</li></ul>
<h3>What does a "good" network plot need?</h3>
""" + TABLE(["Element", "qgraph argument", "Why"], [
["Node layout", "<code>layout = \"spring\"</code>", "Fruchterman–Reingold spring algorithm: strongly connected nodes are \"pulled\" closer together, so the structure is easier to see"],
["Group colors", "<code>groups = list(Depression = 1:9, Anxiety = 10:16)</code>", "Readers can tell scales/constructs apart at a glance"],
["Node labels", "<code>labels = c(\"D1\", …)</code>", "Short labels on the plot; the full items go in the caption or legend"],
["Legend", "<code>legend = TRUE</code>, <code>nodeNames = …</code>", "Explains the groups and gives the full items"],
["Maximum edge weight", "<code>maximum = 0.5</code>", "Fixes \"what counts as thickest,\" so several plots can be compared"],
["Colorblind-friendly", "<code>theme = \"colorblind\"</code> (edges: blue positive, red negative, with colorblind-friendly node colors); <code>palette = \"colorblind\"</code> only changes the colors of the node groups", "About 8% of men have a color vision deficiency; the two arguments do different things (see this lesson's \"Common questions\")"]]) + r"""
<h3>Can you "interpret" a spring layout?</h3>
<p>The spring layout imagines the network as balls joined by springs: the stronger the edge, the tighter the spring and the closer the nodes. The system is then allowed to "relax" into the position with the lowest energy. Its only purpose is to make the plot easy to read:</p>
<ul><li>Two nodes close together usually have a fairly strong connection to each other, or to shared neighbors;</li>
<li>but distances cannot be read precisely: the algorithm starts from random positions, so the same network with another seed may come out rotated or mirrored, and a node in the middle is not necessarily "the most important."</li></ul>
""" + WARN("Common mistake:", "\"Node A sits in the center of the network, so it is the core symptom.\" Position is a product of the plotting algorithm; to judge what is \"core,\" look at centrality indices (6.5) and their stability (8.3).") + r"""
<h3>Comparing networks: fix the layout and the maximum</h3>
<p>If you compare two networks, such as men vs. women, or two CLPNs for T1→T2 and T2→T3, you must:</p>
<ol><li><b>Use the same layout:</b> compute an average layout with <code>L &lt;- averageLayout(net1, net2)</code>, then <code>plot(net1, layout = L)</code> and <code>plot(net2, layout = L)</code>. Otherwise the same node sits in different places in the two plots and readers can't compare them.</li>
<li><b>Use the same maximum:</b> by default qgraph draws the strongest edge in each plot as the thickest. If network 1's strongest edge is 0.3 and network 2's is 0.6, the two look equally thick unless you fix maximum. Setting <code>maximum = 0.6</code> (the larger of the two) makes thickness comparable.</li></ol>
<h3>cor_auto: which correlation for ordinal items?</h3>
<p>Scale items are usually """ + T("ordinal variables") + r""" with 4–5 levels. Treating them as continuous and computing Pearson correlations underestimates the associations. <code>corMethod = "cor_auto"</code> checks how many distinct values each variable has: those with few values (by default ≤ 7) are treated as ordinal and get """ + T("polychoric correlations") + r""" (which assume a continuous normal latent variable behind each item, "cut" into levels); the rest get Pearson correlations. The course data's items were generated exactly this way (continuous scores cut into 4 levels). Note: polychoric correlations can be unstable with very few levels, small samples, or very skewed distributions.</p>
<h3>Exporting figures for publication</h3>
<p>Journals usually want vector graphics (PDF/EPS) or bitmaps of at least 300 dpi. In R, <code>pdf()</code> / <code>cairo_pdf()</code> produce vector graphics, and <code>png(…, res = 300)</code> a high-resolution bitmap. The course's <code>png_open()</code> in <code>_setup.R</code> already takes care of the font settings.</p>
""",
math=r"""
<p>This lesson is mostly about plotting; there are just a few pieces of math worth understanding:</p>
<h4>1. How edge thickness is mapped</h4>
<p>qgraph draws edge width roughly in proportion to (simplified):</p>
""" + MATH(r"\text{width}_{ij}\ \propto\ \frac{|w_{ij}| - \text{minimum}}{\text{maximum} - \text{minimum}}") + SYM([
(r"\(|w_{ij}|\)", "The absolute value of the edge weight"),
(r"\(\text{maximum}\)", "The weight drawn as \"thickest\"; by default the largest |w| in the plot"),
(r"\(\text{minimum}\)", "Edges below it are not drawn (default 0). Note: setting minimum changes only the display, not the model"),
]) + r"""
<p>So if two plots have different maximum values, the same thickness stands for different numbers; that is why you fix maximum.</p>
<h4>2. The "energy" of the spring layout</h4>
<p>The Fruchterman–Reingold algorithm puts an attractive force \(f_a(d)=d^2/k\) between connected nodes and a repulsive force \(f_r(d)=k^2/d\) between all nodes (\(d\) is the distance, \(k\) a constant for the ideal distance); the stronger the edge, the stronger the attraction. Nodes are moved again and again until the forces balance. All you need to know: it is a heuristic algorithm, and there is no "one correct" layout.</p>
<h4>3. The intuition of polychoric correlation</h4>
<p>Suppose item X has a continuous latent variable \(X^*\sim N(0,1)\) behind it, and you observe level 1, 2, 3 or 4 depending on which interval between the thresholds \(\tau_1,\tau_2,\tau_3\) \(X^*\) falls in. The polychoric correlation is the correlation of the two latent variables \(X^*, Y^*\), estimated by maximum likelihood from the cross-table of the two items.</p>
""",
code=CODE(r"""
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(qgraph) })
items <- read.csv(out("L6-4_dep_anx_items.csv"))   # The script first simulates "9 depression + 7 anxiety" items
net <- estimateNetwork(items, default = "EBICglasso",
                       tuning = 0.5, corMethod = "cor_auto")
plot(net, layout = "spring",
     groups = list(Depression = 1:9, Anxiety = 10:16),
     legend = TRUE, palette = "colorblind",
     title = "Depression–Anxiety EBICglasso Network")
# Vector figure for submission
cairo_pdf(out("L6-4_network.pdf"), 8, 6, family = plot_font)
plot(net, layout = "spring", groups = list(Depression = 1:9, Anxiety = 10:16), legend = TRUE)
dev.off()
""", "Core of R/L6-4.R (data simulated by the script with genGGM() + ggmGenerator())") + r"""
<h4>The standard way to compare two networks</h4>
""" + CODE(r"""
dat <- read_course_data()
x1 <- dat[, vars_t(1)]; x2 <- dat[, vars_t(2)]; names(x1) <- names(x2) <- items
n1 <- estimateNetwork(x1, default = "EBICglasso", corMethod = "cor_auto")
n2 <- estimateNetwork(x2, default = "EBICglasso", corMethod = "cor_auto")
L  <- averageLayout(n1, n2)                         # Shared layout
mx <- max(abs(c(n1$graph, n2$graph)))               # Shared maximum
par(mfrow = c(1, 2))
plot(n1, layout = L, maximum = mx, groups = groups_list, title = "T1")
plot(n2, layout = L, maximum = mx, groups = groups_list, title = "T2")
""", "For the exercise: comparing the cross-sectional networks at T1 and T2 in the course data"),
quiz=[
("Why fix the layout and maximum when you compare two network plots?", ["To make the plots nicer and more compact", "So that each node is in the same place and the same thickness means the same value, making the plots comparable", "Fixing maximum puts the edge weights of both networks on the same scale", "To reduce the number of edges"], 1,
 ["Looks are not the point: without fixing them, the same node sits in different places and the same thickness means different values, so the two plots can't be compared.", "Correct.", "maximum only changes how weights are mapped to line width; it doesn't change any edge weight.", "Neither layout nor maximum changes the number of edges or the model."]),
("Can the distance between two nodes in a spring layout be read precisely?", ["Yes: distance = 1 − partial correlation", "No: the layout is the result of a heuristic algorithm and is only a rough guide", "Yes: the central node is the most important", "Only when N > 1000"], 1,
 ["There is no such conversion: the layout only puts strongly connected nodes roughly close together, and a different random start rotates or mirrors it.", "Correct.", "Position is a product of the plotting algorithm; to judge \"importance,\" look at centrality (6.5) and its stability (8.3).", "The randomness of the layout has nothing to do with sample size; a large sample doesn't make distances precisely interpretable."]),
("How does corMethod = \"cor_auto\" decide which correlation to use?", ["By sample size", "By how many distinct values a variable has (few → ordinal, polychoric correlation)", "By whether a variable passes a normality test", "By whether a variable is an integer"], 1,
 ["cor_auto ignores sample size; polychoric correlations can be unstable in small samples, but that is a separate issue to watch.", "Correct.", "cor_auto does no normality test; it decides whether a variable is ordinal by its number of values (by default ≤ 7).", "Integer is not the same as ordinal: an integer variable with many values (such as age) still gets a Pearson correlation as a continuous variable."]),
("What does setting minimum = 0.1 in qgraph do?", ["Sets the edges with |w| < 0.1 in the model to 0", "Only hides the edges with |w| < 0.1; the model itself is unchanged", "Works like a larger EBIC γ, making the estimated network sparser", "Changes the layout algorithm"], 1,
 ["The estimate (net$graph) is unchanged; minimum only affects the plot.", "Correct; if you use it, you must say so in the caption.", "γ acts at the estimation stage; minimum only hides small edges in the plot, and the estimates stay the same.", "The layout algorithm is chosen with layout; minimum decides which edges are drawn."]),
("A network plot for a journal submission is best exported as:", ["A screenshot of the RStudio plot pane", "A vector PDF or a PNG of ≥ 300 dpi", "A bitmap at png()'s default resolution (72 dpi)", "A small image enlarged in Word"], 1,
 ["A screenshot's resolution depends on the screen, usually far below 300 dpi, and it blurs when enlarged.", "Correct.", "Without res, png() uses 72 dpi, which is blurry in print; add res = 300, or export a PDF.", "Enlarging a bitmap adds no detail, it only blurs; choose a vector format or high resolution at export."]),
],
ex=[
("A publication-quality network plot", "Hands-on", r"""<p>Run R/L6-4.R and open R/output/L6-4_network.png and .pdf. Then change the code: add <code>nodeNames</code> (the full item names), put the legend on the right, and export again.</p>""",
 r"""<p>Reference: <code>plot(net, layout = "spring", groups = list(Depression = 1:9, Anxiety = 10:16), nodeNames = c(paste("Depression item", 1:9), paste("Anxiety item", 1:7)), legend.cex = 0.4, palette = "colorblind")</code>. With nodeNames, qgraph puts the legend on the right automatically and lists the full names. Check: are the labels readable, do nodes overlap, does the caption state the estimation method (EBICglasso, γ = 0.5) and what the edge colors mean?</p>"""),
("T1 vs. T2 networks", "Hands-on", r"""<p>Run the "comparing two networks" code above. Plot once without <code>layout = L, maximum = mx</code> and once with them, and describe the difference.</p>""",
 r"""<p>Without fixing: the nodes are in different places in the two plots and hard to match, and each plot draws its own strongest edge as the thickest. With fixing: each item is in the same place, and thickness can be compared directly. In the course data, the T1 and T2 networks should be very similar in structure (the data were generated by a stationary process). You can quantify the similarity with <code>cor(n1$graph[upper.tri(n1$graph)], n2$graph[upper.tri(n2$graph)])</code>: the solution script <code>R/solutions/L6-4_solution.R</code> finds 28 and 29 nonzero edges in the T1 and T2 networks and a correlation of the edge weights of r = 0.878.</p>"""),
("Writing a caption", "Writing", r"""<p>Write a proper caption (3–4 sentences) for your network plot.</p>""",
 r"""<p>Example: "Figure 1. Regularized partial correlation network of depression (D1–D9) and anxiety (A1–A7) items (EBICglasso, γ = 0.5, polychoric correlations, N = 600). Blue edges are positive partial correlations, red edges negative; thicker edges are stronger associations (the maximum edge width corresponds to |r| = 0.5). Nodes were placed with the Fruchterman–Reingold algorithm; distances between nodes have no precise meaning."</p>"""),
],
summary=["bootnet estimates (estimateNetwork), qgraph plots (plot / qgraph).", "A good plot: spring layout, groups colors, short labels + legend, colorblind colors.", "Comparing plots: fix the layout with averageLayout() and fix maximum.", "Layout distances cannot be read precisely; position ≠ importance.", "cor_auto uses polychoric correlations for ordinal items; minimum only affects the display."],
refs=["Epskamp, S., Cramer, A. O. J., Waldorp", "Epskamp, S., Borsboom, D., & Fried", "Isvoranu, A.-M., Epskamp"],
)

L["6.5"] = dict(
lead=r"""<p>Once the network is drawn, the question people most want answered is: "Which symptom matters most?" Centrality indices try to answer it. This lesson shows you how to compute and interpret them, and what they cannot tell you. The out-EI / in-EI of CLPN (Lesson 7.4) are the directed versions of this lesson's indices.</p>""",
intuition=r"""
<h3>"Important" can mean many things</h3>
""" + TABLE(["Index", "The question it asks", "Stability in psychological networks"], [
["Strength", "How large is the \"total connection\" of all this node's edges?", "Usually fairly stable"],
["Expected influence (EI)", "Keeping the signs, how large is this node's \"net\" association with its neighbors?", "Usually fairly stable"],
["Betweenness", "How often does this node lie on the shortest path between other nodes?", "Often unstable"],
["Closeness", "How short is this node's average distance to all other nodes?", "Often unstable"],
["Bridge EI", "How strong is this node's net connection to other communities?", "Depends on the data"]]) + r"""
<h3>Strength vs. expected influence: what negative edges change</h3>
<p>""" + T("Strength") + r""" adds up the absolute values of all edges; """ + T("expected influence", "EI") + r""" adds them up with their signs (Robinaugh, Millner & McNally, 2016). If a node has only two edges, +0.3 and −0.3: strength = 0.6, EI = 0. Imagine "social support" has a strong negative edge with "loneliness": judged by strength, social support looks very "central." But if you think in terms of "activation" (when one symptom rises, does the network as a whole get more active or calmer?), a negative edge acts as a brake, and EI reflects that better. When a network has negative edges, EI is usually more suitable than strength; when all edges are positive, the two are the same.</p>
<h3>Bridge centrality: the "connection points" of comorbidity</h3>
<p>When a network contains two (or more) communities defined in advance, such as depression and anxiety, """ + T("bridge centrality") + r""" (Jones, Ma & McNally, 2021) counts only the edges between a node and the nodes of other communities. A node with high bridge EI may be a channel through which one disorder "spreads" to another, which bears directly on research on """ + T("comorbidity") + r""". In CLPN we will use "bridge out-EI" to ask: which loneliness item best predicts the later depression items?</p>
<p>In the calculator below, select the bridge edge "D3—A1," change its weight from 0.25 to −0.25, and watch how D3's strength, EI and bridge EI change; then find a case with "high bridge strength but low bridge EI."</p>
""" + W("cent") + r"""
<h3>Why use betweenness and closeness with care?</h3>
<p>Betweenness and closeness are both based on "shortest paths," and shortest paths are extremely sensitive to small changes in single edges: whether one weak edge is pushed to 0 by regularization or kept can reroute a shortest path completely. The stability analyses of Epskamp et al. (2018) keep finding that, at typical sample sizes, the CS-coefficients of betweenness and closeness are often very low (Lesson 8.3), so more and more papers report only strength and EI.</p>
<h3>"Central = intervention target"? Not so simple</h3>
<p>"The most central symptom is the best target for intervention" is a popular claim in the network literature, but it has several problems:</p>
<ol><li><b>The edges of a cross-sectional network are undirected associations</b> and say nothing about direction: a node with high strength may be the one "most affected by the others," a result rather than a cause.</li>
<li><b>Centrality may reflect overlapping item content</b>: two items with similar wording have a strong edge between them, which raises both of their centralities ("topological overlap," Lesson 9.2).</li>
<li><b>Can it be changed?</b> Being statistically central doesn't mean something can be changed in practice (for example, "loss of interest" is hard to target directly).</li>
<li><b>Stability</b>: if the centrality ranking itself is unstable (low CS), any claim about "the most central" has no basis.</li></ol>
""" + KEY("An acceptable way to write it:", "\"In this cross-sectional network, A6 had the highest expected influence (z = …), suggesting many positive connections with other symptoms; the stability of this index was CS = …. This result can suggest candidate targets for later longitudinal or intervention studies, but cannot on its own justify choosing an intervention target.\""),
math=r"""
""" + MATH(r"\text{Strength}_i=\sum_{j\neq i}|w_{ij}|,\qquad \mathrm{EI}_i=\sum_{j\neq i}w_{ij}") + MATH(r"\text{Bridge strength}_i=\sum_{j\notin C(i)}|w_{ij}|,\qquad \text{Bridge EI}_i=\sum_{j\notin C(i)}w_{ij}") + SYM([
(r"\(w_{ij}\)", "The weight of the edge between nodes i and j (a partial correlation in a GGM)"),
(r"\(\sum_{j\neq i}\)", "Sum over all nodes j other than i"),
(r"\(C(i)\)", "The community node i belongs to (e.g., \"depression\")"),
(r"\(j\notin C(i)\)", "Sum only over nodes not in i's community: the edges \"across communities\""),
]) + r"""
<h4>A small example</h4>
<p>Node D3 has the edges D3—D1 = 0.2, D3—D2 = 0.3, D3—A1 = 0.25 (bridge edge), D3—A3 = −0.1 (bridge edge).</p>
<ul><li>Strength = 0.2 + 0.3 + 0.25 + 0.1 = 0.85</li><li>EI = 0.2 + 0.3 + 0.25 − 0.1 = 0.65</li><li>Bridge strength = 0.25 + 0.1 = 0.35; bridge EI = 0.25 − 0.1 = 0.15</li></ul>
<h4>Standardized reporting</h4>
<p>From qgraph 1.9 on, <code>centralityPlot()</code> defaults to <code>scale = "raw0"</code> (raw values, starting from 0); only <code>centralityPlot(…, scale = "z-scores")</code> turns each index into z scores, \(z_i=(c_i-\bar c)/s_c\), which makes it easy to put different indices in one plot. A z score only says how high a node is "relative to the other nodes in this network"; it cannot be compared directly across studies.</p>
<h4>Two-step bridge (for reference)</h4>
<p>networktools also offers "Bridge Expected Influence (2-step)," which also counts indirect connections through one intermediate node (indirect edge weight = the product of the two weights). The course always reports the 1-step version.</p>
""",
code=CODE(r"""
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(qgraph); library(networktools) })
items <- read.csv(out("L6-4_dep_anx_items.csv"))      # Run L6-4.R first
net <- estimateNetwork(items, default = "EBICglasso", tuning = 0.5, corMethod = "cor_auto")
W <- net$graph
data.frame(strength = colSums(abs(W)),                # Strength = Σ|w|
           EI       = colSums(W))                     # EI = Σw
centralityPlot(net, include = c("Strength", "ExpectedInfluence"), scale = "z-scores")
# Bridge centrality uses the 9 T1 items of the course data instead: 4 loneliness and 5 depression items are two communities defined in advance
dat <- read_course_data()
t1 <- dat[, vars_t(1)]; colnames(t1) <- items
net_c <- estimateNetwork(t1, default = "EBICglasso", tuning = 0.5, corMethod = "cor_auto")
b <- bridge(net_c$graph, communities = ifelse(items %in% lone_items, "Loneliness", "Depression"))  # Communities must be specified
sort(b$`Bridge Expected Influence (1-step)`, decreasing = TRUE)
plot(b, include = "Bridge Expected Influence (1-step)")
""", "Core of R/L6-5.R") + r"""
<p>Excerpt of the actual results (R/output/L6-5_log.txt): the highest strength is A6 (0.566), and the highest EI is also A6 (0.565); D1 has strength 0.473 but EI only 0.252, so D1 has sizable negative edges.</p>
<p>The bridge part uses the 9 T1 items of the course data (two communities, loneliness and depression). The top two in bridge EI are lone3 Feeling isolated (0.163) and dep5 Worthlessness (0.133); the strongest single edge across communities is lone3—dep5 itself (0.103). All 12 edges across communities are positive, so here bridge EI equals bridge strength; the lowest is dep4 Fatigue (0.016).</p>
""" + NOTE("About the data:", "The \"9 depression + 7 anxiety items\" data in 6.4–6.5 are cross-sectional data simulated at random by the script with <code>genGGM()</code>; the node names D1–D9 and A1–A7 do not correspond to real scale items. Its true network is a \"ring lattice\" (each node is connected only to its neighbors in the numbering), and there are no \"depression\" and \"anxiety\" communities in it; bridge indices computed on it would only reflect where a node sits on the ring. So strength and EI are demonstrated on these data, and bridge centrality on the course data, which has real communities."),
quiz=[
("A node has only two edges, +0.3 and −0.3. What are its strength and EI?", ["0.6 and 0.6", "0.6 and 0", "0 and 0.6", "0.3 and 0"], 1,
 ["EI keeps the signs, so +0.3 and −0.3 cancel to 0; 0.6 is the strength.", "Correct.", "The wrong way round: strength adds absolute values (0.6), EI adds with signs (0).", "0.3 counts only one edge; strength adds the absolute values of both."]),
("When a network has negative edges, why is EI usually more suitable than strength?", ["Strength counts negative edges as negative numbers, pulling the node's score down", "Strength counts braking negative edges as \"connection\" too; EI reflects the net direction of activation", "EI is always larger than strength", "Strength can't be used for directed networks"], 1,
 ["The opposite: strength takes absolute values, so negative edges are added as positive \"connection.\"", "Correct (Robinaugh et al., 2016).", "EI ≤ strength: a sum with signs can't exceed the sum of absolute values.", "Directed networks have out-strength and in-strength too (7.4); that is not a reason to choose EI."]),
("Why does bridge centrality need the communities to be specified in advance?", ["Because it only adds up edges to nodes in other communities, so it must know who belongs where", "The communities are only used for coloring and don't affect the values of the bridge indices", "bridge() splits the communities automatically by edge weight; specifying them only speeds things up", "To compute betweenness"], 0,
 ["Correct.", "The community split directly decides which edges count as \"across communities\"; a different split gives different bridge values.", "The split has to come from the researcher (it can also come from a community detection algorithm run beforehand and passed in); the comment in this lesson's R code says exactly \"Communities must be specified.\"", "Betweenness is based on shortest paths and needs no communities; it is the bridge indices that do."]),
("What is the main problem with \"the most central symptom is the best intervention target\"?", ["Centrality in a cross-sectional network only describes associations, so it is worthless", "Cross-sectional edges have no direction, may reflect overlapping content, say nothing about whether the symptom can be changed, and centrality may be unstable", "With a large enough sample, the most central node is the target", "Intervention targets can only be found with RCTs"], 1,
 ["That goes too far: centrality can suggest candidate targets; it just can't justify an intervention on its own.", "Correct: each of these needs extra evidence.", "A large sample only makes estimates more stable; it can't fix the problems of direction, overlapping content and changeability.", "An RCT is the final test; the problem with the claim is the big jump from centrality straight to a target."]),
("In the psychological network literature, which centrality indices are usually the least stable?", ["Strength", "Expected influence", "Betweenness and closeness", "Bridge EI"], 2,
 ["Strength adds up all edges, so a small change in one edge matters little; it is usually fairly stable.", "Like strength, EI is a sum of edges and usually fairly stable.", "Correct: they are based on shortest paths, and whether one weak edge stays or goes can reroute a path.", "It depends on the data, but it is also a sum of edges and usually does better than betweenness and closeness."]),
],
ex=[
("Centrality and bridges", "Hands-on", r"""<p>Run R/L6-5.R and open L6-5_centrality.png and L6-5_bridge.png. Name the top 2 nodes in bridge EI and write a careful interpretation (3–4 sentences). Extra: change <code>include</code> to <code>c("Betweenness", "Closeness")</code>, draw the centralityPlot again, and explain in a sentence or two why this lesson doesn't put these two indices in its conclusions.</p>""",
 r"""<p>Top two: lone3 Feeling isolated (0.163) and dep5 Worthlessness (0.133). Suggested interpretation: "In the cross-sectional network at T1, 'Feeling isolated' and 'Worthlessness' had the strongest conditional associations with the other construct, and the edge between them was the strongest edge across constructs; they are candidate 'connection points' where loneliness and depression occur together. Because the network is cross-sectional and undirected, we cannot tell the direction, and the stability of these estimates must be checked with a case-dropping bootstrap (see 8.3). These nodes are candidates worth attention in later longitudinal research." Extra: betweenness and closeness are both based on "shortest paths"; whether a weak edge is pushed to 0 or kept reroutes the shortest paths, so the ranking changes easily, and what a "path" actually means in a psychological network is unclear. Their CS-coefficients are usually very low (8.3), so they are for reference only and stay out of the conclusions.</p>"""),
("Centrality by hand", "Basic", r"""<p>Node X has edges to Y (0.4) and Z (−0.2) in its own community, and to U (0.1) and V (0.15) in the other community. Compute strength, EI, bridge strength and bridge EI.</p>""",
 r"""<p>Strength = 0.4 + 0.2 + 0.1 + 0.15 = 0.85; EI = 0.4 − 0.2 + 0.1 + 0.15 = 0.45; bridge strength = 0.25; bridge EI = 0.25.</p>"""),
("Feeling the negative edges in the calculator", "Understanding", r"""<p>In this page's calculator, set D1—D2 = 0.4 and D1—D3 = −0.4, and compare D1's strength and EI. Then explain: if you reported only strength, how would readers misread D1?</p>""",
 r"""<p>D1's strength is high (≥ 0.8) and its EI close to 0. With only strength, readers would think D1 is "tightly connected to many symptoms, and activating it would set the network going," but in fact its positive and negative connections cancel out, and the net effect of "activating D1" in the network may be small. That is the motivation for Robinaugh and colleagues' EI.</p>"""),
],
summary=["Strength = Σ|w|; EI = Σw; prefer EI when there are negative edges.", "Bridge strength / bridge EI count only edges across communities; the communities must be specified in advance.", "Betweenness and closeness are based on shortest paths, are often unstable, and should be used with care.", "Centrality ≠ intervention target: direction, overlapping content, changeability and stability all need extra evidence.", "The out-EI / in-EI of CLPN are directed versions of EI (7.4)."],
refs=["Robinaugh, D. J., Millner", "Jones, P. J., Ma", "Epskamp, S., Borsboom, D., & Fried"],
)
