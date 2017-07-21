#!/usr/bin/env python
"""create-database.py

Tool to generate the files database.
The <artist_list> list must be align with <cover_artist> list.

Description of files:
<artist_list>       must have Artist_Name , Track_Name
<cover_artist>      must contain Gender id (M, F) , Cover_Artist_Name 

Files must be contain same number of lines.
The content of <artist_list>[x] must be related with content of <cover_artist>[x]

Usage:
  create_database.py  <artist_list> <cover_artist> <link_list> <outroute>
  create_database.py  --help

Options:
  <artist_list>     Name of the file that contain the artist and song list.
  <cover_artist>    Name of the file that contain the gender and the name 
                    of the Cover artist
  <link_list>       Name of the file that contain the list of links to videos.
  <outroute>        Name of directory for output files      
  --help            Print this help screen
"""

import docopt

from lyrics.tools import helps


def gen_database(artist_list, cover_artist, link_list, outroute):
    print "Creating database..."    

    artists = []
    tracks = []
    with open(artist_list) as f:
        for index, line in enumerate(f):
            artists.append(line.replace('\n','').split(",")[0].replace('\n','').lstrip().rstrip().title())
            tracks.append(line.replace('\n','').split(",")[1].replace('\n','').lstrip().rstrip().title())
    
    cartists = []
    gender = []
    instrument = []
    channel = []
    with open(cover_artist) as f:
        for index, line in enumerate(f):
            gender.append(line.replace('\n','').split(",")[0].replace('\n','').lstrip().rstrip().title())
            cartists.append(line.replace('\n','').split(",")[1].replace('\n','').lstrip().rstrip().title())
            instrument.append(line.replace('\n','').split(",")[2].replace('\n','').lstrip().rstrip().lower())
            channel.append(line.replace('\n','').split(",")[3].replace('\n','').lstrip().rstrip())

    linklist = []
    with open(link_list) as f:
        for index, line in enumerate(f):
            linklist.append(line.replace('\n','').split(",")[0].replace('\n','').lstrip().rstrip())
    
    cartists, cartist_id = helps.gen_id_list_unique(cartists, digits=3, concatenate=0)
    artist, artists_id = helps.gen_id_list_unique(artists, tracks, digits=3, concatenate=0, concatenator=" - ")
    
    # Clean folder before new files   
    #shutil.rmtree(outroute)

    # Save Cover Artist
    database = outroute + "id_cover_artist.txt"
    helps.ensure_dir(database)
    f = open(database, 'wab')
    for i in range(len(cartists)):
        f.write(gender[i]+str(cartist_id[i])+","+cartists[i]+","+channel[i]+"\n")
    f.close
    print "File 'id_cover_artist' created"
    
    # Save Original Artist + Track
    database = outroute + "id_artist_song.txt"
    helps.ensure_dir(database)
    f = open(database, 'wab')
    for i in range(len(artist)):
        f.write(artists_id[i] +","+ artist[i]+"\n")
    f.close
    print "File 'id_artist_song' created"
    
    # Save ID Base of Covers
    for i in range(len(artist)):
        database = outroute + "covers"
        helps.ensure_dir(database)
        try:
            f = open(database, 'ab')
        except ValueError:
            f = open(database, 'wab')
        if instrument[i] == "guitar":
            f.write(str(gender[i])+str(cartist_id[i]) + "_" + str(artists_id[i]) + "_01_0101," + str(linklist[i]) + "," + str(cartists[i]) + "," + str(artist[i]) + "," + instrument[i] +",original,original\n")
        elif instrument[i] == "piano":
            f.write(str(gender[i])+str(cartist_id[i]) + "_" + str(artists_id[i]) + "_02_0101," + str(linklist[i]) + "," + str(cartists[i]) + "," + str(artist[i]) + "," + instrument[i] +",original,original\n")
        f.close
        if instrument[i] == "guitar":
            database = outroute + "covers_" + instrument[i] + ".txt"
            helps.ensure_dir(database)
            try:
                f = open(database, 'ab')
            except ValueError:
                f = open(database, 'wab')
            f.write(str(gender[i])+str(cartist_id[i]) + "_" + str(artists_id[i]) + "_01_0101," + str(linklist[i]) + "," + str(cartists[i]) + "," + str(artist[i]) + "," + instrument[i] +",original,original\n")
            f.close
        elif instrument[i] == "piano":
            database = outroute + "covers_" + instrument[i] + ".txt"
            helps.ensure_dir(database)
            try:
                f = open(database, 'ab')
            except ValueError:
                f = open(database, 'wab')
            f.write(str(gender[i])+str(cartist_id[i]) + "_" + str(artists_id[i]) + "_02_0101," + str(linklist[i]) + "," + str(cartists[i]) + "," + str(artist[i]) + "," + instrument[i] +",original,original\n")
            f.close
        else:
            print str(cartist_id[i]) + "_" + str(artists_id[i]) + "_02_0101," + str(linklist[i]) + "," + str(cartists[i]) + "," + str(artist[i]) + "," + instrument[i] 
    
    print "File 'covers' created"
    print "Database created."  


def main():
    """Main method called from commandline."""
    arguments = docopt.docopt(__doc__)
    artist_list = arguments['<artist_list>']
    cover_list = arguments['<cover_artist>']
    link_list = arguments['<link_list>']
    outroute = arguments['<outroute>']
    gen_database(artist_list, cover_list, link_list, outroute)

if __name__ == '__main__':
    main()