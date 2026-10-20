# -*- coding: utf-8 -*-
RES_FIELDS = [["N", "Sample size N", "800"], ["p", "Number of nodes", "9"], ["E", "Number of nonzero cross-lagged edges", "52"], ["Emax", "Possible cross-lagged edges p(p−1)", "72"],
["armin", "Smallest autoregression", "0.28"], ["armax", "Largest autoregression", "0.45"],
["e1", "Strongest edge 1 (with β)", "T1 'Sleep problems' → T2 'Fatigue' (β = 0.14)"], ["e2", "Strongest edge 2", "T1 'Feeling left out' → T2 'No one understands me' (β = 0.13)"], ["e3", "Strongest edge 3", "T1 'No one understands me' → T2 'Fatigue' (β = 0.11)"],
["ld", "Sum of loneliness → depression edges", "0.56"], ["dl", "Sum of depression → loneliness edges", "0.08"],
["outn", "Node with highest out-EI (value)", "'No one understands me' (0.61)"], ["inn", "Node with highest in-EI (value)", "'Fatigue' (0.40)"],
["bridge", "Node with highest bridge out-EI (value)", "'No one understands me' (0.35)"],
["cso", "CS of out-EI", "{{V:cs10_out}}"], ["csi", "CS of in-EI", "{{V:cs10_in}}"],
["boot", "Bootstrap conclusion", "{{V:b10_n_excl0}} of the {{V:b10_n}} cross-lagged edges had 95% bootstrap intervals excluding 0, and the intervals of the strongest edges overlapped heavily"],
["sens", "Sensitivity results", "lambda.1se (r = .67, 17 edges), adding covariates (r = 1.00), T2→T3 replication (r = .64)"],
["full", "Full-procedure sensitivity analysis", "the {{V:fp10_n_keep}} cross-lagged paths that were nonzero in either interval entered the path model; equality test Δχ²({{V:fp10_eq_ddf}}) = {{V:fp10_eq_dchisq}}, p = {{V:fp10_eq_p}}, so the {{V:fp10_final_short}} was used; after pruning at p < .01, {{V:fp10_n_sig01}} cross-lagged edges were kept, including {{V:fp10_top_kept}} of the {{V:fp10_top_n}} strongest edges of the main analysis"]]
RES_TEXT = """Results

Network structure. Among the {{p}} nodes of the cross-lagged panel network (N = {{N}}), {{E}} nonzero cross-lagged edges were estimated (of {{Emax}} possible edges). All autoregressive edges were positive, ranging from {{armin}} to {{armax}}, indicating moderate stability of the items between the two measurements. The three strongest cross-lagged edges were {{e1}}, {{e2}} and {{e3}} (see Figure 1 and Table 2). The sum of edge weights from loneliness items to depression items was {{ld}}, and from depression items to loneliness items {{dl}}.

Centrality. The node with the highest out-expected influence was {{outn}}, and the node with the highest in-expected influence was {{inn}}; the node with the highest bridge out-expected influence was {{bridge}} (see Figure 2 and Table 3).

Accuracy and stability. The nonparametric bootstrap showed that {{boot}} (see Figure 3). The case-dropping bootstrap gave a correlation stability coefficient of CS = {{csi}} for in-expected influence and CS = {{cso}} for out-expected influence (see Figure 4). The CS of in-expected influence is close to the 0.5 cutoff (about 0.44–0.52 under different random seeds), i.e., borderline stable, so its ranking is interpreted only cautiously. Following Epskamp et al. (2018), the ranking of an index with CS below 0.25 should not be interpreted, and CS above 0.5 is desirable.

Sensitivity analyses. {{sens}}.

Full-procedure sensitivity analysis. Following the full procedure recommended by Wysocki et al. (2025) (LASSO edge selection → unpenalized re-estimation of the path model → equality test across time → pruning at p < .01), {{full}}."""
PRES_ITEMS = ["#Structure of a 10-minute talk (about 8–10 slides)",
"1 slide: title, your name, the research question in one sentence",
"1 slide: why it matters (practice background: what you observed in your work)",
"1 slide: data and design (N, waves, interval, nodes)",
"1 slide: flow chart of the method (nodewise LASSO → network → centrality → stability)",
"2 slides: main results (network plot + strongest edges / centrality, one point each)",
"1 slide: stability and sensitivity (which conclusions hold; which edges are kept in both the main analysis and the full procedure)",
"1 slide: limitations (between/within-person, causation, measurement, sample)",
"1 slide: practice implications and next steps",
"#Self-check before the talk",
"Each slide has only one point",
"The network plot is labeled with the item names, not just lone4, dep4",
"You can explain \"cross-lagged edge\" in one non-statistical sentence",
"Ready to answer: \"Why not RI-CLPM?\" \"Why isn't the full procedure the main analysis?\" \"What does a low CS mean?\" \"Does this show causation?\"",
"Rehearse once with a timer and stay within 10 minutes"]
L["10.3"] = dict(
lead=r"""<p>The last step: turn the analysis into text that others can read and check, and explain it clearly in 10 minutes. This lesson provides a template for the results section (with numbers filled in automatically), a guide to writing limitations and a checklist for the talk.</p>""",
intuition=r"""
<h3>Principle: every number can be found in the code output</h3>
<p>The most common error in a results section is a miscopied number: the table was revised, but the text still has the old version. The best fix is to let the code fill in the numbers. <code>R/L10-3.R</code> reads the results saved by L10-2 (<code>L10-2_results.rds</code>) and automatically generates a draft of the results, <code>R/output/L10-3_results_draft.md</code> (see the actual output below). You rewrite the wording on the basis of the draft, but you do not change numbers by hand; when a number changes, rerun the script.</p>
<h3>Structure of the """ + T("results section") + r""" (APA style)</h3>
<ol><li><b>Network structure:</b> number of edges (as a share of the possible edges), range of autoregression, the strongest cross-lagged edges, sums of edge weights in the two directions.</li>
<li><b>Centrality:</b> nodes with the highest out-EI / in-EI / bridge EI (point to the table and figure).</li>
<li><b>Accuracy and stability:</b> overall picture of the bootstrap intervals, CS-coefficients and the standard used.</li>
<li><b>Sensitivity:</b> how well the alternative analyses agree with the main analysis, and whether the main conclusions change.</li>
<li><b>Full-procedure sensitivity analysis:</b> model choice (equality test, AIC, BIC), edges kept after pruning, edge-by-edge agreement with the main analysis (see "How to write up the two analyses" below).</li></ol>
<p>The results section only states the findings without discussing them; interpretation, comparison with the literature, limitations and practical implications go in the discussion.</p>
<h3>Results template (fill in the blanks)</h3>
<p>The gray hints in the input boxes are the actual results for the course data (from the L10-2 / L10-3 output), so you can follow them; if you use your own data, replace them with your numbers.</p>
""" + WJ("tpl", "Results template (matches L10-3_results_draft.md)", "res103", {"fields": RES_FIELDS, "text": RES_TEXT}) + r"""
""" + WARN("Two things you must change after filling it in", "<p>(1) In the course data, the CS of out-EI = {{V:cs10_out}} &lt; 0.25, so the sentence \"the node with the highest out-expected influence was 'No one understands me'\" must be followed by \"but this index was not sufficiently stable, so the ranking is not interpreted\". (2) Avoid causal verbs such as \"influences\" or \"causes\": write \"edge A → B\" as \"A at T1 predicted B at T2\".</p>") + r"""
<h3>How to write up the two analyses: methods, results and discussion</h3>
<p>The main analysis (LASSO only) and the required sensitivity analysis (the full procedure, Lesson 10.2) each appear once in three places, with different jobs: the methods say how each analysis was done and how results are interpreted; the results state the two sets of results side by side; the discussion explains what the agreements and disagreements mean.</p>
<h4>Writing the methods (data analysis)</h4>
<p>Describe the settings of both analyses in enough detail that someone else could redo them (Lesson 9.3). You can adapt the paragraph below, replacing the content in parentheses with your own settings:</p>
<blockquote>“The main analysis was a LASSO-only cross-lagged panel network: each T2 item was regressed on all 9 T1 items in a separate LASSO regression (glmnet, 10-fold cross-validation, lambda.min, random seed 2026), with items z-standardized beforehand; the nonzero coefficients form the edges of the network. As specified in the analysis plan, the full procedure recommended by Wysocki et al. (2025) served as a sensitivity analysis: the same LASSO was run for T1→T2 and for T2→T3, cross-lagged paths that were 0 in both intervals were fixed to 0, and the remaining cross-lagged paths and all autoregressive paths were estimated without penalty in a path model in lavaan (version number); all residuals within a wave were allowed to correlate, and missing values were handled with FIML. A model with equality constraints across time was compared with an unconstrained model using a nested χ² test, AIC and BIC, and the constrained model was used when none of the three argued against equality. Cross-lagged paths with p &lt; .01 in the final model were considered retained, and each node's in-prediction and out-prediction were computed. Edges retained in both analyses were treated as main findings, and edges found in only one analysis as exploratory findings.”</blockquote>
<p>Note the last sentence: the interpretation rule is part of the method, so it belongs in the methods, not introduced only in the discussion.</p>
<h4>Writing the results</h4>
<p>The full procedure gets its own paragraph, after the other sensitivity analyses. The draft generated automatically by <code>R/L10-3.R</code> (<code>L10-3_results_draft.md</code> in the "Actual output" below) already contains this paragraph, which covers five things in order:</p>
<ol><li>what was done (a one-sentence recap of the settings; details in the methods);</li>
<li>model choice: Δχ², degrees of freedom and p-value of the equality test, which way AIC and BIC point, which model was used and its fit indices;</li>
<li>how many cross-lagged edges were kept after pruning, and how many in each direction;</li>
<li>agreement with the main analysis: how many of the main analysis's edges were kept, and which of the strongest were not (with both estimates and the p-value);</li>
<li>construct level: the sums of edge weights in the two directions in each analysis.</li></ol>
<p>For the course data, the key numbers of this paragraph are: {{V:fp10_n_keep}} cross-lagged paths entered the SEM; equality test Δχ²({{V:fp10_eq_ddf}}) = {{V:fp10_eq_dchisq}}, p = {{V:fp10_eq_p}}, so the {{V:fp10_final_short}} was used; {{V:fp10_n_sig01}} edges kept after pruning; {{V:fp10_top_kept}} of the {{V:fp10_top_n}} strongest edges of the main analysis kept. The results only state these, without explaining "why".</p>
<h4>Writing the discussion</h4>
""" + TABLE(["Situation", "Results", "Discussion"], [
["Kept by both analyses", "List these edges with both estimates", "Interpret them as main findings; note that they do not depend on the estimation method. Cite the unpenalized estimates for effect sizes"],
["Nonzero only in the main analysis", "State that they were not kept by the full procedure (give the p-value)", "Describe them as \"sensitive to the estimation method\" and interpret them only as exploratory; do not base practice recommendations on them. If an edge appears in only one interval of data, say so"],
["Kept only by the full procedure", "State that they were 0 in the main analysis", "Likewise report them only as exploratory; explain that they come from combining the two intervals of data"],
["Direction at the construct level", "Sums of edge weights in the two directions, one set per analysis", "If the directions agree, it can go in the abstract; if not, you can only say \"the direction depends on the estimation method\""]]) + r"""
<p>A discussion paragraph for the course data could read like this (numbers from the L10-2b output):</p>
<blockquote>“The networks from the two estimation methods are similar overall (correlation of the coefficients over the 72 cross-lagged positions r = {{V:fp10_r_lasso_sem}}), but the full procedure keeps far fewer edges ({{V:fp10_n_sig01}}, against {{V:fp10_n_lasso_main}} in the main analysis). Loneliness → depression edges kept by both analyses: {{V:fp10_kept_ld_list}}; depression → loneliness edges: {{V:fp10_kept_dl_list}}. The fairly strong 'No one understands me → Fatigue' edge of the main analysis was not kept by the full procedure: it appears only in the T1→T2 interval (its LASSO estimate in the T2→T3 interval is {{V:fp10_lone4>dep4_t23}}), and it is not significant once the two intervals are combined (p = {{V:fp10_lone4>dep4_p}}). This study therefore does not treat it as a main path from loneliness to depression. In both analyses, the sum of edge weights in the loneliness → depression direction is larger than in the reverse direction; this construct-level pattern does not depend on the estimation method.”</blockquote>
""" + WARN("Common mistakes when writing up the two analyses", r"""<ul>
<li><b>Mentioning the full procedure only when it agrees.</b> It is required, and it matters even more when it disagrees.</li>
<li><b>Writing "the full procedure confirmed …".</b> A sensitivity analysis can only show whether a result depends on the estimation method; it cannot "confirm" an edge, let alone prove causation.</li>
<li><b>Attributing numbers to the wrong analysis.</b> p-values and standard errors come only from the full procedure (LASSO gives no p-values); CS-coefficients and bootstrap intervals come only from the main analysis. Make clear which analysis each number comes from.</li>
<li><b>Mixing the coefficients of the two analyses in one ranking table.</b> LASSO coefficients are shrunk and unpenalized estimates are not, so their sizes cannot be compared.</li>
<li><b>Thinking that agreement between the two analyses removes the limitations.</b> Both are based on observed scores and both mix between-person and within-person effects (Lesson 10.2, "Agreement between the two analyses does not make it a within-person process").</li></ul>""") + r"""
<h3>""" + T("Limitations") + r"""</h3>
<p>The limitations tell readers where the results can and cannot be generalized. A CLPN study should discuss at least these five points:</p>
""" + TABLE(["Aspect", "What to say", "Example wording"], [
["Between-person / within-person", "A standard CLPN is based on observed scores and mixes stable individual differences with within-person change (Lessons 5.2–5.3)", "“The cross-lagged edges in this study may partly reflect stable between-person differences rather than within-person dynamic processes; future research could use models that separate between-person effects (such as network extensions of the RI-CLPM).”"],
["Causation", "Edges are predictive relationships over time and may be affected by unmeasured third variables", "“The cross-lagged edges cannot be interpreted as causal effects.”"],
["Measurement", "Single items have low reliability; item content may overlap; the measurement interval may not be the best time scale for the process (Lesson 5.4)", "“Each node was measured by a single item … the 6-month interval may …”"],
["Estimation method", "The LASSO coefficients of the main analysis are shrunk and include false positives; the full procedure is more conservative and misses weak edges; both are based on observed scores", "“Some edges of the main analysis were not retained by the full procedure, and their interpretation is exploratory; at p < .01 the full procedure may miss weaker true edges.”"],
["Sample", "Source of the sample, representativeness, attrition", "“The sample came from …; whether the conclusions generalize to … remains to be tested.”"]]) + r"""
<p>If you used the simulated data, you can also say: "Because the true structure is known, this study assessed the method's performance: the correlation between estimated and true edges was 0.65, suggesting …"</p>
<h3>""" + T("Practice implications") + r""": how to explain it to social work colleagues</h3>
<p>Imagine explaining the main findings to a social work colleague who has never studied statistics. You could say:</p>
<blockquote>“We followed 800 people for six months. People who felt lonelier tended to have more depressive symptoms six months later; the other way round, depression predicted later loneliness much more weakly (this difference was tested with the bootstrap, Lesson 8.3, exercise 1). Which particular kind of loneliness matters, these data cannot say: the top few items could change with a different group of people. And this is only a predictive relationship; it does not prove that depression will go down if loneliness is reduced. If you design a group program, you could try making the reduction of loneliness as a whole the goal, and evaluate the effect.”</blockquote>
<p>This explanation has three parts: the finding (in everyday language), its limits (not causal, rankings of single items unstable) and a testable suggestion for action.</p>
""" + WARN("Why not recommend \"focus on feeling understood\"", "<p>In the sample, \"No one understands me\" has both the highest out-EI and the highest bridge out-EI, and \"No one understands me → Fatigue\" is one of the strongest edges, so it is tempting to write \"helping clients feel understood should be the priority\". But the CS of out-EI is only {{V:cs10_out}}, so the ranking cannot be interpreted. And against the two kinds of truth for the course data (Lesson 10.2, \"Edge-by-edge comparison with the true structure\"), \"No one understands me → Fatigue\" is only {{V:pop_lone4>dep4}} in the population, while the strongest loneliness → depression edge under both kinds of truth is \"Feeling isolated → Depressed mood\" ({{V:truth_ld_pop}}). The required full-procedure sensitivity analysis did not keep this edge either (Lesson 10.2: SEM re-estimate {{V:fp10_lone4>dep4_sem}}, p = {{V:fp10_lone4>dep4_p}}). An intervention designed around the most eye-catching item in the sample would pick the wrong focus. Practice recommendations can only rest on patterns that are stable, overall and consistent across the two analyses.</p>") + r"""
<h3>""" + T("Academic presentation") + r""": 10 minutes</h3>
""" + WJ("checklist", "10-minute talk checklist (saved automatically)", "pres103", PRES_ITEMS) + r"""
<h3>Questions readers or reviewers may ask (prepare your answers)</h3>
<details class="ans"><summary>“Why not use the RI-CLPM?”</summary><p>Suggested answer: the RI-CLPM separates between-person and within-person effects, but so far it is used mainly for a few variables (total scores); the strength of a CLPN is the network structure at the item level. The two answer different questions. In the limitations I state that the CLPN mixes between-person and within-person effects.</p></details>
<details class="ans"><summary>“What does CS = {{V:cs10_out}} mean?”</summary><p>It means that dropping only a small share of participants may change the out-EI ranking considerably, so I do not interpret the out-EI ranking and only report the values.</p></details>
<details class="ans"><summary>“Wysocki et al. recommend the full procedure; why did you still use LASSO only for the main analysis?”</summary><p>Suggested answer: to allow direct comparison with published CLPN studies, and to be able to run the edge-weight bootstrap and compute CS-coefficients, both of which are built on the LASSO estimate. The analysis plan lists the full procedure as a required sensitivity analysis, and its results are reported alongside; the main findings are only the edges kept by both analyses.</p></details>
<details class="ans"><summary>“When the two analyses disagree, which one do you believe?”</summary><p>Suggested answer: I do not believe either one all the way. LASSO tends to report too many edges, the full procedure too few. By the rule written in advance, edges kept by both are the main findings; edges found in only one analysis I describe as "sensitive to the estimation method" and interpret only as exploratory. Because the course data are simulated, you can see the cost of this rule: the full procedure misses quite a few weak real edges.</p></details>
<details class="ans"><summary>“Does this show causation?”</summary><p>No. A cross-lagged edge is a predictive relationship over time, controlling for all T1 items, and it may still be affected by unmeasured variables or between-person differences.</p></details>
<details class="ans"><summary>“If you did the study again, what would you change?”</summary><p>For example: add waves, so that models separating within-person effects (the RI-CLPM and its network extensions) can be estimated more stably (with 3 waves the RI-CLPM is just identified, but its estimates are very imprecise; see Lesson 5.3); choose an interval that fits the time scale of the process; measure key nodes with several items; preregister; enlarge the sample to improve the stability of centrality.</p></details>
<h3>Scoring guide (for self-assessment)</h3>
""" + TABLE(["Dimension", "What excellent looks like"], [
["Research question", "Not causal, item level, two-directional, and relevant to practice"],
["Reproducibility", "Runs in one step; every number can be found in the output"],
["Analysis", "Follows the plan; includes stability analysis, the required full-procedure sensitivity analysis and other sensitivity analyses; does not over-interpret unstable indices or edges found in only one analysis"],
["Writing", "Clear structure; figures and tables follow the conventions; numbers accurate"],
["Limitations and implications", "Honest and specific, with testable practice suggestions"],
["Presentation", "Clear within 10 minutes; able to answer questions"]]) + r"""
""",
math=r"""
<p>The summary numbers the results section reports can all be computed directly from the estimated matrix \(\hat B\).</p>
""" + MATH(r"\text{density}=\frac{E}{p(p-1)}=\frac{52}{72}\approx 0.72") + SYM([
["\\(E\\)", "Number of nonzero cross-lagged edges"], ["\\(p\\)", "Number of nodes; \\(p(p-1)\\) is the number of possible cross-lagged edges"]]) + r"""
<p>A density of 0.72 is high, which is typical of lambda.min (it tends to keep edges, including some false positives; Lesson 7.2). Reporting the density in the results reminds readers how "dense" the network is.</p>
""" + MATH(r"S_{L\to D}=\sum_{k\in L}\sum_{j\in D}\hat\beta_{kj}=0.56,\qquad S_{D\to L}=\sum_{k\in D}\sum_{j\in L}\hat\beta_{kj}=0.08") + SYM([
["\\(L,\\ D\\)", "The set of loneliness items (lone1–4) and the set of depression items (dep1–5)"],
["\\(S_{L\\to D}\\)", "Sum of the weights of all cross-lagged edges from loneliness to depression"]]) + r"""
<p>Note: the number of nonzero edges may differ between the two directions, but in each direction there are 4 × 5 = 20 possible edges, so the two sums can be compared directly. They are only descriptive summaries, though, and have no significance test of their own; to say "the loneliness → depression direction is stronger", you need to test the distribution of this difference in the bootstrap (Lesson 8.3, exercise 1, does this test with <code>L8-2_boot.rds</code>).</p>
<h4>APA number format</h4>
<p>Whether to write a 0 before the decimal point and how many decimals to keep: follow the rules under "Reporting precision" in Lesson 9.3, consistently throughout.</p>
""",
code=CODE(r"""
source("R/_setup.R")
res <- readRDS(out("L10-2_results.rds"))      # run L10-2.R first
B <- res$B; CL <- cl_only(B); cen <- res$cen; cs <- res$cs
f <- function(x) sprintf("%.2f", x)
txt <- c("## Results (draft, numbers filled in automatically)",
  sprintf("A total of %d nonzero cross-lagged edges were estimated; autoregressive edges ranged from %s to %s.",
          sum(CL != 0), f(min(diag(B))), f(max(diag(B)))),
  sprintf("The sum of edge weights from loneliness to depression was %s, and %s in the reverse direction.",
          f(sum(CL[1:4, 5:9])), f(sum(CL[5:9, 1:4]))))
writeLines(txt, out("L10-3_results_draft.md"))
""", "The core idea of R/L10-3.R: use sprintf to \"fill\" numbers into sentences (excerpt)"),
quiz=[
("What is the best way to get the numbers in the results section?", ["Read them off the plots", "Copy them by hand from the tables", "Generate them automatically from the result objects with code", "Copy them from the printout in the R console, keeping all decimals"], 2,
 ["Reading off plots is imprecise, and you cannot read the third decimal from a plot.", "Easy to miscopy; the table gets revised and the text still has the old version.", "Correct.", "More precise than reading off plots, but still copying by hand: once the analysis is rerun, the text is out of date; and keeping all decimals does not follow reporting precision."]),
("Which sentence belongs in the results section?", ["Loneliness caused depression", "T1 'No one understands me' predicted T2 'Fatigue' (β = 0.11)", "This shows social workers should make loneliness the first target of intervention", "This matched our expectations completely, which is exciting"], 1,
 ["\"Caused\" is causal wording; a CLPN gives only predictive relationships.", "Correct.", "This belongs in the discussion (practical implications), and it jumps straight from a predictive relationship to intervention.", "Subjective evaluation is not a result; the results only state findings."]),
("In discussing the limitations of a CLPN, which point is most specific to the method and must be mentioned?", ["Sample size", "An observed-score CLPN mixes between-person and within-person effects", "Single items have low reliability", "Software version"], 1,
 ["It should be discussed too, but every study has sample size issues; it is not specific to CLPN.", "Correct.", "It should be discussed too, but single-item reliability is common to all item-level networks; the mixing of between- and within-person effects is what is specific to an observed-score CLPN.", "The software version goes in the methods; it is not a limitation."]),
("When explaining to colleagues without a statistics background, what should you include?", ["The LASSO formula in detail", "The finding in everyday language + its limits (not causal, unstable) + a testable suggestion for action", "All 52 edges", "Just the conclusion"], 1,
 ["They do not need the formula; they need the finding and its limits.", "Correct.", "Information overload; cover only the most important overall pattern.", "With only the conclusion, listeners easily take the predictive relationship as causal; the limits must come with it."]),
("A results section says: \"The full procedure confirmed the predictive role of Feeling left out → No one understands me.\" What is wrong?", ["Nothing", "A sensitivity analysis only shows that a result does not depend on the estimation method; it cannot \"confirm\" an edge. Write \"both analyses retained this edge\"", "It should say \"the full procedure proved causation\"", "The sentence should be deleted; sensitivity analyses are not reported in the results"], 1,
 ["\"Confirmed\" goes too far.", "Correct.", "The full procedure also gives only predictive relationships.", "The required sensitivity analysis must be reported in the results."]),
("Which of these numbers can come only from the full procedure, not from the LASSO-only main analysis?", ["The bootstrap interval of an edge", "The p-value and standard error of an edge", "The CS-coefficient of out-EI", "The number of nonzero cross-lagged edges"], 1,
 ["Bootstrap intervals come from the main analysis (the bootstrap of Lesson 10.2).", "Correct: LASSO gives no p-values or standard errors.", "The CS-coefficient comes from the case-dropping of the main analysis.", "Each analysis has its own edge count; say which one it comes from."]),
("What does a density of 52/72 ≈ 0.72 suggest?", ["The network is very sparse", "The network is very dense; lambda.min may have kept some false-positive edges", "The relationship between loneliness and depression is very strong", "The network was estimated wrongly"], 1,
 ["Quite the opposite: 52 of the 72 possible positions are nonzero.", "Correct.", "Plausible but wrong: density only counts nonzero edges and says nothing about their strength; many of the edges lambda.min keeps are very weak.", "There is no evidence of an error; high density is typical of lambda.min (Lesson 7.2)."]),
],
ex=[
("Generate and rewrite the results draft", "Writing", r"""<p>Run R/L10-3.R to get the automatic draft; then fill in a full version with the template on this page, compare the two, and write a results section of 500–700 words; add the methods (data analysis) you wrote in Lesson 9.3, for 800–1,200 words in total.</p>""",
 r"""<p>Checks: (1) every number matches the output; (2) the out-EI ranking is marked "not sufficiently stable, not interpreted"; (3) no causal verbs; (4) figure and table numbers match the text; (5) the settings in the methods (λ rule, seed, number of bootstrap replicates) match L10-2.R; (6) the full procedure has its own paragraph covering all five things (settings, model choice, edges kept, agreement with the main analysis, construct level), with settings matching L10-2b.R.</p>"""),
("Write the discussion paragraph on the two analyses", "Writing", r"""<p>Following the table "Writing the discussion" on this page, write a 200–300-word discussion paragraph for your project: which edges both analyses kept, which appeared in only one, whether the construct-level direction agrees, and what these results mean for your research question.</p>""",
 r"""<p>Self-check: (1) the main findings come only from edges kept by both analyses; (2) edges found only in the main analysis are described as "sensitive to the estimation method", with a reason where possible (e.g., they appear in only one interval of data); (3) effect sizes cite the unpenalized estimates, with their source stated; (4) no words such as "confirmed" or "proved"; (5) the last sentence returns to the research question. You can compare it with the example paragraph for the course data on this page.</p>"""),
("Write a limitations paragraph", "Writing", r"""<p>Following the five aspects in the table on this page, write a 200–300-word discussion of limitations.</p>""",
 r"""<p>Reference: "First, this study used an observed-score CLPN, so the cross-lagged edges may reflect both stable between-person differences and within-person dynamic change … Second, the edges represent only predictive relationships over time … Third, each node was measured by a single item, and a 6-month interval is not necessarily the best time scale for these processes … Finally, the sample was …, so generalization requires caution."</p>"""),
("A 10-minute talk", "Synthesis", r"""<p>Make 8–10 slides following the talk checklist on this page, rehearse once with a timer, and prepare answers to the four questions.</p>""",
 r"""<p>Self-assessment points: one point per slide; the network plot has item-name labels; "stability and sensitivity" gets its own slide; it ends with a testable practice suggestion and a design for the next study.</p>"""),
],
summary=["Let the code fill in the numbers (L10-3.R): every number can be found in the output.", "Results: structure → centrality → accuracy and stability → sensitivity; state, do not interpret.", "Full-procedure sensitivity analysis: the methods describe the settings of both analyses and the interpretation rule; the results give it its own paragraph; in the discussion the main findings are only the edges kept by both analyses.",
"Limitations: mixing of between-/within-person effects, not causal, measurement and interval, estimation method, sample and attrition.", "Practice wording: finding in everyday language + limits + a testable suggestion for action; in a 10-minute talk, one point per slide."],
refs=["Wysocki, A., McCarthy", "Epskamp, S., Borsboom, D., & Fried", "Burger, J., Isvoranu"],
)
