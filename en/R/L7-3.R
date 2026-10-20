# =====================================================================
# L7-3.R  CLPN Visualization and Interpretation (Plotting & interpreting a CLPN)
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L7-3_log.txt")
dat <- read_course_data()
set.seed(2026)
B <- clpn_estimate(dat[, vars_t(1)], dat[, vars_t(2)], rule = "lambda.min")  # Same estimation as L7-2
CL <- cl_only(B); labs <- rownames(B)

# ---- Lesson Code: Directed Network Plot (omitting autoregressive self-loops) ----
png_open("L7-3_clpn.png", 1800, 1500)
qgraph(CL, directed = TRUE, layout = "spring",
       labels = labs, groups = list(Loneliness = 1:4, Depression = 5:9),
       theme = "colorblind", asize = 4, legend = TRUE,
       nodeNames = paste(labs, item_en[labs]), legend.cex = 0.45,
       title = "CLPN (T1 -> T2), lambda.min; autoregressive edges omitted")
invisible(dev.off())
# Display only |beta| >= 0.05 edges (display threshold: changes only the plot, not the model; must be stated in caption)
png_open("L7-3_clpn_threshold.png", 1800, 1500)
qgraph(CL, directed = TRUE, layout = "spring", labels = labs, groups = groups_list,
       theme = "colorblind", asize = 4, threshold = 0.05, legend = TRUE, curveAll = TRUE, curve = 0.4,
       title = "Cross-lagged edges with |beta| >= 0.05 only (note in caption)")
invisible(dev.off())

# Table: Autoregressive edges + strongest cross-lagged edges
cat("Autoregressive edges (AR):\n"); print(round(diag(B), 3))
el <- edge_list(CL)
el$from_en <- item_en[el$from]; el$to_en <- item_en[el$to]
cat("\nTop 10 strongest cross-lagged edges:\n"); print(head(el, 10), row.names = FALSE, digits = 3)
write.csv(el, out("L7-3_cl_edges.csv"), row.names = FALSE)
top_x <- el[comm[match(el$from, items)] != comm[match(el$to, items)], ][1, ]   # Strongest cross-construct edge
cat(sprintf("\nCautious reporting example: \"Controlling for all T1 items, T1 '%s' had the strongest unique (cross-construct) predictive effect on T2 '%s' (beta = %.2f)\",\nrather than \"%s causes %s\".\n",
    top_x$from_en, top_x$to_en, top_x$weight, top_x$from_en, top_x$to_en))
log_close()
