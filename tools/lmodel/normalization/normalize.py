__all__ = ['normalize']
"""
Created on Fri Jun  3 21:58:54 2016

@author: gerardo
"""

import inflect

def number2word(number):
    p = inflect.engine()
    return p.number_to_words(number, group=2).replace("," , "").replace("-", " ")

def normalize(text):
    text_norm = ''
    text = text.split(' ')
    for word in text:
        if word.isdigit():
            word = number2word(word)
        text_norm += word + " "
    
    print text_norm.strip()


def main():
    text = "We both know we ain't kids no 99 more"
    normalize(text)

if __name__ == '__main__':
    main()