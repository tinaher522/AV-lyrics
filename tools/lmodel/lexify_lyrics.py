#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""lexify_lyrics.py

Translate raw lyrics into lexicon entries

Usage:
  lexify_lyric.py <lyrics_in_fn> <lexicon_fn> <lyrics_out_fn> <oov_words_fn>
  lexify_lyric.py --help

Options:
  <lyrics_in_fn>  File storing raw lyrics
  <lexicon_fn>   File storing lexicon
  <lyrics_out_fn> Lexified lyric output
  <oov_words_fn> File storing oov words
  --help         print this help screen

"""

from __future__ import print_function
import docopt
import inflect


def del_repeatedletters(line):
    while 'AA' in line:
        line = line.replace('AA', 'A')
    while 'EEE' in line:
        line = line.replace('EEE', 'EE')
    while 'II' in line:
        line = line.replace('II', 'I')
    while 'OOO' in line:
        line = line.replace('OOO', 'OO')
    while 'UU' in line:
        line = line.replace('UU', 'U')
    while 'HH' in line:
        line = line.replace('HH', 'H')
    while 'WW' in line:
        line = line.replace('WW', 'W')
    
    return line


def del_repeatedword(line):
    word1=""
    newline = []
    for word in line.split():
        if word != word1:
            newline.append(word)
            word1 = word
    nl = " ".join(newline) #+ "\n"
    return nl + "\n"


def number2word(number):
    p = inflect.engine()
    return p.number_to_words(number, group=2).replace("," , "").replace("-", " ")
    # By default 995 is returned as ninety-nine, five
    # Changed as ninety nine five
    

def read_lexicon(lex_fname):
    """Read a lexicon file."""
    with open(lex_fname, 'r') as f:
        lexicon = {line.split()[0].split('(')[0] for line in f}
    return lexicon


def lexify_raw_lyrics(lyrics_fname, lexicon):
    """Lexify raw lyrics."""
    with open(lyrics_fname, 'r') as f:
        oov_words = set()
        lexlines = []
        for line in f:
            
            # Clean repeated letter in a word
            line = del_repeatedletters(line)
                        
            # Clean repeated word in a sentence
            line = del_repeatedword(line)
            
            lexwords = []
            if "CHORUS" in line.upper():
                line = ""
            line = line.replace('-', ' ').replace('...', ' ').replace(',' , ' ').strip(' ')
            for word in line.split():
                if word[0] in ['[', '('] and word[-1] in [']', ')'] :
                    word = ""                
                word = word.replace('“' , '').replace('»', '').strip(' ')
                
                word = word.upper().translate(None, "{[*!?:()+#|/\";]}").strip('.')  

                if word.isdigit():
                    word = number2word(word).upper()

                
                # The split occurs after a number normalization
                # example:
                # word = 55
                # become = fifty five 
                for w in word.split(" "):
                    w = w.replace("\xe2\x80\x99", "'")\
                            .replace("\xe2\x80\x98", "'")\
                            .replace("\xc3\xa9", "e")\
                            .replace("\xc3\xaf", "i")\
                            .replace("\xc2\xa0" , "")\
                            .replace("\xe2\x80\x94", " ")\
                            .replace("\xe2\x80\xa8", " ")\
                            .replace("\xe2\x81\xa5", "")\
                            .replace("\xe2\x81\xb2", "")\
                            .replace("\xe2\x81\xb3", "")\
                            .replace("\xe2\x80\xa6", "").strip()
                    if w not in lexicon:
                        if w[-3:]== "IN'":
                            w1 = w.replace("IN'", "ING")
                            if w1 not in lexicon:
                                oov_words.add(w)
                                w = '<UNK>' + w + '</UNK>'
                            else:
                                w = w1
                    # Add word in lexword but prevent empty words.
                    # Empty words can produce several empty sentences.
                    if w <> "":
                        lexwords.append(w)
            sentence = " ".join(lexwords)
            
            # Keep only 2 <UNK> words per sentence
            if sentence.count('<UNK>')<3:
                if len(lexwords)>0:
                    lexlines.append(sentence)

    return lexlines, oov_words


def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    lyrics_in_fn = arguments['<lyrics_in_fn>']
    lexicon_fn = arguments['<lexicon_fn>']
    lyrics_out_fn = arguments['<lyrics_out_fn>']
    oov_words_fn = arguments['<oov_words_fn>']

    lexicon = read_lexicon(lexicon_fn)
    lex_lines, oov_words = lexify_raw_lyrics(lyrics_in_fn, lexicon)

    with open(lyrics_out_fn, 'w') as f:
        f.write("\n".join(lex_lines))

    with open(oov_words_fn, 'w') as f:
        f.write("\n".join(sorted(oov_words)))

if __name__ == '__main__':
    main()

# e.g.,
# ./lexify_lyrics.py dictionary/collection \
#     lexicon/cmudict_SPHINX_40 lyrics_out.txt oov_words.txt

# raw - 30192 (183081) missing; 18791 (1522479) present
# removed '"'  28570 missing; 18819 present
# removed *!?:()\",;] 14649 (60260) missing; 19696 present (1645300)
# stripped .  11259 missing (45777)  ; 19773 present (1659783)
# removed '-' 9016 missing (39135); 19914 present (1673484)
# removed '...' 8650 missing (38685); 19920 present (1674657)
# removed {[  8412 missing (37908); 19930 present (1675434)
