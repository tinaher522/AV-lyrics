#!/usr/bin/env python
"""batch_modification.py

Tool import create_modification and perform a set of modification 
to the entire database generating a mix of them in diferent directories

Usage:
  batch_modification.py  <audio_route> <destroute> <text_files_route>
  batch_modification.py --help

Options:
  <audio_route>              Root directory of the segments audios
  <destroute         >       Root directoy of where the modifications will be save
  <text_files_route>         Root directorie where the "text" files are save
  --help                     Print this help screen
  
"""

import os
import shutil
import sys
import docopt

import create_modification as cm
sys.path.append('tools')
from helps import * 


def gen_modifications(fil, root, destroute, text_files_route):
    
    audio_code = fil[:16]
    gender = audio_code[0]
    singer = audio_code[:4]
    
    

    dest = destroute + gender + "/" + singer + "/"
    ensure_dir(dest)
    
    cm.create_modification(fil, root, dest, 1    ,  200)
    cm.create_modification(fil, root, dest, 1    , -200)
    cm.create_modification(fil, root, dest, 1.10 ,    0)
    cm.create_modification(fil, root, dest, 0.90 ,    0)
    cm.create_modification(fil, root, dest, 1.10 ,  200)
    cm.create_modification(fil, root, dest, 0.90 , -200)
    cm.create_modification(fil, root, dest, 1.10 , -200)
    cm.create_modification(fil, root, dest, 0.90 ,  200)
       
    
    
def gen_mod_text(text_files_route, audio_code, tempo, pitch):
    
    tempo_mod = "{0:02d}".format(tempo)  
    pitch_mod = "{0:02d}".format(pitch)
        
    infile = text_files_route + '/' + audio_code[0] + '/' + audio_code[:4] + '/' + audio_code + '.text'
    outdir = text_files_route.replace('text' , 'text_mod') + "/" + audio_code[0] + '/' + audio_code[:4] + '/' 
    outfile =  outdir + audio_code[0:12] + pitch_mod + tempo_mod + '.text'
    
    ensure_dir( outdir )
    shutil.copy(infile, outfile)
    dest = []
    with open(infile) as f:
        for line in f:
            dest.append(line.replace(audio_code, audio_code[0:12] + pitch_mod + tempo_mod))
    
    with open(outfile, 'w') as f:
        f.write("".join(dest))
    
    

def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    audio_route = arguments['<audio_route>']
    destroute = arguments['<destroute>']
    text_files_route = arguments['<text_files_route>']
        
    for root, dirs, files in os.walk(audio_route, topdown=True):         
        for fil in files:
            if ".wav" in fil:
                gen_modifications(fil, root, destroute, text_files_route)
    
    for root, dirs, files in os.walk(text_files_route, topdown = True):
        for fil in files:
            if "MOD" not in root:
                gen_mod_text(text_files_route, fil[:16], 1, 2)
                gen_mod_text(text_files_route, fil[:16], 1, 3)
                gen_mod_text(text_files_route, fil[:16], 2, 1)
                gen_mod_text(text_files_route, fil[:16], 3, 1)
                gen_mod_text(text_files_route, fil[:16], 2, 2)
                gen_mod_text(text_files_route, fil[:16], 3, 2)
                gen_mod_text(text_files_route, fil[:16], 2, 3)
                gen_mod_text(text_files_route, fil[:16], 3, 3)
   

if __name__ == '__main__':
    main()