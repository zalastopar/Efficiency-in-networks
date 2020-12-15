library(readr)
library(ggplot2)

Sim <- read.csv("Data/Sim.csv")

# Grid 4x3x2
grid_4x3x2 <- Sim[c(301:310), c(2:6)]

percent <- rep(c("0.01", "0.02", "0.03", "0.04", "0.05", "0.1", "0.15", "0.2", "0.25", "0.5"), 3)
vrsta <- c(rep("10", 10), rep("100", 10), rep("1000", 10))
napaka_gr <- c(abs(grid_4x3x2[, 2] - grid_4x3x2[,3]), abs(grid_4x3x2[, 2] - grid_4x3x2[,4]), abs(grid_4x3x2[, 2] - grid_4x3x2[,5]))
napake_grid <- data_frame("Percent" = percent, "value" = vrsta, "napaka" = napaka_gr)


graf_napaka_grid <- ggplot(napake_grid, aes(x = Percent, y = napaka, color = value, group = value)) + geom_line(size = 1) + 
  theme_classic() + labs(color = "Število poskousov", x = "Delež", y = "Absolutna napaka", title = "Napaka približkov za graf 4x3x2") +
  theme(legend.position = c(0.8, 0.8),legend.direction = "vertical") + 
  theme(panel.border = element_rect(colour = "black", fill=NA, size=1)) + 
  scale_color_manual(values = c("deeppink", "cyan", "green1"))
png("Vizualizacija/Grid_4x3x2.png")
print(graf_napaka_grid)
dev.off()

# Tree 5
tree_5 <- Sim[c(351:360), c(2:6)]
napaka_tr <- c(abs(tree_5[, 2] - tree_5[,3]), abs(tree_5[, 2] - tree_5[,4]), abs(tree_5[, 2] - tree_5[,5]))
napake_tree <- data_frame("Percent" = percent, "value" = vrsta, "napaka" = napaka_tr)

graf_napaka_tree <- ggplot(napake_tree, aes(x = Percent, y = napaka, color = value, group = value)) + geom_line(size = 1) + 
  theme_classic() + labs(color = "Število poskousov", x = "Delež", y = "Absolutna napaka", title = "Napaka približkov za drevo globine 5") +
  theme(legend.position = c(0.8, 0.8),legend.direction = "vertical") + 
  theme(panel.border = element_rect(colour = "black", fill=NA, size=1)) + 
  scale_color_manual(values = c("deeppink", "cyan", "green1"))

png("Vizualizacija/Tree_5.png")
print(graf_napaka_tree)
dev.off()


