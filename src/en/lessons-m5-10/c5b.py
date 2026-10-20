# -*- coding: utf-8 -*-
L["5.3"] = dict(
lead=r"""<p>This lesson separates between-person questions from within-person questions and introduces the RI-CLPM, which can tell the two apart. The limitations section of a CLPN paper has to discuss this point, and reviewers often ask: "Are your results between-person or within-person?"</p>""",
intuition=r"""
<h3>Two questions that sound alike but are completely different</h3>
<ul><li><b>Between-person question:</b> "Are people who are lonelier than others also more depressed than others?" This compares different people.</li>
<li><b>Within-person question:</b> "When a person is lonelier than they usually are, do they later become more depressed than they usually are?" This compares the same person at different times.</li></ul>
<p>What social work interventions really care about is usually the second question: if we help a resident become less lonely (relative to their own usual level), will their depression improve as a result? But CLPM coefficients mix the two kinds of information.</p>
<p>In the demonstration below, 12 people are each measured 6 times. You can set the "between-person" and "within-person" correlations separately. By default, people with high trait loneliness also have high trait depression (ρ<sub>B</sub> = 0.7), but for any one person, times when loneliness is higher than usual are times when depression is slightly lower (ρ<sub>W</sub> = −0.4). Switch between the three views and see.</p>
""" + W("bw") + r"""
<p>You will find that a correlation computed on all the points pooled together is driven mainly by "differences between people," and it can have the opposite sign from "the relationship within each person." In statistics this phenomenon has the same roots as Simpson's paradox and the ecological fallacy.</p>
<h3>The critique by Hamaker et al. (2015)</h3>
<p>Hamaker, Kuiper and Grasman pointed out that many psychological characteristics have """ + T("trait-like stability") + r""": some people are simply lonelier than others over long periods. The autoregressive paths of a CLPM treat these "stable individual differences" as "carryover from T1 to T2," with three consequences:</p>
<ol><li>The autoregressive paths are overestimated (things look very stable, but it is "people being different," not "states carrying over");</li>
<li>The cross-lagged paths may be overestimated, underestimated, or even get the wrong sign, because they are mixed with "the correlation between the traits";</li>
<li>Researchers believe they have found a within-person dynamic process when much of it is actually between-person difference.</li></ol>
<h3>The RI-CLPM's solution: give each person a "personal baseline"</h3>
<p>The """ + T("random-intercept CLPM", "RI-CLPM") + r""" splits each observed score into two parts:</p>
""" + KEY("Decomposition:", "Observed score = grand mean + the person's stable deviation (" + T("random intercept") + ", constant over time) + this occasion's deviation from the person's baseline (" + T("within-person component") + ", changes over time)") + r"""
<p>The autoregressive and cross-lagged paths are then placed only between the within-person components. The cross-lagged path now means: <i>if a person is lonelier than they usually are at T1, are they more depressed than they usually are at T2?</i> That is a question much closer to a "process." The correlation between the two random intercepts expresses the between-person relationship separately ("people who are lonely in the long run are also depressed in the long run").</p>
<h3>Comparison on the course data</h3>
<p>The simulated data were deliberately generated with fairly strong stable traits (loneliness and depression traits correlated .50). Actual results from the companion script <code>R/L5-3.R</code>:</p>
""" + TABLE(["Path", "CLPM (standardized)", "RI-CLPM within-person (standardized)"], [
["Loneliness T1 → loneliness T2 (autoregressive)", "0.607", "0.348"], ["Depression T1 → depression T2 (autoregressive)", "0.539", "0.218"],
["Loneliness T1 → depression T2 (cross-lagged)", "0.128", "0.265"], ["Depression T1 → loneliness T2 (cross-lagged)", "0.016", "0.083"],
["Loneliness T2 → loneliness T3 (autoregressive)", "0.559", "0.198"], ["Depression T2 → loneliness T3 (cross-lagged)", "0.068", "0.245"],
["Model comparison", "χ²(4) = 67.99", "χ²(1) = 0.33; Δχ²(3) = 67.65, p &lt; .001"]]) + r"""
<p>Two observations: (1) The autoregressive paths of the RI-CLPM are much smaller: a large part of the CLPM's "stability" comes from between-person differences. (2) The cross-lagged values change too; for example, "depression T2 → loneliness T3" goes from 0.068 to 0.245. Be careful with point (2): when you compare with the large-sample values in the next section, you will see that this change is mainly sampling fluctuation in this one sample, so you cannot conclude from it that "depression → loneliness" is stronger within persons. (Note: the within-person components have smaller variances, so their standardized values cannot be compared one by one with the CLPM's, but the drop in the autoregressive paths is robust. Also, strictly speaking, the CLPM is the RI-CLPM with the random-intercept variances fixed at 0; since a variance cannot be below 0, that value lies on the boundary of the parameter space, which makes the ordinary χ² difference test conservative. Here the difference is huge (Δχ² = 67.65), so the conclusion is not affected.)</p>
<h3>Against large-sample values: how far is one sample from the population?</h3>
<p>The course data are simulated, so the generating model is known. The companion script <code>R/L5-3b.R</code> fits the same two models to a sample of 200,000 people to get the standardized paths for an infinitely large sample (the "large-sample value" in the table below). The objects here are total scores, not the 9 items, so these are not the two item-level matrices used from Lesson 7.2 on: the large-sample value in a CLPM row is the CLPM's population target (trait confounding included), and the large-sample values in the RI-CLPM within-person rows correspond to the within-person process at the total-score level in the generating model. The script then generates 200 datasets of N = 800 from the same generating model, to show how far a single sample's estimate wanders around the large-sample value.</p>
""" + TABLE(["Path (RI-CLPM within-person, standardized)", "Large-sample value", "Course sample", "90% range over 200 samples of N = 800"], [
["Loneliness T1 → loneliness T2 (autoregressive)", "{{V:ri53_RICLPM_lone1→lone2_truth}}", "{{V:ri53_RICLPM_lone1→lone2_course}}", "[{{V:ri53_RICLPM_lone1→lone2_q05}}, {{V:ri53_RICLPM_lone1→lone2_q95}}]"],
["Loneliness T1 → depression T2 (cross-lagged)", "{{V:ri53_RICLPM_lone1→dep2_truth}}", "{{V:ri53_RICLPM_lone1→dep2_course}}", "[{{V:ri53_RICLPM_lone1→dep2_q05}}, {{V:ri53_RICLPM_lone1→dep2_q95}}]"],
["Depression T1 → loneliness T2 (cross-lagged)", "{{V:ri53_RICLPM_dep1→lone2_truth}}", "{{V:ri53_RICLPM_dep1→lone2_course}}", "[{{V:ri53_RICLPM_dep1→lone2_q05}}, {{V:ri53_RICLPM_dep1→lone2_q95}}]"],
["Depression T2 → loneliness T3 (cross-lagged)", "{{V:ri53_RICLPM_dep2→lone3_truth}}", "{{V:ri53_RICLPM_dep2→lone3_course}}", "[{{V:ri53_RICLPM_dep2→lone3_q05}}, {{V:ri53_RICLPM_dep2→lone3_q95}}]"],
["Random-intercept correlation (between-person)", "{{V:ri53_RICLPM_RI_lone~~RI_dep_truth}}", "{{V:ri53_RICLPM_RI_lone~~RI_dep_course}}", "[{{V:ri53_RICLPM_RI_lone~~RI_dep_q05}}, {{V:ri53_RICLPM_RI_lone~~RI_dep_q95}}]"]]) + KEY("What the table shows:", "<ol><li><b>The drop in the autoregressive paths is real.</b> The large-sample value of the within-person autoregressive path is {{V:ri53_RICLPM_lone1→lone2_truth}}, while the CLPM gives {{V:ri53_CLPM_lone1→lone2_truth}} even with an infinite sample: the CLPM's \"stability\" really is inflated by the stable traits.</li><li><b>The true direction is the same as in the CLPM, but the course sample overestimates both directions.</b> The within-person large-sample values are about {{V:ri53_RICLPM_lone1→dep2_truth}} for loneliness → depression and about {{V:ri53_RICLPM_dep1→lone2_truth}} for depression → loneliness, the same direction as the CLPM (loneliness → depression is stronger). The course sample's \"loneliness T1 → depression T2 = {{V:ri53_RICLPM_lone1→dep2_course}}\" is {{V:ri53_RICLPM_lone1→dep2_pos}}, and \"depression T2 → loneliness T3 = {{V:ri53_RICLPM_dep2→lone3_course}}\" is also {{V:ri53_RICLPM_dep2→lone3_pos}}; at the same time, the random-intercept correlation of {{V:ri53_RICLPM_RI_lone~~RI_dep_course}} is {{V:ri53_RICLPM_RI_lone~~RI_dep_pos}}. These numbers are off together: the random intercepts absorbed too little of the between-person association of loneliness with depression, and that part of the association moved into the within-person cross-lagged paths. The course data happen to be a rather untypical sample.</li><li><b>With 3 waves and N = 800, the within-person cross-lagged paths of an RI-CLPM are very imprecise.</b> One sample's estimate can land anywhere in a range as wide as the fourth column above; if you compare the two directions by their point estimates alone, you can easily reach the opposite conclusion.</li></ol><p>So the value of the RI-CLPM is that it removes between-person confounding, and the price is precision. Always report confidence intervals; to compare the two directions, test their difference instead of comparing two point estimates.</p>") + r"""
""" + WARN("What this means for CLPN:", "A CLPN (both the simplified \"LASSO-only\" version that is this course's main approach and the full procedure of Wysocki et al., 2025) uses observed item scores and has <b>no</b> random intercepts, so, like the CLPM, it mixes between-person and within-person information. In the course data, <code>data/true_B_within.csv</code> (the within-person truth: the within-person structure used to generate the data) and <code>data/true_B_population.csv</code> (the population target: what a CLPN converges to in an infinitely large sample) are clearly different; the latter has many extra small positive edges caused by the stable traits. From Lesson 7.2 on, the two appear side by side, and Lesson 7.5 discusses them in detail.") + r"""
<h3>Requirements and limitations of the RI-CLPM</h3>
<ul><li>It needs at least 3 waves: with 2 waves, the "stable part" and the "changing part" cannot be separated (the model is not identified).</li>
<li>It assumes the trait part is completely constant over time; if there are long-term trends, you may need a more complex model (e.g., adding random slopes or a linear trend; the three extensions discussed by Mulder and Hamaker (2021) add time-invariant predictors and outcomes, multiple-group comparisons, and multiple-indicator models).</li>
<li>It is still only "prediction over time within persons"; it does not turn into causation automatically (Lesson 5.4).</li></ul>
""",
math=r"""
<p>Take loneliness as an example. For person \(i\) at time \(t\), the observed score is:</p>
""" + MATH(r"\text{Loneliness}_{it} = \mu_t + \kappa_i + w_{it}") + MATH(r"w^{L}_{i,t+1} = \alpha\, w^{L}_{it} + \gamma\, w^{D}_{it} + u^{L}_{i,t+1}") + SYM([
(r"\(i,\ t\)", "Subscripts: person i, measurement t"),
(r"\(\mu_t\)", "Greek letter mu: the overall mean at wave t (the average of everyone)"),
(r"\(\kappa_i\)", "Greek letter kappa: person i's random intercept = how far they are stably above/below the mean (constant over time)"),
(r"\(w_{it}\)", "Within-person component: how far this occasion is from the person's own baseline (within)"),
(r"\(w^{L},\ w^{D}\)", "Superscript L = loneliness, D = depression: their within-person components"),
(r"\(\alpha\)", "Alpha: within-person autoregressive path (how much a lonelier-than-usual state carries over)"),
(r"\(\gamma\)", "Gamma: within-person cross-lagged path (more depressed than usual → lonelier than usual next time)"),
(r"\(u_{i,t+1}\)", "Residual of the within-person equation (a new shock, the innovation)"),
]) + r"""
<h4>Why is the CLPM biased? A two-line derivation</h4>
<p>If you ignore \(\kappa_i\) and predict \(\text{Loneliness}_{t+1}\) from \(\text{Loneliness}_t\), their covariance is</p>
""" + MATH(r"\mathrm{Cov}(\text{Loneliness}_t,\text{Loneliness}_{t+1}) = \underbrace{\mathrm{Var}(\kappa)}_{\text{between-person}} + \underbrace{\mathrm{Cov}(w_t, w_{t+1})}_{\text{within-person}}") + r"""
<p>The first term has nothing to do with any process over time, yet the CLPM treats it as "stability." In the same way, the covariance of the loneliness and depression random intercepts, \(\mathrm{Cov}(\kappa^L,\kappa^D)\), leaks into the cross-lagged paths. The RI-CLPM separates these parts by estimating \(\kappa\) as its own latent variable.</p>
""" + NOTE("How to do it in lavaan:", "A random intercept is a latent variable whose loadings on the three waves of observed scores are all fixed at 1 (<code>RI_lone =~ 1*lone1 + 1*lone2 + 1*lone3</code>); each observed score also gets a within-person latent variable (loading 1), and the error variance of the observed variable itself is fixed at 0."),
code=CODE(r"""
riclpm <- '
  # 1) Random intercepts: each person's stable "trait level," loadings fixed at 1
  RI_lone =~ 1*lone1 + 1*lone2 + 1*lone3
  RI_dep  =~ 1*dep1  + 1*dep2  + 1*dep3
  # 2) Within-person components
  wl1 =~ 1*lone1; wl2 =~ 1*lone2; wl3 =~ 1*lone3
  wd1 =~ 1*dep1;  wd2 =~ 1*dep2;  wd3 =~ 1*dep3
  # 3) Within-person autoregressive and cross-lagged paths
  wl2 ~ wl1 + wd1;  wd2 ~ wd1 + wl1
  wl3 ~ wl2 + wd2;  wd3 ~ wd2 + wl2
  # 4) Within-wave correlations and (residual) variances
  wl1 ~~ wd1; wl2 ~~ wd2; wl3 ~~ wd3
  wl1 ~~ wl1; wd1 ~~ wd1; wl2 ~~ wl2; wd2 ~~ wd2; wl3 ~~ wl3; wd3 ~~ wd3
  RI_lone ~~ RI_lone; RI_dep ~~ RI_dep; RI_lone ~~ RI_dep
  # 5) Random intercepts uncorrelated with the T1 within-person components; observed-variable errors fixed at 0
  RI_lone ~~ 0*wl1 + 0*wd1;  RI_dep ~~ 0*wl1 + 0*wd1
  lone1 ~~ 0*lone1; lone2 ~~ 0*lone2; lone3 ~~ 0*lone3
  dep1 ~~ 0*dep1;   dep2 ~~ 0*dep2;   dep3 ~~ 0*dep3
'
fit_ri <- lavaan(riclpm, data = wide, missing = "fiml",
                 meanstructure = TRUE, int.ov.free = TRUE)
summary(fit_ri, standardized = TRUE, fit.measures = TRUE)
anova(fit_c, fit_ri)    # Compare with the CLPM (the CLPM is nested in the RI-CLPM)
""", "Core of R/L5-3.R (structure follows the lavaan example by Mulder & Hamaker)") + r"""
<p><b>Block by block:</b> block 1 defines the two random intercepts; block 2 gives each observed score a within-person latent variable; block 3 is the within-person dynamics we care about; block 4 holds the within-wave correlations and the variances; block 5 contains the fixed constraints needed for identification. <code>wide</code> and <code>fit_c</code> come from the earlier part of the script (the same total scores and CLPM as in 5.2).</p>
""" + TIP("What to look at in the results:", "(1) The standardized value of <code>RI_lone ~~ RI_dep</code> = the between-person correlation; (2) whether the random-intercept variances are clearly above 0 (if they are close to 0, the RI-CLPM and the CLPM reach similar conclusions); (3) the within-person cross-lagged paths such as <code>wl2 ~ wd1</code>; (4) the model comparison from <code>anova()</code>."),
quiz=[
("\"When a person is lonelier than they usually are, they later become more depressed than they usually are\" describes:",
 ["A between-person effect", "A within-person effect", "A within-wave correlation", "Measurement error"], 1,
 ["Between-person compares different people; the reference point in this sentence is the person themselves.",
  "Correct: the reference point is \"their own usual level.\"",
  "A within-wave correlation describes change together at the same moment and says nothing about \"later.\"",
  "Measurement error is random noise in the scores, not a relationship about \"later.\""]),
("What does the random intercept in an RI-CLPM stand for?",
 ["The overall mean at each wave",
  "Each person's stable individual difference that does not change over time (the trait-like part)",
  "The cross-lagged coefficients",
  "Measurement error"], 1,
 ["The overall mean at each wave is μ_t, shared by everyone; the random intercept is each person's own stable deviation.",
  "Correct.",
  "The cross-lagged paths sit between the within-person components, not on the random intercepts.",
  "In this model the observed errors are fixed at 0; the random intercept is the part that is stable over time, not error."]),
("Why does the RI-CLPM need at least 3 waves?",
 ["A software limitation",
  "With 2 waves the stable part and the changing part cannot be separated (not identified)",
  "Because estimating cross-lagged paths needs at least two time intervals",
  "Because equality constraints have to be estimated"], 1,
 ["It is a statistical identification problem; any software has it.",
  "Correct.",
  "Two waves give one interval, and a CLPM can still estimate cross-lagged paths; the RI-CLPM needs 3 waves to separate the stable part from the changing part.",
  "Equality constraints are optional; without them, a 2-wave RI-CLPM is still not identified."]),
("In the course data, the autoregressive coefficients drop clearly when you switch from the CLPM to the RI-CLPM. What is the most reasonable explanation?",
 ["The RI-CLPM fits worse, so the coefficients are pushed down",
  "Much of the CLPM's \"stability\" comes from stable between-person differences",
  "Within-person states actually have no inertia",
  "The within-person process is more stable"], 1,
 ["The RI-CLPM fits clearly better (Δχ²(3) = 67.65); the coefficients shrink because the random intercepts take over the stable individual differences.",
  "Correct.",
  "The within-person autoregressive paths are still positive (e.g., 0.348), just smaller than in the CLPM: there is inertia, but less than the CLPM shows.",
  "The opposite: smaller within-person autoregressive paths mean that states carry over less than the CLPM suggests."]),
("Does a standard CLPN already separate between-person from within-person?",
 ["Yes, a CLPN is a within-person model by nature",
  "No; it is based on observed scores and, like the CLPM, mixes the two, which you must say when you interpret results and write the limitations",
  "Only when lambda.1se is used",
  "Standardizing is enough to separate them"], 1,
 ["A common misunderstanding: a CLPN uses observed scores and has no random intercepts.",
  "Correct: this is a point every CLPN paper must make in its limitations.",
  "λ only decides how many edges are shrunk away; it does not separate the stable traits from the scores.",
  "Standardizing only changes units; it cannot remove stable traits."]),
],
ex=[
("One between-person and one within-person example", "Basic",
 r"""<p>Using "social participation" and "loneliness," write one between-person and one within-person research question, and imagine a situation in which the two relationships go in opposite directions.</p>""",
 r"""<p>Between-person: "Are residents who participate more socially less lonely than residents who participate less?" (probably a negative correlation). Within-person: "When a resident takes part in more activities than usual for a while, are they lonelier than usual?" This could be positive: for example, a resident who has just moved to a new neighborhood is invited to lots of activities while still settling in, and feels lonely precisely then. The two levels can go in opposite directions.</p>"""),
("Read the table and explain it in 200 words", "Writing",
 r"""<p>Using the CLPM vs. RI-CLPM table above, write an explanation of about 200 words for "a social work colleague who has never studied statistics."</p>""",
 r"""<p>Key points: ① The ordinary model (CLPM) shows loneliness and depression as "very stable," with loneliness mainly predicting depression. ② But in these data, some people are lonelier and more depressed than others over the long run, and the ordinary model mistakes these "long-term differences" for a process of change. ③ Once each person's long-term level is taken out (RI-CLPM), we see the relationship between fluctuations of the kind "lonelier / more depressed than usual." In this sample both directions are estimated as fairly large, but the comparison with the large-sample values (the section "Against large-sample values" on this page) shows that, with 3 waves and N = 800, these within-person cross-lagged estimates vary a lot, so you cannot tell from them which direction is stronger. ④ So if an intervention aims to change a person's state, look at the results with the long-term differences removed, while admitting that such estimates are imprecise and are still statistical prediction, not causation.</p>"""),
("Hands-on: random-intercept variances", "Hands-on",
 r"""<p>Run <code>R/L5-3.R</code>, find the standardized estimates of <code>RI_lone ~~ RI_lone</code>, <code>RI_dep ~~ RI_dep</code> and <code>RI_lone ~~ RI_dep</code> in <code>summary(fit_ri)</code>, and answer: how large is the between-person correlation? Is it close to the 0.50 set in the simulation?</p>""",
 r"""<p>In the <code>Covariances:</code> part, look up the <code>Std.all</code> of <code>RI_lone ~~ RI_dep</code>: that is the correlation of the two random intercepts. The simulation set the trait correlation to 0.50, but the observed scores were built from "trait + item-specific part + within-person state" and then cut into Likert categories, so the estimate need not equal 0.50. The actual result in this data (<code>R/solutions/L5-3_solution.R</code>) is a random-intercept correlation of 0.20, 95% CI [−0.02, 0.42], clearly below 0.50 and with a very wide interval. The main reason is sampling error: under the same generating model, the random-intercept correlation for an infinite sample is {{V:ri53_RICLPM_RI_lone~~RI_dep_truth}} (<code>R/L5-3b.R</code>); the 90% range over 200 samples of N = 800 is [{{V:ri53_RICLPM_RI_lone~~RI_dep_q05}}, {{V:ri53_RICLPM_RI_lone~~RI_dep_q95}}], and the course sample's {{V:ri53_RICLPM_RI_lone~~RI_dep_course}} is {{V:ri53_RICLPM_RI_lone~~RI_dep_pos}}. With only 3 waves the RI-CLPM is just identified, and the "stable part" and the "within-person part" are hard to tell apart, so the estimate is very imprecise. The large-sample value itself is also a little below 0.50; that is a secondary reason: each item also has its own independent stable component, women have a stable offset on the depression items, and Likert categories weaken correlations. Also, the random-intercept variances (loneliness 3.40, depression 4.35) are about 38% of the variance of the observed totals (the average of the per-wave variances: loneliness 9.07, depression 11.52). That is smaller than the depression ICC from the multilevel model in Lesson 4.1 (0.53): the multilevel model attributes all of the covariance across waves to stable differences between people, while the RI-CLPM attributes part of it to within-person deviations carrying over (see the paragraph "Why does Lesson 5.3 say 'the stable part is about 38%'?" in Lesson 4.1). With only 3 waves these two sources are hard to separate, so 0.38 is as imprecise as the random-intercept correlation. Even when the model's "structure is right," with 3 waves and N = 800 the between-person estimates can be far from the large-sample values, so report them with confidence intervals.</p>"""),
],
summary=[
    "Between-person: comparing people with each other; within-person: comparing a person with their own usual level. The two can go in opposite directions.",
    "Hamaker et al. (2015): the CLPM mixes stable traits into the autoregressive and cross-lagged paths.",
    "RI-CLPM = random intercepts (the stable part) + within-person components (the dynamic part); needs at least 3 waves.",
    "Course data: the RI-CLPM's autoregressive paths drop sharply and the model fits significantly better; with 3 waves and N = 800 the within-person cross-lagged paths are very imprecise, and a single sample cannot tell you the direction (large-sample values in L5-3b.R).",
    "A standard CLPN has no random intercepts; say so when you interpret the results and write the limitations."
],
refs=["Hamaker, E. L., Kuiper", "Mulder, J. D.", "Wysocki, A., McCarthy"],
)

L["5.4"] = dict(
lead=r"""<p>In longitudinal and CLPN papers, the most common reviewer comment is usually not "the code is wrong" but "the conclusions go too far." This lesson discusses where prediction over time ends and causal inference begins, and how to report results in accurate, restrained language.</p>""",
intuition=r"""
<h3>What does causal inference need?</h3>
<p>The classic answer: to say "A causes B" you need at least (1) an association between A and B; (2) A occurring before B (""" + T("temporal precedence") + r"""); (3) other explanations (such as common causes) ruled out. Cross-lagged paths in panel data help with (2) at best, and partly with (1); (3) is almost never achieved.</p>
<h3>"Granger causality" is not real causality</h3>
<p>The economist Granger proposed: if knowing A's past predicts B's future better than "knowing B's past" alone, then A "Granger-causes" B. The cross-lagged paths of the CLPM and CLPN are essentially predictions of this """ + T("Granger causality") + r""" kind. Despite "causality" in the name, it is only predictability: "seeing many people on the street carrying umbrellas" Granger-predicts "rain later," but carrying umbrellas obviously does not cause rain. Both are driven by the same common cause, the rainy weather on its way (people learn about it from the forecast or the dark clouds and take an umbrella).</p>
<h3>Five common threats</h3>
""" + TABLE(["Threat", "Example: loneliness and depression"], [
["Unmeasured confounding", "Chronic illness, widowhood or financial hardship may raise both loneliness and depression; what you did not measure, you cannot control"],
["Reverse causation", "Depression makes people withdraw and so become lonelier; if the two act on each other within the lag, the direction is hard to tell apart"],
["Measurement error", "Self-report scales contain error; error makes the autoregressive paths underestimated, so the cross-lagged paths end up \"speaking for\" the autoregressive paths"],
["Unsuitable time lag", "If the true effect peaks within 2 months, measuring every 6 months may catch it after it has faded"],
["Between-/within-person confounding", "See 5.3: people who are lonely in the long run are also depressed in the long run"]]) + r"""
<p>The demonstration below shows the role of the time lag. Suppose the "true process" runs month by month: each month loneliness gives depression a small push, and each variable has its own inertia. Measure it with different lags and you get cross-lagged coefficients of completely different sizes.</p>
""" + W("lag") + r"""
<h3>Lucas (2023): why the CLPM is "almost never the right choice"</h3>
<p>Lucas showed by simulation that whenever there are stable individual differences (and almost every psychological variable has them), the CLPM easily produces "significant" cross-lagged paths even when the true within-person effect is 0, and the larger the sample, the more easily these "false positives" reach significance. He therefore argues that you should at least use a model that handles stable traits (such as the RI-CLPM) and be very restrained about causal readings of cross-lagged paths. The critique applies equally to the standard CLPN.</p>
<h3>A spectrum of wording: from most careful to overreaching</h3>
""" + TABLE(["Level", "Example", "Assessment"], [
["Descriptive", "\"T1 loneliness is positively correlated with T2 depression\"", "Safe, but says little"],
["Predictive", "\"Controlling for baseline depression, T1 loneliness positively predicts T2 depression\"", "The standard wording for CLPM/CLPN"],
["Suggestive", "\"This result is consistent with the hypothesis that loneliness may worsen depression\"", "Fine, if paired with a statement of limitations"],
["Causal", "\"Loneliness causes / leads to / produces depression\"", "Usually not supported by observational panel data"],
["Interventional", "\"So reducing loneliness will lower depression\"", "Needs an intervention study (such as a randomized controlled trial)"]]) + r"""
<p>The small tool below checks your paragraph for "risky words." Paste in a conclusion you wrote and try it.</p>
""" + W("cause") + r"""
""" + NOTE("Social work perspective:", "Wording affects how resources are allocated. If your policy recommendation says \"reducing loneliness will lower depression,\" but in reality both are caused by financial hardship, money spent only on \"befriending visits\" may achieve little. While wording things accurately, you can still actively propose \"hypotheses worth testing in an intervention study.\""),
math=r"""
<p>The math of this lesson is one central contrast: prediction and intervention are two different conditional expectations.</p>
""" + MATH(r"\underbrace{\mathbb{E}[\,D_{t+1}\mid L_t = l,\ D_t = d\,]}_{\text{prediction: people observed with } L_t=l} \quad\text{vs}\quad \underbrace{\mathbb{E}[\,D_{t+1}\mid \mathrm{do}(L_t = l),\ D_t = d\,]}_{\text{intervention: setting } L_t \text{ to } l}") + SYM([
(r"\(L_t,\ D_t\)", "Loneliness (L) and depression (D) at time t"),
(r"\(\mathbb{E}[\,\cdot \mid \cdot\,]\)", "Conditional expectation: the average of the variable on the left among the people for whom the condition on the right holds"),
(r"\(\mathrm{do}(L_t=l)\)", "Pearl's do notation: not \"observed to be\" but \"set to\" l (for example, by an intervention)"),
]) + r"""
<p>A cross-lagged coefficient estimates the left side (prediction). The left side equals the right side only when conditions such as "no unmeasured confounding" hold. If a common cause \(U\) (such as chronic illness) raises both \(L_t\) and \(D_{t+1}\), then people observed with high \(L_t\) also tend to have high \(U\), so the left side "seems" to show an effect while the right side (actually changing loneliness) may be 0.</p>
<h4>The math of the time lag (for reference)</h4>
<p>If the true process runs monthly, \(\mathbf{x}_{m+1} = A\,\mathbf{x}_m + \boldsymbol\varepsilon\) (\(\mathbf{x}\) is the vector of loneliness and depression, \(A\) the monthly coefficient matrix), then the coefficient matrix for a lag of \(\Delta\) months is \(A^{\Delta}\) (the matrix to the power \(\Delta\)). In the demonstration above, \(A=\begin{pmatrix}a&0\\c&a\end{pmatrix}\), and you can work out that the cross effect at lag \(\Delta\) is \(\Delta\,a^{\Delta-1}c\): it first grows with \(\Delta\), then shrinks as \(a^{\Delta-1}\) decays. So results from studies with different lags cannot simply be compared.</p>
""",
code=r"""
<p>This lesson is mostly about writing and reasoning. The companion script <code>R/L5-4.R</code> uses only simulated data (only in a simulation do we know the "truth") and has four parts: ① unmeasured confounding; ② the measurement lag; ③ stable traits causing false positives in the CLPM; ④ checking a conclusion for "risky causal words." Here is the core code of part 1.</p>
""" + CODE(r"""
set.seed(2026)
N <- 800
U  <- rnorm(N)                       # Unmeasured common cause (e.g., severity of a chronic illness)
L1 <- 0.6 * U + rnorm(N, 0, 0.8)     # T1 loneliness: affected by U
D1 <- 0.6 * U + rnorm(N, 0, 0.8)     # T1 depression: affected by U
D2 <- 0.5 * D1 + 0.4 * U + rnorm(N, 0, 0.7)   # T2 depression: affected by D1 and U; loneliness has NO effect on it
summary(lm(scale(D2) ~ scale(D1) + scale(L1)))  # The L1 coefficient will be significantly > 0!
summary(lm(scale(D2) ~ scale(D1) + scale(L1) + scale(U)))  # With U controlled, the L1 coefficient ≈ 0
""", "Small simulation: a \"significant cross-lagged path\" without any causation (copy into R and run)") + r"""
<p><b>Actual results (R/output/L5-4_log.txt):</b> in the first model the coefficient of <code>scale(L1)</code> is β = 0.186 (SE = 0.028, p &lt; .001), "significant"; in the second model, with U controlled, it falls to β = 0.016 (p = 0.58), close to 0. The script also repeats the simulation 500 times: the true effect is 0, yet the loneliness coefficient has p &lt; .05 in 100% of them. At N = 800, confounding of this size produces a "significant cross-lagged path" almost every time. In real studies we usually cannot measure U, so all we can do is name this possibility in the discussion.</p>
""" + OUT(RLOG("L5-4_log.txt", "→ Cross-lag", 3), "L5-4_log.txt (part 1, excerpt)") + TIP("Going further:", "Change <code>0.4 * U</code> to <code>0</code> and run the first model again: when U no longer affects D2 directly, what happens to L1's \"false effect\"? The script's answer is β = 0.028 (p = 0.38): it has essentially disappeared. The reason: U still affects D2 through D1, but D1 is already controlled, so this \"borrowed\" path is blocked. For a confounder to create a false effect, it has to bypass the variables you control and act on the outcome directly.") + r"""
<h3>Part 2: a different lag gives a different coefficient</h3>
<p>Following "the math of the time lag" above, the script works out the cross effect \(\Delta\,a^{\Delta-1}c\) month by month and checks it by repeated matrix multiplication. With a monthly autoregressive effect a = 0.80 and a monthly cross effect c = 0.15, the cross-lagged paths at lags of 1 / 3 / 6 / 12 / 24 months are 0.150 / 0.288 / 0.295 / 0.155 / 0.021, peaking at about 4 months (theoretical value \(-1/\ln a\approx4.5\)); with a = 0.90 and c = 0.05 they are 0.050 / 0.122 / 0.177 / 0.188 / 0.106, peaking at about 10 months. The same process, measured with a 1-month and a 24-month lag, gives two completely different conclusions: "effect 0.15" and "effect 0.02." The figure is <code>R/output/L5-4_lag.png</code>.</p>
<h3>Part 3: stable traits and false positives in the CLPM</h3>
<p>Following Lucas (2023), the script simulates data in which "trait loneliness" and "trait depression" are correlated but the within-person cross-lagged effect is exactly 0, and then tests loneliness → depression with a CLPM-style regression (D2 ~ D1 + L1). Result: 39% of samples are "significant" at N = 200, 95% at N = 800, 100% at N = 3000. As a control, with the traits removed, the share at N = 800 is only 8.0% (close to the nominal 5%; 200 simulations have sampling fluctuation). The larger the sample, the more "confidently" the CLPM reports an effect that does not exist; controlling for T1 depression does not remove the trait, because T1 depression is only a noisy measure of the trait.</p>
""",
quiz=[
("At most, which condition for causal inference does \"A at T1 predicts B at T2\" satisfy?",
 ["Ruling out all other explanations",
  "Temporal precedence (and association)",
  "Random assignment",
  "Error-free measurement"], 1,
 ["Ruling out other explanations is exactly what observational data find hardest, and cross-lagged paths can't do it.",
  "Correct.",
  "Panel studies usually have no random assignment, and cross-lagged paths cannot replace it.",
  "Self-report scales still have measurement error, and cross-lagged paths do not remove it."]),
("Which of these is a possible unmeasured confounder of the \"loneliness → depression\" relationship?",
 ["The wording of the loneliness items",
  "Chronic illness or financial hardship",
  "Sample size",
  "The choice of λ"], 1,
 ["Wording is a measurement issue, not a third variable that affects both loneliness and depression.",
  "Correct: it may affect both loneliness and depression.",
  "Sample size affects precision, but it is not a third variable that affects both loneliness and depression.",
  "λ is the analyst's setting, not something in the data that affects both variables."]),
("What is Granger causality closest to?",
 ["A real causal effect",
  "Given B's past, A's past adds to the prediction of B's future",
  "A within-wave correlation of A and B",
  "A comes before B, so A causes B"], 1,
 ["\"Causality\" is in the name, but it only shows predictability; umbrellas predicting rain is a counterexample.",
  "Correct: it is \"predictability.\"",
  "Granger causality is about \"the past predicting the future\"; a within-wave correlation involves no time order.",
  "Temporal precedence is only one necessary condition for causation and cannot establish it on its own."]),
("Which sentence is most appropriate?",
 ["Loneliness causes depression",
  "Reducing loneliness will lower depression",
  "Controlling for baseline depression, T1 loneliness positively predicted depression 6 months later, consistent with the hypothesis that loneliness may worsen depression",
  "Depression has no effect at all on loneliness"], 2,
 ["Observational panel data do not support causal wording such as \"causes.\"",
  "This is an interventional conclusion; it needs an intervention study (such as a randomized controlled trial).",
  "Correct: it states the control and the lag, and makes a careful suggestion.",
  "Not significant ≠ absent: the sample size or the lag may simply be unsuitable."]),
("What is the core of Lucas's (2023) critique of the CLPM?",
 ["The CLPM needs samples so large that ordinary studies can't reach them",
  "When there are stable individual differences, the CLPM easily produces spurious cross-lagged paths, and they become \"significant\" more easily in large samples",
  "The CLPM can't be used with three waves",
  "The CLPM must be estimated with LASSO"], 1,
 ["Lucas's worry is the opposite: the larger the sample, the more easily spurious cross-lagged paths become significant.",
  "Correct.",
  "The CLPM works with three or more waves; Lesson 5.2 uses three.",
  "The CLPM is estimated by ordinary maximum likelihood and doesn't need LASSO; LASSO is what the CLPN uses."]),
],
ex=[
("Rewrite 5 overly causal conclusions", "Writing",
 r"""<ol><li>Loneliness causes depression in community residents.</li><li>Sleep problems are the root cause of fatigue.</li><li>Social support protects residents from depression.</li><li>Worthlessness drives the whole depression network.</li><li>Therefore social workers should intervene on loneliness first to lower depression.</li></ol><p>For each sentence, write an accurate version and give one alternative explanation.</p>""",
 r"""<ol><li>"Controlling for baseline depression, T1 loneliness positively predicted T2 depression." Alternative explanation: a chronic illness causes both loneliness and depression.</li>
<li>"T1 sleep problems had a fairly strong cross-lagged prediction of T2 fatigue." Alternative explanation: both reflect a physical illness or a side effect of medication.</li>
<li>"Residents with higher T1 social support had lower T2 depression." Alternative explanation: people less prone to depression find it easier to get, and to perceive, support (reverse causation / between-person differences).</li>
<li>"Worthlessness had the highest out-expected influence in the network, suggesting that it predicts later levels of other symptoms fairly strongly." Alternative explanation: the item may overlap in content with other items, or be less stable.</li>
<li>"Loneliness may be a target worth testing in an intervention study; the present results are not enough to establish that intervening on loneliness lowers depression."</li></ol>"""),
("Draw a confounding diagram", "Basic",
 r"""<p>Draw an arrow diagram with U (unmeasured confounder) → loneliness T1, U → depression T2, and depression T1 → depression T2. Explain why the cross-lagged path "loneliness T1 → depression T2" comes out significant.</p>""",
 r"""<p>There is a "backdoor path" between loneliness T1 and depression T2: loneliness T1 ← U → depression T2. The regression only controls for depression T1, which does not block this path, so loneliness T1 gets a nonzero coefficient as a "proxy" for U. Only measuring and controlling for U (or a design such as randomization) can block it.</p>"""),
("Time lag", "Understanding",
 r"""<p>In the "measurement lag" demonstration on this page, set the monthly autoregressive effect to 0.9 and the monthly cross effect to 0.05, and read off the cross-lagged paths at lags of 1, 6 and 12 months. If two papers used lags of 3 and 12 months and reached different conclusions, how would you interpret that?</p>""",
 r"""<p>With the formula \(\Delta\, a^{\Delta-1} c\): 1 month 0.05; 6 months \(6\times0.9^5\times0.05\approx0.177\); 12 months \(12\times0.9^{11}\times0.05\approx0.188\) (the peak is around 9–10 months). Different lags giving different coefficients is normal, so you can't simply say that "the findings are inconsistent"; the discussion should consider the difference in lags, and ideally you would use a continuous-time model or data with several lags.</p>"""),
],
summary=[
    "A cross-lagged path = Granger-style \"predictability\"; at most it satisfies temporal precedence, and ruling out other explanations is almost impossible.",
    "Five threats: unmeasured confounding, reverse causation, measurement error, an unsuitable lag, between-/within-person confounding.",
    "Prediction E[D|L] ≠ intervention E[D|do(L)].",
    "Wording: descriptive → predictive → suggestive are fine; avoid \"causes\" and \"will reduce.\"",
    "Lucas (2023): with stable traits, the CLPM easily produces spurious cross-lagged paths, and the critique applies equally to the CLPN."
],
refs=["Lucas, R. E. (2023)", "Hamaker, E. L., Kuiper"],
)
