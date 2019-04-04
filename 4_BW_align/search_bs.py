import naive_sa
from math import log2



class search_bs:
    def __init__(self, S):
        self.S = S
        self.sa = naive_sa.sa(S)[0]


    def find_start_pos(self, p):
        j = -1
        L = 0
        R = len(S) - 1
        # print('sa')
        # print('==========')
        # for _i, i in enumerate(self.sa):
        #     print(f'{_i}: {i} {S[i:]}')
        # print('==========')

        #while True:
        for i in range(int(log2(len(S))+2)):
            M = -(-(R+L)//2) # ceiling integer division
            m_str = S[self.sa[M]:self.sa[M]+len(p)]




            if p == m_str:
                j = self.sa[M]


            elif p > m_str:
                L = M

            elif p < m_str:

                R = M-1

            
            if j != -1:
                break



        print(j)



S = 'noteuhsnatoheisthaosneuthsaonteidstaoheusnthaoseintdsanoteuhsnatoesitdasoethntaheduntahoudntaoheduthedunitaonstuehontehuidsantoehunst'


o = search_bs(S)
for i in range(len(S)):
    string = S[i:]
    print(string, end = ' ')
    o.find_start_pos(string)
o.find_start_pos(''.join([i for i in reversed(S)]))

# Når startpositionen er fundet, skal vi fortsætte indtil de næstkommede naboer ikke længere indeholder det samme.
