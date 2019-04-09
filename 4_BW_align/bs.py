import naive_sa
from math import ceil, log2

class search_bs:
    def __init__(self, S):
        self.S = S
        self.sa = naive_sa.sa(S)[0]


    def find_positions(self, pattern):
        """ Finds all matches of pattern in the string S. """
        
        def find_start_position(pattern):
            """ Binary search.
                The position returned by this function should be the first of the suffix arrays that equals the pattern. """
            
            j = -1
            left = 0
            right = len(self.S) - 1
            theoretical_max = int(ceil(log2(len(self.S))))
            for i in range(theoretical_max):
                middle = -(-(right+left)//2) # ceiling integer division
                middle_string = self.S[self.sa[middle]:self.sa[middle]+len(pattern)]

                if pattern == middle_string:
                    j = self.sa[middle]
                elif pattern > middle_string:
                    left = middle
                elif pattern < middle_string:
                    right = middle-1 # Because the pattern is in the upper part, we can exclude the lower.

                if j != -1:
                    break

            return middle, j # The index of SA that contains the matching string.

        start_position, j = find_start_position(pattern)
        if j == -1:
            return []
        else:
            positions = [self.sa[start_position]] # Add the first element for free.
            for i in self.sa[start_position+1:]:
                if self.S[i:i+len(pattern)] == pattern:
                    positions.append(i)
                else:
                    break

            #return [(i, self.S[i:i+len(pattern)]) for i in positions]
            return positions



if __name__ == '__main__':
    o = search_bs('mississippi')
    print(o.find_positions('iss'))