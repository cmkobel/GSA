# Author: Carl M. Kobel 2019

# Write a program, search-st2, where you have replaced the suffix tree construction algorithm that you wrote in the previous project with the new construction algorithm, i.e. constructs the suffix tree from the LCP and suffix arrays as generated by gen-lcp.
# The program, search-st2, should support both generating and serialising a suffix tree and search for reads using it.
# If search-st2 is called with the option -p, it should take an additional argument that should be a FASTA file. In this case, it creates files that can be used to rebuild the suffix trees of the strings contained in the FASTA file in linear time.
# For searching, the search-st2 program should take the same input and produce the same output as in all the previous projects.

import gen_lcp
from trienode import trienode # for making a tree in linear time from sa and lcp-a


# ~ Pseudocode ~
# for suffix in suffix_array.
    # if next lcp == 0:
        #insert suffix at root



# Getting the sa and lcp into distinct strings.
S = 'mississippi'
suffixes, sa, lcp = list(zip(*gen_lcp.lcp(S)))
n = len(S)


root = trienode('', '')

current_node = root

print('sa\tlcp\tstr\n~~~~~~~~~~~')


# Iterating over each suffix, being able to look around in sa and lcp.
for i, suffix in enumerate(suffixes):
    print(sa[i], lcp[i], suffixes[i], sep = '\t')
    
    if lcp[i] == 0:
        curr_node = root
        new_node = trienode(suffix[:-1], suffix[:-1])
        curr_node.adopt(new_node)
        curr_node = new_node
        curr_node.append_sentinel()
    else:
        new_node = trienode(suffix[lcp[i]:-1], curr_node.string_label + suffix[lcp[i]:-1])
        curr_node.adopt(new_node)
        curr_node = new_node
        curr_node.append_sentinel()

root.visualize()







