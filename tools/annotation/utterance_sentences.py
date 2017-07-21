#!/usr/bin/env python
"""utterance_sentences.py

This tool propagate the end and start time defined in refine.py tool to
the previous files.
The original files are backed up in .backup subfolder into each parent folder. 
This tool also generate the Kaldi's "text" file for the song.
This files can be concatenates to generate the total Kaldi's "text" file

Output file:
The output file have the structure of the Kaldi's "text" file which have
every utterance matched with its text transcription. 
The utterance that appears in this file are only the ones marked as 
"selected" equal true  and not marked as "wrong" in refine.py tool. 

PATTERN: <utteranceID> <text_transcription>
Example:

    F002_002_01_0101.00.001 This was all you
    F002_002_01_0101.00.002 none of it me
    F002_002_01_0101.00.003 You put your hands on 
    F002_002_01_0101.00.004 on my body and told me

Usage:
  utterance_sentences.py <codeaudio> <rootroute>
  utterance_sentences.py --help

Options:
  <codeaudio>         Code Name of the audio file (e.i. F001_01_01_0101)
  <rootroute>         The root route of the project directory.                         
  --help              Print this help screen
"""

import json
import shutil
import sys
import docopt
sys.path.append('..')
import helps


def gen_utterancesentence(track, rootroute):
    segfile = rootroute + 'segments/' +  track + '.json'
    jlyrics = rootroute + 'json_lyrics/' +  track + '.json'
    
    helps.ensure_dir(rootroute + 'segments/.backup/')
    
    shutil.copy(segfile, rootroute + 'segments/.backup/' +  track + '.json')
    
    outfolder = rootroute +'text/' + track[0] +'/'+ track[:4]+'/'
    helps.ensure_dir(outfolder)
    
    outfile = outfolder + track +'.text'
    helps.save_file(outfile, '')
    
    
    with open(segfile, 'r') as f:
        seg_file = json.load(f)
    with open(jlyrics, 'r') as f:
        json_lyrics = json.load(f)
    
    for line in range(len(json_lyrics)):    
        correct_sentence = 0
        if not 'wrong' in json_lyrics[line]:
            correct_sentence = 1
            
        elif json_lyrics[line]['wrong'] == False:
            correct_sentence = 1

        if  correct_sentence > 0:
            outtemplate = '{}.{:02d}.{:03d}'
            seg_file[line]['start'] = json_lyrics[line]['start']
            seg_file[line]['end'] = json_lyrics[line]['end']
            segment_name = outtemplate.format(json_lyrics[line]['wavfile'],
                                   json_lyrics[line]['repeat'],
                                   json_lyrics[line]['index'],
                                   0)

            if 'transcription' in json_lyrics[line]:
                text = json_lyrics[line]['transcription']
            else:
                text = json_lyrics[line]['lyric']  
            
            text = text.replace('\n', ' ').rstrip()
            text = text + '\n'
            
            not_letters_or_digits = u'{[*!?:()+/\",.-;]}'
            translate_table = dict((ord(char), None) for char in not_letters_or_digits)
            text = text.upper().translate(translate_table)
            segText = segment_name + " " + text    
            helps.append_file(outfile, segText)
        
    with open(segfile, 'wb') as f:
        json.dump(seg_file, f, indent=4, sort_keys=True)
        


def main():
     """Main method called from commandline."""
     arguments = docopt.docopt(__doc__)
     codeaudio = arguments['<codeaudio>']
     rootroute = arguments['<rootroute>']   
     gen_utterancesentence(codeaudio, rootroute)
    



if __name__ == '__main__':
    main()
