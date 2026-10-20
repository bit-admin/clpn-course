# -*- coding: utf-8 -*-
# Pre-test: take it before starting the course; ungraded. Tests prerequisite skills only, no CLPN content.
LEAD = "<p>Spend about 20 minutes on this before you start. The pre-test is <b>ungraded</b>: recommended, but optional. It only shows your starting point: arithmetic and proportions, reading tables, statistical intuition, terminology, and basic computer skills. When you finish, use the table at the bottom of the page to choose your study pace.</p>"
INTRO = """<section class="sec" id="how"><h2>How to take it</h2>
<ul><li>Answer from what you know now: no looking things up, and no tools other than a calculator. If you don't know, guess. A wrong guess is fine; the point of the pre-test is to find what you don't know yet.</li>
<li>Only your <b>first</b> answer to each question counts. The top of the page shows "(y correct on first try)"; write down y.</li></ul></section>
<section class="sec" id="self"><h2>First, the 6 self-assessment items (ungraded)</h2>
<p>On paper or in your study log, mark each statement "Yes" or "No":</p>
<ol><li>I have used Excel or similar software to calculate an average.</li>
<li>I have heard of terms such as p-value and correlation coefficient.</li>
<li>I can read a short English-language research abstract (with a dictionary if needed).</li>
<li>I have written computer code of any kind (even if I only copied, pasted and ran it).</li>
<li>I can find a downloaded file on my computer and unzip an archive.</li>
<li>I can reliably set aside at least 6 hours a week for this course.</li></ol></section>"""
ITEMS = [
dict(obj="1.2-1", q="""Q: A community center served 30 clients this month; 12 of them reported "often feeling lonely." What percentage of clients reported feeling lonely? (Enter a number only, e.g. 25)
N: 40 | 0.5
H: Proportion = part ÷ whole; then multiply by 100.
E: 12 ÷ 30 = 0.4, i.e. 40%. Proportions and percentages are the first step in descriptive statistics; see <a href="../lessons/L1-2.html">1.2</a>."""),
dict(obj="1.2-1", q="""Q: Five adolescents do 2, 4, 4, 6 and 9 hours of volunteer work per week. What is the average number of hours per person?
N: 5 | 0.01
H: Mean = sum of all values ÷ number of people.
E: (2 + 4 + 4 + 6 + 9) ÷ 5 = 25 ÷ 5 = 5. For how to calculate a mean, see <a href="../lessons/L1-2.html">1.2</a>."""),
dict(obj="1.2-1", q="""Q: A depression scale has 9 items, each scored 0–3, and the total score is the sum of the 9 items. What is the highest possible total score?
N: 27 | 0
H: Each item scores at most 3. How many items are there?
E: 9 × 3 = 27. You need to know a scale's possible range to judge whether a score is high or low; for the difference between items and total scores, see <a href="../lessons/L1-1.html">1.1</a>."""),
dict(obj="1.2-2", q="""Q: The table shows how often 100 students at a school met friends last week: 0 times, 40 students; 1–2 times, 35; 3–5 times, 20; 6 or more times, 5. Which statement is most accurate?
- Most students met friends 3 or more times a week || Only 20 + 5 = 25 students met friends 3 or more times.
+ Meeting 0 times is the most common, and the higher the frequency, the fewer the students || Correct. A shape that piles up on the left with a tail stretching to the right is called right-skewed.
- The four groups are about the same size || 40 and 5 are very different.
- The table shows no pattern || You can see that the number of students falls as the number of meetings rises.
E: Reading a frequency table means looking at how many people fall into each category. This shape, many on the left and few on the right, is called right-skewed (positively skewed); see <a href="../lessons/L1-2.html">1.2</a>."""),
dict(obj="1.1-1", q="""Q: A questionnaire codes "Marital status: 1 = never married, 2 = married, 3 = divorced, 4 = widowed." Which of the following is the WRONG thing to do?
- Count how many people fall into each category || This is reasonable.
- Calculate the percentage of respondents in each category || This is reasonable.
+ Average the codes 1–4 and report "the average marital status is 2.1" || Correct, this is the wrong thing to do. The numbers are only labels for categories, not amounts, so their average means nothing.
- Draw a bar chart || This is reasonable.
E: A variable whose values only name categories is a nominal variable. The level of measurement decides which calculations make sense; see <a href="../lessons/L1-1.html">1.1</a>."""),
dict(obj="1.2-2", q="""Q: A line chart shows the yearly number of calls to a hotline from 2020 to 2023: 800, 1,200, 1,500 and 1,450. Which description is most accurate?
- Calls fell every year || Calls rose over the first three years.
+ Calls rose over the first three years and dipped slightly in the last year || Correct.
- Calls stayed the same throughout || The changes are clearly visible.
- Calls peaked in 2023 || The peak was 1,500 in 2022.
E: When reading a chart, first check what the vertical axis shows, then look for the trend and turning points. For the basics of describing data, see <a href="../lessons/L1-2.html">1.2</a>."""),
dict(obj="1.2-1", q="""Q: Among the monthly salaries of 6 employees at an agency, one director earns far more than everyone else. Which number better describes "the typical employee's monthly salary"?
- The mean, because it uses every employee's data || The mean is pulled up by that one very high value.
+ The median, because it is not affected by a few extreme values || Correct.
- The maximum || The maximum only describes the director.
- There is no difference between the two || With an extreme value, the difference can be large.
E: When there are extreme values or the distribution is skewed, the median represents "the person in the middle" better than the mean; see <a href="../lessons/L1-2.html">1.2</a>."""),
dict(obj="1.4-4", q="""Q: A study finds that older adults who take part in more community activities have lower depression scores. Which statement is the most cautious?
- Taking part in community activities reduces depression || "Reduces" is a causal claim, and this association alone cannot support it.
- Depression keeps people from taking part in community activities || This is also a causal guess, and it has not been shown either.
+ The two are associated, but the cause could run in both directions, or a third factor (such as physical health) could affect both || Correct.
- The two are unrelated || The study did find an association.
E: Correlation is not causation. A third variable that affects both is called a confounder; see <a href="../lessons/L1-4.html">1.4</a>."""),
dict(obj="1.5-1", q="""Q: A researcher randomly samples 500 of a city's 20,000 college students and computes their mean loneliness score. What is this mean of the 500 students called in statistics?
- A parameter, because it describes the city's college students || A parameter is the (usually unknown) value that describes all 20,000 students.
+ A statistic, because it is computed from a sample || Correct. We use sample statistics to estimate population parameters.
- The population || The population is the 20,000 college students themselves.
- Error || No.
E: For population vs sample and parameter vs statistic, see <a href="../lessons/L1-5.html">1.5</a>."""),
dict(obj="1.4-4", q="""Q: "In months when ice cream sales are high, there are also more drownings," yet ice cream does not make people drown. What do statisticians call the "third variable" that drives both?
T: confounder||confounding variable||confounding||third variable||confounding factor
H: In hot weather, more people eat ice cream and more people go swimming. What is "the weather" called in statistics?
E: Weather (temperature) affects both, and a variable like that is called a confounder (confounding variable); see <a href="../lessons/L1-4.html">1.4</a>."""),
dict(obj="1.1-3", q="""Q: What is a single question on a questionnaire scale called in the research literature? (One word)
T: item||items
H: It starts with "i" and is contrasted with the scale score.
E: A single question is an item, the summed score is the scale score, and the psychological trait they aim to measure is a construct; see <a href="../lessons/L1-1.html">1.1</a>."""),
dict(obj="1.4-2", q="""Q: What is the statistical term for the degree to which two variables vary together?
T: correlation||correlation coefficient||correlations
H: A statistic that describes whether two variables change together.
E: Correlation describes how two variables vary together; it is usually expressed as Pearson's correlation coefficient r. See <a href="../lessons/L1-4.html">1.4</a>."""),
dict(obj="2.4-3", q="""Q: You downloaded the course archive <code>clpn-course-en.zip</code>. What should you do first, before using any of the files in it?
- Double-click a file inside the archive, edit it and save || Changes made to files inside an archive are often not saved.
+ Extract (unzip) the archive into a folder you can easily find || Correct. Open the files only after extracting them.
- Rename the archive to .exe || Never do this.
- Delete the archive and download it again || There is no need to.
E: Extract all course files before using them; see the <a href="../START_HERE.html">learning guide</a> and <a href="../lessons/L2-4.html">2.4</a>."""),
dict(obj="2.1-2", q="""Q: You created a folder called "course" inside your computer's "Documents" folder and put <code>data.csv</code> in it. Which of these is most likely the file's full path on Windows?
- data.csv\\course\\Documents || The order is reversed: a path goes from the outer folder to the inner one and ends with the file name.
+ C:\\Users\\YourName\\Documents\\course\\data.csv || Correct.
- course.csv || This is just a file name; it does not say which folder the file is in.
- http://data.csv || This is how a web address is written, not a path on your computer.
E: A path goes from the drive, folder by folder, down to the file. When R reads data, you have to tell it where the file is; see <a href="../lessons/L2-4.html">2.4</a>."""),
]
SHORT = []
OUTRO = """<section class="sec" id="route"><h2>When you finish: choose your pace</h2>
<div class="tablewrap"><table><tr><th>Correct on first try (out of 14)</th><th>Recommendation</th></tr>
<tr><td>6 or fewer, or "No" on self-assessment item 6</td><td>Take the <b>relaxed pace of about 19 weeks</b> (add a buffer week after weeks 5, 8 and 13; see <a href="../index.html#pacing">Recommended Pacing in the syllabus</a>). Move on past M1 and M2 only after scoring at least 70% on their module quizzes.</td></tr>
<tr><td>7–11</td><td>Follow the <b>standard {{C:weeks}} weeks</b>. Go more slowly through the lessons linked from the questions you missed, and work the examples once more.</td></tr>
<tr><td>12 or more</td><td>You can consider the <b>compressed pace of about 12 weeks</b>, but do not compress R (M2) or CLPN (M7).</td></tr></table></div>
<p>Write your first-try score and your 6 self-assessment answers in your <a href="study_log.html">study log</a>. After Lesson 10.3, take the <a href="assessment.html">final exam</a>; some of its questions test the same points as the pre-test, so you can compare and see your progress.</p></section>"""
