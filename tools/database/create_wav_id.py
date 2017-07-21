#!/usr/bin/env python
"""create_wav_id.py

Create a copy of the audios en 16k mono version

Usage:
  create_wav_id.py <originroute> <originfile> <destroute> <destnamelist>
  create_wav_id.py --help

Options:
  <originroute>         Route where original files are located 
  <originfile>          File with name of the original files' names.                      
  <destroute>           Route where the copy files will be saved.
  <destnamelist>        File with name of destination files      
  --help                Print this help screen
"""

import subprocess
import docopt

def copyfiles(oroute, oname, droute, dname):
    print "Copying wav files into format <id>.wav....."  
    origins = []
    with open(oname) as f:
        for index, line in enumerate(f):
            origins.append(oroute + line.replace('\n',''))
    
    destinations = []
    with open(dname) as f:
        for index, line in enumerate(f):
            name = line.replace('\n','').split(",")[0].replace('\n','').lstrip().rstrip() 
            if name[0] == 'F':
                destinations.append(droute + "F/" + name + ".wav")
            elif name[0] == 'M':
                destinations.append(droute + "M/" + name + ".wav")
    
    count = 0
    for i in range(len(origins)):
        count += 1
        #sox wonderwall_1.wav wonderwall_1.16k.wav rate 16000 channels 1
        subprocess.call(['sox', '-G', '-v', '0.99', origins[i], destinations[i], 'rate', '16000' ,
                         'channels', '1'])
    
    print "Created", count, "files."
    
    

def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    oroute = arguments['<originroute>']
    oname = arguments['<originfile>']
    droute = arguments['<destroute>']
    dname = arguments['<destnamelist>']
    copyfiles(oroute, oname, droute, dname)

if __name__ == '__main__':
    main()
