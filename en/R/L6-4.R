# =====================================================================
# L6-4.R  Estimating and Visualizing Networks with qgraph and bootnet
#   (estimateNetwork + qgraph)
# Course example uses "9 depression items + 7 anxiety items": simulate cross-sectional data here
# =====================================================================
source("R/_setup.R")
suppressPackageStartupMessages({ library(bootnet); library(qgraph) })
log_open("L6-4_log.txt")
set.seed(64)
# genGGM generates a "true" network; ggmGenerator generates 4-category ordinal data from the network (nLevels = 4)
true_net <- genGGM(16, p = 0.15, nei = 2, propPositive = 0.9, constant = 1.5)
gen <- ggmGenerator(ordinal = TRUE, nLevels = 4)
items <- as.data.frame(gen(600, true_net))
colnames(items) <- c(paste0("D", 1:9), paste0("A", 1:7))   # D = Depression, A = Anxiety
write.csv(items, out("L6-4_dep_anx_items.csv"), row.names = FALSE)

# ---- Lesson Code ----
net <- estimateNetwork(items, default = "EBICglasso",
                       tuning = 0.5, corMethod = "cor_auto", verbose = FALSE)
png_open("L6-4_network.png", 1800, 1400)
plot(net, layout = "spring",
     groups = list(Depression = 1:9, Anxiety = 10:16),
     legend = TRUE, palette = "colorblind", title = "Depression-Anxiety EBICglasso Network")
invisible(dev.off())
# Publication-ready PDF (vector graphic)
if (capabilities("cairo")) {
  cairo_pdf(out("L6-4_network.pdf"), 8, 6, family = plot_font)
  plot(net, layout = "spring", groups = list(Depression = 1:9, Anxiety = 10:16), legend = TRUE, palette = "colorblind")
  invisible(dev.off())
}
cat("Estimated network number of edges =", sum(net$graph[upper.tri(net$graph)] != 0), "\n")
saveRDS(net, out("L6-4_net.rds"))
log_close()
