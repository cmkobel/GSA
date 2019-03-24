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
lcp = [i for i in lcp] + [lcp[-1]] # Måske ville det være smartere at duplikere den sidste værdi, fordi så skal der ikke splittes på nogen måde ahead of time.

root = trienode('', '')



print('i\tsa\tlcp\tsuffixes\n~~+~~~~~~~~')


# Iterating over each suffix, being able to look around in sa and lcp.
for i, suffix in enumerate(suffixes):
    print(i, sa[i], lcp[i], suffixes[i], sep = '\t')

    # Case 0: lcp is zero.
    if lcp[i] == 0:
        splitcounter = 0
        curr_node = root # This line is strictly not necessary, but it makes the whole lot easier to understand.
        new_node = trienode(suffix, suffix)
        curr_node.adopt(new_node)
        
        curr_node = new_node
        parent_stack = [curr_node]
        
        #print(' inserting at root')
    
    # Case 1: lcp has increased.
    elif i > 0 and lcp[i] > lcp[i-1]: # lcp has increased
        curr_node.split(lcp[i]-splitcounter) # i=4: den ved ikke at der allerede er blevet splittet. Derfor splitter den en position for højt.
        splitcounter += lcp[i]


        new_node = trienode(suffix[lcp[i]:], curr_node.string_label + suffix[lcp[i]:])
        curr_node.adopt(new_node)
         
    # Case 2: lcp is the same.
    elif lcp[i] == lcp[i-1]: # lcp is the same, append to the same parent.
        new_node = trienode(suffix[lcp[i]:], curr_node.string_label + suffix[lcp[i]:])
        curr_node.adopt(new_node)

        if lcp[i+1] > lcp[i]: # because the next suffix has a larger lcp, we know that it is going to be appenden to this new node.
            curr_node = new_node
            parent_stack.append(curr_node)
        # Do not change parents.

    # Case 3: lcp is lower.
    # I'm excited to find out, if it is at all possible to make this work without a parent pointer?
    # I have to traverse upwards, and split nodes. Doesn't sound like it is possible??
    # Hvad, hvis jeg antager at lcp kun kan stige med en for hver iteration? Det er selvfølgelig en selvopfyldende profeti at det kommer til at virke fordi dette eksempel ikke har andre cases..
    # Nu ved jeg at jeg er nødt til at lave en forældrekø.





    






    root.visualize(f'iter/{i} {suffix}')


# Jeg tror jeg spilder rigtig meget tid på ikke bare at have en parent pointer. Det vil kun tilføje konstant tid, men gør det noget?





