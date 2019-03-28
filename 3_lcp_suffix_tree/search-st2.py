from st2 import st2
from parsers import parse_fasta, parse_fastq
import sys

genome_file = sys.argv[1]
reads_file = sys.argv[2]
    


for genome in parse_fasta(genome_file):
    
    for read in parse_fastq(reads_file):

        st = st2(genome['sequence'])
        st.construct_tree()

        for match in st.find_positions(read['sequence']):

            print(f"\
{read['sequence']}\t\
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




