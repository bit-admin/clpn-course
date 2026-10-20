# -*- coding: utf-8 -*-
# M2 module quiz: R foundations (Week 5, together with M1). No need to run R; answer by reading the code.
LEAD = "<p>Take this after Lessons 2.1–2.6 (Week 5 of the standard pace, together with the M1 module quiz). 8 auto-graded questions + 1 short-answer question, about 15 minutes. You only need to read the code, not run R; afterwards you can check your answers in RStudio.</p>"
ITEMS = [
dict(obj="2.1-3", q="""Q: In R you run <code>x &lt;- 5</code> and then <code>x &lt;- x * 2 + 1</code>. What is the value of <code>x</code> now?
N: 11 | 0
H: <code>&lt;-</code> stores the result computed on the right under the name on the left. The second line uses the old value of x, 5.
E: 5 × 2 + 1 = 11, and the result is stored back in x. For assignment and objects, see <a href="../lessons/L2-1.html">2.1</a>."""),
dict(obj="2.2-1", q="""Q: If <code>scores &lt;- c(3, 8, 5, 10)</code>, what is <code>scores[3]</code>?
N: 5 | 0
H: R counts positions from 1.
E: The 3rd element is 5. R counts from 1 (some languages count from 0); see <a href="../lessons/L2-2.html">2.2</a>."""),
dict(obj="2.2-3", q="""Q: <code>dep &lt;- c(2, NA, 4)</code>. What does <code>mean(dep)</code> return?
- 3 || By default, R does not skip missing values.
+ NA || Correct. If even one value is NA, the default mean is NA; you need <code>mean(dep, na.rm = TRUE)</code> to get 3.
- 2 || No.
- An error, and the code stops || There is no error; it just returns NA.
E: NA means missing; <code>na.rm = TRUE</code> tells the function to drop missing values before calculating; see <a href="../lessons/L2-2.html">2.2</a>."""),
dict(obj="2.2-2", q="""Q: In a dataset, gender is stored as the text values <code>"Male"</code> and <code>"Female"</code>. Which R data type is best for a categorical variable like this?
- Numeric || Text is not a number.
- Logical || A logical value is only TRUE or FALSE.
+ Factor || Correct. Factors are made for variables with a fixed set of categories.
- Function || A function is not a choice of data type.
E: For numeric, character, logical, factor and other types, see <a href="../lessons/L2-2.html">2.2</a>."""),
dict(obj="2.3-1", q="""Q: After you read the course data <code>clpn_sim_wide.csv</code> into R, <code>dim(dat)</code> shows <code>800 34</code>. What do the two numbers mean?
+ 800 rows (800 people), 34 columns (34 variables) || Correct. In a data frame, rows are cases and columns are variables.
- 800 variables, 34 people || The other way round.
- 800 items, 34 waves || No.
- Mean 800, standard deviation 34 || dim() gives dimensions, not statistics.
E: For the structure of data frames, see <a href="../lessons/L2-3.html">2.3</a>."""),
dict(obj="2.3-2", q="""Q: You want to keep only the women (<code>gender == 1</code>) in the data frame <code>dat</code>. Which dplyr code should you write?
- <code>dat |&gt; select(gender == 1)</code> || select() chooses columns, not rows.
+ <code>dat |&gt; filter(gender == 1)</code> || Correct. filter() chooses rows by a condition.
- <code>dat |&gt; mutate(gender = 1)</code> || This would set everyone's gender to 1.
- <code>dat |&gt; summarise(gender == 1)</code> || summarise() computes summary statistics.
E: select chooses columns, filter chooses rows, mutate creates or changes columns, and summarise summarizes; see <a href="../lessons/L2-3.html">2.3</a>. Note that testing "equals" takes two equals signs, <code>==</code>."""),
dict(obj="2.4-1", q="""Q: You ran <code>install.packages("glmnet")</code> yesterday. Today you open RStudio again. Which line should you run to use glmnet?
- Run <code>install.packages("glmnet")</code> again || You only need to install once; installing again wastes time.
+ <code>library(glmnet)</code> || Correct. You load the package once in every new R session.
- Nothing; yesterday's package is still loaded || When you close R, loaded packages are gone.
- <code>source("glmnet")</code> || source() runs a script file.
E: install.packages() installs once; library() loads every session; see <a href="../lessons/L2-4.html">2.4</a>."""),
dict(obj="2.4-3", q="""Q: A classmate copies your course folder to their own computer, and the line <code>read.csv("C:/Users/XiaoZhang/Desktop/data/clpn_sim_wide.csv")</code> in the script now fails. What is the best fix?
- Ask your classmate to rename their user account to "XiaoZhang" || Not realistic.
+ Open <code>clpn-course.Rproj</code> and use the relative path <code>read.csv("data/clpn_sim_wide.csv")</code> || Correct. The project sets the working directory to the course folder, so a relative path works on any computer.
- Copy the data to their desktop || It will break again on the next computer.
- Stop using CSV and use a screenshot instead || That won't work.
E: An RStudio Project and relative paths are what let someone else run your code; see <a href="../lessons/L2-4.html">2.4</a>."""),
]
SHORT = [
dict(obj="2.1-4", q="<p>You run <code>read.csv(\"data/my_survey.csv\")</code> and get the error <code>cannot open file 'data/my_survey.csv': No such file or directory</code>. Write a request for help to post on an R forum or in a study group (4–6 sentences). Someone who has never seen your computer should be able to find the problem without having to ask you follow-up questions.</p>",
     answer="<p>Example: \"Hi, when I run line 12 of R/L2-4.R, <code>read.csv(\"data/my_survey.csv\")</code>, I get the error: cannot open file 'data/my_survey.csv': No such file or directory. I opened the project by double-clicking clpn-course.Rproj, and <code>getwd()</code> shows .../clpn-course-en. The data folder contains clpn_sim_wide.csv, but I just noticed that my_survey.csv is in my Downloads folder. I have already tried retyping the file name. Where should I put the file? My R version is 4.5.0 (the text output of <code>sessionInfo()</code> is pasted below).\"</p><p>Key points: say exactly which line of code you ran, give the full error message word for word, say what you have already checked (working directory, whether the file is in that location), and give your software version.</p>",
     rubric=[(3, "Includes the code that was run, the full error message, the checks already made (e.g. getwd(), file location) and the software version, so a reader can find the problem directly"),
             (2, "Has the code and the error, but not the checks already made or the environment details"),
             (1, "Only says \"reading the data gives an error, what do I do?\" with no code or error text"),
             (0, "No answer")]),
]
