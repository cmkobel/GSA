# Author: Carl M. Kobel 2019

# Write a program, search-st2, where you have replaced the suffix tree construction algorithm that you wrote in the previous project with the new construction algorithm, i.e. constructs the suffix tree from the LCP and suffix arrays as generated by gen-lcp.
# The program, search-st2, should support both generating and serialising a suffix tree and search for reads using it.
# If search-st2 is called with the option -p, it should take an additional argument that should be a FASTA file. In this case, it creates files that can be used to rebuild the suffix trees of the strings contained in the FASTA file in linear time.
# For searching, the search-st2 program should take the same input and produce the same output as in all the previous projects.

import gen_lcp
from trienode import trienode # for making a tree in linear time from sa and lcp-a


# Setup
S = 'sassasass'
S = 'asassassasasassasasasasasasasasas'
S = 'Mississippi'


#S = S.replace(' ', '')

suffixes, sa, lcp = list(zip(*gen_lcp.lcp(S)))
n = len(S)
lcp = [i for i in lcp] + [lcp[-1]] # Måske ville det være smartere at duplikere den sidste værdi, fordi så skal der ikke splittes på nogen måde ahead of time.

root = trienode('', '')


print('i\t\tsa\tlcp\tsuffixes\n~~~~+~~~~~~~~~~~~~~~~')

parent_stack = []
# Iterating over each suffix, being able to look around in sa and lcp.
for i, suffix in enumerate(suffixes):
    print(i, '|', sa[i], lcp[i], suffixes[i], parent_stack, sep = '\t', end = ' ')
    


    # Case 0: lcp is zero.
    if lcp[i] == 0:
        parent_stack = [root]
        new_node = trienode(suffix, suffix)
        parent_stack[-1].adopt(new_node)
        

    # Case 1: lcp has increased.
    elif i > 0 and lcp[i] > lcp[i-1]: # lcp has increased
        if len(parent_stack) == 0:
            print('parentstack er tom')
            parent_stack = [root]

        parent_stack[-1].split(lcp[i]-lcp[i-1])
        
        new_node = trienode(suffix[lcp[i]:], parent_stack[-1].string_label + suffix[lcp[i]:])
        parent_stack[-1].adopt(new_node)
    

    # Case 2: lcp is the same.
    elif lcp[i] == lcp[i-1]: # lcp is the same, append to the same parent.
        new_node = trienode(suffix[lcp[i]:], parent_stack[-1].string_label + suffix[lcp[i]:])
        parent_stack[-1].adopt(new_node)


    # Case 3: lcp is lower.    
    elif i > 0 and lcp[i] < lcp[i-1]:
        print()
        # Gå op igennem forældrestakken indtil der findes en forælder der skal splittes.
        backtraced_letters = 0
        while len(parent_stack) > 0:
            parent = parent_stack.pop() # Man kunne sikkert også lave en pytonisk iterator som bruger pop til at loope igennem bagfra. 
            backtraced_letters += len(parent.in_edge_label) # Tæl længden af hver parent op.
            print('  parent:', parent_stack[-1], 'backtraced_letters:', backtraced_letters)
            print('  ps', parent_stack)

            # Hvis backtraced_letters indeholder den forskel der er mellem lcp[i-1] og lcp[i], ved vi, at vi er gået langt nok op.
            if backtraced_letters >= lcp[i-1]-lcp[i]:
                split_point = backtraced_letters - (lcp[i-1]-lcp[i])
                print('   ready to split', parent, 'at position:', split_point)
                #parent_stack.append(parent) # because we removed the parent, we should add it again? Apparently not.
                parent.split(split_point)
                print('   parent stack after split')
                for kaaa in parent_stack:
                    print('    >', kaaa) # Det betyder at roden stadig er der.


                new_node = trienode(suffix[lcp[i]:], parent_stack[-1].string_label + suffix[lcp[i]:])
                parent_stack[-1].adopt(new_node) 

                break # stop her

    # Before completing each suffix-insertion, we want to check whether to put the newly inserted node as current parent:
    if lcp[i+1] > lcp[i]:
        parent_stack.append(new_node) 

    print('=>', parent_stack)


    root.visualize(f'iter/{i} {suffix}')

root.visualize(f'iter/Done')





