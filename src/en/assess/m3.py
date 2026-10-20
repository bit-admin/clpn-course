# -*- coding: utf-8 -*-
# M3 module quiz: regression and regularization (Week 8, together with M4)
LEAD = "<p>Take this after Lessons 3.1–3.5 (Week 8 of the standard pace, together with the M4 module quiz). 10 auto-graded questions + 1 short-answer question, about 20 minutes. You may use a calculator.</p>"
ITEMS = [
dict(obj="3.1-1", q="""Q: Predicting "loneliness score" (y) from "social activities per week" (x) gives the regression equation ŷ = 3.2 − 0.15x. What does the slope −0.15 mean?
- Social activity reduces loneliness by 15% || The slope is not a percentage, and you cannot say social activity "reduces" loneliness from it.
+ People with 1 more social activity per week have a predicted loneliness score that is 0.15 points lower on average || Correct.
- People with no social activities have a loneliness score of −0.15 || The predicted value at x = 0 is the intercept, 3.2.
- The correlation between loneliness and social activity is −0.15 || A slope and a correlation are generally not equal unless both variables are standardized.
E: Slope = how much ŷ changes on average for each 1-unit increase in x; see <a href="../lessons/L3-1.html">3.1</a>."""),
dict(obj="3.1-1", q="""Q: Using the same equation, ŷ = 3.2 − 0.15x, what is the predicted loneliness score of an older adult who takes part in 4 social activities a week?
N: 2.6 | 0.01
H: Substitute x = 4 into the equation.
E: 3.2 − 0.15 × 4 = 3.2 − 0.6 = 2.6; see <a href="../lessons/L3-1.html">3.1</a>."""),
dict(obj="3.1-2", q="""Q: What condition does the regression line chosen by least squares satisfy?
- It passes through the most data points || No.
+ The sum of the squared residuals (observed − predicted) over all points is as small as possible || Correct.
- It has the largest slope || No.
- Its intercept is 0 || No.
E: The smallest sum of squared residuals is what "least squares" means; see <a href="../lessons/L3-1.html">3.1</a>."""),
dict(obj="3.2-1", q="""Q: You predict depression from "social support" and "age" together, and the coefficient for social support is −0.40. How should you read this coefficient?
- Each extra point of social support lowers depression by 0.40 points, whatever the age || The key is the condition "holding age constant."
+ Among people of the same age, each extra point of social support goes with a predicted depression score 0.40 points lower on average || Correct; this is what "controlling for age" means.
- Social support explains 40% of depression || That is how you describe R², not a coefficient.
- Age has no effect on depression || The question does not give the coefficient for age.
E: A partial regression coefficient means "with the other variables held constant"; see <a href="../lessons/L3-2.html">3.2</a>."""),
dict(obj="3.2-2", q="""Q: Predicting depression from "loneliness" alone gives a coefficient of 0.50. After you add "social support," the loneliness coefficient drops to 0.30. What is the most likely explanation?
- Adding the variable caused a calculation error || Coefficients often change; it is not an error.
+ Loneliness and social support share information, and part of the original 0.50 overlaps with social support || Correct.
- The effect of loneliness on depression declined over time || These are the same cross-sectional data; time plays no role.
- Social support made loneliness harder to measure || No.
E: Coefficients change when you control for other variables because the predictors overlap; see <a href="../lessons/L3-2.html">3.2</a>."""),
dict(obj="3.2-3", q="""Q: A researcher puts the "UCLA Loneliness total score" and "the total score of another loneliness scale" into the same regression. They correlate at 0.92. What problem is most likely?
- The model's R² will certainly be 0 || It won't.
+ Multicollinearity: both coefficients get larger standard errors and unstable estimates, and it is hard to tell their roles apart || Correct.
- Both coefficients will certainly be significant || Quite the opposite: often neither is.
- No effect at all || Highly correlated predictors do cause problems.
E: For multicollinearity and its effects, see <a href="../lessons/L3-2.html">3.2</a>. In network analysis, items with heavily overlapping content cause the same problem."""),
dict(obj="3.3-1", q="""Q: In predicting depression, the unstandardized coefficient of "monthly income (in yuan, the Chinese currency unit)" is b = −0.0004 and that of "social support (1–5 points)" is b = −0.35. Can you conclude from this that social support matters far more than income?
- Yes, the absolute value of −0.35 is far larger than that of −0.0004 || The units differ, so the b values cannot be compared directly.
+ Not directly, because the units differ (yuan vs. points); to compare relative size, look at the standardized coefficients β || Correct.
- Yes, because income is unimportant || The size of b cannot tell you that.
- No, because income is negative || The sign is not the reason.
E: b carries the units of the variables; β is the standardized coefficient and is suited to comparing relative size; see <a href="../lessons/L3-3.html">3.3</a>."""),
dict(obj="3.4-2", q="""Q: A logistic regression predicts "whether an adolescent drops out of school." The odds ratio for "classes skipped per week" is OR = 1.5. How should you read it?
- Each extra skipped class raises the probability of dropping out by 1.5 percentage points || An OR is a multiple of the odds, not percentage points of probability.
+ Each extra skipped class multiplies the odds of dropping out by 1.5 || Correct.
- 1.5% of students who skip class drop out || No.
- Skipping class is unrelated to dropping out || Only OR = 1 means no relationship.
E: For how to read odds and odds ratios (OR), see <a href="../lessons/L3-4.html">3.4</a>."""),
dict(obj="3.5-2", q="""Q: What is the key difference between LASSO and ordinary regression?
- LASSO can only use one predictor || It can use many.
+ LASSO penalizes the absolute values of the coefficients and pushes very small coefficients exactly to 0, which amounts to automatic variable selection || Correct. A CLPN uses this to decide which edges to keep.
- LASSO coefficients are always larger than ordinary regression coefficients || LASSO coefficients are usually smaller (shrunk).
- LASSO doesn't need data || Of course it does.
E: For the LASSO penalty and how it sets coefficients to 0, see <a href="../lessons/L3-5.html">3.5</a>."""),
dict(obj="3.5-3", q="""Q: After cross-validation with <code>cv.glmnet</code>, you can choose <code>lambda.min</code> or <code>lambda.1se</code>. Compared with <code>lambda.min</code>, what kind of model does <code>lambda.1se</code> give?
- More nonzero coefficients and more complexity || The opposite direction.
+ A stronger penalty, fewer nonzero coefficients, a more "conservative" model || Correct.
- Exactly the same model || They usually differ.
- All coefficients are 0 || Usually not all are 0.
E: <code>lambda.1se</code> is the largest λ whose cross-validated error is within 1 standard error of the minimum, so its model is sparser; see <a href="../lessons/L3-5.html">3.5</a>."""),
]
SHORT = [
dict(obj="3.5-1", q="<p>A colleague built a regression model from 40 clients' data with 30 predictors. It predicts \"almost perfectly\" for those 40 people, and the colleague plans to use it to screen new clients. In 3–4 sentences, explain the likely problem to them and give one concrete recommendation.</p>",
     answer="<p>With only 40 people and 30 predictors, the model has probably \"memorized\" chance features (noise) of these 40 people. This is called overfitting: predicting the old data well does not mean predicting new clients accurately. Recommendation: test the predictions with cross-validation or a new batch of data; use fewer predictors, or use a regularization method such as LASSO to make the model simpler.</p>",
     rubric=[(3, "Names overfitting (memorizing noise), identifies few people and many predictors as the cause, and gives a concrete recommendation such as cross-validation, testing on a new sample, or regularization"),
             (2, "Names overfitting, but the cause or the recommendation is incomplete"),
             (1, "Only says the model is unreliable, without explaining why or giving an actionable recommendation"),
             (0, "No answer, or says the model can be used as it is")]),
]
