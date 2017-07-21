#Work flow

1. Annotate using **annotate.py**
2. Produce utterance level json file **segment.py**
3. Turn lyrics into json **jsonify_lyric.py**
4. Add lyrics to main json **add_lyrics.py**
5. Refine annotations using **refine.py**
6. Extract utterance segments **extract.py**
7. Generate the text file of song **utterance_sentences.py** 
8. Integrate tools 2 to 6 into **unify_annotation.py**


#Song data preparation tools

## 1. annotate.py

Interactive tool that allows to play an unsegmented audio and manually record the start and end points of each utterances. The output is a raw annotation file in a json format.

Used as :

*./annotate.py M001_001_01_0101.wav annotation/annotate/M001_001_01_0101.json*

## 2. segment.py

Takes a raw annotation file in a json file and produces an utterance level segmentation json file.

Used as :

*./segment.py annotation/annotate/M001_001_01_0101.json annotation/segments/M001_001_01_0101.json*

## 3. jsonify_lyric.py

Take the lyric file and produce a json file with it.
It is mandatory that the lines in the lyrics file match with the sentences in the segments file. In order to do this, it recomended that before to do the segmentation of the wavfile prepare this file with the actual lyrics sentences. It is not necessary to analize the singed words in this stage, only match the sentences and later will be refine the words of each sentence.

Used as :

*./jsonify_lyric.py annotation/lyrics/lyrics/chk01/M001_001_01_0101.lyrics annotation/lyrics/json/M001_001_01_0101.lyrics.json*


## 4. add_lyrics.py

This tool merge the segment and the lyrics json files.

Used as :

*./add_lyrics.py annotation/segments/M001_001_01_0101.json annotation/lyrics/json/M001_001_01_0101.lyrics.json annotation/json_lyrics/M001_001_01_0101.json*

## 5. refine.py

This tool allows to refine the start and end point of each sentences. Also allows to change and refina the exact word that the singer said. It is expected that as the database are covers versions the singer do not sing the exact words in each sentences of the original lyrics. Moreover, it is also expected that the cover do not sing the whole song but, only a fraction of the song.

Used as :

*./refine.py annotation/json_lyrics/M001_001_01_0101.json wav/16k/M/*


## 6. extract.py

Using the refined json lyrics from above, takes the undivided audio and extracts the individual utterance wav files.

Used as :

*./extract.py annotation/json_lyrics/M001_001_01_0101.json wav/16k/M/ wav/wav_segments/M/M001/*

## 7. utterance_sentences.py

This tool takes the json lyrics file and produce the kaldi's format *text* file of the song. 

Used as :

*./utterance_sentences.py M001_001_01_0101 annotation/*


## 8. unify_annotation.py

One of the objective that all the names are similars is because allows to unify several steps into one process calling the functions of each tool. This tool group tools 2 to 7 automatically waiting in the refine process and ends with the extraction. Before run this tool the lyric file must be produced and the annotate tool must be ran. 

Used as :

*./unify_annotation.py . M001_001_01_0101 chk01*

