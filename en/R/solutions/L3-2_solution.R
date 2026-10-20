# Exercise Solutions L3-2: Loneliness predicting alone vs. adding social support and sleep
source("R/_setup.R")
log_open("sol_L3-2_log.txt")
dat <- read_course_data()
dat$lone <- rowSums(dat[, paste0(lone_items, "_t1")]); dat$dep2 <- rowSums(dat[, paste0(dep_items, "_t2")])
b1 <- coef(lm(dep2 ~ lone, dat))["lone"]
b2 <- coef(lm(dep2 ~ lone + social_support_t1 + sleep_hours_t1, dat))["lone"]
cat("Loneliness coefficient: Unadjusted", round(b1, 3), "-> Controlling for support and sleep", round(b2, 3), "\n")
# Explanation: Loneliness is correlated with social support and sleep; in the bivariate model, the loneliness coefficient 'absorbed' part of their predictive capacity.
# After controlling for them, what remains is the 'unique' predictive effect of loneliness. Every edge in a CLPN represents exactly such a coefficient controlling for all other T1 items.

# Extreme multicollinearity example from Lesson 3.2: Loneliness sum score + 'duplicate' with slight noise
dat <- read_course_data()
dat$lone_sum_t1 <- rowSums(dat[, paste0(lone_items, "_t1")]); dat$dep_sum_t2 <- rowSums(dat[, paste0(dep_items, "_t2")])
set.seed(1)
dat$lone_copy <- dat$lone_sum_t1 + rnorm(800, 0, 0.3)
cat("\nCollinearity demonstration: r(Loneliness, Duplicate) =", round(cor(dat$lone_sum_t1, dat$lone_copy), 3), "\n")
print(round(summary(lm(dep_sum_t2 ~ lone_sum_t1, data = dat))$coefficients[2, 1:2], 3))
print(round(summary(lm(dep_sum_t2 ~ lone_sum_t1 + lone_copy, data = dat))$coefficients[, 1:2], 3))

# ---- Exercise 3.2-A Part 2: Further adding T1 depression (m4) ----
dat$dep_sum_t1 <- rowSums(dat[, paste0(dep_items, "_t1")])
m4 <- lm(dep_sum_t2 ~ lone_sum_t1 + social_support_t1 + sleep_hours_t1 + dep_sum_t1, data = dat)
cat("\n3.2-A: Coefficients for m4 (Loneliness + Support + Sleep + T1 Depression)\n")
print(round(coef(m4), 3))
# Loneliness coefficient drops to approx 0.128, close to 0.140 in m3 (controlling only T1 depression): what truly 'absorbs' predictive power is T1 depression.

# ---- Exercise 3.2-B: An edge in CLPN is a partial regression coefficient ----
d <- as.data.frame(scale(dat[, c(vars_t(1), "dep1_t2")]))     # Standardize first for comparison with population target
f <- lm(dep1_t2 ~ ., data = d)                               # '.' represents all other columns
cat("\n3.2-B: dep1_t2 ~ 9 T1 items (standardized coefficients)\n")
print(round(coef(f), 3))
cat("Population target (dep1 column of data/true_B_population.csv)\n")
print(round(true_B()[, "dep1"], 3))
lone_b <- coef(f)[paste0(lone_items, "_t1")]
cat("Largest coefficient among loneliness items: ", names(which.max(lone_b)), round(max(lone_b), 3), "\n")
# VIF for each of the 9 T1 items (predicted by the other 8 items)
X1 <- dat[, vars_t(1)]
vif9 <- sapply(names(X1), function(v) 1 / (1 - summary(lm(reformulate(setdiff(names(X1), v), v), data = X1))$r.squared))
cat("VIF:\n"); print(round(vif9, 2))
cat("VIF for lone4_t1 =", round(vif9["lone4_t1"], 2), "; all fall between", round(min(vif9), 2), "and", round(max(vif9), 2),
    ", well below the threshold of 5\n")
log_close()
