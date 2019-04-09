import naive_sa
from t4 import t4_genome as t4

#S = t4()
S = 'mississippi'
sentinel = '$'
S += sentinel
sa, sa_str = naive_sa.sa(S)
alphabet = sorted(set(S))


def O_table():


    def compute_c_table():

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

    
    bwt = [S[i-1] for i in sa]


    c_table = [i for i in compute_c_table()]


    O = [[] for i in range(len(S))]

    row = [0 for i in range(len(c_table))]
    for _i, i in enumerate(bwt):

        row[alphabet.index(i)] += 1
        O[_i] = [i for i in row]

    return O

print(O_table())












