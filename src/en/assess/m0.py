# -*- coding: utf-8 -*-
# M0 module quiz: the course map and "why learn CLPN"
LEAD = "<p>Take this after Lessons 0.1 and 0.2. 6 questions, about 10 minutes. It checks whether you can see the route through the whole course and the difference between the network view and the \"total-score view.\"</p>"
ITEMS = [
dict(obj="0.1-1", q="""Q: The course teaches statistical foundations (M1) and regression and LASSO (M3) before CLPN (M7). What is the main reason?
- Statistics is easier, so it works as a warm-up || It is not because it is easier, but because you will need it later.
+ Every T2 node in a CLPN is one regularized regression; without regression and LASSO you cannot read CLPN results || Correct. M1 statistics and M3 regression are the "engine parts" of CLPN.
- Journals require descriptive statistics to be reported first || This has nothing to do with the order of the course.
- R can only be installed after you finish statistics || R is learned alongside statistics from Week 2.
E: Each module supplies one skill the final CLPN analysis needs; see the course map in <a href="../lessons/L0-1.html">0.1</a>."""),
dict(obj="0.1-2", q="""Q: Every lesson is laid out in the same order. Which order is correct?
- R Code → Intuition → Exercises → Essential Math → Concept Check || Wrong order.
+ Intuition → Essential Math → R Code → Concept Check → Exercises → Summary || Correct. First build a picture, then write it as formulas, then work hands-on.
- Exercises → Summary → Intuition || Wrong order.
- Each lesson uses a different order || All lessons share the same structure.
E: A fixed structure tells you how to use each part; see <a href="../lessons/L0-1.html">0.1</a>."""),
dict(obj="0.2-1", q="""Q: Xiao Li has lately had insomnia, fatigue and poor concentration. How would the "common cause" view and the "network" view each explain this?
- The two views explain it in exactly the same way || They start from different assumptions.
+ Common cause view: an underlying "depression" causes all these symptoms at once. Network view: insomnia may make a person tired, and tiredness makes it hard to concentrate; the symptoms affect one another || Correct.
- The network view assumes the symptoms are unrelated to each other || The network view is precisely about the relationships among symptoms.
- The common cause view says insomnia causes depression || In the common cause view, the latent "depression" causes each symptom.
E: For the contrast between the latent variable (common cause) view and the network view, see <a href="../lessons/L0-2.html">0.2</a>."""),
dict(obj="0.2-2", q="""Q: Two clients both score 12 on a depression scale. Why shouldn't a social worker look only at the total score?
- Because the total-score formula is often miscalculated || It is not a calculation problem.
+ Because the same 12 can come from completely different combinations of symptoms (one mostly insomnia, the other mostly worthlessness), and the two may need different help || Correct.
- Because higher total scores are less trustworthy || There is no such rule.
- Because total scores can only be used in research || Total scores are also common in practice; they just lose information.
E: Looking only at the total score loses the information about which symptoms are present and how they combine; see <a href="../lessons/L0-2.html">0.2</a>."""),
dict(obj="0.2-3", q="""Q: A study finds that "loneliness at the first survey predicts depression at the second survey six months later (even after controlling for depression at the first survey)." What is this kind of relationship called?
- Contemporaneous correlation || A contemporaneous correlation is the relationship between two variables at the same time point.
+ A cross-lagged relationship: earlier A predicts later B || Correct.
- Autoregression || Autoregression is earlier A predicting later A itself.
- A proven causal relationship || A predictive relationship is not proven causation.
E: "Cross" means across variables and "lagged" means across time; see <a href="../lessons/L0-2.html">0.2</a>."""),
dict(obj="0.2-4", q="""Q: A CLPN study reports a strong edge "loneliness item A → depression item B." Which conclusion can a CLPN support?
- Reducing loneliness will certainly lower this person's depression || This is a causal claim, and it is also applied to an individual.
- Loneliness is the cause of depression || A CLPN cannot establish causes of a disorder.
+ In this sample, people who scored higher on loneliness item A earlier tended to score higher on depression item B later (controlling for the other items) || Correct. This is a group-level predictive relationship.
- Depression does not affect loneliness || A strong edge in one direction does not mean the reverse direction is absent.
E: A CLPN answers "who predicts whom," not "who causes whom"; see <a href="../lessons/L0-2.html">0.2</a>."""),
]
SHORT = []
