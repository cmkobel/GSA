import bwt_approx as ba
import multiprocessing as mp
import json

S = 'mississippimississippi'
o = ba.search_bwt(S)


o.main_preprocess()

reads = ['mississippimississippi',
         'mmssissippimississippi', 
         'mimsissippimississippi', 
         'mismissippimississippi', 
         'missmssippimississippi', 
         'missimsippimississippi', 
         'missismippimississippi', 
         'mississmppimississippi', 
         'mississimpimississippi', 
         'mississipmimississippi', 
         'mississippmmississippi', 
         'mississippimississippi', 
         'mississippimmssissippi', 
         'mississippimimsissippi', 
         'mississippimismissippi', 
         'mississippimissmssippi', 
         'mississippimissimsippi', 
         'mississippimissismippi', 
         'mississippimississmppi', 
         'mississippimississimpi', 
         'mississippimississipmi', 
         'mississippimississippm']

    


#print(json.dumps(job_list, indent = 4))


def segregate_jobs(reads):
    try:
        num_cores = mp.cpu_count()
    except NotImplementedError:
        num_cores = 2

    job_list = []
    start = 0
    for core in range(num_cores):
        end = start + int(len(reads)/num_cores)
        job_list.append(reads[start:end])
        start = end
    if end < len(reads):
        job_list.append(reads[end:len(reads)])

    return job_list

job_list = segregate_jobs(reads)

def read_mapping(reads):
    


    results = []
    for read in reads:
        for position, cigar in o.find_positions(read, 1):
            results.append((position, cigar))
    return results

def multithread():
    rv = []
    with mp.Pool(mp.cpu_count()) as pool:
        for job in pool.map(read_mapping, job_list):
            for result in job:
                rv.append(result)
    return rv

for match, cigar in multithread():
    print(match, cigar)

