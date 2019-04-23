import bs, bwt
from parsers import parse_fasta, parse_fastq
import sys
import pickle
import t4
import time

### Binary Search

# Binary search preprocessing
if False:
    print('n, t')
    for i in range(200, len(t4.t4_genome()), 10000)[:]:
        print(i, end = ', ')

        t0 = time.time()
        o = bs.search_bs('anytitle', t4.t4_genome()[:i]) # One object for each genome.
        o.preprocess()
        t1 = time.time()
        print(t1 - t0)

# Binary search searching
if False:
    print('n, t')

    genome = t4.t4_genome()
    o = bs.search_bs('anytitle', genome[:])
    o.preprocess()
    print('custom single', o.find_positions('AA'.lower()))


    for i in range(1, len(genome), 100)[:]:
        t0 = time.time()
        search_results = o.find_positions(genome[:i].lower())
        #print('\t', genome[:i])
        t1 = time.time()
        print(i, t1-t0, len(search_results), sep = ', ')



### Burrows Wheeler

# Burrows wheeler preprocessing

if False:
    genome = t4.t4_genome()
    print('n, t')
    for i in range(200, len(genome), 10000)[:]:
        print(i, end = ', ')

        t0 = time.time()
        o = bwt.search_bwt('anytitle', genome[:i]) # One object for each genome.
        o.main_preprocess()
        t1 = time.time()
        print(t1 - t0)


# Burrows wheeler searching. 
if True:
    print('n, t')

    genome = t4.t4_genome()[:]
    o = bwt.search_bwt('anytitle', genome[:])
    o.main_preprocess()
    #print('custom single', o.find_positions('AA'.lower()))


    for i in range(1, len(genome), 1000)[:]:
        t0 = time.time()
        search_results = o.find_positions(genome[:i].lower())
        #print('\t', genome[:i])
        t1 = time.time()
        print(i, t1-t0, len(search_results), sep = ', ')
