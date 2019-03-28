# Author: Carl M. Kobel 2019

# Write a program, search-st2, where you have replaced the suffix tree construction algorithm that you wrote in the previous project with the new construction algorithm, i.e. constructs the suffix tree from the LCP and suffix arrays as generated by gen-lcp.
# The program, search-st2, should support both generating and serialising a suffix tree and search for reads using it.
# If search-st2 is called with the option -p, it should take an additional argument that should be a FASTA file. In this case, it creates files that can be used to rebuild the suffix trees of the strings contained in the FASTA file in linear time.
# For searching, the search-st2 program should take the same input and produce the same output as in all the previous projects.

import gen_lcp
from trienode import trienode # for making a tree in linear time from sa and lcp-a

DEBUG = False
def pprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class st2:
    def __init__(self, S, dump_pdf = False):
        self.S = S.replace('\n', '').replace(' ', '').lower()
        self.dump_pdf = dump_pdf
        self.root = trienode('', '')

        self.lcp_array = list(zip(*gen_lcp.lcp(gen_lcp.suffixes(self.S))))

        # Run the main method:
        #self.construct_tree(lcp_array)



    # Setup
    # S = 'sassasass'
    # S = 'asassassasasassasasasasasasasasas'
    # S = """AATTTTCCTTATTAGGCCGCAAGGGCCTTCATAGTTTTAGCGATTTGGGAAACTTCATCATCACTTAAAGAGTTGCGATAACCGATGAAGTCGGAAACAATACGGAATTTCTTGGTAAACTCAGCAACCATTTTATCACTGTTTTTTGAAGCATTATTTGATAATACATCAAAAAGATTAGTTACTGTCCAAATGTCATGACCGATGGTATCTTTTCCACCATTAAAATATACACCCTGTAATGAACTAACCATATTAGCGAGTCGTGTATATTCTTCAGAAACTTCATCTATACTGAAGTACTTCATCATAAAATCTAACTCAGGATACTTGATAATTTTATCAATATATCGTTTAGCTGAACTTGAATAACCTACATACTTATCATAATCTACATCATCAAAAGCATCTACATATAAATCACGCAAAGCTTCAAAAATACATTGGCACTGACCGAGTTCTTTTACCTTTTTCTGTAAAAGCGGACGAATAACATAAAATTCATTAATGCCAATAAGATTAGCCATACGAATCAAAATATTCATAGATGGATGACAAAGAGATGTAGTACCATCCATAGAGAAAATATCAGAACGATGCATATACGCTACATAACCAGTAATTTCATCTGCTTCTGATGTGAGGCGTAAATAATTCCTCTTTTCCCAGCGCCCGTCTTTAATTTCAAACTTAAACGCTGTAGCAGCTTTAGGACGAGGAGCTTTACTTTTAACTACCTTTGGAATATAACTTTTTACTAAAGCTTCAATTTCTGACAAATAATGAATGTTAACTTCATCACTTTCAAACATCGCCATAATATCAGGAAGCAAATCAATCTGCGATTCTACTTCTGGATTAATAAACAGAAGACGTTCGTTATGATGAATATTCAAAGTGTTATTAAATTCACTATCATCTAACGCACGTGCTAATCCACGGACAATATTAACACGATTTTTAATATTATCAATAACGATATTAATTTTTGTTGTATTAATACCAAACAGACGATAACTTGATGCAACGGCTGAAGTTTCATGACTTTGCTTAATGCGCTTCAGTCGAGGGTCAAGATTTACTTCATACACAACTCCCGCGTTGCATAACTTACTGTCAGGTTCAAACATGCTCTGCATCTTTTTATATGACAGATTTTTAGTCGTGAATTTGACTGAATTACTAATCATATAATCTCGAGCAGAATACCCCATCTTCATCAATTCACGATATGTGTGACGAGGAGATGTAGATTCTTTAAATCGTTTTACATCTTCATTAAATGCTTTCTCACTGAGTTCTTTAACTCGTTCAATAATATTTTTACGAGTGCGATCATCCAGTGAAAGAGCCTCGCGAGATGGAGCAATATCAAGTGAACCCATTGGAAACTTAATGTAATTCACTTCATTGCGAATGCTTAGCCAGTTACGGTCTCTAATAACACCATCGATAGGATAAACAATACCACCGTAGATAGCATATAATCCACCACGATCAGGCCAGTATCTTTCTGGATTTACACCGTAATAGTCATCAAAATCCGGAAAATAATCAATTTCGCGGTCAAGACCATTAATGATAGCCAAATCTTTGAACGGTCGCATGATATAAGAAACTTCATAAGCAAAGTTTCTAAAGTCTTTTTCTTCAACTGGAACTACGATTTCAATACCAGTTTTATCATCTGGACCCATTTCTTTTACGAATGTAGGTTTAATCTGTGGACCATCACCATCCATGTAAGCTACATAACCACGAATTTCACCTTTATGATACGAAGTAATACTAAACGTATCAGTATAACTAAACGGAGATTTAGAACCTAAACCAAATCCGCCAATAAAGTCATTAGATTCAGCTTTAGATGAACTGAAGTATGAATTATACAACCCAGGAGAATTATCATCACCTTGAATATCAAAATCACTCATACCCGGACCAAAATCTCGACAAACAAATCGTGGGTCTAAACGTCCAGGAACTTGTATGATAAATTTTTCAGGATTTCCATTAAGTGCATGAGCATCAATCATGTTAGTAATCAATTCACGGACTACTGCGCGAATCTTGTTTGTATACAAATCAGATGACAGAATTTTAAATACTTTAGGAGATGCTGTGATGCTAAATGCTTTTGATTTAGAACCATTACCAAGAATTGTTTCTTTTTCAGTGGTGATAATCATAATTTCCTCATTAATTCATATTACGCTTAATAACTTCAGCAACTTCTAGTAGTTCATCTTTAGTTGCGGTGTCGGATTGAATTTTATCTCTAATATCTTTAAAGCGGGTTTTAAATTCTTCGGCTTCTCCCATATCGAAAAAGCGTTGAATGATTCTATATTCTCGATGAACTGCTTTATCAAAAAGTTCTAAATTTACTTTATATGATTTCATTTCAATATCCTCATTTGCCCAATTAATTATACCACATCCTTGTGGTAAAGTAAACTACTGGCTCATCCATTCTTTACGAAGGTCAGCATTATCTCCCATGAGCATTTCAAAAAGCTCTTTCCAGTTCTCAGGAAGTTTAACAACATCATATACTGGGTTTTGAATCATCTCACGATATTCAGATTTTTCCAAAGAGCCAAGTCCCTTAATATAACGGATGCTATGTTTAGGTAGAGCATCTTTGGCACTCTCATATTCAGCGACTGTATAAAACCATTCTTGTTTTTTACCGACCTGAGCGATGATTACAGGAGTTTTGACAAAGCGAATTCGTCCTTGCTCAAACAATTCTGGCCAATTACTAAAAAATCCGAGCAGAGAAGGATAAATAGAACCTAATCCAATAATCTCTTAATTATGAGGTATTTCTATAGATAGCCCGAAGGCTATCCATCGTGATCTGCGTCTGTCATAATAGCGACATTCGCATAGTTCATTGAAGAGGATTTAATAGAACGACGAACATTGTTCTGCAATTTATATTTTTTCATATCAACGCTAGAAGAATCAATTTTTACAAATTTCATTATACACCTCATAGAACTTTTCATCAGGAATCCAACCGCGTTTAAATTCATTAAATGCTCGGCCGAATAATTTTGAATTCACAGTTATATTATTAACTGATTTCCATTTAGCAACTCCCGTTCGTTTATAATGATCGGGGTCATATTTCGTGACGTACCATTCATATAAATTTGGTATTAATTTTACAGCCTCTGGATTTGTCGCTGATTTATTATACCATGGTTTCGCTTTTTCAAGTTCAGCTGCTTTTGCAGTAGCAGCAACAGTATTTCCAACACCAACTAATTTTTCAGTTTTAATGCGTGGATCATTAACATGAAGACGAAAAACTTCGCCCTTTTCATTTTTAAAGCATGTCATGCCTTTAATTCCAGGAAGCTTAACACCTTTATTAACACCGCATCATTCCTTTGGGTTAAATGATCCTTTAATTAATAAGGCGCATTTACCCGATTTAACTACTTCTCATTCAACAACTTTATCTTTCATAACGTTTTTTGACCATTCAGATACTGCTCTTTGATGGCTAAATTCTAGCAATTTCACTATAATTTGCACTAGAACGTAAACTATTTTTCAGTGTTTCAACATTCTATTCATCGCATATGCCATTTCACGATTACGATGAATTTTATATAGTAGAAAATAGTGCTAAAAAGTGTTCACGAAAAGTCATGTTTCACCAAATTTTCGTTATCATCAGAACCTCCCATTGATCTTGGAAGGATATGATGAATTTCACCCTTAAATTTAGAAACGCGGGTTTTACCCCGCACTATTAAGTCATTATAGATTTTTTCGTAATTCACCTACTGTTATCCATTTACCATTAATCTGTACTTCATCATTTTCATTTACGATAATTGTATCGCCATTTAGCTCGAAAGTAAACCACTCGCCATCTTCTTTTTCTTCAAACGCTTTTTCACCGAGAACTAGACCAGTGATTGCGCAAATATCAAATAGTTCTTTGTTTTTAAGCATATCTGCATAAGACATACCCCAACTGTTGAGAACTTTACCACGCAATGGATAACCACCGTGAAGTTCTTTATCACGAACATCAATAAGATATCCGATAGCCGAATCACCCTCAGTCAAGAAAAGAGTAGTATCAGCATCTTTACCGCAAAGATTCGCTTTGATATGTTTATGAACCTTAGCTTTAGAAGCCTTTTTAGCTGCTTTAGTTTCTGCTGCTTTTTCTGCCGCCAATTTACGAGCCAAAGCAGCTTCAATAATCGGCATTAGAATTGCTTCATTATTTAGAATATCACGTGAAATCTTTTTAGCATCAAGTTGAATATGACTACGAATTTCGCCAAATGGAGAAGTCAAACGCTCTTTAGTTTGACGAATCAATCGCATGTTTTTCATATCACGAACAAACATAACGATAGTCAAACATTCTTTGACACGTGCTTTAGTCACATCAATTTTGAACTTACGTTTGATTTGTGGAATAAGGTCTTCACAAATATCATCCATAGCGCAGTCAATGTGATGGCCACCATTCTTAGTATGAATGTTATTGACGTATGTTAATTGACGAAAACCATCCGGTGAACGACCAACCGCAATAGAACAATTTTCTTGCTCTTGAACAATAGCATGTTCATCATACTGCCGTGCATATTTCTTAAAATTGCCCTGAACCTTTTTACCATTAAAGGTAAATTGAATATCAGGATAAACTACAGCAAGTGTCTGGAGACGATCCAGTGTAATGTCAAGATAAACTTGGGACAGCTCATTAGTTTCAAATGACATAAAATCAGGAATGAAAGTAACACGAGTTCCTTTCCATTTTCCAGGAATATCTTCCCATGATTTATTTTCCATGCCATTTGAACAACGAACTACAATATTATTTTGACCGTCGCCAGTTTCACCGACAAACATCACAGAAAAAATGTTTGTCAAACTAGAACCAACACCGTTCATACCGCCGGTGACGCGTTCTTTATCATCACCAAAGTTACCACCTGCTTTTGGAATAGTCCATGCGGCAACAGGACCAGGAATTTCTTCACCGGTAGGTGTTTTAACCATCGCTTGTGGAATACCGCGACCGTTATCTTCAACTGTTACTTGATTGTTTTTAATAGTAACATTAATTTTATTCGCGAATTTAAACTTAGTACGAATACCTTCATCTACTGAGTTATCGATAATTTCATCAATAAGCTTAACAAGACCAGGTACATACTGAACACTTTCCCATTTACCAAACATAAAGCGCTCATGCGTTTCATTAGCAGAAGAGCCAATGTACATGCCACTACGCTTTTTGATATGTTCAATATCGCTCAGAATTTTAATTTCATTCTTAATCATCACTTATCCTCGTTTGGTTTCGGGAATATTATACTCCGGTAATCATAAAGCTAAAGGCCCGAAGGCCTTTTATTTAAAACGAATAGTTGAATCCTTAAAGAACAGCCCAGAACATACTGTTCCTTCTACTTTCTGCCCGGTAGGTCCAATAGCACGAAATCCAGTATGCTGGAAATCATTTTCAGAGCAACCGAACCAATTATATCCAGTGATTTCAATATTAGTAAAACCACTTGAAGACAAAACTTTGGTTGCATTAATCAGCATCAGTACTATTAATTAAAGACACTGCTAATACTAATGCTGCAATTGAACGACTAATATATTTCATAACTACCCTTTAAGCAAGTCGTAAAATCCATTATTCCCATGCTTAGGAAGCGGAAACTAACCGAACAGCCAGCCGATGACAATCAGGACATACACCAGTATCTCTTCCAGAAATTTTCTTGATTTTTTCGTATTCTTTTGCACAGTCTTTGGATTGACATTTATAATCATAAAGCGGCATAATTATTCCTTAAAGTAAGCTTTCAACATCTGATATAAAGACCACGCCTGATCATTATTTTCAATAGTAACTTTCATGACTGGGAATTCTGTGAAATCTTCTATTTGTTCTTGCTCTTTCTCTTCCTGCTCTTGCTCTTCAACCGCCTGATATGGATTTTCCACTTCATCAAAGAACCCAGCTTCGTTAGTAGAGAGCCAGATAAAGTTTTCGTCAAGGATATCACCGCCGGCACAACGTTTGAGTACACCTATGGATGTCATAATTTTAGTAGGACGCCCAAGATAATCAGCATCTAAAATTTTAAAAGGCTCCATACCTAAACGTCGTGCATAGATTCCGTTATCAGTATGGTCTTTAATAAAATTTTCTTGAGCTTGTTTATTTTTAAATTGATACCATTTATTAACTTCAAATTTAATAGCCATTAATAAATTTCCTTCCAGTAAGTTGTGCCGTCTTCAGTAATTTCACGAAATACACCATAAATTGGCTGTTTATCACCGACTTTCTCATACACATAAACAGAAGTCAAGTGAGTAAACTTGCTAGTATGTTCCTTTTGAACTACTACCAAATTTGGATCAAATAATACATCTTCAAATTCATCATTAGTGCAATTCTGAACAATTTTACGTTTCATTACAATTTCCTCATTAATTGAACAGTGGAGCGATACGTTTCAGAAGAGTATCAACACCTTTAGCGAATTTTCCATTTTATTCTCCAAGTTGTTTTCTGTATCAGTAGTTGATATTGATATAGTACCATAATCAACTACTGATGTATATAGTTTTATGAAAAATTTAAACTTTATGCATAGAGAGCATTGCTATAGTGTTTAATCCAACTTTCAGGAATGACTTTGTATGTTCCTAAAAATACCACGTTGTACAACTTAACACCATCTTCTACCCATTGATCGGTAATGTATCCACACATAGCGCGAGTATAAACAACCCTTCCATCATCTTTAATAAAGTTAAATTCACAAGGAGCAATGAACTTGATAGCCTGACCGAGTTTCCACTTAAAGTCTACACCTACATGCGAAGTATCAATCGTTTCAATTCCTTTAGCAGGAACAGCTTTTAAAAACGCAGACTCAAGAAATTTCGCACGAACATAGCCAAACTGGGGTTTAGACTTTCCATCTTTAGGAATGATACGCACTTTTACTTCAGAATCTTCATCTTTAACACCATGCTTAAGCTGAATGCTTACAACTTCGACCAATTTTCCTGCTGCTTTAGAACGGGATTTATCAGATACACGAGCTAATTCACCAATATTAATAATCATAGTTATCTCTCACTTGTTAAAAAGATTTTATACTCCACGGGACCATTATACTCTGGTCCCAAGAGTTTGTAAACTATTAATTCAAAATAGCTACCACTGCACTACGAGGAACTACGGAGTACTCTCCAGCATGAACTACGTTCAGAAGTTCAACGCCATCTTCCAATCCATTGGTCAGTTACCCAACCACCAATCGGATTCGCAAATGGACGACGAATGTAAACTGCCTTACACAACAAATCAGTCGGGTCTTCAGGTTTTTCAATTTCTGTCAATAGATTAAAATCTTCTTCATAGATGATGAATGATGATACCCTTCCATAATAGTTTCTAATTTCCATGTACACTGTACCAATGAGAATTCCACTATTAACACTAATGACAGTAAAAGGATATCCGCCAGTTGTACCAAGAAGTTCCCAAAATTTGCTATCAGTCGTATTCGACATTGTCTGAAAATCAATTTCAGATGGTTTTTTCATTTGATACGCAGTATTAATTTTAATCATAATTTTCTCTTTAGTTTAAGGTAATAAAGCCTTTTAGTTCGGCATAGGATTTACGGAACATTACTTGATGCCCGCCAATGATAACTTGGTCATCTGGTACTTCGTATACAGCAAGATAAAATCCTTTCGAAGCTAATTCTTCACGCTCTTCTCGTGTGAACCATTTCATCATATCATATTCGCTAGCAAAAGCAAAATGATAAAGAGCTACAAACCATCCGGGAATATGATATTCTACTCCAACATAATCTTTCTTGAACTTAGTATTAATTACGATATTAGCATTTTTAACTAATAGTTTGTCTTCGTGCGGCACAGGAATTCTTTTATTATCATTACTATGATGCATAAAATTAGGTCTGTCATAACCTACATGTAATAACCACTCTTCACTCCATGAATCTATTATACTTCTATACGGCGTTATTTGAACACAAAGATCTCGGCGTATTGTTATAGCGTCTTCATAATTAAGAATACTAAACGATGATTCAACACGATAAATTTTCATTTTATTATCCTCAGTAGCTATGGTGTTATAGTACCACAACTAACCGAGGAAGTAAACAACTTTTTATCGTTTTGTTGGAAGAGATAGAGGATCGCATTCTTCCTCTGATGGAGCATCTTCAAGACCCATAGCATATCGCAAAGCATACTTCATCATCAGGATGTCTTTCGCACAGTCATGAATAGAATCATGTGCAACGAATCCATCTAAAGTTCCCTTTGGAAGAGGACACGTTGTCATATCACGAACAAGCAGAAGTGCTTCAATTCTAGTACGAATATCACGCTGATTCCAAAATTTACAAGGTTCTAACTTAAATGTATCAAGCTCATTCTCGGAAACGCCGTTAAGACGTTGAATATCGCGAATAAGATCGACTAAAATTGGAAAATCAAACGACATTCCACGGCACCAGCCTTGAGATTTCCAAGGATCGATATTATGTGCATTGATGTAATCATTAAATTTTGCAATACCGTCGATAGTGCTTACATCTTCATCGGATGGTGCAATATTTTTTCGAGCTTCAGGAGATTGATTCTTCCACCATTCGATAGTACTTTTAGTAAAAAGACGGTGTCCTTTTTGGCTTTTTAAATCAAATTTGATTTTAATGCCACGTGAAACTAATTCATCGAATGTTTCAACTACTTCTGGATTAGGGTCAAAAGCAATTACAGCCAAATCAATAACCGCTGCTTTTTCACCACTTCCCATTGTTTCAAAATCTATAATAAAATCAAACATTAAATTTTCCTCGCTAAATCACGAATTTGACCTACAGTATAGTCTTGAATATAAACTTTATTAATAGGCTCATCAATAAATTTTGCCATAGATTCAATATCTTTTTGTATTTCTTCAAGACTGTATACTATCTTTGAAGCTTTTTCGCGAATAGTGATATTTTCAGGACCCGGATTTTCTTGAATGACAACTTTAACATTTGTCATAAGAGATTTAAACTGGTACCAACTTAATTCAATCATTAATAATCGCCTCATAAAGATAGCTAATTTCGCCTAAAACATAATCATTGATTGTAACAGTTTTAACTTCACCGCAAAAGAATTCTAACGCAATTAAATCTCGTTCAATTTCTTCTAATTGAAGCATCAACTTACTAGATTCAATTTTTACAGTTTCACGATTTTTGCTATAAGCTATTTCATAAATTTCGCTTACTTTATCTTGAAGAAGATAAAACTGATCTTTAGTTATTTCCACGAATAGCTTCCTCAAATTTAATCATACATAAAACACATCATAACGACCACGGGTGACACCAACATAAAGAAGTTGTTGAGCTAATTCAACATCTGCATAATGAATACAAGGCGTATAAATGAAAGCACGGTCTACAGACATACCCTGCGCTTTATGGAATGTTGATGCAGGAAGTGCTTTCACTTTACTAAACTGTGATTTAGCATCCCAAAAATCACTCCACGGAGCTTTTCCGCCTTTGTTCCAATTTTTATAAGTTTCTGCTGTTTTAGCTAAAAATAGGTTAAACTTATACAATTCTTCGTCAGATGAAATTATTTTAATCTTTTCACGATAATATTCATCATCGCCATAAGTTTCTACTGTTAAATCCCAATGACGAATTAGATATTCTCCAGGAACACCACGGGCTTTAACAAACGTTGATGTATACTCTGCTTCTATAATACGAACTAATTGTCCGTTATTAAAAATAATTTCTGACACAGGCTTTCCATCAATTTTATATGTTTTAAATAATGGTTCCTGCATTACAATAATTTCACCGACAATAAAATCTTTATCAGTTTCAAAAATCTTTTTACGAATAATGCTATTTAACTTGTCAACAGATTTATTCGTAAATGCCATTACGCGATTTTCAAACAAATCATCTAGTGATTTGACGATTGAAAAATAATTTACCATAAAATCGCGTAAAGCGGTATCACCAGTAAATCCACGTACTCCATGCCCGTCAACAACTTTATCATAATTCCACTTACCGTTGCGAACGTCAGTAGCTACATCAATAATAGGAGCATTACTGCGTTTAACTTCAGTGAGTTCACACTGATAAAAATCTTTATGTGTAAAGAATGGACTGATATAAGCAGTATTTTCTCCTGGTTCAACAGGTCTGATTTGCTTATTATCCCCTATTCCAATTATAGTACACCAAGGTGGAATAGTTGAAAGCAGAATTTTAAATAGCTTTCTATCATACATTGACACTTCGTCGCAGATTAATACTCTGCATTTGGCTAAATCAGGTACTTCTTTTTGTTCAAAAAGAACATTTTCTTCATATGTTACTGGGTTAATTTTAAGAATACTATGAATAGTACTCGCTTCTTTCCCTGATAGTTTTGAAAGAATCTTTTTAGCTGCATGTGTAGGAGCTGCTAAAATAATACCAGTTCCACCCGTAGATATTAAAGCTTCAATGATGAACTTAGTAAGAGTAGTCTTACCGGTACCAGCAGGTCCATTAATAGTTACATGATGTTTCTTTTCTTTAATAGCCTTCATAACAATGTTAAAGGCATTTTTCTGGCCTTCGGTCAAATCATCAAATGTCATCGTAAATTCCCTGCAATTGGTATACTAACAATACGCCCAGTATCTAAAATTCGCTGATATAATCTTTGCGTGTCTACGTCAGGCTTAACATGTTTAACTTCTATTTTATTAAACCAAAATTTACGTGGAGTCTCAACTAATCTTGGAATTCCCTTACCTAAAGCTAATCGATACTGCTCTTTAAGAGTGGTAAATACTTTATCAGCAATCTTCCATTCAAAAAATACAGCAGGACGATGTTCATCAAGCGGAACTGGCGCTGTAAATCCGTCTTTGTCTCGGTAAACTATCGCATATACATAAACCATATTATCCTCGGATAAGTTTAAAAATTGAACAATTTAGCGGATATCCTCTTTTCAGTTTAAGTTTATCAATAAAAGACAAATTTTGATACCGCTCTACACCTTGAATAATTTTATCACACATATCATATTGCATTTCTGCTTCTGACAACTTTTTCACAATTTTCCAATCCGAGCCTTTAAGAAGAACGTTCAATTTAACAACTTCAGCGCCTTCTGCTATGCGAGAACCATCAATACGTGCTTTAAGTGCTATAATTCTCAGCTTAATGTCAGAGGTCTGTTTTGATTTAGAAAGCTGAGAAATGTGTTCAATTCGATTTTCACGTTTTTTCTGTATAGCTTTAATTTGATTATAAGTCTTTTTGATTTTAGCCCATTTCTTTTCATCTAAATTTAGTTTATGAACTTTTTTCGCAGATGAACGACCAATTCGCAAAGCAAATAAATCACGCTTTTCAATCAACTCTTCTAAAGTATAATCAGAACGAAATGTATTATACTTTTTCTTTACTGCAATAACATTCCCTTTAATGTATCCAACGTTATTATCAAAACGTTCTAATGATAATTTCTCTCCTTCAAT""" 
    # S = 'Mississippi'


    def construct_tree(self):
        #suffixes, sa, lcp = list(zip(*gen_lcp.lcp(self.S)))
        suffixes, sa, lcp = self.lcp_array

        n = len(self.S)
        lcp = [i for i in lcp] + [lcp[-1]] # Måske ville det være smartere at duplikere den sidste værdi, fordi så skal der ikke splittes på nogen måde ahead of time.



        pprint('i\t\tsa\tlcp\tsuffixes\n~~~~+~~~~~~~~~~~~~~~~')

        parent_stack = []
        # Iterating over each suffix, being able to look around in sa and lcp.
        for i, suffix in enumerate(suffixes):
            pprint(i, '|', sa[i], lcp[i], suffixes[i], parent_stack, sep = '\t', end = '')
            


            # Case 0: lcp is zero.
            if lcp[i] == 0:
                parent_stack = [self.root]
                new_node = trienode(suffix, suffix, start_index = sa[i])
                parent_stack[-1].adopt(new_node)
                

            # Case 1: lcp has increased.
            elif i > 0 and lcp[i] > lcp[i-1]: # lcp has increased
                if len(parent_stack) == 0:
                    pprint('parentstack er tom')
                    parent_stack = [self.root]

                parent_stack[-1].split(lcp[i]-lcp[i-1])
                
                new_node = trienode(suffix[lcp[i]:], parent_stack[-1].string_label + suffix[lcp[i]:], start_index = sa[i])
                parent_stack[-1].adopt(new_node)
            

            # Case 2: lcp is the same.
            elif lcp[i] == lcp[i-1]: # lcp is the same, append to the same parent.
                new_node = trienode(suffix[lcp[i]:], parent_stack[-1].string_label + suffix[lcp[i]:], start_index = sa[i])
                parent_stack[-1].adopt(new_node)


            # Case 3: lcp is lower.    
            elif i > 0 and lcp[i] < lcp[i-1]:
                pprint()
                # Gå op igennem forældrestakken indtil der findes en forælder der skal splittes.
                backtraced_letters = 0
                while len(parent_stack) > 0:
                    parent = parent_stack.pop() # Man kunne sikkert også lave en pytonisk iterator som bruger pop til at loope igennem bagfra. 
                    backtraced_letters += len(parent.in_edge_label) # Tæl længden af hver parent op.
                    pprint('  parent:', parent_stack[-1], 'backtraced_letters:', backtraced_letters)
                    pprint('  ps', parent_stack)

                    # Hvis backtraced_letters indeholder den forskel der er mellem lcp[i-1] og lcp[i], ved vi, at vi er gået langt nok op.
                    if backtraced_letters >= lcp[i-1]-lcp[i]:
                        split_point = backtraced_letters - (lcp[i-1]-lcp[i])
                        pprint('   ready to split', parent, 'at position:', split_point)
                        if split_point > 0:
                            parent_stack.append(parent) # because we removed the parent, we should add it again? Apparently not.
                        parent.split(split_point, start_index = sa[i])
                        pprint('   parent stack after split')
                        for kaaa in parent_stack:
                            pprint('    >', kaaa) # Det betyder at roden stadig er der.


                        new_node = trienode(suffix[lcp[i]:], parent_stack[-1].string_label + suffix[lcp[i]:], start_index = sa[i])
                        parent_stack[-1].adopt(new_node) 

                        break # stop her

            # Before completing each suffix-insertion, we want to check whether to put the newly inserted node as current parent:
            if lcp[i+1] > lcp[i]:
                parent_stack.append(new_node) 

            pprint('=>', parent_stack)


            #self.root.visualize(f'iter/{i} {suffix}')
        if self.dump_pdf:
            self.root.visualize(f'iter/Done')
        pprint()


    def find_node(self, p):
        """ Returns the node where a match has been completed.
        If no match; returns False"""
        
        def rec_search(node, p):
            """ Returns the index in S where the match is found. """
            len_p = len(p)
            if len_p == 0: # base case: when an empty string has been asked for, we are done.
                return node


            for child in node.children: # for hvert barn
                lower_bound = min(len_p, len(child.in_edge_label))

                if p[0:lower_bound] == child.in_edge_label[0:lower_bound]:
                    return rec_search(child, p[lower_bound:])
            return False

        return rec_search(self.root, p)


    def find_position(self, p):
        """ Returns the first match position. """
        rv = self.find_node(p)
        if rv == False:
            return -1
        else: 
            return rv.start_index
        

    def find_positions(self, p):
        """ Returns all matches in a list.
        First, it finds a match nodes. Then it iterates through all children in order to 
        obtain all positions. """
        match_node = self.find_node(p)
        if match_node == False:
            return []
        else: # solutions exist:
            return list(set([subnode.start_index for subnode in match_node])) #


    # Functions for proj. 3

    # def retrieve_suffixes_sorted(self):
    #     rv = [reversed([node]) for node in self]
    #     #return reversed(rv)
    #     return rv





if __name__ == '__main__':
    S = 'mississippi'


    o = st2(S)

    print(o.find_positions('iss'))
    print()
    for _i, i in enumerate(S):
        print(S[_i:], o.find_position(S[_i:]), o.find_node(S[_i:]))
    print(o.find_positions('iss'))









