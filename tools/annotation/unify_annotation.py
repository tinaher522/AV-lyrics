#!/usr/bin/env python
"""unify_annotation.py

Tool that integrate the diferent annotation tools in one.
this tool assume an specific folder and files structure.

Usage:
  unify_annotation.py  <rootroute> <codeaudio> <chk> [-r]
  unify_annotation.py  --help

Options:
  <codeaudio>         Code Name of the audio file (e.i. F001_01_01_0101)
  <rootroute>         The root route of the project directory. 
  <chk>               chunk (i.e.  chk01)
  -r                  Replace files if exist                        
  --help              Print this help screen
"""

import subprocess
import segment
import add_lyrics
import jsonify_lyric
import extract
import docopt
import os.path
import time



def create_files(rootroute, codeaudio, gender, chunk):
    
    segment.do_segment(rootroute+'annotation/annotate/'+codeaudio+'.json',
                       rootroute+'annotation/segments/'+codeaudio+'.json')
    print rootroute+'annotation/lyrics/lyrics/'+chunk+'/'+codeaudio+'.lyrics'                 
    jsonify_lyric.jsonify_lyric(rootroute+'annotation/lyrics/lyrics/'+chunk+'/'+codeaudio+'.lyrics',
                                rootroute+'annotation/lyrics/json/'+codeaudio+'.lyrics.json')
   
    add_lyrics.add_lyrics(rootroute+'annotation/segments/'+codeaudio+'.json', 
                         rootroute+'annotation/lyrics/json/'+codeaudio+'.lyrics.json', 
                         rootroute+'annotation/json_lyrics/'+codeaudio+'.json')
   

def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    codeaudio = arguments['<codeaudio>']
    gender = codeaudio[0]
    cartist = codeaudio[0:4]
    rootroute = arguments['<rootroute>']
    chunk = arguments['<chk>']
    replacefiles = 0    
    if (arguments['-r']):
        replacefiles = 1
    
    if (not os.path.isfile(rootroute+'annotation/segments/'+codeaudio+'.json')):              
        create_files(rootroute, codeaudio, gender, chunk)
    elif (replacefiles == 1):     
        create_files(rootroute, codeaudio, gender, chunk)
        
    subprocess.call(['python', rootroute+'tools/annotation/refine.py',
                     rootroute+'annotation/json_lyrics/'+codeaudio+'.json',
                     rootroute+'wav/16k/'+gender+'/'])
                     
    extract.do_extract(rootroute+'annotation/json_lyrics/'+codeaudio+'.json',
                       rootroute+'wav/16k/'+gender+'/', 
                       rootroute+'wav/wav_segments/'+gender+'/'+cartist+'/', 
                       padding=0.0)
                       
    subprocess.call(['python', rootroute+'tools/annotation/utterance_sentences.py',
                     codeaudio,rootroute + 'annotation/'])
    
    time.sleep(2)

    
    
if __name__ == '__main__':
    main()