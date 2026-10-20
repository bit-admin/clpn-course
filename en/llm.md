# CLPN From Scratch · Course Map

Self-paced English course on Cross-Lagged Panel Network (CLPN) analysis: 11 modules, 45 core lessons + 2 optional lessons, ~85 hours of core lesson reading (plus hands-on exercises), scheduled over 16 weeks. Assumed background: introductory calculus, no prior R experience required. The primary panel dataset is simulated and contains no personal data.

© 2026 ZHANG. Course content (text, lessons, materials, figures, data and data documentation) licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); code (R scripts, data/simulate_data.R, website JavaScript/CSS, build and test scripts) under the MIT License (https://opensource.org/license/mit). See LICENSE. Source: https://github.com/bit-admin/clpn-course

This file is a machine-readable directory for agents/LLMs. Each lesson's full text lives in its own Markdown file. Use the map below to decide which lesson to read, then fetch only the relevant file rather than loading all lessons at once.

Lesson IDs map to filenames by replacing `.` with `-`: Lesson 1.1 is `lessons/L1-1.md`. All relative links below resolve from this folder (`en/`).

## Site Map

| Path | Contents |
| --- | --- |
| [index.html](index.html) | Human-readable course syllabus |
| [START_HERE.html](START_HERE.html) | Study Guide: how to navigate the course, 16-week schedule, how to study each lesson |
| [START_HERE.md](START_HERE.md) | Markdown version of the Study Guide (generated from the same source as START_HERE.html) |
| [materials/glossary.html](materials/glossary.html) | Glossary of core terms |
| [materials/cheatsheets.html](materials/cheatsheets.html) | Cheat sheets: R basics, regression, CLPN pipeline, reporting checklist |
| [materials/formulas.html](materials/formulas.html) | Formula reference |
| [materials/faq.html](materials/faq.html) | Frequently asked questions (FAQ) |
| [materials/study_log.html](materials/study_log.html) | Study log (fill in directly in your browser) |
| [materials/writing.html](materials/writing.html) | Writing workshop: before/after examples and rewrite tasks for Methods, Results, and Limitations |
| [materials/reading.html](materials/reading.html) | Paper reading pack: curated papers with DOI links and guided reading questions |
| [materials/case_elsoc.html](materials/case_elsoc.html) | Real-data case: CLPN of depressive symptoms in ELSOC (`data/elsoc_phq8_wide.csv`, CC0) |
| [materials/assessment.html](materials/assessment.html) | Assessments hub: pre-test, module quizzes, and final exam (instructions & rubrics) |
| [downloads/index.html](downloads/index.html) | Download the complete course package (offline site, data, R scripts, exercise solutions) |
| [data/data_dictionary.md](data/data_dictionary.md) | Data dictionary for the simulated panel and public datasets |
| [R/README.md](R/README.md) | Installing R/RStudio, running scripts, and execution order |
| `lessons/L*.md` | Plain-text reading version of each lesson |
| `R/L*.R` | Companion R scripts for each lesson |

In the `.md` reading files, interactive widgets are noted by title and quiz questions mark the correct option.

## Download

The complete English course is packaged as [../downloads/clpn-course-en.zip](../downloads/clpn-course-en.zip) (see the [Download page](downloads/index.html)), which extracts to `clpn-course-en/` containing:

| Path | Contents |
| --- | --- |
| `README.md` | Learner guide for the unpacked folder: where to start and how to run R |
| `index.html`, `START_HERE.html`, `lessons/*.html`, `materials/` | Complete offline edition of the website—double-click `index.html` to browse without internet |
| `data/` | Simulated panel data, data dictionary, `simulate_data.R`, true coefficient matrices; `coaches_mhc_raw.csv` (CC0) for Lesson 7.6; ELSOC original `.RData` and preprocessed `elsoc_phq8_wide.csv` (CC0) |
| `R/` | Lesson R scripts, `_setup.R`, `run_all.R`, `assess_answers.R`, `data_elsoc.R`, `case_elsoc.R`, `R/README.md`, `R/solutions/` exercise solutions, and `R/output/` reference outputs |
| `clpn-course.Rproj`, `LICENSE`, `THIRD_PARTY_NOTICES.md` | RStudio project file and license notices (content CC BY 4.0, code MIT) |

Double-click `clpn-course.Rproj` to open the project in RStudio. For script dependencies (e.g., 4.3 → 10.1 → 10.2 → 10.3), see [R/README.md](R/README.md).

## Suggested Pacing

| Week | Lessons | Focus |
| --- | --- | --- |
| Week 1 | 0.1 · 0.2 · 1.1 | Getting started: course map, why learn CLPN, variables and measurement |
| Week 2 | 1.2 · 1.3 · 2.1 · 0.2 Quick Run | Descriptive statistics, z-scores; install R (in Weeks 2–5, M1 Statistics and M2 R are studied side by side); once R is installed, do the 'Quick Run' in Lesson 0.2 (about 30 min): copy the ready-made code and produce your first CLPN plot |
| Week 3 | 2.2 · 1.4 · 2.3 | R syntax; covariance and correlation; data frames |
| Week 4 | 1.5 · 1.6 · 2.4 | Standard errors, confidence intervals, p-values; packages and importing data |
| Week 5 | 2.5 · 2.6 · Module Quizzes | Redoing the statistics basics in R; plots and reports; M1 and M2 module quizzes |
| Week 6 | 3.1 · 3.2 · 3.3 | After M1 and M2, on to M3 Regression: simple regression, multiple regression, standardized coefficients |
| Week 7 | 3.4 · 3.5 · 4.1 | Logistic regression, regularization and LASSO; longitudinal designs |
| Week 8 | 4.2 · 4.3 · Module Quizzes | Reshaping data, missing data and attrition; M3 and M4 module quizzes (midterm) |
| Week 9 | 5.1 · 5.2 · 5.3 | CLPM intuition, lavaan in practice, RI-CLPM |
| Week 10 | 5.4 · 6.1 · 6.2 | The limits of causal inference; the language of networks; partial correlation and GGMs |
| Week 11 | 6.3 · 6.4 · 6.5 | Regularized networks, qgraph / bootnet, centrality |
| Week 12 | 7.1 · 7.2 (2 sessions) | CLPN model logic; nodewise estimation with glmnet |
| Week 13 | 7.3 · 7.4 · 7.5 | CLPN visualization, out/in-EI, multi-wave data and design choices; the optional advanced lessons 7.6, 7.7 are not part of the standard hours and can be studied after this week |
| Week 14 | 8.1 · 8.2 (2 sessions) · 8.3 | Bootstrap, edge accuracy, CS-coefficient (4 sessions this week) |
| Week 15 | 9.1 · 9.2 · 9.3 · 10.1 | Reading papers, critique, reporting standards; project design (4 sessions this week) |
| Week 16 | 10.2 (2 sessions) · 10.3 | Capstone project: analysis, write-up and presentation |

## Modules & Lessons

### M0 Course Overview: Why Study CLPN

A map of the whole course: what questions CLPN tries to answer, which problems in social work and psychology research it addresses, and how, over the next 16 weeks, you will work step by step toward completing an analysis on your own.

- [0.1 Course Map, Learning Methods, and Tool Preparation](lessons/L0-1.md). Prerequisites: None. Objectives: Explain the order of the course's 11 modules and what each contributes to the final CLPN analysis; Know the structure every lesson follows: 'Intuition → Essential Math → R Code → Concept Check → Exercises'; Set up your own study folder: a study log, a list of questions, and a code folder
- [0.2 From Total Scores to Symptom Interactions: Why CLPN Matters](lessons/L0-2.md). Prerequisites: 0.1. Objectives: Tell apart how the 'common cause' (latent variable) view and the 'network' view explain psychological problems; Use a social work example to explain why looking only at total scores loses information; Get a first idea of what 'cross-lagged' means: earlier A predicting later B; Know which questions CLPN can and cannot answer (a predictive relationship ≠ proven causation)

### M1 Statistics Foundations

Build statistical intuition from scratch. The math uses only basic calculus ideas you already know (sums, functions, an intuition for derivatives); the focus is on 'what is this number telling us?'

- [1.1 Variables and Measurement: Where Data Come From](lessons/L1-1.md). Prerequisites: 0.2. Objectives: Distinguish among levels of measurement: nominal, ordinal, interval, and ratio; Understand how Likert items are usually treated in analysis, and the debate around it; Distinguish items, scale scores and constructs
- [1.2 Distributions and Descriptive Statistics: Mean, Variance, and Standard Deviation](lessons/L1-2.md). Prerequisites: 1.1. Objectives: Calculate and interpret the mean, median, variance, and standard deviation; Read a histogram and describe the shape of a distribution (skewness, kurtosis, ceiling/floor effects); Understand the normal distribution and its 68–95–99.7 rule
- [1.3 Standardization and z-Scores](lessons/L1-3.md). Prerequisites: 1.2. Objectives: Convert raw scores to z-scores and interpret them; Understand why variables on different scales need standardizing before you compare them (groundwork for LASSO and standardized coefficients)
- [1.4 Covariance and Correlation: How Two Variables Co-Vary](lessons/L1-4.md). Prerequisites: 1.3. Objectives: Get an intuitive feel for covariance and correlation from scatter plots; Calculate Pearson's correlation coefficient r and interpret its direction and size; Know when Spearman's correlation and the polychoric correlation are appropriate; Keep in mind that correlation is not causation, and be able to give an example of a confounder
- [1.5 Sampling, Standard Errors, and Confidence Intervals](lessons/L1-5.md). Prerequisites: 1.4. Objectives: Distinguish population from sample and parameter from statistic; Use simulation to build an intuition for sampling distributions and standard errors; Interpret a 95% confidence interval correctly (and know the common misreadings)
- [1.6 Hypothesis Testing, p-Values, and Effect Sizes](lessons/L1-6.md). Prerequisites: 1.5. Objectives: Describe the logical steps of a null hypothesis test; Interpret p-values correctly and spot common misreadings; Distinguish statistical significance from practical importance (effect size); Understand Type I / Type II errors, statistical power, and the multiple comparisons problem

### M2 R and RStudio: From Scratch

An introduction to programming for complete beginners. You study it side by side with Module 1 (Statistics), alternating in Weeks 2–5 (see 'Recommended Pacing'): as soon as you learn a statistical idea, you do it in R. Module 3 (Regression) comes after.

- [2.1 Installing R and RStudio and Running Your First Line of Code](lessons/L2-1.md). Prerequisites: 0.1. Objectives: Install R and RStudio (Posit) on your computer and get to know its four panes; Tell the console from a script, and save .R files; Use R as a calculator, assign values with <-, and name objects; Use the help (?function_name), read error messages, and put together a question when asking others for help (a minimal reproducible example)
- [2.2 R Basic Syntax: Vectors, Data Types, and Functions](lessons/L2-2.md). Prerequisites: 2.1. Objectives: Create and index vectors, and understand R's 'vectorized' operations; Recognize data types: numeric, character, logical, factor; Understand NA (missing values) and na.rm = TRUE; Write a very simple function of your own
- [2.3 Data Frames and Introduction to the Tidyverse](lessons/L2-3.md). Prerequisites: 2.2. Objectives: Understand the structure of a data frame: rows = cases, columns = variables; Use the core dplyr verbs: select, filter, mutate, summarise, group_by; Chain steps together with the pipe |>
- [2.4 Installing Packages, Importing Data, and Project Management](lessons/L2-4.md). Prerequisites: 2.3. Objectives: Tell install.packages() (install once) from library() (load every session); Import CSV, Excel and SPSS (.sav) data (readr, readxl, haven); Use an RStudio Project and relative paths, and get into the habit of a reproducible folder structure
- [2.5 Descriptive Statistics, Correlation, and Regression in R](lessons/L2-5.md). Prerequisites: 2.4, 1.6. Objectives: Get descriptive statistics with psych::describe(); Compute a correlation matrix with cor() and handle missing values; Fit regressions with lm() and glm() and read the summary() output
- [2.6 Data Visualization with ggplot2 and Reproducible Reporting with Quarto / R Markdown](lessons/L2-6.md). Prerequisites: 2.5. Objectives: Draw histograms, scatter plots and grouped box plots with ggplot2; Understand the layered grammar: data + mappings + geometric objects; Use Quarto or R Markdown to produce a report that combines code, results and text (you will hand in the capstone project this way)

### M3 Regression Analysis

Regression is the 'engine' of CLPN: at heart, a CLPN runs one (regularized) regression for each variable at time point 2. This module goes from a single straight line to LASSO. Study it after Module 1 (Statistics) and Module 2 (R).

- [3.1 Simple Linear Regression: Making Predictions with a Straight Line](lessons/L3-1.md). Prerequisites: 1.4, 2.1. Objectives: Explain the intercept, slope, residuals and R²; Understand that least squares means making the sum of squared residuals as small as possible (using your intuition for derivatives); Fit a model with lm() in R and read the output
- [3.2 Multiple Regression and 'Controlling for Other Variables'](lessons/L3-2.md). Prerequisites: 3.1. Objectives: Explain what a partial regression coefficient means: 'with the other variables held constant'; Understand why coefficients change when you control for other variables (confounding, overlapping information); Recognize multicollinearity and its effects
- [3.3 Standardized Coefficients and Results Interpretation](lessons/L3-3.md). Prerequisites: 3.2, 1.3. Objectives: Distinguish the unstandardized coefficient b from the standardized coefficient β; Compare the relative size of predictors measured on different scales; Write a properly formatted sentence reporting a regression result
- [3.4 Introduction to Logistic Regression: Binary Outcomes](lessons/L3-4.md). Prerequisites: 3.2. Objectives: Understand why ordinary linear regression is not used when the outcome is binary (e.g. 'dropped out of school or not'); Read odds and odds ratios (OR); Know that glmnet can also fit logistic regression (family = "binomial"), in preparation for binary nodes
- [3.5 Overfitting and Regularization: Ridge, LASSO, and Cross-Validation](lessons/L3-5.md). Prerequisites: 3.3, 2.5. Objectives: Understand overfitting: with many variables and a small sample, a model 'memorizes noise'; Understand how LASSO, by penalizing the absolute values of the coefficients, pushes small coefficients to 0 (automatic variable selection); Understand the tuning parameter λ and k-fold cross-validation, and tell lambda.min from lambda.1se; Run glmnet / cv.glmnet in R for the first time

### M4 Longitudinal and Panel Data

A CLPN needs 'the same people, measured at several time points, with the same items.' This module explains how such data are structured and prepared, and the biggest headache: missing data and dropout.

- [4.1 The Language of Longitudinal Design: Waves, Time Lags, Within-Person and Between-Person Effects](lessons/L4-1.md). Prerequisites: 1.6. Objectives: Distinguish cross-sectional, repeated cross-sectional and panel (longitudinal) designs; Understand how the choice of waves and of the time lag affects which effects you can see; Make a first distinction between between-person differences and within-person change; Understand what measurement invariance basically means
- [4.2 Wide vs. Long Formats: Data Reshaping](lessons/L4-2.md). Prerequisites: 4.1, 2.3. Objectives: Distinguish wide format (one row per person) from long format (one row per person per wave); Convert between them with tidyr::pivot_longer() / pivot_wider(); Prepare a 'T1 item matrix + T2 item matrix' for a CLPN, with the cases matched one to one
- [4.3 Missing Data and Participant Attrition](lessons/L4-3.md). Prerequisites: 4.2. Objectives: Distinguish the three missingness mechanisms MCAR, MAR and MNAR, and what they mean; Understand how attrition threatens longitudinal conclusions, and be able to do an attrition analysis; Compare the pros and cons of listwise deletion, pairwise deletion, FIML and multiple imputation; Run a simple multiple imputation with mice, and know the usual approaches in network analysis

### M5 Traditional Cross-Lagged Panel Models (CLPM) and RI-CLPM

A CLPN can be seen as an 'item-level network version' of the CLPM. First understand autoregressive and cross-lagged paths at the construct (total-score) level, then Hamaker et al.'s key criticism of the CLPM; only then can you read a CLPN correctly and write its limitations honestly.

- [5.1 Intuition of the CLPM: Autoregressive and Cross-Lagged Paths](lessons/L5-1.md). Prerequisites: 3.2, 4.1. Objectives: Draw the path diagram of a two-variable, multi-wave CLPM; Distinguish autoregressive paths (stability) from cross-lagged paths (predicting another variable); Understand what same-time-point (residual) correlations mean; Understand structural equation modeling (SEM) and the basic symbols of path diagrams
- [5.2 Fitting CLPM with lavaan and Evaluating Model Fit](lessons/L5-2.md). Prerequisites: 5.1, 2.5. Objectives: Write and fit a two-variable, three-wave CLPM in lavaan syntax; Read parameter estimates and fit indices (χ², CFI, TLI, RMSEA, SRMR); Understand what equality constraints (equal paths across waves) are for
- [5.3 RI-CLPM: Separating Stable Trait Differences from Within-Person Fluctuations](lessons/L5-3.md). Prerequisites: 5.2. Objectives: Understand the core criticism by Hamaker, Kuiper & Grasman (2015): the CLPM mixes up between-person and within-person effects; Understand that the random intercept represents stable, trait-like differences between individuals; Compare CLPM and RI-CLPM results and explain the differences; Know that an RI-CLPM needs at least 3 waves
- [5.4 From Prediction to Causality: What Longitudinal Models Can and Cannot Claim](lessons/L5-4.md). Prerequisites: 5.3. Objectives: Distinguish 'prediction over time' (Granger-style) from causal effects; Recognize threats such as unmeasured confounding, the time lag, and measurement error; Practice writing longitudinal results in cautious, accurate language

### M6 Foundations of Network Psychometrics

Learn all the basics of psychological networks on cross-sectional data first: partial correlations, GGMs, regularization, visualization, centrality. CLPN estimation, plotting and centrality indices build directly on these ideas.

- [6.1 The Language of Networks: Nodes, Edges, Weights, and Adjacency Matrices](lessons/L6-1.md). Prerequisites: 1.4. Objectives: Say what nodes, edges, weights, and directed / undirected mean; Convert between a network plot and its weights matrix; Understand that in a psychological network, node = item/symptom and edge = statistical association
- [6.2 Partial Correlation Networks and Gaussian Graphical Models (GGMs)](lessons/L6-2.md). Prerequisites: 6.1, 3.2. Objectives: Understand partial correlation: the association left between two variables after controlling for all the others; Understand conditional independence and 'no edge' in a GGM; Know how the precision matrix (the inverse of the covariance matrix) relates to partial correlations (background only); Compare correlation and partial correlation networks and see why they differ so much
- [6.3 Regularized Network Estimation: LASSO, Graphical LASSO, and EBICglasso](lessons/L6-3.md). Prerequisites: 6.2, 3.5. Objectives: Understand why, with limited samples, regularization is needed to avoid 'a screen full of tiny edges'; Understand the graphical lasso, EBIC model selection, and the role of the hyperparameter γ; Know when EBICglasso is appropriate and its limits
- [6.4 Estimating and Visualizing Networks with qgraph and bootnet](lessons/L6-4.md). Prerequisites: 6.3, 2.6. Objectives: Estimate an EBICglasso network with bootnet::estimateNetwork(); Use the qgraph plotting arguments: layout, groups, labels, legend, maximum; Use the same layout across several network plots so they can be compared (averageLayout)
- [6.5 Centrality Indices: Strength, Expected Influence, and Bridge Centrality](lessons/L6-5.md). Prerequisites: 6.4. Objectives: Calculate and interpret strength and expected influence (EI); Understand why EI is more suitable than strength when there are negative edges (Robinaugh et al., 2016); Understand bridge centrality (Jones, Ma & McNally, 2021) and how it relates to comorbidity research; Know that betweenness and closeness are often unstable in psychological networks and should be used with care

### M7 Cross-Lagged Panel Networks (CLPN)

The core module. CLPN was proposed by Wysocki, van Bork, Cramer and Rhemtulla (2022 preprint; published in 2025 as 'Cross-lagged panel networks'). The main line of this module teaches the simplified 'LASSO-only' version most common in applied research (e.g. Funkhouser et al., 2021): for each T2 item, run a LASSO-regularized regression on all T1 items and put the coefficients together into a directed network. Lesson 7.5 then introduces the full procedure recommended by Wysocki et al. (2025): LASSO edge selection → unpenalized re-estimation in lavaan (same-wave residual correlations, FIML, tests of equality across time) → in-/out-prediction, with runnable examples.

- [7.1 Model Logic of CLPN: Unpacking CLPM to the Item Level](lessons/L7-1.md). Prerequisites: 5.3, 6.5, 3.5. Objectives: Explain how CLPN differs from, and relates to, the CLPM (construct level) and cross-sectional networks (no time direction); Understand that each T2 node = one regression equation, and all the coefficients together form a p × p directed weights matrix; Distinguish autoregressive edges (diagonal) from cross-lagged edges (off-diagonal) in a CLPN; Understand what a CLPN edge means: the unique prediction of B at T2 from A at T1, controlling for all T1 nodes
- [7.2 Nodewise CLPN Estimation with glmnet](lessons/L7-2.md). Prerequisites: 7.1, 4.2. Objectives: Prepare and standardize matched T1 / T2 item matrices; Fit a LASSO regression for each T2 node with a loop + cv.glmnet(); Understand and record the key decisions: lambda.min or lambda.1se, number of folds, random seed, whether to add covariates; Arrange the coefficients into a directed weights matrix with row and column names, and check it is correct
- [7.3 CLPN Visualization and Interpretation](lessons/L7-3.md). Prerequisites: 7.2. Objectives: Plot a directed CLPN with qgraph (usually without the autoregressive loops, which are reported in a separate table); Color the nodes by construct and label them; if you show only the stronger edges for readability, say so in the figure note; Report the autoregressive edges and the strongest cross-lagged edges in tables; Write cautious, non-causal interpretations of the edges
- [7.4 Out-Expected Influence, In-Expected Influence, and Cross-Construct Bridging](lessons/L7-4.md). Prerequisites: 7.3. Objectives: Calculate and interpret out-expected influence (out-EI: how much a node predicts the other nodes in total) and in-expected influence (in-EI: how much a node is predicted by the other nodes in total); Tell 'predictive' nodes from 'predictable' nodes, and know the limits of these labels; Calculate bridge out-/in-EI using only the edges between constructs
- [7.5 Design Choices and Extensions: Multi-Wave Data, Covariates, and Within-Person Disentanglement](lessons/L7-5.md). Prerequisites: 7.4. Objectives: With 3 or more waves, estimate the T1→T2 and T2→T3 networks separately and discuss how well the structure replicates; Understand how and why to add covariates (such as age and gender); Understand how the standard CLPN mixes between-person and within-person effects, know the extensions in the literature (such as panel GVAR, psychonetrics), and know when a standard CLPN is not enough and you need to switch to these methods; Know how sample size, number of items and the interval between measurements affect a CLPN
- [7.6 Measurement Invariance and Sample Size Planning](lessons/L7-6.md) (optional advanced). Prerequisites: 5.2, 7.2. Objectives: Explain measurement invariance with social work examples: does the same item measure the same thing at different waves or in different groups?; Fit models in lavaan in the order configural → metric → scalar, judging each level with Δχ², ΔCFI and ΔRMSEA; if a level fails, use score tests to find the problem items and consider partial invariance; Explain, given that a CLPN uses observed items directly as nodes, why equal loadings are the prerequisite for comparing relationships (edges) across waves, and equal intercepts the prerequisite for comparing means; Use simulation to estimate the sample size needed to recover target edges, and name the assumptions that estimate depends on (true network, λ rule, number of nodes)
- [7.7 Between-Group Comparisons: Are Two Group CLPNs Identical?](lessons/L7-7.md) (optional advanced). Prerequisites: 7.2, 6.4. Objectives: Turn a question like 'are men's and women's loneliness–depression networks the same?' into a statistical question: what is compared, and what is the null hypothesis?; Understand the logic of a permutation test: shuffle the group labels and re-estimate to get the null distribution 'if the groups did not differ,' then see where the observed value falls; Calculate and interpret M (the edge with the largest difference), S (the difference in global strength) and differences in single edges, and know the multiple comparisons problem; Know that 'not significant ≠ the same,' and that group comparisons need very large samples; Know that NCT (NetworkComparisonTest) is used for cross-sectional networks, and the limits of applying it directly to a CLPN

### M8 Stability and Accuracy Assessment

A network can easily 'look meaningful' and yet be unstable. Following the framework of Epskamp, Borsboom & Fried (2018), this module shows you how to use the bootstrap to check whether edges and centrality can be trusted.

- [8.1 The Idea of the Bootstrap: Using the Sample to Simulate 'Running the Study Again'](lessons/L8-1.md). Prerequisites: 1.5, 2.5. Objectives: Understand the nonparametric bootstrap: resampling cases with replacement; Use the bootstrap to build an interval for a mean or a correlation; Understand why network analysis particularly needs accuracy checks
- [8.2 Edge-Weight Accuracy: bootnet and a Custom CLPN Estimation Function](lessons/L8-2.md). Prerequisites: 8.1, 7.4. Objectives: Wrap the estimation code from Lesson 7.2 in a function that bootnet's estimateNetwork(default = "none", fun = ..., directed = TRUE) can call; Run a nonparametric bootstrap and plot the bootstrap intervals of the edge weights; Use the edge-weight difference test and interpret it cautiously; Know what to keep in mind when reading bootstrap intervals under regularized estimation (they cannot be treated as strict confidence intervals)
- [8.3 Case-Dropping Bootstrap and the CS-Coefficient](lessons/L8-3.md). Prerequisites: 8.2. Objectives: Understand the case-dropping bootstrap: drop more and more of the sample and see whether the centrality ranking holds; Calculate and interpret the correlation stability coefficient (CS-coefficient), with the usual reference values (not below 0.25, preferably above 0.5); Report and judge the stability of out-EI / in-EI

### M9 Reading, Critique, and Reporting Standards

Getting the analysis to run is only half the job; the other half is reading other people's CLPN papers, spotting the problems, and reporting your own analysis to the standards.

- [9.1 How to Read an Empirical CLPN Paper](lessons/L9-1.md). Prerequisites: 8.3. Objectives: Use a structured checklist to pull out quickly: sample, waves, interval, nodes, estimation method, λ selection, stability results; Match the paper's tables and figures to each concept you have learned; Distinguish the authors' findings, their interpretations, and over-reaching inferences
- [9.2 Critical Appraisal: A Checklist of Common CLPN Problems](lessons/L9-2.md). Prerequisites: 9.1, 5.4. Objectives: Spot common problems such as over-reading centrality, causal wording, and mixing up between- and within-person effects; Evaluate the choice of nodes (overlapping item content, reliability of single items); Judge whether the sample size, missing data handling and interval are reasonable; Know the overall challenges of network methodology (Fried & Cramer, 2017)
- [9.3 Reporting Standards: Writing Methods and Results Others Can Check](lessons/L9-3.md). Prerequisites: 9.2. Objectives: Learn the Burger et al. (2023) reporting standards for cross-sectional networks and carry them over to CLPN; List what a CLPN Methods section must report (data, missing data handling, standardization, estimation function and λ choice, seed, software versions, stability checks); Know the basics of sharing code and data (OSF) and of preregistration

### M10 Capstone Project: A Complete CLPN Analysis

Carry out a complete CLPN on your own, from the data to the written results. The default is the three-wave simulated data with a known true structure (4 loneliness items + 5 depression items, N = 800); if you can, you may use a public longitudinal dataset instead, after reading its license and citation requirements.

- [10.1 Project Design, Data Preparation, and Analysis Plan](lessons/L10-1.md). Prerequisites: 9.3. Objectives: Pose a clear, non-causally worded research question; Do the data cleaning, reverse scoring, and missing data and attrition analysis; Write a one-page analysis plan (a simple preregistration): nodes, λ rule, seed, stability checks, sensitivity analyses, including the required Wysocki et al. (2025) full procedure, and state in advance how you will interpret disagreement between the two analyses
- [10.2 Complete Analysis: Estimation, Visualization, Centrality, and Stability](lessons/L10-2.md). Prerequisites: 10.1. Objectives: In one Quarto project: descriptive statistics → CLPN estimation → plot → out/in-EI and bridge EI → bootstrap edge accuracy → CS-coefficients → at least one sensitivity analysis; With simulated data: compare the results with the true structure to judge how well the method works; Produce figures and tables ready for submission; Do the required sensitivity analysis: the Wysocki et al. (2025) full procedure (LASSO edge selection → unpenalized SEM re-estimation → tests of equality across time → pruning at p < .01 → in/out-prediction), and compare it edge by edge with the main analysis
- [10.3 Writing the Results and Presenting Them](lessons/L10-3.md). Prerequisites: 10.2. Objectives: Write an 800–1200-word 'Methods (analysis) + Results' in APA style, reporting the main analysis and the full-procedure sensitivity analysis side by side; Write an honest discussion of limitations (within- vs between-person, causation, sample, measurement); Explain your analysis clearly in 10 minutes and answer the questions readers or reviewers might raise
