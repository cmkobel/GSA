import t4
import bwt_approx as ba
import time

S = 'mississippimississippi'
    

print('n, t')
for i in range(0, len(genome), 20000):
    #print(genome[:i])
    genome_sub = genome[:i]
    o = ba.search_bwt(genome_sub)
    t0 = time.time()
    o.main_preprocess()
    t1 = time.time()
    print(i, t1 - t0, sep = ', ')
















# pattern = 'sissippi'

# for position, cigar in o.find_positions('ppimissi', 1):
#         print(position, cigar)