# -*- coding: utf-8 -*-
# Writing workshop materials/writing.html. exec'd by src/build_materials.py after the assessment pages (page, sec, L, _qz, _RVG available).
# All examples use results from the course's simulated data; numbers in the results example are {{V:key}}, read from R/output/, never copied by hand.
def _A(*parts):
    """Sentence-by-sentence notes: parts are (sentence, note) tuples or plain text; clicking a sentence with a dashed underline shows below it why it is written that way."""
    out = "".join(f'<span data-tip="{E(t)}">{s}</span>' if t else s for s, t in (p if isinstance(p, tuple) else (p, "") for p in parts))
    return f'<p class="annot">{out}</p>'
def _BEFORE(t): return f'<div class="box warnbox"><b class="bt">Before</b><p>{t}</p></div>'
def _TASK(n, q, ans, rub):
    rows = "".join(f"<tr><td>{lv}</td><td>{d}</td></tr>" for lv, d in rub)
    return (f'<div class="exitem"><h4>Rewriting task {n}</h4>{q}<details class="faq"><summary>Model answer and rubric</summary>{ans}'
            f'<div class="tablewrap"><table><tr><th>Level</th><th>Criteria</th></tr>{rows}</table></div></details></div>')
_R3 = lambda a, b, c: [(3, a), (2, b), (1, c), (0, "No answer, or the rewrite still has the main problems of the original")]

wbody = sec("how", "How to use this page", """
<p>This page links <a href="../lessons/L9-3.html">9.3 Reporting standards</a> and <a href="../lessons/L10-3.html">10.3 Writing the results</a>. The four parts of a paper that most often go wrong are data and measures, statistical analysis, results, and limitations. For each one you get a "before" and an "after" example:</p>
<ol><li>Read the "before" version first and find the problems yourself.</li><li>Then read the "after" version and <b>click the sentences with a dashed underline</b> to see why they are written that way.</li><li>Answer a short question, then do the rewriting task (the model answer and a 0–3 rubric are folded away below it).</li></ol>
<p>All examples use the course's simulated data. The numbers in the results example are read automatically from <code>R/output/</code>, so they match what you get when you run the course scripts. When you have finished writing, go through <a href="cheatsheets.html#report">Cheat Sheet 4 · Reporting checklist</a> item by item.</p>""")

wbody += sec("ex1", "Example 1: Data and measures", _BEFORE("We collected data from 800 people and measured loneliness and depression. The data quality was very good, with no problems.") + "<h3>After</h3>" + _A(
 ("This study used the simulated panel data provided with the course (N = 800 community adults aged 18–85), with 3 waves 6 months apart.", "State the sample size, where the sample comes from, the number of waves and the interval. The interval decides how fast a process you can see (4.1, 5.4). If the data are simulated, say so."),
 ("Loneliness was measured with 4 items (modeled on the UCLA Loneliness Scale, scored 1–4) and depression with 5 items (modeled on the PHQ-9, scored 0–3); each item is one node in the network.", "In a CLPN the nodes are items, so say how many items each construct has and how they are scored, and ideally list the item wording in a table or appendix (9.3)."),
 ("There were no missing data; a real study should report the number of people who completed each wave, the attrition rate, and how those who stayed and those who dropped out compare on the main wave-1 variables.", "\"The data quality was very good\" says nothing. Use numbers to describe missing data and attrition, and say how you handled them (4.3)."),
) + _qz.quiz("""Q: The "before" paragraph leaves out one design detail that a CLPN must report: how much time passed between two measurements. What does the course call this? (1–2 words)
T: lag||time interval||interval||lag interval||measurement interval
H: In English it is called the lag or time interval.
E: The time interval (lag) affects which effects you can see; see <a href="../lessons/L4-1.html">4.1</a> and <a href="../lessons/L5-4.html">5.4</a>.""") + _TASK(1,
 "<p>Rewrite this sentence so that others can check it (2–3 sentences): \"We ran several surveys in a community using a common depression scale.\"</p>",
 "<p>Example: \"We recruited residents aged 60 and over from 3 communities in one city (N = 412) and surveyed them in 3 waves, in March 2025, September 2025 and March 2026 (6 months apart). Depressive symptoms were measured with the first 8 items of the PHQ-9 (scored 0–3) … 78% completed wave 3; those who dropped out had slightly higher wave-1 loneliness scores (see Table S1).\" (Fill in the numbers from your own study.)</p>",
 _R3("States the sample, recruitment, number of waves and interval, scale name and scoring, and attrition", "One or two of these are missing", "Still vague; only one item added")))

wbody += sec("ex2", "Example 2: Statistical analysis", _BEFORE("We used network analysis to study the relationship between loneliness and depression, estimated the network with LASSO, and tested its stability.") + "<h3>After</h3>" + _A(
 ("We estimated a cross-lagged panel network (CLPN): for each T2 item we ran a separate LASSO regression with all 9 T1 items as predictors (Wysocki et al., 2025).", "Name the model, describe the nodewise regression and give the reference. This tells readers that the edges are directed regression coefficients (7.1)."),
 ("All items were z-standardized before the analysis; λ was chosen by 10-fold cross-validation (lambda.min), with random seed 2026; a sensitivity analysis used lambda.1se instead and added gender and age (unpenalized) as covariates.", "The λ rule, the number of folds, the seed and whether covariates are penalized each change the results, so all of them must be stated (7.2, 7.5)."),
 ("Edge accuracy was assessed with 1000 nonparametric bootstrap resamples, and the stability of out- and in-expected influence with the case-dropping bootstrap and the CS-coefficient (Epskamp et al., 2018).", "\"Tested its stability\" is too vague: give the type of bootstrap, the number of resamples and the index used to judge (8.2, 8.3)."),
 ("The analysis was run in R (versions in the supplementary material) with glmnet and bootnet; the code is on OSF.", "Software versions and shared code let others reproduce the analysis (9.3)."),
) + _qz.quiz("""Q: The "before" version only says "estimated the network with LASSO" and does not say how λ was chosen. What is the rule the course's main analysis uses when choosing λ by cross-validation? (Give its name in R.)
T: lambda.min||lambdamin||lambda.min rule
H: The other, more conservative rule is called lambda.1se.
E: The difference between the two rules is explained in <a href="../lessons/L7-2.html">7.2</a>. The methods section must say which one you used, and what the sensitivity analysis used.""") + _TASK(2,
 "<p>Write a statistical analysis paragraph for your capstone project (4–6 sentences) that covers at least: the model, the λ rule and number of folds, the random seed, covariates, accuracy and stability checks, and software.</p>",
 '<p>Use the "after" version above as a model, then check each point against the <a href="cheatsheets.html#report">reporting checklist</a>.</p>',
 _R3("All six points covered, and specific (with numbers and names)", "One or two points missing, or one is vague", "Only the model name")))

wbody += sec("ex3", "Example 3: Results", _BEFORE("The results show that loneliness caused depression. \"No one understands me\" is the core symptom, because its centrality is the highest. All edges were very stable.") + "<h3>After</h3>" + _A(
 ("In the loneliness → depression direction, the strongest cross-lagged edge was T1 \"{{V:fx_ld_from_zh}}\" → T2 \"{{V:fx_ld_to_zh}}\" (B = {{V:b8_lone4>dep4_sample}}, bootstrap interval [{{V:b8_lone4>dep4_q2.5}}, {{V:b8_lone4>dep4_q97.5}}]).", "Give the direction first (which T1 item → which T2 item), then the number and interval. The numbers come from the output of R/L8-2.R."),
 ("That is, controlling for all T1 items, participants who more often felt \"{{V:fx_ld_from_zh}}\" at wave 1 tended to report more \"{{V:fx_ld_to_zh}}\" six months later.", "Use \"predicted\" and \"tended to\", not \"caused\" or \"made\". This is a predictive relationship over time (5.4, 7.3)."),
 ("\"{{V:fx_out_top_zh}}\" had the highest out-expected influence ({{V:fx_out_top_v}}), but out-EI was not stable enough (CS = {{V:cs8_out}}, {{V:cs8_out_short}}), so its ranking is not interpreted; for in-EI, CS = {{V:cs8_in}} ({{V:cs8_in_short}}).", "Always report centrality together with its stability. If CS is below 0.25, don't interpret the ranking, let alone call a node the \"core symptom\" (8.3, 9.2)."),
 ("Pairwise difference tests among the 10 strongest cross-lagged edges: {{V:b8_diff_text}}; so the ranking of the strong edges should also be read with caution.", "\"All edges were very stable\" is a claim without evidence; report the difference tests as they are (8.2)."),
) + _qz.quiz("""Q: Which word in the first sentence of the "before" version is causal language? (Give the word as it appears in the text.)
T: caused||cause||causes
H: A CLPN can only say "predict".
E: "Cause", "lead to", "drive" and "make" are all causal language; see <a href="../lessons/L5-4.html">5.4</a> and <a href="../lessons/L7-3.html">7.3</a>.""") + _TASK(3,
 "<p>Rewrite this sentence as a careful statement of results (1–2 sentences): \"Fatigue has the highest in-expected influence, which shows that fatigue is the end result caused by loneliness.\"</p>",
 "<p>Example: \"'Fatigue' had the highest in-expected influence (in-EI = {{V:fx_in_top_v}}, CS = {{V:cs8_in}}), meaning it was the item best predicted by the other T1 items; this is a predictive relationship over time and does not show that fatigue is 'caused' by loneliness.\"</p>",
 _R3("Gives the number and its stability, says \"predicted\" rather than \"caused\", and makes no causal or individual-level claim", "Causal language removed, but the number or the stability is missing", "Still makes a causal claim")))

wbody += sec("ex4", "Example 4: Limitations", _BEFORE("This study proved a causal relationship between loneliness and depression. Its only limitation is that the sample was not large enough.") + "<h3>After</h3>" + _A(
 ("First, a standard CLPN does not separate between-person and within-person effects; the cross-lagged edges may partly reflect stable differences between people rather than processes of change within a person (Hamaker et al., 2015).", "This is the most important limitation of the CLPN, and almost every paper needs it (5.3, 7.5)."),
 ("Second, the results show only predictive relationships over time; unmeasured confounders (such as financial strain in the household) may affect both loneliness and depression.", "Replace \"causal\" with specific threats: confounding, the interval, measurement error (5.4)."),
 ("Third, an interval of 6 months may miss faster processes of change; we did not test measurement invariance, so whether the items meant the same thing at every wave remains to be confirmed.", "The interval and measurement invariance are concrete limitations that can be tested (4.1, 7.6)."),
 ("Fourth, out-EI was not stable enough, and conclusions based on it need to be replicated in a larger sample.", "A limitation should match your results, not just say vaguely that \"the sample was not large enough\" (8.3)."),
) + _qz.quiz("""Q: Which word in the first sentence of the "before" version states the conclusion too strongly? (Give the word as it appears in the text.)
T: proved||prove||proves
H: An observational study can rarely "____" anything.
E: Use "suggests" or "is consistent with" instead of "proved"; see <a href="../lessons/L10-3.html">10.3</a>.""") + _TASK(4,
 "<p>Write 3 limitations for your capstone project (1–2 sentences each), covering at least two of the three types (within- vs. between-person, causality, measurement), each tied to your actual results.</p>",
 "<p>Use the \"after\" version above as a model. For each limitation, say what the problem is → how it might affect your conclusions → how future work could do better.</p>",
 _R3("All 3 are specific, tied to the results, and cover at least two types", "Three limitations, but one is generic", "Only one or two, and very general")))

wbody += sec("check", "After writing", """<ul><li>Go through <a href="cheatsheets.html#report">Cheat Sheet 4 · Reporting checklist</a> item by item.</li>
<li>Search the whole text for "cause", "lead to", "prove", "core symptom" and "drive", and fix each one.</li>
<li>Every number should trace back to a file in <code>R/output/</code> (this is how the results draft in Lesson 10.3 is generated automatically).</li>
<li>Reporting standards for network analysis: Burger et al. (2023), <a href="https://doi.org/10.1037/met0000471">doi.org/10.1037/met0000471</a>. More literature in the <a href="reading.html">reading pack</a>.</li></ul>""")
page("writing.html", "Writing Workshop: Methods, Results and Limitations", "<p>Four \"before → after\" examples; click a sentence to see why it is written that way. Each example ends with a short question and a rewriting task. Links Lesson 9.3 (reporting standards) and Lesson 10.3 (writing the results).</p>", _RVG["fillV"](wbody).replace("< ", "&lt; "))   # cs_short text contains "< 0.25"; escape it for HTML
