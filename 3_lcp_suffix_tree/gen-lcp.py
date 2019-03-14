# Author: Carl M. Kobel 2019

# Write a program, gen-lcp, that uses the construction algorithm from the previous algorithm to generate a suffix tree. 
# Then use this suffix tree to output a file that contains the suffix indices in lexicographical order and the LCP 
# array.
import st


def lcp(root):
    """ This generator yields the suffix array as well as the lcp array. It might as 
    well do that, since it uses the suffix array to compute the lcp array anyway.
    
    The input should be a root node from a suffix tree made with iterable children.
    
    A tuple with three values are yielded: suffix, start_index and lcp.
    """
    
    # helper function
    def sorted_suffixes(root):
            for child in root:
                child.children.sort()

            for child in root:
                if len(child.children) == 0:
                    yield child.string_label, child.start_index

    old_suffix = ''
    for suffix, start_index in sorted_suffixes(root):
        lcp = 0
        for char_idx in range(len(old_suffix)): # old_suffix is mostly shorter
            if suffix[char_idx:char_idx+1] != old_suffix[char_idx:char_idx + 1]:
                break
            lcp += 1
        old_suffix = suffix
        yield (suffix, start_index, lcp)
        

if __name__ == '__main__':
    S = 'banana'
    o = st.suffixtree(S, show = True) 
    
    print('sa\tlcp\tstr')
    print('~~~~~~~~~~~~~~~~~~~~')
    for (str, sa, lcp) in lcp(o.tree):
        print(f'{sa+1}\t{lcp}\t{str}') # +1 for 1-indexed arrays