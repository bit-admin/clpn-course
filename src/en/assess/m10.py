# -*- coding: utf-8 -*-
# M10 module quiz: the capstone project (Week 16, before the project is finalized). The main assessment is the capstone rubric.
LEAD = "<p>Take this before you finalize your capstone project (Week 16 of the standard pace). 4 auto-graded questions, about 10 minutes. The capstone project itself is scored on the <a href=\"../index.html#assessment\">dimensions in the syllabus</a>.</p>"
ITEMS = [
dict(obj="10.1-1", q="""Q: Which of these is a suitable research question for a CLPN capstone project?
- Which depressive symptoms does loneliness cause? || "Cause" is a causal statement; a CLPN cannot answer it.
+ Among older adults living in the community, which loneliness items predict which depressive symptoms six months later? || Correct. Clear, not causal, and matched to what a CLPN can answer.
- Are all depressed people very lonely? || This is a cross-sectional question that mixes up the group and individual levels.
- How can loneliness among older adults be eliminated completely? || This is an intervention question, not a CLPN research question.
E: For how to write a research question, see <a href="../lessons/L10-1.html">10.1</a>."""),
dict(obj="10.1-2", q="""Q: A loneliness item is answered on a 1–4 scale (1 = never, 4 = often). Its wording is positive, "I have many people I can rely on," so it needs reverse scoring. A person answered "2." What is their score after reverse scoring?
N: 3 | 0
H: Reverse scoring on a 1–4 scale: new score = (minimum + maximum) − original score.
E: (1 + 4) − 2 = 3. For reverse scoring, see <a href="../lessons/L10-1.html">10.1</a>."""),
dict(obj="10.1-3", q="""Q: When should the analysis plan (a simple preregistration) be written?
- After you have seen the results and know which are significant || Then it no longer does what a preregistration is for.
+ Before you run the main analysis and see any results || Correct. Any later departure from the plan must be stated in the report.
- After a journal rejects the paper || No.
- Any time, as long as it gets written || The timing is exactly what matters.
E: For what goes into an analysis plan (nodes, λ rule, seed, stability checks, sensitivity analyses) and when to write it, see <a href="../lessons/L10-1.html">10.1</a>."""),
dict(obj="10.3-2", q="""Q: Which sentence best belongs in the Limitations section of a capstone project?
- "This study proved that loneliness is a cause of depression." || This is a causal conclusion, and it is not a limitation.
+ "A standard CLPN does not separate within-person from between-person effects, so these edges do not necessarily represent change processes within individuals." || Correct.
- "This study has no limitations." || Every study has limitations.
- "The results were not significant, which shows the method was flawed." || A nonsignificant result is not in itself a problem with the method.
E: For writing the Limitations section, see <a href="../lessons/L10-3.html">10.3</a> (and 7.5, 9.2)."""),
]
