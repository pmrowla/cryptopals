#!/usr/bin/env python
'''Set 1 Challenge 1'''

from base64 import b64encode
from binascii import unhexlify


def hex_to_b64(hex):
    '''Convert a hex string to a base64 encoded string'''
    # cheating with standard library functions
    return b64encode(unhexlify(hex))


def main():
    hex_str = \
        '49276d206b696c6c696e6720796f757220627261696e206c696b' \
        '65206120706f69736f6e6f7573206d757368726f6f6d'
    print hex_to_b64(hex_str)


if __name__ == '__main__':
    main()
