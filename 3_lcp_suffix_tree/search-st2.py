# Author: Carl M. Kobel 2019

# Write a program, search-st2, where you have replaced the suffix tree construction algorithm that you wrote in the previous project with the new construction algorithm, i.e. constructs the suffix tree from the LCP and suffix arrays as generated by gen-lcp.
# The program, search-st2, should support both generating and serialising a suffix tree and search for reads using it.
# If search-st2 is called with the option -p, it should take an additional argument that should be a FASTA file. In this case, it creates files that can be used to rebuild the suffix trees of the strings contained in the FASTA file in linear time.
# For searching, the search-st2 program should take the same input and produce the same output as in all the previous projects.

import gen_lcp
from trienode import trienode # for making a tree in linear time from sa and lcp-a



# Setup
S = 'mississippi'
suffixes, sa, lcp = list(zip(*gen_lcp.lcp(S)))
n = len(S)
lcp = [i for i in lcp] + [0]

root = trienode('', '')



print('i\tsa\tlcp\tsuffixes\n~~+~~~~~~~~')


# Iterating over each suffix, being able to look around in sa and lcp.
for i, suffix in enumerate(suffixes):
    print(i, sa[i], lcp[i], suffixes[i], sep = '\t')

    if lcp[i] == 0:
        curr_node = root
        if lcp[i+1] > 0: 
            # If next lcp is higher; split the node into two parts.
            first = trienode(suffix[:lcp[i+1]], suffix[:lcp[i+1]])
            second = trienode(suffix[lcp[i+1]:], first.string_label + suffix[lcp[i+1]:])

            first.adopt(second)
            curr_node.adopt(first)
            curr_node = first
        else:
            #insert suffix
            curr_node.adopt(trienode(suffix, suffix))
    
    else:
        if lcp[i+1] > lcp[i]:
            #split
            first = trienode(suffix[lcp[i]:lcp[i+1]], curr_node.string_label + suffix[lcp[i]:lcp[i+1]])
            second = trienode(suffix[lcp[i+1]:], first.string_label + suffix[lcp[i+1]:]) # Hvorfor får den ikke det med, der står i foregående node?
            first.adopt(second)
            curr_node.adopt(first)
            curr_node = first
        else:
            # Insert as is
            new_node = trienode(suffix[lcp[i]:], curr_node.string_label + suffix[lcp[i]:])
            curr_node.adopt(new_node)



    root.visualize(f'iter/{i}')






