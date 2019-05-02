import naive_sa
import pickle
from t4 import t4_genome as t4


class search_bwt:
    def __init__(self, S, title = 'anonymous_read'):
        """ Common to both preprocess and search. """
        self.title = title # Used to keep track of the id of the read.
        self.sentinel = '$'
        self.S = S.lower() + self.sentinel


    def main_preprocess(self):
        """ Computes and saves anything needed for later searching. """

        self.sa = naive_sa.sa(self.S)[0] # suffix array from sort.

        # Debug:
        if True:
            self.sa_all = naive_sa.sa(self.S)
            print('i', 'sa', 'sa_str', sep = '\t')
            print('-----------------')
            for h, (i, j) in enumerate(zip(*self.sa_all)):
                print(h, i, j, sep = '\t')
            print()

        self.alphabet = sorted(set(self.S))

        self.bwt = self.compute_bwt()
        self.C_table = [i for i in self.compute_C_table()]
        self.O = self.compute_O_table()
        self.inv_alph = {j: i for i, j in enumerate(self.alphabet)} # reverse lookup in alphabet f('$') = 0


    def compute_bwt(self):
        return [self.S[i-1] for i in self.sa]


    def compute_C_table(self):
        counts = {}
        # Set counts-table to zero.
        for i in self.alphabet:
            counts[i] = 0

        # Count occurences of letters
        for i in self.S:
            counts[i] +=1

        # Calc. prefix sum.
        for i in counts:
            if i == self.alphabet[0]:
                yield 0
            elif i == self.alphabet[1]:
                yield 0
                prev = counts[i]
            else:
                yield prev
                prev += counts[i]


    def compute_O_table(self):
        O = [[] for i in range(len(self.S))]


        row = [0 for i in range(len(self.C_table))]
        for _i, i in enumerate(self.bwt):

            row[self.alphabet.index(i)] += 1
            O[_i] = [i for i in row]

        return O



    # Helper funcs/vars for O and C-table

    def access_O(self, char, idx):
        return self.O[idx][self.inv_alph[char]]

    def present_O(self):
        """ Pretty prints the O-table for debug. """
        print(self.S)
        print('\t', end = '')
        for char in self.bwt:
            print(char, '\t', end = '')
        print()
        for char in self.alphabet:
            print(char, '\t', end = '')
            for i in range(len(self.S)):
                print(self.access_O(char, i), '\t', end = '')
            print()

        print()


    def iter_exact(self, pattern):
        """ Iterative exact search. """

        L = 0
        R = len(self.S)-1
        i = len(pattern)-1

        while i >= 0 and L <= R:

            # compute L(w[i...m]) from L(w[i+1...m])
            L = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], L-1) * (L != 0) + 1

            # compute R(w[i...m]) from R(w[i+1...m])
            R = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], R)
            i -= 1


        if i < 0 and L <= R:
            #print(L, R)
            #return [str(self.sa_str[i])[:len(pattern)] for i in range(L, R+1)]
            return [self.sa[i] for i in range(L, R+1)]
        else:
            #print(L,R)
            return []

    def rec_exact(self, pattern):
        """ Recursive exact search. """

        # Setup.
        L = 0
        R = len(self.S) - 1
        i = len(pattern) - 1


        def rec(i, L, R):
            if i < 0: # Base case.
                return [self.sa[i] for i in range(L, R+1)]

            L = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], L-1) * (L != 0) + 1
            # compute R(w[i...m]) from R(w[i+1...m])
            R = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], R)
            
            if L <= R:
                return rec(i-1, L, R)

        return rec(i, L, R)

    
    def rec_approx(self, pattern, d):
        """ Recursive edit search. """
        results = []
        def rec(i, d, L, R, cigar):
            """
            i:      Position in genome.
            d:      Number of edits left.
            L, R:   Left and right pointers in suffix array.
            cigar:  The CIGAR-string for the match. 
            """
            #print((i, d, L, R))

            if i < 0: # Base case.
                return results.append((i, d, L, R, [self.sa[i] for i in range(L, R+1)], cigar))

            # Deletion
            if d > 0:
                rec(i-1, d-1, L, R, 'D' + cigar)

            if L <= R: # At least one match.
                L = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], L-1) * (L != 0) + 1
                R = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], R)
            
            if L <= R: # At least one match.                
                # Match
                rec(i-1, d, L, R, 'M' + cigar)





        # Setup.
        i = len(pattern) - 1 # Hvert objekt kan kun have et pattern ad gangen.
        d = d
        L = 0
        R = len(self.S) - 1
        cigar = ''
        edit = 'match' # match | deletion | insertion | substitution

        rec(i, d, L, R, cigar)
        return results





if __name__ == "__main__":

    S = 'mississippi'

    o = search_bwt(S)
    o.main_preprocess()


    pattern = 'mississippi'
    print('i', 'd', 'L', 'R', 'pos', S, sep = '\t')
    for i in o.rec_approx(pattern, 1):        
        print(*i, sep = '\t')

"""
Cigar encoding

op  desc
M   Alignment match or mismatch 
I   Insertion to the reference
D   Deletion from the reference
"""


"""
i   sa  sa_str
-----------------
0   11  $
1   10  i$
2   7   ippi$
3   4   issippi$
4   1   ississippi$
5   0   mississippi$
6   9   pi$
7   8   ppi$
8   6   sippi$
9   3   sissippi$
10  5   ssippi$
11  2   ssissippi$
"""