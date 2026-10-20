# -*- coding: utf-8 -*-
# M6 module quiz: foundations of network psychometrics (Week 11, after Lesson 6.5)
LEAD = "<p>Take this after Lessons 6.1–6.5 (Week 11 of the standard pace). 10 auto-graded questions + 1 short-answer question, about 20 minutes. You don't need to open R.</p>"
ITEMS = [
dict(obj="6.1-2", q="""Q: An undirected network has 5 nodes (no self-loops). What is the largest possible number of edges?
N: 10 | 0
H: There is at most one edge between each pair of nodes: how many ways are there to choose 2 of 5?
E: 5 × 4 / 2 = 10. The matching weights matrix is a symmetric 5 × 5 matrix, and you only need to look at the 10 cells of its upper triangle. See <a href="../lessons/L6-1.html">6.1</a>."""),
dict(obj="6.1-1", q="""Q: What is the main difference between the "edges" of a cross-sectional partial correlation network (GGM) and those of a CLPN?
- GGM edges have a direction; CLPN edges don't || The other way round.
+ GGM edges have no direction (conditional associations at the same time); CLPN edges have a direction (A at T1 predicts B at T2) || Correct.
- The edges are exactly the same || One is undirected and within one time point; the other is directed and across time.
- A GGM has no edge weights || GGM edge weights are partial correlations.
E: For directed vs undirected networks, see <a href="../lessons/L6-1.html">6.1</a>; for the directed edges of a CLPN, see Lesson 7.1."""),
dict(obj="6.1-3", q="""Q: In the psychological networks of this course, what do "nodes" and "edges" represent?
+ Nodes are items (symptoms); edges are statistical associations between items || Correct.
- Nodes are people; edges are social ties between people || That is social network analysis (SNA), not a psychological network.
- Nodes are scale total scores; edges are causal effects || This course uses items as nodes, and edges are statistical associations, not proven causal effects.
- Nodes are time points; edges are amounts of change || No.
E: For the basic setup of a psychological network, see <a href="../lessons/L6-1.html">6.1</a>. The "social networks" (who knows whom) that social workers often deal with are a different thing from the psychological networks here."""),
dict(obj="6.2-1", q="""Q: "Insomnia" and "fatigue" correlate at .45, but after controlling for the other 7 items, their partial correlation is only .05. What is the most reasonable reading?
- A calculation error: a partial correlation can't be that much smaller than the correlation || This happens often.
+ Most of what the two share can be explained by other items (e.g. depressed mood); once those are taken out, the direct, unique association between the two is weak || Correct.
- Insomnia causes fatigue || Neither a correlation nor a partial correlation shows causation on its own.
- Report the correlation, not the partial correlation || The two answer different questions.
E: A partial correlation is the association left after controlling for all the other variables; see <a href="../lessons/L6-2.html">6.2</a>."""),
dict(obj="6.2-2", q="""Q: In a GGM, what does "no edge" between A and C mean statistically?
- The correlation between A and C is 0 || They may be strongly correlated, for example by being linked through B.
+ After controlling for all other nodes in the network, A and C are conditionally independent (their partial correlation is 0) || Correct.
- A and C are the same item || Irrelevant.
- A or C is missing from the data || Irrelevant.
E: For "no edge = conditional independence," see <a href="../lessons/L6-2.html">6.2</a>."""),
dict(obj="6.2-4", q="""Q: In the correlation matrix of the 9 loneliness and depression items, almost every pair of items is significantly positively correlated. Drawn as a "correlation network," the screen is full of lines; drawn as a partial correlation network, it is much cleaner. What is the main reason?
- The partial correlation network drops the negative values || A partial correlation network can have negative edges too.
+ The correlation network also draws an edge for associations that run indirectly through other items; partial correlations keep only the direct associations left after the other items are taken out || Correct.
- The partial correlation network uses a smaller sample || Both use the same data.
- The correlation network was miscalculated || It wasn't; it just answers a different question.
E: For the comparison of correlation and partial correlation networks, see <a href="../lessons/L6-2.html">6.2</a>."""),
dict(obj="6.3-1", q="""Q: One regression method adds a penalty during estimation and pushes very small coefficients exactly to 0. What is its abbreviation? (5 letters)
T: LASSO||lasso||Lasso
H: You met it in Lesson 3.5; its full name is least absolute shrinkage and selection operator.
E: LASSO (an L1 penalty) pushes weak coefficients to 0 and so gives a sparse network; the graphical lasso is its version for partial correlation networks. See <a href="../lessons/L6-3.html">6.3</a> and 3.5."""),
dict(obj="6.3-2", q="""Q: When you estimate a network with EBICglasso and change the hyperparameter γ from 0 to 0.5, how does the network usually change?
+ It becomes sparser: fewer edges, keeping only those with stronger evidence || Correct. The larger γ, the more heavily EBIC penalizes complex models.
- It becomes denser: more edges || The opposite direction.
- Not at all || γ affects which λ is chosen.
- All edges become negative || Irrelevant.
E: For the role of γ, see <a href="../lessons/L6-3.html">6.3</a>. γ = 0.5 is the common default and leans conservative; with smaller samples some researchers use 0.25."""),
dict(obj="6.5-1", q="""Q: A node's three edges have weights 0.30, 0.20 and −0.10. What is its expected influence (EI)?
N: 0.4 | 0.001
H: EI adds the edge weights as they are (keeping the signs); strength adds their absolute values.
E: EI = 0.30 + 0.20 − 0.10 = 0.40; strength = 0.30 + 0.20 + 0.10 = 0.60. With negative edges the two differ; see <a href="../lessons/L6-5.html">6.5</a>."""),
dict(obj="6.5-4", q="""Q: Which statement about using betweenness and closeness centrality in psychological networks best matches this course's advice?
- They are the most stable and should be reported first || Quite the opposite.
+ They are often unstable in psychological networks and should be used with care; if you report them, check their stability first || Correct.
- With 9 nodes in the network they are safe to use || Stability depends on many things and has to be tested.
- They are the same index as strength || They are not.
E: For the limits of betweenness and closeness, see <a href="../lessons/L6-5.html">6.5</a>; for stability testing, see Lesson 8.3."""),
]
SHORT = [
dict(obj="6.5-2", q="<p>In a network, the node \"self-blame\" ranks 1st of 9 nodes in strength, but only 6th in expected influence (EI). In 3–4 sentences, explain: (1) Why does this happen? (2) Which index should this network rely on more, and why?</p>",
     answer="<p>(1) Strength adds the absolute values of the edge weights; EI adds them with their signs. \"Self-blame\" probably has a few fairly strong <b>negative edges</b>: as absolute values they make its strength large, but added with their signs they cancel out positive edges, so its EI is low. (2) When the network has negative edges and what we care about is the overall direction in which a node \"activates\" the others, EI is more suitable (Robinaugh et al., 2016): strength counts an \"inhibiting\" relationship as \"tight connection\" too. Whichever index you use, check its stability first (Lesson 8.3), and don't read high centrality directly as \"the best intervention target.\"</p>",
     rubric=[(3, "Gives the reason (negative edges: strength takes absolute values, EI keeps the signs), explains why EI is more suitable when there are negative edges, and adds a word of caution about interpretation"),
             (2, "The reason is right, but the argument for choosing an index is unclear"),
             (1, "Only says \"the two indices are calculated differently,\" without mentioning negative edges"),
             (0, "No answer, or wrong")]),
]
