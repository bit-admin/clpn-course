# -*- coding: utf-8 -*-
L["7.3"] = dict(
lead=r"""<p>Once you have estimated the matrix B, you need to turn it into figures and tables that readers can understand, and write text that does not overstate the results. Not overstating is the focus of this lesson: every figure, table, and sentence should trace back to the numbers in the matrix.</p>""",
intuition=r"""
<h3>Common conventions for CLPN plots</h3>
<ol><li><b>Leave out the autoregressive loops.</b> Autoregressive edges (0.3–0.45) are usually much larger than cross-lagged edges (mostly below 0.15). If you draw the diagonal too (<code>diag = TRUE</code> in qgraph), qgraph gives the thickest lines to the self-loops, and the cross-lagged edges become thin and hard to tell apart; the loops also crowd the plot. So most papers report the autoregressive edges in a separate table and draw only the cross-lagged edges.</li>
<li><b>Color the nodes by construct</b> (loneliness vs. depression), and give the full item wording in the legend.</li>
<li><b>Directed arrows</b> (<code>directed = TRUE</code>); when there are edges in both directions, curved lines keep them apart (qgraph does this automatically; adjust with <code>curveAll</code> and <code>curve</code>).</li>
<li><b>State any display threshold.</b> Showing only edges with |β| ≥ some value is fine for readability, but it changes only the picture, not the model; say so in the figure note and give all edges in a table or the supplementary materials.</li></ol>
<p>In the widget below, check “Show autoregressive loops” and watch the cross-lagged edges fade; then drag the display threshold and see the plot get cleaner, and think about what the reader can no longer see. Click a node to highlight its outgoing and incoming edges.</p>
""" + W("clpn", title="CLPN plot: self-loops, display threshold, and node highlighting (population target of the course data)") + r"""
<h3>Tables: the two you need</h3>
<p>Table 1, autoregressive edges: β<sub>kk</sub> for each of the 9 nodes. For the course data (<code>lambda.min</code>): lone1 0.416, lone2 0.434, lone3 0.341, lone4 0.445, dep1 0.315, dep2 0.310, dep3 0.331, dep4 0.281, dep5 0.361.</p>
<p>Table 2, the strongest cross-lagged edges: an """ + T("edge list") + r""" sorted by |β| (from, to, β, ideally with the bootstrap intervals from Lesson 8.2). The 5 strongest in the course data:</p>
""" + TABLE(["Rank", "T1 → T2", "β (<code>lambda.min</code>)", "Population target", "Within-person truth"], [["1", "dep3 Sleep problems → dep4 Fatigue", "0.135", "{{V:pop_dep3>dep4}}", "{{V:win_dep3>dep4}}"], ["2", "lone2 Feeling left out → lone4 No one understands me", "0.127", "{{V:pop_lone2>lone4}}", "{{V:win_lone2>lone4}}"], ["3", "lone4 No one understands me → dep4 Fatigue", "0.108", "{{V:pop_lone4>dep4}}", "{{V:win_lone4>dep4}}"], ["4", "lone4 No one understands me → lone2 Feeling left out", "0.101", "{{V:pop_lone4>lone2}}", "{{V:win_lone4>lone2}}"], ["5", "lone4 No one understands me → lone3 Feeling isolated", "0.096", "{{V:pop_lone4>lone3}}", "{{V:win_lone4>lone3}}"]]) + r"""
<p class="muted" style="font-size:.88rem">Source: R/output/L7-3_log.txt (simulated course data, set.seed(2026), <code>lambda.min</code>); the two answer keys come from the two CSV files in data/. A real study does not have the last two columns.</p>
<p>Against the last two columns, the “5 strongest” fall into three cases:</p>
<ul><li>Edges 1 and 2 exist in both answer keys: these are trustworthy findings.</li>
<li>Edges 4 and 5 exist in the population target (about 0.06–0.07) but are 0 in the within-person truth: they are within-construct trait edges. If the research question is about “predictive relations in the population,” they are right; if you describe them as a process of individual change, such as “after feeling left out, people come to feel that no one understands them,” you are wrong (Lesson 7.2).</li>
<li>Edge 3, lone4 → dep4, is close to 0 in both answer keys. It is a false positive: sampling error pushed it to third place in this particular sample.</li></ul>
<p>Three of the top 5 start from lone4, which will put lone4 first on out-expected influence in Lesson 7.4. A ranked table looks certain, but the ranking from a single estimate carries both sampling error and trait edges into it. What you can do in a real study is check how unstable each edge is with the bootstrap intervals of Lesson 8.2, and draw conclusions in the text only about stable edges.</p>
<h3>How to write a careful interpretation</h3>
""" + TABLE(["Overstated", "Accurate"], [
["“Sleep problems cause fatigue.”", "“Controlling for all T1 items, T1 sleep problems had the strongest unique prediction of T2 fatigue (β = 0.14).”"],
["“‘No one understands me’ is the core symptom that drives depression.”", "“T1 ‘No one understands me’ had several edges to T2 depression items, suggesting it is a predictor worth following up in future research.”"],
["“Where there is no arrow in the plot, the two are unrelated.”", "“At the chosen penalty level, these cross-lagged edges were regularized to 0; that is, there was not enough evidence for a unique predictive effect.”"],
["“Loneliness is more important than depression.”", "“The total edge weight in the loneliness → depression direction was higher than in the depression → loneliness direction (0.56 vs. 0.08; see Lesson 7.4).”"]]) + r"""
""" + KEY("Writing formula:", "“Controlling for [all T1 nodes], T1 [A] positively/negatively predicted T2 [B] (β = …[, 95% bootstrap interval …]).” Then add a qualifier: “This is a temporal predictive association and may be affected by stable individual differences and unmeasured variables.”") + r"""
<h3>Figure note template</h3>
<p>“Figure 2. Cross-lagged panel network of loneliness (orange, lone1–lone4) and depressive symptoms (cyan, dep1–dep5), T1 → T2, N = 800. Arrows show standardized LASSO regression coefficients of T1 nodes predicting T2 nodes, controlling for all T1 nodes (10-fold cross-validation, <code>lambda.min</code>). Blue = positive, red = negative; thicker edges indicate larger |β|. For readability, autoregressive edges are not shown (see Table 1)[, and only edges with |β| ≥ 0.05 are shown; all edges are in Supplementary Table S1]. Node layout: Fruchterman–Reingold algorithm.”</p>
""",
math=r"""
<p>The “math” of this lesson is the rule that maps the matrix to the plot, and what a display threshold means.</p>
""" + MATH(r"\text{Draw edge } k\to j \iff |\hat\beta_{kj}|\ \ge\ \text{threshold}\ \ \text{and}\ k\neq j") + MATH(r"\text{Edge width}_{kj}\propto \frac{|\hat\beta_{kj}|}{\text{maximum}},\qquad \text{Color}=\mathrm{sign}(\hat\beta_{kj})") + SYM([
(r"\(\hat\beta_{kj}\)", "Estimated coefficient (the “hat” ^ marks an estimate, not the true value)"),
(r"\(\text{threshold}\)", "qgraph's <code>threshold</code> argument: only <b>show</b> edges with |β| at least this large"),
(r"\(\text{maximum}\)", "The |β| drawn as the thickest line; keep it fixed when you compare several plots"),
(r"\(\mathrm{sign}(\cdot)\)", "Sign function: positive → blue, negative → red"),
(r"\(k\neq j\)", "The diagonal (autoregression) is not drawn"),
]) + r"""
<h4>Why do self-loops “dilute” the cross-lagged edges?</h4>
<p>This applies only if the self-loops are actually drawn (<code>diag = TRUE</code>, or checking “Show autoregressive loops” in this page's widget); the code in this lesson first sets the diagonal to 0 with <code>cl_only()</code>, so the problem does not arise. If you don't fix <code>maximum</code>, qgraph sets it to the largest |β| in the plot. With self-loops, maximum ≈ 0.45 (an autoregression), so a cross-lagged edge of 0.1 has a relative width of only 0.1/0.45 ≈ 0.22; without self-loops, maximum ≈ 0.14 and the same edge has a relative width of 0.1/0.14 ≈ 0.71. The number has not changed, but it looks about three times as strong, so the figure note should state the maximum and whether self-loops are included.</p>
<h4>A threshold is not the same as “0”</h4>
<p>An edge that LASSO estimates as 0 (“no edge” in the model) and an edge not drawn because |β| is below the display threshold (“not drawn” in the plot) are two different things. The first is an estimation result; the second is a plotting choice. A paper must describe the two separately.</p>
""",
code=CODE(r"""
source("R/_setup.R"); library(qgraph)
dat <- read_course_data()
set.seed(2026)
B  <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], rule = "lambda.min")
CL <- cl_only(B); labs <- rownames(B)          # remove the diagonal
qgraph(CL, directed = TRUE, layout = "spring",
       labels = labs, groups = list(Loneliness = 1:4, Depression = 5:9),
       theme = "colorblind", asize = 4, legend = TRUE,
       nodeNames = paste(labs, item_en[labs]))  # item wording in the legend
# show only edges with |β| ≥ 0.05 (state this in the figure note!)
qgraph(CL, directed = TRUE, layout = "spring", labels = labs, groups = groups_list,
       theme = "colorblind", asize = 4, threshold = 0.05, curveAll = TRUE, curve = 0.4)
round(diag(B), 3)                              # Table 1: autoregressive edges
el <- edge_list(CL)                            # Table 2: edge list sorted by |β|
head(el, 10)
""", "Core of R/L7-3.R") + r"""
<p><b>Arguments:</b> <code>asize</code> sets the arrow size; <code>nodeNames</code> with <code>legend = TRUE</code> lists the full items on the right; <code>threshold</code> is the display threshold; <code>curveAll = TRUE</code> curves all edges so that edges in both directions don't overlap; <code>edge_list()</code> is a course helper that turns the matrix into a long from/to/weight table sorted by |β|.</p>""",
quiz=[
("Why do many CLPN papers leave the autoregressive edges out of the plot?", ["Autoregression doesn't matter", "Autoregressive edges are usually much larger than cross-lagged ones; drawing them crowds the plot and makes the cross-lagged edges hard to tell apart, so they are reported in a table instead", "qgraph cannot draw self-loops", "A CLPN estimates only cross-lagged edges, not autoregression"], 1,
 ["Autoregression matters: it represents stability and is part of what the cross-lagged estimates control for; it is just reported in a table instead.", "Correct.", "qgraph can draw self-loops (when the matrix includes the diagonal and diag = TRUE); leaving them out is a plotting choice.", "Every regression includes the outcome node's own T1 score, so the autoregression is always estimated."]),
("Does showing only edges with |β| above a threshold change the model? Where must you say so?", ["It changes the model; no need to say so", "It doesn't change the model, only the display; say so in the figure note and give all edges in a table or the supplementary materials", "It changes λ", "It is the same as LASSO shrinking these edges to 0"], 1,
 ["The threshold applies only to the plot; the model and its coefficients are unchanged. But readers cannot see these edges, so you must say so.", "Correct.", "λ is chosen by cross-validation during estimation; a plotting threshold does not change it.", "They differ: a LASSO 0 is an estimation result; edges below the threshold are merely not drawn and are still nonzero coefficients in the model."]),
("How should you write “the T1 insomnia → T2 fatigue edge is the strongest” accurately?", ["Insomnia causes fatigue", "Controlling for all T1 nodes, T1 insomnia had the strongest unique prediction of T2 fatigue (β = …)", "Fatigue is a consequence of insomnia", "Insomnia is the most important symptom in the network"], 1,
 ["“Causes” is causal language; a CLPN edge is only prediction over time after controlling for the T1 nodes.", "Correct.", "“Consequence” is causal language too; one predictive relation does not show that insomnia produces fatigue.", "The strongest single edge does not make its node the most important; at the node level you look at out-EI and similar measures and their stability (Lessons 7.4, 8.3)."]),
("No arrow between two nodes in the plot may mean:", ["The two are entirely unrelated", "LASSO estimated the edge as 0, or its |β| is below the display threshold; the two mean different things", "The edge is exactly 0 in the population", "The correlation between the two across time is 0"], 1,
 ["You cannot conclude they are unrelated: the edge may have been shrunk to 0 or simply not drawn; and the two may still be related through other nodes.", "Correct.", "A LASSO 0 only means there is not enough evidence; in the population target of the course data, no cell is exactly 0.", "A zero edge means no unique prediction after controlling for all T1 nodes; a correlation across time can still arise through other nodes."]),
("When you compare two CLPN plots, T1 → T2 and T2 → T3, you should:", ["Use the default settings for each", "Use the same layout (averageLayout) and the same maximum", "Draw self-loops in one and not the other", "Set each plot's display threshold to the median edge weight of that plot"], 1,
 ["With default settings, each plot's maximum is its own strongest edge and each layout is computed separately, so the same line width stands for different values.", "Correct.", "In the plot with self-loops the maximum is set by an autoregression, so its cross-lagged edges look thinner and the two plots are not comparable.", "Different thresholds mean different rules for which edges are shown; use the same threshold and state it in the figure note."]),
],
ex=[
("Plot and write a 150-word interpretation", "Hands-On + Writing", r"""<p>Run R/L7-3.R and open L7-3_clpn.png and L7-3_clpn_threshold.png. Write a 150-word paragraph that describes the figure and interprets the 3 strongest cross-lagged edges, paying close attention to your wording.</p>""",
 r"""<p>Sample: “Figure 2 shows the cross-lagged panel network from T1 to T2 (autoregressive edges in Table 1). Controlling for all T1 items, the three strongest cross-lagged edges were T1 sleep problems → T2 fatigue (β = 0.14), T1 feeling left out → T2 no one understands me (β = 0.13), and T1 no one understands me → T2 fatigue (β = 0.11). The third is a cross-construct edge: people with higher T1 scores on ‘no one understands me’ had slightly higher predicted T2 fatigue. This edge is weak, and its stability needs to be judged with bootstrap results. All of these are temporal predictive associations and do not represent within-person causal effects.”</p><p>The quoted text is how you would write it in a paper: a real study does not know the answer and can only check stability with the bootstrap (Lesson 8.2). For the course data the answer is known: the population target for lone4 → dep4 is only {{V:pop_lone4>dep4}}, and the within-person truth is {{V:win_lone4>dep4}}. The third-strongest edge in the sample is close to 0 in both answer keys, so being “the strongest” is not enough to draw a conclusion.</p>"""),
("Self-loops on and off", "Conceptual", r"""<p>In this page's widget, check and uncheck “Show autoregressive loops.” Describe how the cross-lagged edges change visually, and explain it with the formula from Essential Math.</p>""",
 r"""<p>With self-loops, the maximum is set by the largest autoregression (about 0.39), so a cross-lagged edge has a relative width of about β/0.39; without self-loops, maximum ≈ 0.17 and the same edge looks much thicker. (The widget draws the population target matrix true_B_population, hence 0.39 / 0.17 here; Essential Math used the <code>lambda.min</code> estimate, for which the numbers are 0.45 / 0.14. Same principle, different matrix.) The values don't change, but the visual impression does, so the figure note must state the plotting choices.</p>"""),
("Rewrite an overinterpretation", "Writing", r"""<p>Rewrite: “The results show that ‘no one understands me’ (lone4) is the key symptom through which loneliness drives depression, so interventions should target ‘no one understands me’ first.”</p>""",
 r"""<p>“In this sample, T1 ‘No one understands me’ had several positive cross-lagged edges to T2 depression items (e.g., → fatigue, → worthlessness) and the highest bridge out-expected influence (see Lesson 7.4). This suggests that ‘no one understands me’ may be a target worth testing in intervention studies; however, because CLPN edges are predictive relations in observational data and mix in stable individual differences, this result is not enough to establish an intervention target.”</p>"""),
],
summary=["CLPN plots: no self-loops (report them in a separate table), color by construct, directed arrows, full item wording in the legend.", "A display threshold changes only the plot, not the model; state it in the figure note.", "Two tables you need: autoregressive edges + a list of the strongest cross-lagged edges (better with bootstrap intervals).", "Writing formula: “Controlling for all T1 nodes, T1 A predicted T2 B (β = …).”", "A 0 in the model (LASSO) ≠ an edge not drawn in the plot (threshold)."],
refs=["Wysocki, A., McCarthy", "Epskamp, S., Cramer, A. O. J., Waldorp", "Funkhouser, C. J."],
)

L["7.4"] = dict(
lead=r"""<p>The strength and expected influence of Lesson 6.5 were designed for undirected networks. In a directed CLPN, each node has outgoing edges (it predicts others) and incoming edges (others predict it), so EI naturally splits in two: out-expected influence and in-expected influence.</p>""",
intuition=r"""
<h3>Two questions, two measures</h3>
<ul><li>""" + T("out-expected influence", "out-EI") + r""": as a T1 node, how much does this node predict the other T2 nodes in total? This is the sum of row k of B (diagonal excluded). Nodes with a high out-EI are often called “highly predictive.”</li>
<li>""" + T("in-expected influence", "in-EI") + r""": as a T2 node, how much is this node predicted by the other T1 nodes in total? This is the sum of column j (diagonal excluded). Nodes with a high in-EI are “easily predicted” and may lie “downstream” of other problems.</li></ul>
<p>As in Lesson 6.5, the “strength” versions sum absolute values: """ + T("out-strength / in-strength") + r""". When a CLPN has negative edges, report the EI versions first.</p>
<p>Where do these two measures come from? Summarizing CLPN nodes with out-EI / in-EI is common practice in the applied literature (e.g., Funkhouser et al., 2021), and the main track of this course follows it. The full procedure of Wysocki et al. (2025) uses a different pair of measures: in-prediction and out-prediction, which summarize a node by the proportion of variance explained instead of by adding up edge weights (definitions and formulas in <a href="L7-5.html#full-clpn">Lesson 7.5</a>). The two pairs answer similar questions (how strongly a node predicts others, how strongly others predict it), but on different scales: EI is a sum of signed coefficients, so positive and negative edges cancel; in-/out-prediction is a proportion of variance between 0 and 1. When you read a paper, first check which one the authors used; the numbers of the two cannot be compared directly.</p>
<h3>Why leave out the autoregression?</h3>
<p>The autoregression is a node “predicting itself,” whereas out-EI and in-EI are about relations with other nodes. If you included the autoregression, it would dominate the measures (0.3–0.45 is far larger than the cross-lagged edges) and the ranking would basically become “who is most stable.” So the diagonal is left out of the calculation.</p>
<h3>Bridge out-/in-EI: the “channels” between constructs</h3>
<p>Add up only the cross-construct edges: """ + T("bridge out-EI") + r""" = the sum of the edges from one loneliness item to all depression items (or from one depression item to all loneliness items); bridge in-EI is defined the same way. This answers the question we care most about directly: <i>which loneliness item best predicts later depression? Which depression item is most easily predicted by earlier loneliness?</i></p>
<p>The widget below shows the network, a table of the four measures, and bar charts at the same time (based on the population target matrix true_B_population of the course data, not the <code>lambda.min</code> estimate and not the within-person truth). Click a node to see its outgoing and incoming edges; then check in the table that out-EI is the sum of the outgoing edge weights.</p>
""" + W("clpn", mode="ei", title="Out-/in-expected influence and bridge EI (population target true_B_population of the course data)") + r"""
<h3>Results for the course data (<code>lambda.min</code> estimate)</h3>
""" + TABLE(["Node", "out-EI", "in-EI", "Bridge out", "Bridge in"], [
["lone1 Lack of companionship", "0.252", "0.092", "0.217", "0.000"], ["lone2 Feeling left out", "0.237", "0.055", "0.039", "−0.050"],
["lone3 Feeling isolated", "−0.027", "0.248", "−0.046", "0.081"], ["lone4 No one understands me", "<b>0.608</b>", "0.198", "<b>0.347</b>", "0.048"],
["dep1 Depressed mood", "0.352", "0.349", "0.045", "<b>0.177</b>"], ["dep2 Loss of interest", "0.193", "0.316", "0.055", "0.116"],
["dep3 Sleep problems", "0.250", "0.192", "0.000", "0.026"], ["dep4 Fatigue", "0.068", "<b>0.401</b>", "−0.028", "0.097"],
["dep5 Worthlessness", "0.224", "0.309", "0.007", "0.141"]]) + r"""
<p class="muted" style="font-size:.88rem">Source: R/output/L7-4_log.txt. Total loneliness → depression edge weight = {{V:ei74_est_sum_ld}}; depression → loneliness = {{V:ei74_est_sum_dl}}.</p>
<p>How to read it: lone4 (No one understands me) has the highest out-EI and bridge out-EI; dep4 (Fatigue) has the highest in-EI; dep1 (Depressed mood) has the highest bridge in-EI. The total edge weight from loneliness to depression is far larger than in the other direction, which agrees in direction with the CLPM result of Lesson 5.1 (loneliness → depression 0.13 vs. depression → loneliness 0.02).</p>
""" + WARN("But note:", "In neither answer key do lone4's outgoing edges stand out like this. With the population target, lone4's out-EI is {{V:ei74_pop_out_lone4}}, rank {{V:ei74_pop_out_lone4_rank}} of the 9 nodes; with the within-person truth it is {{V:ei74_win_out_lone4}}, rank {{V:ei74_win_out_lone4_rank}}. Its only cross-construct within-person edge is lone4 → dep5 ({{V:win_lone4>dep5}}). The estimated lone4 → dep4 ({{V:est72_min_lone4>dep4}}) is only {{V:pop_lone4>dep4}} in the population target and {{V:win_lone4>dep4}} in the within-person truth: a false positive. In other words, a centrality ranking from a single estimate can mislead. The CS-coefficient in Lesson 8.3 checks whether such a ranking is stable within this sample; whether it is close to the answer can only be checked with simulated data.") + r"""
<p>The construct-level totals can also be checked against the two answer keys (end of R/output/L7-4_log.txt):</p>
""" + TABLE(["Direction", "<code>lambda.min</code> estimate", "Population target", "Within-person truth"], [
["Loneliness → depression (sum of 4 × 5 edges)", "{{V:ei74_est_sum_ld}}", "{{V:ei74_pop_sum_ld}}", "{{V:ei74_win_sum_ld}}"],
["Depression → loneliness (sum of 5 × 4 edges)", "{{V:ei74_est_sum_dl}}", "{{V:ei74_pop_sum_dl}}", "{{V:ei74_win_sum_dl}}"]]) + r"""
<p>“Loneliness → depression” is larger than the reverse in all three columns. But “depression → loneliness” is positive in the population target ({{V:ei74_pop_sum_dl}}) and slightly negative in the within-person truth ({{V:ei74_win_sum_dl}}): the within-person truth has only two depression → loneliness edges, dep2 → lone3 ({{V:win_dep2>lone3}}) and dep4 → lone2 ({{V:win_dep4>lone2}}), one positive and one negative, which almost cancel. In the population target the negative edge is weakened to {{V:pop_dep4>lone2}}, and most of the other 18 positions hold small positive values, so the total becomes positive. So even with an infinite sample, the standard CLPN's “depression → loneliness is positive” is not a picture of the within-person process.</p>
<h3>Worked example: which edges make up lone4's out-expected influence?</h3>
<p>EI is a sum; take it apart before you interpret it. lone4's out-EI is the sum of the 8 numbers in the lone4 row of B (diagonal excluded):</p>
""" + TABLE(["T1 lone4 → T2", "<code>lambda.min</code> estimate", "Population target", "Within-person truth"],
 [[f"{ZH[j]} ({j})", "{{V:est72_min_lone4>" + j + "}}", "{{V:pop_lone4>" + j + "}}", "{{V:win_lone4>" + j + "}}"] for j in NODES if j != "lone4"]
 + [["Total (out-EI)", "{{V:ei74_est_out_lone4}}", "{{V:ei74_pop_out_lone4}}", "{{V:ei74_win_out_lone4}}"]]) + r"""
<p class="muted" style="font-size:.88rem">Source: R/output/L7-2_B_lambda_min.csv (the same estimate as in this lesson) and R/output/L7-4_log.txt; the two answer keys come from the two CSV files in data/.</p>
<ol><li><b>No single strong edge.</b> All 8 outgoing edges are positive, and even the largest, lone4 → dep4, is only {{V:est72_min_lone4>dep4}}. An out-EI of about 0.6 is many small edges added up, not one strong predictive relation.</li>
<li><b>Small edges are exactly where the errors are.</b> Among the small edges that LASSO (<code>lambda.min</code>) keeps, false positives are most common (Lesson 7.2). When you add up 8 edges, you add up their errors too: the estimated total is {{V:ei74_est_out_lone4}}, the population target only {{V:ei74_pop_out_lone4}}. Most of the gap comes from edges such as lone4 → dep4 and lone4 → dep1 that are close to 0 in the population.</li>
<li><b>Against the within-person truth.</b> Of the 8 edges, only lone4 → dep5 ({{V:win_lone4>dep5}}) is an edge in the within-person truth; the edges to the other 3 loneliness items are trait edges.</li></ol>
<p>So when you read that “node X has the highest out-EI,” first check whether it consists of one or two strong edges or of many small ones. In the first case you can go back and check those one or two edges (the intervals of Lesson 8.2); in the second, the total is sensitive to both sampling error and the λ rule, and the ranking may change with <code>lambda.1se</code>. This is also why Lesson 8.3 checks the stability of EI rankings.</p>
<h3>The term “""" + T("driver node") + r"""”</h3>
<p>Some papers call nodes with a high out-EI “drivers” and nodes with a high in-EI “receivers.” These words strongly suggest causation. More careful wording is “most predictive” and “most predicted.” To call a node an intervention target, you also need (1) a stable measure (CS ≥ 0.25, preferably ≥ 0.5); (2) replication in other samples or time periods; (3) theoretical plausibility and a node you can actually intervene on; and (4) ultimately, a test in intervention studies.</p>
""",
math=r"""
""" + MATH(r"\text{out-EI}_k=\sum_{j\neq k}\beta_{kj}\quad(\text{sum of row }k),\qquad \text{in-EI}_j=\sum_{k\neq j}\beta_{kj}\quad(\text{sum of column }j)") + MATH(r"\text{bridge out-EI}_k=\sum_{j\notin C(k)}\beta_{kj},\qquad \text{bridge in-EI}_j=\sum_{k\notin C(j)}\beta_{kj}") + SYM([
(r"\(\beta_{kj}\)", "CLPN coefficient: k at T1 → j at T2"),
(r"\(\sum_{j\neq k}\)", "Sum over all elements of row k except the diagonal"),
(r"\(C(k)\)", "The construct node k belongs to (loneliness or depression)"),
(r"\(j\notin C(k)\)", "Sum only over nodes of the other construct"),
]) + r"""
<h4>A check: the two totals are equal</h4>
<p>The sum of out-EI over all nodes = the sum of in-EI over all nodes = the sum of all off-diagonal elements of the matrix (each edge is “sent” by exactly one node and “received” by exactly one node). For the course data: total out-EI = 0.252 + 0.237 − 0.027 + 0.608 + 0.352 + 0.193 + 0.250 + 0.068 + 0.224 ≈ 2.157, total in-EI ≈ 2.159 (rounding error). Likewise, the sum of bridge out-EI over all loneliness nodes = the total loneliness → depression edge weight = 0.557. This is a good way to check your code.</p>
<h4>In R</h4>
<p><code>rowSums(CL)</code> = out-EI; <code>colSums(CL)</code> = in-EI, where CL is the matrix with its diagonal set to 0. <code>rowSums(abs(CL))</code> and <code>colSums(abs(CL))</code> give out-strength and in-strength.</p>
""",
code=CODE(r"""
source("R/_setup.R"); library(qgraph)
dat <- read_course_data()
set.seed(2026)
B  <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)])
CL <- cl_only(B); p <- ncol(CL)
outEI <- rowSums(CL)   # edges leaving the node (predicting others)
inEI  <- colSums(CL)   # edges entering the node (predicted by others)
comm  <- c(rep("Loneliness", 4), rep("Depression", 5))
bridgeOut <- sapply(seq_len(p), function(k) sum(CL[k, comm != comm[k]]))
bridgeIn  <- sapply(seq_len(p), function(j) sum(CL[comm != comm[j], j]))
data.frame(node = rownames(CL), outEI, inEI, bridgeOut, bridgeIn)
sum(CL[comm == "Loneliness", comm == "Depression"])   # total loneliness → depression edge weight
sum(CL[comm == "Depression", comm == "Loneliness"])   # total depression → loneliness edge weight
# qgraph's built-in measures (directed network)
g <- qgraph(CL, directed = TRUE, DoNotPlot = TRUE)
centralityPlot(g, include = c("OutExpectedInfluence", "InExpectedInfluence"), scale = "raw0")
""", "Core of R/L7-4.R") + r"""
<p><b>Notes:</b> <code>sapply(1:p, function(k) …)</code> computes once for each node k; <code>comm != comm[k]</code> picks the columns of the construct that k does not belong to. <code>centralityPlot(…, scale = "raw0")</code> shows raw values (with 0 as the reference); you can also use <code>"z-scores"</code>.</p>""",
quiz=[
("What do rowSums(CL) and colSums(CL) correspond to?", ["in-EI; out-EI", "out-EI; in-EI", "Strength; EI", "Autoregression; cross-lagged edges"], 1,
 ["Reversed: rows are origins, so a row sum is the sum of a node's edges to others, i.e., out-EI.", "Correct: row = origin, column = destination.", "Strength and EI differ in whether you take absolute values, not in rows vs. columns; rowSums(abs(CL)) is out-strength.", "The diagonal of CL is already 0, so neither row sums nor column sums contain autoregression."]),
("Why is the autoregressive edge usually left out when computing EI?", ["Autoregression is always negative", "The measures are about relations with other nodes; including the autoregression would let stability dominate the ranking", "Autoregression is too small to affect the ranking", "Autoregression is not a regression coefficient"], 1,
 ["In the course data all autoregressions are positive (about 0.28–0.45).", "Correct.", "The opposite: autoregressions (0.3–0.45) are far larger than cross-lagged edges and would dominate the ranking.", "It is a regression coefficient too (k at T1 → k at T2); it is left out because it answers a different question (stability)."]),
("Is the node with the highest out-EI necessarily the best intervention target?", ["Yes", "Not necessarily: you also need stability (CS), replication, theory and the ability to intervene, and a test in intervention studies", "Yes, if out-EI > 0.5", "Yes, if the bootstrap interval of its out-EI does not include 0"], 1,
 ["That is overinterpretation: in the course data, lone4 has the highest out-EI, yet it does not stand out in either answer key (see “But note” in this lesson).", "Correct.", "There is no such cutoff; the size of EI also depends on which nodes are in the network.", "An interval that excludes 0 only says the estimate is unlikely to be 0; whether the ranking is stable, replicates, and can be intervened on needs other evidence."]),
("A loneliness node's bridge out-EI is:", ["The sum of its edges to all nodes", "The sum of its edges to all depression nodes", "The sum of the edges from all depression nodes to it", "The sum of the absolute values of its edges to all depression nodes"], 1,
 ["That is out-EI, which also includes edges to nodes of its own construct (loneliness).", "Correct.", "Wrong direction: that is its bridge in-EI.", "With absolute values it is bridge out-strength; bridge out-EI keeps the signs, so negative edges cancel."]),
("How does the sum of out-EI over all nodes relate to the sum of in-EI over all nodes?", ["The first is always larger", "They are equal (both equal the sum of all cross-lagged edges)", "They are equal only when there are no negative edges", "They are opposites"], 1,
 ["Each edge is counted exactly once in out-EI and once in in-EI, so the two totals must be equal.", "Correct: you can use this to check your code.", "Negative edges are also counted once as “out” and once as “in,” so the totals are equal with negative edges too.", "They are equal, not opposites."]),
],
ex=[
("Out-/in-EI bar charts and comparing constructs", "Hands-On", r"""<p>Run R/L7-4.R and open L7-4_EI_bars.png. Which construct “predicts” the other more? Support your answer with the two totals, and add a one-sentence qualifier.</p>""",
 r"""<p>Total loneliness → depression edge weight 0.557, depression → loneliness 0.079: in this sample, the loneliness items predict later depression items far more than the reverse. Qualifier: “This is a descriptive comparison based on a single LASSO estimate; it does not yet take sampling variability into account (the difference can be tested with the bootstrap), and the result may be affected by stable individual differences.”</p>"""),
("Compute by hand and check", "Foundational", r"""<p>A 3-node CLPN has the CL matrix (row → column): A→B = 0.2, A→C = −0.1, B→C = 0.3, C→A = 0.05, all others 0. Find each node's out-EI and in-EI, and check that the two totals are equal.</p>""",
 r"""<p>out-EI: A = 0.1, B = 0.3, C = 0.05 (total 0.45). in-EI: A = 0.05, B = 0.2, C = 0.2 (total 0.45). Equal.</p>"""),
("Estimated EI ranking vs. the two answer keys", "Extension", r"""<p>Read the population target matrix with <code>true_B()</code> and the within-person truth with <code>read.csv("data/true_B_within.csv", row.names = 1)</code>. For each, set the diagonal to 0, compute out-EI, and compute its Spearman correlation with the estimated out-EI (<code>cor(…, method = "spearman")</code>). Do the same for in-EI. Do the rankings agree? What does this tell you?</p>""",
 r"""<p>Reference code: <code>Bt &lt;- true_B(); diag(Bt) &lt;- 0; cor(rowSums(Bt), outEI, method = "spearman")</code>; the same for the within-person truth (the end of R/L7-4.R already computes both comparisons). Results for the course data:</p>
<ul><li><b>out-EI</b>: the Spearman correlation is only {{V:ei74_rho_out_pop}} with the population target and only {{V:ei74_rho_out_win}} with the within-person truth. In the estimate, {{V:ei74_est_out_top}} ranks first ({{V:ei74_est_out_lone4}}); in the population target the highest are {{V:ei74_pop_out_top}} ({{V:ei74_pop_out_dep3}}) and {{V:ei74_pop_out_top2}} ({{V:ei74_pop_out_lone2}}), with lone4 ({{V:ei74_pop_out_lone4}}) at rank {{V:ei74_pop_out_lone4_rank}}; in the within-person truth the highest is yet another node, {{V:ei74_win_out_top}} ({{V:ei74_win_out_lone3}}). The two answer keys themselves give different out-EI rankings.</li>
<li><b>in-EI</b>: the Spearman correlations with the population target and the within-person truth are {{V:ei74_rho_in_pop}} and {{V:ei74_rho_in_win}}, much more consistent.</li></ul>
<p>Two conclusions. First, a centrality ranking from a single estimate can be swayed by sampling variability and LASSO selection; assess its stability with the case-dropping bootstrap (Lesson 8.3) before you interpret it. Second, even a stable ranking, even one that matches the population target, is not necessarily the ranking of the within-person process: out-EI also adds up the small within-construct edges produced by traits.</p>"""),
],
summary=["out-EI = row sum (predicting others); in-EI = column sum (predicted by others); neither includes the autoregression.", "Bridge out-/in-EI count only cross-construct edges and answer “which loneliness item best predicts later depression?”", "Course data: total loneliness → depression edge weight 0.557 vs. depression → loneliness 0.079; lone4 has the highest out-EI, dep4 the highest in-EI.", "A ranking from a single estimate can mislead → check the CS-coefficient (Lesson 8.3).", "Avoid causal words such as “driver”; say “most predictive” / “most predicted.”"],
refs=["Robinaugh, D. J., Millner", "Jones, P. J., Ma", "Wysocki, A., McCarthy"],
)
