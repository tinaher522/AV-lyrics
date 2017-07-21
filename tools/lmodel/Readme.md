#Requirements

Before run any of this tools, the database files must be created.

#Work flow

1. Download Artist Discography **down_lyrics.py**
2. Collate each track into *collection* file **join_lyrics.py**
3. Lexify the collaction lyrics **lexify_lyrics.py**
4. Create 5K vocabulary **create_vocabulary.py**

#Language Model Tools

##down_lyrics.py

Download the lyrics discography of a list of artist. The source of the lyrics is lyrics.wikia.com 

Used as:
*down_lyrics.py database/csv_extracted/Artist_Song.txt lmodel/dictionary/base/*

##join_lyrics.py

Collate all the lyrics downloded using tool (1) into one file

Used as:
*join_lyrics.py lmodel/dictionary/base lmodel/dictionary/collection.txt*

##lexify_lyrics.py

Analize the content of the lyrics, normalize it and compare words with lexicon.

Used as:
*lexify_lyrics.py dictionary/collection.txt lexicon/cmudict_SPHINX_40 lyrics_out.txt oov_words.txt*

##create_vocabulary.py

Generate the 5K words vocabulary. Output is the lexicon.txt file.

Used as:
*create_vocabulary.py annotation/lyrics/lyrics lmodel/lyrics_out.txt lmodel/lexicon/cmudict_SPHINX_40 --output lmodel/5K_lexicon.txt --words=5000*



