library("tidyverse")
preprocess <- read_csv("Bioinformatik/Genome Scale Algorithms/gr_GSA_naotei/5_read_mapper/timetests/preprocess.csv")

preprocess %>% ggplot(aes(n, t)) +
    geom_point() +
    labs(title = "-p (preprocessing)", x = "length of genome", y = "time in seconds")
