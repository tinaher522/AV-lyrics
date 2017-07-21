#!/usr/bin/env python
"""segment.

Segment WSJ utterances from CHiME continuous audio.

Reads annotations file containing timestamped code and generates
utteranc start-end time pairs and extracts audio from unsegmented wav.
Annotation file uses the following code,

'1' = utterance start
'9' = utterance end
'0' = repetition end
'D' = indicates a delta time to all future timestamps

Usage:
  segment.py <annotations> <outfilenm>
  segment.py --help

Options:
  <annotations>  Name of the file storing the annotation data
  <outfilenm>    Name of the output file
  --help         print this help screen

"""

from __future__ import print_function
import os
import json
import docopt


def segment_to_string(segment):
    """Return string representation of segment."""
    return "{}:{}-{}:{:03d}({:03d})".format(segment['wavfile'],
                                            segment['start'],
                                            segment['end'],
                                            segment['index'],
                                            segment['repeat'])


def build_segments(annotations, wav_filenm):
    """Build list of segment objects from list of annotation tuples."""
    opened = False
    segment = {}
    segments = []
    reaction_time = start_time = end_time = delay = 0.0
    segment_index = 0
    repeat = 0

    def add_segment():
        segment['index'] = segment_index
        segment['repeat'] = repeat
        segment['start'] = start_time - delay - reaction_time
        segment['end'] = end_time - delay
        segments.append(segment.copy())

    segment['wavfile'] = wav_filenm

    for (parameter, code) in annotations:
        if code in {'environment', 'speaker'}:
            segment[code] = parameter
        elif code in {'delay', 'D'}:  # A fix to the time code
            delay += parameter
        elif code in {'reaction_time'}:  # Command for reaction time setting
            reaction_time = parameter
        elif code in {'segment_index'}:  # Command to set next segment's index
            segment_index = parameter - 1
        elif code == '1':
            start_time = parameter
            if opened:
                # Multiple start point
                print('here')
            opened = True
        elif code == '9' or code == '0':
            opened = False
            if code == '9':
                segment_index += 1
                repeat = 0
            elif code == '0':
                repeat += 1
            end_time = parameter
            add_segment()
#            segment['index'] = segment_index
#            segment['repeat'] = repeat
#            segment['start'] = start_time - delay - reaction_time
#            segment['end'] = end_time - delay
#            segments.append(segment.copy())
            start_time = end_time
    return segments


def do_segment(annot_filenm, out_filenm):
    """Process raw annot_file to produce output segmentation file."""
    with open(annot_filenm, 'r') as infile:
        json_string = infile.read()
    annotations = json.loads(json_string)

    wav_filenm, ext = os.path.splitext(os.path.basename(annot_filenm))

    segments = build_segments(annotations, wav_filenm)

    with open(out_filenm, 'w') as outfile:
        outfile.write(json.dumps(segments, sort_keys=True, indent=4))


def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    out_filenm = arguments['<outfilenm>']
    annot_filenm = arguments['<annotations>']
    do_segment(annot_filenm, out_filenm)

if __name__ == '__main__':
    main()

# ./segment.py TR_141106_01.txt TR2_141106_01.seg
