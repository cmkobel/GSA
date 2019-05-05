import naive_sa # Suffix array creation.
import pickle # Object serialization.
#from t4 import t4_genome as t4 # Genome for test purposes.


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
        if not True:
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

    
    def rec_approx(self, pattern, d):
        """ Recursive edit search. """
        results = []
        def recursive(i, d, L, R, cigar):
            """
            i:      Position in pattern.
            d:      Number of edits left.
            L, R:   Left and right pointers in suffix array.
            cigar:  The CIGAR-string for the match.
            """


            #print(i, d, (L, R), cigar)

            if i < 0: # Base case.
                results.append((i, d, L, R, [self.sa[i] for i in range(L, R+1)], cigar)) #  Debug version
                #results.append(([self.sa[i] for i in range(L, R+1)],cigar)) #                Short version
                return
            
            next_L = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], L-1) * (L != 0) + 1
            next_R = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], R)

            if d > 0 and next_L > next_R:               
                # Insert
                # Insert at this letter and move on: Continue with matching next i, without taking into account the L and R for the current i.
                recursive(i-1, d-1, L, R, 'I' + cigar)


                # Match the next letter in advance for Delete and Substite.
                next_letter_in_S = self.S[self.sa[L]-1]
                next_S_L = self.C_table[self.inv_alph[next_letter_in_S]] + self.access_O(next_letter_in_S, L-1) * (L != 0) + 1
                next_S_R = self.C_table[self.inv_alph[next_letter_in_S]] + self.access_O(next_letter_in_S, R)
                
                # Delete
                # Because the letter has been deleted from the pattern, we try to match the next char in S, instead of the next in pattern.                 
                recursive(i, d-1, next_S_L, next_S_R, 'D' + cigar)

                # Substitute
                recursive(i-1, d-1, next_S_L, next_S_R, 'm' + cigar)


            
            if next_L <= next_R: # At least one match.                
                # Match this letter and move on
                recursive(i-1, d, next_L, next_R, 'M' + cigar)


        # Initialize values.
        i = len(pattern) - 1
        d = d
        L = 0
        R = len(self.S) - 1
        cigar = ''


        recursive(i, d, L, R, cigar)
        return results



if __name__ == "__main__":

    S = 'mississippi'

    o = search_bwt(S)
    o.main_preprocess()
    pattern = 'mississippi'
    
    debug_header = True
    if debug_header:
        print('i', 'd', 'L', 'R', 'pos', S, sep = '\t')
        print('-----------------------------------')
        

    def test_single():
        """ Used to test a single case. """
        run = o.rec_approx(pattern, 1)
        for i in run:
            print(*i, sep = '\t')
            
    #test_single()


    def test_multiple():
        """ Used to test a rippling case. """
        def ripple_I(ins):
            for i in range(len(S)+1):
                yield f'{S[:i]}{ins}{S[i:]}'

        def ripple_m(ins): # substitutions
            for i in range(len(S)):
                yield f'{S[:i]}{ins}{S[i+1:]}'
        
        def ripple_D():
            for i in range(len(S)):
                yield f'{S[:i]}{S[i+1:]}'


        for rippling_pattern in ripple_I('m'):
            print(rippling_pattern, end = ' -> ')
            for search_res in o.rec_approx(rippling_pattern, d = 1):
                print(search_res, end = ', ')
            print()
    test_multiple()


"""
Cigar encoding

op  desc
M   Alignment match or mismatch
m   substitution 
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