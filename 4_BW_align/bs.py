import naive_sa
from math import ceil, log2

class search_bs:
    def __init__(self, title, S):
        self.title = title
        self.S = S.lower() + '$'


    def preprocess(self):
        self.sa = naive_sa.sa(self.S)[0]





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
                middle_string = self.S[self.sa[middle]:self.sa[middle]+len(pattern)] # prefixed

                if pattern == middle_string:
                    j = self.sa[middle]
                elif pattern > middle_string:
                    left = middle
                else:
                    right = middle-1 # Because the pattern is in the upper part, we can exclude the lower.

                if j != -1:
                    break

            return middle, j # The index of SA that contains the matching string.


        start_position, j = find_start_position(pattern)
        if j == -1: # ingen matches
            return []
        else:
            #positions = []
            positions = [self.sa[start_position]] # Add first element for free.
            for i in self.sa[start_position+1:]:
                if self.S[i:i+len(pattern)] == pattern:
                    positions.append(i)
                else:
                    break


            for i in reversed(self.sa[:start_position]):
                if self.S[i:i+len(pattern)] == pattern:
                    positions.append(i)
                else:
                    break

            #return [(i, self.S[i:i+len(pattern)]) for i in positions]
            return positions



if __name__ == '__main__':
    S = 'mississippi'
    
    o = search_bs('first', S)
    o.preprocess()



    print(o.find_positions('i'))

    print('testingall')
    for _i, i in enumerate(S):

        print(o.find_positions(S[_i:]))
