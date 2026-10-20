# -*- coding: utf-8 -*-
# Module 5: CLPM and RI-CLPM
L["5.1"] = dict(
lead=r"""<p>From this lesson on, we look at relationships over time. Module 5 explains the logic of cross-lagged models, and their pitfalls, at the level of constructs (total scores); the CLPN in Module 7 takes each of these ideas down to the level of single items.</p>""",
intuition=r"""
<h3>A social work scenario</h3>
<p>You work at a community service center. Three times, six months apart, you ask the same group of residents to fill in a loneliness scale and a depression scale. The center's director asks you: "Is it loneliness that makes people depressed, or depression that makes people lonelier and lonelier?" Questions of "which comes first" like this are what the """ + T("cross-lagged panel model", "CLPM") + r""" tries to answer.</p>
<p>The idea of the CLPM can be broken into three statements:</p>
<ol>
<li><b>People have inertia.</b> Someone who was very lonely six months ago will probably still be fairly lonely six months later. This "predicting yourself from yourself" arrow is called an """ + T("autoregressive path", "AR") + r"""; it stands for the stability of individual differences.</li>
<li><b>After removing the inertia, see whether the other variable adds anything.</b> If, once you know a person's depression six months ago, also knowing their loneliness six months ago predicts their current depression better, then the """ + T("cross-lagged path", "CL") + r""" "loneliness T1 → depression T2" is not 0.</li>
<li><b>At the same time point, the two move together anyway.</b> The correlation between loneliness and depression within one measurement occasion (and, at T2 and T3, the correlation between "the parts not explained by the previous wave") is shown as a """ + T("within-wave correlation / residual covariance") + r""", drawn as a curved double-headed arrow.</li>
</ol>
""" + KEY("Key intuition:", "A cross-lagged coefficient does not answer \"are loneliness and depression related?\" It answers \"given your past depression, does your past loneliness predict your future depression any better?\" That is what \"controlling for the autoregressive path\" means.") + r"""
<h3>Path diagrams: the visual language of SEM</h3>
<p>The CLPM is a """ + T("structural equation model", "SEM") + r""". SEM usually expresses a model as a """ + T("path diagram") + r""", and the conventions are few:</p>
""" + TABLE(["Symbol", "Meaning", "In the CLPM"], [
    ["Box □", "Observed variable (a score measured directly)", "Loneliness T1, depression T2, … (here, scale totals)"],
    ["Ellipse ○", "Latent variable (cannot be measured directly)", "The \"random intercepts\" of Lesson 5.3 are latent variables"],
    ["Single-headed arrow →", "Regression (prediction) path", "Autoregressive paths a, b; cross-lagged paths c, d"],
    ["Curved double-headed arrow ↔", "Correlation / covariance", "(Residual) correlation within a wave"]
]) + r"""
<p>The interactive diagram below is a CLPM with two variables and three waves. Try three things: (1) switch off "cross-lagged" and watch the model become "each variable on its own"; (2) switch off "autoregressive," keep only the cross-lagged paths, and read the warning below; (3) set d to a negative value and ask yourself whether "the lonelier someone is, the less depressed they become later" makes sense in practice.</p>
""" + W("clpm") + r"""
<h3>Why must a cross-lagged path "control for" the autoregressive path?</h3>
<p>Suppose loneliness and depression are already strongly correlated at T1 (say r = .5), and each is very stable. Even if loneliness adds nothing at all to the prediction of depression, "loneliness T1" and "depression T2" will still be quite strongly correlated, because loneliness T1 is correlated with depression T1, and depression T1 strongly predicts depression T2. If depression T1 is left out of the equation, the path "loneliness T1 → depression T2" takes credit for this "borrowed" correlation. This is the same omitted-variable bias you met in Module 3 (leave out a variable that is correlated with the predictor and also affects the outcome, and the coefficient "absorbs" its effect; here it is inflated; review """ + LINK("3.2") + r""").</p>
<h3>If c is significant and d is not, what does that tell you?</h3>
<p>Suppose "depression T1 → loneliness T2" (c) is significant and "loneliness T1 → depression T2" (d) is not. The most careful wording is: <i>in this sample and at this lag, people with higher depression at T1 also had higher loneliness at T2, after controlling for T1 loneliness; the prediction in the other direction was not supported.</i> Note three things: (1) "not significant" does not mean "absent"; the sample size or the lag may simply be unsuitable; (2) one path significant and the other not does not mean the two "differ significantly"; comparing them needs its own test (e.g., constrain c and d to be equal in lavaan and compare the models); (3) this is still prediction over time, not causation (see """ + LINK("5.4") + r""").</p>
<h3>CLPM vs. CLPN: from "total scores" to "items"</h3>
<p>In a traditional CLPM, each box is the total score of a construct (e.g., the sum of the 4 loneliness items), so all you can say is that "loneliness as a whole" predicts "depression as a whole." But in social work practice you would rather know: is it the feeling that "no one understands me," or the situation of "lacking companionship," that better predicts later "loss of interest"? CLPN simply replaces each box of the CLPM with a single item, so the 4 paths between 2 variables become 81 paths among 9 items (9 autoregressive + 72 cross-lagged). With that many paths, you need LASSO to "pick" among them (""" + LINK("3.5") + r""" in Module 3, and Module 7).</p>
""" + NOTE("A reminder:", "This lesson's R script first uses ordinary regression, <code>lm()</code>, to \"approximate\" one time interval of the CLPM (T1→T2), so you can see that \"each T2 variable is one regression equation.\" The next lesson, 5.2, fits the whole three-wave model in one go with lavaan."),
math=r"""
<p>The math of the CLPM is just two multiple regression equations (per time interval). Assume all variables have been standardized (z scores, mean 0, standard deviation 1; see Module 1):</p>
""" + MATH(r"\text{Loneliness}_{t+1} = a\cdot \text{Loneliness}_{t} + c\cdot \text{Depression}_{t} + e^{L}_{t+1}") + MATH(r"\text{Depression}_{t+1} = b\cdot \text{Depression}_{t} + d\cdot \text{Loneliness}_{t} + e^{D}_{t+1}") + SYM([
(r"\(t,\ t+1\)", "Two adjacent measurement occasions (waves), e.g., T1 and T2"),
(r"\(a,\ b\)", "Autoregressive coefficients: how strongly \"your own past\" predicts \"your own present,\" controlling for the other variable. Standardized, they are usually between 0.3 and 0.8"),
(r"\(c,\ d\)", "Cross-lagged coefficients: how much \"the other variable's past\" adds to the prediction of \"your own present,\" controlling for your own past. c = depression → loneliness, d = loneliness → depression"),
(r"\(e^{L}_{t+1},\ e^{D}_{t+1}\)", "Residuals: the part the equation does not explain. The superscripts L and D are just labels for the loneliness and depression equations"),
(r"\(\mathrm{Cov}(e^{L}_{t+1}, e^{D}_{t+1})\)", "The covariance of the two residuals in the same wave: the curved double-headed arrows at T2 and T3 in the path diagram. It stands for \"shared change that happens at the same time but cannot be explained by the previous wave\""),
]) + r"""
<h4>How do you read a standardized coefficient?</h4>
<p>If \(d = 0.13\), read it as: <i>of two people with the same T1 depression, the one whose T1 loneliness is 1 standard deviation higher has a predicted T2 depression that is on average 0.13 standard deviations higher.</i> "Of two people with the same …" is the plain-language version of "controlling for."</p>
<h4>How many paths do three waves have?</h4>
<p>Two variables, three waves: T1→T2 has 2 autoregressive + 2 cross-lagged paths, T2→T3 another 4, so 8 regression paths in all; add the T1 correlation and the T2 and T3 residual correlations, 3 double-headed arrows. In general: with k variables, each time interval needs k equations, each with k predictors, so each interval has \(k \times k\) coefficients. That is where the \(p\times p\) coefficient matrix of a CLPN comes from.</p>
""" + TIP("Connection to calculus:", "If you remember partial derivatives, the cross-lagged coefficient \\(d\\) is \\(\\partial\\,\\mathbb{E}[\\text{Depression}_{t+1}] / \\partial\\,\\text{Loneliness}_t\\): hold \\(\\text{Depression}_t\\) fixed and let only \\(\\text{Loneliness}_t\\) change by one unit; how much does the prediction change? If you don't remember, that's fine: \"holding the other variables constant\" is all it means."),
code=r"""
<p>Every course script starts with <code>source("R/_setup.R")</code>: it sets the working directory to the course folder, defines the item names <code>lone_items</code> (4 loneliness items) and <code>dep_items</code> (5 depression items), and provides the data-loading function <code>read_course_data()</code>. The data, <code>data/clpn_sim_wide.csv</code>, are a simulated three-wave panel with N = 800; variable names look like <code>lone1_t1</code> (loneliness item 1, wave 1).</p>
""" + CODE(r"""
source("R/_setup.R")            # Shared setup: paths, item names, fonts, helper functions
dat <- read_course_data()       # Read data/clpn_sim_wide.csv (N = 800)
z <- function(x) as.numeric(scale(x))   # Standardize to z scores
for (t in 1:3) {                # Total score of each construct at each wave, standardized
  dat[[paste0("lone", t)]] <- z(rowSums(dat[, paste0(lone_items, "_t", t)]))
  dat[[paste0("dep", t)]]  <- z(rowSums(dat[, paste0(dep_items, "_t", t)]))
}
# Each T2 variable = one regression equation
coef(lm(lone2 ~ lone1 + dep1, data = dat))   # a (lone1) and c (dep1)
coef(lm(dep2  ~ dep1 + lone1, data = dat))   # b (dep1) and d (lone1)
""", "Core of R/L5-1.R (with line-by-line comments)") + r"""
<p><b>How to read it:</b> <code>paste0(lone_items, "_t", t)</code> builds column names such as <code>"lone1_t1" "lone2_t1" …</code>; <code>rowSums()</code> adds up each person's 4 loneliness items; <code>lm(y ~ x1 + x2)</code> is the multiple regression from Module 3, and the tilde <code>~</code> reads "is predicted by."</p>
""" + TIP("Actual results on the course data:", "<code>lone2 ~ lone1 + dep1</code> gives a ≈ 0.607, c ≈ 0.016; <code>dep2 ~ dep1 + lone1</code> gives b ≈ 0.539, d ≈ 0.128. So in this simulated data, \"loneliness T1 → depression T2\" is clearly larger than the reverse. (These numbers are exactly the same as lavaan's standardized results in the next lesson, because the regression part of a one-interval CLPM is just two regressions.)") + r"""
<h4>Try changing it</h4>
<ol><li>Drop <code>dep1</code> from the second equation and write only <code>lm(dep2 ~ lone1, dat)</code>. What does the <code>lone1</code> coefficient become, starting from about 0.13? Why does it get so much larger? (The answer is in Exercise 2.)</li>
<li>Write out T2→T3 as well: <code>lm(dep3 ~ dep2 + lone2, dat)</code>, and check whether d is similar in the two intervals.</li></ol>
""",
quiz=[
("In a CLPM, what is the path \"depression T1 → depression T2\" called?",
 ["Cross-lagged path", "Autoregressive path", "Within-wave correlation", "Residual"],
 1,
 ["A cross-lagged path connects different variables at different times; this path is a variable predicting itself.",
  "Autoregressive = a variable predicting itself; it stands for stability.",
  "A within-wave correlation connects two variables in the same wave and is a double-headed arrow.",
  "A residual is the part an equation does not explain, not a path."]),
("Why must a cross-lagged path control for the autoregressive path?",
 ["To make the model fit look better",
  "Because the two variables are correlated at T1 and each is stable; without the control, the cross-lagged path \"borrows\" the association that stability produces",
  "Because lavaan requires it",
  "To turn the coefficients into standardized coefficients"],
 1,
 ["The control removes \"borrowed\" association; it has nothing to do with how good the fit indices look.",
  "Correct: at heart this is omitted-variable bias.",
  "lavaan lets you leave out the autoregressive paths; the control is required by the statistical logic, not by the software.",
  "Standardization only changes units; it has nothing to do with which variables are controlled in the equation."]),
("c (depression → loneliness) is significant and d (loneliness → depression) is not. What is the most appropriate conclusion?",
 ["Depression causes loneliness",
  "Loneliness does not affect depression",
  "In this sample and at this lag, T1 depression adds to the prediction of T2 loneliness; the other direction was not supported, and the difference between the two needs its own test",
  "The effects in the two directions differ significantly"],
 2,
 ["A CLPM only gives evidence of prediction over time; it cannot say \"causes\" directly.",
  "Not significant ≠ absent: the sample size or the lag may simply be unsuitable.",
  "Correct: careful wording, and it notes that \"one significant, one not\" is not the same as \"significantly different.\"",
  "One path significant and the other not does not show that they differ significantly; you need a constraint test to conclude that."]),
("What does the curved double-headed arrow ↔ mean in a path diagram?",
 ["Regression", "Correlation / covariance", "Causation", "Latent variable"],
 1,
 ["Regression (prediction) is a single-headed arrow.",
  "Correct.",
  "Path diagrams have no special symbol for \"causation\"; a single-headed arrow also means only regression.",
  "A latent variable is drawn as an ellipse, not as a kind of arrow."]),
("What is the main difference between a CLPM and a CLPN?",
 ["A CLPM doesn't need longitudinal data",
  "The variables of a CLPM are construct total scores; the nodes of a CLPN are single items / symptoms",
  "A CLPN has no autoregressive paths",
  "A CLPN can only use two time points"],
 1,
 ["Both need panel data from the same people.",
  "Correct: a CLPN takes the CLPM \"down to the item level.\"",
  "A CLPN has autoregressive paths too: the diagonal of the coefficient matrix holds the autoregressive edges.",
  "A CLPN can use more than two waves (Lesson 7.5)."]),
],
ex=[
("Draw the full three-wave CLPM", "Basic",
 r"""<p>On paper, draw the full path diagram for three waves of "loneliness ↔ depression," label a, b, c, d (you can write a₁, a₂, … for the two intervals), and explain each kind of path in one sentence of social work language.</p>""",
 r"""<p>There should be 6 boxes (loneliness T1/T2/T3, depression T1/T2/T3); 4 horizontal autoregressive arrows; 4 diagonal cross-lagged arrows; and 3 curved double-headed arrows (the T1 correlation and the T2 and T3 residual correlations).</p>
<ul><li><b>Autoregressive:</b> "Residents who were lonelier than others six months ago are usually still lonelier than others six months later."</li><li><b>Cross-lagged (loneliness → depression):</b> "Among residents who were equally depressed six months ago, those who were lonelier then have higher depression scores six months later."</li><li><b>Residual correlation:</b> "Over the same period, people whose loneliness rose more than expected also tended to have depression that rose more than expected."</li></ul>"""),
("What happens if you leave out the autoregressive path", "Understanding",
 r"""<p>In R, compare the coefficient of <code>lone1</code> in <code>lm(dep2 ~ lone1, dat)</code> and in <code>lm(dep2 ~ dep1 + lone1, dat)</code>. Why is the first one so much larger?</p>""",
 r"""<p>In the first model, the coefficient of <code>lone1</code> is close to "the correlation of loneliness T1 with depression T2," about 0.30 in this data (standardized and with a single predictor, the coefficient equals the correlation r(loneliness T1, depression T2) = 0.296, as in Lesson 4.3); with <code>dep1</code> added it drops to about 0.13. The reason: loneliness T1 is correlated with depression T1, and depression T1 strongly predicts depression T2. Without controlling for <code>dep1</code>, all of this indirect, "borrowed" association is credited to <code>lone1</code>. That is why a cross-lagged path must control for the autoregressive path.</p>"""),
("Wording practice", "Writing",
 r"""<p>Rewrite this sentence so it is accurate: "The study found that loneliness makes community residents' depression worse."</p>""",
 r"""<p>Suggested version: "After controlling for baseline depression, residents with higher loneliness scores at T1 also had higher depression scores six months later (β = 0.13). This prediction over time is consistent with the hypothesis that loneliness may worsen depression, but other explanations, such as unmeasured common causes, cannot be ruled out." Key points: say what was controlled, give the direction and the lag, and use "predicts / is consistent with" instead of "causes."</p>"""),
],
summary=[
    "CLPM = one multiple regression equation for each variable at the later wave; autoregressive paths stand for stability, and cross-lagged paths for \"how much the other variable's past adds, once your own past is controlled.\"",
    "Path diagram symbols: box = observed variable, ellipse = latent variable, single arrow = regression, double arrow = correlation.",
    "A cross-lagged path must control for the autoregressive path; otherwise it picks up \"borrowed\" association from the T1 correlation and from stability.",
    "A CLPN breaks the total-score boxes of a CLPM into item nodes: p items → p × p coefficients."
],
refs=["Hamaker, E. L., Kuiper", "Rosseel, Y. (2012)"],
)

# 5.2 "Actual output": standardized solution with standardized CIs (standardizedSolution).
# Printed at the end of R/L5-2.R; if not yet in the log (R/L5-2.R has not been rerun), falls back to the four cross-lagged paths in the solution log.
def _l52_std_out():
    try:
        std = RLOG("L5-2_log.txt", "Standardized solution (standardizedSolution)", 10)
        src = "R/output/L5-2_log.txt"
    except StopIteration:
        std = RLOG("sol_L5-2_log.txt", "dep1 → lone2", 4)
        src = "R/output/sol_L5-2_log.txt (R/solutions/L5-2_solution.R)"
    fitm = RLOG("L5-2_log.txt", "chisq     df pvalue", 2)
    return OUT(std + "\n" + fitm, "Actual output excerpt: " + src)

L["5.2"] = dict(
lead=r"""<p>The previous lesson took apart one time interval of the CLPM with two <code>lm()</code> calls. This lesson fits the whole three-wave model at once with the structural equation modeling (SEM) package lavaan, shows you how to read model fit indices, and explains why many CLPN papers don't report them.</p>""",
intuition=r"""
<h3>Why not just keep using lm()?</h3>
<p>Four <code>lm()</code> calls also give you the 8 paths of a three-wave CLPM, but with three drawbacks: (1) they cannot estimate the residual correlations at the same time; (2) they cannot test whether "the model as a whole agrees with the data"; (3) they make it awkward to add constraints (e.g., "the paths are equal in both intervals") or to handle missing data. SEM estimates all the equations together and fits a "model-implied covariance matrix" to the "sample covariance matrix."</p>
<h3>What does "model fit" mean?</h3>
<p>Suppose you give the model only certain paths (e.g., T1 loneliness is not allowed to predict T3 depression directly). From these paths, the model "works out" what the covariances among all the variables should be. Compare these with the actual sample covariances: the smaller the difference, the better the """ + T("model fit") + r""". Poor fit means your model has missed important structure in the data.</p>
""" + KEY("Analogy:", "A model is like a \"simplified map,\" and the fit indices tell you \"how far the map is from the actual terrain.\" A map with no simplification at all (a saturated model) always fits perfectly, but it tells you nothing.") + r"""
<h3>Four common fit indices</h3>
""" + TABLE(["Index", "Full name", "Intuition", "Common cutoff"], [
    ["χ² test", "chi-square test", "Significance test of \"the model fits perfectly\"; almost always significant in large samples", "p > .05 means no significant misfit (of limited use when N is large)"],
    ["CFI / TLI", "comparative / Tucker–Lewis fit index", "How much better the model is than a baseline model in which no variables are correlated", "≥ .95 good, ≥ .90 acceptable"],
    ["RMSEA", "root mean square error of approximation", "Average misfit per degree of freedom; takes the model's parsimony into account", "≤ .06 good, > .10 poor"],
    ["SRMR", "standardized root mean square residual", "Average size of the differences between observed and model-implied correlations", "≤ .08 good"]
]) + r"""
""" + WARN("Note:", "These cutoffs (often called the \"Hu & Bentler criteria\") are rules of thumb, not laws. Different indices can contradict each other, and good fit does not mean the model is \"right,\" only that \"the data have not clearly rejected it.\"") + r"""
<h3>Actual results on the course data</h3>
<p>The companion script <code>R/L5-2.R</code> gives, on the simulated data with N = 800: χ²(4) = 67.99, p &lt; .001; CFI = .962; TLI = .856; RMSEA = .141; SRMR = .031. The indices disagree: CFI and SRMR look acceptable, but TLI and RMSEA are poor. Why? One important reason is that the simulated data contain strong, stable personal traits, and the standard CLPM has no way to express "a direct similarity between T1 loneliness and T3 loneliness other than through T2." The RI-CLPM in Lesson 5.3 was designed for exactly this, and it fits significantly better.</p>
<h3>Equality constraints: are the paths the same in both intervals?</h3>
<p>If T1→T2 and T2→T3 have the same lag and people are at a similar stage of life, you might assume that the autoregressive and cross-lagged paths are equal in the two intervals. This is called an """ + T("equality constraint") + r""". Benefits: fewer parameters, more stable estimates, simpler interpretation ("every six months …"). Cost: if the two intervals really differ, the constraint makes the fit worse. You can compare the "constrained" and "unconstrained" models (a nested-model χ² difference test) and let the data tell you whether the constraint is reasonable.</p>
<p>In lavaan, giving two paths the same "label" constrains them to be equal: <code>dep2 ~ d*lone1</code> and <code>dep3 ~ d*lone2</code> both use the label <code>d</code>.</p>
""" + NOTE("Connection to CLPN:", "The simplified \"LASSO-only\" CLPN that this course teaches as its main approach is not an SEM but a set of separate LASSO regressions, so it has <b>no</b> overall fit indices such as CFI or RMSEA; nor does it constrain T1→T2 and T2→T3 to be equal by default. Instead it estimates them separately and compares how well they \"replicate\" (Lesson 7.5). The full procedure recommended by Wysocki et al. (2025) is different: it refits the model selected by LASSO in lavaan without a penalty, so it <b>does</b> have χ², CFI, TLI and RMSEA, and it can test equality over time with nested χ² tests. <code>R/L7-5b.R</code> in Lesson 7.5 demonstrates this on the course data: χ²(91) = 164.70, CFI = .988, RMSEA = .032. When you read a CLPN paper, first check which of the two the authors used."),
math=r"""
<p>The core idea of SEM in one mathematical sentence: find the parameters \(\theta\) that make the model-implied covariance matrix \(\Sigma(\theta)\) as close as possible to the sample covariance matrix \(S\).</p>
""" + MATH(r"\hat\theta = \arg\min_{\theta}\ F\big(S,\ \Sigma(\theta)\big)") + SYM([
(r"\(\theta\)", "Greek letter theta: the set of all parameters to estimate (path coefficients, variances, covariances)"),
(r"\(S\)", "Sample covariance matrix: computed directly from the data"),
(r"\(\Sigma(\theta)\)", "Capital sigma: the covariance matrix the model \"works out\" for given parameters"),
(r"\(F(\cdot)\)", "Discrepancy function. With maximum likelihood (ML) estimation, it measures the gap between S and Σ(θ)"),
(r"\(\arg\min\)", "\"The parameter value that makes … smallest\""),
]) + r"""
<h4>Where do the degrees of freedom (df) come from?</h4>
<p>6 observed variables have \(6\times7/2 = 21\) variances and covariances (plus 6 means = 27 pieces of "known information"). The model estimates 23 parameters (lavaan prints "Number of model parameters 23," means/intercepts included), so \(df = 27 - 23 = 4\). The more df, the more "parsimonious" the model, and the more chances the data have to reject it.</p>
<h4>The RMSEA formula (for reference)</h4>
""" + MATH(r"\mathrm{RMSEA}=\sqrt{\max\!\left(\frac{\chi^2-df}{df\,(N-1)},\,0\right)}") + r"""
<p>With χ² = 67.99, df = 4, N = 800: \(\sqrt{(67.99-4)/(4\times799)} = \sqrt{0.0200}\approx 0.141\), matching the output. You can see that RMSEA is large when χ² is much larger than df, and that the larger N is, the smaller the RMSEA for the same χ².</p>
""",
code=CODE(r"""
source("R/_setup.R")
library(lavaan)
dat  <- read_course_data()
wide <- data.frame(id = dat$id)
for (t in 1:3) {                                   # Construct totals (raw scores, not standardized)
  wide[[paste0("lone", t)]] <- rowSums(dat[, paste0(lone_items, "_t", t)])
  wide[[paste0("dep", t)]]  <- rowSums(dat[, paste0(dep_items, "_t", t)])
}
clpm <- '
  lone2 ~ lone1 + dep1      # ~  reads "is predicted by" (regression)
  dep2  ~ dep1  + lone1
  lone3 ~ lone2 + dep2
  dep3  ~ dep2  + lone2
  lone1 ~~ dep1             # ~~ reads "is correlated with" (covariance)
  lone2 ~~ dep2             # At T2 and T3 these are residual covariances
  lone3 ~~ dep3
'
fit <- sem(clpm, data = wide, missing = "fiml")   # FIML: full information maximum likelihood, handles missing data
summary(fit, standardized = TRUE, fit.measures = TRUE)
fitMeasures(fit, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr"))
ssol <- standardizedSolution(fit)                 # Standardized estimates + their own SEs and 95% CIs
ssol[ssol$op == "~", c("lhs", "op", "rhs", "est.std", "se", "ci.lower", "ci.upper", "pvalue")]
""", "Core of R/L5-2.R") + r"""
<p><b>Reading the output:</b> the <code>Regressions:</code> part of <code>summary(..., standardized = TRUE)</code> has a <code>Std.all</code> column (fully standardized coefficients), but the <code>Std.Err</code> and <code>P(&gt;|z|)</code> on the same row, and the <code>ci.lower</code> / <code>ci.upper</code> from <code>parameterEstimates()</code>, all belong to the <b>unstandardized</b> estimates (raw-score units). If you put an unstandardized interval next to a standardized coefficient, readers will think "the interval for 0.607 is [0.524, 0.634]," although the two are not on the same scale at all. So when you report β, use <code>standardizedSolution()</code>: it recomputes the standard error, z test and 95% CI for the standardized estimate <code>est.std</code> with the delta method, so all numbers are on the same scale as β. Excerpt of the results on the course data:</p>
""" + _l52_std_out() + r"""
<p class="muted" style="font-size:.88rem"><code>est.std</code> and <code>Std.all</code> are the same number. The p values of the standardized and unstandardized estimates are usually very close but not identical, because their standard errors are computed separately.</p>
<h4>Adding equality constraints and comparing</h4>
""" + CODE(r"""
clpm_eq <- '
  lone2 ~ a*lone1 + c*dep1
  dep2  ~ b*dep1  + d*lone1
  lone3 ~ a*lone2 + c*dep2      # Same label = constrained to be equal
  dep3  ~ b*dep2  + d*lone2
  lone1 ~~ dep1; lone2 ~~ dep2; lone3 ~~ dep3
'
fit_eq <- sem(clpm_eq, data = wide, missing = "fiml")
anova(fit_eq, fit)     # Nested-model χ² difference test: significant → the constraints make the fit clearly worse
""", "For the exercise: equality-constrained version (run it yourself)"),
quiz=[
("In lavaan syntax, what do <code>~</code> and <code>~~</code> mean?",
 ["Correlation; regression", "Regression; correlation (covariance)", "Latent variable definition; regression", "Mean; variance"],
 1,
 ["The wrong way round: <code>~</code> is regression, <code>~~</code> is covariance.",
  "Correct: <code>y ~ x</code> is a regression, <code>x ~~ y</code> a covariance.",
  "A latent variable is defined with <code>=~</code>, not <code>~</code>.",
  "A mean is written <code>x ~ 1</code> and a variance <code>x ~~ x</code>; <code>~</code> and <code>~~</code> themselves mean regression and covariance."]),
("What does RMSEA = 0.141 tell you?",
 ["The model fits very well",
  "The model fits poorly (> .10) and has probably missed important structure",
  "The cross-lagged paths are significant",
  "The sample is too small"],
 1,
 ["Only RMSEA ≤ .06 is usually considered good, and .141 is above .10.",
  "Correct; in this data, what was missed is mainly the stable traits (see 5.3).",
  "Overall fit indices have nothing to do with whether a single path is significant.",
  "N = 800 is not small; and the larger N is, the smaller the RMSEA for the same χ²."]),
("CFI = .962 but TLI = .856. Which statement is correct?",
 ["Looking at CFI alone is enough",
  "When indices disagree, weigh them together and think about what the model may be missing",
  "TLI must have been computed wrongly",
  "It shows that the cross-lagged paths are 0"],
 1,
 ["Picking only the index that suits you hides the model's problems; here RMSEA is also poor.",
  "Correct.",
  "TLI penalizes model complexity more, so it often differs from CFI; that does not mean a calculation error.",
  "Overall fit indices do not test whether any single path is 0."]),
("What is the main reason for putting an \"equality constraint\" on matching paths in T1→T2 and T2→T3?",
 ["To make the p values smaller",
  "When the lags and settings are similar, it is more parsimonious and more stable, and a model comparison can test whether it is reasonable",
  "lavaan requires it",
  "It guarantees a larger CFI"],
 1,
 ["Constraints are for parsimony and stability; choosing a model to get smaller p values is selective reporting.",
  "Correct.",
  "By default lavaan estimates every path freely; whether to constrain is the researcher's decision, and it should be tested.",
  "A constraint removes free parameters, so the fit usually gets slightly worse or stays the same; CFI does not necessarily increase."]),
("Many CLPN papers don't report CFI / RMSEA. What is the most likely reason?",
 ["Item-level data have no covariance matrix",
  "They use the simplified \"LASSO-only\" version: separate nodewise LASSO regressions, with no re-estimation of the model as one SEM, so there are no overall fit indices; papers that use the full procedure of Wysocki et al. (2025) (refitting in lavaan) do report χ² / CFI / TLI / RMSEA",
  "A CLPN always fits perfectly",
  "No CLPN can ever have fit indices"],
 1,
 ["Items have a covariance matrix too; the SEM refit in the full procedure computes fit indices at exactly the item level.",
  "Correct. The simplified version chooses λ by cross-validation / EBIC and assesses stability with the bootstrap; the full procedure has overall fit indices after the SEM refit and can test equality over time with nested χ² tests (Lesson 7.5, R/L7-5b.R).",
  "Separate nodewise LASSO regressions have no overall fit test, so \"always perfect\" makes no sense; and the fit after the full procedure's refit can also be poor.",
  "The SEM refit in the full procedure does give these indices (7.5)."]),
],
ex=[
("Reporting in APA style", "Basic",
 r"""<p>Using the actual output above, write two sentences in APA style: one reporting the model fit, one reporting the cross-lagged path "loneliness T1 → depression T2."</p>""",
 r"""<p>Suggested version: "The fit indices of the CLPM were inconsistent, χ²(4) = 67.99, p &lt; .001, CFI = .962, TLI = .856, RMSEA = .141, SRMR = .031, suggesting that the model may have omitted stable individual differences. Controlling for T1 depression, T1 loneliness significantly and positively predicted T2 depression (β = .13, 95% CI [.07, .19], p &lt; .001)." Note: give fit indices to three decimals without a leading zero (the APA convention for statistics that cannot exceed 1), and use the standardized estimate for β.</p>"""),
("RMSEA and degrees of freedom by hand", "Understanding",
 r"""<p>(1) Explain why this model has df = 4. (2) If the same model gave the same χ² = 67.99 in a sample of N = 200, what would the RMSEA be? What does that show?</p>""",
 r"""<p>(1) 6 variables give 21 variances/covariances + 6 means = 27 pieces of information; the model estimates 23 parameters (6 intercepts/means, 8 regressions, 2 T1 variances, 4 residual variances, 3 covariances), so 27 − 23 = 4. (2) \(\sqrt{63.99/(4\times199)}\approx 0.284\). The same χ² means much worse misfit in a small sample; conversely, χ² easily becomes significant in a large sample, so you can't rely on the p value of χ² alone.</p>"""),
("Testing the equality constraints", "Hands-on",
 r"""<p>Run the "equality-constrained version" code above, report the result of <code>anova(fit_eq, fit)</code>, and decide whether the paths can be constrained to be equal across the two intervals.</p>""",
 r"""<p>Decision rule: if the χ² difference test is not significant (p &gt; .05), the constraints did not make the fit clearly worse, and you can use the more parsimonious equal-paths model; if it is significant, at least one kind of path differs between the intervals, and you should report the unconstrained results and discuss why (e.g., different lags, a change in developmental stage). You can also look at AIC/BIC (smaller is better). Results on the course data (end of the solution script <code>R/solutions/L5-2_solution.R</code>, log <code>R/output/sol_L5-2_log.txt</code>): Δχ²(4) = 4.87, p = .301; both AIC (23196) and BIC (23285) of the equality model are smaller than those of the unconstrained model (23199, 23306). So you can use the equality model: the paths do not differ significantly between the two intervals. (The equality model itself still fits poorly, χ²(8) = 72.85, RMSEA = .101, again because the stable traits are missing; see 5.3.)</p>"""),
],
summary=[
    "SEM fit = how close the model-implied covariance Σ(θ) is to the sample covariance S.",
    "Common indices: χ², CFI/TLI (≥ .95), RMSEA (≤ .06), SRMR (≤ .08); these are rules of thumb and must be weighed together.",
    "The CLPM on the course data: RMSEA = .141, TLI = .856, a sign that stable traits were omitted.",
    "Equality constraint = give paths the same label; a nested-model χ² difference test shows whether it is reasonable.",
    "The LASSO-only CLPN has no overall fit indices; it \"makes its case\" through the choice of λ and bootstrap stability. (The full procedure of Wysocki et al., 2025, does give fit indices after its unpenalized SEM refit.)"
],
refs=["Rosseel, Y. (2012)", "Hamaker, E. L., Kuiper"],
)
