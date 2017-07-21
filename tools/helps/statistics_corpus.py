__all__ = ['read_songs']

import re

def read_songs(f):
    delimiters = ",", "-", "(", ")", " ", "\n", "?", ".", "<", ">", "\"", "!", ";", ":", "@", "#"
    regexPattern = '|'.join(map(re.escape, delimiters))

    listwords = {}
    countwords = 0
    countlines = 0
    fi = open(f, 'r')
    for line in fi:
        countlines += 1
        words = re.split(regexPattern, line)
        for word in words:
            word = word.lower()
            if word in listwords:
                listwords[word] += 1
            else:
                listwords[word] = 1
                countwords += 1
    
    listwords = listwords.items()
    listwords = sorted(listwords, key=lambda word: word[1], reverse=True)
    listwords_str = ""
    for id in range(len(listwords)):
        listwords_str = listwords_str + listwords[id][0] + " , " + str(listwords[id][1]) + "\n"

    return listwords_str, countwords, countlines
