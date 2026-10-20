# =====================================================================
# data_elsoc.R — Download & preprocess ELSOC real data (real-data case study; see materials/case_elsoc.html)
# Download & preprocess the ELSOC panel (Estudio Longitudinal Social de Chile 2016–2021)
#
# Data source (Harvard Dataverse recommended citation format):
#   Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022,
#   "Estudio Longitudinal Social de Chile 2016-2021", https://doi.org/10.7910/DVN/LQMURF,
#   Harvard Dataverse, V1, UNF:6:z/vWFguq9fg03YaOLWFddA== [fileUNF]
#   License: CC0 1.0 (as marked on the Dataverse dataset page), redistributable.
#   This script strictly pins to the V1 file ELSOC_Wide_2016_2021_v1.00_R.RData (4.8 MB, MD5 verified).
#
# The raw file data/elsoc/ELSOC_Wide_2016_2021_v1.00_R.RData and the preprocessed analysis file data/elsoc_phq8_wide.csv
# are both bundled with the course (in both the repository and clpn-course.zip). This script documents how the analysis file
# is derived from the raw file:
# When the raw file is present and its MD5 matches, it is used directly (no internet required);
# only if absent is it downloaded from Harvard Dataverse (no registration needed).
# It then writes data/elsoc_phq8_wide.csv, yielding a file identical to the bundled one. run_all.R runs this script.
#
# Processing: Keep only the original cohort (recruited in 2016); negative missing codes (-999 / -888 / -777 / -666) are set to NA;
# extract PHQ items 1–8 (PHQ-8), sex, and age across three waves (2016, 2017, 2018); original IDs are omitted.
# Why omit item 9: Item 9 asks about "thoughts of death or self-harm", a high-risk clinical item requiring follow-up.
# It is unsuitable as a standard node in pedagogical exercises, and research standard PHQ-8 likewise omits this item.
#
# Output: data/elsoc_phq8_wide.csv (for analysis), R/output/data_elsoc_log.txt (run log)
# Next step: R/case_elsoc.R (CLPN analysis). Runtime: download ~5–60 s (depending on connection), processing ~2 s.
# =====================================================================
source("R/_setup.R")
t_start <- Sys.time()

DOI       <- "10.7910/DVN/LQMURF"
VERSION   <- "V1"
FILE_ID   <- 6160174
FILE_NAME <- "ELSOC_Wide_2016_2021_v1.00_R.RData"
FILE_MD5  <- "a5a45571d39cf9db12e1949fdcb6fff2"
URL       <- paste0("https://dataverse.harvard.edu/api/access/datafile/", FILE_ID)
DATA_DIR  <- "data/elsoc"
dir.create(DATA_DIR, showWarnings = FALSE, recursive = TRUE)
raw_file  <- file.path(DATA_DIR, FILE_NAME)
if (!file.exists(raw_file) && file.exists(file.path("..", raw_file))) raw_file <- file.path("..", raw_file)

# Stop with instructions if download fails (no network connection, blocked by proxy, server maintenance, etc.)
download_failed <- function(why) {
  cat("\n================ Download Failed ================\n",
      "Failed to download ELSOC data from Harvard Dataverse.\n",
      "Reason (reported by R): ", why, "\n\n",
      "Suggested steps:\n",
      "1. Check connection: open https://doi.org/", DOI, " in your browser to verify access.\n",
      "2. On university or corporate networks, proxy configuration may be needed; or try another network (e.g., mobile hotspot).\n",
      "3. The server occasionally undergoes maintenance; retry after a short while.\n",
      "4. You can also download manually: find ", FILE_NAME, " on the webpage above,\n",
      "   and place it into ", DATA_DIR, "/ in the course directory, then re-run this script (the download step will be skipped).\n",
      "=================================================\n", sep = "")
  stop("ELSOC data download failed; see details above.", call. = FALSE)
}

md5_ok <- function(f) file.exists(f) && unname(tools::md5sum(f)) == FILE_MD5

# ---- Step 1: Download (skip if already downloaded and checksum matches) ----
if (md5_ok(raw_file)) {
  cat("Found existing downloaded file; skipping download: ", raw_file, "\n", sep = "")
} else {
  cat("Downloading ", FILE_NAME, " (~4.8 MB) from Harvard Dataverse...\n", sep = "")
  tmp <- tempfile(fileext = ".RData")
  old_timeout <- options(timeout = max(300, getOption("timeout")))
  res <- tryCatch(download.file(URL, tmp, mode = "wb", quiet = TRUE),
                  error = function(e) conditionMessage(e),
                  warning = function(w) conditionMessage(w))
  options(old_timeout)
  if (!identical(res, 0L) && !identical(res, 0)) {
    unlink(tmp); download_failed(as.character(res))
  }
  if (unname(tools::md5sum(tmp)) != FILE_MD5) {
    unlink(tmp)
    download_failed(paste0("Downloaded file is incomplete or not the expected version (MD5 checksum mismatch). ",
                           "If a new version of the dataset exists, this script strictly pins to ", VERSION, "."))
  }
  file.copy(tmp, raw_file, overwrite = TRUE); unlink(tmp)
  cat("Download complete; MD5 checksum verified.\n")
}

# ---- Step 2: Read and preprocess ------------------------------------
log_open("data_elsoc_log.txt")
cat("ELSOC data preprocessing log\n")
cat("Data: Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022,\n",
    "      \"Estudio Longitudinal Social de Chile 2016-2021\", https://doi.org/", DOI, ",\n",
    "      Harvard Dataverse, ", VERSION, " (CC0 1.0)\n", sep = "")
cat("File: ", FILE_NAME, "  MD5 = ", FILE_MD5, " (verified)\n\n", sep = "")

env <- new.env()
obj <- load(raw_file, envir = env)
d <- get(obj[1], envir = env)
cat("Raw data: ", nrow(d), " rows x ", ncol(d), " columns\n", sep = "")
cat("Sample composition (muestra): original sample ", sum(d$muestra == 1),
    " participants; refreshment sample (from 2018 onward) ", sum(d$muestra == 2), " participants\n", sep = "")

clean <- function(x) { x <- as.numeric(x); x[x < 0] <- NA; x }   # Negative numbers are various missing value codes
phq_en <- c("Little interest", "Depressed mood", "Sleep problems", "Fatigue", "Appetite change", "Trouble concentrating", "Low self-worth", "Psychomotor retardation")
cat("\nPHQ items (ELSOC item order swaps items 6 and 7 relative to standard PHQ-9; 1 = Never ... 5 = Almost every day):\n")
for (i in 1:8) {
  v <- sprintf("s11_%02d_w01", i)
  cat(sprintf("  phq%d  %-25s  %s\n", i, phq_en[i], sub(" \\(estado de animo\\) \\(2016\\)", "", attr(d[[v]], "label"))))
}
cat("  (Item 9 'thoughts of death or self-harm' not exported: high-risk item, excluded from pedagogical exercises.)\n")

keep <- d$muestra == 1                       # Original sample only; eligible across all three waves
w <- data.frame(id = seq_len(sum(keep)),     # New sequential ID; omit original idencuesta
                female = as.integer(clean(d$m0_sexo_w01[keep]) == 2),
                age = clean(d$m0_edad_w01[keep]))
for (t in 1:3) for (i in 1:8)
  w[[sprintf("phq%d_t%d", i, t)]] <- clean(d[[sprintf("s11_%02d_w%02d", i, t)]][keep])

phq_t <- function(t) sprintf("phq%d_t%d", 1:8, t)
cc <- function(ts) complete.cases(w[, unlist(lapply(ts, phq_t))])
cat("\nOriginal sample N =", nrow(w), "\n")
for (t in 1:3) cat(sprintf("  Wave %d (%d) complete PHQ-8: %d participants\n", t, 2015 + t, sum(cc(t))))
cat("  Complete across Waves 1–2: ", sum(cc(1:2)), " participants; complete across Waves 1–3: ", sum(cc(1:3)), " participants (for CLPN analysis)\n", sep = "")
a <- w[cc(1:3), ]
cat(sprintf("  Complete across Waves 1–3: %d females (%.1f%%); 2016 age M = %.1f, SD = %.1f, range %d–%d\n",
            sum(a$female, na.rm = TRUE), 100 * mean(a$female, na.rm = TRUE),
            mean(a$age, na.rm = TRUE), sd(a$age, na.rm = TRUE), min(a$age, na.rm = TRUE), max(a$age, na.rm = TRUE)))

out_csv <- "data/elsoc_phq8_wide.csv"
write.csv(w, out_csv, row.names = FALSE)
cat("\nWritten ", out_csv, ": ", nrow(w), " rows x ", ncol(w), " columns (identical to the bundled course file)\n", sep = "")
cat("Next step: source(\"R/case_elsoc.R\")\n")
log_close()
cat("Time elapsed: ", round(as.numeric(difftime(Sys.time(), t_start, units = "secs")), 1), " seconds\n", sep = "")
