# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:47:51 2016

@author: gerardo
"""

import librosa
import os
import subprocess

audio_route = '/home/gerardo/ARS-Music/wav/16k'
for root, dirs, files in os.walk(audio_route, topdown=True):
    for fil in files:
        if ".wav" in fil:

            audiofile = root + "/" + fil
            # audioout =  '/home/gerardo/Desktop/a.wav'

            y, sr = librosa.load(audiofile)
            onset_env = librosa.onset.onset_strength(y, sr=sr)
            tempo = librosa.beat.estimate_tempo(onset_env, sr=sr)

            print fil, tempo

# targetbeat = 75
#
# subprocess.call(['sox', '-G', '-v', '0.99', audiofile, audioout ,  'tempo', str(targetbeat/tempo)])
#
# y2, sr2 = librosa.load(audioout)
# onset_env2 = librosa.onset.onset_strength(y2, sr=sr2)
# tempo2 = librosa.beat.estimate_tempo(onset_env2, sr=sr2)


#print tempo2