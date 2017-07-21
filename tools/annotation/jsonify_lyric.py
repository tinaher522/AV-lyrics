#!/usr/bin/env python
"""jsonify_lyrics.

Tool to turn lyrics text file into JSON format

Usage:
  jsonify_lyric.py <lyricfilenm> <outfilenm>
  jsonify_lyric.py --help

Options:
  <lyricfilenm>  Name of the lyric file
  <outfilenm>    Name of the output jsonified lyric file
  --help         print this help screen

"""

from __future__ import print_function
import json
import docopt


def jsonify_lyric(lyricfilenm, outfilenm):
    """Turn lyrics file into json format."""
    lyrics = []
    with open(lyricfilenm) as f:
        for index, line in enumerate(f):
            line_dict = dict()
            line_dict = {'lyric': line, 'index': index + 1}
            lyrics.append(line_dict)

    with open(outfilenm, 'w') as outfile:
        outfile.write(json.dumps(lyrics, sort_keys=True, indent=4))


def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    lyricfilenm = arguments['<lyricfilenm>']
    outfilenm = arguments['<outfilenm>']

    jsonify_lyric(lyricfilenm, outfilenm)

if __name__ == '__main__':
    main()
