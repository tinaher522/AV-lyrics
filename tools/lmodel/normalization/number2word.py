__all__ = ['number2word']
"""
Created on Fri Jun  3 21:58:54 2016

@author: gerardo
"""

import inflect


def number2word(number):
    p = inflect.engine()
    return p.number_to_words(number, group=2).replace("," , "").replace("-", " ")


def main():
    number = 1995
    print number2word(number)

if __name__ == '__main__':
    main()