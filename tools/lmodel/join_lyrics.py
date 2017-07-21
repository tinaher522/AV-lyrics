#!/usr/bin/env python
"""join_lyrics.py

Tool to download lyrics text from wikia website

Usage:
  join_lyrics.py <lyrics_origin_route> <collection_out> <artistsong_list> [-r=<repetitions>] 
  join_lyrics.py --help

Options:
  <lyrics_origin_route>         Route of folder that content all the lyrics
  <collection_out>              Output file with all the lyrics
  <artistsong_list>             List of Artist-Song pair. This list is used in order to exclude its from the unification
  -r=<repetition>               Maximus number of sentence repetition in a song [default: 4]
  --help                        print this help screen

"""

import docopt
import os
import re

def joining_lyric(lyric_path, repetition, artist_song, songs):
    collection_lyrics = []
    by_procesed = []
    by_annotated = []
    by_cover = []
    procesed_songs = []
    for root, dirs, files in os.walk(lyric_path, topdown=True):
        for fil in files:
            fil_clean = re.sub(r'\_\(.*?\)', '', fil).upper()
            if fil_clean not in artist_song:
                if fil_clean.split('-')[1][:-4] not in songs:
                    if fil_clean.split('-')[1][:-4] not in procesed_songs:
                        procesed_songs.append(fil_clean.split('-')[1][:-4].upper())
                        with open(root + '/' + fil) as f:
                            sentences = {}
                            for index, line in enumerate(f):
                                if line != '\n' and '</song>' not in line and '<song' not in line:
                                                                            
                                    # Clean repeated sentences in a song
                                    if line in sentences:
                                        if sentences[line] < repetition:
                                            sentences[line] += 1
                                            collection_lyrics.append(line)
                                    else:
                                        sentences[line] = 1
                                        collection_lyrics.append(line)
                    else:
                        by_procesed.append(fil)
                else:
                    by_cover.append(fil)
            else:
                by_annotated.append(fil)
        
    #print "By procesed",len(by_procesed)
    #print "By cover", len(by_cover)  
    #print "By annotatde", len(by_annotated)  
    #print by_procesed       
    return collection_lyrics
    

def get_artistsonglist(artistsong_list):
    artSong = []
    songs = []
    with open(artistsong_list) as f:
        for line in f:
            line = line.replace(',' , '-').replace(' ','_').replace('\n','')
            artSong.append((line + '.txt').upper())
            line = line.split('-')[1]
            songs.append(line.upper())
    return artSong, songs


def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    lyric_path = arguments['<lyrics_origin_route>']
    out_file = arguments['<collection_out>']
    artistsong_list = arguments['<artistsong_list>']
    repetition = int(arguments['-r'])

    artist_song, songs = get_artistsonglist(artistsong_list)
    collection_lyrics = joining_lyric(lyric_path, repetition, artist_song, songs)
    
      
    with open(out_file, 'w') as f:
        f.write("".join(collection_lyrics))
    
    #listwords, countwords, countlines, counttotalwords = gerardo.read_songs(out_file)
    #print countwords,countlines,counttotalwords  

if __name__ == '__main__':
    main()
