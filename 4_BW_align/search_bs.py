import bs
from parsers import parse_fasta, parse_fastq
import sys
import pickle

"""
Usage:

python3 search_bs.py -p <reference.fasta>            Preprocess only.
python3 search_bs.py -i <reads.fastq>                Import preprocessed file and search only.



"""


if sys.argv[1] == '-p' or sys.argv[1] == '--preprocess':
    """ Preprocess only. """
    state = 'preprocess'
    genome_file = sys.argv[2]
    print('Will preprocess', genome_file)
    #out_file = '.'.join(genome_file.split('/')[-1].split('.')[0:-1]) + '.pickle' # isolate file name from path and extension.
    out_file = 'preprocessed_sequences_bs.pickle' # Use the same file name.


    dictionary = {} # Collects all the objects.

    for _i, genome in enumerate(parse_fasta(genome_file)):
        print('\t', _i, ': preprocessing ', genome['title'], sep = '')
        o = bs.search_bs(genome['title'], genome['sequence']) # One object for each genome.
        o.preprocess()
        dictionary[_i] = o


    # Save dictionary with objects of all sequences to disk with pickle.
    with open(out_file, 'wb') as file:
        pickle.dump(dictionary, file)
        print()
        print('Successfully saved to:')
        print()
        print('\t' + out_file)

    print()
    print('Use these preprocessed sequences with a .fastq file containing reads by typing:')
    print()
    print('\tpython3 search_bw.py -i <reads_file.fastq>')
    print()




elif sys.argv[1] == '-i' or sys.argv[1] == '--import':
    """ Import files and search. """
    state = 'search'
    reads_file = sys.argv[2]
    preprocessed_file = 'preprocessed_sequences_bs.pickle' 
    #print('will map reads from', reads_file, 'onto sequence(s) from', preprocessed_file)

    with open(preprocessed_file, 'rb') as file:
        dictionary = pickle.load(file)

    for i in dictionary: # Analogous to: for genome in genome_file:
        o = dictionary[i]

        for read in parse_fastq(reads_file):
            #print(read['title'])
            #print(o.find_positions(read['sequence']))

            for match in o.find_positions(read['sequence'].lower()):

                print(f"\
{read['title']}\t\
0\t\
{o.title}\t\
{match+1}\t\
0\t\
{len(read['sequence'])}M\t\
*\t\
0\t\
0\t\
{read['sequence']}\t\
{len(read['sequence'])*'~'}")




    
