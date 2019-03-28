library(gridExtra)
library(tidyverse)


fancyarrange3 = function(p1, p2, p3, sometitle) {
    gA <- ggplotGrob(p1)
    gB <- ggplotGrob(p2)
    gC <- ggplotGrob(p3)
    
    maxWidth = grid::unit.pmax(gA$widths[2:5], gB$widths[2:5], gC$widths[2:5])
    gA$widths[2:5] <- as.list(maxWidth)
    gB$widths[2:5] <- as.list(maxWidth)
    gC$widths[2:5] <- as.list(maxWidth)
    
    grid.arrange(gA, gB, gC, ncol=1, top = paste(sometitle))
}

fancyarrange2 = function(p1, p2, sometitle) {
    gA <- ggplotGrob(p1)
    gB <- ggplotGrob(p2)
    
    
    maxWidth = grid::unit.pmax(gA$widths[2:5], gB$widths[2:5])
    gA$widths[2:5] <- as.list(maxWidth)
    gB$widths[2:5] <- as.list(maxWidth)
    
    
    grid.arrange(gA, gB, ncol=1, top = paste(sometitle))
}



# sa - suffix array
sa <- read_csv("sa.csv")
p_sa1 = sa %>% ggplot(aes(n, s)) + geom_point()# + labs(title = 'some subtitle')
p_sa2 = sa %>% ggplot(aes(n, s/(n*log(n)))) + geom_point()
p_sa3 = sa %>% ggplot(aes(n, s/(n^2))) + geom_point()


fancyarrange3(p_sa1, p_sa2, p_sa3, 'Suffix Array')



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
p_st3 = st %>% ggplot(aes(n, s/(n*log(n)))) + geom_point()


fancyarrange3(p_st1, p_st2, p_st3, 'Suffix Tree')





