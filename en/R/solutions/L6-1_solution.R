# Solution L6-1: Constructing a 5x5 weight matrix and plotting with qgraph
source("R/_setup.R"); library(qgraph)
log_open("sol_L6-1_log.txt")
labs <- c("Loneliness", "Insomnia", "Fatigue", "Depressed", "Social")
W <- matrix(0, 5, 5, dimnames = list(labs, labs))
W["Loneliness", "Depressed"] <- .4; W["Insomnia", "Fatigue"] <- .5; W["Fatigue", "Depressed"] <- .3; W["Loneliness", "Social"] <- -.35
W <- W + t(W)                                 # Undirected network -> symmetric
stopifnot(isSymmetric(W))
png_open("sol_L6-1_network.png", 1300, 1200); qgraph(W, labels = labs, edge.labels = TRUE, theme = "colorblind"); invisible(dev.off())
# Answer: Undirected network matrix is symmetric; in directed networks [i, j] = directed from i to j;
# thickness = |weight|, color = positive (blue) / negative (red).
log_close()
