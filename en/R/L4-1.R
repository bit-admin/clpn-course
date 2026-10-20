# =====================================================================
# L4-1.R  The language of longitudinal design: waves, within-person, and between-person
# Directly observing with course data: total variance = between-person (stable differences) + within-person (fluctuations over time)
# =====================================================================
source("R/_setup.R")
log_open("L4-1_log.txt")
dat <- read_course_data()
dep <- sapply(1:3, function(t) rowSums(dat[, paste0(dep_items, "_t", t)]))  # 800 x 3 matrix
colnames(dep) <- paste0("T", 1:3)
print(round(colMeans(dep), 2))                     # Mean depression per wave
print(round(cor(dep), 2))                          # Cross-wave correlations (rank-order stability)
person_mean <- rowMeans(dep)                       # 3-wave average per person = between-person component
within <- dep - person_mean                        # Deviations from person mean = within-person component
cat("\nBetween-person variance (between) ≈", round(var(person_mean), 2),
    "; within-person variance (within) ≈", round(mean(apply(within, 1, var)), 2), "\n")
png_open("L4-1_spaghetti.png", 1600, 1200)
set.seed(3); idx <- sample(nrow(dep), 30)
matplot(1:3, t(dep[idx, ]), type = "l", lty = 1, col = rgb(0, 0, 1, .4), xaxt = "n",
        xlab = "Wave", ylab = "Depression sum score", main = "Depression trajectories for 30 individuals (spaghetti plot)")
axis(1, 1:3, paste0("T", 1:3)); lines(1:3, colMeans(dep), lwd = 4, col = "red")
invisible(dev.off())

# ---- Supplementary: between-person vs. within-person correlation; multilevel model variance components ----
lone <- sapply(1:3, function(t) rowSums(dat[, paste0(lone_items, "_t", t)]))
print(cor(rowMeans(lone), rowMeans(dep)))                            # Between-person: correlation between person means
print(cor(as.vector(lone - rowMeans(lone)), as.vector(dep - rowMeans(dep))))   # Within-person: correlation between deviations
# Estimate variance components and ICC using multilevel modeling (requires lme4 package: install.packages("lme4"))
long <- data.frame(id = rep(1:800, 3), y = as.vector(dep))
m <- lme4::lmer(y ~ 1 + (1 | id), data = long)
print(as.data.frame(lme4::VarCorr(m))[, c("grp", "vcov")])
log_close()
