library(ggplot2)


ggplot(data = commits, aes( x = date, y = org)) +
  geom_jitter(aes(col = org))
