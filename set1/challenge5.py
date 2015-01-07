#!/usr/bin/env python
'''Set 1 Challenge 5'''


from __future__ import division

from binascii import hexlify
from challenge2 import xor_buffers


def repeating_xor_encrypt(plaintext, key):
    '''Encrypt a plaintext using repeating-key XOR'''
    repeats = len(plaintext) // len(key)
    extended_key = '%s%s' % (key * repeats, key[0:len(plaintext) % len(key)])
    return xor_buffers(plaintext, extended_key)


def main():
    key = 'ICE'
    plaintext = '''Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal'''
    print hexlify(repeating_xor_encrypt(plaintext, key))


if __name__ == '__main__':
    main()
