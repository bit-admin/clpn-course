# =====================================================================
# L6-1.R  The Language of Networks: Nodes, Edges, Weights, and Adjacency Matrices
#   (Nodes, edges, weights matrix)
# =====================================================================
source("R/_setup.R")
library(qgraph)
log_open("L6-1_log.txt")
labs5 <- c("Lonely", "Insomnia", "Fatigue", "Depressed", "Support")
# Undirected network: weights matrix is symmetric, W[i, j] = W[j, i]
W <- matrix(c( 0, .3,  0, .4, -.3,
              .3,  0, .5,  0,   0,
               0, .5,  0, .2,   0,
              .4,  0, .2,  0, -.2,
             -.3,  0,  0, -.2,  0), 5, 5, byrow = TRUE, dimnames = list(labs5, labs5))
print(W); cat("Symmetric?", isSymmetric(W), "\n")
cat("Density = number of non-zero edges / possible edges =", sum(W[upper.tri(W)] != 0), "/", choose(5, 2), "\n")
png_open("L6-1_undirected.png", 1400, 1300)
qgraph(W, labels = labs5, edge.labels = TRUE, theme = "colorblind", label.font = 1,
       title = "Undirected network: Blue/solid = positive edge, Red/dashed = negative edge (colorblind theme)")
invisible(dev.off())
# Directed network: W[i, j] indicates from i (row) pointing to j (column)
D <- matrix(0, 3, 3, dimnames = list(labs5[1:3], labs5[1:3])); D["Lonely", "Insomnia"] <- .4; D["Insomnia", "Fatigue"] <- .5
png_open("L6-1_directed.png", 1200, 1100)
qgraph(D, directed = TRUE, edge.labels = TRUE, asize = 6, theme = "colorblind", title = "Directed network: D[\"Lonely\",\"Insomnia\"] = Lonely -> Insomnia")
invisible(dev.off())
log_close()
