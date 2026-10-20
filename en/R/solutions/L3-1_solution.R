# Exercise Solutions L3-1: Social support predicting depression; hand-drawn line vs. OLS
source("R/_setup.R")
log_open("sol_L3-1_log.txt")
dat <- read_course_data(); dat$dep <- rowSums(dat[, paste0(dep_items, "_t1")])
fit <- lm(dep ~ social_support_t1, dat); print(coef(fit))
my_line <- c(10, -1.8)          # E.g., hand-drawn line on scatterplot: y = 10 - 1.8x
rss <- function(b) sum((dat$dep - (b[1] + b[2] * dat$social_support_t1))^2)
cat("Hand-drawn RSS =", round(rss(my_line)), "; OLS RSS =", round(rss(coef(fit))), "(OLS is always minimal)\n")

# ---- 3.1-A Using the starting values from the lecture code block: my_b0 = 7, my_b1 = -1 ----
cat("\n3.1-A: Lecture template line y = 7 - 1x RSS =", round(rss(c(7, -1)), 1),
    "; OLS intercept =", round(coef(fit)[1], 2), " slope =", round(coef(fit)[2], 2),
    " RSS =", round(rss(coef(fit)), 1), "\n")
# Why hand-drawn lines are often steeper than OLS: SD line slope = -sd(y)/sd(x); OLS slope = r * sd(y)/sd(x)
r <- cor(dat$social_support_t1, dat$dep)
cat("SD line slope =", round(-sd(dat$dep) / sd(dat$social_support_t1), 2),
    "; OLS slope = r * sd(y)/sd(x) =", round(r * sd(dat$dep) / sd(dat$social_support_t1), 2), "\n")

# ---- 3.1-B Numbers required for reporting ----
sm <- summary(fit)
cat("\n3.1-B: b =", round(coef(fit)[2], 2), " SE =", round(sm$coefficients[2, 2], 2),
    " p =", signif(sm$coefficients[2, 4], 3), " R^2 =", round(sm$r.squared, 3), "\n")

# ---- 3.1-C Paper-and-pencil problem verified with R ----
x <- c(1, 2, 3, 4); y <- c(2, 4, 5, 5)
b1 <- sum((x - mean(x)) * (y - mean(y))) / sum((x - mean(x))^2)
b0 <- mean(y) - b1 * mean(x)
e  <- y - (b0 + b1 * x)
cat("\n3.1-C: b1 =", b1, " b0 =", b0, "\nResiduals: ", e, "; Sum of residuals =", sum(e), "\n")
print(coef(lm(y ~ x)))         # Compare with lm()
log_close()
