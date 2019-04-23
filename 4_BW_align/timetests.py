import bs, bwt
from parsers import parse_fasta, parse_fastq
import sys
import pickle
import t4
import time


# Binary search
print('n, t')
for i in range(200, len(t4.t4_genome()), 10000)[:]:
    print(i, end = ', ')

    t0 = time.time()
    o = bs.search_bs('anytitle', t4.t4_genome()[:i]) # One object for each genome.
    o.preprocess()
    t1 = time.time()
    print(t1 - t0)


