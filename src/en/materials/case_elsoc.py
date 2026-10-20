# -*- coding: utf-8 -*-
# Real-data case materials/case_elsoc.html. exec'd by src/en/build_materials.py after the writing workshop
# (page, sec, L, E, _qz, _RVG available). Run results in the text are {{V:key}} or the tables in _RVG;
# src/en/common/rvals.py reads the keys from R/output/data_elsoc_log.txt and case_elsoc_*.csv. Never copy numbers by hand.
RV, fillV = _RVG["RV"], _RVG["fillV"]
def fill_all(s):
    """f-strings collapse {{V:key}} into {V:key}; replace both forms with numbers from the log."""
    s = fillV(s)
    def rep(m):
        k = m.group(1)
        if k not in RV:
            raise KeyError("The text refers to an R result key that does not exist: " + k)
        return RV[k]
    return re.sub(r"(?<!\{)\{V:([^}]+)\}(?!\})", rep, s)
def _tbl(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)   # Headers may contain unreplaced {{V:key}}
    body = "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def Q(src):
    return _qz.quiz(fill_all(src))   # numeric answers also come from the log: fill them in before rendering the quiz

_y1, _y2, _y3 = "{{V:el_y1}}", "{{V:el_y2}}", "{{V:el_y3}}"
desc = _tbl(["Item", "Label", f"{_y1} mean", f"{_y1} SD", f"{_y2} mean", f"{_y3} mean"], _RVG["EL_DESC"])
ar = _tbl(["Item", "Label", "Autoregressive B"], [(a, b, c) for a, b, c in _RVG["EL_AR"]])
top = _tbl(["From (T)", "Label", "To (T+1)", "Label", "Sample B", "2.5%", "97.5%", "Proportion shrunk to 0"],
           [r for r in _RVG["EL_TOP"]])
ei = _tbl(["Node", "Label", "Out-expected influence", "In-expected influence"], _RVG["EL_EI"])

body = sec("what", "What this page is", f"""
<p>The network analyses in the lessons all use simulated data, because only simulated data have a known "true structure" to compare against. This page runs <b>the same workflow</b> on a public, real longitudinal panel: the 8 depressive symptom items of the Chilean Longitudinal Social Study (ELSOC), predicting {_y2} from {_y1}. The method is the course's main-line "LASSO-only" CLPN ({L("7.1", "7.1")}–{L("7.4", "7.4")}), plus an edge-weight bootstrap with 200 resamples ({L("8.2", "8.2")}).</p>
<p>Read it after Lessons 7.4 and 8.2. It is not a new method but a comparison: real data have no "answer key", so all you can say is what the data support and what they don't.</p>
<div class="box key"><b class="bt">Where the numbers come from</b><p>Every count, coefficient and interval below is read from <code>R/output/data_elsoc_log.txt</code> and <code>case_elsoc_*.csv</code> when the site is built; the scripts are <code>R/data_elsoc.R</code> and <code>R/case_elsoc.R</code> (seed 2026). Don't copy these numbers into your own paper: with your sample and your seed, the numbers will be different.</p></div>""")

body += sec("data", "The data", f"""
<p>Source: Reproducible Research, Centre for Social Conflict and Cohesion Studies COES (2022). <i>Estudio Longitudinal Social de Chile 2016-2021</i>. Harvard Dataverse, {{V:el_version}}. <a href="https://doi.org/{{V:el_doi}}">https://doi.org/{{V:el_doi}}</a>, UNF:6:z/vWFguq9fg03YaOLWFddA== [fileUNF]. The Dataverse page marks this version as CC0 1.0, so it may be redistributed.</p>
<p>The course comes with two files, both in the repository and in <code>clpn-course.zip</code>: the original file <code>data/elsoc/{{V:el_file}}</code> (byte-identical to V1 on Dataverse, MD5 <code>{{V:el_md5}}</code>), and the analysis file <code>data/elsoc_phq8_wide.csv</code> that <code>R/data_elsoc.R</code> writes from it (original sample, PHQ-8 at three waves plus gender and age, 27 columns). For the case you only need:</p>
<div class="codeblk"><pre><code class="language-r">source("R/case_elsoc.R")   # CLPN and {{V:el_boot_n}} bootstrap resamples, about 1–2 minutes</code></pre></div>
<p>To check the preprocessing, run <code>source("R/data_elsoc.R")</code>: it reads the bundled original file (and downloads it from Dataverse only if it is missing) and writes the analysis file again; the result should be the same as the file that comes with the course. No internet connection is needed.</p>
<h3>What the preprocessing does</h3>
<ul>
<li>Only the original sample recruited in 2016 is used, not the refresher sample that joined in {{V:el_sup_when}} (it has no data for the first two waves).</li>
<li>Negative values are missing-data codes (−999 / −888 / −777 / −666) and are all set to NA. The original IDs are not kept.</li>
<li>Only the first 8 PHQ items are kept, at three waves ({{V:el_y1}}, {{V:el_y2}}, {{V:el_y3}}).</li>
</ul>
<div class="box warnbox"><b class="bt">Why item 9 is left out</b><p>Item 9 asks about thoughts of death or of hurting yourself. It is a high-risk item that calls for clinical follow-up and should not be treated as an ordinary node in a teaching exercise. The PHQ-8, widely used in research, is exactly the version without this item. The script does not export item 9; please don't add it back yourself just to "get 9 nodes".</p></div>
<p>Two more things you need to know before reading the results:</p>
<ul>
<li><b>The scoring is not the clinical 0–3.</b> In ELSOC these 8 items are scored 1 = never … 5 = every day. The sum of the 8 items runs from 8 to 40, not the usual PHQ-8 range of 0–24. <b>Don't interpret the totals here with clinical cut-offs such as 10 or 20.</b></li>
<li><b>The item numbers do not quite match the standard PHQ-9.</b> ELSOC swaps item 6 (feeling bad about yourself) and item 7 (trouble concentrating) of the standard questionnaire. The labels in the tables below follow the actual item wording, not the standard numbering: the node called phq6 is about concentration, not "feeling bad about yourself".</li>
</ul>""")

body += sec("sample", "Who is in the analysis", f"""
<p>The original file has {{V:el_n_raw}} rows × {{V:el_n_col}} columns. The original sample has {{V:el_n_orig}} people, the refresher sample {{V:el_n_sup}} (not used). In the original sample, the number who answered all 8 PHQ-8 items was:</p>
<div class="tablewrap"><table><thead><tr><th>Wave</th><th>Year</th><th>Answered all 8 items in this wave</th></tr></thead><tbody>
<tr><td>1</td><td>{{V:el_y1}}</td><td>{{V:el_n_w1}}</td></tr>
<tr><td>2</td><td>{{V:el_y2}}</td><td>{{V:el_n_w2}}</td></tr>
<tr><td>3</td><td>{{V:el_y3}}</td><td>{{V:el_n_w3}}</td></tr>
</tbody></table></div>
<p>{{V:el_n_w12}} people are complete at waves 1–2, and <b>{{V:el_n}}</b> at all of waves 1–3. The case's CLPN uses only these {{V:el_n}} people (complete cases, not multiple imputation). Of them, {{V:el_n_f}} are women ({{V:el_pct_f}}%); their mean age in {{V:el_age_y}} was {{V:el_age_m}} (SD {{V:el_age_sd}}, range {{V:el_age_lo}}–{{V:el_age_hi}}).</p>
<p>Going from {{V:el_n_orig}} people in the original sample to {{V:el_n}} complete at all three waves, the people who were lost may not be like those who stayed ({L("4.3", "4.3")}). This page does not compare them. In a paper you must add this: whether those who stayed differed in wave-1 symptoms from those who did not complete all three waves.</p>""")

body += sec("desc", "How common are the symptoms?", f"""
<p>Below are the item means (1–5) for the {{V:el_n}} people complete at all three waves. Fatigue is highest and feeling bad about yourself lowest; over the three years the means moved only a little.</p>
{desc}
<p>Sum of the 8 items (range 8–40): mean {{V:el_tot_m1}} in {{V:el_tot_y1}}, {{V:el_tot_m2}} in {{V:el_tot_y2}}, {{V:el_tot_m3}} in {{V:el_tot_y3}}. The totals of {{V:el_tot_y1}} and {{V:el_tot_y2}} correlate r = {{V:el_tot_r}}. Over an interval of about a year, the total is only moderately stable, and an item-level network asks exactly this: between which items does that stability lie?</p>""")

body += sec("model", "Which model is estimated", f"""
<p>The same as the main analysis of {L("7.2", "7.2")}, not the full procedure of Lesson 7.5 (no SEM re-estimation, no equality constraints across time):</p>
<ul>
<li>One LASSO regression for each {{V:el_y2}} item, with all 8 {{V:el_y1}} items as predictors (the nodewise regression of {L("7.1", "7.1")}).</li>
<li>Before the regressions, <code>clpn_estimate()</code> z-standardizes the items. The B values below are in <b>standard deviation units</b>: 0.10 means "1 SD higher on this item at T, 0.10 SD higher predicted value on that item at T+1", not 0.10 raw score points.</li>
<li>λ is chosen as <code>lambda.min</code> by 10-fold cross-validation, with <code>set.seed(2026)</code>. This is the course default, and also the rule with more false positives ({L("7.2", "7.2")}, {L("7.5", "7.5")}).</li>
<li>There are {{V:el_n_cell}} cross-lagged positions (8 × 7). The autoregressive edges are counted separately and not drawn in the plot.</li>
</ul>""")

if RV["el_top1_b"] == RV["el_top2_b"]:
    _top = 'The two strongest edges, tied, are "{V:el_top1_from_zh}" → "{V:el_top1_to_zh}" and "{V:el_top2_from_zh}" → "{V:el_top2_to_zh}", both with a sample estimate of {V:el_top1_b}. '
else:
    _top = 'The strongest edge is "{V:el_top1_from_zh}" → "{V:el_top1_to_zh}" ({V:el_top1_b}), followed by "{V:el_top2_from_zh}" → "{V:el_top2_to_zh}" ({V:el_top2_b}). '
_neg_clause = " (no negative edges this time: the nonzero edges are all positive, and the rest were shrunk to 0)" if RV["el_n_neg"] == "0" else ""
_fig_neg = "There are no negative cross-lagged edges this time, so the plot is all blue." if RV["el_n_neg"] == "0" else "Red edges are negative."
body += sec("edges", RV["el_y1"] + " → " + RV["el_y2"] + " edges", f"""
<p><b>{{V:el_n_cl}} / {{V:el_n_cell}}</b> cross-lagged edges are nonzero, {{V:el_n_neg}} of them negative{_neg_clause}. The largest |B| = {{V:el_max_b}}. There are many edges, and they are small: <code>lambda.min</code> still keeps many small edges in this large sample, in line with Lesson 7.5: the false positives of cross-validation do not go away as N grows.</p>
<p>{_top}Read it as in {L("7.3", "7.3")}: among people with the same other symptoms in {{V:el_y1}} (including "{{V:el_top1_to_zh}}" itself), those 1 SD higher on "{{V:el_top1_from_zh}}" that year have a predicted "{{V:el_top1_to_zh}}" about {{V:el_top1_b}} SD higher the next year. <b>This is prediction, not "{{V:el_top1_from_zh}} caused {{V:el_top1_to_zh}}".</b></p>
{top}
<p class="muted">The table shows the {{V:el_top_n}} edges with the largest absolute sample estimates. The intervals are the 2.5% and 97.5% quantiles of {{V:el_boot_n}} resamples of people; the last column is the proportion of those {{V:el_boot_n}} resamples in which LASSO shrank the coefficient to 0. Don't use {{V:el_boot_n}} resamples in a formal report; see the bootstrap section below.</p>
<figure><img src="../R/output/case_elsoc_clpn.png" alt="Cross-lagged network of the ELSOC PHQ-8 items; blue arrows are positive predictions" loading="lazy"><figcaption>Figure: <code>R/output/case_elsoc_clpn.png</code>. Only cross-lagged edges are drawn, no autoregressive edges. Colorblind theme, as everywhere in the course: blue = positive, red = negative. {_fig_neg}</figcaption></figure>
<h3>Autoregressive edges: which item is most "stable"?</h3>
<p>The diagonal is "this item this year predicts the same item next year" (controlling for the other 7 items). The highest is "{{V:el_ar_hi_zh}}" ({{V:el_ar_hi}}), the lowest "{{V:el_ar_lo_zh}}" ({{V:el_ar_lo}}). The lowest one has almost no autoregression of its own: its level next year is predicted more by the other symptoms (you will see this again in the in-expected influence below).</p>
{ar}""")

body += sec("ei", "Out- and in-expected influence", f"""
<p>Only cross-lagged edges are summed, without autoregression (as in {L("7.4", "7.4")}). The highest out-expected influence belongs to "{{V:el_out_top_zh}}" ({{V:el_out_top_v}}), the highest in-expected influence to "{{V:el_in_top_zh}}" ({{V:el_in_top_v}}). <b>The node that best predicts the others and the node most easily predicted by the others are not the same.</b></p>
{ei}
<div class="box warnbox"><b class="bt">Don't use this to decide what to target first</b><p>This case does <b>not</b> run the case-dropping bootstrap and has <b>no</b> CS-coefficient ({L("8.3", "8.3")}). The table is only the weighted out-degree and in-degree in this one sample. You cannot say "depressed mood is the core symptom", nor "depressed mood should be targeted first". Even once stability has been checked, ranking first only means a stronger predictive relationship; whether an intervention works needs separate research ({L("9.2", "9.2")}, {L("10.1", "10.1")}).</p></div>""")

body += sec("again", "Another interval, and two covariates", f"""
<h3>Doing it again with {{V:el_rep_y1}} → {{V:el_rep_y2}}</h3>
<p>Same people, same settings. {{V:el_n_cl_rep}} / {{V:el_rep_den}} cross-lagged edges are nonzero. Across all {{V:el_rep_den}} cross-lagged positions (including those shrunk to 0), the correlation with {{V:el_y1}} → {{V:el_y2}} is r = {{V:el_rep_r}}. Of the 8 strongest edges in the sample, {{V:el_rep_same}} are still nonzero with the same sign in the next interval.</p>
<p>r = {{V:el_rep_r}} is moderate; it does not mean "the structure replicated". A year later, part of the broad direction is still there, but many of the individual edges have changed. In your write-up, report this correlation and these {{V:el_rep_same}} edges; don't write "the results were consistent across the two intervals".</p>
<h3>Adding gender and age (unpenalized)</h3>
<p>In the {{V:el_n_sens}} people complete at all three waves and also not missing gender or age, these two go into every regression as covariates with <code>penalty.factor = 0</code> (not shrunk; their coefficients are not drawn in the network). {{V:el_n_cl_sens}} / {{V:el_sens_den}} cross-lagged edges are nonzero, and across all cross-lagged positions they correlate r = {{V:el_r_sens}} with the main analysis.</p>
<p>The <b>pattern</b> of edges hardly changes. This only shows that "in this sample, the predictive relationships between items remain after controlling for gender and age"; it does not show that all confounding is controlled ({L("5.4", "5.4")}). Things that were not measured (income, physical illness, social support) can still push up both this year's fatigue and next year's change in appetite.</p>""")

body += sec("boot", "What the 200 bootstrap resamples show, and what they don't", f"""
<p>Step 6 is a nonparametric bootstrap: draw {{V:el_n}} people with replacement, {{V:el_boot_n}} times, and redo the LASSO with 10-fold CV each time. This is the idea of {L("8.2", "8.2")}, but <b>written by hand and with only {{V:el_boot_n}} resamples</b>, not the 1000 bootnet resamples of the course's main analysis. Changing <code>B_BOOT</code> to 1000 in the script takes a few more minutes; for a paper, use at least 1000.</p>
<p>Of the {{V:el_top_n}} strongest edges, {{V:el_top_excl0}} have an interval that excludes 0. Before you read anything into that, remember three limits:</p>
<ol>
<li>These {{V:el_top_n}} edges were <b>picked after looking at the sample estimates</b>, not registered as hypotheses before the analysis. Picking them first and then reporting "{{V:el_top_excl0}} / {{V:el_top_n}} exclude 0" makes them look "all significant" more easily than naming one edge in advance would.</li>
<li>With {{V:el_boot_n}} resamples, numbers such as the "proportion shrunk to 0" can only change in steps of 1/{{V:el_boot_n}}. That is the <b>resolution</b>, not the precision. Precision depends on Monte Carlo error: estimating a proportion whose true value is p from B resamples has a standard error of about √(p(1 − p) / B), which for B = 200 and p = 0.05 is about 0.015, three times the resolution of 0.005. The interval ends are just as unstable: with 200 resamples, the 2.5% and 97.5% quantiles each rest on only the outermost 5 or so resamples, and another seed may move them noticeably. There is also no correction for multiple comparisons across the {{V:el_n_cell}} edges (for how a correction pushes p-values up, see {L("7.7", "7.7")}).</li>
<li>An interval that excludes 0 only means "resampling did not easily remove this predictive coefficient". It is still not causation, and it is not a CS-coefficient.</li>
</ol>""")

body += sec("limits", "Limitations to state at minimum in a report", """
<ul>
<li><b>A standard CLPN mixes between-person and within-person effects</b> (""" + L("5.3", "5.3") + """, """ + L("7.5", "7.5") + """). Part of an edge may only mean "people who are more depressed in the long run score higher on every item", not "this person's mood was lower than usual this year, so their interest is worse next year".</li>
<li><b>Complete cases.</b> People who answered all three waves may differ from those with missing waves; this page does not compare them.</li>
<li><b>Only <code>lambda.min</code></b>, no SEM re-estimation. There will be false positives among the {{V:el_n_cl}} nonzero edges.</li>
<li><b>Measurement invariance was not tested</b> (""" + L("7.6", "7.6") + """ shows how with the course's simulated data and the coaches data; this case does not test it for ELSOC). You cannot assume that "fatigue" in 2016 and "fatigue" in 2018 are measured with the same ruler.</li>
<li><b>An interval of about one year</b>, so ups and downs within a few weeks are invisible. The items are 1–5 frequency ratings, so the totals cannot be compared with clinical cut-offs.</li>
<li><b>A community sample from one country and one period.</b> You cannot write "this is how depressive symptoms generally predict each other".</li>
</ul>
<p>Sentence patterns you can borrow are in the "Results" and "Limitations" examples of the <a href="writing.html">writing workshop</a>. To see how others write up real data, read Funkhouser et al. (2021) and Grygiel et al. (2026) in the <a href="reading.html">reading pack</a>.</p>""")

body += sec("quiz", "Check your understanding", Q("""Q: Why does this case not use item 9 of the PHQ?
- Item 9 has too much missing data, and putting it in the network would make LASSO fail || The script leaves it out because of its content, not its missing rate.
+ Item 9 asks about thoughts of death or of hurting yourself and is not suitable as an ordinary node in teaching; the PHQ-8 itself does not include it || Right. The analysis file does not contain it either; please don't add it back from the original data.
- Item 9 is reverse-scored, so its sign would flip after standardizing || The case says nothing about reverse scoring.
- 9 nodes are too many; only 8 can be computed || The course's simulated data have 9 nodes.
H: It has to do with clinical risk, not sample size.
E: See "The data" on this page. The PHQ-8 used widely in research is exactly the version without this item.""") + Q("""Q: For "Depressed mood → Little interest" with B = {{V:el_top1_b}}, which of these can you say?
- Depressed mood caused the loss of interest the following year || "Caused" is causal language. A CLPN does not rule out unmeasured confounding, nor does it separate between-person and within-person effects.
- Little interest is the symptom to target first, because its in-expected influence is the highest || High in-expected influence only means "easily predicted by the other items". This page has no CS-coefficient, and an intervention target cannot be inferred from centrality anyway.
+ Controlling for the other symptoms in the first year, people with higher depressed mood in the first year have a slightly higher predicted little interest the next year; this is a predictive relationship || Right. Also give the interval, the standardized units, and the fact that this is not causal.
- Because the bootstrap interval excludes 0, this edge is certainly not 0 in the population || With {{V:el_boot_n}} resamples and an edge picked after the fact, you cannot say "certainly".
H: The verb the course allows is "predict", not "cause" or "should be targeted".
E: See """ + L("5.4", "5.4") + """, """ + L("7.3", "7.3") + """, and """ + L("9.2", "9.2") + """.""") + Q(f"""Q: How many people answered the PHQ-8 at all three waves and entered this CLPN? (Enter a whole number)
N: {{{{V:el_n}}}} | 0
H: Not the number of rows in the original file, and not the size of the original sample.
E: {{V:el_n}} people. The original sample has {{V:el_n_orig}}; only those complete at all three waves enter the network. See "Who is in the analysis".""") + Q(f"""Q: How many nonzero cross-lagged edges does {{V:el_y1}} → {{V:el_y2}} have? (Enter a whole number)
N: {{{{V:el_n_cl}}}} | 0
H: Out of {{V:el_n_cell}} cross-lagged positions. Autoregressive edges are not counted.
E: {{V:el_n_cl}}, of which {{V:el_n_neg}} are negative. That there are many small edges has to do with the false positives of lambda.min; see """ + L("7.5", "7.5") + """."""))

body += sec("do", "When you run it yourself", """
<ol>
<li>Open the project with <code>clpn-course.Rproj</code> and run <code>source("R/case_elsoc.R")</code>.</li>
<li>Compare <code>R/output/case_elsoc_log.txt</code> with this page. With the same R, the same packages and seed 2026, the coefficients should match this page; if you change <code>B_BOOT</code> or the R version, the intervals may differ slightly.</li>
<li>If you write anything with these data, cite ELSOC in the format given under "The data" above.</li>
</ol>
<p>Variable meanings, license and citation format are also in the last section of the <a href="../data/data_dictionary.html">data dictionary</a>.</p>""")

page("case_elsoc.html", "Real-Data Case: An ELSOC Depressive Symptom Network",
     fill_all("<p>The course's main-line &ldquo;LASSO-only&rdquo; CLPN on public longitudinal data on depressive symptoms from ELSOC. The analysis file comes with the course; run <code>R/case_elsoc.R</code> to reproduce the results on this page.</p>"),
     fill_all(body))
