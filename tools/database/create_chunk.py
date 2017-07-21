#!/usr/bin/env python
"""create_chunk.py



Usage:
  create_chunk.py <coversfile> <outroute> [--chunksize=<chunk>] [--firstchunk=<value>]
  create_chunk.py -h | --help

Options:
  <coversfile>          output from "create-database.py"
  <outroute>            Name of directory for output files      
  --chunksize=S         The S int size of each chunk [default: 20]
  --firstchunk=<value>  Number of the first chunk [default: 1]
  -h --help             Print this help screen
"""

import sys

import docopt

from lyrics.tools import helps


def get_ocurrentid(base, id_base):
    return [oc for oc,x in enumerate(base) if x == id_base]

# result = result list of positions
def search_by_artist(result, cartist, track, searchvalue, maxvalue):
    result_temp = get_ocurrentid(cartist, searchvalue)
        

    for ca in result_temp:
        if not ca in result:
            result.append(ca)
            if len(result) > maxvalue:
                print "ERROR"
                print "Chunk size:", maxvalue
                print "Current size in recusive:", len(result)
                print "Increase chunk size"
                sys.exit(0)
            result_tt = search_by_track(result, cartist, track, track[ca],maxvalue)

    
    return result

def search_by_track(result, cartist, track, searchvalue, maxvalue):
    result_temp = get_ocurrentid(track, searchvalue)
    for temp in result_temp:
        if not temp in result_temp:
            result.append(temp)
    
    for ca in result_temp:
        if not ca in result:
            result.append(ca)
            result_tt = search_by_artist(result, cartist, track, cartist[ca],maxvalue)
        
    return result_temp
 
    

def gen_chunks(coversfile, outroute, chunksize, firstchunk):
    
    idlist = []    
    covers = []
    with open(coversfile) as f:
        for index, line in enumerate(f):
            idlist.append(line.replace('\n','').split(",")[0].replace('\n','').lstrip().rstrip())
            covers.append(line)    
            
    cartist = []
    for i in range(len(idlist)):
        cartist.append(idlist[i][:4])
        
    track = []  
    for i in range(len(idlist)):
        track.append(idlist[i][5:8])

    
    nc = len(idlist) / chunksize
    
    chunks = [[] for i in range(nc)]

    chunk = 0
    
    for i in range(len(cartist)):
        if cartist[i] != "":
            temp_list = search_by_artist([], cartist, track, cartist[i], chunksize)
            if ((chunksize - len(chunks[chunk])) >= len(temp_list)):
                # print chunk+1, chunksize, len(chunks[chunk]), len(temp_list)
                for s in temp_list:              
                    chunks[chunk].append(s)   
                if len(chunks[chunk]) == chunksize:
                    chunk += 1  
            else: 
                for s in temp_list:              
                    chunks[chunk+1].append(s) 
                # print "else", chunk+1, chunksize, len(chunks[chunk]), len(temp_list)
            for j in temp_list:
                cartist[j]=""
    
    coversfile_chunk = ""
    for subchunk in range(len(chunks)):
        for pos in range(chunksize):
            coversfile_chunk += covers[chunks[subchunk][pos]].replace("\n","") + ",chk" + str(subchunk+1+firstchunk) +"\n"
    
    database = outroute + "covers_chunk_" + coversfile.split('_')[-1] 
    helps.ensure_dir(database)
    f = open(database, 'wb')
    f.write(coversfile_chunk)
    f.close
    print "File covers with chunk created"


       
   

def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    coversfile = arguments['<coversfile>']
    outroute = arguments['<outroute>']
    chunksize = int(arguments['--chunksize'])
    firstchunk = int(arguments['--firstchunk']) - 1
    gen_chunks(coversfile, outroute, chunksize, firstchunk)

if __name__ == '__main__':
    main()
