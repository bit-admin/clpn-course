# -*- coding: utf-8 -*-
# Reading pack materials/reading.html. Links (DOIs) only, no PDFs.
# All DOIs were verified against api.crossref.org/works/<doi> on 2026-10-18 for title, journal, volume/issue/pages and authors; re-check when you change an entry.
# Exception: The Crossref record for Wysocki et al. (2025) omits the 5th author, Rhemtulla (listed on the journal page, and the corresponding author); cited as on the journal page.
READING = [
 ("Getting started: what is a CLPN?", [
  ("Wysocki, A., McCarthy, I., van Bork, R., Cramer, A. O. J., &amp; Rhemtulla, M. (2025). Cross-lagged panel networks. <i>advances.in/psychology, 2</i>, e739621.", "10.56296/aip00037", "CC BY 4.0, open access",
   "Why do the authors say that CLPN edges are \"regression coefficients\" rather than \"correlations\"? What question does an autoregressive edge answer, and what question does a cross-lagged edge answer?", ["7.1", "7.2"]),
  ("Epskamp, S., Borsboom, D., &amp; Fried, E. I. (2018). Estimating psychological networks and their accuracy: A tutorial paper. <i>Behavior Research Methods, 50</i>(1), 195–212.", "10.3758/s13428-017-0862-1", "CC BY 4.0, open access",
   "What question does the edge-weight bootstrap answer, and what question does the case-dropping bootstrap answer? Where do the CS-coefficient lines of 0.25 and 0.5 come from?", ["8.2", "8.3"]),
 ]),
 ("Empirical examples: how to write up a CLPN", [
  ("Funkhouser, C. J., Chacko, A. A., Correa, K. A., Kaiser, A. J. E., &amp; Shankman, S. A. (2021). Unique longitudinal relationships between symptoms of psychopathology in youth: A cross-lagged panel network analysis in the ABCD study. <i>Journal of Child Psychology and Psychiatry, 62</i>(2), 184–194.", "10.1111/jcpp.13256", "subscription journal (available through a university library)",
   "How do the authors handle replication across the two intervals T1→T2 and T2→T3? Which stability indices do they use? Does the conclusion avoid causal language?", ["9.1"]),
  ("Grygiel, P., Opozda-Suder, S., &amp; Dolata, R. (2026). The longitudinal interplay between loneliness and depressive symptoms during late childhood: Cross-lagged panel network analyses. <i>European Journal of Investigation in Health, Psychology and Education, 16</i>(6), 78.", "10.3390/ejihpe16060078", "CC BY 4.0, open access",
   "The sample comes from the NLSY79 Children and Young Adults survey (NLSY79-CY): N = 4,333 children aged 10–12, with only two time points. How are the item-level relationships between loneliness and depression similar to, and different from, the structure of the course's simulated data? With only two waves, what can the authors test and what can they not (for example, can they check replication in T2→T3)? How does the age of the sample affect how far the conclusions generalize?", ["9.1", "10.3"]),
  ("Fried, E. I., Papanikolaou, F., &amp; Epskamp, S. (2022). Mental health and social contact during the COVID-19 pandemic: An ecological momentary assessment study. <i>Clinical Psychological Science, 10</i>(2), 340–354.", "10.1177/21677026211017839", "CC BY 4.0, open access",
   "How do the questions that intensive longitudinal (EMA) data answer differ from those of three-wave panel data? What does \"within-person\" mean here?", ["5.3", "7.5"]),
 ]),
 ("Model critique: within-person vs. between-person", [
  ("Hamaker, E. L., Kuiper, R. M., &amp; Grasman, R. P. P. P. (2015). A critique of the cross-lagged panel model. <i>Psychological Methods, 20</i>(1), 102–116.", "10.1037/a0038889", "subscription journal",
   "Why do stable individual differences make cross-lagged coefficients \"look like\" effects? What does the RI-CLPM add? What does this mean for how you interpret a CLPN?", ["5.3", "7.5"]),
 ]),
 ("Measurement invariance (optional Lesson 7.6)", [
  ("Putnick, D. L., &amp; Bornstein, M. H. (2016). Measurement invariance conventions and reporting: The state of the art and future directions for psychological research. <i>Developmental Review, 41</i>, 71–90.", "10.1016/j.dr.2016.06.004", "subscription journal",
   "What does each of configural, metric (weak) and scalar (strong) invariance constrain? How are the model comparisons usually reported in papers?", ["7.6"]),
  ("Cheung, G. W., &amp; Rensvold, R. B. (2002). Evaluating goodness-of-fit indexes for testing measurement invariance. <i>Structural Equation Modeling, 9</i>(2), 233–255.", "10.1207/S15328007SEM0902_5", "subscription journal",
   "Why look at ΔCFI instead of the chi-square difference test? What is the basis for the ΔCFI ≤ 0.01 line?", ["7.6"]),
  ("Chen, F. F. (2007). Sensitivity of goodness of fit indexes to lack of measurement invariance. <i>Structural Equation Modeling, 14</i>(3), 464–504.", "10.1080/10705510701301834", "subscription journal",
   "What cut-offs are recommended for ΔRMSEA and ΔSRMR? How does sample size affect them?", ["7.6"]),
 ]),
 ("Group comparison and sample size (optional Lesson 7.7, advanced)", [
  ("van Borkulo, C. D., van Bork, R., Boschloo, L., Kossakowski, J. J., Tio, P., Schoevers, R. A., Borsboom, D., &amp; Waldorp, L. J. (2023). Comparing network structures on three aspects: A permutation test. <i>Psychological Methods, 28</i>(6), 1273–1285.", "10.1037/met0000476", "subscription journal",
   "Which three aspects does the Network Comparison Test (NCT) test? How should you set the number of permutations and the correction for multiple comparisons?", ["7.7"]),
  ("Constantin, M. A., Schuurman, N. K., &amp; Vermunt, J. K. (2026). A general Monte Carlo method for sample size analysis in the context of network models. <i>Psychological Methods, 31</i>(3), 385–405.", "10.1037/met0000555", "APA open access",
   "Why does the sample size for a network model have to be estimated by repeated simulation? How is \"power\" defined here?", ["7.6", "7.7"]),
 ]),
 ("Reporting standards", [
  ("Burger, J., Isvoranu, A.-M., Lunansky, G., Haslbeck, J. M. B., Epskamp, S., Hoekstra, R. H. A., Fried, E. I., Borsboom, D., &amp; Blanken, T. F. (2023). Reporting standards for psychological network analyses in cross-sectional data. <i>Psychological Methods, 28</i>(4), 806–824.", "10.1037/met0000471", "subscription journal",
   "These standards are for cross-sectional networks. Which items can you use directly for a CLPN, and which need additions (for example, the time interval and autoregression)?", ["9.3", "10.3"]),
 ]),
]
def _reading_body():
    out = sec("how", "How to read", """<ul><li>This page gives <b>links only</b> (DOIs), no PDFs. Papers marked "open access" can be downloaded directly; for subscription journals, go through your university library, or look for the authors' own copy on their homepage or a preprint server.</li>
<li>Each paper comes with a <b>reading question</b> and companion lessons. Finish the companion lessons first, then read with the question in mind. You don't need to follow every formula; it is enough if you can answer the question in your own words.</li>
<li>When you finish, write three sentences in your <a href="study_log.html">study log</a>: what question the paper answers, what method it uses, and what it suggests for your capstone project.</li></ul>""")
    n = 0
    for gi, (h, items) in enumerate(READING):
        lis = ""
        for cite, doi, acc, q, les in items:
            n += 1
            lis += (f'<li><p>{cite} <a href="https://doi.org/{doi}">https://doi.org/{doi}</a> ({acc})</p>'
                    f'<p><b>Reading question: </b>{q}</p><p><b>Companion lessons: </b>{", ".join(L(i) for i in les)}</p></li>')
        out += sec(f"g{gi + 1}", h, f"<ol>{lis}</ol>")
    out += sec("more", "When you write your paper", '<p>For writing practice, see the <a href="writing.html">writing workshop</a>; for every reference cited in the course, see the <a href="../index.html#readings">syllabus · references</a>.</p>')
    return n, out
_n_read, _rb = _reading_body()
page("reading.html", "Paper Reading Pack", f"<p>{_n_read} selected papers grouped by topic, each with a reading question and companion lessons (DOI links; papers marked &ldquo;open access&rdquo; can be downloaded directly).</p>", _rb)
