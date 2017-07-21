#!/usr/bin/env python
"""add_lyrics.

Tools to add the lyrics the utterance level JSON segmentation file

Usage:
  add_lyrics.py <segfilenm> <lyricfilenm> <outfilenm>
  add_lyrics.py --help

Options:
  <segfilenm>    Name of the segmentation file
  <lyricfilenm>  Name of json lyric file
  <outfilenm>    Name of the output segmentation file
  --help         print this help screen

"""

from __future__ import print_function
import json
import pandas as pd
import docopt


def add_lyrics(seg_filenm, lyric_filenm, out_filenm):
    """Add prompts to JSON segmentation files."""
    print('Processing: {}'.format(seg_filenm))

    segments = pd.read_json(seg_filenm)
    lyrics = pd.read_json(lyric_filenm)
    segments = pd.merge(segments, lyrics)

    with open(out_filenm, 'w') as outfile:
        json.dump(segments.T.to_dict().values(), outfile,
                  indent=4, sort_keys=True)


def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    segfilenm = arguments['<segfilenm>']
    lyricfilenm = arguments['<lyricfilenm>']
    outfilenm = arguments['<outfilenm>']

    add_lyrics(segfilenm, lyricfilenm, outfilenm)

if __name__ == '__main__':
    main()
