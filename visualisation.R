library(readr)
library(ggplot2)

Sim <- read.csv("Data/Sim.csv")

# Grid 4x3x2
grid_4x3x2 <- Sim[c(301:310), c(2:6)]
grid_4x3x2$Napaka_10 <- abs(grid_4x3x2[, 2] - grid_4x3x2[,3])
grid_4x3x2$Napaka_100 <- abs(grid_4x3x2[, 2] - grid_4x3x2[,4])
grid_4x3x2$Napaka_1000 <- abs(grid_4x3x2[, 2] - grid_4x3x2[,5])
grid_4x3x2$Percent <- c("0.01", "0.02", "0.03", "0.04", "0.05", "0.1", "0.15", "0.2", "0.25", "0.5")

x_axis <- c(0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5)
l <- plot(grid_4x3x2[, c(1, 6)], type = "l")
axis(1, labels = x_axis, at = x_axis)

m <- ggplot(grid_4x3x2, aes(x = Percent, y = Napaka_10)) + geom_point()
