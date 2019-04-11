import naive_sa
from t4 import t4_genome as t4


class bwt:
    def __init__(self, S):

        self.S = S.lower() + '$'
        self.sa, self.sa_str = naive_sa.sa(self.S)
        self.alphabet = sorted(set(self.S))

        for _i, (i, j) in enumerate(zip(self.sa, self.sa_str)):
            #print(_i, i, j)
            pass

        # Routine:
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
        """ Pretty prints the O-table for debug. 
            mississippi$
                i   p   s   s   m   $   p   i   s   s   i   i   
            $   0   0   0   0   0   1   1   1   1   1   1   1   
            i   1   1   1   1   1   1   1   2   2   2   3   4   
            m   0   0   0   0   1   1   1   1   1   1   1   1   
            p   0   1   1   1   1   1   2   2   2   2   2   2   
            s   0   0   1   2   2   2   2   2   3   4   4   4   
        """
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

    def find_positions(self, pattern):
        print(self.S)


        L = 0
        R = len(self.S)-1
        i = len(pattern)-1

        while i >= 0 and L <= R:
            # compute L(w[i...m]) from L(w[i+1...m])
            # if L == 0:
            #     L = self.C_table[self.inv_alph[pattern[i]]] + 1
            # else:
            L = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], L-1) * (L != 0) + 1

            # compute R(w[i...m]) from R(w[i+1...m])
            R = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], R)
            i -= 1

        if i < 0 and L <= R:
            print(L, R,[i for i in range(L, R+1)])
            return [str(self.sa_str[i]) for i in range(L, R+1)]
        else:
            print(L, R, [i for i in range(L, R+1)])
            return []



o = bwt('mississippi')
print(o.find_positions('i'))