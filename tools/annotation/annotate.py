#!/usr/bin/env python
"""annotate.

Simple tool for marking start and end of each lyric.
Once running press
   '1' to mark the start of a line.
   '9' to mark the end of a line
   ' ' to mark an annotation error
   'q' to quit

Usage:
  annotate.py <wavfilenm> <outfilenm>
  annotate.py --help

Options:
  <wavfilenm>    Name of the audio file to annotate
  <outfilenm>    Name of output file in which to store annotations
  --help         print this help screen
"""

from __future__ import print_function
import json
import subprocess
import sys
import tempfile
import termios
import time
import tty

import docopt


def getch():
    """Return character corresponding to a key press."""
    file_desc = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_desc)
    try:
        tty.setraw(file_desc)
        char_code = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)
    return char_code


class Annotations(object):
    """
    Class to represent a set of annotation.

         annotations are represented as a list of tuples
         (timestamp, code) where
         timestamp -- floating point time in seconds
         code -- a single character code indicating type of event
      Annotation codes:
       'S' - start of recording
       '1' - start of an utterance
       '9' - end of an utterance
       ' ' - annotator error. Preceding annotations need checking.
    """

    def __init__(self, wavfilenm, outfilenm, valid_chars):
        """Construct and start an annotator."""
        self.annotations = []
        self.valid_chars = valid_chars
        self.wavfilenm = wavfilenm
        self.outfilenm = outfilenm
        self.start_time = 0.0
        self.proc = None
        # Start the audio player
        print(wavfilenm)

    def start(self):
        """Start the annotator."""
        _tempfile = tempfile.TemporaryFile()
        self.proc = subprocess.Popen(['play', self.wavfilenm],
                                     stdin=_tempfile,
                                     stderr=_tempfile)
        # Note, tempfile necessary above as subprocess.PIPE
        # will hang after a few minutes of auido see,
        # http://thraxil.org/users/anders/posts/2008/
        # 03/13/Subprocess-Hanging-PIPE-is-your-enemy/
        self.start_time = time.time()
        self.add('S', 0.0)

    def add(self, code, timestamp=None):
        """Add an annotation with code 'code' at time 'timestamp'."""
        if code not in self.valid_chars:
            return False

        if timestamp is None:
            timestamp = time.time() - self.start_time
        new_annotation = (timestamp, code)
        self.annotations.append(new_annotation)
        with open(self.outfilenm, 'a') as outfile:
            outfile.write(str(new_annotation) + '\n')
        print(new_annotation)
        return True

    def stop(self):
        """Finish annotating."""
        # Kill the audio player
        subprocess.call(['kill', '-9', '%d' % self.proc.pid])
        self.add('E')
        self.save(self.outfilenm)

    def save(self, outfilenm):
        """Save the annotations to a file."""
        with open(outfilenm, 'w') as outfile:
            json.dump(self.annotations, outfile, indent=2)

    def get_annotations(self):
        """Return the list of annotations."""
        return self.annotations


def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    wavfilenm = arguments['<wavfilenm>']
    outfilenm = arguments['<outfilenm>']

    annotations = Annotations(wavfilenm, outfilenm, valid_chars='SE19 ')

    annotations.start()

    print('Ready...')
    mychar = None
    while mychar != 'q':
        mychar = getch()
        annotations.add(mychar)

    annotations.stop()


if __name__ == '__main__':
    main()

# ./annotate.py ../../data/16khz16bit/LR_141121_01_ch0.wav LR_141121_01.txt
