#!/usr/bin/env python
"""create_modification.py

Tool to create a PITCH and/or TEMPO modification of a collection of utterance.
This tool use SOX in order to create these modifications

Usage:
  create_modification.py  <audio_code> <sourceroute> <destroute> ([--tempo TEMPO] [--pitch PITCH])   
  create_modification.py --help

Options:
  <audio_code>               Original Audio Code (eg. F002_002_01_0101) 
  <sourceroute>              Route to where the original utterances of the song are saved
  <destroute>                Route whete the modification of the utterances will be saved.
  --tempo TEMPO              Value of the tempo modification [default: 1]
  --pitch PITCH              Value of the pitch modification [default: 0]
  --help                     Print this help screen
  
"""

import os
import subprocess
import sys
import docopt
sys.path.append('tools')
from helps import * 


def create_modification(audio, route, destroute, tempo, pitch):
    if tempo > 1:
        tempo_mod = "02" # up
    elif tempo < 1:
        tempo_mod = "03" # down 
    else:
        tempo_mod = "01" # original
    
    if pitch > 0:
        pitch_mod = "02" # up
    elif pitch < 0:
        pitch_mod = "03" # down
    else:
        pitch_mod = "01" # original
        
    ensure_dir(destroute)
    
    new_name = audio[:12] + pitch_mod + tempo_mod + audio[16:] 
    if tempo == 1 and pitch != 0:
        subprocess.call(['sox', '-G', '-v', '0.99', route + "/"+ audio, destroute + new_name ,  'pitch', str(pitch)])
    
    if tempo != 1 and pitch == 0:
        subprocess.call(['sox', '-G', '-v', '0.99', route +  "/"+ audio, destroute + new_name ,  'tempo', str(tempo)])
        
    if tempo != 1 and pitch != 0:
        subprocess.call(['sox', '-G', '-v', '0.99', route +  "/"+ audio, destroute + new_name ,  'pitch', str(pitch) ,
                         'tempo', str(tempo)])
    

def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    audio_code = arguments['<audio_code>']
    sourceroute = arguments['<sourceroute>']
    destroute = arguments['<destroute>']
    tempo = float(arguments['--tempo'])
    pitch = int(arguments['--pitch'])
        
    for root, dirs, files in os.walk(sourceroute, topdown=True):
        for fil in files:
            if audio_code in fil:
                 create_modification(fil, root, destroute, tempo, pitch)
            
   

if __name__ == '__main__':
    main()
