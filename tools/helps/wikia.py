###################################################
# This file is a modification of library PyLyrics
# created by geekpradd.
#
# The original project can be found in:
# https://github.com/geekpradd/PyLyrics
#
# All the credits all from geekpradd
#
###################################################


import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import sys, codecs, json
import sys
import urllib

reload(sys)
sys.setdefaultencoding('utf8')


class Track(object):
    def __init__(self, trackName, album, artist):
        self.name = trackName
        self.album = album
        self.artist = artist

    def __repr__(self):
        return self.name.encode('utf-8')

    def link(self):
        return 'http://lyrics.wikia.com/{0}:{1}'.format(self.artist.replace(' ', '-'), self.name.replace(' ', '-'))

    def getLyrics(self):
        return PyLyrics.getLyrics(self.artist, self.name)


class Artist(object):
    def __init__(self, name):
        self.name = name

    def getAlbums(self):
        return PyLyrics.getAlbums(self.name)

    def __repr__(self):
        return self.name.encode('utf-8')


class Album(object):
    def __init__(self, name, link, singer):
        self.year = name.split(' ')[-1]
        self.name = name.replace(self.year, ' ').rstrip()
        self.url = link
        self.singer = singer

    def link(self):
        return self.url

    def __repr__(self):
        if sys.version_info[0] == 2:
            return self.name.encode('utf-8', 'replace')
        return self.name

    def artist(self):
        return self.singer

    def tracks(self):
        return PyLyrics.getTracks(self)


class PyLyrics:
    @staticmethod
    def getAlbums(singer):
        singer = singer.replace(' ', '_')
        s = BeautifulSoup(requests.get('http://lyrics.wikia.com/wiki/{0}'.format(singer)).text ,"lxml")
        spans = s.findAll('span', {'class': 'mw-headline'})

        als = []

        for tag in spans:
            try:
                a = tag.findAll('a')[0]
                als.append(Album(a.text, 'http://lyrics.wikia.com' + a['href'], singer))
            except:
                pass

        if als == []:
            #raise ValueError("Unknown Artist Name given")
            return None
        return als

    @staticmethod
    def getTracks(album):

        url = "http://lyrics.wikia.com/api.php?action=lyrics&artist={0}&fmt=xml".format(
            urllib.quote_plus(album.artist()))
        # url = "http://lyrics.wikia.com/api.php?artist={0}&fmt=xml".format(album.artist())
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        for al in soup.find_all('album'):
            currentAlbum = None
            if al.text.lower().strip() == album.name.strip().lower():
                currentAlbum = al
                break
        songs = []
        if not currentAlbum is None:
            songs = [Track(song.text, album, album.artist()) for song in currentAlbum.findNext('songs').findAll('item')]
        return songs

    @staticmethod
    def getLyrics(singer, song):
        # Replace spaces with _
        singer = singer.replace(' ', '_')
        song = song.replace(' ', '_')
        # urlSong = 'http://lyrics.wikia.com/api.php?action=lyrics&artist=' + singer + \
        #		  '&song=' + song  +'&fmt=xml&func=getSong'
        # r = requests.get(urlSong.format(singer,song))
        r = requests.get('http://lyrics.wikia.com/{0}:{1}'.format(urllib.quote_plus(singer.encode('utf8')), urllib.quote_plus(song.encode('utf8'))))
        s = BeautifulSoup(r.text, "lxml")
        # Get main lyrics holder
        lyrics = s.find("div", {'class': 'lyricbox'})
        if lyrics is None:
            # raise ValueError("Song or Singer does not exist or the API does not have Lyrics")
            #print "Song :" + song + " or Singer: " + singer + " does not exist or the API does not have Lyrics"
            return None
        # Remove Scripts
        [s.extract() for s in lyrics('script')]

        # Remove Comments
        comments = lyrics.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]

        # Remove unecessary tags
        for tag in ['div', 'i', 'b', 'a', 'span', 'img']:
            for match in lyrics.findAll(tag):
                match.replaceWithChildren()
        # Get output as a string and remove non unicode characters and replace <br> with newlines
        output = str(lyrics).encode('utf-8', errors='replace')[22:-6:].decode("utf8").replace('\n', '').replace('<br/>',
                                                                                                                '\n')
        try:
            return output
        except:
            return output.encode('utf-8')


def main():
    albums = PyLyrics.getAlbums('OneRepublic')
    print (albums)
    tracks = PyLyrics.getTracks(albums[-1])
    print (tracks[7].getLyrics())


if __name__ == '__main__':
    main()
