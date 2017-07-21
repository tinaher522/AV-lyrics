#!/usr/bin/env python
"""down_lyrics.py

Tool to download lyrics text from wikia website

Usage:
  down_lyrics.py <artist_list> <outroute>
  down_lyrics.py --help

Options:
  <artist_list>  Name of the file with Artist list
  <outroute>     Name of directory for output files
  --help         print this help screen

"""

import docopt
from helps.wikia import *
import helps as gerardo
import time

def download_lyric(artist_list, outroute):
    start_time = time.time()
    """Down Discography from each artist."""
    artists = []
    with open(artist_list) as f:
        for index, line in enumerate(f):
            line = line.replace('\n','').split(",")[0]
            if not line in artists:
                artists.append(line.replace('\n',''))
    artists =  sorted(artists)

    songs = set()

    artists_list = []
 
    for artist in artists:
        artist = artist.replace(" " , "_")
        print "\nScraping Artist",str(artist)
        
        route = outroute  + artist.replace('/','') + "/"
        gerardo.ensure_dir(route)
        
        artists_list.append(artist)
        albums = PyLyrics.getAlbums(singer=artist)
        
        if albums is not None:

            countcurrentalbum = 0
            for album in albums:  # Select album based on Index
                tracks = PyLyrics.getTracks(album)
                for track in tracks:
                    tname = track.name.replace("/" , "-").replace(" ", "_")
                    if artist + "-" + tname not in songs:
                        songs.add( artist + "-" + tname )
                        
                        lyrics_track = track.getLyrics()
                        if lyrics_track is not None:
                            content ='<song artist="' + artist + '" title="'+ tname +'">\n'
                            content = content + lyrics_track
                            content = content +"\n</song>"
                            countcurrentalbum += 1
                            content = content.replace('\n\n', '\n')
                            gerardo.save_file(route + artist.replace('/','') + "-" + tname + ".txt" , content)
            print "\t", countcurrentalbum, "songs"

    f.close()
    
    #gerardo.save_file(outroute + "artist", "\n".join(artists_list))
    #gerardo.save_file(outroute + "song", "\n".join(songs))									

    print "\nEnd capturing lyrics"
    print "Total time : %.2f minutes" % ((time.time() - start_time) / 60)


def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    artist_list = arguments['<artist_list>']
    outroute = arguments['<outroute>']


    download_lyric(artist_list, outroute)

if __name__ == '__main__':
    main()
