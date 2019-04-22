import bwt
from parsers import parse_fasta, parse_fastq
import sys
import pickle

"""
Usage:

python search_bw.py -p <reference.fasta>            Preprocess only.
python search_bw.py -i <reads.fastq>                Import preprocessed file and search only.
python search_bw.py <reference.fasta reads.fastq>   Do everything, ignore files on disk.

"""



if sys.argv[0] == '-p':
    """ Preprocess only. """
    genome_file = sys.argv[1]
    sa = naive_sa.sa('')


elif sys.argv[0] == '-i':
    """ Import external files. """
    genome_file = sys.argv[1]


else:
    """ Ignore external files. """
    genome_file = sys.argv[0]
    reads_file = sys.argv[1]

    

if not preprocess:
    for genome in parse_fasta(genome_file):
        
        for read in parse_fastq(reads_file):

            # st = st2(genome['sequence'])
            # st.construct_tree()

            o = bwt.search_bwt(genome['sequence'])



            for match in o.find_positions(read['sequence']):

                print(f"\
    {read['title']}\t\
    0\t\
    {genome['title']}\t\
    {match+1}\t\
    0\t\
    {len(read['sequence'])}M\t\
    *\t\
    0\t\
    0\t\
    {read['sequence']}\t\
    {len(read['sequence'])*'~'}")




