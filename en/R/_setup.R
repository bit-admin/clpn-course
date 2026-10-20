# =====================================================================
# _setup.R — Common setup shared across all course R scripts
# Every Lx-y.R script begins with source("R/_setup.R"); you do not need to run it directly.
# It performs 4 tasks:
#   1) Locate the course root directory (clpn-course-en/ or clpn-course/) and set it as the working directory
#   2) Create the output directory R/output/
#   3) Configure a clean sans-serif font for PNG and ggplot2 figures
#   4) Define shared helper objects and functions used throughout the course, such as clpn_estimate()
# =====================================================================

## 1) Locate course root: walk upward until data/clpn_sim_wide.csv is found
find_root <- function() {
  d <- normalizePath(getwd())
  for (i in 1:4) {
    if (file.exists(file.path(d, "en", "data", "clpn_sim_wide.csv"))) return(file.path(d, "en"))
    if (file.exists(file.path(d, "data", "clpn_sim_wide.csv"))) return(d)
    d <- dirname(d)
  }
  stop("Cannot find course root: open clpn-course.Rproj in RStudio first.")
}
setwd(find_root())

## 2) Output directory
out_dir <- file.path("R", "output")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
out <- function(name) file.path(out_dir, name)   # out("L1-2_hist.png") -> "R/output/L1-2_hist.png"
# Scripts with upstream dependencies call need_output() at the top
need_output <- function(files, script, chain = NULL) {
  miss <- files[!file.exists(out(files))]
  if (length(miss) == 0) return(invisible(TRUE))
  stop("\nMissing prerequisite output file(s): ", paste(out(miss), collapse = ", "),
       "\nPlease run ", script, " first to generate them before running this script.",
       if (!is.null(chain)) paste0("\nFull execution order: ", chain) else "",
       "\n(Or run source(\"R/run_all.R\") to execute all scripts in course order.)", call. = FALSE)
}

## 3) Plot font setup
plot_font <- "sans"
png_open <- function(name, width = 1800, height = 1400, res = 220) {
  if (.Platform$OS.type == "windows") png(out(name), width, height, res = res)
  else png(out(name), width, height, res = res, type = if (capabilities("cairo")) "cairo" else NULL,
           family = plot_font)
  par(family = plot_font)
}
if (requireNamespace("ggplot2", quietly = TRUE))
  ggplot2::theme_set(ggplot2::theme_bw(base_family = plot_font))

## 4) Shared course objects & helper functions --------------------------------
items      <- c("lone1", "lone2", "lone3", "lone4", "dep1", "dep2", "dep3", "dep4", "dep5")
lone_items <- items[1:4]; dep_items <- items[5:9]
item_en    <- c(lone1 = "Lack of companionship", lone2 = "Feeling left out",
                lone3 = "Feeling isolated",      lone4 = "No one understands me",
                dep1  = "Depressed mood",        dep2  = "Loss of interest",
                dep3  = "Sleep problems",        dep4  = "Fatigue",
                dep5  = "Worthlessness")
comm        <- c(rep("Loneliness", 4), rep("Depression", 5))
groups_list <- list(Loneliness = 1:4, Depression = 5:9)
vars_t      <- function(t) paste0(items, "_t", t)
read_course_data <- function() read.csv("data/clpn_sim_wide.csv")
true_B      <- function() as.matrix(read.csv("data/true_B_population.csv", row.names = 1))

# ---- CLPN estimator (nodewise LASSO regression; "LASSO-only" CLPN,
#      Step 1 of the full procedure in Wysocki et al., 2025; for SEM re-estimation see R/L7-5b.R) ----
# X: item matrix at wave T; Y: item matrix at wave T+1 (same item order, same participants)
# rule: "lambda.min" (minimum CV error), "lambda.1se" (1-SE sparser rule), or "ebic" (Extended BIC)
# Returns p x p matrix B where B[k, j] = directed edge from item k at T to item j at T+1
clpn_estimate <- function(X, Y, rule = "lambda.min", nfolds = 10, covariates = NULL,
                          gamma = 0.5) {
  stem <- function(M) sub("_t[0-9]+$", "", colnames(M))
  if (ncol(X) != ncol(Y) || nrow(X) != nrow(Y))
    stop("X has ", nrow(X), " rows x ", ncol(X), " cols, while Y has ", nrow(Y), " rows x ", ncol(Y),
         " cols: both must have the same participants and items (Lesson 4.2: use vars_t(1) and vars_t(2)).", call. = FALSE)
  if (!is.null(colnames(X)) && !is.null(colnames(Y)) && !identical(stem(X), stem(Y)))
    stop("Item order in X and Y does not match (after stripping _t1/_t2 suffixes):\n  X: ", paste(stem(X), collapse = " "),
         "\n  Y: ", paste(stem(Y), collapse = " "),
         "\nSelect columns using dat[, vars_t(1)] and dat[, vars_t(2)] from the same item vector (Lesson 4.2).", call. = FALSE)
  for (nm in c("X", "Y", "covariates")) {
    M <- get(nm)
    if (!is.null(M) && anyNA(M))
      stop(nm, " contains ", sum(is.na(M)), " missing value(s) (NA) across ", sum(!stats::complete.cases(M)), " participant(s); ",
           "glmnet does not accept missing values.\nHandle missingness first—for example, apply na.omit() jointly to X, Y (and covariates) ",
           "or use multiple imputation (Lesson 4.3)—and report your handling method.", call. = FALSE)
  }
  X <- scale(as.matrix(X)); Y <- scale(as.matrix(Y))
  p <- ncol(X); labs <- if (is.null(colnames(X))) paste0("V", seq_len(p)) else stem(X)
  Z <- X; pf <- rep(1, p)
  if (!is.null(covariates)) {
    C <- scale(as.matrix(covariates)); Z <- cbind(X, C); pf <- c(pf, rep(0, ncol(C)))
  }
  B <- matrix(0, p, p, dimnames = list(labs, labs))
  for (j in seq_len(p)) {
    if (rule == "ebic") {
      fit <- glmnet::glmnet(Z, Y[, j], alpha = 1, penalty.factor = pf)
      n <- nrow(Z); rss <- (1 - fit$dev.ratio) * fit$nulldev
      ebic <- n * log(rss / n) + fit$df * log(n) + 2 * gamma * fit$df * log(ncol(Z))
      b <- as.numeric(coef(fit, s = fit$lambda[which.min(ebic)]))[-1]
    } else {
      cvfit <- glmnet::cv.glmnet(Z, Y[, j], alpha = 1, nfolds = nfolds, penalty.factor = pf)
      b <- as.numeric(coef(cvfit, s = rule))[-1]
    }
    B[, j] <- b[1:p]
  }
  B
}
# Zero out the diagonal (autoregressive edges), keeping only cross-lagged edges
cl_only <- function(B) { diag(B) <- 0; B }
# Convert weight matrix B into an edge list sorted by |weight| descending
edge_list <- function(B, drop_zero = TRUE) {
  e <- data.frame(from = rep(rownames(B), times = ncol(B)),
                  to   = rep(colnames(B), each = nrow(B)),
                  weight = as.vector(B))
  e$type <- ifelse(e$from == e$to, "AR (autoregressive)", "CL (cross-lagged)")
  if (drop_zero) e <- e[e$weight != 0, ]
  e[order(-abs(e$weight)), ]
}
# Log helper: print to console and write to R/output/<name>.txt simultaneously
log_open  <- function(name) sink(out(name), split = TRUE)
log_close <- function() sink()
