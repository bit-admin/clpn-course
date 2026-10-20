# Analysis Plan (Preregistration Template)
Research Question: To what extent do T1 loneliness items uniquely predict T2 depression items, and vice versa? (Avoid causal phrasing such as 'causes' or 'leads to')
Nodes: lone1–lone4, dep1–dep5 (9 items); Time Intervals: T1→T2 (primary analysis), T2→T3 (replication)
Estimation: Nodewise LASSO regression (glmnet), 10-fold CV, lambda.min; set.seed(2026); items z-standardized
Centrality: out-EI, in-EI, bridge out/in-EI (communities = Loneliness/Depression), excluding autoregressive edges
Stability: Nonparametric bootstrap (1,000 replications); case-dropping bootstrap (1,000 replications), interpreting rank order only if CS >= 0.25
Sensitivity: lambda.1se; including gender and age as unpenalized covariates; T2→T3 replication
Sensitivity (Required): Full procedure of Wysocki et al. (2025) (R/L10-2b.R): LASSO edge selection (T1→T2 and T2→T3, fixed to 0 only if 0 in both lags) -> unpenalized SEM re-estimation in lavaan (cross-sectional residual covariances within wave, FIML) -> cross-time invariance testing (nested chi-square + AIC/BIC) to select final model -> pruning at p < .01 -> in-/out-prediction; report edge-by-edge concordance with primary analysis, interpreting discordant edges exploratorily only
Missing Data: No missing data in this dataset; if present, report attrition analysis and apply multiple imputation (or FIML)
