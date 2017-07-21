#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_vocabulary.py

From a collection of files. this tool create a vocabulary of the <wr> most
common words. 
By default <wr> = 5000

Usage:
  create_vocabulary.py <rootroute> <lyrics_in_fn> <lexicon_fn> [-o FILE] [--words=<wr>] 
  create_vocabulary.py --help

Options:
    <rootroute>                 Origin path of the lyrics test and train data.
    <lyrics_in_fn>              File storing raw lyrics
    <lexicon_fn>                File storing lexicon
    --words=<wr>                Size of Vocabulary [default: 5000].  
    -o FILE, --output FILE      Path and name of the output file [default: lmodel/lexicon.txt].
    --help                      Print this help screen.
"""

import docopt
import os
import re
import random
import inflect

def number2word(number):
    p = inflect.engine()
    return p.number_to_words(number, group=2).replace("," , "").replace("-", " ")
    
def gen_dictofwords(lyric_path):
    dictwords = {}
    delimiters = ",", "!", "-", "(", ")", " ", "\n", "?", ".", "<", ">", "\"", "!", ";", ":", "@", "#", "/"
    regexPattern = '|'.join(map(re.escape, delimiters))
    for root, dirs, files in os.walk(lyric_path, topdown=True):
        for fil in files:
            with open(root + '/' + fil) as f:
                for index, line in enumerate(f):
                    words = re.split(regexPattern, line)
                    for word in words:
                        word = word.replace("\xe2\x80\x99", "'")\
                            .replace("\xe2\x80\x98", "'")\
                            .replace("\xc3\xa9", "e")\
                            .replace("\xc3\xaf", "i")\
                            .replace("\xc2\xa0" , "")
                        
                        if not word == "":
                            if word.isdigit():
                                 word = number2word(word).upper()
                            for w in word.split():
                                if w.upper() in dictwords:
                                    dictwords[w.upper()] += 1
                                else:
                                    dictwords[w.upper()] = 1
    return dictwords

def gen_vocabulary(lyrics_in_fn, rootroute, lexicon_fn, numberwords):
    # Words in Train and Test Lyrics 
    words = gen_dictofwords(rootroute)
    # Words in the Lexicon File
    lexicon = {}
    with open(lexicon_fn, 'r') as f:
        for line in f:
            splited_line = line.split('\t')
            lexicon[splited_line[0]] = splited_line[1]
    
    # Words of Train and Test data 
    # in the lexicon file
    vocabulary = []
    for word in words:
        if word in lexicon:
            if word not in vocabulary:
                vocabulary.append(word.replace("\n",""))
        else:
            if word[-3:]== "IN'":
                word = word.replace("IN'", "ING")
                if word in lexicon:
                    if word not in vocabulary:
                        vocabulary.append(word.replace("\n",""))
                

    lyrics_words = []
    # Words in all the lyrics Collection  
    with open(lyrics_in_fn) as f:   
        for line in f:
            for word in line.split():
                lyrics_words.append(word)

    if len(vocabulary) > numberwords:
        vocabulary = vocabulary[:numberwords]

    # Words of the Lyrics Collection
    # in the Lexicon File
    # and OOV words that are necessary for complete the 
    # 5k words

    while len(vocabulary) < numberwords:
        random_index = random.randrange(0,len(lyrics_words))
        if lyrics_words[random_index] not in vocabulary:
            if lyrics_words[random_index] in lexicon:
                vocabulary.append(lyrics_words[random_index].replace("\r",""))
            
    
    for i in range(numberwords):
        vocabulary[i]= vocabulary[i] + " " + lexicon[vocabulary[i]].replace("\r","")
    vocabulary = ['!SIL SIL\n','<UNK> SPN\n'] + vocabulary
    return vocabulary
        

def main():
    
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    
    lyrics_in_fn = arguments['<lyrics_in_fn>'] 
    rootroute = arguments['<rootroute>']  
    lexicon_fn = arguments['<lexicon_fn>']
    numberwords = int(arguments['--words'])
    outputfile = arguments['--output']  
     
    vocabulary = gen_vocabulary(lyrics_in_fn, rootroute, lexicon_fn, numberwords)
    
    with open(outputfile, 'w') as f:
        f.write("".join(vocabulary))

    
if __name__ == '__main__':
    random.seed('ASR-music')
    main()
    
    
    
    
    