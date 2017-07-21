__all__ = ['ensure_dir', 'save_file', 'append_file']

import os

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def save_file(fi, content):
    ensure_dir(fi)
    f = open(fi, 'wb')
    f.write(content)
    f.close()


def append_file(fi, content):
    f = open(fi, 'ab')
    f.write(content)
    f.close()

