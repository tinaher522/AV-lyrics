#!/usr/bin/env python
"""extract.

Extract video segments from continuous video

Usage:
  extract.py [-f] [-p pad] [-c channel] <segfilenm> <inwavroot> <outwavroot>
  extract.py --help

Options:
  <segfilenm>    Name of the segmentation file
  <inwavroot>    Name of the root dir for the input video file
  <outwavroot>   Name of the root dir for the output segments
  -p <pad>, --padding=<pad> padding at start and end in seconds  [default: 0]
  --help         print this help screen

"""

from __future__ import print_function
import json
import os
import subprocess
import argparse
import sys


def extract(segment, in_root, out_root, padding=0.0, channel=0):
    """Use ffmpeg to extract segment from mp4 file.

    in_root - root directory for unsegmented video files
    out_root - root directory for output video segments
    """
    infilenm = '{}/{}.mp4'.format(in_root, segment['wavfile'], channel)

    outtemplate = '{}/{}.{:02d}.{:03d}.mp4'
    outfilenm = outtemplate.format(out_root,
                                   segment['wavfile'],
                                   segment['repeat'],
                                   segment['index'],
                                   channel)
    correct_sentence = 0
    if not 'wrong' in segment:
        correct_sentence = 1
        
    elif segment['wrong'] == False:
        correct_sentence = 1

    if  correct_sentence > 0:                            
        subprocess.call(['ffmpeg', '-ss', str(segment['start'] - padding),
                         '-i', infilenm ,'-t', str(segment['end'] -segment['start']), outfilenm ])


def to_string(segment):
    """Return string representation of a segment."""
    return "{}:{}-{}:{:03d}({:03d})".format(segment['wavfile'],
                                            segment['start'],
                                            segment['end'],
                                            segment['index'],
                                            segment['repeat'])


def do_extract(seg_filenm, in_root, out_root, padding=0.0):
    """Extract segments listed in seg file."""
    with open(seg_filenm, 'r') as infile:
        json_string = infile.read()
    segments = json.loads(json_string)

    if not os.path.isdir(out_root):
        os.makedirs(out_root)

    print('Extracting video ...')

    for i, segment in enumerate(segments):
        sys.stdout.write(' Processing segment {: 5}/{: <5}\r'
                         .format(i + 1, len(segments)))
        sys.stdout.flush()

        extract(segment, in_root, out_root, padding=padding)
    sys.stdout.write('\n')
    sys.stdout.flush()


def main():
    """Main method called from commandline."""
    parser = argparse.ArgumentParser(description='Extract CHiME 3 video segments from continuous video.')
    parser.add_argument('segfilenm', metavar='<segfilenm>',
                        help='Name of the segmentation file', type=str)
    parser.add_argument('inmp4root', metavar='<inmp4root>',
                        help='Name of the root dir for the input video file',
                        type=str)
    parser.add_argument('outmp4root', metavar='<outmp4root>',
                        help='Name of the root dir for the output segments',
                        type=str)
    parser.add_argument('-p', '--padding', metavar='pad',
                        help='Padding at start and end in seconds [default: 0]',
                        type=float, default=0)

    args = parser.parse_args()

    segfilenm = args.segfilenm
    in_root = args.inmp4root
    out_root = args.outmp4root
    padding = args.padding

    do_extract(segfilenm, in_root, out_root, padding)


if __name__ == '__main__':
    main()

# ./extract.py ../../data/annotations/utterance/LR_141103_01.json \
#     ../../data/16khz16bit xxx
#./extract1.py /Users/xinghuihe/Desktop/AV/annotation/json_lyrics/F002_102_01_0101.json /Users/xinghuihe/Desktop/AV/video/origin /Users/xinghuihe/Desktop/AV/video/mp4_segments/F/F002