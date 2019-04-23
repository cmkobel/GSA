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



# sa - suffix array
prep_bs <- read_csv("prep_bs.csv")


p_prep_bs1 = prep_bs %>% ggplot(aes(n, t)) + geom_line() + labs(y = "t [s]", x = "") #+ labs(title = 'some subtitle')
p_prep_bs2 = prep_bs %>% ggplot(aes(n, t/(n*log(n)))) + geom_line() + labs(x = "")
p_prep_bs3 = prep_bs %>% ggplot(aes(n, t/(n*sqrt(n)))) + geom_line() + labs(x = "")
p_prep_bs4 = prep_bs %>% ggplot(aes(n, t/(n^2))) + geom_line()



fancyarrange3(p_prep_bs1, p_prep_bs3, p_prep_bs4, 'Binary Search preprocessing', 'Creating a suffix array and sorting naively.\nEnterobacteria phage T4 genome.')



#sa %>%  mutate(ratio = s/(n^2)) %>%  View


# lcp - longest common prefix
lcp <- read_csv("lcp.csv")
p_lcp1 = lcp %>% ggplot(aes(n, s)) + geom_point()
p_lcp2 = lcp %>% ggplot(aes(n, s/(n*sqrt(n)))) + geom_point()
fancyarrange2(p_lcp1, p_lcp2, 'Longest Common Prefix')


# st - suffix tree
st <- read_csv("st.csv")
p_st1 = st %>% ggplot(aes(n, s)) + geom_point()
p_st2 = st %>% ggplot(aes(n, s/(n))) + geom_point()
p_st3 = st %>% ggplot(aes(n, s/n^2)) + geom_point()


fancyarrange3(p_st1, p_st2, p_st3, 'Suffix Tree')





