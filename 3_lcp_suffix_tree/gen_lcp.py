# Author: Carl M. Kobel 2019

# Write a program, gen-lcp, that uses the construction algorithm from the previous algorithm to generate a suffix tree. 
# Then use this suffix tree to output a file that contains the suffix indices in lexicographical order and the LCP 
# array.

# Should be breaked up into two parts, so the time can be taken individually.


def suffixes(S):
    #S = 'Missisippi'
    S += '$'
    S = S.lower()

    suffixes = [(S[i:],i) for i in range(len(S))]
    suffixes.sort(key=lambda tup: tup[0])

    return suffixes



def lcp(suffixes):
    previous_suffix = ''
    for suffix, start_index in suffixes:
        #print(suffix, start_index)
        lcp = 0
        for char_idx in range(len(previous_suffix)): # previous_suffix is mostly shorter
            if suffix[char_idx:char_idx+1] != previous_suffix[char_idx:char_idx + 1]:
                break
            lcp += 1
        previous_suffix = suffix
        yield suffix, start_index, lcp

        

if __name__ == '__main__':
    
    print('sa\tlcp\tstr')
    print('~~~~~~~~~~~~~~~~~~~~')
    for (str, sa, lcp) in lcp(suffixes("mississippi")):
        print(f'{sa+1}\t{lcp}\t{str}') # +1 for 1-indexed arrays