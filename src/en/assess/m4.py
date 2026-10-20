# -*- coding: utf-8 -*-
# M4 module quiz: longitudinal data (Week 8, together with M3)
LEAD = "<p>Take this after Lessons 4.1–4.3 (Week 8 of the standard pace, together with the M3 module quiz). 8 auto-graded questions + 1 short-answer question, about 15 minutes.</p>"
ITEMS = [
dict(obj="4.1-1", q="""Q: Each year for 5 years, a city surveys loneliness in a new random sample of 1000 residents. What kind of design is this?
- Panel (longitudinal) design || A panel design measures the same people again and again.
+ Repeated cross-sectional design || Correct. Each year has different people, so you can see population trends but not how the same person changes.
- Cross-sectional design || A plain cross-sectional design surveys only once.
- Experimental design || Nobody is randomly assigned to an intervention.
E: For the difference between cross-sectional, repeated cross-sectional and panel designs, see <a href="../lessons/L4-1.html">4.1</a>. A CLPN needs panel data."""),
dict(obj="4.1-2", q="""Q: A researcher wants to know whether "poor sleep leads to low mood the next day," but measures only once a year. What is the main problem?
- Once a year is too often || The opposite direction.
+ The interval is far longer than the time scale of the process itself, so such a short-term effect is unlikely to show up || Correct.
- The interval has nothing to do with which effects you can see || The interval does affect which effects you can see.
- It should be changed to a cross-sectional design || A cross-sectional design is even less able to say what comes "after."
E: The interval between waves (the lag) has to match the process you want to study; see <a href="../lessons/L4-1.html">4.1</a> (Lesson 5.4 goes deeper)."""),
dict(obj="4.1-3", q="""Q: "People who are lonelier over the long run are also more depressed over the long run" and "during the periods when a person is lonelier than usual for them, they are also more depressed than usual for them." At which levels are these two relationships?
+ The first is between-person; the second is within-person || Correct.
- The first is within-person; the second is between-person || The other way round.
- Both are between-person || The second compares a person with their own usual level, so it is within-person.
- They are the same thing || They can be completely different; this is one of the core difficulties of longitudinal research.
E: For between-person vs within-person, see <a href="../lessons/L4-1.html">4.1</a>; the RI-CLPM in Lesson 5.3 separates the two."""),
dict(obj="4.1-4", q="""Q: A loneliness scale was given on paper in Year 1 and on mobile phones in Year 3, and the Year 3 mean is clearly higher. Before you conclude that "people have become lonelier," what do you need to check first?
- Whether the sample is larger than 1000 || Sample size cannot answer this.
+ Measurement invariance: whether the scale measures the same thing in the same way at both time points || Correct. A change in how people respond can change how they understand the items or where they draw the line when answering.
- Whether the mean is a whole number || Irrelevant.
- Whether LASSO was used || Irrelevant.
E: For what measurement invariance means, see <a href="../lessons/L4-1.html">4.1</a>; the optional advanced Lesson 7.6 shows you how to test it in R."""),
dict(obj="4.2-1", q="""Q: The course data have 800 people and 3 waves; in wide format each person is one row. After you convert it to long format (one row per person per wave), how many rows are there?
N: 2400 | 0
H: In long format, each person takes one row for every wave.
E: 800 × 3 = 2400 rows. For wide vs long format, see <a href="../lessons/L4-2.html">4.2</a>."""),
dict(obj="4.2-3", q="""Q: When you prepare the "T1 item matrix" and the "T2 item matrix" for a CLPN, what is the key requirement?
- The two matrices can have different numbers of rows || With different numbers of rows, the rows cannot be matched.
+ Row i of both matrices must be the same person, and the items must be in the same order || Correct. Otherwise you would be using person A's T1 to predict person B's T2.
- Shuffle each matrix randomly first || Shuffling destroys the matching of cases.
- The T2 matrix must have one more item than T1 || Both matrices should contain the same items.
E: Matching cases one to one is the bare minimum of CLPN data preparation; see <a href="../lessons/L4-2.html">4.2</a>."""),
dict(obj="4.3-1", q="""Q: In a panel survey, people with higher depression scores at Wave 1 are more likely to drop out by Wave 2; but once you know their Wave 1 depression score, whether they drop out is unrelated to how depressed they would have been at Wave 2. What kind of missingness is this?
- MCAR (missing completely at random) || Dropout is related to Wave 1 depression, so it is not completely random.
+ MAR (missing at random: missingness is related to observed variables) || Correct. In this case FIML or multiple imputation can use the Wave 1 information.
- MNAR (missing not at random) || MNAR means missingness depends on the unobserved value itself, which is not what the question describes.
- Not missing data || Dropout is missing data.
E: For the difference between MCAR, MAR and MNAR, see <a href="../lessons/L4-3.html">4.3</a>."""),
dict(obj="4.3-3", q="""Q: In three-wave data, you delete a person's whole row if any wave has a missing value (listwise deletion). What is the main risk?
- The calculations get slower || Deleting data only makes them faster.
+ The sample gets smaller, and if the data are not missing completely at random, the people who remain are systematically biased || Correct.
- It always makes the results more accurate || Quite the opposite.
- There is no risk || There is.
E: For the pros and cons of listwise deletion, pairwise deletion, FIML and multiple imputation, see <a href="../lessons/L4-3.html">4.3</a>."""),
]
SHORT = [
dict(obj="4.3-2", q="<p>In a three-wave panel study of adolescents, only 60% of participants remain at Wave 3. In 3–4 sentences: (1) Why does attrition threaten the study's conclusions? (2) What analysis would you do to check the effect of attrition?</p>",
     answer="<p>(1) If the people who stay differ from those who drop out (for example, the dropouts were lonelier at Wave 1 or came from families in greater difficulty), the Wave 3 results represent only \"those who stayed,\" and both the mean levels and the relationships between variables may be biased. (2) Do an attrition analysis: compare stayers and dropouts on the main Wave 1 variables (loneliness, depression, gender, age, etc.), e.g. with t-tests, chi-square tests, or a logistic regression predicting dropout; report the attrition rate, handle the missing data with a method such as FIML or multiple imputation, and run a sensitivity analysis if needed.</p>",
     rubric=[(3, "Explains clearly that stayers and dropouts differ, so the results are biased, and gives a concrete attrition analysis (comparing Wave 1 variables or predicting dropout with logistic regression) and a way to handle the missing data"),
             (2, "Gives either the threat or the analysis; the other is incomplete"),
             (1, "Only says \"the sample got smaller,\" without systematic bias or a concrete analysis"),
             (0, "No answer, or wrong")]),
]
