import naive_sa
from math import ceil, log2


class search_bs:
    def __init__(self, S):
        self.S = S
        self.sa, self.sa_str = naive_sa.sa(S)

    def find_start_position(self, pattern):
        """ The position returned by this function should be the first of the suffix arrays that equals. 
            This function could be put instide find_positions. """

        j = -1
        left = 0
        right = len(S) - 1
        theoretical_max = int(ceil(log2(len(S))))
        for i in range(theoretical_max):
            middle = -(-(right+left)//2) # ceiling integer division
            middle_string = S[self.sa[middle]:self.sa[middle]+len(pattern)]

            if pattern == middle_string:
                j = self.sa[middle]
            elif pattern > middle_string:
                left = middle
            elif pattern < middle_string:
                right = middle-1 # Because the pattern is in the upper part, we can exclude the lower.
            
            if j != -1:
                break


        return middle # The index of SA that contains the matching string.

    def find_positions(self, pattern):
        start_position = self.find_start_position(pattern)
        positions = []

        for i in self.sa[start_position:]:
            #print(i, S[i:i+len(pattern)])
            if S[i:i+len(pattern)] == pattern:
                positions.append(i)
            else:
                break

        return [(i, S[i:i+len(pattern)]) for i in positions]






S = 'mississippi'

o = search_bs(S)

positions = o.find_positions('iss')

print( positions)

