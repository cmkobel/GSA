library(gridExtra)
library(tidyverse)


fancyarrange3 = function(p1, p2, p3, sometitle, somesubtitle) {
    gA <- ggplotGrob(p1)
    gB <- ggplotGrob(p2)
    gC <- ggplotGrob(p3)
    
    maxWidth = grid::unit.pmax(gA$widths[2:5], gB$widths[2:5], gC$widths[2:5])
    gA$widths[2:5] <- as.list(maxWidth)
    gB$widths[2:5] <- as.list(maxWidth)
    gC$widths[2:5] <- as.list(maxWidth)
    
    grid.arrange(gA, gB, gC, ncol=1, top = paste(sometitle), bottom = somesubtitle)
}

fancyarrange2 = function(p1, p2, sometitle, somesubtitle) {
    gA <- ggplotGrob(p1)
    gB <- ggplotGrob(p2)
    
    
    maxWidth = grid::unit.pmax(gA$widths[2:5], gB$widths[2:5])
    gA$widths[2:5] <- as.list(maxWidth)
    gB$widths[2:5] <- as.list(maxWidth)
    
    
    grid.arrange(gA, gB, ncol=1, top = paste(sometitle), bottom = somesubtitle)
}



# 1 Binary search: preprocessing
prep_bs <- read_csv("bs_prep.csv")

p_prep_bs1 = prep_bs %>% ggplot(aes(n, t)) + geom_line() + labs(y = "t [s]", x = "") #+ labs(title = 'some subtitle')
p_prep_bs2 = prep_bs %>% ggplot(aes(n, t/(n*log(n)))) + geom_line() + labs(x = "")
p_prep_bs3 = prep_bs %>% ggplot(aes(n, t/(n*sqrt(n)))) + geom_line() + labs(x = "")
p_prep_bs4 = prep_bs %>% ggplot(aes(n, t/(n^2))) + geom_line()

#fancyarrange3(p_prep_bs1, p_prep_bs3, p_prep_bs4, 'Binary Search: preprocessing', 'Creating a suffix array and sorting naively.\nEnterobacteria phage T4 genome.')


# 2 Binary search: searching
bs_search <- read_csv("bs_search.csv")

p_bs_search1 = bs_search %>% ggplot(aes(n, t)) + geom_point(alpha = 0.5, size = 1) + labs(y = "t [s]", x= "")# title = "Binary Search: searching", subtitle = "Searching for reads with size n.\nEnterobacteria phage T4 genome.")
p_bs_search2 = bs_search %>% ggplot(aes(n, t/(log(n)))) + geom_point(alpha = 0.5, size = 1)



fancyarrange2(p_bs_search1, p_bs_search2,  'Binary Search: searching', 'Searching for read with size n.\nEnterobacteria phage T4 genome.')


# 3 BW: preprocessing
prep_bw <- read_csv("bw_prep.csv")

p_prep_bw1 = prep_bw %>% ggplot(aes(n, t)) + geom_line() + labs(y = "t [s]", x = "") #+ labs(title = 'some subtitle')
p_prep_bw2 = prep_bw %>% ggplot(aes(n, t/(n*log(n)))) + geom_line() + labs(x = "")
p_prep_bw3 = prep_bw %>% ggplot(aes(n, t/(n*sqrt(n)))) + geom_line() + labs(x = "")
p_prep_bw4 = prep_bw %>% ggplot(aes(n, t/(n^2))) + geom_line()

#fancyarrange3(p_prep_bw1, p_prep_bw2, p_prep_bw4, 'Burrows wheeler: preprocessing', 'Creating: suffix array, c-table, o-table.\nEnterobacteria phage T4 genome.')


# 4 BW: searching
bw_search <- read_csv("bw_search.csv")

p_bw_search1 = bw_search %>% ggplot(aes(n, t)) + geom_point(alpha = 0.5, size = 1) + labs(y = "t [s]", x= "")# title = "Binary Search: searching", subtitle = "Searching for reads with size n.\nEnterobacteria phage T4 genome.")
p_bw_search2 = bw_search %>% ggplot(aes(n, t/n)) + geom_point(alpha = 0.5, size = 1)

fancyarrange2(p_bw_search1, p_bw_search2,  'Burrows Wheeler: searching', 'Searching for read with size n.\nEnterobacteria phage T4 genome.')




