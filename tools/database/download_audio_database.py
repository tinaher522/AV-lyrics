#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""download_audio_database.py

Download videos from YouTube and keep only the audio stream.

Usage:
  download_audio_database.py  <batch_file> <output_dir>
  download_audio_database.py  --help

Options:
  <batch_file>   Batch file with the list of video's URL
  <output_dir>   Directory where the audio will be save it
  --help         print this help screen

"""

import docopt
import subprocess
import progress



def download_videos(batch_file, output_dir):
    with open(batch_file) as f:
        for index, line in enumerate(f):
            autonumber = "0" * (3 - len(str(index + 1))) + str(index + 1)
            subprocess.call(['youtube-dl', line, '--output', output_dir + "/" +
            autonumber + '|%(uploader)s|%(uploader_id)s|%(title)s.%(ext)s', '--extract-audio'
            , '--audio-format', 'wav', '--audio-quality', '0'
            , '--prefer-ffmpeg', '--autonumber-size',  '3', '--quiet' ])
            progress.progress(index+1, 240, status='Download Data')
            
def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    batch_file = arguments['<batch_file>']
    output_dir = arguments['<output_dir>']
    download_videos(batch_file, output_dir)


if __name__ == '__main__':
    main()

# youtube-dl --batch-file $batch_file --output  \
#	"wav/wav_source/%(autonumber)s|%(uploader)s|%(uploader_id)s|%(title)s.%(ext)s" \
#	--extract-audio --audio-format "wav" --audio-quality 0 --prefer-ffmpeg \
#	--autonumber-size 3 --no-progress || exit 1