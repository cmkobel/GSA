import naive_sa
from t4 import t4_genome as t4

#S = t4()
S = 'Mississippi'
sentinel = '$'
S = S.lower() + sentinel
sa, sa_str = naive_sa.sa(S)
alphabet = sorted(set(S))


def compute_bwt():
    return [S[i-1] for i in sa]


bwt = compute_bwt()


def compute_C_table():
    counts = {}
    # Set counts-table to zero.
    for i in alphabet:
        counts[i] = 0

    # Count occurences of letters
    for i in S:
        counts[i] +=1

    # Calc. prefix sum.
    for i in counts:
        if i == alphabet[0]:
            yield 0
        elif i == alphabet[1]:
            yield 0
            prev = counts[i]
        else:
            yield prev
            prev += counts[i]


C_table = [i for i in compute_C_table()]


def compute_O_table():
    O = [[] for i in range(len(S))]

    row = [0 for i in range(len(C_table))]
    for _i, i in enumerate(bwt):

        row[alphabet.index(i)] += 1
        O[_i] = [i for i in row]

    return O


O = compute_O_table()


# Helper funcs/vars for O and C-table
inv_alph = {j: i for i, j in enumerate(alphabet)} # reverse lookup in alphabet f('$') = 0
def access_O(char, idx):
    return O[idx][inv_alph[char]]

def present_O():
    """ Pretty prints the O-table for debug. 
        mississippi$
            i   p   s   s   m   $   p   i   s   s   i   i   
        $   0   0   0   0   0   1   1   1   1   1   1   1   
        i   1   1   1   1   1   1   1   2   2   2   3   4   
        m   0   0   0   0   1   1   1   1   1   1   1   1   
        p   0   1   1   1   1   1   2   2   2   2   2   2   
        s   0   0   1   2   2   2   2   2   3   4   4   4   
    """
    print(S)
    print('\t', end = '')
    for char in bwt:
        print(char, '\t', end = '')
    print()
    for char in alphabet:
        print(char, '\t', end = '')
        for i in range(len(S)):
            print(access_O(char, i), '\t', end = '')
        print()

present_O()
#print(access_O('p', 1))











