# Write a program, gen-lcp, that uses the construction algorithm from the previous algorithm to generate a suffix tree. 
# Then use this suffix tree to output a file that contains the suffix indices in lexicographical order and the LCP 
# array.
import st


S = 'abbaab'
o = st.suffixtree(S, show = True) 

def sorted_suffixes(root):
        for child in root:
            child.children.sort()

        for child in o.tree:
            if len(child.children) == 0:
                yield child.string_label, child.start_index


def lcp(root):
    old_suffix = ''
    for suffix, start_index in sorted_suffixes(root):
        lcp = 0
        #print('suffix: \'', suffix, '\'', sep = '')
        #print('', len(old_suffix), 'char(s) to compare:')
        
        for char_idx in range(len(old_suffix)): # old_suffix is mostly shorter
            #print('  comparing', suffix[char_idx:char_idx+1], 'and', old_suffix[char_idx:char_idx + 1])
            if suffix[char_idx:char_idx+1] != old_suffix[char_idx:char_idx + 1]:
                #print('breaking')
                break
            lcp += 1

        old_suffix = suffix
        #print(start_index, '   lcp:', lcp)
        yield (start_index, lcp)




for i in lcp(o.tree):
    print(i)