import naive_sa # Suffix array creation.
import sa2
import pickle # Object serialization.
#from t4 import t4_genome as t4 # Genome for test purposes.

def dprint(*args):
    pass
    #print('computing', *args)


class search_bwt:
    def __init__(self, S, title = 'anonymous_read'):
        """ Common to both preprocess and search. """
        self.title = title # Used to keep track of the id of the read.
        self.sentinel = '$'
        self.S = S.lower() + self.sentinel


    def main_preprocess(self):
        """ Computes and saves anything needed for later searching. """
        dprint('sa')
        
        #self.sa = naive_sa.sa(self.S)[0] # suffix array from sort.
        self.sa = sa2.sa(self.S)
        

        # Debug:
        if not True:
            self.sa_all = naive_sa.sa(self.S)
            print('i', 'sa', 'sa_str', sep = '\t')
            print('-----------------')
            for h, (i, j) in enumerate(zip(*self.sa_all)):
                print(h, i, j, sep = '\t')
            print()

        dprint('alphabet')
        self.alphabet = sorted(set(self.S))

        dprint('bwt')
        self.bwt = self.compute_bwt()

        dprint('c table')
        self.C_table = [i for i in self.compute_C_table()]

        dprint('o table')
        self.O = self.compute_O_table()

        self.inv_alph = {j: i for i, j in enumerate(self.alphabet)} # reverse lookup in alphabet f('$') = 0

        dprint('preprocessing done')


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



    def simplify_cigar(self, input):

        prev = input[0]
        count = 1
        rv = ''
        for i in range(1,len(input)):
            if input[i] == prev:
                count += 1
            else:
                rv += str(count) + prev
                count = 1
            
            prev = input[i]

        rv += str(count) + input[i]

        return rv

    def calculate_D(self, pattern):
        L = 0
        R = len(self.S) - 1
        z = 0
        D = [0 for i in range(len(self.S))]
        for i in range(len(pattern)):
            new_L = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], L-1) * (L != 0) + 1
            new_R = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], R)
            if L > R:
                L = 0
                R = len(self.S) - 1
                z += 1





    
    def rec_approx(self, pattern, d):
        
        """ Recursive edit search. """
        results = []
        
        def inexrecur(i, d, L, R, cigar):
            """
            i:      Position in pattern.
            d:      Number of edits left.
            L, R:   Left and right pointers in suffix array.
            cigar:  The CIGAR-string for the match.
            """

            #print(i, d, (L, R), cigar)

            if d < 0:
                return

    
            if i < 0: # Base case.
                #if cigar[-1] != 'D':
                results.append(([self.sa[i] for i in range(L, R+1)], cigar)) #                Short version


                return
            
            # match_L = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], L-1) * (L != 0) + 1
            # match_R = self.C_table[self.inv_alph[pattern[i]]] + self.access_O(pattern[i], R)

            # Insertion
            inexrecur(i-1, d-1, L, R, 'I' + cigar)

            for b in self.alphabet[1:]:
                new_L = self.C_table[self.inv_alph[b]] + self.access_O(b, L-1) * (L != 0) + 1
                new_R = self.C_table[self.inv_alph[b]] + self.access_O(b, R)

                if new_L <= new_R:
                    if i < len(pattern) -1:
                        inexrecur(i, d-1, new_L, new_R, 'D' + cigar)
                    if b == pattern[i]:
                        inexrecur(i-1, d, new_L, new_R, 'M' + cigar)
                    else:
                        inexrecur(i-1, d-1, new_L, new_R, 'M' + cigar)
                        pass



        # Initialize values.
        i = len(pattern) - 1
        d = d
        L = 0
        R = len(self.sa) - 1
        cigar = ''


        inexrecur(i, d, L, R, cigar)
        return results


    
    


    def find_positions(self, pattern, d):
        """ Backwards compatibility. """
        for positions, cigar in self.rec_approx(pattern, d):
            for position in positions:
                yield position, self.simplify_cigar(cigar)


if __name__ == "__main__":

    S = 'mississippimississippi'
    
    debug_header = True
    if debug_header:
        print('i', 'd', 'L', 'R', 'pos', S, sep = '\t')

    o = search_bwt(S)
    o.main_preprocess()
    pattern = 'sippimissi'
    o.calculate_D(pattern)
        

    def test_single():
        """ Used to test a single case. """
        run = o.rec_approx(pattern, 1)
        for i in run:
            print(*i, sep = '\t')
            
    # test_single()


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



        print('\nInsertions')
        for rippling_pattern in ripple_I('m'):
            print(rippling_pattern, end = ' -> ')
            for search_res in o.rec_approx(rippling_pattern, d = 1):
                print(search_res, end = ', ')
            print()
    
        print('\nDeletions')
        for rippling_pattern in ripple_D():
            print(rippling_pattern, end = ' -> ')
            for search_res in o.rec_approx(rippling_pattern, d = 1):
                print(search_res, end = ', ')
            print()
    
        print('\nSubstitutions')
        for rippling_pattern in ripple_m('m'):
            print(rippling_pattern, end = ' -> ')
            for search_res in o.rec_approx(rippling_pattern, d = 1):
                print(search_res, end = ', ')
            print()
    
    #test_multiple()

    for position, cigar in o.find_positions('sippimissi', 1):
        print(position, cigar)


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