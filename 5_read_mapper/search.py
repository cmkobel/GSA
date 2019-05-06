import bwt_approx
from parsers import parse_fasta, parse_fastq
import sys
import pickle
import argparse
import sys
from pathlib import Path as path


parser = argparse.ArgumentParser(description = 'Read mapper based on burrows wheeler with branch and bound approximation.')

prep = parser.add_argument_group('preprocess')
prep.add_argument('--fasta', type = argparse.FileType('r'), help = 'genome file in fasta format', metavar = 'seqs.fasta')

map = parser.add_argument_group('map')
map.add_argument('--fastq', type = argparse.FileType('r'), help = 'reads file in fastq format', metavar = 'reads.fastq')
map.add_argument('-d', type = int, default = 0, help = 'number of edits, omission leads to exact search', metavar = 'edits')

args = parser.parse_args()



if hasattr(args.fasta, 'read'):
    #print('preprocessing', args.fasta)

#if sys.argv[1] == '-p' or sys.argv[1] == '--preprocess':
    """ Preprocess only. """

    #genome_file = sys.argv[2]
    genome_file = args.fasta

    print('will preprocess', genome_file.name)
    #out_file = '.'.join(genome_file.split('/')[-1].split('.')[0:-1]) + '.pickle' # isolate file name from path and extension.
    out_file = 'preprocessed_sequences_bw.pickle' # Use the same file name.


    dictionary = {} # Collects all the objects.

    for _i, genome in enumerate(parse_fasta(genome_file)):
        print('\t', _i, ': preprocessing ', genome['title'], sep = '')
        o = bwt_approx.search_bwt(genome['sequence'], genome['title']) # One object for each genome.
        o.main_preprocess()
        dictionary[_i] = o

    
    # Save dictionary with objects of all sequences to disk with pickle.
    with open(out_file, 'wb') as file:
        pickle.dump(dictionary, file)
        print()
        print('Successfully saved to:')
        print()
        print('\t' + out_file)
        print()

    if not hasattr(args.fastq, 'read'):
        print()
        print('Use these preprocessed sequences with a .fastq file containing reads by typing:')
        print()
        print('\t$ python3 search.py --fastq <reads_file.fastq>')
        print()





if hasattr(args.fastq, 'read'):
    #print('mapping reads from', args.fastq, 'with edit distance', args.d)
    """ Import files and search. """
    state = 'search'
    reads_file = args.fastq
    n_edits = args.d
    #print(sys.argv)
    preprocessed_file = 'preprocessed_sequences_bw.pickle' 
    #print('will map reads from', reads_file, 'onto sequence(s) from', preprocessed_file)

    try:
        with open(preprocessed_file, 'rb') as file:
            dictionary = pickle.load(file)
    except FileNotFoundError as e:
        print(e)
        print('\tYou need to preprocess the genome before you can map reads.')
        print('\texample: $ python3 search.py --fasta <seqs_file.fasta>')
        sys.exit()

    for i in dictionary: # Analogous to: for genome in genome_file:
        o = dictionary[i]

        for read in parse_fastq(args.fastq):
            #print(read['title'])
            #print(o.find_positions(read['sequence']))

            for match, cigar in o.find_positions(read['sequence'].lower(), n_edits):

                print(f"\
{read['title']}\t\
0\t\
{o.title}\t\
{match+1}\t\
0\t\
{cigar}\t\
*\t\
0\t\
0\t\
{read['sequence']}\t\
{len(read['sequence'])*'~'}")




    
