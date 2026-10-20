# -*- coding: utf-8 -*-
# Module 9: Reading, critique and reporting standards
READ_FIELDS = [
    ["cite", "Paper (authors, year)", "e.g., Funkhouser et al. (2021)"],
    ["sample", "Sample and recruitment", "Size, age, source"],
    ["waves", "Waves and interval", "How many waves? How far apart?"],
    ["nodes", "Nodes", "Which items/symptoms? How many? From which scales?"],
    ["missing", "Missing data and attrition", "Listwise deletion / imputation / FIML? Attrition rate?"],
    ["est", "Estimation method", "Nodewise LASSO? Other? Standardized?"],
    ["lambda", "λ selection rule", "lambda.min / 1se / EBIC? Number of folds?"],
    ["cov", "Covariates", "Which ones? Penalized or not?"],
    ["centr", "Centrality indices", "out-EI / in-EI / bridge?"],
    ["stab", "Stability results", "Number of bootstrap replicates, CS-coefficients"],
    ["rep", "Replication or sensitivity analysis", "T2→T3? Other samples?"],
    ["main", "Authors' main findings (quoted)", "Summarize in the authors' words"],
    ["interp", "Authors' interpretations", "Which statements are interpretation rather than results?"],
    ["over", "Possible overreach", "Causal words? Centrality = target?"],
    ["limit", "The biggest limitation, in my view", "One sentence"]
]

READ_TEXT = """[CLPN paper reading card] {{cite}}
1. Sample: {{sample}}; waves/interval: {{waves}}
2. Nodes: {{nodes}}
3. Missing data/attrition: {{missing}}
4. Estimation: {{est}}; λ rule: {{lambda}}; covariates: {{cov}}
5. Centrality: {{centr}}
6. Stability: {{stab}}; replication/sensitivity: {{rep}}
7. Findings (quoted): {{main}}
8. Authors' interpretation: {{interp}}
9. Possible overreach: {{over}}
10. Biggest limitation: {{limit}}"""

L["9.1"] = dict(
lead=r"""<p>This module turns to reading, evaluating and writing empirical papers. The first step is to read a CLPN paper quickly and systematically: with a structured checklist, pull out the sample, nodes, estimation settings and stability results one by one.</p>""",
intuition=r"""
<h3>Why "structured reading"?</h3>
<p>The first time you read a methods paper, it is easy to drown in terms and numbers and come away remembering only that it "looked impressive". """ + T("Structured reading") + r""" means reading with a fixed checklist and putting each piece of information into its slot as you find it; when you finish, the empty slots show what the paper did not report (or what you did not understand). The items on the checklist follow the content of M4–M8 in order.</p>
<h3>A recommended reading order</h3>
<ol><li><b>Abstract</b> (5 minutes): research question, sample, main findings. First write a one-sentence summary of what you think the authors want to say.</li>
<li><b>Figures and tables</b> (10 minutes): network plot, centrality plot, stability plot. Read them with what you learned in Lessons 7.3 and 8.2–8.3: which edges are thickest? Are autoregressive edges drawn? Does the centrality come with a CS-coefficient?</li>
<li><b>""" + T("Method section") + r"""</b> (20 minutes): fill in the checklist item by item: sample—waves—nodes—missing data—estimation—λ—covariates—centrality—stability.</li>
<li><b>Results and discussion</b> (20 minutes): tell apart three kinds of content (see below) and mark the sentences you think go too far.</li>
<li><b>""" + T("Supplementary materials") + r""" and """ + T("open data & code") + r"""</b> (10 minutes): many key details (the full edge table, the λ rule, stability plots) appear only in the supplement. Check whether there is an OSF link and whether the code can be rerun.</li></ol>
<h3>Three kinds of content: finding, interpretation, overreach</h3>
""" + TABLE(["Type", "How to recognize it", "Example (made up)"], [
["Finding", "You can find a matching number in a results table or figure", "\"The cross-lagged coefficient from T1 loneliness item X to T2 depression item Y was 0.12.\""],
["Interpretation", "The authors' guess at what a finding means, usually with \"may\" or \"suggests\"", "\"This may reflect the role of social withdrawal in the development of depression.\""],
["Overreach", "Goes beyond what the data can support: causal words, intervention advice, generalization", "\"Interventions should therefore target X first to prevent depression.\""]]) + r"""
<p>The next lesson (9.2) lists the most common kinds of overreach systematically.</p>
<h3>This lesson's example: Funkhouser et al. (2021)</h3>
<p>The course uses Funkhouser and colleagues' ABCD study, published in the <i>Journal of Child Psychology and Psychiatry</i>, as its close-reading example. It uses a CLPN to study longitudinal relations among adolescents' psychopathology symptoms in a sample of 4,093 adolescents, and checks whether the results replicate in a later interval (T2→T3). Read it with the reading card below, and take every detail from the original paper (this page does not summarize the paper's specific results, so you come to it without preconceptions).</p>
""" + NOTE("Getting the paper", "The link (DOI) is under \"Further reading\" at the end of the page. If you cannot get the full text through a library, look for a public version on the authors' homepages, an institutional repository or a preprint server (such as PsyArXiv), or email the corresponding author. As you read, copy sentences you do not understand word for word into your notes, and go back to them one by one after you finish the paper.") + r"""
<h3>Interactive reading card</h3>
<p>The reading card below is saved automatically in your browser and generates a copyable "reading card" text as you type, ready to paste into your notes or study log.</p>
""" + WJ("tpl", "CLPN paper reading card (fill it in to generate copyable text)", "read91", {"fields": READ_FIELDS, "text": READ_TEXT}) + r"""
<h3>Matching the paper's figures and tables to course concepts</h3>
""" + TABLE(["What you see in the paper", "Course concept", "Questions to ask"], [
["A network plot with arrows", "7.3 Visualizing a CLPN", "Are autoregressive edges drawn? Is a threshold shown? Is maximum stated?"],
["A table of \"autoregressive / cross-lagged effects\"", "7.1 Autoregressive and cross-lagged", "Are all edges reported? Are they standardized?"],
["\"Out-/in-expected influence\"", "7.4 Out-/in-EI", "Are autoregressive edges excluded? How are communities defined for bridge EI?"],
["\"Case-dropping\", \"CS-coefficient\"", "8.3 CS-coefficient", "Is CS ≥ 0.25? Do the authors interpret only stable indices?"],
["\"Bootstrapped CIs\"", "8.2 Edge accuracy", "Do the authors treat them as significance tests?"],
["\"LASSO\", \"cross-validation\", \"EBIC\"", "6.3 / 7.2 Choosing λ", "lambda.min or 1se? What γ?"],
["\"Replication in T2→T3\"", "7.5 Replication across waves", "What measure of replication? What was the result?"]]) + r"""
""",
math=r"""
<p>The "math" in this lesson is a few quick checks you will use most often when reading papers, to see whether a paper's numbers are consistent.</p>
<h4>1. Counting edges</h4>
""" + MATH(r"\text{max. cross-lagged edges}=p(p-1),\qquad \text{density}=\frac{\#\{\hat\beta_{kj}\neq0,\ k\neq j\}}{p(p-1)}") + r"""
<p>If a paper says "16 nodes, 300 cross-lagged edges estimated", you know at once that this is impossible (at most 16 × 15 = 240).</p>
<h4>2. Ratio of sample size to parameters</h4>
""" + MATH(r"\frac{N}{p}\quad(\text{people per predictor in each regression})") + SYM([
(r"\(N\)", "Sample size used in the analysis (note: may be smaller than the number recruited because of missing data)"),
(r"\(p\)", "Number of nodes = number of predictors in each nodewise regression"),
]) + r"""
<p>There is no accepted hard rule of the kind "N must be at least so many times p". N/p is only a rough number for a quick check while reading: the smaller it is, the less information each nodewise regression has, the larger the λ chosen by cross-validation, the sparser the network and the worse the stability. The course data have N/p = 800/9 ≈ 89; a study with N = 300 and p = 20 has N/p = 15, and its results need extra caution. How large a sample a study really needs depends on what the true network looks like (how strong the edges are, how many there are) and on the question the study asks, and has to be settled by simulation: Constantin, Schuurman and Vermunt (2026) give a general Monte Carlo method for sample size planning in network models, and Lesson 7.6 does a simplified version. So when you read a paper, a small N/p is only a prompt: check whether the authors planned their sample size and whether they report bootstrap intervals and CS-coefficients.</p>
<h4>3. Attrition rate</h4>
""" + MATH(r"\text{attrition rate}=1-\frac{N_{\text{completed all waves}}}{N_{\text{T1}}}") + r"""
<p>When attrition is high (e.g., &gt; 20%) and not dealt with, ask: is dropping out related to baseline symptoms (review Lesson 4.3)?</p>
<h4>4. Reading CS and intervals</h4>
<p>When you see a CS, compare it at once with the 0.25 / 0.5 lines; when you see bootstrap intervals for edges, check at once whether the intervals of the strongest edges overlap and whether they contain 0.</p>
""",
code=r"""
<p>This lesson is mostly reading and has no R script of its own. But there is one very practical R skill: <b>reproducing the numbers in a paper</b>. If the authors share their data and code (OSF), you can check their λ rule, seed and CS-coefficients. Below is a "reproduction check" template, assuming you have downloaded the authors' wide-format data:</p>
""" + CODE(r"""
source("R/_setup.R")
paper <- read.csv("paper_data.csv")             # data shared by the authors (example file name)
t1 <- grep("_t1$", names(paper), value = TRUE)  # find T1 items using the authors' naming convention
t2 <- sub("_t1$", "_t2", t1)                    # the matching T2 items (same order!)
stopifnot(all(t2 %in% names(paper)))
d  <- na.omit(paper[, c(t1, t2)])               # if the authors used listwise deletion
nrow(d)                                         # does it match the N reported in the paper?
set.seed(2026)                                  # if the authors report a seed, use theirs
B  <- clpn_estimate(d[, t1], d[, t2], rule = "lambda.min")   # or the rule the authors used
CL <- cl_only(B)
sum(CL != 0)                                    # compare with the number of edges in the paper
head(edge_list(CL), 10)                         # compare with the paper's table of strongest edges
sort(rowSums(CL), decreasing = TRUE)            # out-EI ranking
""", "Reproduction check template (uses the course's clpn_estimate(); adjust variable names and rule to the paper)") + r"""
""" + TIP("What if you cannot reproduce it?", "Check 4 things first: (1) is the sample the same (missing-data handling)? (2) were the variables standardized? (3) the λ rule and number of folds; (4) the random seed. Even if all of these match, different glmnet or R versions can cause small differences, which is why Lesson 9.3 asks you to report software versions."),
quiz=[
("Which of these is a \"finding\" rather than an \"interpretation\"?",
 ["This may reflect the role of social withdrawal",
  "The cross-lagged coefficient from T1 item A to T2 item B was 0.12",
  "A should therefore be the first target of intervention",
  "A is the core driver of the network"], 1,
 ["This is interpretation: \"may reflect …\" is the authors' guess at what a number means; you will not find this sentence in a results table.",
  "Correct: you can find the matching number in a results table.",
  "This is overreach: it jumps straight from a predictive relationship to intervention advice.",
  "This is overreach: \"core driver\" carries a causal meaning, and nothing is said about the stability of the centrality."]),
("A paper's 16-node CLPN reports 280 cross-lagged edges. What should you do?",
 ["Accept it: with a large sample there can be many edges",
  "Question it: there can be at most 16 × 15 = 240",
  "Accept it: the authors may have counted the autoregressive edges as well",
  "Accept it: lambda.min keeps many edges anyway"], 1,
 ["The maximum number of edges depends only on the number of nodes: at most p(p − 1), whatever the sample size.",
  "Correct.",
  "Even adding the 16 autoregressive edges gives only 256, still short of 280.",
  "The λ rule only decides how many are kept; the maximum is still 240."]),
("Why must you look at the supplementary materials when reading a CLPN paper?",
 ["Results in the supplement are more reliable than in the main text",
  "Key information such as the full edge table, the λ rule and the stability plots is often only in the supplement",
  "Journals require readers to read the supplement",
  "The supplement contains negative results the authors hid in the main text"], 1,
 ["Both are results of the same study and equally credible; the difference is the level of detail.",
  "Correct.",
  "Journals have no such requirement; you read it because the information needed to judge the conclusions is often only there.",
  "Most supplements just hold details that did not fit in the main text; that is not hiding anything. But do check that the conclusions in the main text agree with the numbers in the supplement."]),
("A paper reports a CS of 0.18 for out-EI, yet calls a node the \"core driving symptom\" in the discussion. This is…",
 ["A reasonable interpretation: its out-EI really is the highest in the sample",
  "Overreach: with CS < 0.25 the out-EI ranking should not be interpreted, and \"driving\" implies causation",
  "A finding: its out-EI value is in the table",
  "A replication result"], 1,
 ["CS < 0.25 means this \"highest\" may change after dropping a few cases; and \"driving\" implies causation.",
  "Correct.",
  "The table contains only the out-EI value; \"core driving symptom\" is the authors' reading, which goes beyond the number itself.",
  "This has nothing to do with replication: replication means getting similar results in another interval or sample."]),
("When reproducing someone else's CLPN results, which of these least needs checking?",
 ["Missing-data handling and sample size",
  "The λ rule and the random seed",
  "Whether the items were standardized",
  "Whether the authors used RStudio or another code editor"], 3,
 ["Needs checking: different missing-data handling means different people enter the analysis, and the network changes.",
  "Needs checking: the rule decides how many edges are kept, the seed decides the cross-validation folds, and both change weak edges.",
  "Needs checking: standardizing changes the relative strength of the LASSO penalty and therefore which edges are kept.",
  "Correct: the editor is just an interface for writing code and does not affect the computation; what you need to check are the versions of R and the packages."]),
],
ex=[
("Close reading of Funkhouser et al. (2021)", "Reading", r"""<p>Read the paper closely, fill in all 15 items of the reading card on this page, and prepare a 10-minute talk (suggested: 2 minutes research question, 3 minutes methods, 3 minutes results, 2 minutes your assessment).</p>""",
 r"""<p>Scoring points (for self-assessment): (1) you can state the waves, sample size and nodes accurately; (2) you can state exactly how λ was chosen and how stability was checked (as in the original paper); (3) you can tell the authors' findings from their interpretations; (4) you name at least one concrete limitation, such as "between-person and within-person effects are not separated", "the nodes come from different informants/scales" or "the interval is long", and explain why it affects the conclusions; (5) you do not describe the paper's predictive relationships as causal.</p>"""),
("Consistency check", "Basics", r"""<p>A paper: N = 450, p = 12 nodes, reports "75 nonzero cross-lagged edges, density 0.57". Check whether the density is right and compute N/p.</p>""",
 r"""<p>At most 12 × 11 = 132 edges, and 75/132 ≈ 0.57, so the density checks out. N/p = 37.5, less than half that of the course data (≈ 89). There is no hard standard for N/p, but this value is a reminder to look closely at the bootstrap intervals and CS-coefficients the authors report, and at whether they planned their sample size.</p>"""),
("Three questions for yourself", "Reflection", r"""<p>After reading the paper, write down 3 questions you are still unsure about (the more specific the better). After each, write one sentence: to answer it, which part of the paper do you need, or what would you need to do yourself in R?</p>""",
 r"""<p>Examples of good questions: "The authors used lambda.min rather than 1se; would the strongest cross-construct edge survive with 1se?" "Did the authors' T2→T3 replication use a correlation of edge weights or of centrality?" "Why does the supplement not report a CS for bridge EI?" Avoid vague questions such as "is this paper good?".</p>"""),
],
summary=["Structured reading: read with a checklist; an empty slot = not reported, or not understood.", "Order: abstract → figures and tables → methods → results and discussion → supplement and code.", "Tell apart findings, interpretation and overreach.", "Quick checks: maximum edges p(p−1), N/p, attrition rate, CS thresholds.", "Funkhouser et al. (2021): ABCD study, 4,093 adolescents, with a T2→T3 replication; take the details from the original paper."],
refs=["Funkhouser, C. J.", "Wysocki, A., McCarthy", "Burger, J., Isvoranu", "Constantin, M. A."],
)

L["9.2"] = dict(
lead=r"""<p>Once you can read a paper, the next step is to evaluate it critically. This lesson goes through ten common problems in CLPN papers and shows how to use sensitivity analysis to check whether a conclusion depends on one particular analysis decision. You need to avoid the same problems in your own project.</p>""",
intuition=r"""
<h3>Ten common problems in CLPN papers</h3>
""" + TABLE(["#", "Problem", "How to spot it", "Related lessons"], [
["1", "Causal wording", "\"leads to\", \"drives\", \"acts on\", \"interventions should therefore …\"", "5.4"],
["2", "Mixing up between-person and within-person", "No discussion of stable traits; edges treated as within-person processes", "5.3, 7.5"],
["3", "Over-reading centrality", "Ranking interpreted although CS is not reported or &lt; 0.25; \"central = target\"", "6.5, 8.3"],
["4", "Topological overlap (overlapping item content)", "Two near-synonymous items have a very strong edge and inflate each other's centrality", "This lesson"],
["5", "Arbitrary choice of nodes", "Why these items? Were important variables (such as physical illness) left out?", "This lesson"],
["6", "Low reliability of single items", "Single items have large measurement error, which weakens autoregression and distorts cross-lagged edges", "5.4"],
["7", "Sample too small", "Small N/p; very sparse network; very wide intervals", "6.3, 8.2"],
["8", "Poor handling of missing data and attrition", "Attrition not reported; plain listwise deletion; attrition related to baseline symptoms", "4.3"],
["9", "Interval not justified", "Does the interval suit the process being studied?", "5.4"],
["10", "Undisclosed researcher degrees of freedom", "λ rule, γ, seed, covariates etc. not reported, or it looks like \"tried many and picked the nicest\"", "This lesson"]]) + r"""
<h3>Two new concepts in more depth</h3>
<h4>""" + T("Topological overlap", "item redundancy") + r"""</h4>
<p>If two items ask almost the same thing (for example "I feel lonely" and "I feel lonesome"), the edge between them will be very strong, and their patterns of connections with the other nodes will also be very similar. This is not "two symptoms acting on each other" but "the same thing measured twice". Consequences: (1) the edge between the pair is misread as a dynamic relationship; (2) their centrality is artificially inflated. The <code>goldbricker()</code> function in the networktools package finds item pairs whose patterns of correlation with the other nodes are very similar, to help you decide whether to merge or drop items.</p>
<h4>""" + T("Researcher degrees of freedom") + r"""</h4>
<p>A CLPN involves many decisions that could go either way: lambda.min or 1se? Which γ? Which seed? Covariates or not? Which items? If a researcher tries many combinations and reports only the "nicest-looking" one, the result may be due to chance. The remedy: write an analysis plan in advance (Lesson 10.1) and report a """ + T("sensitivity analysis") + r""": with another reasonable decision, do the main conclusions stay the same?</p>
<h3>Sensitivity checks on the course data (R/L9-2.R)</h3>
""" + TABLE(["Check", "Result", "Meaning"], [
["λ rule: lambda.min / 1se / EBIC", "CL edges 52 / 17 / 31; the strongest edge is dep3 → dep4 under all three; the highest out-EI is lone4 under all three; highest in-EI: dep4 / dep1 / dep4", "The number of edges is very sensitive to the rule; the strongest edge is robust; the top in-EI node changes"],
["Random seed: 20 different seeds", "49 CL edges always nonzero, 12 always 0, 11 \"sometimes there, sometimes not\"", "About 15% of edges depend on the random fold assignment of cross-validation → you must report the seed"],
["Item redundancy: goldbricker()", "Flags 9 item pairs (e.g., lone2 &amp; lone1, dep4 &amp; dep3), all within the same construct", "Limited power to discriminate with 9 nodes (see the note after \"goldbricker parameters\" below); judge by the item wording. In this simulated data set the items were generated by construct, so their similarity comes mainly from the shared trait, not repeated content"]]) + r"""
""" + WARN("Another reminder about out-EI:", "lone4 has the highest out-EI under all three λ rules, which looks \"robust\", but the CS in Lesson 8.3 is only {{V:cs8_out}}, and lone4 does not stand out in either the population target matrix or the within-person truth matrix (Lesson 7.4). In a sensitivity analysis, \"the conclusion does not change\" is not the same as \"the conclusion is correct\": the different λ rules use the same sample and share its sampling error. So look at the sensitivity analysis and the bootstrap stability checks together.") + r"""
<h3>Fried &amp; Cramer (2017): the big questions for network methods</h3>
<p>Fried and Cramer discuss the challenges facing psychopathology network theory and methods systematically, including how nodes are defined and chosen, whether network results replicate across samples, and the distance between a statistical network and a theoretical "causal system". Reading it helps you place CLPN in a wider context: CLPN is a useful tool for description and for generating hypotheses, but it is not a machine that "reads off the causal network". (Take the specific arguments from the original paper.)</p>
<h3>How to structure a review</h3>
<ol><li><b>Overall assessment</b> (2–3 sentences): research question, method, main contribution.</li>
<li><b>Strengths</b> (2 points): specific and sincere, e.g., "reports a T2→T3 replication", "shares the code".</li>
<li><b>Major issues</b> (3 points): each with "what the problem is → why it matters → a concrete suggestion".</li>
<li><b>Minor issues</b>: wording, figures and tables, citations.</li>
<li><b>Tone</b>: address the work, not the people; write "the authors could consider …" rather than "the authors wrongly …".</li></ol>
""",
math=r"""
<h4>1. Why does item redundancy inflate centrality?</h4>
<p>Suppose items A and A′ are nearly identical: \(A' = A + e\), with \(e\) small. The A—A′ edge in the network (partial correlation or cross-lagged) will be large, and the strength/EI of both A and A′ goes up by about \(|w_{AA'}|\). If you merge the two items into one node, this "self-to-self" edge disappears.</p>
<h4>2. Measuring sensitivity to the seed</h4>
""" + MATH(r"\pi_{kj}=\frac{1}{S}\sum_{s=1}^{S}\mathbb{1}\big[\hat\beta^{(s)}_{kj}\neq0\big]") + SYM([
(r"\(S\)", "Number of seeds tried (S = 20 in R/L9-2)"),
(r"\(\hat\beta^{(s)}_{kj}\)", "The edge estimated with the s-th seed"),
(r"\(\pi_{kj}\)", "Proportion of seeds under which the edge is nonzero: 1 = always kept, 0 = always 0, in between = sometimes there, sometimes not"),
]) + r"""
<h4>3. Agreement measures for a sensitivity analysis</h4>
""" + MATH(r"r=\mathrm{cor}\big(\hat\beta^{\text{main}}_{\text{CL}},\ \hat\beta^{\text{alternative}}_{\text{CL}}\big),\qquad \text{Jaccard}=\frac{|E_1\cap E_2|}{|E_1\cup E_2|}") + SYM([
(r"\(E_1, E_2\)", "Sets of nonzero edges in the two analyses"),
(r"\(|E_1\cap E_2|\)", "Number of edges present in both"),
(r"\(\text{Jaccard}\)", "Jaccard similarity coefficient: 0 = completely different, 1 = identical"),
]) + r"""
<p>Reporting whether the main conclusions (strongest edges, centrality ranking, direction between constructs) hold in the alternative analysis means more than reporting an abstract correlation.</p>
<h4>4. A note on repeated CV</h4>
<p>The cross-validation error \(\mathrm{CV}(\lambda)\) itself depends on the random fold split. Repeating the split R times and averaging, \(\overline{\mathrm{CV}}(\lambda)=\frac1R\sum_r \mathrm{CV}_r(\lambda)\), reduces the randomness in choosing λ (at the cost of R times the computation).</p>
""",
code=CODE(r"""
source("R/_setup.R")
suppressPackageStartupMessages(library(networktools))
dat <- read_course_data()
X <- dat[, vars_t(1)]; Y <- dat[, vars_t(2)]
off <- matrix(TRUE, 9, 9); diag(off) <- FALSE
# 1) sensitivity to the λ rule
rules <- c("lambda.min", "lambda.1se", "ebic")
Bs <- lapply(rules, function(r) { set.seed(2026); clpn_estimate(X, Y, rule = r) })
names(Bs) <- rules
sapply(Bs, function(B) sum(cl_only(B) != 0))            # number of CL edges per rule
sapply(Bs, function(B) names(which.max(rowSums(cl_only(B)))))   # top out-EI node
# 2) sensitivity to the random seed
arr <- sapply(1:20, function(s) { set.seed(s); clpn_estimate(X, Y)[off] })
nz  <- rowMeans(arr != 0)
table(cut(nz, c(-.01, 0, .99, 1), labels = c("Always 0", "Intermittent", "Always Nonzero")))
# 3) item redundancy
gb <- goldbricker(dat[, vars_t(1)], p = 0.05, method = "hittner2003",
                  threshold = 0.25, corMin = 0.5)
gb$suggested_reductions
""", "Core of R/L9-2.R") + r"""
<p><b>goldbricker parameters:</b> <code>corMin = 0.5</code> checks only item pairs with correlation ≥ 0.5; <code>threshold = 0.25</code> means that if fewer than 25% of the two items' correlations with the other items differ significantly, the pair is flagged as "possibly redundant" (smaller values = more similar). This is only a prompt; whether to merge depends on item content and theory.</p>
""" + WARN("With few nodes, goldbricker has limited power to discriminate", "<p>Look at the actual output for the course data (<code>R/output/L9-2_log.txt</code>): goldbricker flags 9 item pairs, 5 loneliness pairs and 4 depression pairs, all within one construct and none across constructs. This does not show that all 9 pairs \"ask the same thing\"; the method simply cannot tell them apart with only 9 nodes.</p><p>The reason is how it compares. For a pair of items, it compares only the two items' correlations with the remaining items. With 9 nodes there are only 7 remaining items, so the \"proportion significantly different\" can only take the values 0, 1/7 (≈ 0.14), 2/7 (≈ 0.29) …. A threshold of 0.25 means a pair is flagged if at most 1 of the 7 comparisons is significant. Items of the same construct already have similar patterns of correlation with the remaining items (they share the same latent trait), so almost every pair crosses the line. The fewer the nodes, the fewer \"remaining items\" there are to compare and the lower the power of each comparison, so the tool more easily misreports \"belonging to the same construct\" as \"redundant content\".</p><p>So in a 9-node CLPN, goldbricker's output can only be a starting point: take the flagged pairs back to the item wording, see whether they really ask the same thing (for example \"I feel lonely\" and \"I feel lonesome\"), and decide with theory whether to merge them. The same goes for reading papers: when a study with very few nodes reports \"goldbricker found no redundancy\" or \"found a lot of redundancy\", first ask whether the method can discriminate at all with that few nodes.</p>") + r"""""",
quiz=[
("When two items have nearly the same content, what does a strong edge between them mean?",
 ["The two symptoms strongly influence each other",
  "Most likely the same construct measured twice (topological overlap), which inflates centrality",
  "The network was estimated wrongly",
  "A larger λ is needed"], 1,
 ["This is the common misreading named in this lesson: the same thing measured twice, not two symptoms acting on each other.",
  "Correct.",
  "The estimate itself may be fine: the two items really are highly correlated in the data; the problem is how to interpret the edge.",
  "λ only controls the strength of the penalty; a strong edge caused by overlapping content survives at any reasonable λ."]),
("Why is centrality \"not the same\" as an intervention target?",
 ["The most central node is the most severe symptom and should be treated first",
  "Centrality summarizes statistical association/prediction; it can be affected by unclear direction, overlapping content and instability, and it does not consider whether the node can be changed by intervention",
  "Only betweenness centrality can represent a target",
  "Because EI can be negative"], 1,
 ["Treating centrality as severity is a common misreading: centrality measures association with other nodes, not the average level of a symptom, and the two can be completely different.",
  "Correct.",
  "Betweenness is even less stable in psychological networks (Lesson 6.5), and it is likewise just a summary of statistical associations.",
  "That EI can be negative is a computational property, not the reason centrality cannot serve as a target."]),
("How would you check whether a CLPN conclusion is sensitive to the choice of λ?",
 ["Report only lambda.min, but raise the number of bootstrap replicates to 5,000",
  "Estimate with lambda.min, lambda.1se and EBIC separately and compare whether the main conclusions (strongest edges, centrality ranking, construct direction) hold",
  "Set λ to 0 (equivalent to OLS) and compare with the LASSO result",
  "Re-estimate with 20 different random seeds"], 1,
 ["The bootstrap addresses sampling uncertainty, not whether the conclusion changes under another λ rule.",
  "Correct.",
  "λ = 0 is not a reasonable alternative rule: it keeps every coefficient, so you would be comparing \"regularize or not\", not \"another reasonable choice\".",
  "Plausible but wrong: changing the seed tests the randomness of the cross-validation folds, while the λ rule itself stays the same. It is also a useful sensitivity analysis, but it answers a different question."]),
("With 20 different seeds on the course data, 11 CL edges are \"sometimes there, sometimes not\". What does this show?",
 ["glmnet has a bug",
  "The randomness of the cross-validation folds affects whether weak edges are selected; you must report the seed and interpret weak edges with caution",
  "You should pick the seed with the most edges for the main analysis",
  "The seed only affects weak edges, so it need not be reported"], 1,
 ["Not a bug: cv.glmnet splits the folds at random, and different splits choose slightly different λ.",
  "Correct.",
  "This is exactly the misuse of researcher degrees of freedom: picking the seed after seeing the results.",
  "Plausible but wrong: it does mainly affect weak edges, but precisely because of that, if you do not report the seed, nobody can reproduce your edge count and weak edges."]),
("lone4 has the highest out-EI under all three λ rules, but CS = {{V:cs8_out}}. What is the most appropriate conclusion?",
 ["lone4 is robustly the most important node",
  "Agreement across rules does not mean sampling stability; with a low CS you still should not interpret the out-EI ranking",
  "CS was computed wrongly; go by the sensitivity analysis",
  "Switch to EBIC for the main analysis"], 1,
 ["Agreement across rules is not sampling stability: all three rules use the same sample.",
  "Correct: the different rules share the sampling error of the same sample.",
  "The two checks answer different questions, so the results do not contradict each other, and there is no reason to think CS was computed wrongly.",
  "Changing the main-analysis rule after seeing the results breaks the analysis plan; and under EBIC lone4 also has the highest out-EI, so the CS problem remains."]),
],
ex=[
("Writing a review", "Writing", r"""<p>Pick a published CLPN paper in social work or psychology (for example from the reading pack) and write a 600–800-word review: 2 strengths, 3 major issues and 2 concrete suggestions for revision. At least one major issue should connect to the big questions discussed by Fried and Cramer (2017) (such as how nodes are defined and chosen, whether results replicate, the distance between a statistical network and a causal system).</p>""",
 r"""<p>Example structure: "This paper uses three waves of data and a CLPN to examine longitudinal relations between X and Y symptoms … [Strengths] 1. It reports a T2→T3 replication; 2. It shares the analysis code. [Major issues] 1. The discussion calls the node with the highest out-EI a 'driver' and recommends it as an intervention target, but the CS of out-EI is 0.21 (Supplementary Table S4), below the recommended 0.25; I suggest removing the interpretation of the ranking or scaling back the wording. 2. The effect of stable individual differences on the cross-lagged edges is not discussed; I suggest addressing it in the limitations or adding an analysis that separates within- from between-person effects. 3. Items 3 and 7 are very similar in content and have the largest edge weight, which may reflect overlapping content; I suggest a goldbricker check or a sensitivity analysis with the two items merged. (This point corresponds directly to what Fried and Cramer call 'how nodes are defined and chosen'.) [Suggestions for revision] …"</p>"""),
("Find the problems", "Understanding", r"""<p>Below is a made-up description of results. Find at least 4 problems: "We used a CLPN to analyze 25 items measured twice (2 weeks apart) in 120 community residents. The results show that 'tension' is the core symptom driving the whole network (highest out-EI). The community service center should therefore make tension its first target for intervention."</p>""",
 r"""<p>(1) N = 120, p = 25, N/p ≈ 4.8: the sample is far too small; (2) only two waves, so no replication is possible; (3) no λ rule, seed or stability (CS) reported; (4) "driving" and "core" are causal wording; (5) "should therefore make … its first target" is intervention overreach; (6) 25 items may overlap in content; (7) between-person versus within-person is not discussed; (8) no argument that a 2-week interval suits the process being studied.</p>"""),
("A hands-on sensitivity analysis", "Hands-on", r"""<p>Run R/L9-2.R. Add one more check: estimate with <code>clpn_estimate(…, covariates = dat[, c("gender","age")])</code> and compare whether the 5 strongest edges are the same.</p>""",
 r"""<p>Reference solution <code>R/solutions/L9-2_solution.R</code>: with the covariates, the edge weights barely change (r = 0.997, largest difference 0.018), and the 5 strongest edges are exactly the same (consistent with Lesson 7.5). How to write it: "With gender and age as unpenalized covariates, the 5 strongest cross-lagged edges were identical to the main analysis (correlation of edge weights r = .997)."</p>"""),
],
summary=["Ten problems: causal wording, between- vs within-person, over-reading centrality, topological overlap, choice of nodes, single-item reliability, sample size, missing data, interval, researcher degrees of freedom.", "goldbricker() can flag item pairs whose content/association patterns overlap heavily.", "Sensitivity analysis: λ rule, seed, covariates, redundant items; report whether the main conclusions hold.", "Course data: 11 edges come and go across 20 seeds; agreement across rules ≠ sampling stability.", "Review: strengths → major issues (problem–reason–suggestion) → minor issues; address the work, not the people."],
refs=["Fried, E. I., & Cramer", "Epskamp, S., Borsboom, D., & Fried", "Lucas, R. E. (2023)"],
)
