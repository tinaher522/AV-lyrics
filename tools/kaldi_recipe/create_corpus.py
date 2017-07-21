#!/usr/bin/env python
"""create_corpus.py

Tool to download lyrics text from wikia website

Usage:
  create_corpus.py  <lexify_lyrics> <dictionary> <corpus_file> 
  create_corpus.py --help

Options:
  <lexify_lyrics>               File with the lexify lyrics
  <dictionary>                  5K dictionary
  <corpus_file>                 File with output corpus.
  --help                        print this help screen

"""

import docopt

def create_corpus(lexify_lyrics, dictionary):
    lexicon = []
    with open(dictionary) as f:
        for line in f:
            lexicon.append(line.split()[0])

    corpus = []
    with open(lexify_lyrics) as f:
        for line in f:
            delete = 0
            for word in line.split():
                if word not in lexicon:
                    delete = 1
                    break
            if delete == 0:
                line = line.replace('\n', "")
                corpus.append("<s> " + line + " </s>")
    
    return corpus

def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    lexify_lyrics = arguments['<lexify_lyrics>']
    dictionary = arguments['<dictionary>']
    corpus_file = arguments['<corpus_file>']

    corpus = create_corpus(lexify_lyrics, dictionary)
            
    with open(corpus_file, 'wb') as f:
        f.write("\n".join(corpus))


if __name__ == '__main__':
    main()
