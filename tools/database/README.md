#Requirements

Before run any of this tools, the file */database/videolist.csv* must be generated manually.

#Work flow

1. Transform videolist file into several necesary files **transform_csv.py**
2. Create ID files for the DB **create_database.py**
3. Download Audio Database **download_audio_database.py**
4. Create chunk files for each group of music **create_chunk.py**
5. Create wav files with the proper ID **create_wav_id.py**

#Database Tools

## 1. transform_csv.py

Tool that take file */database/videolist.csv* and produce the files *Video_Links.txt*, *Artist_Song.txt*, *Cover_Artist.txt* and the file *Extracted_Files.md*.

The file Video_Links.txt is the batch file used with youtube-dl for downloading the audios.
The files Artist_Song.txt and Cover_Artist.txt are necessary for generate the Artist-Song pair and Cover Artis's IDs.
The file Extracted_Files.md is an explenation of the extracted files.

Used as:
*transform_csv.py database/videolist.csv database/csv_extracted*

## 2. create_database.py

Tool that create the files *Artist_Song.txt*, *Cover_Artist.txt* and *Video_Links.txt*
Produce several files with unique ids for *Artist_Song* and *Cover_Artist*

File *id_artist_song.txt* have unique id for Artist-Song pair
File *id_cover_artist.txt* have unique id for Cover Artist
File cover.txt have list of the songs with their proper unique id
Files cover_<instrument>.txt have the list of songs per instruments with their unique IDs

Used as:
*create_database.py database/csv_extracted/Artist_Song.txt database/csv_extracted/Cover_Artist.txt database/csv_extracted/Video_Links.txt database/id_files/*

## 3. download_audio_database.py

Tool that download the videos and extract the audio.
This tool only save the audio and not the video

Used as:
*download_audio_database.py database/csv_extracted/Video_Links.txt wav/wav_source/*

## 4. create_chunk.py

This tool recieve the *covers_<instrument>.txt* and assign a chunk to each song.
The output file is *covers_chunk_<instrument>.txt* with their chunk division.

The chunks rules are :
1. Each **COVER ARTIST** can have more one or more different songs.
2. Each **COVER ARTIST** songs must be together in only one chunk.
3. Each **ARTIST-SONG** can be interpreted by one or more **COVER-ARTIST**
4. Each **ARTIST-SONG** interpretations must be together only in one chunk.

Used as:
*create_chunk.py database/id_files/covers_guitar.txt database/id_files/ --chunksize=20 --firstchunk=1*

## 5. create_wav_id.py

This tool use the IDS in step 2 and the audio files downloaded by step 3 and generate a 16K mono version of the wav files. This files are saved with code name.

Used as:
*ls wav/wav_source/ > video_source_name.txt*
*create_wav_id.py wav/wav_source/ video_source_name.txt wav/16k/ covers.txt*


